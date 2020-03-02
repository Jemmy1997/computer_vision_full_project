import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy import ndimage, signal
from skimage import filters
import random 


def rgb2gray(rgb_image):
    # convert RGB img to grayScale img
    return np.dot(rgb_image[...,:3], [0.299, 0.587, 0.114])

def generate_gaussian_noise( mu, sigma, img_size ):
    #generrate random Gaussian noise array 
    return np.random.normal( mu, sigma, img_size)

def add_gaussian_noise(mu, sigma, img):
    #add randam Gaussian noise to the img
    gaussian_noise= generate_gaussian_noise(mu,sigma, img.shape)
    img_with_gaussian_noise = img + gaussian_noise
    return img_with_gaussian_noise

def gaussian_Filter(sigma = 0.1, shape= [3,3]):
    # generate gaussian kernal
    shape = np.asarray(shape)
    shape = shape//2 *2 + 1
    [m,n] = shape//2
    filter = np.zeros(shape)
    # to set limts uncomment this
    # size = 2*int(4*sigma + 0.5) + 1
    # if shape[0] > size:
    #     m = size//2
    # if shape[1] > size:
    #     n = size//2
    for x in range (-m, m+1):
        for y in range (-m, m+1):
            filter[x+m, y+m] =np.exp(-(x**2 + y**2)/(2*sigma**2))/(2*np.pi*(sigma**2))
    sum = filter.sum()
    filter = filter * (1/sum)
    return filter

def img_gaussian_Filter(img, sigma=0.1, shape=(3,3)):
    kernal = gaussian_Filter(sigma,shape)
    return signal.convolve2d(img,kernal,mode='valid')

def roberts_edge_detection(img):
    # output = np.sqrt(roberts_H_edge_detection(img)**2 + roberts_V_edge_detection(img)**2)
    # it gives the same output but it should be faster
    output = np.abs(roberts_H_edge_detection(img))+np.abs(roberts_V_edge_detection(img))
    return output

def roberts_H_edge_detection(img):
    ROBERTS_H_MASK= np.array([[1,0],[0,-1]])
    return signal.convolve2d(img,ROBERTS_H_MASK,mode='valid')

def roberts_V_edge_detection(img):
    ROBERTS_V_MASK= np.array([[0,1],[-1,0]])
    return signal.convolve2d(img,ROBERTS_V_MASK,mode='valid')

def prewitt(img):
    vertical = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
    horizontal = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
    horizontalGrad = signal.convolve2d(img,horizontal)
    verticalGrad = signal.convolve2d(img,vertical)
    output =  np.sqrt(pow(horizontalGrad, 2.0) + pow(verticalGrad, 2.0))
    verticalGrad /= np.max(verticalGrad)
    horizontalGrad /= np.max(horizontal) 
    output /=  np.max(output) 
    return output     


def median_filter(img, filter_size):
    index = filter_size // 2
    filtered = np.zeros(img.shape, np.uint8)

    row, col = img.shape

    for i in range(row):
        for j in range(col):
            temp = []
            for z in range(filter_size):
                if i + z - index < 0 or i + z - index > img.shape[0] - 1:
                    for c in range(filter_size):
                        temp.append(0)
                else:
                    if j + z - index < 0 or j + index > img.shape[1] - 1:
                        temp.append(0)
                    else:
                        for k in range(filter_size):
                            temp.append(img[i + z - index][j + k - index])

            temp.sort()
            filtered[i][j] = temp[len(temp) // 2]

    return filtered


def saltNpepper(img, low):
    high = 1-low
    output = np.zeros(img.shape, np.uint8)
    row, col = img.shape
    for i in range(row):
        for j in range(col):
            rndm = random.random()
            if rndm < low:
                output[i][j] = 0
            elif rndm > high:
                output[i][j] = 255
            else:
                output[i][j] = img[i][j]
    return output