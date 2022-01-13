import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from skimage import transform
board = io.imread('imp-brd-643-1_1.jpg')

src = np.array([[300,0], [0, 0], [0, 300], [300, 300]])
dst = np.array([[810, 230], [180, 460], [775, 850], [1410, 490]])

tform3 = transform.ProjectiveTransform()
tform3.estimate(src, dst)
warped = transform.warp(board, tform3, output_shape=(300, 300))

fig, ax = plt.subplots(nrows=2, figsize=(8, 3))

ax[0].imshow(board, cmap=plt.cm.gray)
ax[0].plot(dst[:, 0], dst[:, 1], '.r')
ax[1].imshow(warped, cmap=plt.cm.gray)

for a in ax:
    a.axis('off')

plt.tight_layout()
# plt.show()
