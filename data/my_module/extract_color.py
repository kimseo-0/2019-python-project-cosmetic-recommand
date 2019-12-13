import numpy as np
import cv2
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import colorsys

def RGB_To_HSL(rgb):
    '''
    rgb로 나타낸 색상을 hsl 변환하여 반환
    '''
    r = rgb[0]/255
    g = rgb[1]/255
    b = rgb[2]/255
    
    hls = colorsys.rgb_to_hls(r, g, b)

    h = hls[0] * 360
    l = hls[1] * 100
    s = hls[2] * 100

    return [h,s,l]


def promise_color(rgb):
    '''
    유효한 색상 추출
    해당 범위 안에 드는 색상 -> true

    해당 범위의 색상만 mask에 포함하기 위해서
    '''
    hsl = RGB_To_HSL(rgb)
    s = hsl[1]
    l = hsl[2]

    if s-((l-50)**2)/20-20 > 0 and 10 < l < 90:
        return True
    return False

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

    KMeans 알고리즘에 따라 비슷한 색상으로(군집화)
    num 만큼 이미지를 나누고,
    각 나뉜 이미지의 평균 색상과 이미지에서 차지하는 비율의 리스트
    '''
    clt = KMeans(n_clusters = num)
    clt.fit(image)
    clt_center = clt.cluster_centers_
    hist = centroid_histogram(clt)
    return hist, clt_center

def get_mean_color_of_image(hist,clt_center) :
    '''
    input 받은 색상과 해당 색상의 비율을 고려하여 
    평균 색을 계산한다.

    만약, 해당 색상이 유효하지 않을 경우 제외하여
    전체 비율을 재조정하여 계산한다.
    '''
    mean_color = [0,0,0]
    need_clt = []
    need_hist = []
    sum_hist = 0
    list(hist)
    clt_center = list(map(lambda elem : list(elem), clt_center))

    for i in range(len(hist)) :
        if promise_color(clt_center[i]) : #clt_center[i][0]>50 :
            need_clt.append(clt_center[i])
            need_hist.append(hist[i])
            sum_hist += float(hist[i])
            
    for i in range(len(need_hist)) :
        need_hist[i] = need_hist[i]/sum_hist
    
    for i in range(3) :
        for j in range(len(need_hist)) :
            mean_color[i] += need_clt[j][i] * need_hist[j]
        mean_color[i] = mean_color[i]

    np.array(mean_color)
    np.array(need_hist)
    need_clt = (map(lambda elem : np.array(elem), need_clt))

    return mean_color , need_hist, need_clt

def plot_colors_bar(hist, centroids):
    '''
    색상 bar를 생성
    각 색상의 비율에 따라 bar에서 차지하는 면적을 설정하여,
    각 색상이 차지하는 비중을 시각화 하여 보여줄 수 있다.
    '''
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

def mean_color_box(mean_color) :
    '''
    list -> np.array
    mean color box
    색상 박스 이미지 생성
    '''
    mean_color = np.array(mean_color)
    box = np.zeros((50, 50, 3), dtype="uint8")
    cv2.rectangle(box, (0, 0), (50, 50),mean_color.astype("uint8").tolist(), -1)

    return box

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
    (open cv에서 이미지 읽을 때 bgr로 읽기 때문에 rgb로 변환하여 띄워준다. )
    reshape D3-> D2

    return image
    '''
    image = cv2.imread(imgfile)
    # cv2.imshow(imgfile,image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = image.reshape((image.shape[0] * image.shape[1], 3)) # height, width 통합
    return image

def show_color(bar, num):
    plt.figure(num)
    plt.axis("off")
    plt.imshow(bar)
    plt.show()

def extract_color(imgfile) :
    '''
    색 추출 함수
    '''
    image = read_image(imgfile)

    hist, clt_center = get_mean_colors_image(5,image)

    mean_rgb_color, need_hist, need_clt = get_mean_color_of_image(hist,clt_center)

    show_color(plot_colors_bar(need_hist, need_clt),1)
    show_color(mean_color_box(mean_rgb_color),2)

    mean_hsl_color = RGB_To_HSL(mean_rgb_color)
    
    return mean_hsl_color
    
#extract_color("../image/0.jpg")

# https://inyl.github.io/programming/2017/07/31/opencv_image_color_cluster.html