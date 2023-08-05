# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 01:06:31 2019

@author: Rob
"""

# By first doing least squares with np.linalg.lstsq on the whole image, and
# then redoing it per pixel when the result is NaN, I have sped up the computation
# from 28 s to 1 s. It now also works when a certain pixel is NaN in multiple images
# or all images.

#TODO: Think about how to set the bad pixel clusters to NaN and rotating them. Probably
# cannot rotate with NaN's present, but can mask after rotation by computing coordinates
# of bad pixel clusters

import time
import datetime
import numpy as np
import matplotlib.pyplot as plt

number_images = 30
image_size = 1024
fraction_nan = 0.001

# Create cube Y with Q/U measurements in order of HWP cycles
Y = np.random.rand(number_images, image_size, image_size)
A = np.random.rand(number_images, 2)

# Insert NaN's in Y
Y[Y<fraction_nan] = np.nan

# Make images 1D, compute linear least-squares solution and reshape final images to 2D again
time_start = time.time()

Y_stretched = Y.reshape(Y.shape[0], Y.shape[1]*Y.shape[2])
X_stretched = np.linalg.lstsq(A, Y_stretched, rcond=None)[0]
X = X_stretched.reshape(X_stretched.shape[0], Y.shape[1], Y.shape[2])
X1 = X[0, :, :]
X2 = X[1, :, :]

# Compute linear least squares on coordinates with NaN's after removing NaN's
X_stretched_nan = np.copy(X_stretched)

mask_not_nan = np.isfinite(Y_stretched)

index_pixel_nan = np.unique(np.where(~mask_not_nan)[1])

for index_sel in index_pixel_nan:

    mask_not_nan_sel = mask_not_nan[:, index_sel]

    if not np.all(mask_not_nan_sel == False):
        X_stretched_nan[:, index_sel] = \
        np.linalg.lstsq(A[mask_not_nan_sel],
                        Y_stretched[:, index_sel][mask_not_nan_sel],
                        rcond=None)[0]

Xnan = X_stretched_nan.reshape(X_stretched_nan.shape[0], Y.shape[1], Y.shape[2])
X1nan = Xnan[0, :, :]
X2nan = Xnan[1, :, :]

time_end = time.time()
d = datetime.datetime(1, 1, 1) + datetime.timedelta(seconds = time_end - time_start)
print('\nTime elapsed: %d h %d min %d s' % (d.hour, d.minute, d.second))

print(X1)
print(X1nan)
print('')
print(X2)
print(X2nan)
print('')
print(np.all(X1[~np.isnan(X1)] == X1nan[~np.isnan(X1)]))
print(np.all(X2[~np.isnan(X2)] == X2nan[~np.isnan(X2)]))

plt.figure(figsize=(8,8))
plt.imshow(X1)
plt.show

plt.figure(figsize=(8,8))
plt.imshow(X1nan)
plt.show

