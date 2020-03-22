import time
import torch
from torch import nn, optim
# import torchvision
from bagdata import train_dataloader, test_dataloader
# import matplotlib.pyplot as plt
 
# import sys

class AlexNet(nn.Module):
    def __init__(self):
        super(AlexNet, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(3, 32, 9, 1, 4), # in_channels, out_channels, kernel size, stride, padding
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Conv2d(32, 64, 5, 1, 2), 
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(3, 2, padding=1), # 缩小1/2
            nn.Conv2d(64, 64, 3, 1, 1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(3, 2, padding=1), # 缩小1/4
            nn.ConvTranspose2d(64, 32, kernel_size=3, stride=2, padding=1, dilation=1, output_padding=1),#放大到1/2
            nn.BatchNorm2d(32),
            nn.ConvTranspose2d(32, 16, kernel_size=3, stride=2, padding=1, dilation=1, output_padding=1),#放大到1
            nn.BatchNorm2d(16),
            nn.Conv2d(16, 2, kernel_size=1)
        )
    
    def forward(self, x):
        return self.conv(x)

def loss_func(x, x_real):
    loss = (x[:, 0] - x_real[:, 0])**2 + (x[:, 1] - x_real[:, 1])**2
    loss = loss.sum()
    return loss

def train():
    net = AlexNet()
    optimizer = torch.optim.SGD(net.parameters(), lr=0.000002)
    
    for epo in range(3):
        start_time = time.time()
        loss_entir = 0
        for rgb, msk, imgname in train_dataloader:
            res = net(rgb)
            loss = loss_func(res, msk)
            loss_entir += loss.detach().item()
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        print(loss_entir)
        end_time = time.time()
        print('epo %d, cost time %d'%(epo, end_time-start_time))

    torch.save(net.state_dict(), './fcn.pt')

if __name__ == '__main__':
    train()
    