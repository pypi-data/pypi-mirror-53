# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 01:06:31 2019

@author: Rob
"""

#TODO: Make it work when a certain pixel is NaN in multiple images
#TODO: Make sure it outputs NaN when a certain pixel is NaN in all Y-images

import numpy as np
import time
import datetime

number_images = 3
image_size = 5
fraction_nan = 0.07

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

coord_nan = np.where(~np.isfinite(Y_stretched))

for index_image, index_pixel in zip(coord_nan[0], coord_nan[1]):

    X_stretched_nan[:, index_pixel] = \
    np.linalg.lstsq(np.delete(A, index_image, axis=0),
                    np.delete(Y_stretched[:, index_pixel], index_image),
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




##Too slow, 28 s when image size is 1024x1024:
## Alternatively, use a for loop to compute the LSQ solutions
#time_start = time.time()
#
#Y_stretched = Y.reshape(Y.shape[0], Y.shape[1]*Y.shape[2])
#
#X_stretched = np.zeros((A.shape[1], Y_stretched.shape[1]))
#
#for i, Y_sel in enumerate(Y_stretched.T):
#    X_stretched[:, i] = np.linalg.lstsq(A, Y_sel, rcond=None)[0]
#
#X = X_stretched.reshape(X_stretched.shape[0], Y.shape[1], Y.shape[2])
#X1a = X[0, :, :]
#X2a = X[1, :, :]
#
#time_end = time.time()
#d = datetime.datetime(1, 1, 1) + datetime.timedelta(seconds = time_end - time_start)
#print('\nTime elapsed: %d h %d min %d s' % (d.hour, d.minute, d.second))
#
#print('')
#print(np.all(X1 == X1a))
#print(np.all(X2 == X2a))
