import torch
import torch.nn as nn
from torchvision import models
from efficientnet_pytorch import EfficientNet

class Net(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        self.model = EfficientNet.from_pretrained('efficientnet-b0', num_classes=num_classes)
    
    def forward(self, x):
        return self.model(x)

    def predict(self, x):
        return self.model(x).argmax() 