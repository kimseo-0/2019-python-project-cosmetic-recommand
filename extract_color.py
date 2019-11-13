import numpy as np
import cv2
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def show_image(imgfile) :
    '''
    show image
    '''
    img = cv2.imread(imgfile, cv2.IMREAD_COLOR)

    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def read_image(imgfile) :
    '''
    read image
    BGR -> RGB
    reshape D3-> D2

    return image
    '''
    image = cv2.imread(imgfile)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = image.reshape((image.shape[0] * image.shape[1], 3)) # height, width 통합
    return image

def centroid_histogram(clt):
    '''
    return 추출된 색상들(clt)의 비율을 나타내는 list
    '''
    # grab the number of different clusters and create a histogram
    # based on the number of pixels assigned to each cluster
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    # normalize the histogram, such that it sums to one
    hist = hist.astype("float")
    hist /= hist.sum()

    # return the histogram
    return hist

def get_mean_colors_image(num,image) :
    '''
    divie image into num
    cal mean each parts

    return mean color list, ratio of each color list (num elements)
    '''
    clt = KMeans(n_clusters = num)
    clt.fit(image)
    clt_center = clt.cluster_centers_
    hist = centroid_histogram(clt)

    return clt_center, hist

def get_mean_color_image(clt_center,hist) :
    mean_color = [0,0,0]
    for i in range(3) :
        for j in range(len(hist)) :
            mean_color[i] += clt_center[j][i] * hist[j]
        mean_color[i] = mean_color[i]
    
    return mean_color

def plot_colors(hist, centroids):
    # initialize the bar chart representing the relative frequency
    # of each of the colors
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0

    # loop over the percentage of each cluster and the color of
    # each cluster
    for (percent, color) in zip(hist, centroids):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        startX = endX

    # return the bar chart
    return bar

def show_color_bar(mean_color) :
    '''
    list -> np.array
    '''
    mean_color = np.array(mean_color)
    bar = np.zeros((50, 50, 3), dtype="uint8")
    cv2.rectangle(bar, (0, 0), (50, 50),mean_color.astype("uint8").tolist(), -1)
    plt.figure()
    plt.axis("off")
    plt.imshow(bar)
    plt.show()


# test
imgfile = "image/32181/0.jpg"
image = read_image(imgfile)

clt_center,hist = get_mean_colors_image(5,image)

mean_color = get_mean_color_image(clt_center,hist)

show_color_bar(mean_color)