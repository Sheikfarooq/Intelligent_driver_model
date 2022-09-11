
# Car following Model

Adjusting the acceleration of the ego vehicle based on the velocity of the front vehicle. 

Implementing the Intelligent driver model to avoid the collisions with the front vehicle.

Using Radar sensor in Carla simulator to observe the surroundings




## Acknowledgements

 - [Intelligent driver model](https://en.wikipedia.org/wiki/Intelligent_driver_model)
## Tools

Python 3.7

Carla
## Scenario - I

In this condition, the front vehicle / obstacle is in stationary condition. Ego vehicle stops behind the obstacle by keeping the safe distance, to avoid the collision

<p><img align="left" src="https://github.com/Sheikfarooq/Intelligent_driver_model/blob/main/Obstacle_Stationary.gif" width="500" /></p>

## Scenario - II

In this condition, the front vehicle / obstacle is in moving condition, but its velocity is less compared to the ego vehicle. Ego vehicle adjusts its speed based on the front vehicle's speed to avoid collision.

<p><img align="left" src="https://github.com/Sheikfarooq/Covid-19_simulation/blob/main/Covid_Simulation.gif" width="500" /></p>
