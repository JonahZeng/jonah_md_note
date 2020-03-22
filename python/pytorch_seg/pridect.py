from fcn import AlexNet
import torch
import matplotlib.pyplot as plt
# from bag_data import test_dataloader
from bagdata import train_dataloader, test_dataloader
import cv2 as cv

net2 = AlexNet()
net2.load_state_dict(torch.load('./fcn.pt'))

for rgb, msk, name in train_dataloader:
    for i in range(4):
        res = net2(rgb)
        f1 = plt.figure(0)
        ax1 = f1.add_subplot(111)
        cs1 = ax1.contourf(res[i][0].detach().numpy(), cmap='coolwarm')
        ax1.set_ylim([160, 0])
        ax1.set_title(name[i])
        f1.colorbar(cs1)
        f2 = plt.figure(1)
        ax2 = f2.add_subplot(111)
        cs2 = ax2.contourf(res[i][1].detach().numpy(), cmap='coolwarm')
        ax2.set_title(name[i])
        ax2.set_ylim([160, 0])
        f2.colorbar(cs2)
        f2 = plt.figure(2)
        ax3 = f2.add_subplot(111)
        img = cv.imread('./bag_data/'+name[i])
        ax3.imshow(img)
        plt.show()
    break