# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 14:47:57 2020

@author: Kacper
"""

'''
Pipeline:
1. copy files (.csv, .avi or .mp4)
2. check path_name
3. add file_name variables
4. choose analysis_type
4. check video_input
5. run imports and _names
6. run calibration
7. create bcg_frame
8. modify obj coordinates
9. execute functions and generate selected output files (analysis_type!)
'''

#functions for behavioral analysis

#%%
import os
import numpy as np
import math
from matplotlib import pyplot as plt
import matplotlib.cm as cm
from PIL import Image

#%%
path_name = 'C:\\Users\\Kacper\\Documents\\ASD_computational_ethology\\Fmr1KO_analysis\\FXG15_WT_M_R'

#file_name = 'FXG10_WT_M_LR_hab3DLC_resnet50_TDTv1Jul8shuffle1_126000.csv'
#file_name = 'FXG10_WT_M_LR_enc1DLC_resnet50_TDTv1Jul8shuffle1_126000.csv'
#file_name = 'FXG10_WT_M_LR_testDLC_resnet50_TDTv1Jul8shuffle1_126000.csv'

#file_name = 'FXG11_WT_M_LL_hab3DLC_resnet50_TDTv1Jul8shuffle1_126000.csv'
#file_name = 'FXG11_WT_M_LL_enc1DLC_resnet50_TDTv1Jul8shuffle1_126000.csv'
#file_name = 'FXG11_WT_M_LL_testDLC_resnet50_TDTv1Jul8shuffle1_126000.csv'

#file_name = 'FXG11_WT_M_RR_hab3DLC_resnet50_TDTv1Jul8shuffle1_126000.csv'
#file_name = 'FXG11_WT_M_RR_enc1DLC_resnet50_TDTv1Jul8shuffle1_126000.csv'
#file_name = 'FXG11_WT_M_RR_testDLC_resnet50_TDTv1Jul8shuffle1_126000.csv'

#file_name = 'FXG12_KO_M_LL_hab3DLC_resnet50_TDTv1Jul8shuffle1_126000.csv'
#file_name = 'FXG12_KO_M_LL_enc1DLC_resnet50_TDTv1Jul8shuffle1_126000.csv'

#file_name = 'FXG12_KO_M_R_hab3DLC_resnet50_TDTv1Jul8shuffle1_126000.csv'
#file_name = 'FXG12_KO_M_R_enc1DLC_resnet50_TDTv1Jul8shuffle1_126000.csv'

#file_name = 'FXG14_KO_M_LR_hab3DLC_resnet50_TDTv1Jul8shuffle1_126000.csv'
#file_name = 'FXG14_KO_M_LR_enc1DLC_resnet50_TDTv1Jul8shuffle1_126000.csv'
#file_name = 'FXG14_KO_M_LR_testDLC_resnet50_TDTv1Jul8shuffle1_126000.csv'

#file_name = 'FXG14_KO_M_R_hab3DLC_resnet50_TDTv1Jul8shuffle1_126000.csv'
#file_name = 'FXG14_KO_M_R_encDLC_resnet50_TDTv1Jul8shuffle1_126000.csv'
#file_name = 'FXG14_KO_M_R_testDLC_resnet50_TDTv1Jul8shuffle1_126000.csv'

#file_name = 'FXG14_WT_M_L_hab3DLC_resnet50_TDTv1Jul8shuffle1_126000.csv'
#file_name = 'FXG14_WT_M_L_encDLC_resnet50_TDTv1Jul8shuffle1_126000.csv'
#file_name = 'FXG14_WT_M_L_testDLC_resnet50_TDTv1Jul8shuffle1_126000.csv'

#file_name = 'FXG15_KO_M_L_hab3DLC_resnet50_TDTv1Jul8shuffle1_126000.csv'
#file_name = 'FXG15_KO_M_L_enc1DLC_resnet50_TDTv1Jul8shuffle1_126000.csv'
#file_name = 'FXG15_KO_M_L_test1DLC_resnet50_TDTv1Jul8shuffle1_126000.csv'

#file_name = 'FXG15_KO_M_LR_hab3DLC_resnet50_TDTv1Jul8shuffle1_126000.csv'
#file_name = 'FXG15_KO_M_LR_enc1DLC_resnet50_TDTv1Jul8shuffle1_126000.csv'
#file_name = 'FXG15_KO_M_LR_test1DLC_resnet50_TDTv1Jul8shuffle1_126000.csv'

#file_name = 'FXG15_WT_M_R_hab3DLC_resnet50_TDTv1Jul8shuffle1_126000.csv'
#file_name = 'FXG15_WT_M_R_enc1DLC_resnet50_TDTv1Jul8shuffle1_126000.csv'
file_name = 'FXG15_WT_M_R_test1DLC_resnet50_TDTv1Jul8shuffle1_126000.csv'

file = path_name + '\\' + file_name
print(file)

# choose analysis_type = ('hab', 'enc', 'test')
analysis_type = 'test'

#%%
try:
    parameters = open(file[0:-4]+'_parameters_log.csv').readlines()
    fps = float(parameters[1].split(',')[1].strip())
    calibration = float(parameters[1].split(',')[2].strip())
except IOError: 
    # video calibration
    fps = 30
    # arena measured from upper left to lower right corner
    arena_length_cm = 38
    arena_width_cm = 28
    arena_length_pxl = 455
    arena_width_pxl = 326
    calibration = ((arena_length_pxl / arena_length_cm) +  (arena_width_pxl / arena_width_cm)) / 2 #1cm = n pxl

try:
    parameters = open(file[0:-4]+'_parameters_log.csv').readlines()
    FOV_deg = float(parameters[1].split(',')[9].strip())
    cFOV_deg = float(parameters[1].split(',')[10].strip())
except IOError:
    FOV_deg = 240 #FOV in degrees
    cFOV_deg = 120 #centralFOV in degrees
    #convert deg to rad:  n deg * (pi/180) = n rad
    #convert rad to deg:  n rad * (180/pi) = n degree
    FOV_rad = FOV_deg * (math.pi / 180) #FOV in radians
    cFOV_rad = cFOV_deg * (math.pi / 180) #cFOV in radians
    FOV05_rad = FOV_rad * 0.5
    cFOV05_rad = cFOV_rad * 0.5

#%%
# bcg frame extraction
#video_input = file[0:-4]+'_labeled.mp4'
video_input = file[0:-41]+'.avi'
bcg_frame_name = file[0:-4]+'_frame01.png'
os.system('ffmpeg -ss 00:00:01 -i {0} -vframes 1 -q:v 2 {1}'.format(video_input, bcg_frame_name))

#%%
try:
    parameters = open(file[0:-4]+'_parameters_log.csv').readlines()
    objL = (float(parameters[1].split(',')[3].strip()), float(parameters[1].split(',')[4].strip())) 
    objLradius = float(parameters[1].split(',')[5].strip())
    objR = (float(parameters[1].split(',')[6].strip()), float(parameters[1].split(',')[7].strip())) 
    objRradius = float(parameters[1].split(',')[8].strip())
except IOError:
    objL = (226, 239) #object coorinates - left column
    objLradius = 50
    objR = (430, 237) #object coorinates - right column
    objRradius = 50

#%%
def fn_parameters_log (file, fps, calibration, objL, objLradius, objR, objRradius, FOV_deg, cFOV_deg):
    log_table = []
    log = ('file', 'fps', 'calibration', 'objL_x', 'objL_y', 'objLradius', 'objR_x', 'objR_y', 'objRradius', 'FOVdeg', 'cFOVdeg')
    log_table.append(log)
    log = (file, fps, calibration, objL[0], objL[1], objLradius, objR[0], objR[1], objRradius, FOV_deg, cFOV_deg)
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


def fn_body_part_table (file, body_part, xy):
    lines = open(file).readlines()
    body_part_table = []
    for line in lines[3:]:
        #print(line)
        try:
            record = fn_body_part(body_part, xy, line)
            #print(body_part)
            body_part_table.append(record)
        except ValueError:
            #print("error")
            body_part_table.append("NaN")
    return body_part_table[1:]


def fn_bpart_obj_distance (body_part, obj, line):
    try:
        bpartx = fn_body_part(body_part, 'x', line)
        bparty = fn_body_part(body_part, 'y', line)
        dx = obj[0] - bpartx
        dy = obj[1] - bparty
        distance = math.hypot(dx, dy) 
    except ValueError:
        #print("error")
        distance = 'NaN'
    return distance


def fn_bpart_obj_distance_table (file, body_part, obj, closer="false"):
    lines = open(file).readlines()
    bpart_obj_distance_table = []
    for line in lines[3:]:
        try:
            if closer == 'true':
                obj = fn_closer_obj(body_part, objL, objR, line)
            bpart_obj_distance = fn_bpart_obj_distance(body_part, obj, line)
            bpart_obj_distance_table.append(bpart_obj_distance)
        except ValueError:
            #print("error")
            bpart_obj_distance_table.append("NaN")
    return bpart_obj_distance_table[1:]


def fn_closer_obj (body_part, objL, objR, line): 
    if fn_bpart_obj_distance(body_part, objL, line) < fn_bpart_obj_distance(body_part, objR, line):
        closer_obj = objL
    else: 
        closer_obj = objR
    return closer_obj


def fn_closer_obj_table (file, body_part, objL, objR):
    lines = open(file).readlines()
    closer_obj_table = []
    for line in lines[3:]:
        try:
            closer_obj = fn_closer_obj (body_part, objL, objR, line)
            closer_obj_table.append(closer_obj)
        except ValueError:
            #print("error")
            closer_obj_table.append("NaN")
    return closer_obj_table


def fn_bpart1_bpart2_distance (file, body_part1, body_part2):
    lines = open(file).readlines()
    bpart1_bpart2_distance_table = []
    for line in lines[3:]:
        #print(line)
        try:
            bpart1x = fn_body_part(body_part1, 'x', line)
            bpart1y = fn_body_part(body_part1, 'y', line)
            bpart2x = fn_body_part(body_part2, 'x', line)
            bpart2y = fn_body_part(body_part2, 'y', line)
            
            dx = bpart1x - bpart2x
            dy = bpart1y - bpart2y
            bpart12_distance = math.hypot(dx, dy) / calibration
            
            bpart1_bpart2_distance_table.append(bpart12_distance)
        except ValueError:
            #print("error")
            bpart1_bpart2_distance_table.append("NaN")
    return bpart1_bpart2_distance_table
     
def fn_all_bpart_distance (file):
    all_bpart_distance = [fn_bpart1_bpart2_distance(file, 'nose', 'head'),
           fn_bpart1_bpart2_distance(file, 'head', 'neck'),
           fn_bpart1_bpart2_distance(file, 'neck', 'body'),
           fn_bpart1_bpart2_distance(file, 'body', 'tail')
           ]
    return np.transpose(all_bpart_distance)

   
# fn_bpart_distance_moved - for selected bodypart returns table with distance in cm for each frame
def fn_bpart_distance_moved (file, body_part):
    lines = open(file).readlines()
    bpart_distance_table = []
    bpart_distance = 0
    previous_bpartx = 0
    previous_bparty = 0
    for line in lines[3:]:
        #print(line)
        try:
            bpartx = fn_body_part(body_part, 'x', line)
            bparty = fn_body_part(body_part, 'y', line)
            dx = bpartx - previous_bpartx
            dy = bparty - previous_bparty
            bpart_distance = math.hypot(dx, dy) / calibration #math.hypot - returns the Euclidean distance
            bpart_distance_table.append(bpart_distance)
        except ValueError:
            #print("error")
            bpart_distance_table.append("NaN")
        previous_bpartx = bpartx
        previous_bparty = bparty
    return bpart_distance_table[1:]


# fn_bpart_velocity - for selected bodypart returns table with velocity in cm/s for each frame
def fn_bpart_velocity (file, body_part):
    lines = open(file).readlines()
    bpart_velocity_table = []
    bpart_velocity = 0
    previous_bpartx = 0
    previous_bparty = 0
    for line in lines[3:]:
        #print(line)
        try:
            bpartx = fn_body_part(body_part, 'x', line)
            bparty = fn_body_part(body_part, 'y', line)
            dx = bpartx - previous_bpartx
            dy = bparty - previous_bparty
            bpart_velocity = math.hypot(dx, dy) * fps / calibration #math.hypot - returns the Euclidean distance
            bpart_velocity_table.append(bpart_velocity)
        except ValueError:
            #print("error")
            bpart_velocity_table.append("NaN")
        previous_bpartx = bpartx
        previous_bparty = bparty
    return bpart_velocity_table[1:]


# fn_angle_head_nose_obj - for selected object returns table with vectors and 0;1 for is in FOV and cFOV for each frame
def fn_angle_head_nose_obj (file, obj, closer="false"):
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
            if closer == 'true':
                obj = fn_closer_obj('nose', objL, objR, line)
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


def fn_bpart_inROI (file, body_part, obj, radius, closer="false"):
    lines = open(file).readlines()
    bpart_inROI_table = []
    for line in lines[3:]:
        #print(line)
        try:
            if closer == 'true':
                obj = fn_closer_obj('nose', objL, objR, line)
            distance = fn_bpart_obj_distance(body_part, obj, line)
            if distance <= radius:
                bpart_inROI = 1
            else:
                bpart_inROI = 0
            
            bpart_inROI_table.append(bpart_inROI)
        except ValueError:
            #print("error")
            bpart_inROI_table.append("NaN")
    return bpart_inROI_table    


# sqrt transformation
def fn_sqrt_bpart_velocity (table):
    length = len(fn_bpart_velocity (file, 'body'))
    for record in range(length):
        table[record] = math.sqrt(table[record])
    return table


def fn_save_bodypart_velocity_plot (file, bodypart, bcg_filename):
    #plotting position
    img_name = bcg_filename
    img  = Image.open(img_name)
    #plt.imshow(img)
    
    plt.figure()
    plt.set_cmap('gray')
    plt.imshow(img, alpha=0.5)
    #color = 'r'
    #plt.plot(fn_body_part_table(file, 'nose', 'x'), fn_body_part_table(file, 'nose', 'y'), color)
    #m = cm.ScalarMappable(norm=norm, cmap=cmap)
    # https://matplotlib.org/3.2.2/api/_as_gen/matplotlib.pyplot.scatter.html#matplotlib.pyplot.scatter
    plt.scatter(fn_body_part_table(file, bodypart, 'x'), 
                fn_body_part_table(file, bodypart, 'y'), 
                c=cm.jet(fn_bpart_velocity (file, bodypart)),
                #https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html
                #c=cm.jet(fn_norm_bpart_velocity(fn_bpart_velocity (file, 'nose'))),
                marker = '.')
    plt.savefig(file[0:-4]+ '_' + bodypart + '_velocity_plot.png')


#for filename in os.listdir(path):
#    if (filename.endswith(".mp4")): #or .avi, .mpeg, whatever.
#        os.system("ffmpeg -i {0} -f image2 -vf fps=fps=1 output%d.png".format(filename))
#    else:
#        continue


print("done")


#%%
np.savetxt(file[0:-4]+'_parameters_log.csv', 
           fn_parameters_log(file, fps, calibration, objL, objLradius, objR, objRradius, FOV_deg, cFOV_deg), delimiter=',', fmt='%s')


np.savetxt(file[0:-4]+'_body_distance.csv', 
           fn_bpart_distance_moved (file, 'body'), delimiter=',', fmt="%s")

np.savetxt(file[0:-4]+'_nose_distance.csv', 
           fn_bpart_distance_moved (file, 'nose'), delimiter=',', fmt="%s")

np.savetxt(file[0:-4]+'_bparts_Euclidean_distance.csv', 
           fn_all_bpart_distance (file), 
           delimiter=',', fmt="%f")


np.savetxt(file[0:-4]+'_nose_velocity.csv', 
           fn_bpart_velocity(file, 'nose'), delimiter=',', fmt="%s")

np.savetxt(file[0:-4]+'_body_velocity.csv', 
           fn_bpart_velocity(file, 'body'), delimiter=',', fmt="%s")

#np.savetxt(file[0:-4]+'_body_velocity_sqrt.csv', 
#           fn_sqrt_bpart_velocity(fn_bpart_velocity (file, 'body')), delimiter=',', fmt="%s")


if analysis_type == 'enc' or analysis_type == 'test':
    np.savetxt(file[0:-4]+'_angle_head_nose_objL.csv', 
               fn_angle_head_nose_obj(file, objL), delimiter=',', fmt="%s")

    np.savetxt(file[0:-4]+'_angle_head_nose_objR.csv', 
               fn_angle_head_nose_obj(file, objR), delimiter=',', fmt="%s")

    np.savetxt(file[0:-4]+'_angle_head_nose_closerobj.csv', 
               fn_angle_head_nose_obj(file, 1, 'true'), delimiter=',', fmt="%s")


    np.savetxt(file[0:-4]+'_ROI_nose_objL.csv', 
               fn_bpart_inROI(file, 'nose', objL, objLradius), delimiter=',', fmt="%s")

    np.savetxt(file[0:-4]+'_ROI_nose_objR.csv', 
               fn_bpart_inROI(file, 'nose', objR, objRradius), delimiter=',', fmt="%s")

    np.savetxt(file[0:-4]+'_ROI_nose_closerobj.csv', 
               fn_bpart_inROI(file, 'nose', 1, objRradius, 'true'), delimiter=',', fmt="%s")


    np.savetxt(file[0:-4]+'_nose_objL_distance.csv', 
               fn_bpart_obj_distance_table(file, 'nose', objL), delimiter=',', fmt="%s")

    np.savetxt(file[0:-4]+'_nose_objR_distance.csv', 
               fn_bpart_obj_distance_table(file, 'nose', objR), delimiter=',', fmt="%s")


    np.savetxt(file[0:-4]+'_closer_obj.csv', 
               fn_closer_obj_table(file, 'nose', objL, objR), delimiter=',', fmt="%s")

    np.savetxt(file[0:-4]+'_nose_closer_obj_distance.csv', 
               fn_bpart_obj_distance_table(file, 'nose', 1, 'true'), delimiter=',', fmt="%s")

    np.savetxt(file[0:-4]+'_body_closer_obj_distance.csv', 
               fn_bpart_obj_distance_table(file, 'body', 1, 'true'), delimiter=',', fmt="%s")



fn_save_bodypart_velocity_plot (file, 'body', bcg_frame_name)

fn_save_bodypart_velocity_plot (file, 'nose', bcg_frame_name)
