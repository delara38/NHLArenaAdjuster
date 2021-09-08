NHLArenaAdjuster
=======================

package for arena adjusting the event level coordinate data available in the NHL api


_______________________
PURPOSE
========================


Performs stadium adjustments on NHL Play-By-Play coordinate data to remove rink bias.

Great post on rink bias: https://hockey-statistics.com/2020/08/02/indications-that-shot-location-data-is-flawed-depends-on-where-games-are-being-played/

NHL API Documentation: https://gitlab.com/dword4/nhlapi


----------------------------
CoordinateAdjuster
-------------------


The pakcage is centered around the CoordinateAdjuster object.
  
 _____________________________________________
 CoordinateAdjuster
 -----------------------

Built in the scikit-learn mould of having fit, transform and fit_transform.


>  From NHLArenaAdjuster import CoordinateAdjuster
>  
> CoordinateAdjuster()


- CoordinateAdjuster.fit(pandas DataFrame):
  - fits model using a method developed by Shuckers and Curro in their THoR paper.
  - param data: pandas dataframe with following columns:
                 *   [x coordinate, y coordinate, arena, away team name, away shot boolean]
  - return: None

- CoordinateAdjuster.transform(pandas DataFrame):
  - adjusts data to remove rink bias
  - param data: pandas dataframe with following columns:
                 *   [x coordinate, y coordinate, arena, away team name, away shot boolean]
  - return: 2xN array where N is the length of the input dataframe with columns: [ adjusted x coordinate, adjusted y coordinate ]
   

- CoordinateAdjuster.fit_transform(pandas DataFrame):
  - fits model to dataframe and then returns transformed version
  - param data: pandas dataframe with following columns:
                 *   [x coordinate, y coordinate, arena, away team name, away shot boolean]
  - return: 2xN array where N is the length of the input dataframe with columns: [ adjusted x coordinate, adjusted y coordinate ]
    


 
