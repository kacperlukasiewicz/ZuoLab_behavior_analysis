# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 14:47:57 2020

@author: Kacper
"""

#functions for behavioral analysis

import numpy as np
import math


path_name = 'C:\\Users\\Kacper\\Documents\\ASD_computational_ethology\\KL011_enc-sample'
file_name = 'KL011-encDLC_resnet50_texture_sucroseJun18shuffle1_126000.csv'
file = path_name + '\\' + file_name
print(file)

# video calibration
fps = 30
# arena measured from upper left to lower right corner
arena_length_cm = 38
arena_width_cm = 28
arena_length_pxl = 455
arena_width_pxl = 326
calibration = ((arena_length_pxl / arena_length_cm) +  (arena_width_pxl / arena_width_cm)) / 2 #1cm = n pxl

objL = (230, 230) #object coorinates - left column
objR = (428, 225) #object coorinates - right column
FOV_deg = 240 #FOV in degrees
cFOV_deg = 120 #centralFOV in degrees
#convert deg to rad:  n deg * (pi/180) = n rad
#convert rad to deg:  n rad * (180/pi) = n degree
FOV_rad = FOV_deg * (math.pi / 180) #FOV in radians
cFOV_rad = cFOV_deg * (math.pi / 180) #cFOV in radians
FOV05_rad = FOV_rad * 0.5
cFOV05_rad = cFOV_rad * 0.5

def fn_parameters_log (file, fps, calibration, objL, objR, FOV_deg, cFOV_deg):
    log_table = []
    log = ('file', 'fps', 'calibration', 'objL_x', 'objL_y', 'objR_x', 'objR_y', 'FOVdeg', 'cFOVdeg')
    log_table.append(log)
    log = (file, fps, calibration, objL, objR, FOV_deg, cFOV_deg)
    log_table.append(log)
    return log_table


def fn_body_part (body_part, xy, line):
    if body_part == 'nose':
        if xy == 'x':
            body_part = float(line.split(',')[1].strip())
        elif xy == 'y':
            body_part = float(line.split(',')[2].strip())
    elif body_part == 'head':
        if xy == 'x':
            body_part = float(line.split(',')[4].strip())
        elif xy == 'y':
            body_part = float(line.split(',')[5].strip())
    elif body_part == 'neck':
        if xy == 'x':
            body_part = float(line.split(',')[7].strip())
        elif xy == 'y':
            body_part = float(line.split(',')[8].strip())
    elif body_part == 'body':
        if xy == 'x':
            body_part = float(line.split(',')[10].strip())
        elif xy == 'y':
            body_part = float(line.split(',')[11].strip())
    elif body_part == 'tail':
        if xy == 'x':
            body_part = float(line.split(',')[13].strip())
        elif xy == 'y':
            body_part = float(line.split(',')[14].strip())
    return body_part

# fn_nose_velocity - returns table with velocity in pxl for each frame
def fn_nose_velocity (file):
    lines = open(file).readlines()
    nose_velocity_table = []
    nose_velocity = 0
    previous_nosex = 0
    previous_nosey = 0
    for line in lines[3:]:
        #print(line)
        try:
            nosex = fn_body_part('nose', 'x', line)
            nosey = fn_body_part('nose', 'y', line)
            dx = nosex - previous_nosex
            dy = nosey - previous_nosey
            nose_velocity = math.hypot(dx, dy) * fps / calibration #math.hypot - returns the Euclidean distance
            nose_velocity_table.append(nose_velocity)
        except ValueError:
            #print("error")
            nose_velocity_table.append("NaN")
        previous_nosex = nosex
        previous_nosey = nosey
    return nose_velocity_table[1:]

# fn_body_velocity - returns table with velocity in pxl for each frame
def fn_body_velocity (file):
    lines = open(file).readlines()
    body_velocity_table = []
    body_velocity = 0
    previous_bodyx = 0
    previous_bodyy = 0
    for line in lines[3:]:
        #print(line)
        try:
            bodyx = fn_body_part('body', 'x', line)
            bodyy = fn_body_part('body', 'y', line)
            dx = bodyx - previous_bodyx
            dy = bodyy - previous_bodyy
            body_velocity = math.hypot(dx, dy) * fps / calibration #math.hypot - returns the Euclidean distance
            body_velocity_table.append(body_velocity)
        except ValueError:
            #print("error")
            body_velocity_table.append("NaN")
        previous_bodyx = bodyx
        previous_bodyy = bodyy
    return body_velocity_table[1:]

def fn_head_nose_vector (file):
    lines = open(file).readlines()
    head_nose_vector_table = []
    for line in lines[3:]:
        #print(line)
        try:
            headx = fn_body_part('head', 'x', line)
            heady = fn_body_part('head', 'y', line)
            nosex = fn_body_part('nose', 'x', line)
            nosey = fn_body_part('nose', 'y', line)
            dx = nosex - headx
            dy = nosey - heady
            head_nose_vector = (dx, dy)
            head_nose_vector_table.append(head_nose_vector)
        except ValueError:
            #print("error")
            head_nose_vector_table.append("NaN")
    return head_nose_vector_table

def fn_head_obj_vector (file, obj):
    lines = open(file).readlines()
    head_obj_vector_table = []
    for line in lines[3:]:
        #print(line)
        try:
            headx = fn_body_part('head', 'x', line)
            heady = fn_body_part('head', 'y', line)
            dx = obj[0] - headx
            dy = obj[1] - heady
            head_obj_vector = (dx, dy)
            head_obj_vector_table.append(head_obj_vector)
        except ValueError:
            #print("error")
            head_obj_vector_table.append("NaN")
    return head_obj_vector_table

def fn_angle_head_nose_obj (file, obj):
    lines = open(file).readlines()
    angle_head_nose_obj_table = []
    for line in lines[3:]:
        #print(line)
        try:
            headx = fn_body_part('head', 'x', line)
            heady = fn_body_part('head', 'y', line)
            nosex = fn_body_part('nose', 'x', line)
            nosey = fn_body_part('nose', 'y', line)
            
            dx_head_nose = nosex - headx
            dy_head_nose = nosey - heady
            head_nose_vector = (dx_head_nose, dy_head_nose)
            
            dx_head_obj = obj[0] - headx
            dy_head_obj = obj[1] - heady
            head_obj_vector = (dx_head_obj, dy_head_obj)
            
            
            # Return atan(y / x), in radians. The result is between -pi and pi. 
            #The vector in the plane from the origin to point (x, y) makes this angle with the positive X axis. 
            #The point of atan2() is that the signs of both inputs are known to it, so it can compute the correct quadrant for the angle. 
            #For example, atan(1) and atan2(1, 1) are both pi/4, but atan2(-1, -1) is -3*pi/4.
            polar_head_nose = math.atan2(head_nose_vector[1], head_nose_vector[0])       
            polar_head_obj = math.atan2(head_obj_vector[1], head_obj_vector[0])
            
            diff_polar_head_nose_obj = math.fabs(polar_head_nose - polar_head_obj)
            if diff_polar_head_nose_obj > math.pi:
                diff_polar_head_nose_obj = (2 * math.pi) - diff_polar_head_nose_obj
            
            if diff_polar_head_nose_obj <= FOV05_rad:
                isinFOV = 1
            else:
                isinFOV = 0
                
            if diff_polar_head_nose_obj <= cFOV05_rad:
                isincFOV = 1
            else:
                isincFOV = 0
            
            angle_head_nose_obj = (polar_head_nose, polar_head_obj, diff_polar_head_nose_obj, isinFOV, isincFOV)
            angle_head_nose_obj_table.append(angle_head_nose_obj)
        except ValueError:
            #print("error")
            angle_head_nose_obj_table.append("NaN", "NaN", "NaN", "NaN", "NaN")
    return angle_head_nose_obj_table

print("done")

np.savetxt(file[0:-4]+'_parameters_log.csv', 
           fn_parameters_log(file, fps, calibration, objL, objR, FOV_deg, cFOV_deg), delimiter=',', fmt="%s")

np.savetxt(file[0:-4]+'_nose_velocity.csv', 
           fn_nose_velocity(file), delimiter=',', fmt="%s")

np.savetxt(file[0:-4]+'_body_velocity.csv', 
           fn_body_velocity(file), delimiter=',', fmt="%s")

np.savetxt(file[0:-4]+'_head_nose_vector.csv', 
           fn_head_nose_vector(file), delimiter=',', fmt="%s")

np.savetxt(file[0:-4]+'_head_objL_vector.csv', 
           fn_head_obj_vector(file, objL), delimiter=',', fmt="%s")

np.savetxt(file[0:-4]+'_angle_head_nose_objL.csv', 
           fn_angle_head_nose_obj(file, objL), delimiter=',', fmt="%s")

np.savetxt(file[0:-4]+'_head_objR_vector.csv', 
           fn_head_obj_vector(file, objR), delimiter=',', fmt="%s")

np.savetxt(file[0:-4]+'_angle_head_nose_objR.csv', 
           fn_angle_head_nose_obj(file, objR), delimiter=',', fmt="%s")