# importing necessary packages
import cv2
import numpy as np
import matplotlib.pyplot as plt
from hist import histeq
from hist import return_intersection


# Loading the test data, healthy sample,
image = cv2.imread('/home/admin1/PycharmProjects/ModuleA_1/Train_Data/ddd.jpg')

#K-MEANS convert to np.float32  define criteria, number of clusters(K) and apply kmeans()
# Now convert back into uint8, and make original image
z = image.reshape((-1,3))
z = np.float32(z)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 8
ret,label,center=cv2.kmeans(z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
center = np.uint8(center)
res = center[label.flatten()]
res2 = res.reshape((image.shape))
cv2.imshow('res2',res2)
scaled_image = cv2.resize(res2,None,fx=2,fy=2,interpolation=cv2.INTER_CUBIC)

# Grey Conversion
gray_image = cv2.cvtColor(scaled_image,cv2.COLOR_BGR2GRAY)
new_img, h, new_h, sk = histeq(gray_image)

# show old and new image
# show original image
plt.subplot(121)
plt.imshow(res2)
plt.title('original image')
plt.set_cmap('gray')
# show original image
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

# SVM Prediction and Histogram Classifier is being done at this
# method block, defined at hist.py
def match_parameter(img_hist):
    intersection = return_intersection(img_hist,new_h)
    return intersection

cv2.waitKey(0)
cv2.destroyAllWindows()

