Python SuperTuxKart interface

**class pystk.Action**

   SuperTuxKart action

   **__init__(self: pystk.Action, steer: float=0, acceleration:
   float=0, brake: bool=False, nitro: bool=False, drift: bool=False,
   rescue: bool=False, fire: bool=False) -> None**

   **property acceleration**

      Acceleration, normalize to 0..1 (float)

   **property brake**

      Hit the brakes (bool)

   **property drift**

      Drift while turning (bool)

   **property fire**

      Fire the current pickup item (bool)

   **property nitro**

      Use nitro (bool)

   **property rescue**

      Call the rescue bird (bool)

   **property steer**

      Steering angle, normalize to -1..1 (float)
