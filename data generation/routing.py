import random
import numpy as np
import math
from args import get_parser

class RANDOM_ROUTING:
    def __init__(self,init_pos,frames):
        self.angle = [0,0]
        self.pos = init_pos
        self.frames = frames
        
        parser = get_parser()
        arg = parser.parse_args()
        self.arg = arg
        
        # adjustment value
        self.speed = self.arg.routing_speed
        self.camera_fps = self.arg.camera_fps
        self.f_speed = self.speed*(1000/3600)/self.camera_fps #m/frame 
        self.p = self.arg.rp
        self.ver_speed = self.arg.ver_speed
        self.ver_hlimit = self.arg.ver_highlimit
        self.ver_llimit = self.arg.ver_lowlimit
        self.ver_space = self.arg.ver_space
        
    def get_routing(self): # main
        route = np.zeros((self.frames,3),dtype=np.float64)
        angle_out = np.zeros((self.frames,2),dtype=np.float64)
        
        self.walk_dir = -1
        walk_flag = False
        cal = 0
        for frame_idx in range(self.frames):
            if(frame_idx == 0): # first frame
                route[frame_idx,:] = self.pos
                angle_out[frame_idx,:] = self.angle
                continue
            if(self.walk_dir == -1):
                self.walk_dir = random.randint(0,36000)/100*math.pi/180
                walk_flag = True
                cal += 1
            else:
                if(walk_flag):
                    if(self.p**cal>random.randint(0,100)/100): #keep walking
                        cal+=1
                    else: # waiting
                        walk_flag = False
                        cal = 0
                else:
                    if(self.p**cal>random.randint(0,100)/100): #keep waiting
                        cal+=1
                    else:
                        self.walk_dir = random.randint(0,36000)/100*math.pi/180 #start walking and given new direction
                        walk_flag = True
                        cal = 0
                
            self.update_pos()
            route[frame_idx,:] = self.pos
            angle_out[frame_idx,:] = self.angle
            
        return route,angle_out
    
    def update_pos(self):
        # turn degree into radian
        self.angle = [self.walk_dir,0]
        
        # hor pos
        self.pos[0] += self.f_speed*math.cos(self.walk_dir)
        self.pos[2] += self.f_speed*math.sin(self.walk_dir)

        # ver pos
        sign = random.randint(0,1)
        if(sign == 1):
            self.pos[1] += np.random.normal(self.ver_speed,self.ver_speed*3/20)
        elif(sign == 0):
             self.pos[1] -= np.random.normal(self.ver_speed,self.ver_speed*3/20)
        else:
            pass

        # ver pos restriction
        if(self.pos[1]>=self.ver_hlimit):
            self.pos[1] = self.ver_hlimit-self.ver_space
        elif(self.pos[1]<= self.ver_llimit):
            self.pos[1] = self.ver_llimit+self.ver_space
#         print(self.pos)         
        