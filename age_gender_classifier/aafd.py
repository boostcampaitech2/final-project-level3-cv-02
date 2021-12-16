import cv2
import numpy as np
import os
import os.path as osp
import torch
import torch.nn as nn
from torch.utils.data import Dataset

def get_age_label(age):
    # 0~20
    if age < 18:
        return 0
    # 20~30
    elif 18 <= age < 27:
        return 1
    # 30~40
    elif 27 <= age < 39:
        return 2
    # 40~60
    elif 39 <= age < 60:
        return 3
    # 60~
    elif 60 <= age:
        return 4
    
class AAFD(Dataset):
    def __init__(self, root="./data/AAFD", mode="train", transform=None):
        super().__init__()
        
        assert mode in ["train", "val"]
        self.root = root
        self.mode = mode
        self.transform = transform
        self.data = []

        path = osp.join(self.root, "init_"+mode+".txt")
        with open(path, "r") as f:
            meta = f.readlines()
        for m in meta:
            image_path, gender = m.split()
            gender = int(gender)
            age = int(image_path.split(".")[0][-2:])
            image_path = osp.join(self.root, "images", image_path)
            self.data.append([image_path, gender, age])
    
    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        image_path, gender, age = self.data[idx]
        image= cv2.imread(image_path, cv2.IMREAD_COLOR)
        image= cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # age = age_group[age//10]
        age =get_age_label(age)
        label = age * 2 + gender

        if self.transform is not None:
            image= self.transform(image=image)["image"]
        return image, label
