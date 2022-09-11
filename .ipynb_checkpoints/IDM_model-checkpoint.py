import glob
import os
import sys
import random
import time
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import math


try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass


import carla


# Radar_data processing
def process(radar_data):
    #print(sensor_data)
    #points = np.frombuffer(radar_data.raw_data, dtype=np.dtype('f4'))
    #points = np.reshape(points, (len(radar_data), 4))  # points = points.reshape(len(radar_data), 4)
    for detect in radar_data:
        rel_vel = detect.velocity # Relative velocity
        rel_dis = detect.depth # distance b/w sensor to the detected object
        vel_car = vehicle.get_velocity().x
        acc = IDM(vel_car, rel_dis, rel_vel)  # acceleration from rule-based model
        if acc>=0:
            throttle = acc
            brake = 0
        else:
            throttle = 0
            brake = abs(acc)
            
        vehicle.apply_control(carla.VehicleControl(throttle = throttle, steer = 0.0, brake = brake))  # Acceleration provided to the vehicle control
        
        # Printing relative velcity, relative distance (sensor data), car velocity (actor data), acceleration (rule based model)
        print("acceleration " + str(acc) + " rel_vel " + str(rel_vel) + " rel_dis "+str(rel_dis) + " vel_car " + str(vel_car) + " throttle = " + str(throttle) + "brake = " +str(brake))
        return acc


# Rule-Based driver model (Car following model)
def IDM(vel_car, rel_dis, rel_vel, v_0 = 30, T = 1.5, a = 0.6, b = 1.67, s_0 = 2):
    Term_int = s_0 + vel_car*T + (vel_car*rel_vel/(2*math.sqrt(a*b)))
    acc = a*(1-((vel_car/v_0)**4)-(Term_int/rel_dis)**2)
    return acc


    

actor_list =[]


try:
    # Connecting to the servers and Retrieving the current world
    client = carla.Client("localhost", 2000)
    client.set_timeout(120.0)
    world = client.get_world()
    # world = client.load_world('Town02')
    # print(client.get_available_maps())
    

    # accessing the blueprint library to selecting the vehicles
    blueprint_library = world.get_blueprint_library()
    # bp = random.choice(blueprint_library.filter('vehicle'))
    bp = blueprint_library.filter("model3")[0]

    # Spawning (Positioning) the vehicle in the world map
    # spawn_point = random.choice(world.get_map().get_spawn_points())
    spawn_point = carla.Transform(carla.Location(x=100, y=192, z = 0.25))
    vehicle = world.spawn_actor(bp, spawn_point)

    # Storing all the created actors in a list
    actor_list.append(vehicle)
    print('created %s' % vehicle.type_id)
    
    
    ## Adding sensor to the vehicle
    # Selecting the sensor
    sensor_bp = blueprint_library.find('sensor.other.radar')
    
    # Setting attributes of sensor
    sensor_bp.set_attribute('horizontal_fov', str(60))
    sensor_bp.set_attribute('vertical_fov', str(30))
        
    # Attaching sensor to the vehicle
    sensor_spawn = carla.Transform(carla.Location(x=2.5,z=0.7))
    sensor = world.spawn_actor(sensor_bp, sensor_spawn, attach_to=vehicle)
    actor_list.append(sensor)
    print('created %s' % sensor.type_id)
    
    
    ## Retrieving data from sensor
    # Radar Sensor
    sensor.listen(lambda data: process(data))
    
    
    # Pausing the program till we enter the enter key
    # input("Press Enter to continue...")
    time.sleep(150)


finally:
    for actor in actor_list:
        actor.destroy()
    print("All cleaned up!")