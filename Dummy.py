#!/usr/bin/env python

# Copyright (c) 2021 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

"""Example script to generate traffic in the simulation"""

import glob
import os
import sys
import time

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla


actorList = []
try:
    client = carla.Client('localhost', 2000)
    client.set_timeout(100.0)
    # world = client.load_world('Town02')
    world = client.get_world()
    # print(client.get_available_maps())
        
    blueprint_library = world.get_blueprint_library()
    # bp = random.choice(blueprint_library.filter('vehicle'))
    bp = blueprint_library.filter("model3")[0]
    spawn_point = carla.Transform(carla.Location(x=130, y=192, z = 0.25))
    # spawn_point = random.choice(world.get_map().get_spawn_points())
    vehicle = world.spawn_actor(bp, spawn_point)
    actorList.append(vehicle)
    print('created %s' % vehicle.type_id)
    actorList.append(vehicle)
    vehicle.apply_control(carla.VehicleControl(throttle = 0.15, steer = 0.0))
    time.sleep(150)
        
finally:
    for actor in actorList:
        actor.destroy()
    print("All cleaned up!") 