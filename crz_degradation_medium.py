
import cv2
import numpy as np
import os
import pprint
import random
import time
import torch
from PIL import Image
from scipy.io import loadmat


def AddBlur(img): # gaussian blur or motion blur
    img = np.array(img)
    if random.random() > -1: ##gaussian blur
        blursize = 9 
        blursigma = 10
        img = cv2.GaussianBlur(img, (blursize,blursize), blursigma/10)
    else: #motion blur
        M = random.randint(1,32)
        KName = './data/MotionBlurKernel/m_%02d.mat' % M
        k = loadmat(KName)['kernel']
        k = k.astype(np.float32)
        k /= np.sum(k)
        img = cv2.filter2D(img,-1,k)
    return Image.fromarray(img)

def AddDownSample(img, size): # downsampling
    sampler = 30.0
    img = img.resize((int(size[0]/sampler*10.0), int(size[1]/sampler*10.0)), Image.BICUBIC)
    return img


def AddJPEG(img): # JPEG compression
    imQ = 60
    img = np.array(img)
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY),imQ] # (0,100),higher is better,default is 95
    _, encA = cv2.imencode('.jpg',img,encode_param)
    img = cv2.imdecode(encA,1)
    return Image.fromarray(img)

def AddNoise(img): # noise
    sigma = 5
    img_tensor = torch.from_numpy(np.array(img)).float()
    noise = torch.ones(img_tensor.size()).mul_(sigma/1.0)

    noiseimg = torch.clamp(noise+img_tensor,0,255)
    return Image.fromarray(np.uint8(noiseimg.numpy()))

def AddUpSample(img, size):
    return img.resize(size, Image.BICUBIC)

def img_deg(img, choice=1):
    
    ori_size = img.size

    # 添加模糊
    img = AddBlur(img)

    # downsampling
    img = AddDownSample(img, ori_size)

    # add noise
    img = AddNoise(img)

    # add JPEG
    img = AddJPEG(img)

    # upsampling
    img = AddUpSample(img, ori_size)

    return img
    


def read_imgs(dataset):
    paths = []
    if dataset == "wflw":
        PATH = "./data/wflw/images"
        folders = os.listdir(PATH)
        for folder in folders:
            sub_folder = PATH + "/" + folder
            img_names = os.listdir(sub_folder)
            for img_name in img_names:
                img_path = sub_folder + "/" + img_name
                paths.append(img_path)
        return paths

if __name__ == "__main__":
    paths = read_imgs("wflw")
    for path in paths:
        img = cv2.read(path)
        img = img_deg(img, choice=0.5)
    