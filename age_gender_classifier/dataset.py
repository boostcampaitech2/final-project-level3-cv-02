import cv2
import numpy as np
import os
import os.path as osp
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
import albumentations as A
from albumentations.pytorch.transforms import ToTensorV2
import glob

class MLflowDataset:
    def __init__(self, root="./data/", transform=None):
        super().__init__()
        self.root = root
        self.data = []
        self.transform = transform
        exts = ["*.jpg", "*.png", "*.JPG", "*.PNG", "*.jpeg", "*.JPEG"]
        exts = [osp.join(self.root, "**", ext) for ext in exts]
        for ext in exts:
            self.data.extend(glob.iglob(ext, recursive=True))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        image_path = self.data[idx]
        image= cv2.imread(image_path, cv2.IMREAD_COLOR)
        image= cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        filename = image_path.split("/")[-1]
        if self.transform is not None:
            image= self.transform(image=image)["image"]
        return image, filename


def test_transform():
    return A.Compose([
        A.Resize(256, 256),            
        A.Normalize(
            [0.485, 0.456, 0.406],
            [0.229, 0.224, 0.225],
        ),
        ToTensorV2(),
    ])

def MLflowDataLoader(root = "./data", batch_size=128, num_workers=8, shuffle=False):
    dataset = MLflowDataset(root=root, transform=test_transform())
    return DataLoader(dataset, batch_size=batch_size, num_workers=num_workers,shuffle=shuffle)
    