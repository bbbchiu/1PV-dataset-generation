import numpy as np
import math
import cv2
import pickle
import matplotlib.pyplot as plt
import random
import copy
import os
from datetime import datetime

import definition
from args import get_parser
from lookat import lookAtM
from routing import RANDOM_ROUTING
from viewing import VIEWING

start_time = datetime.now()
print("dataset generation ~")
## definition
definition.init()

## arg parser
parser = get_parser()
arg = parser.parse_args()

# parameter transform
target_filepos = arg.output_dir
viewing_type = arg.viewing_type
dataset=arg.dataset
datapath=arg.input_data
detailpath = arg.detail_file
dataInfopath = arg.info_file

# other definition (make dir)
if(not os.path.isdir(target_filepos+viewing_type+"/")):
    os.makedirs(target_filepos+viewing_type)
    target_filepos = target_filepos+viewing_type+"/"
else:
    cnt = 0
    while(os.path.isdir(target_filepos+viewing_type +"_"+str(cnt)+"/")):
        cnt += 1
        if(cnt >= 100):
            break
    os.makedirs(target_filepos+viewing_type +"_"+str(cnt)+"/")
    target_filepos = target_filepos+viewing_type +"_"+str(cnt)+"/"
target_file_name = target_filepos+"dataset.pkl"
    
## initialize dataset 
print("Input dataset path: "+datapath)
print("Output dataset path: "+target_file_name)

print("")
print("Starting~")

ntu60_bones = definition.bone_pairs[arg.dataset]
## prepare dataset
bones = definition.bone_pairs[arg.dataset]

with open(datapath, 'rb') as fr:
    ntu60_skes_joints = pickle.load(fr)  # a list
print(len(ntu60_skes_joints))

data = ntu60_skes_joints
new_data = copy.deepcopy(data)

# detail definition
data_cnt = 0
skeleton_cnt = 0
frame_cnt = 0
missing_frame_cnt = 0
missing_data_cnt = 0

max_x = 0
max_y = 0
max_z = 0

data_info = []

for s_index,skeleton in enumerate(data):
    if(s_index%10000 == 0):
        print(s_index)

    data_cnt += 1
    skeleton_cnt += len(list(skeleton['data'].keys()))
    for index_num, index_key in enumerate(list(skeleton['data'].keys())):
        d_flag = False 

        frame_num = int(skeleton['data'][str(index_key)]['joints'].shape[0]/25)
        skeleton_joints = skeleton['data'][str(index_key)]['joints'].reshape((frame_num,25,3))
        new_skeleton = np.zeros(skeleton_joints.shape)

        ## routing and viewing
        camera = RANDOM_ROUTING(init_pos=[0,0,0],frames=skeleton_joints.shape[0])
        route,angle = camera.get_routing()

        if(max(route[:,0])>max_x):
            max_x = max(route[:,0])
        if(max(route[:,1])>max_y):
            max_y = max(route[:,1])
        if(max(route[:,2])>max_z):
            max_z = max(route[:,2])
            
        v = VIEWING(skeleton_joints,route)
        view_arr = v.get_viewing() 

        dic = {'routing':route,'viewing':view_arr,'skeleton':skeleton_joints[:,2,:]}
        data_info.append(dic)
        
        frame_cnt += frame_num
        for index,frame in enumerate(skeleton_joints):
            M = lookAtM(route[index],route[index]+view_arr[index],[0,1,0])

            temp = frame
            temp = np.hstack([skeleton_joints[index],np.array([[1]]*25)])
            temp = temp.dot(M)

            cnt = 0
            for single_joint in temp:
#                 print(single_joint[0],single_joint[2],single_joint[2]*math.tan(35*math.pi/180))
                if(single_joint[2]<0 or\
                   single_joint[0]<-abs(single_joint[2]*math.tan(35*math.pi/180)) or\
                   single_joint[0]>abs(single_joint[2]*math.tan(35*math.pi/180)) or\
                   single_joint[1]<-abs(single_joint[2]*math.tan(30*math.pi/180)) or\
                   single_joint[1]>abs(single_joint[2]*math.tan(30*math.pi/180))):
                    cnt += 1

            if(cnt == len(temp)):
                temp = np.zeros(temp.shape)
            new_skeleton[index] = temp[:,:3]
            if((new_skeleton[index] == 0).all()):
                missing_frame_cnt+=1
                if(not d_flag):
                    missing_data_cnt += 1
                    d_flag = True

        new_data[s_index]['data'][str(index_key)]['interval'] = list(range(new_skeleton.shape[0]))
        new_data[s_index]['data'][str(index_key)]['num_frames'] = new_skeleton.shape[0]
        new_data[s_index]['data'][str(str(index_key))]['joints'] = new_skeleton.reshape((new_skeleton.shape[0]*25,3))

print()
print("data writing~")
        
with open(target_file_name, 'wb') as fr:
    pickle.dump(new_data,fr)  # a list

with open(target_filepos+dataInfopath, 'wb') as fr:
    pickle.dump(data_info,fr) 

# make dataset detail txt file
with open(target_filepos+detailpath,"w") as f:
    f.write("Dataset Detail Information: \n")
    f.write("Dataset: "+dataset+"\n")
    f.write("Dataset Path: "+datapath+"\n")
    f.write("Viewing Type: "+arg.viewing_type+"\n")
    f.write("Data Num: "+str(data_cnt)+" ; Skeleton Num: "+str(skeleton_cnt)+" ; Frame Num: "+str(frame_cnt)+"\n")
    f.write("Missing Data Num: "+str(missing_data_cnt)+" ; Missing Frame Num: "+str(missing_frame_cnt)+"\n")
    f.write("\n")
    
    f.write("Camera Information: \n")
    f.write("Camera FPS: "+str(arg.camera_fps)+"\n")
    f.write("\n")
    
    f.write("Routing Information: \n")
    f.write("Routing Speed: "+str(arg.routing_speed)+"\n")
    f.write("Routing Possiblity: "+str(arg.rp)+"\n")
    f.write("Max camera x: "+str(max_x)+" ; ")
    f.write("Max camera y: "+str(max_y)+" ; ")
    f.write("Max camera z: "+str(max_z)+"\n")
    f.write("Vertical Speed: "+str(arg.ver_speed)+"\n")
    f.write("Vertical highest limit: "+str(arg.ver_highlimit)+"\n")
    f.write("Vertical lowest limit: "+str(arg.ver_lowlimit)+"\n")
    f.write("Vertical Space: "+str(arg.ver_space)+"\n")
    f.write("\n")
    
    f.write("Viewing Information: \n")
    f.write("Linear Distribution Hyperparameter: "+str(arg.linear_hyper)+"\n")
    f.write("Pareto Distibution Min Value: "+str(arg.pareto_xmin)+"\n")
    f.write("Pareto Distibution K Value: "+str(arg.pareto_k)+"\n")
    f.write("Log Min Distance: "+str(arg.log_mind)+"\n")
    f.write("Log Max Distance: "+str(arg.log_maxd)+"\n")
    f.write("Viewing Possiblity: "+str(arg.vp)+"\n")
    f.write("Variance: "+str(arg.variance)+"\n")
    f.write("\n")
        
end_time = datetime.now()
print()
print("Take Time: "+str(end_time-start_time)+" secs")
print("over")
