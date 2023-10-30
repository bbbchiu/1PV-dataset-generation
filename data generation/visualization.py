import numpy as np
import matplotlib.pyplot as plt
import math
import pickle
import random

class VISUAL:
    def __init__(self):
        pass
    
    def get_random_data(self,datapath):
        with open(datapath, 'rb') as fr:
            self.info = pickle.load(fr)  # a list
        print(len(self.info))

        self.index = random.randint(0,len(self.info))

    def plt_rv(self,datapath,ratio):
        self.get_random_data(datapath)
        
        routing = self.info[self.index]['routing']
        viewing = self.info[self.index]['viewing']
#         skeleton = self.info[self.index]['skeleton']
        
        print(self.index)
        
        plt.figure()
        ax = plt.axes(projection='3d')
#         ax.view_init()
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        
        # yz opposite
#         temp = skeleton.copy()
#         skeleton[:,1] = skeleton[:,2]
#         skeleton[:,2] = temp[:,1]
        
        temp = routing.copy()
        routing[:,1] = routing[:,2]
        routing[:,2] = temp[:,1]
        
        temp = viewing.copy()
        viewing[:,1] = viewing[:,2]
        viewing[:,2] = temp[:,1]
        
#         ax.plot3D(skeleton[:,0],skeleton[:,1],skeleton[:,2]) # skeleton
        ax.plot3D(routing[:,0],routing[:,1],routing[:,2],'r') # routing
        for index,i in enumerate(viewing):
            if(index == 0):
                i =  i/np.linalg.norm(i)*ratio
                ax.plot3D([routing[index,0],routing[index,0]+i[0]],\
                          [routing[index,1],routing[index,1]+i[1]],\
                          [routing[index,2],routing[index,2]+i[2]],'b')
                continue
            if((i == viewing[index-1]).all()):
                continue
            i =  i/np.linalg.norm(i)*ratio
            ax.plot3D([routing[index,0],routing[index,0]+i[0]],\
                          [routing[index,1],routing[index,1]+i[1]],\
                          [routing[index,2],routing[index,2]+i[2]],'b')
            
            ax.legend(['routing','viewing'])
    
    def get_missing_info(self,datapath):
        missing_cnt= 0
        all_frame = 0
        
        data_missing_cnt = np.zeros((300,))
#         data_missing_rcnt = np.zeros((10001,))
        data_missing_rcnt = np.zeros((101,))
        max_r = 0
        with open(datapath, 'rb') as fr:
            data = pickle.load(fr)  # a list
        print(len(data))
        self.skeleton_arr = []
        for s_index,skeleton in enumerate(data):
            for index_num, index_key in enumerate(list(skeleton['data'].keys())):
                frame_num = int(skeleton['data'][str(index_key)]['joints'].shape[0]/25)
                all_frame += frame_num
                skeleton_joints = skeleton['data'][str(index_key)]['joints'].reshape((frame_num,25,3))
                
                data_miss = 0
                for index,frame in enumerate(skeleton_joints):
                    if((frame == 0).all()):
                        missing_cnt += 1
                        data_miss += 1
                data_missing_cnt[data_miss]+=1
                
#                 ratio = int((data_miss/frame_num)*10000)
                ratio = int((data_miss/frame_num)*100)
                data_missing_rcnt[ratio] += 1
                if(ratio>max_r):
                    max_r = ratio
        print(missing_cnt,all_frame,missing_cnt/all_frame*100,max_r)
        
        self.data_missing_cnt = data_missing_cnt
        self.data_missing_rcnt = data_missing_rcnt
        self.max_r = max_r
        
    def plot_missing_frame(self):
        plt.figure()
        x = list(range(self.data_missing_cnt.shape[0]))
        plt.bar(x,self.data_missing_cnt)
        plt.xlabel('data missing frames')
        plt.ylabel('data num')
        plt.show()
        
        plt.figure()
        x = list(range(self.data_missing_cnt.shape[0]))
        y = []
        cal = 0
        for index,i in enumerate(self.data_missing_cnt):
            if(index == 0):
                y.append(0)
                continue
            cal += index*i
            y.append(cal)
        plt.plot(x,y)
        plt.xlabel('data missing frames')
        plt.ylabel('cumulative distribution function (missing frames)')
        plt.show()
        
        plt.figure()
        x = list(range(self.data_missing_cnt.shape[0]))
        y = []
        cal = 0
        for index,i in enumerate(self.data_missing_cnt):
            if(index == 0):
                y.append(0)
                continue
            cal += i
            y.append(cal)
        plt.plot(x,y)
        plt.xlabel('data missing frames')
        plt.ylabel('cumulative distribution function (missing data)')
        plt.show()
            
        plt.figure()
        x = np.array(list(range(1,self.max_r+1)))
        plt.bar(x,self.data_missing_rcnt[x])
        plt.xlabel('data missing frames ratio (%)')
        plt.ylabel('data num')
        plt.show()
        
        plt.figure()
        x = np.array(list(range(self.max_r+1)))
        y = []
        cal = 0
        for index,i in enumerate(self.data_missing_rcnt[:x.shape[0]+1]):
            if(index == 0):
                y.append(0)
                continue
            cal += i
            y.append(cal)
        
        plt.plot(x,y)
        plt.xlabel('data missing frames ratio (%)')
        plt.ylabel('cumulative distribution function')
        plt.show()
        
    def missing_block(self,datapath):
        with open(datapath, 'rb') as fr:
            data = pickle.load(fr)  # a list
        print(len(data))

        data_missing_cnt = np.zeros((20,))
        data_missing_len = np.zeros((200,))
        missing_block_sum = 0
        
        for s_index,skeleton in enumerate(data):
            for index_num, index_key in enumerate(list(skeleton['data'].keys())):
                frame_num = int(skeleton['data'][str(index_key)]['joints'].shape[0]/25)
                skeleton_joints = skeleton['data'][str(index_key)]['joints'].reshape((frame_num,25,3))
                
                data_miss = 0
                miss_flag = False
                miss_cnt = 0
                miss_len = 0
                for index,frame in enumerate(skeleton_joints):
                    if((frame == 0).all() and miss_flag == False):
                        miss_flag = True
                        miss_cnt += 1
                        miss_len = 1
                    elif((frame == 0).all() and miss_flag == True):
                        miss_len += 1
                    elif((frame != 0).any() and miss_flag == True):
                        miss_flag = False
                        data_missing_len[miss_len] += 1
                    else:
                        continue
                data_missing_cnt[miss_cnt] += 1
                missing_block_sum += miss_cnt
                
        self.missing_block = data_missing_cnt
        self.missing_len = data_missing_len
        self.miss_block_sum = missing_block_sum
        
    def plot_missing_block(self):
        plt.figure()
        x = list(range(self.missing_block.shape[0]))
        plt.bar(x,self.missing_block)
        plt.xlabel('num of missing blocks')
        plt.ylabel('data num')
        plt.show()
        
        plt.figure()
        x = list(range(self.missing_block.shape[0]))
        y = []
        cal = 0
        for index,i in enumerate(self.missing_block):
            cal += i
            y.append(cal)
        plt.plot(x,y)
        plt.xlabel('num of missing blocks')
        plt.ylabel('cumulative distribution function')
        plt.show()

        print(self.miss_block_sum)
        
        plt.figure()
        x = np.array(list(range(self.missing_len.shape[0])))
        plt.bar(x,self.missing_len)
        plt.xlabel('num of missing block length')
        plt.ylabel('block num')
        plt.show()
        
        plt.figure()
        x = list(range(self.missing_len.shape[0]))
        y = []
        cal = 0
        for index,i in enumerate(self.missing_len):
            cal += i
            y.append(cal)
        plt.plot(x,y)
        plt.xlabel('num of missing blocks length')
        plt.ylabel('cumulative distribution function')
        plt.show()