//
//  SuperTuxKart - a fun racing game with go-kart
//  Copyright (C) 2006-2015 SuperTuxKart-Team
//
//  This program is free software; you can redistribute it and/or
//  modify it under the terms of the GNU General Public License
//  as published by the Free Software Foundation; either version 3
//  of the License, or (at your option) any later version.
//
//  This program is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details.
//
//  You should have received a copy of the GNU General Public License
//  along with this program; if not, write to the Free Software
//  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

#include "karts/kart_properties.hpp"

// #include "addons/addon.hpp"
#include "config/stk_config.hpp"
#include "graphics/central_settings.hpp"
#include "graphics/material_manager.hpp"
#include "graphics/shader_files_manager.hpp"
#include "graphics/stk_tex_manager.hpp"
#include "graphics/sp/sp_shader_manager.hpp"
#include "graphics/sp/sp_texture_manager.hpp"
#include "io/file_manager.hpp"
#include "karts/cached_characteristic.hpp"
#include "karts/combined_characteristic.hpp"
#include "karts/controller/ai_properties.hpp"
#include "karts/kart_model.hpp"
#include "karts/kart_properties_manager.hpp"
#include "karts/xml_characteristic.hpp"
#include "modes/world.hpp"
#include "io/xml_node.hpp"
#include "utils/constants.hpp"
#include "utils/log.hpp"
#include "utils/string_utils.hpp"
#include "utils/translation.hpp"

#include <iostream>
#include <stdexcept>
#include <string>


float KartProperties::UNDEFINED = -99.9f;

std::string KartProperties::getPerPlayerDifficultyAsString(PerPlayerDifficulty d)
{
    switch(d)
    {
    case PLAYER_DIFFICULTY_NORMAL:   return "normal";   break;
    case PLAYER_DIFFICULTY_HANDICAP: return "handicap"; break;
    default:  assert(false);
    }
    return "";
}

/** The constructor initialises all values with invalid values. It can later
 *  then be checked (for STKConfig) that all values are indeed defined.
 *  Otherwise the defaults are taken from STKConfig (and since they are all
 *  defined, it is guaranteed that each kart has well defined physics values).
 */
KartProperties::KartProperties(const std::string &filename)
{
    m_is_addon = false;
    m_icon_material = NULL;
    m_minimap_icon  = NULL;
    m_name          = "NONAME";
    m_ident         = "NONAME";
    m_icon_file     = "";
    m_shadow_file   = "";
    m_shadow_scale    = 1.0f;
    m_shadow_x_offset = 0.0f;
    m_shadow_z_offset = 0.0f;

    m_groups.clear();

    // Set all other values to undefined, so that it can later be tested
    // if everything is defined properly.
    m_wheel_base = m_friction_slip = m_collision_terrain_impulse =
        m_collision_impulse = m_collision_impulse_time =
        m_max_lean = m_lean_speed = m_physical_wheel_position = UNDEFINED;

    m_terrain_impulse_type       = IMPULSE_NONE;
    m_gravity_center_shift       = Vec3(UNDEFINED);
    m_bevel_factor               = Vec3(UNDEFINED);
    m_version                    = 0;
    m_color                      = video::SColor(255, 0, 0, 0);
    m_shape                      = 32;  // close enough to a circle.
    m_nitro_min_consumption      = 64;
    // The default constructor for stk_config uses filename=""
    if (filename != "")
    {
        load(filename, "kart");
    }
    else
    {
        for (unsigned int i = 0; i < RaceManager::DIFFICULTY_COUNT; i++)
        {
            m_ai_properties[i] =
                std::make_shared<AIProperties>((RaceManager::Difficulty) i);
        }
    }
}   // KartProperties

//-----------------------------------------------------------------------------
/** Destructor, dereferences the kart model. */
KartProperties::~KartProperties()
{
#ifndef SERVER_ONLY
    if (CVS->isGLSL() && m_kart_model.use_count() == 1)
    {
        m_kart_model = nullptr;
        SP::SPShaderManager::get()->removeUnusedShaders();
        ShaderFilesManager::getInstance()->removeUnusedShaderFiles();
        SP::SPTextureManager::get()->removeUnusedTextures();
    }
#endif
}   // ~KartProperties

//-----------------------------------------------------------------------------
/** Copies this KartProperties to another one. Important: if you add any
 *  pointers to kart_properties, the data structure they are pointing to
 *  need to be copied here explicitely!
 *  The AIProperties won't get cloned here as they don't differ for each player.
 *  To clone this object for another kart use the copyFrom method.
 *  \param source The source kart properties from which to copy this objects'
 *         values.
 */
void KartProperties::copyForPlayer(const KartProperties *source,
                                   PerPlayerDifficulty d)
{
    *this = *source;

    // After the memcpy any pointers will be shared.
    // So all pointer variables need to be separately allocated and assigned.
    if (source->m_characteristic)
    {
        // Remove the shared reference by creating a new pointer
        m_characteristic = std::make_shared<XmlCharacteristic>();
        m_characteristic->copyFrom(source->getCharacteristic());

        // Combine the characteristics for this object. We can't copy it because
        // this object has other pointers (to m_characteristic).
        combineCharacteristics(d);
    }
}   // copyForPlayer

//-----------------------------------------------------------------------------
/** Copies this KartProperties to another one. Important: if you add any
 *  pointers to kart_properties, the data structure they are pointing to
 *  need to be copied here explicitely!
 *  \param source The source kart properties from which to copy this objects'
 *         values.
 */
void KartProperties::copyFrom(const KartProperties *source)
{
    copyForPlayer(source);

    // Also copy the AIProperties because they can differ for each car
    // (but not for each player).
    for (unsigned int i = 0; i < RaceManager::DIFFICULTY_COUNT; i++)
    {
        m_ai_properties[i] =
            std::make_shared<AIProperties>((RaceManager::Difficulty) i);
        assert(m_ai_properties);
        *m_ai_properties[i] = *source->m_ai_properties[i];
    }
}   // copyFrom

//-----------------------------------------------------------------------------
/** Loads the kart properties from a file.
 *  \param filename Filename to load.
 *  \param node Name of the xml node to load the data from
 */
void KartProperties::load(const std::string &filename, const std::string &node)
{
    // Get the default values from STKConfig. This will also allocate any
    // pointers used in KartProperties

    const XMLNode* root = new XMLNode(filename);
    std::string kart_type;

    if (root->get("type", &kart_type))
    {
        // Handle the case that kart_type might be incorrect
        try
        {
            copyFrom(&stk_config->getKartProperties(kart_type));
        }
        catch (std::out_of_range &)
        {
            copyFrom(&stk_config->getDefaultKartProperties());
        }   // try .. catch
    }
    else
        copyFrom(&stk_config->getDefaultKartProperties());

    // m_kart_model must be initialised after assigning the default
    // values from stk_config (otherwise all kart_properties will
    // share the same KartModel
    m_kart_model = std::make_shared<KartModel>(/*is_master*/true);

    m_root  = StringUtils::getPath(filename)+"/";
    m_ident = StringUtils::getBasename(StringUtils::getPath(filename));

    try
    {
        if(!root || root->getName()!="kart")
        {
            std::ostringstream msg;
            msg << "Couldn't load kart properties '" << filename <<
                "': no kart node.";

            throw std::runtime_error(msg.str());
        }
        getAllData(root);
        m_characteristic = std::make_shared<XmlCharacteristic>(root);
        combineCharacteristics(PLAYER_DIFFICULTY_NORMAL);
    }
    catch(std::exception& err)
    {
        Log::error("[KartProperties]", "Error while parsing KartProperties '%s':",
                   filename.c_str());
        Log::error("[KartProperties]", "%s", err.what());
    }
    if(root) delete root;

    // Set a default group (that has to happen after init_default and load)
    if(m_groups.size()==0)
        m_groups.push_back(DEFAULT_GROUP_NAME);


    // Load material
    std::string materials_file = m_root+"materials.xml";
    std::string unique_id = StringUtils::insertValues("karts/%s", m_ident.c_str());
    file_manager->pushModelSearchPath(m_root);
    file_manager->pushTextureSearchPath(m_root, unique_id);
#ifndef SERVER_ONLY
    if (CVS->isGLSL())
    {
        SP::SPShaderManager::get()->loadSPShaders(m_root);
    }
#endif

    STKTexManager::getInstance()
        ->setTextureErrorMessage("Error while loading kart '%s':", m_name);

    // addShared makes sure that these textures/material infos stay in memory
    material_manager->addSharedMaterial(materials_file);

    m_icon_file = m_root+m_icon_file;

    // Make permanent is important, since otherwise icons can get deleted
    // (e.g. when freeing temp. materials from a track, the last icon
    //  would get deleted, too.
    m_icon_material = material_manager->getMaterial(m_icon_file,
                                                    /*is_full_path*/true,
                                                    /*make_permanent*/true,
                                                    /*complain_if_not_found*/true,
                                                    /*strip_path*/false);
    if (m_minimap_icon_file!="")
    {
        m_minimap_icon = STKTexManager::getInstance()
            ->getTexture(m_root+m_minimap_icon_file);
    }
    else
        m_minimap_icon = NULL;

    // Only load the model if the .kart file has the appropriate version,
    // otherwise warnings are printed.
    if (m_version >= 1)
    {
        const bool success = m_kart_model->loadModels(*this);
        if (!success)
        {
            file_manager->popTextureSearchPath();
            file_manager->popModelSearchPath();
            throw std::runtime_error("Cannot load kart models");
        }
    }

    if(m_gravity_center_shift.getX()==UNDEFINED)
    {
        m_gravity_center_shift.setX(0);
        // Default: center at the very bottom of the kart.
        // If the kart is 'too high', its height will be changed in
        // kart.cpp, the same adjustment needs to be made here.
        if (m_kart_model->getHeight() > m_kart_model->getLength()*0.6f)
            m_gravity_center_shift.setY(m_kart_model->getLength()*0.6f*0.5f);
        else
            m_gravity_center_shift.setY(m_kart_model->getHeight()*0.5f);

        m_gravity_center_shift.setZ(0);
    }

    // The longer the kart,the bigger its turn radius if using an identical
    // wheel base, exactly proportionally to its length.
    // The wheel base is used to compensate this
    // We divide by 1.425 to have a default turn radius which conforms
    // closely (+-0,1%) with the specifications in kart_characteristics.xml
    m_wheel_base = fabsf(m_kart_model->getLength()/1.425f);

    m_shadow_material = material_manager->getMaterialSPM(m_shadow_file, "",
        "alphablend");

    STKTexManager::getInstance()->unsetTextureErrorMessage();
    file_manager->popTextureSearchPath();
    file_manager->popModelSearchPath();

}   // load

// ----------------------------------------------------------------------------
/** Returns a pointer to the KartModel object.
 *  \param krt The KartRenderType, like default, red, blue or transparent.
 *  see the RenderInfo include for details
 */
KartModel* KartProperties::getKartModelCopy(std::shared_ptr<RenderInfo> ri) const
{
    return m_kart_model->makeCopy(ri);
}  // getKartModelCopy

// ----------------------------------------------------------------------------
/** Sets the name of a mesh to be used for this kart.
 *  \param hat_name Name of the mesh.
 */
void KartProperties::setHatMeshName(const std::string &hat_name)
{
    m_kart_model->setHatMeshName(hat_name);
}  // setHatMeshName

//-----------------------------------------------------------------------------
void KartProperties::combineCharacteristics(PerPlayerDifficulty difficulty)
{
    m_combined_characteristic = std::make_shared<CombinedCharacteristic>();
    m_combined_characteristic->addCharacteristic(kart_properties_manager->
        getBaseCharacteristic());
    m_combined_characteristic->addCharacteristic(kart_properties_manager->
        getDifficultyCharacteristic(race_manager->getDifficultyAsString(
            race_manager->getDifficulty())));

    // Try to get the kart type
    const AbstractCharacteristic *characteristic = kart_properties_manager->
        getKartTypeCharacteristic(m_kart_type, m_name);

    // Combine kart type
    m_combined_characteristic->addCharacteristic(characteristic);

    m_combined_characteristic->addCharacteristic(kart_properties_manager->
        getPlayerCharacteristic(getPerPlayerDifficultyAsString(difficulty)));

    m_combined_characteristic->addCharacteristic(m_characteristic.get());
    m_cached_characteristic = std::make_shared<CachedCharacteristic>
        (m_combined_characteristic.get());
}   // combineCharacteristics

//-----------------------------------------------------------------------------
/** Actually reads in the data from the xml file.
 *  \param root Root of the xml tree.
 */
void KartProperties::getAllData(const XMLNode * root)
{
    root->get("version",           &m_version);

    root->get("name",              &m_name             );

    root->get("icon-file",         &m_icon_file        );

    root->get("minimap-icon-file", &m_minimap_icon_file);

    root->get("shadow-file",       &m_shadow_file      );
    Vec3 c;
    root->get("rgb",               &c                  );
    m_color.set(255, (int)(255*c.getX()), (int)(255*c.getY()), (int)(255*c.getZ()));

    root->get("groups",            &m_groups           );
    root->get("type",              &m_kart_type        );

    if(const XMLNode *dimensions_node = root->getNode("center"))
        dimensions_node->get("gravity-shift", &m_gravity_center_shift);

    if(const XMLNode *ai_node = root->getNode("ai"))
    {
        const XMLNode *easy = ai_node->getNode("easy");
        m_ai_properties[RaceManager::DIFFICULTY_EASY]->load(easy);
        const XMLNode *medium = ai_node->getNode("medium");
        m_ai_properties[RaceManager::DIFFICULTY_MEDIUM]->load(medium);
        const XMLNode *hard = ai_node->getNode("hard");
        m_ai_properties[RaceManager::DIFFICULTY_HARD]->load(hard);
        const XMLNode *best = ai_node->getNode("best");
        m_ai_properties[RaceManager::DIFFICULTY_BEST]->load(best);
    }

    if(const XMLNode *friction_node = root->getNode("friction"))
        friction_node->get("slip", &m_friction_slip);

    if(const XMLNode *collision_node = root->getNode("collision"))
    {
        collision_node->get("impulse",         &m_collision_impulse        );
        collision_node->get("impulse-time",    &m_collision_impulse_time   );
        collision_node->get("terrain-impulse", &m_collision_terrain_impulse);
        collision_node->get("restitution",     &m_restitution              );
        collision_node->get("bevel-factor",    &m_bevel_factor             );
        collision_node->get("physical-wheel-position",&m_physical_wheel_position);
        std::string s;
        collision_node->get("impulse-type",    &s                          );
        s = StringUtils::toLowerCase(s);
        if(s=="none")
            m_terrain_impulse_type = IMPULSE_NONE;
        else if(s=="normal")
            m_terrain_impulse_type = IMPULSE_NORMAL;
        else if(s=="driveline")
            m_terrain_impulse_type = IMPULSE_TO_DRIVELINE;
        else
        {
            Log::fatal("[KartProperties]",
                       "Missing or incorrect value for impulse-type: '%s'.",
                       s.c_str());
        }
    }

    //TODO: wheel front right and wheel front left is not loaded, yet is
    //TODO: listed as an attribute in the xml file after wheel-radius
    //TODO: same goes for their rear equivalents

    if(m_kart_model)
        m_kart_model->loadInfo(*root);
}   // getAllData

// ----------------------------------------------------------------------------
/** Checks if all necessary physics values are indeed defines. This helps
 *  finding bugs early, e.g. missing default in stk_config.dat file.
 *  \param filename File from which the data was read (only used to print
 *                  meaningful error messages).
 */
void KartProperties::checkAllSet(const std::string &filename)
{
#define CHECK_NEG(  a,strA) if(a<=UNDEFINED) {                      \
        Log::fatal("KartProperties",                                \
                    "Missing default value for '%s' in '%s'.",    \
                    strA,filename.c_str());                \
    }

    CHECK_NEG(m_friction_slip,              "friction slip"                 );
    CHECK_NEG(m_collision_terrain_impulse,  "collision terrain-impulse"     );
    CHECK_NEG(m_collision_impulse,          "collision impulse"             );
    CHECK_NEG(m_collision_impulse_time,     "collision impulse-time"        );
    CHECK_NEG(m_physical_wheel_position,    "collision physical-wheel-position");

    if(m_restitution.size()<1)
        Log::fatal("KartProperties", "Missing restitution value.");

    for(unsigned int i=0; i<RaceManager::DIFFICULTY_COUNT; i++)
        m_ai_properties[i]->checkAllSet(filename);
}   // checkAllSet

// ----------------------------------------------------------------------------
bool KartProperties::operator<(const KartProperties &other) const
{
    return getName() < other.getName();
}  // operator<

// ----------------------------------------------------------------------------
const AbstractCharacteristic* KartProperties::getCharacteristic() const
{
    return m_characteristic.get();
}   // getCharacteristic

// ----------------------------------------------------------------------------
const AbstractCharacteristic* KartProperties::getCombinedCharacteristic() const
{
    return m_combined_characteristic.get();
}   // getCombinedCharacteristic

// ----------------------------------------------------------------------------
bool KartProperties::isInGroup(const std::string &group) const
{
    return std::find(m_groups.begin(), m_groups.end(), group) != m_groups.end();
}   // isInGroups

// ----------------------------------------------------------------------------
/** This function returns a weighted average of engine power divide by mass
 *  for use as a single number summing-up acceleration's efficiency,
 *  e.g. for use in kart selection. */
float KartProperties::getAccelerationEfficiency() const
{
    std::vector<float> gear_power_increase = m_combined_characteristic->getGearPowerIncrease();
    std::vector<float> gear_switch_ratio = m_combined_characteristic->getGearSwitchRatio();
    unsigned current_gear = 0;
    float sum = 0;
    float base_accel = m_combined_characteristic->getEnginePower()
                     / m_combined_characteristic->getMass();

    // We evaluate acceleration at increments of 0.01x max speed
    // up to 1,1x max speed.
    // Acceleration at low speeds is made to matter more
    for (unsigned int i = 1; i<=110; i++)
    {
        sum += gear_power_increase[current_gear] * base_accel * (150-i);
        if (i/100 >= gear_switch_ratio[current_gear] &&
            (current_gear+1 < gear_power_increase.size() ))
            current_gear++;
    }

    // 10395 is the sum of the (150-i) factors
    return (sum / 10395);
}   // getAccelerationEfficiency

// ----------------------------------------------------------------------------
/** Returns the name of this kart. */
core::stringw KartProperties::getName() const
{
    return _(m_name.c_str());
}   // getName

// ----------------------------------------------------------------------------
// Script-generated content generated by tools/create_kart_properties.py getter
// Please don't change the following tag. It will be automatically detected
// by the script and replace the contained content.
// To update the code, use tools/update_characteristics.py
/* <characteristics-start kpgetter> */
// ----------------------------------------------------------------------------
float KartProperties::getSuspensionStiffness() const
{
    return m_cached_characteristic->getSuspensionStiffness();
}  // getSuspensionStiffness

// ----------------------------------------------------------------------------
float KartProperties::getSuspensionRest() const
{
    return m_cached_characteristic->getSuspensionRest();
}  // getSuspensionRest

// ----------------------------------------------------------------------------
float KartProperties::getSuspensionTravel() const
{
    return m_cached_characteristic->getSuspensionTravel();
}  // getSuspensionTravel

// ----------------------------------------------------------------------------
bool KartProperties::getSuspensionExpSpringResponse() const
{
    return m_cached_characteristic->getSuspensionExpSpringResponse();
}  // getSuspensionExpSpringResponse

// ----------------------------------------------------------------------------
float KartProperties::getSuspensionMaxForce() const
{
    return m_cached_characteristic->getSuspensionMaxForce();
}  // getSuspensionMaxForce

// ----------------------------------------------------------------------------
float KartProperties::getStabilityRollInfluence() const
{
    return m_cached_characteristic->getStabilityRollInfluence();
}  // getStabilityRollInfluence

// ----------------------------------------------------------------------------
float KartProperties::getStabilityChassisLinearDamping() const
{
    return m_cached_characteristic->getStabilityChassisLinearDamping();
}  // getStabilityChassisLinearDamping

// ----------------------------------------------------------------------------
float KartProperties::getStabilityChassisAngularDamping() const
{
    return m_cached_characteristic->getStabilityChassisAngularDamping();
}  // getStabilityChassisAngularDamping

// ----------------------------------------------------------------------------
float KartProperties::getStabilityDownwardImpulseFactor() const
{
    return m_cached_characteristic->getStabilityDownwardImpulseFactor();
}  // getStabilityDownwardImpulseFactor

// ----------------------------------------------------------------------------
float KartProperties::getStabilityTrackConnectionAccel() const
{
    return m_cached_characteristic->getStabilityTrackConnectionAccel();
}  // getStabilityTrackConnectionAccel

// ----------------------------------------------------------------------------
std::vector<float> KartProperties::getStabilityAngularFactor() const
{
    return m_cached_characteristic->getStabilityAngularFactor();
}  // getStabilityAngularFactor

// ----------------------------------------------------------------------------
float KartProperties::getStabilitySmoothFlyingImpulse() const
{
    return m_cached_characteristic->getStabilitySmoothFlyingImpulse();
}  // getStabilitySmoothFlyingImpulse

// ----------------------------------------------------------------------------
InterpolationArray KartProperties::getTurnRadius() const
{
    return m_cached_characteristic->getTurnRadius();
}  // getTurnRadius

// ----------------------------------------------------------------------------
float KartProperties::getTurnTimeResetSteer() const
{
    return m_cached_characteristic->getTurnTimeResetSteer();
}  // getTurnTimeResetSteer

// ----------------------------------------------------------------------------
InterpolationArray KartProperties::getTurnTimeFullSteer() const
{
    return m_cached_characteristic->getTurnTimeFullSteer();
}  // getTurnTimeFullSteer

// ----------------------------------------------------------------------------
float KartProperties::getEnginePower() const
{
    return m_cached_characteristic->getEnginePower();
}  // getEnginePower

// ----------------------------------------------------------------------------
float KartProperties::getEngineMaxSpeed() const
{
    return m_cached_characteristic->getEngineMaxSpeed();
}  // getEngineMaxSpeed

// ----------------------------------------------------------------------------
float KartProperties::getEngineGenericMaxSpeed() const
{
    return m_cached_characteristic->getEngineGenericMaxSpeed();
}  // getEngineMaxSpeed

// ----------------------------------------------------------------------------
float KartProperties::getEngineBrakeFactor() const
{
    return m_cached_characteristic->getEngineBrakeFactor();
}  // getEngineBrakeFactor

// ----------------------------------------------------------------------------
float KartProperties::getEngineBrakeTimeIncrease() const
{
    return m_cached_characteristic->getEngineBrakeTimeIncrease();
}  // getEngineBrakeTimeIncrease

// ----------------------------------------------------------------------------
float KartProperties::getEngineMaxSpeedReverseRatio() const
{
    return m_cached_characteristic->getEngineMaxSpeedReverseRatio();
}  // getEngineMaxSpeedReverseRatio

// ----------------------------------------------------------------------------
std::vector<float> KartProperties::getGearSwitchRatio() const
{
    return m_cached_characteristic->getGearSwitchRatio();
}  // getGearSwitchRatio

// ----------------------------------------------------------------------------
std::vector<float> KartProperties::getGearPowerIncrease() const
{
    return m_cached_characteristic->getGearPowerIncrease();
}  // getGearPowerIncrease

// ----------------------------------------------------------------------------
float KartProperties::getMass() const
{
    return m_cached_characteristic->getMass();
}  // getMass

// ----------------------------------------------------------------------------
float KartProperties::getWheelsDampingRelaxation() const
{
    return m_cached_characteristic->getWheelsDampingRelaxation();
}  // getWheelsDampingRelaxation

// ----------------------------------------------------------------------------
float KartProperties::getWheelsDampingCompression() const
{
    return m_cached_characteristic->getWheelsDampingCompression();
}  // getWheelsDampingCompression

// ----------------------------------------------------------------------------
float KartProperties::getCameraDistance() const
{
    return m_cached_characteristic->getCameraDistance();
}  // getCameraDistance

// ----------------------------------------------------------------------------
float KartProperties::getCameraForwardUpAngle() const
{
    return m_cached_characteristic->getCameraForwardUpAngle();
}  // getCameraForwardUpAngle

// ----------------------------------------------------------------------------
float KartProperties::getCameraBackwardUpAngle() const
{
    return m_cached_characteristic->getCameraBackwardUpAngle();
}  // getCameraBackwardUpAngle

// ----------------------------------------------------------------------------
float KartProperties::getJumpAnimationTime() const
{
    return m_cached_characteristic->getJumpAnimationTime();
}  // getJumpAnimationTime

// ----------------------------------------------------------------------------
float KartProperties::getLeanMax() const
{
    return m_cached_characteristic->getLeanMax();
}  // getLeanMax

// ----------------------------------------------------------------------------
float KartProperties::getLeanSpeed() const
{
    return m_cached_characteristic->getLeanSpeed();
}  // getLeanSpeed

// ----------------------------------------------------------------------------
float KartProperties::getAnvilDuration() const
{
    return m_cached_characteristic->getAnvilDuration();
}  // getAnvilDuration

// ----------------------------------------------------------------------------
float KartProperties::getAnvilWeight() const
{
    return m_cached_characteristic->getAnvilWeight();
}  // getAnvilWeight

// ----------------------------------------------------------------------------
float KartProperties::getAnvilSpeedFactor() const
{
    return m_cached_characteristic->getAnvilSpeedFactor();
}  // getAnvilSpeedFactor

// ----------------------------------------------------------------------------
float KartProperties::getParachuteFriction() const
{
    return m_cached_characteristic->getParachuteFriction();
}  // getParachuteFriction

// ----------------------------------------------------------------------------
int KartProperties::getParachuteDuration() const
{
    return m_cached_characteristic->getParachuteDuration();
}  // getParachuteDuration

// ----------------------------------------------------------------------------
int KartProperties::getParachuteDurationOther() const
{
    return m_cached_characteristic->getParachuteDurationOther();
}  // getParachuteDurationOther

// ----------------------------------------------------------------------------
float KartProperties::getParachuteDurationRankMult() const
{
    return m_cached_characteristic->getParachuteDurationRankMult();
}  // getParachuteDurationRankMult

// ----------------------------------------------------------------------------
float KartProperties::getParachuteDurationSpeedMult() const
{
    return m_cached_characteristic->getParachuteDurationSpeedMult();
}  // getParachuteDurationSpeedMult

// ----------------------------------------------------------------------------
float KartProperties::getParachuteLboundFraction() const
{
    return m_cached_characteristic->getParachuteLboundFraction();
}  // getParachuteLboundFraction

// ----------------------------------------------------------------------------
float KartProperties::getParachuteUboundFraction() const
{
    return m_cached_characteristic->getParachuteUboundFraction();
}  // getParachuteUboundFraction

// ----------------------------------------------------------------------------
float KartProperties::getParachuteMaxSpeed() const
{
    return m_cached_characteristic->getParachuteMaxSpeed();
}  // getParachuteMaxSpeed

// ----------------------------------------------------------------------------
float KartProperties::getFrictionKartFriction() const
{
    return m_cached_characteristic->getFrictionKartFriction();
}  // getFrictionKartFriction

// ----------------------------------------------------------------------------
float KartProperties::getBubblegumDuration() const
{
    return m_cached_characteristic->getBubblegumDuration();
}  // getBubblegumDuration

// ----------------------------------------------------------------------------
float KartProperties::getBubblegumSpeedFraction() const
{
    return m_cached_characteristic->getBubblegumSpeedFraction();
}  // getBubblegumSpeedFraction

// ----------------------------------------------------------------------------
float KartProperties::getBubblegumTorque() const
{
    return m_cached_characteristic->getBubblegumTorque();
}  // getBubblegumTorque

// ----------------------------------------------------------------------------
int KartProperties::getBubblegumFadeInTicks() const
{
    return stk_config->time2Ticks(m_cached_characteristic
                                  ->getBubblegumFadeInTime());
}  // getBubblegumFadeInTime

// ----------------------------------------------------------------------------
float KartProperties::getBubblegumShieldDuration() const
{
    return m_cached_characteristic->getBubblegumShieldDuration();
}  // getBubblegumShieldDuration

// ----------------------------------------------------------------------------
float KartProperties::getZipperDuration() const
{
    return m_cached_characteristic->getZipperDuration();
}  // getZipperDuration

// ----------------------------------------------------------------------------
float KartProperties::getZipperForce() const
{
    return m_cached_characteristic->getZipperForce();
}  // getZipperForce

// ----------------------------------------------------------------------------
float KartProperties::getZipperSpeedGain() const
{
    return m_cached_characteristic->getZipperSpeedGain();
}  // getZipperSpeedGain

// ----------------------------------------------------------------------------
float KartProperties::getZipperMaxSpeedIncrease() const
{
    return m_cached_characteristic->getZipperMaxSpeedIncrease();
}  // getZipperMaxSpeedIncrease

// ----------------------------------------------------------------------------
float KartProperties::getZipperFadeOutTime() const
{
    return m_cached_characteristic->getZipperFadeOutTime();
}  // getZipperFadeOutTime

// ----------------------------------------------------------------------------
float KartProperties::getSwatterDuration() const
{
    return m_cached_characteristic->getSwatterDuration();
}  // getSwatterDuration

// ----------------------------------------------------------------------------
float KartProperties::getSwatterDistance() const
{
    return m_cached_characteristic->getSwatterDistance();
}  // getSwatterDistance

// ----------------------------------------------------------------------------
float KartProperties::getSwatterSquashDuration() const
{
    return m_cached_characteristic->getSwatterSquashDuration();
}  // getSwatterSquashDuration

// ----------------------------------------------------------------------------
float KartProperties::getSwatterSquashSlowdown() const
{
    return m_cached_characteristic->getSwatterSquashSlowdown();
}  // getSwatterSquashSlowdown

// ----------------------------------------------------------------------------
float KartProperties::getPlungerBandMaxLength() const
{
    return m_cached_characteristic->getPlungerBandMaxLength();
}  // getPlungerBandMaxLength

// ----------------------------------------------------------------------------
float KartProperties::getPlungerBandForce() const
{
    return m_cached_characteristic->getPlungerBandForce();
}  // getPlungerBandForce

// ----------------------------------------------------------------------------
float KartProperties::getPlungerBandDuration() const
{
    return m_cached_characteristic->getPlungerBandDuration();
}  // getPlungerBandDuration

// ----------------------------------------------------------------------------
float KartProperties::getPlungerBandSpeedIncrease() const
{
    return m_cached_characteristic->getPlungerBandSpeedIncrease();
}  // getPlungerBandSpeedIncrease

// ----------------------------------------------------------------------------
int KartProperties::getPlungerBandFadeOutTicks() const
{
    return stk_config->time2Ticks(m_cached_characteristic
                                   ->getPlungerBandFadeOutTime());
}  // getPlungerBandFadeOutTime

// ----------------------------------------------------------------------------
float KartProperties::getPlungerInFaceTime() const
{
    return m_cached_characteristic->getPlungerInFaceTime();
}  // getPlungerInFaceTime

// ----------------------------------------------------------------------------
std::vector<float> KartProperties::getStartupTime() const
{
    return m_cached_characteristic->getStartupTime();
}  // getStartupTime

// ----------------------------------------------------------------------------
std::vector<float> KartProperties::getStartupBoost() const
{
    return m_cached_characteristic->getStartupBoost();
}  // getStartupBoost

// ----------------------------------------------------------------------------
float KartProperties::getRescueDuration() const
{
    return m_cached_characteristic->getRescueDuration();
}  // getRescueDuration

// ----------------------------------------------------------------------------
float KartProperties::getRescueVertOffset() const
{
    return m_cached_characteristic->getRescueVertOffset();
}  // getRescueVertOffset

// ----------------------------------------------------------------------------
float KartProperties::getRescueHeight() const
{
    return m_cached_characteristic->getRescueHeight();
}  // getRescueHeight

// ----------------------------------------------------------------------------
float KartProperties::getExplosionDuration() const
{
    return m_cached_characteristic->getExplosionDuration();
}  // getExplosionDuration

// ----------------------------------------------------------------------------
float KartProperties::getExplosionRadius() const
{
    return m_cached_characteristic->getExplosionRadius();
}  // getExplosionRadius

// ----------------------------------------------------------------------------
float KartProperties::getExplosionInvulnerabilityTime() const
{
    return m_cached_characteristic->getExplosionInvulnerabilityTime();
}  // getExplosionInvulnerabilityTime

// ----------------------------------------------------------------------------
float KartProperties::getNitroDuration() const
{
    return m_cached_characteristic->getNitroDuration();
}  // getNitroDuration

// ------------------------------------------------------------------------
float KartProperties::getNitroEngineForce() const
{
    return m_cached_characteristic->getNitroEngineForce();
}  // getNitroEngineForce

// ----------------------------------------------------------------------------
float KartProperties::getNitroEngineMult() const
{
    return m_cached_characteristic->getNitroEngineMult();
}  // getNitroEngineMult

// ----------------------------------------------------------------------------
float KartProperties::getNitroConsumption() const
{
    return m_cached_characteristic->getNitroConsumption();
}  // getNitroConsumption

// ----------------------------------------------------------------------------
float KartProperties::getNitroSmallContainer() const
{
    return m_cached_characteristic->getNitroSmallContainer();
}  // getNitroSmallContainer

// ----------------------------------------------------------------------------
float KartProperties::getNitroBigContainer() const
{
    return m_cached_characteristic->getNitroBigContainer();
}  // getNitroBigContainer

// ----------------------------------------------------------------------------
float KartProperties::getNitroMaxSpeedIncrease() const
{
    return m_cached_characteristic->getNitroMaxSpeedIncrease();
}  // getNitroMaxSpeedIncrease

// ----------------------------------------------------------------------------
float KartProperties::getNitroFadeOutTime() const
{
    return m_cached_characteristic->getNitroFadeOutTime();
}  // getNitroFadeOutTime

// ----------------------------------------------------------------------------
float KartProperties::getNitroMax() const
{
    return m_cached_characteristic->getNitroMax();
}  // getNitroMax

// ----------------------------------------------------------------------------
float KartProperties::getSlipstreamDurationFactor() const
{
    return m_cached_characteristic->getSlipstreamDurationFactor();
}  // getSlipstreamDurationFactor

// ----------------------------------------------------------------------------
float KartProperties::getSlipstreamBaseSpeed() const
{
    return m_cached_characteristic->getSlipstreamBaseSpeed();
}  // getSlipstreamBaseSpeed

// ----------------------------------------------------------------------------
float KartProperties::getSlipstreamLength() const
{
    return m_cached_characteristic->getSlipstreamLength();
}  // getSlipstreamLength

// ----------------------------------------------------------------------------
float KartProperties::getSlipstreamWidth() const
{
    return m_cached_characteristic->getSlipstreamWidth();
}  // getSlipstreamWidth

// ----------------------------------------------------------------------------
float KartProperties::getSlipstreamInnerFactor() const
{
    return m_cached_characteristic->getSlipstreamInnerFactor();
}  // getSlipstreamInnerFactor

// ----------------------------------------------------------------------------
float KartProperties::getSlipstreamMinCollectTime() const
{
    return m_cached_characteristic->getSlipstreamMinCollectTime();
}  // getSlipstreamMinCollectTime

// ----------------------------------------------------------------------------
float KartProperties::getSlipstreamMaxCollectTime() const
{
    return m_cached_characteristic->getSlipstreamMaxCollectTime();
}  // getSlipstreamMaxCollectTime

// ----------------------------------------------------------------------------
float KartProperties::getSlipstreamAddPower() const
{
    return m_cached_characteristic->getSlipstreamAddPower();
}  // getSlipstreamAddPower

// ----------------------------------------------------------------------------
float KartProperties::getSlipstreamMinSpeed() const
{
    return m_cached_characteristic->getSlipstreamMinSpeed();
}  // getSlipstreamMinSpeed

// ----------------------------------------------------------------------------
float KartProperties::getSlipstreamMaxSpeedIncrease() const
{
    return m_cached_characteristic->getSlipstreamMaxSpeedIncrease();
}  // getSlipstreamMaxSpeedIncrease

// ----------------------------------------------------------------------------
int KartProperties::getSlipstreamFadeOutTicks() const
{
    return stk_config->time2Ticks(m_cached_characteristic
                                  ->getSlipstreamFadeOutTime());
}  // getSlipstreamFadeOutTime

// ----------------------------------------------------------------------------
float KartProperties::getSkidIncrease() const
{
    return m_cached_characteristic->getSkidIncrease();
}  // getSkidIncrease

// ----------------------------------------------------------------------------
float KartProperties::getSkidDecrease() const
{
    return m_cached_characteristic->getSkidDecrease();
}  // getSkidDecrease

// ----------------------------------------------------------------------------
float KartProperties::getSkidMax() const
{
    return m_cached_characteristic->getSkidMax();
}  // getSkidMax

// ----------------------------------------------------------------------------
float KartProperties::getSkidTimeTillMax() const
{
    return m_cached_characteristic->getSkidTimeTillMax();
}  // getSkidTimeTillMax

// ----------------------------------------------------------------------------
float KartProperties::getSkidVisual() const
{
    return m_cached_characteristic->getSkidVisual();
}  // getSkidVisual

// ----------------------------------------------------------------------------
float KartProperties::getSkidVisualTime() const
{
    return m_cached_characteristic->getSkidVisualTime();
}  // getSkidVisualTime

// ----------------------------------------------------------------------------
float KartProperties::getSkidRevertVisualTime() const
{
    return m_cached_characteristic->getSkidRevertVisualTime();
}  // getSkidRevertVisualTime

// ----------------------------------------------------------------------------
float KartProperties::getSkidMinSpeed() const
{
    return m_cached_characteristic->getSkidMinSpeed();
}  // getSkidMinSpeed

// ----------------------------------------------------------------------------
std::vector<float> KartProperties::getSkidTimeTillBonus() const
{
    return m_cached_characteristic->getSkidTimeTillBonus();
}  // getSkidTimeTillBonus

// ----------------------------------------------------------------------------
std::vector<float> KartProperties::getSkidBonusSpeed() const
{
    return m_cached_characteristic->getSkidBonusSpeed();
}  // getSkidBonusSpeed

// ----------------------------------------------------------------------------
std::vector<float> KartProperties::getSkidBonusTime() const
{
    return m_cached_characteristic->getSkidBonusTime();
}  // getSkidBonusTime

// ----------------------------------------------------------------------------
std::vector<float> KartProperties::getSkidBonusForce() const
{
    return m_cached_characteristic->getSkidBonusForce();
}  // getSkidBonusForce

// ----------------------------------------------------------------------------
float KartProperties::getSkidPhysicalJumpTime() const
{
    return m_cached_characteristic->getSkidPhysicalJumpTime();
}  // getSkidPhysicalJumpTime

// ----------------------------------------------------------------------------
float KartProperties::getSkidGraphicalJumpTime() const
{
    return m_cached_characteristic->getSkidGraphicalJumpTime();
}  // getSkidGraphicalJumpTime

// ----------------------------------------------------------------------------
float KartProperties::getSkidPostSkidRotateFactor() const
{
    return m_cached_characteristic->getSkidPostSkidRotateFactor();
}  // getSkidPostSkidRotateFactor

// ----------------------------------------------------------------------------
float KartProperties::getSkidReduceTurnMin() const
{
    return m_cached_characteristic->getSkidReduceTurnMin();
}  // getSkidReduceTurnMin

// ----------------------------------------------------------------------------
float KartProperties::getSkidReduceTurnMax() const
{
    return m_cached_characteristic->getSkidReduceTurnMax();
}  // getSkidReduceTurnMax

// ----------------------------------------------------------------------------
bool KartProperties::getSkidEnabled() const
{
    return m_cached_characteristic->getSkidEnabled();
}  // getSkidEnabled

/* <characteristics-end kpgetter> */

