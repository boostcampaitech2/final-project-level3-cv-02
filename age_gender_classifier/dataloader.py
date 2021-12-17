import cv2
import numpy as np
import os
import os.path as osp
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, ConcatDataset
import albumentations as A
from albumentations.pytorch.transforms import ToTensorV2
from aafd import AAFD
from utkface import UTKFace

def train_transform():
    return A.Compose([
        A.Resize(256, 256),
        A.HorizontalFlip(),
        A.Normalize(
            [0.485, 0.456, 0.406],
            [0.229, 0.224, 0.225],
        ),
        A.Cutout(),
        ToTensorV2(),
    ])

def test_transform():
    return A.Compose([
        A.Resize(256, 256),            
        A.Normalize(
            [0.485, 0.456, 0.406],
            [0.229, 0.224, 0.225],
        ),
        ToTensorV2(),
    ])

def AAFDDataLoader(mode="train"):
    assert mode in ["train", "val"]
    if mode=="train":
        dataset = AAFD(mode="train", transform=train_transform())
        return DataLoader(dataset, batch_size=128, num_workers=8,shuffle=True)
    else:
        dataset = AAFD(mode="val", transform=test_transform())
        return DataLoader(dataset, batch_size=128, num_workers=8,shuffle=False)  

def UTKFaceDataLoader(mode="train"):
    assert mode in ["train", "val"]
    if mode=="train":
        dataset = UTKFace(mode="train", transform=train_transform())
        return DataLoader(dataset, batch_size=128, num_workers=8,shuffle=True)
    else:
        dataset = UTKFace(mode="val", transform=test_transform())
        return DataLoader(dataset, batch_size=128, num_workers=8,shuffle=False)  

def FullDataLoader(mode="train"):
    assert mode in ["train", "val"]
    if mode=="train":
        aafd = AAFD(mode="train", transform=train_transform())
        utkface = UTKFace(mode="train", transform=train_transform())
        dataset = ConcatDataset([aafd, utkface])
        return DataLoader(dataset, batch_size=128, num_workers=8,shuffle=True)
    else:
        aafd = AAFD(mode="val", transform=test_transform())
        utkface = UTKFace(mode="val", transform=test_transform())
        dataset = ConcatDataset([aafd, utkface])
        return DataLoader(dataset, batch_size=128, num_workers=8,shuffle=False)  