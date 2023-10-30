import random
import numpy as np
import math
import time
import cv2
from args import get_parser

class VIEWING:
    def __init__(self,skeleton,routing):
        self.skeleton = skeleton
        self.routing = routing
        self.frames = self.skeleton.shape[0]
        self.target_point = self.skeleton[0,2,:]
        self.skeleton_view_len = np.linalg.norm(self.target_point-self.routing[0,:])
        
        self.random_cnt = 0
        self.attention_cnt = 0
        
        parser = get_parser()
        arg = parser.parse_args()
        self.arg = arg
        
        #adjustment
        self.viewing_type = self.arg.viewing_type
        self.linear_hyper = self.arg.linear_hyper
        self.pareto_xmin = self.arg.pareto_xmin
        self.pareto_k = self.arg.pareto_k
        self.log_mind = self.arg.log_mind
        self.log_maxd = self.arg.log_maxd
        self.vp = self.arg.vp

    def set_linear_ratio(self,frame):
        frame_dis = abs(np.linalg.norm(self.routing[frame]-self.skeleton[frame,2,:]))

        self.ratio = 1-((frame_dis-self.log_mind)/(self.log_maxd-self.log_mind))
        if(self.ratio < 0):
            self.ratio = 0
        elif(self.ratio > 1):
            self.ratio = 1
        else:
            pass
        
    def set_pareto_ratio(self,frame):
        frame_dis = abs(np.linalg.norm(self.routing[frame]-self.skeleton[frame,2,:]))
        
        if(frame_dis-self.dis<=self.pareto_xmin):
            self.ratio = 1
        else:
            self.ratio = (self.pareto_k*(self.pareto_xmin**self.pareto_k))/(frame_dis**(self.pareto_k+1))

    def set_log_ratio(self,frame):
        frame_dis = abs(np.linalg.norm(self.routing[frame]-self.skeleton[frame,2,:]))
        
        try:
            self.ratio = (math.log(self.log_maxd+1-frame_dis))/(math.log(self.log_maxd+1-self.log_mind))
            if(self.ratio > 1):
                self.ratio = 1
            elif(self.ratio < 0):
                self.ratio = 0
        except:
            self.ratio = 0

# main
    def get_viewing(self):
        self.view_arr_lookat = np.zeros((self.routing.shape))

        view_flag = True
        cal = 1
        for frame in range(self.view_arr_lookat.shape[0]):         
            if(frame == 0): #initial viewing
                self.view_arr_lookat[frame] = self.target_point-self.routing[frame]
                continue
            if(frame == self.view_arr_lookat.shape[0]-1):
                self.view_arr_lookat[frame] = self.view_arr_lookat[frame-1]
                continue
                
            if(view_flag): # get a new viewing
                self.get_new_viewing(frame)
                cal = 1
                view_flag = False
            else: # keep viewing or not?
                self.view_arr_lookat[frame] = self.view_arr_lookat[frame-1]
                if(self.vp**cal>random.randint(0,1000)/1000): # keep waiting
                    cal+=1
                else: # change to viewing
                    view_flag = True

        return self.view_arr_lookat
        
    def get_new_viewing(self,frame):
        # get distance to ratio
        if(self.viewing_type == 'linear'):
            self.set_linear_ratio(frame)
        elif(self.viewing_type == 'pareto'):
            self.dis = self.skeleton_view_len
            self.set_pareto_ratio(frame)
        elif(self.viewing_type == 'log'):
            self.set_log_ratio(frame)
        else:
            print("Error: Error Viewing Type Providing")
            
        if(frame == 0):
            mean = 0
    
        prevousVv = self.view_arr_lookat[frame-1]
        prevousVv_len = abs(np.linalg.norm(prevousVv))
        currentCSv = self.skeleton[frame,2,:]-self.routing[frame]
        currentCSv_len = abs(np.linalg.norm(currentCSv))
        if(prevousVv_len == 0 or currentCSv_len == 0):
            mean = 0
        else:
            mean = math.acos(round(np.dot(prevousVv,currentCSv)/(prevousVv_len*currentCSv_len),5))*180/math.pi
            mean = mean*(1-self.ratio)
            
        variance = self.arg.variance*(1.1-self.ratio)
        
        randomAngle = np.random.normal(mean,variance**(1/2))
        if(randomAngle > 90):
            randomAngle = 90
        elif(randomAngle < -90):
            randomAngle = -90
        else:
            pass

        # set viewing        
        rv = prevousVv
        rs = currentCSv
        angle = randomAngle
        law = np.cross(rs,rv)
        if(abs(np.linalg.norm(law))==0):
            R = np.array([[1,0,0],[0,1,0],[0,0,1]])
        else:
            law = law/abs(np.linalg.norm(law))*angle*math.pi/180
            R,_ = cv2.Rodrigues(law)
        self.view_arr_lookat[frame] = np.dot(rs,R)

        
        
        
        
        
#         # get viewing distribution
#         meanV = 0
#         varianceV = ((1-self.ratio/10)+0.1)*1000
# #         y1 = math.e**(-(x-mean1)**2/(2*variance1))/(2*math.pi*variance1)**(1/2)

#         # get previous distribution
#         if(frame == 0):
#             meanP = 0
#         prevousVv = self.view_arr_lookat[frame-1]
#         prevousVv_len = abs(np.linalg.norm(prevousVv))
#         currentCSv = self.skeleton[frame,2,:]-self.routing[frame]
#         currentCSv_len = abs(np.linalg.norm(currentCSv))
        
#         if(prevousVv_len == 0 or currentCSv_len == 0):
#             meanP = 0
#         else:
#             meanP = math.acos(round(np.dot(prevousVv,currentCSv)/(prevousVv_len*currentCSv_len),5))*180/math.pi
#         varianceP = self.arg.varianceP

#         meanFinal = (meanV + meanP)/2
#         varianceFinal = (varianceV + varianceP)/2