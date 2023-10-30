import numpy as np

def lookAtM(camera_pos,target_pos,up_pos):
    camera_pos = np.array(camera_pos)
    target_pos = np.array(target_pos)
    up_pos = np.array(up_pos)
    
    forward = target_pos - camera_pos 
    forward = forward if(np.linalg.norm(forward)==0) else forward/np.linalg.norm(forward)
    
    left= np.cross(up_pos,forward)
    left = left if(np.linalg.norm(left)==0) else left/np.linalg.norm(left)
    
    up = np.cross(forward,left)

    return [[left[0],up[0],forward[0],0],\
           [left[1],up[1],forward[1],0],\
           [left[2],up[2],forward[2],0],\
           [-left.dot(camera_pos),-up.dot(camera_pos),-forward.dot(camera_pos),1]]

# print(lookAtM([0,0,0],[1,1,1],[0,0,1]))

# print()
# pos = np.array([1,2,0])
# point1 = np.array([0,0,3])
# point2 = np.array([1,0,0])
# point3 = np.array([0,0,2])

# view = point1-pos
# M=lookAtM(pos,pos+view,[0,1,0])
# c_point1 = np.hstack([point1,np.array([1])]).dot(M)

# M=lookAtM(pos,pos+view,[0,1,0])
# c_point2 = np.hstack([point2,np.array([1])]).dot(M)

# M=lookAtM(pos,pos+view,[0,1,0])
# c_point3 = np.hstack([point3,np.array([1])]).dot(M)

# # print("original point: ",point)
# # print("pos: ",pos)
# # print("view: ",view)
# print("new point: ",c_point1)
# print("new point: ",c_point2)
# print("new point: ",c_point3)
# print(abs(np.linalg.norm(c_point1-c_point2)))
# print(abs(np.linalg.norm(c_point1-c_point3)))