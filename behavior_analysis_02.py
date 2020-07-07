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

nosex = 0
nosey = 0

headx = 0
heady = 0

neckx = 0
necky = 0

bodyx = 0
bodyy = 0

tailx = 0
taily = 0


def fn_nosex (file):
    lines = open(file).readlines()
    nosex_table = []
    for line in lines[3:]:
        #print(line)
        try:
            nosex = float(line.split(',')[1].strip())
            #print(nosex)
            nosex_table.append(nosex)
        except ValueError:
            #print("error")
            nosex_table.append("NaN")
    return nosex_table

def fn_nosey (file):
    lines = open(file).readlines()
    nosey_table = []
    for line in lines[3:]:
        #print(line)
        try:
            nosey = float(line.split(',')[2].strip())
            #print(nosey)
            nosey_table.append(nosey)
        except ValueError:
            #print("error")
            nosey_table.append("NaN")
    return nosey_table

def fn_headx (file):
    lines = open(file).readlines()
    headx_table = []
    for line in lines[3:]:
        #print(line)
        try:
            headx = float(line.split(',')[4].strip())
            #print(nosex)
            headx_table.append(headx)
        except ValueError:
            #print("error")
            headx_table.append("NaN")
    return headx_table

def fn_heady (file):
    lines = open(file).readlines()
    heady_table = []
    for line in lines[3:]:
        #print(line)
        try:
            heady = float(line.split(',')[5].strip())
            #print(nosey)
            heady_table.append(heady)
        except ValueError:
            #print("error")
            heady_table.append("NaN")
    return heady_table

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
            nosex = float(line.split(',')[1].strip())
            nosey = float(line.split(',')[2].strip())
            dx = nosex - previous_nosex
            dy = nosey - previous_nosey
            nose_velocity = math.hypot(dx, dy) #math.hypot - returns the Euclidean distance
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
            bodyx = float(line.split(',')[10].strip())
            bodyy = float(line.split(',')[11].strip())
            dx = bodyx - previous_bodyx
            dy = bodyy - previous_bodyy
            body_velocity = math.hypot(dx, dy) #math.hypot - returns the Euclidean distance
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
            headx = float(line.split(',')[4].strip())
            heady = float(line.split(',')[5].strip())
            nosex = float(line.split(',')[1].strip())
            nosey = float(line.split(',')[2].strip())
            dx = nosex - headx
            dy = nosey - heady
            head_nose_vector = (dx, dy)
            head_nose_vector_table.append(head_nose_vector)
        except ValueError:
            #print("error")
            head_nose_vector_table.append("NaN")
    return head_nose_vector_table

obj = (230, 230) #object coorinates, sample(230,230) - left column
FOV_deg = 240
cFOV_deg = 120
#convert deg to rad:  n deg * (pi/180) = n rad
FOV_rad = FOV_deg * (math.pi / 180)
cFOV_rad = cFOV_deg * (math.pi / 180)
FOV05_rad = FOV_rad * 0.5
cFOV05_rad = cFOV_rad * 0.5

def fn_head_obj_vector (file, obj):
    lines = open(file).readlines()
    head_obj_vector_table = []
    for line in lines[3:]:
        #print(line)
        try:
            headx = float(line.split(',')[4].strip())
            heady = float(line.split(',')[5].strip())
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
            headx = float(line.split(',')[4].strip())
            heady = float(line.split(',')[5].strip())
            nosex = float(line.split(',')[1].strip())
            nosey = float(line.split(',')[2].strip())
            
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

#math.fabs(x)
#math.pi
#convert rad to deg:  n rad * (180/pi) = n degree


print("done")

np.savetxt(file[0:-4]+'_nose_velocity.csv', 
           fn_nose_velocity(file), delimiter=',', fmt="%s")

np.savetxt(file[0:-4]+'_body_velocity.csv', 
           fn_body_velocity(file), delimiter=',', fmt="%s")

np.savetxt(file[0:-4]+'_head_nose_vector.csv', 
           fn_head_nose_vector(file), delimiter=',', fmt="%s")

np.savetxt(file[0:-4]+'_head_obj_vector.csv', 
           fn_head_obj_vector(file, obj), delimiter=',', fmt="%s")

np.savetxt(file[0:-4]+'_angle_head_nose_obj.csv', 
           fn_angle_head_nose_obj(file, obj), delimiter=',', fmt="%s")