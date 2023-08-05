Python SuperTuxKart interface

**class pystk.RaceConfig**

   SuperTuxKart race configuration.

   **class RaceMode**

      ``CAPTURE_THE_FLAG = RaceMode.CAPTURE_THE_FLAG``

      ``FOLLOW_LEADER = RaceMode.FOLLOW_LEADER``

      ``FREE_FOR_ALL = RaceMode.FREE_FOR_ALL``

      ``NORMAL_RACE = RaceMode.NORMAL_RACE``

      ``SOCCER = RaceMode.SOCCER``

      ``THREE_STRIKES = RaceMode.THREE_STRIKES``

      ``TIME_TRIAL = RaceMode.TIME_TRIAL``

   **property difficulty**

      Skill of AI players 0..2 (int)

   **property laps**

      Number of laps the race runs for (int)

   **property mode**

      Specify the type of race (RaceMode)

   **property num_kart**

      Total number of karts, fill the race with num_kart -
      len(players) AI karts (int)

   **property players**

      List of all agent players (List[PlayerConfig])

   **property render**

      Is rendering enabled? (bool)

   **property reverse**

      Reverse the track (bool)

   **property seed**

      Random seed (int)

   **property step_size**

      Game time between different step calls (float)

   **property track**

      Track name (str)

**pystk.list_tracks() -> List[str]**

   Return a list of track names (possible values for RaceConfig.track)

**pystk.list_karts() -> List[str]**

   Return a list of karts to play as (possible values for
   PlayerConfig.kart
