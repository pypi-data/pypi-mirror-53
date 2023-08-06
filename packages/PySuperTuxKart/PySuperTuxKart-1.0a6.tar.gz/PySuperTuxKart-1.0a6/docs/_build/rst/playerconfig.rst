Python SuperTuxKart interface

**class pystk.PlayerConfig**

   SuperTuxKart player configuration

   **class Controller**

      Let the player or AI drive, AI ignores step(action)

      ``AI_CONTROL = Controller.AI_CONTROL``

      ``PLAYER_CONTROL = Controller.PLAYER_CONTROL``

   **property controller**

      Controller type (PlayerConfig.Controller)

   **property kart**

      Kart type (string), see list_karts for a list of kart types

   **property team**

      Team of the player (int) 0 or 1
