import argparse

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Unsupported value encountered.')

def get_parser():
    # parameter priority: command line > config > default
    parser = argparse.ArgumentParser( description='Simulated Dataset')
 
    # file name/dir and dataset
    parser.add_argument('--output_dir', type=str, default="./Dataset/1PV/", help='output_skeletondata_dir')
    parser.add_argument('--input_data', type=str, default="./Dataset/3PV/raw_skes_data.pkl", help='input_skeletondata_filename')
    parser.add_argument('--detail_file', type=str, default="record.txt", help='')
    parser.add_argument('--info_file', type=str, default="info.pkl", help='')    
    parser.add_argument('--dataset', type=str, default="ntu", help='')
    parser.add_argument('--datapath', type=str, default="", help='')
    
    # camera parameter
    parser.add_argument('--camera_fps', type=int, default=30, help='camera fps')

    # routing parameter
    parser.add_argument('--routing_speed', type=float, default=4, help='camera moving speed')
    parser.add_argument('--rp', type=float, default=0.97, help='')
    parser.add_argument('--ver_speed', type=float, default=0.03, help='')
    parser.add_argument('--ver_highlimit', type=float, default=1, help='')
    parser.add_argument('--ver_lowlimit', type=float, default=-1, help='')
    parser.add_argument('--ver_space', type=float, default=0.3, help='')

    # viewing parameter
    parser.add_argument('--vp', type=float, default=0.97, help='')    
    parser.add_argument('--linear_hyper', type=float, default=1, help='')
    parser.add_argument('--pareto_xmin', type=float, default=2, help='')
    parser.add_argument('--pareto_k', type=float, default=2, help='')
    parser.add_argument('--log_mind', type=float, default=3.16, help='')
    parser.add_argument('--log_maxd', type=float, default=4.81, help='')
    parser.add_argument('--viewing_type', type=str,required=True, help='')
    parser.add_argument('--variance',type=int,default=4000,help='')

        #     parser.add_argument('', type=, default="", help='')

    
    return parser

