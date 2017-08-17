#importing necessary Packages

import cv2
import numpy as np
import matplotlib.pyplot as plt
from hist import histeq
from Train_module import match_parameter

# Capturing Image from the webcam,
camera_port = 0
ramp_frames = 30
camera = cv2.VideoCapture(camera_port)
def get_image():
    retval, im = camera.read()
    return im

for i in range(ramp_frames):
    temp = get_image()
print("Taking image...")
camera_capture = get_image()
file = "/home/admin1/PycharmProjects/ModuleA_1/leaf.jpg"
cv2.imwrite(file, camera_capture)
del(camera)
image = cv2.imread('leaf_1.jpg')

# K-MEANS clustering is being performed on the captured image
cv2.imshow('win1',image)
z = image.reshape((-1,3))
# convert to np.float32
z = np.float32(z)
# define criteria, number of clusters(K) and apply kmeans()
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 8
ret,label,center=cv2.kmeans(z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
# Now convert back into uint8, and make original image
center = np.uint8(center)
res = center[label.flatten()]
res2 = res.reshape((image.shape))
cv2.imshow('res2',res2)
scaled_image = cv2.resize(res2,None,fx=2,fy=2,interpolation=cv2.INTER_CUBIC)

# Grey Conversion for reducing complexity
gray_image = cv2.cvtColor(scaled_image,cv2.COLOR_BGR2GRAY)
cv2.imshow('res1',gray_image)
new_img, h, new_h, sk = histeq(gray_image)

# Plot histogram based on the labels and descriptors obtained by KMeans,
#Equalise the histogram to get a better in sight at the usable data
# show original image
plt.subplot(121)
plt.imshow(res2)
plt.title('original image')
plt.set_cmap('gray')
# show equalised image
plt.subplot(122)
plt.imshow(new_img)
plt.title('hist. equalized image')
plt.set_cmap('gray')
plt.show()

# plot histograms and transfer function
fig = plt.figure()
fig.add_subplot(221)
plt.plot(h)
plt.title('Original histogram') # original histogram

fig.add_subplot(222)
plt.plot(new_h)
plt.title('New histogram') #hist of eqlauized image

fig.add_subplot(223)
plt.plot(sk)
plt.title('Transfer function') #transfer function

plt.show()

# Fed the parameters to SVM PRedict at Train_moule.py, for pattern matching
# Possible outcomes of intersection
# 0.00 < intersection < 0.30 - Severly Damaged sample
# 0.31 < intersection < 0.60 - Partilly Damaged sample
# 0.61 < intersection < 1.00 - Healthy sample
intersection = match_parameter(new_h)
print(intersection)
cv2.waitKey(0)
cv2.destroyAllWindows()

