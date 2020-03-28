import time
import torch
from torch import nn, optim
# import torchvision
from facedata import get_train_test_data
import matplotlib.pyplot as plt
# import cv2 as cv
 
# import sys

class AlexNet(nn.Module):
    def __init__(self):
        super(AlexNet, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(3, 32, 11, 2, 5), # in_channels, out_channels, kernel size, stride, padding; 1/2
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Conv2d(32, 64, 7, 1, 3), 
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(3, 2, padding=1), # 缩小1/4
            nn.Conv2d(64, 128, 3, 1, 1),
            nn.ReLU(),
            nn.Conv2d(128, 192, 3, 1, 1),
            nn.ReLU(),
            nn.Conv2d(192, 128, 3, 1, 1),
            nn.ReLU(),
            nn.MaxPool2d(3, 2, padding=1), # 缩小1/8
            nn.ConvTranspose2d(128, 32, kernel_size=3, stride=2, padding=1, dilation=1, output_padding=1),#放大到1/4
            nn.BatchNorm2d(32),
            nn.ConvTranspose2d(32, 32, kernel_size=3, stride=2, padding=1, dilation=1, output_padding=1),#放大到1/2
            nn.BatchNorm2d(32),
            nn.ConvTranspose2d(32, 32, kernel_size=3, stride=2, padding=1, dilation=1, output_padding=1),#放大到1
            nn.BatchNorm2d(32),
            nn.Conv2d(32, 2, kernel_size=1),
            nn.ReLU()
        )
    
    def forward(self, x):
        return self.conv(x)

class VGGNet(nn.Module):
    def __init__(self):
        super(VGGNet, self).__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=11, stride=1, padding=5),
            nn.BatchNorm2d(16),
            nn.Conv2d(16, 32, kernel_size=7, stride=1, padding=3),
            nn.BatchNorm2d(32),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )

        self.conv2 = nn.Sequential(
            nn.Conv2d(32, 64, kernel_size=5, stride=1, padding=2),
            nn.BatchNorm2d(64),
            nn.Conv2d(64, 64, kernel_size=5, stride=1, padding=2),
            nn.BatchNorm2d(64),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )

        self.conv3 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=5, stride=1, padding=2),
            nn.BatchNorm2d(128),
            nn.Conv2d(128, 128, kernel_size=5, stride=1, padding=2),
            nn.BatchNorm2d(128),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )

        self.conv4 = nn.Sequential(
            nn.Conv2d(128, 128, kernel_size=5, stride=1, padding=2),
            nn.BatchNorm2d(128),
            nn.Conv2d(128, 256, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(256),
            nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(256),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )

        self.transConv4 = nn.Sequential(
            nn.ConvTranspose2d(256, 128, kernel_size=5, stride=2, padding=2, dilation=1, output_padding=1)
        )

        self.transConv3 = nn.Sequential(
            nn.ConvTranspose2d(128, 64, kernel_size=5, stride=2, padding=2, dilation=1, output_padding=1)
        )

        self.transConv2 = nn.Sequential(
            nn.ConvTranspose2d(64, 32, kernel_size=5, stride=2, padding=2, dilation=1, output_padding=1)
        )

        self.transConv1 = nn.Sequential(
            nn.ConvTranspose2d(32, 16, kernel_size=5, stride=2, padding=2, dilation=1, output_padding=1),
            nn.Conv2d(16, 2, kernel_size=1),
            nn.ReLU()
        )

    def forward(self, x):
        x1 = self.conv1(x)
        x2 = self.conv2(x1)
        x3 = self.conv3(x2)
        x4 = self.conv4(x3)

        t_x = self.transConv2(self.transConv3(self.transConv4(x4) + x3) + x2)
        return self.transConv1(t_x)

class UNet(nn.Module):
    def __init__(self):
        super(UNet, self).__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=11, stride=1, padding=5),
            nn.ReLU(),
            nn.BatchNorm2d(16),
            nn.Conv2d(16, 32, kernel_size=7, stride=1, padding=3),
            nn.ReLU(),
            nn.BatchNorm2d(32)
        )

        self.downSample1 = nn.Sequential(
            nn.MaxPool2d(kernel_size=2, stride=2)
        )

        self.conv2 = nn.Sequential(
            nn.Conv2d(32, 64, kernel_size=5, stride=1, padding=2),
            nn.ReLU(),
            nn.BatchNorm2d(64),
            nn.Conv2d(64, 64, kernel_size=5, stride=1, padding=2),
            nn.ReLU(),
            nn.BatchNorm2d(64)
        )

        self.downSample2 = nn.Sequential(
            nn.MaxPool2d(kernel_size=2, stride=2)
        )

        self.conv3 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=5, stride=1, padding=2),
            nn.ReLU(),
            nn.BatchNorm2d(128),
            nn.Conv2d(128, 128, kernel_size=5, stride=1, padding=2),
            nn.ReLU(),
            nn.BatchNorm2d(128)
        )

        self.downSample3 = nn.Sequential(
            nn.MaxPool2d(kernel_size=2, stride=2)
        )

        self.conv4 = nn.Sequential(
            nn.Conv2d(128, 128, kernel_size=5, stride=1, padding=2),
            nn.ReLU(),
            nn.BatchNorm2d(128),
            nn.Conv2d(128, 256, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(256),
            nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(256)
        )



        self.upSample3 = nn.Sequential(
            nn.ConvTranspose2d(256, 128, kernel_size=5, stride=2, padding=2, dilation=1, output_padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(128)
        )

        self.contact_conv3 = nn.Sequential(
            nn.Conv2d(128+128, 128, kernel_size=5, stride=1, padding=2),
            nn.ReLU(),
            nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(128)
        )

        self.upSample2 = nn.Sequential(
            nn.ConvTranspose2d(128, 64, kernel_size=5, stride=2, padding=2, dilation=1, output_padding=1),
            nn.BatchNorm2d(64)
        )

        self.contact_conv2 = nn.Sequential(
            nn.Conv2d(64+64, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(64)
        )

        self.upSample1 = nn.Sequential(
            nn.ConvTranspose2d(64, 32, kernel_size=5, stride=2, padding=2, dilation=1, output_padding=1),
            nn.BatchNorm2d(32)
        )

        self.contact_conv1 = nn.Sequential(
            nn.Conv2d(32+32, 16, kernel_size=5, stride=1, padding=2),
            nn.ReLU(),
            nn.BatchNorm2d(16),
            nn.Conv2d(16, 2, kernel_size=1),
            nn.ReLU(),
            nn.BatchNorm2d(2)
            # nn.ReLU()
        )

    def forward(self, x):
        s1 = self.conv1(x)
        # print('s1.shape :', s1.shape)
        d1 = self.downSample1(s1)
        # print('d1.shape :', d1.shape)
        s2 = self.conv2(d1)
        # print('s2.shape :', s2.shape)
        d2 = self.downSample2(s2)
        # print('d2.shape :', d2.shape)
        s3 = self.conv3(d2)
        # print('s3.shape :', s3.shape)
        d3 = self.downSample3(s3)
        # print('d3.shape :', d3.shape)
        s4 = self.conv4(d3)
        # print('s4.shape :', s4.shape)


        u4 = torch.cat((self.upSample3(s4), s3), dim=1)
        # print('u4.shape :', u4.shape)
        u4 = self.contact_conv3(u4)
        u4 = torch.cat((self.upSample2(u4), s2), dim=1)
        # print('u4.shape :', u4.shape)
        u4 = self.contact_conv2(u4)
        u4 = torch.cat((self.upSample1(u4), s1), dim=1)
        # print('u4.shape :', u4.shape)
        u4 = self.contact_conv1(u4)
        # print('u4.shape :', u4.shape)
        
        return u4

def loss_func(x, x_real):
    loss = (x[:, 0] - x_real[:, 0])**2 + (x[:, 1] - x_real[:, 1])**2
    loss = loss.sum()
    return loss


def train():
    train_dataloader, test_dataloader = get_train_test_data()
    # net = AlexNet()
    # net = VGGNet()
    net = UNet()
    # for param in net.parameters():
        # print(param)
    net = net.to('cuda' if torch.cuda.is_available() else 'cpu')
    optimizer = torch.optim.SGD(net.parameters(), lr=0.0000008)

    # loss_fn = nn.CrossEntropyLoss()
    
    for epo in range(10):
        start_time = time.time()
        loss_entir = 0
        for rgb, msk, imgname in train_dataloader:
            res = net(rgb.to('cuda'))
            loss = loss_func(res, msk.to('cuda'))
            # loss = loss_fn(res, msk.to('cuda'))
            loss_entir += loss.detach().cpu().item()
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        print(loss_entir)
        end_time = time.time()
        print('epo %d, cost time %d'%(epo, end_time-start_time))

    torch.save(net.state_dict(), './fcn.pt')

if __name__ == '__main__':
    train()
