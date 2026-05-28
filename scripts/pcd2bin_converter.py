import os
import argparse
import numpy as np
from pypcd import pypcd
from tqdm import tqdm


def convert_all(in_path:str, out_path:str):
    
    if os.path.isdir(in_path):
        filenames = os.listdir(in_path)
        for filename in tqdm(filenames, 'Converting pcd\'s'):
            if filename[-4:] != '.pcd':
                continue
            pcd_data = pypcd.PointCloud.from_path(in_path+'/'+filename)
            points = np.zeros([pcd_data.width, 4], dtype=np.float32)
            points[:, 0] = pcd_data.pc_data['x'].copy()
            points[:, 1] = pcd_data.pc_data['y'].copy()
            points[:, 2] = pcd_data.pc_data['z'].copy()
            points[:, 3] = pcd_data.pc_data['rgb'].copy().astype(np.float32)
            with open(out_path + '/'+ filename[:-4] +'.bin', 'wb') as f:
                f.write(points.tobytes())
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Converts a single or multiple pointclouds form '.pcd' to '.bin' format.")
    parser.add_argument('--in_path', type=str, action='store',
        help="Path to directory containing the '.pcd' pointclouds to be converted into '.bin'")
    parser.add_argument('--out_path', type=str, action='store',
        help="Path to the directory where the converted '.bin' pointclouds will be saved")
    args = parser.parse_args()

    convert_all(in_path=args.in_path, out_path=args.out_path)