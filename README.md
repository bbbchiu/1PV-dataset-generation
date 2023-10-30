# 1PV dataset generation
this is the official github for 1PV dataset generation

## Method
We aim to simulate a first-person view (1PV) dataset by third-person view (3PV) dataset. 

## Implement Detail


### Dataset preparation
* Download the 3PV dataset, NTU60 [pdf](https://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Shahroudy_NTU_RGBD_A_CVPR_2016_paper.pdf)
    * download it by the [official website](https://rose1.ntu.edu.sg/dataset/actionRecognition/) 
    * or download it by the [github](https://github.com/shahroudy/NTURGB-D)

* download the 3PV dataset and  transform it into pkl file, place it in the ./Dataset/3PV/ 
    * or you can place it whatever, and remember to modify the input data in the ./data generation/args.py or use command line to correct the input data path

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

* command line for generate a 1PV dataset
```
python ../data generation/main.py --output_dir=./Dataset/1PV/ --viewing_type=log --routing_speed=4
```