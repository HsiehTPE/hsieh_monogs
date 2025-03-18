"""
代码用途: 将EndoMapper Simulator数据集转换成给MonoGS模型(TUM)输入格式
作者: Hsieh Cheng-Tai @IRMV
邮箱: hsiehtpe_sjtu@sjtu.edu.cn
创建日期: 2025年3月17日
最后修改日期: 2025年3月18日
版权所有: © 2025 Hsieh Cheng-Tai @IRMV, 保留所有权利

使用说明:
1. 按照要求import库
2. 终端执行python文件, 同时需要指定目标数据集的路径，可以指定输出路径，默认与目标数据集统一路径
3. 执行后约10秒得到输出

注意事项:
- 该脚本针对的是EndoMapper Simulated Sequence Dataset, 数据集需要从Synapse网页上下来且未经处理
- 该脚本可以在执行时附加上选取帧的片段, 默认71_250
- 深度图按照作者要求进行了变换, 并分别储存为npy格式和png格式使用, 可以按照具体人物需求使用

Purpose: Convert EndoMapper Simulator dataset to the input format of MonoGS model(TUM)
Author: Hsieh Cheng-Tai @IRMV
email: hsiehtpe_sjtu@sjtu.edu.cn
Created Date: March 17, 2025
Last Modified Date: March 18, 2025
Copyright: © 2025 Hsieh Cheng-Tai @IRMV, All rights reserved

Usage Instructions:
1. Import the required libraries as specified.
2. Run the Python script from the terminal, specifying the path to the target dataset. \
    You can also specify the output path; by default, it is the same as the target dataset path.
3. The output will be generated in approximately 10 seconds.

Notes:
- This script is intended for the EndoMapper Simulated Sequence Dataset, \
    which needs to be downloaded from the Synapse website and should be unprocessed.
- You can specify the frame range to be selected when running the script; the default range is 71 to 250.
- The depth maps are transformed according to the author's requirements and saved in both npy and png formats. \
    You can use them according to your specific task requirements.
"""

# 你的代码从这里开始
# Your code starts here
import argparse
import os
import shutil
import csv
import OpenEXR
import glob
import numpy as np
from PIL import Image

def select_frames(input_folder, output_folder, start_frame, end_frame):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    depth_output_folder = os.path.join(output_folder, 'depth_exr')
    rgb_output_folder = os.path.join(output_folder, 'rgb')
    if not os.path.exists(depth_output_folder):
        os.makedirs(depth_output_folder)
    if not os.path.exists(rgb_output_folder):
        os.makedirs(rgb_output_folder)

    for frame_num in range(start_frame, end_frame + 1):
        exr_file = os.path.join(input_folder, 'depth', f'aov_image_{frame_num:04d}.exr')
        png_file = os.path.join(input_folder, 'rgb', f'image_{frame_num:04d}.png')
        
        if os.path.exists(exr_file):
            shutil.copy(exr_file, os.path.join(output_folder, 'depth_exr', f'{frame_num:08d}.exr'))
        if os.path.exists(png_file):
            shutil.copy(png_file, os.path.join(output_folder, 'rgb', f'{frame_num:08d}.png'))

def convert_trajectory(input_file, output_file, start_frame, end_frame):
    with open(input_file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        header = next(reader)  # Skip the header row
        data = list(reader)

    with open(output_file, 'w') as txtfile:
        filename_parts = os.path.basename(input_file).split('.')
        filename_prefix = '_'.join(filename_parts[-3:])  # 取倒数前3个部分作为前缀
        txtfile.write("# ground truth trajectory\n")
        txtfile.write("# file: '" + filename_prefix + "'\n")
        txtfile.write("# timestamp tx ty tz qx qy qz qw\n")
        
        for i in range(start_frame, end_frame + 1):
            row = data[i]
            timestamp = float(row[7])
            tx, ty, tz = row[0], row[1], row[2]
            qx, qy, qz, qw = row[3], row[4], row[5], row[6]
            txtfile.write(f"{timestamp} {tx} {ty} {tz} {qx} {qy} {qz} {qw}\n")

def convert_txt(input_file, rgb_output_file, depth_output_file, start_frame, end_frame):
    with open(input_file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        header = next(reader)  # Skip the header row
        data = list(reader)
    with open(rgb_output_file, 'w') as rgbtxtfile, open(depth_output_file, 'w') as depthtxtfile:
            rgbtxtfile.write("# color images\n")
            rgbtxtfile.write("# file: 'rgb.txt'\n")
            rgbtxtfile.write("# timestamp filename\n")
            depthtxtfile.write("# depth images\n")
            depthtxtfile.write("# file: 'depth.txt'\n")
            depthtxtfile.write("# timestamp filename\n")
            
            for i in range(start_frame, end_frame + 1):
                row = data[i]
                timestamp = float(row[7])
                rgbtxtfile.write(f"{timestamp} {os.path.join('rgb', f'{i:08d}.png')}\n")
                depthtxtfile.write(f"{timestamp} {os.path.join('depth', f'{i:08d}.png')}\n")

def read_exr(file_path):
    # Open the EXR file
    exr_file = OpenEXR.InputFile(file_path)
    
    # Get the header to extract size information
    header = exr_file.header()
    dw = header['dataWindow']
    width = dw.max.x - dw.min.x + 1
    height = dw.max.y - dw.min.y + 1
    
    # Define the channels to read
    channels = ['R']
    # for channel, info in header['channels'].items():
    #     print(f"通道: {channel}, 类型: {info}")

    # Read the pixel data for each channel
    channel_data = {}
    for channel in channels:
        channel_data[channel] = np.frombuffer(exr_file.channel(channel), dtype=np.float32).reshape(height, width)

    # Combine the channels into a single image
    image = np.stack([channel_data[channel] for channel in channels], axis=-1)

    return image

def convert_exr_to_npy(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    exr_files = glob.glob(os.path.join(input_folder, '*.exr'))
    for exr_file in exr_files:
        image = read_exr(exr_file)
        # print(image)

        # 进行转换  @pazagra, author of the endomapper dataset
        far_ = 4.0
        near_ = 0.01
        x = 1.0 - far_ / near_
        y = far_ / near_
        z = x / far_
        w = y / far_
        image = 1.0 / (z * (1 - image) + w)
        # # print(image, type(image), image.shape)
        image = image.reshape((720 , 960))
        # # print(image, type(image), image.shape)
        # # exit()

        npy_file_path = os.path.join(output_folder, os.path.splitext(os.path.basename(exr_file))[0] + '.npy')
        assert isinstance(image, np.ndarray)
        np.save(npy_file_path, image.astype(np.float32))
        # try:
        #     data = np.load(npy_file_path, allow_pickle=True)  # 尝试加载
        #     print("文件加载成功，数据类型：", type(data))
        #     print(data)
        #     exit()
        # except Exception as e:
        #     print("读取失败，错误信息：", e)
        # print(f"Saved {npy_file_path}")
        # with open(npy_file_path, "rb") as f:
        #     header = f.read(100)
        #     print(header)  # 查看文件头是否正确
        #     print(f)
        # exit()

def convert_npy_to_png(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    npy_files = glob.glob(os.path.join(input_folder, '*.npy'))
    for npy_file in npy_files:
        image = np.load(npy_file)
        image = (image - image.min() )/ (image.max() - image.min())  # Normalize to 0-1
        image = (image * 255).astype(np.uint8)  # Scale to 0-255 and convert to uint8
        image_pil = Image.fromarray(image)
        png_file_path = os.path.join(output_folder, os.path.splitext(os.path.basename(npy_file))[0] + '.png')
        image_pil.save(png_file_path)

def main():
    # 加载数据集信息
    parser = argparse.ArgumentParser(description="将EndoMapper Simulator数据集转换成给MonoGS模型(TUM)输入格式")
    parser.add_argument('--input_folder', type=str, required=True, \
                        help='输入需要转换的SimEndpmapper文件夹路径')
    parser.add_argument('--start_frame', type=int, required=False, default=71, help='开始帧编号')
    parser.add_argument('--end_frame', type=int, required=False, default=320, help='结束帧编号')
    
    args = parser.parse_args()
    input_folder = args.input_folder
    output_folder = input_folder + '_monogs'

    # 选取指定的帧
    select_frames(input_folder, output_folder, args.start_frame, args.end_frame)

    # 得到TUM格式下的各类txt文档
    trajectory_input_file = os.path.join(input_folder, 'trajectory.csv')
    groundtruth_output_file = os.path.join(output_folder, 'groundtruth.txt')
    convert_trajectory(trajectory_input_file, groundtruth_output_file, args.start_frame, args.end_frame)
    rgb_txt_file = os.path.join(output_folder, 'rgb.txt')
    depth_txt_file = os.path.join(output_folder, 'depth.txt')
    convert_txt(trajectory_input_file, rgb_txt_file, depth_txt_file, args.start_frame, args.end_frame)

    # 对simulated的exr格式深度进行处理
    convert_exr_to_npy(os.path.join(output_folder, 'depth_exr'), os.path.join(output_folder, 'depth_npy'))
    convert_npy_to_png(os.path.join(output_folder, 'depth_npy'), os.path.join(output_folder, 'depth'))

    print("Convert Finished.")

if __name__ == "__main__":
    main()