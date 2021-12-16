import torch
import torch.nn as nn
from model import Net
from dataset import MLflowDataLoader  
from tqdm import tqdm
import os
import os.path as osp
import json
import argparse

config = {
    0 : {"age": "~19", "gender": "female"},
    1 : {"age": "~19", "gender": "male"},
    2 : {"age": "20~29", "gender": "female"},
    3 : {"age": "20~29", "gender": "male"},
    4 : {"age": "30~39", "gender": "female"},
    5 : {"age": "30~39", "gender": "male"},
    6 : {"age": "40~59", "gender": "female"},
    7 : {"age": "40~59", "gender": "male"},
    8 : {"age": "60~", "gender": "female"},
    9 : {"age": "60~", "gender": "male"},
}

def inference(model, args):
    inference_loader = MLflowDataLoader(root=args.data, batch_size=args.batch_size, num_workers=args.num_workers)

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print("device is {}".format(device))
    model = model.to(device)

    with torch.no_grad():
        for x, paths in tqdm(inference_loader):
            x = x.to(device)
            y_ = model.forward(x)
            preds = y_.argmax(dim=1).detach().cpu().numpy()
            
            lst = []
            for path, pred in zip(paths, preds):
                result = {}
                json_path = path.split(".")[0] + ".json"
                result["path"]=path
                result["info"]=config[pred]
                lst.append(result)
    print("inference complete")
    return lst

def main():
    parser = argparse.ArgumentParser(description='Age and Gender Classifier')
    parser.add_argument("-c", "--ckpt", 
        type=str, 
        default="./model.pt",
        help = "checkpoint path"
    )
    parser.add_argument("-d", "--data", type=str, default="./data", help="data path")
    parser.add_argument("-b", "--batch_size", type=int, default=128, help="batch size")
    parser.add_argument("-n", "--num_workers", type=int, default=8, help="num_workers")
    args = parser.parse_args()

    model = Net()
    model.load_state_dict(torch.load(args.ckpt))
    model.eval()
    print(inference(model, args))

main()