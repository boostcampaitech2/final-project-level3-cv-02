import cv2
import numpy as np
import os
import os.path as osp
import torch
import torch.nn as nn
from torch.utils.data import Dataset
from sklearn.model_selection import train_test_split
import glob
import dlib
# 0 : ~19 female
# 1 : ~19 male
# 2 : 20~29 female
# 3 : 20~29 male
# 4 : 20~29 female
# 5 : 30~39 male
# 6 : 30~39 female
# 7 : 40~59 male
# 8 : 60~ female
# 9 : 60~ male

def get_age_label(age):
    # 0~20
    if age < 20:
        return 0
    # 20~30
    elif 20 <= age < 30:
        return 1
    # 30~40
    elif 30 <= age < 40:
        return 2
    # 40~60
    elif 40 <= age < 60:
        return 3
    # 60~
    elif 60 <= age:
        return 4
    
class UTKFace(Dataset):
    def __init__(self, root="./data/UTKFace", mode="train", transform=None):
        super().__init__()
        
        assert mode in ["train", "val"]
        self.root = root
        self.mode = mode
        self.transform = transform
        self.data = []

        self.detector = dlib.get_frontal_face_detector()
        data_path = []
        exts = ["*.png", "*.PNG"]
        exts = [osp.join(self.root, "**", ext) for ext in exts]

        for ext in exts:
            data_path.extend(glob.iglob(ext, recursive=True))
        train_path, val_path = train_test_split(data_path, train_size=0.8, random_state=42)
        
        if mode == "train":
            self.data = train_path
        else:
            self.data = val_path
    
    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        image_path = self.data[idx]
        image= cv2.imread(image_path, cv2.IMREAD_COLOR)
        image= cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        try:
            face = self.detector(image)[0]
            top = max(0, face.top()-5)
            bottom = min(face.bottom()+5, image.shape[0])
            left = max(0, face.left()-5)
            right = min(face.right()+5, image.shape[1])
            image = image[top:bottom, left:right]
        except IndexError:
            pass
        

        filename = image_path.split("/")[-1]
        age, gender, race, _ = filename.split("_")

        # UTFK에서는 0이 male, 1이 female
        # AAFD는 0이 female, 0이 male
        # 통일성을 위해 0을 female, 1을 male로 변환
        gender = 0 if gender == "1" else 1
        age = get_age_label(int(age))
        label = age * 2 + gender

        if self.transform is not None:
            image= self.transform(image=image)["image"]
        return image, label

if __name__ == "__main__":
    pass