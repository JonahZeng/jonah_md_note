import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

np.random.seed(seed=1990)

origin = np.random.randint(0, 1023, size=(3, 18), dtype=np.int32)
noise = np.random.randint(-45, 45, size=(3, 18), dtype=np.int32)
# print('origin:', origin)
CCM = np.array([[ 1.4472656,   0.1953125 , -0.6425781],
    [-0.09082031,  1.3515625,  -0.2607422],
    [ 0.29492188, -0.13867188,  0.84375   ]], dtype=np.float32)

apply_ccm_rgb = CCM.dot(origin)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# x1 = origin[0]
# y1 = origin[1]
# z1 = origin[2]

x2 = apply_ccm_rgb[0]
y2 = apply_ccm_rgb[1]
z2 = apply_ccm_rgb[2]

# ax.scatter(x1, y1, z1, marker='o', c='r', label='origin RGB')
ax.scatter(x2, y2, z2, marker='*', c='b', label='standard RGB')
# for i in range(len(x1)):
    # ax.plot([x1[i], x2[i]], [y1[i], y2[i]], [z1[i], z2[i]], 'k-.')

# ax.legend()
ax.set_xlim(-300, 1500)
ax.set_ylim(-300, 1500)
ax.set_zlim(-300, 1500)
ax.set_xlabel('R')
ax.set_ylabel('G')
ax.set_zlabel('B')



def get_loss_grad(origin_RGB, CCM, standard_RGB, pathch_W):
    applyed_ccm_rgb_w = CCM.dot(origin_RGB) # CCM 3X3; origin_rgb, 3x18; pathch_W, I 18x18
    standard_rgb_w = standard_RGB
    square_dist = ((applyed_ccm_rgb_w - standard_rgb_w).dot(pathch_W))**2 # 18x18 3x18
    loss = np.sum(square_dist.flatten())

    grad = np.zeros_like(CCM)
    grad = ((applyed_ccm_rgb_w - standard_RGB).dot(pathch_W)).dot(np.transpose(origin_RGB)) # 3x3
    # grad[0, 0] = -grad[0, 1] - grad[0, 2]
    # grad[1, 1] = -grad[1, 0] - grad[1, 2]
    # grad[2, 2] = -grad[2, 0] - grad[2, 1]
    return loss, grad

patch_W = np.eye(18)
patch_W[10, 10] = 10
noise_rgb = origin + noise

init_CCM = np.eye(3, dtype=np.float32) + np.random.randn(3 , 3)*0.1


loweat_loss = 1e128
best_ccm = None

for i in range(1500):
    loss, grad = get_loss_grad(noise_rgb, init_CCM, apply_ccm_rgb, patch_W)
    if loss<loweat_loss:
        loweat_loss = loss
        best_ccm = init_CCM
    init_CCM -= 0.00000001 * grad
    # init_CCM[0, 0] = 1.0 -init_CCM[0, 1] - init_CCM[0, 2]
    # init_CCM[1, 1] = 1.0 -init_CCM[1, 0] - init_CCM[1, 2]
    # init_CCM[2, 2] = 1.0 -init_CCM[2, 0] - init_CCM[2, 1]
    # init_CCM[0] *= 1.0/np.sum(init_CCM[0])
    # init_CCM[1] *= 1.0/np.sum(init_CCM[1])
    # init_CCM[2] *= 1.0/np.sum(init_CCM[2])

print(best_ccm)
# print(np.sum(best_ccm, axis=1))
# print(best_ccm/np.sum(best_ccm, axis=1).reshape((3, 1)))
print('=====')
print('origin CCM:', CCM)

real_rgb = best_ccm.dot(noise_rgb)
x3 = real_rgb[0]
y3 = real_rgb[1]
z3 = real_rgb[2]

dist_patches = np.sum((real_rgb - apply_ccm_rgb)**2, axis=0)
# largest_patch = np.argmax(dist_patches)
# print(largest_patch)
print('dist_patch10=', dist_patches[10])

ax.scatter(x3, y3, z3, marker='o', c='c', label='real rgb')
for i in range(len(x3)):
    # if i==largest_patch:
        # ax.plot([x2[i], x3[i]], [y2[i], y3[i]], [z2[i], z3[i]], 'r--')
    # else:
    ax.plot([x2[i], x3[i]], [y2[i], y3[i]], [z2[i], z3[i]], 'k-.')
ax.legend()
plt.show()
