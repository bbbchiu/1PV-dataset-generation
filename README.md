# 1PV dataset generation
this is the official github for 1PV dataset generation

## Method

## Implement Detail

### Dataset preparation
* Download the 3PV dataset, NTU60 [pdf](https://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Shahroudy_NTU_RGBD_A_CVPR_2016_paper.pdf)
    * download it by the [official website](https://rose1.ntu.edu.sg/dataset/actionRecognition/) 
    * or download it by the [github](https://github.com/shahroudy/NTURGB-D)

```

```

### Dataset Generation
* Files
```
args.py: contains tunable parameters, they can be changed by command line
routing.py: RWP routing method
viewing.py: viewing method
main.py: the main file
lookat.py: the camera coordinate transformation method
definition.py: definitions of NTU60 dataset
visualization.py: for 1PV dataset visualization
```