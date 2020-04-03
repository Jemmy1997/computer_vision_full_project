from scipy import misc
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from CV404Filters import sobel , rgb2gray
from Canny import canny
import numpy as np
import cv2
from collections import defaultdict

def hough_line(img):
    #Get image dimensions
    Y, X = np.nonzero(img)
    #Max diatance is diagonal one 

    Maxdist = int(np.round(np.sqrt(img.shape[0]**2 + img.shape[1]** 2)))

    # 1. initialize parameter space rs, thetas
    # Theta in range from -90 to 90 degrees
    # thetas = np.deg2rad(np.arange(-90, 90))
    thetas = np.linspace(-np.pi / 2, np.pi / 2, 180)
    #Range of radius
    rhos = np.linspace(-Maxdist, Maxdist, 2*Maxdist)
    
    #2. Create accumulator array and initialize to zero
    accumulator = np.zeros((2 * Maxdist, len(thetas)))

    #3. Loop for each edge pixel 
    for i in range(len(X)):
        x = X[i]
        y = Y[i]
        #4. Loop for each theta
        # Map edge pixel to hough space
        for k in range(len(thetas)):
            #5. calculate $\rho$
            # Calculate space parameter
            rho = x*np.cos(thetas[k]) + y * np.sin(thetas[k]) 

            #6. Increment accumulator at rho, theta
            # Update the accumulator
            # map r to its idx 0 : 2*max
            accumulator[int(rho)+ Maxdist,k] += 1

    return accumulator, thetas, rhos

def extract_lines( accumulator , thetas , rhos , threshold = 0.5) :
    theta_peak =[]
    rho_peak = []
    # threshold = np.quantile( accumulator , threshold )
    threshold = threshold * np.max(accumulator)
    acc2 = np.zeros(accumulator.shape)
    acc=[]
    for rho_idx in range(accumulator.shape[0]) :
        for theta_idx in range(accumulator.shape[1]) :
            if accumulator[rho_idx, theta_idx] > threshold :
                theta_peak.append(thetas[theta_idx])
                rho_peak.append(rhos[rho_idx])
                acc2[rho_idx,theta_idx] = accumulator[rho_idx, theta_idx]
    theta_peak = np.array(theta_peak)
    rho_peak = np.array(rho_peak)
    return acc2, theta_peak, rho_peak

def get_hough_lines(img, threshold = 0.5):
    gray = rgb2gray(img)
    edge = canny(gray)
    accs, ths, rs  = hough_line(edge)
    acc,theta_peak,rho_peak =extract_lines(acc,th,r,threshold)
    return acc,theta_peak,rho_peak



# fig, ax = plt.subplots()
# ax.imshow(img_c)
# ax.autoscale(False)
# origin = np.array((0, img.shape[1]))
# for _, angle, dist in zip(*extract_lines(acc, th, r)):
#     y0, y1 = (dist - origin * np.cos(angle)) / np.sin(angle)
#     ax.plot(origin, (y0, y1), '-r')
# plt.show()


# def hough_line(img, angle_step=1, lines_are_white=True, value_threshold=5):
    
#     img = cv2.Canny(img,100,200)
#     # rho and theta ranges
#     thetas = np.deg2rad(np.arange(-90.0, 90.0, angle_step))
#     width, height = img.shape
#     diag_len = int(round(math.sqrt(width * width + height * height)))
#     rhos = np.linspace(-diag_len, diag_len, diag_len * 2)

#     cos_t = np.cos(thetas)
#     sin_t = np.sin(thetas)
#     num_thetas = len(thetas)

#     # Hough accumulator 
#     accumulator = np.zeros((2 * diag_len, num_thetas), dtype=np.uint8)
#     are_edges = img > value_threshold if lines_are_white else img < value_threshold
#     y_idxs, x_idxs = np.nonzero(are_edges)

#     # hough accumulator voting
#     for i in range(len(x_idxs)):
#         x = x_idxs[i]
#         y = y_idxs[i]

#         for t_idx in range(num_thetas):
#             rho = diag_len + int(round(x * cos_t[t_idx] + y * sin_t[t_idx]))
#             accumulator[rho, t_idx] += 1

#     return accumulator, thetas, rhos


# def show_hough_line(img, accumulator, thetas, rhos, save_path=None):
#     import matplotlib.pyplot as plt

#     fig, ax = plt.subplots(1, 2, figsize=(10, 10))

#     ax[0].imshow(img, cmap=plt.cm.gray)
#     ax[0].set_title('Input image')
#     ax[0].axis('image')

#     ax[1].imshow(
#         accumulator, cmap='jet',
#         extent=[np.rad2deg(thetas[-1]), np.rad2deg(thetas[0]), rhos[-1], rhos[0]])
#     ax[1].set_aspect('equal', adjustable='box')
#     ax[1].set_title('Hough transform')
#     ax[1].set_xlabel('Angles (degrees)')
#     ax[1].set_ylabel('Distance (pixels)')
#     ax[1].axis('image')

#     if save_path is not None:
#         plt.savefig(save_path, bbox_inches='tight')
#     plt.show()


# if __name__ == '__main__':
#     # pass here the image path 
#     imgpath = '/home/muhamed/cv404-2020-assignment-02-sbme404-2020-team05/images/dog.jpg'
#     img = imageio.imread(imgpath)
#     if img.ndim == 3:
#         img = rgb2gray(img)
#     accumulator, thetas, rhos = hough_line(img)
#     # pass here the saved path
#     show_hough_line(img, accumulator, save_path='/home/muhamed/cv404-2020-assignment-02-sbme404-2020-team05/output01.jpg')