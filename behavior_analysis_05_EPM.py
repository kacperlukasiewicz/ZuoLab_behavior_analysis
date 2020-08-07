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
4. check video_input
5. run imports and _names
6. run calibration
7. create bcg_frame
8. modify coordinates
9. execute functions and generate selected output files
'''

#functions for behavioral analysis

#%%
import os
import glob
import numpy as np
import math
from matplotlib import pyplot as plt
import matplotlib.cm as cm
from PIL import Image

#%%
path_name = 'C:\\Users\\Kacper\\Documents\\ASD_computational_ethology\\EPM_analysis'

file_names = glob.glob(path_name + '\\' + '*12000.csv')

#file_name = 'LM174MR_ctlDLC_resnet50_PlusMazeJul22shuffle1_12000.csv'
#file = path_name + '\\' + file_name

#%%
def fn_parameters_log (file, fps, calibration, left_x_border, right_x_border, upper_y_border, lower_y_border, limit):
    log_table = []
    log = ('file', 'fps', 'calibration', 'left_x_border', 'right_x_border', 'upper_y_border', 'lower_y_border', 'limit')
    log_table.append(log)
    log = (file, fps, calibration, left_x_border, right_x_border, upper_y_border, lower_y_border, limit)
    log_table.append(log)
    return log_table

def fn_sum (file, limit, param):
    lines = open(file).readlines()
    sum_file = 0
    for line in lines[0:limit]:
        record = float(line.split(',')[param].strip())
        sum_file = sum_file + record
    sum_file_list = [sum_file]
    return sum_file_list

def fn_average (file, limit, param):
    lines = open(file).readlines()
    sum_file = 0
    for line in lines[0:limit]:
        record = float(line.split(',')[param].strip())
        sum_file = sum_file + record
    average_file = sum_file / limit
    average_file_list = [average_file]
    return average_file_list

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
    

def fn_in_arm (file, left_x_border, right_x_border, upper_y_border, lower_y_border):
    in_arm_table = []
    lines = open(file).readlines()
    prev_armLeft = 0
    prev_armRight = 0
    prev_armUpper = 0
    prev_armLower = 0
    armLeft_entry = 0
    armRight_entry = 0
    armUpper_entry = 0
    armLower_entry = 0
    for line in lines[3:]:
        armLeft = 0
        armRight = 0
        armUpper = 0
        armLower = 0
        try: 
            neckx = fn_body_part ('neck', 'x', line)
            necky = fn_body_part ('neck', 'y', line)
            tailx= fn_body_part ('tail', 'x', line)
            taily = fn_body_part ('tail', 'y', line)
            if neckx < left_x_border and tailx < left_x_border:
                armLeft = 1
                if prev_armLeft == 0:
                    armLeft_entry = 1
                else:
                    armLeft_entry = 0
                
                prev_armLeft = armLeft
                prev_armRight = 0
                prev_armUpper = 0
                prev_armLower = 0
                    
            if necky < upper_y_border and taily < upper_y_border:
                armUpper = 1
                if prev_armUpper == 0:
                    armUpper_entry = 1
                else:
                    armUpper_entry = 0
                    
                prev_armUpper = armUpper
                prev_armRight = 0
                prev_armLeft = 0
                prev_armLower = 0
                    
            if neckx > right_x_border and tailx > right_x_border:
                armRight = 1
                if prev_armRight == 0:
                    armRight_entry = 1
                else:
                    armRight_entry = 0
                    
                prev_armRight = armRight
                prev_armLeft = 0
                prev_armUpper = 0
                prev_armLower = 0
                
            if necky > lower_y_border and taily > lower_y_border:
                armLower = 1
                if prev_armLower == 0:
                    armLower_entry = 1
                else:
                    armLower_entry = 0
                    
                prev_armLower = armLower
                prev_armRight = 0
                prev_armUpper = 0
                prev_armLeft = 0
                
            in_arm_record = (armLeft, armRight, armUpper, armLower, armLeft_entry, armRight_entry, armUpper_entry, armLower_entry)
            in_arm_table.append(in_arm_record)
            
        except ValueError:
            in_arm_table.append('NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN')
    return in_arm_table
    

print("done")


#%%

for file in file_names:
    print(file)

    #%%
    # video calibration
    
    limit = 7317
    try:
        parameters = open(file[0:-4]+'_parameters_log.csv').readlines()
        fps = float(parameters[1].split(',')[1].strip())
        calibration = float(parameters[1].split(',')[2].strip())
        #limit = float(parameters[1].split(',')[7].strip())
    except IOError: 
        fps = 24.39
        # arena measured from upper left to lower right corner
        arena_length_cm = 65 # 30+30+5
        arena_width_cm = 65 # 30+30+5
        arena_length_pxl = 976
        arena_width_pxl = 968
        calibration = ((arena_length_pxl / arena_length_cm) +  (arena_width_pxl / arena_width_cm)) / 2 #1cm = n pxl
        #limit = 7317
    
    #%%
    # bcg frame extraction
    #video_input = file[0:-4]+'_labeled.mp4'
    
    #video_input = file[0:-4]+'_labeled.mp4'
    #bcg_frame_name = file[0:-4]+'_frame01.png'
    bcg_frame_name = file[0:-44]+'_frame01.png'
    #os.system('ffmpeg -ss 00:00:01 -i {0} -vframes 1 -q:v 2 {1}'.format(video_input, bcg_frame_name))
    
    #%%
    try:
        parameters = open(file[0:-4]+'_parameters_log.csv').readlines()
        left_x_border = float(parameters[1].split(',')[3].strip())
        right_x_border = float(parameters[1].split(',')[4].strip())
        upper_y_border = float(parameters[1].split(',')[5].strip())
        lower_y_border = float(parameters[1].split(',')[6].strip())
    except IOError: 
        ULcorner = (926, 514)
        URcorner = (1000, 517)
        LRcorner = (1000, 597)
        LLcorner = (925, 597)
        left_x_border = 925
        right_x_border = 1000
        upper_y_border = 515
        lower_y_border = 597
    
    
    
    #%%
    np.savetxt(file[0:-4]+'_parameters_log.csv', 
               fn_parameters_log(file, fps, calibration, left_x_border, right_x_border, upper_y_border, lower_y_border, limit), 
               delimiter=',', fmt="%s")
    
    
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
    
    
    fn_save_bodypart_velocity_plot (file, 'body', bcg_frame_name)
    
    fn_save_bodypart_velocity_plot (file, 'nose', bcg_frame_name)
    
    np.savetxt(file[0:-4]+'_in_arm.csv', 
               fn_in_arm(file, left_x_border, right_x_border, upper_y_border, lower_y_border), 
               delimiter=',', fmt="%f")
    
    np.savetxt(file[0:-4]+'_in_arm_left_sum.csv', 
               fn_sum(file[0:-4]+'_in_arm.csv', limit, 0), 
               delimiter=',', fmt="%f")
    
    np.savetxt(file[0:-4]+'_in_arm_right_sum.csv', 
               fn_sum(file[0:-4]+'_in_arm.csv', limit, 1), 
               delimiter=',', fmt="%f")
    
    np.savetxt(file[0:-4]+'_in_arm_upper_sum.csv', 
               fn_sum(file[0:-4]+'_in_arm.csv', limit, 2), 
               delimiter=',', fmt="%f")
    
    np.savetxt(file[0:-4]+'_in_arm_lower_sum.csv', 
               fn_sum(file[0:-4]+'_in_arm.csv', limit, 3), 
               delimiter=',', fmt="%f")
    
    np.savetxt(file[0:-4]+'_entries_left_sum.csv', 
               fn_sum(file[0:-4]+'_in_arm.csv', limit, 4), 
               delimiter=',', fmt="%f")
    
    np.savetxt(file[0:-4]+'_entries_right_sum.csv', 
               fn_sum(file[0:-4]+'_in_arm.csv', limit, 5), 
               delimiter=',', fmt="%f")
    
    np.savetxt(file[0:-4]+'_entries_upper_sum.csv', 
               fn_sum(file[0:-4]+'_in_arm.csv', limit, 6), 
               delimiter=',', fmt="%f")
    
    np.savetxt(file[0:-4]+'_entries_lower_sum.csv', 
               fn_sum(file[0:-4]+'_in_arm.csv', limit, 7), 
               delimiter=',', fmt="%f")
    
    np.savetxt(file[0:-4]+'_body_distance_sum.csv', 
               fn_sum(file[0:-4]+'_body_distance.csv', limit, 0), 
               delimiter=',', fmt="%f")
    
    np.savetxt(file[0:-4]+'_body_velocity_average.csv', 
               fn_average(file[0:-4]+'_body_velocity.csv', limit, 0), 
               delimiter=',', fmt="%f")
