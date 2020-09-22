#Miranda Harrison
#400065695

import numpy
import cv2

def bicubic2(img,x,y):
    img = cv2.copyMakeBorder(img,2,2,2,2,cv2.BORDER_REPLICATE) #pad original image in all directions

    arr=numpy.zeros([4,4,3]) #create double array to store 4x4 neighborhood
    arr[0][0] = img[x][y]
    arr[0][1] = img[x][y+1]
    arr[0][2] = img[x][y+2]
    arr[0][3] = img[x][y+3]
    arr[1][0] = img[x+1][y]
    arr[1][1] = img[x+1][y+1]
    arr[1][2] = img[x+1][y+2]
    arr[1][3] = img[x+1][y+3]
    arr[2][0] = img[x+2][y]
    arr[2][1] = img[x+2][y+1]
    arr[2][2] = img[x+2][y+2]
    arr[2][3] = img[x+2][y+3]
    arr[3][0] = img[x+3][y]
    arr[3][1] = img[x+3][y+1]
    arr[3][2] = img[x+3][y+2]
    arr[3][3] = img[x+3][y+3]

    arr1=numpy.zeros([4,3]) #create array to store first result of cubic
    arr1[3] = cubic(arr[0],y).astype(numpy.uint8)
    arr1[2] = cubic(arr[1],y).astype(numpy.uint8)
    arr1[1] = cubic(arr[2],y).astype(numpy.uint8)
    arr1[0] = cubic(arr[3],y).astype(numpy.uint8)
  
    return cubic(arr1,x).astype(numpy.uint8) #returns result of bicubic


def cubic(f,x):
    return f[1] + (-0.5*f[0]+(3/2)*f[1]-(3/2)*f[2]+0.5*f[3])*x*x*x \
        + (-0.5*f[0]+0.5*f[2])*x \
            + (f[0]-(5/2)*f[1]+2*f[2]-0.5*f[3])*x*x

image = cv2.imread('image.png') #open image
og_height = image.shape[0]
og_width = image.shape[0]

height = og_height*2 #output image height and width (twice the original size)
width = og_width*2

output = numpy.zeros([height,width,3], numpy.uint8)

h = 0
w = 0
for i in range(int(height/2)): #placing the original pixels in the output image
    h = i*2
    for j in range(int(width/2)):
        w = j*2
        output[h][w] = image[i][j]


for i in range(int(height/2)): #placing the interpolated pixels in the output image (double offset)
    h = i*2+1
    for j in range(int(width/2)):
        w = j*2+1
        output[h][w] = bicubic2(image,i,j)

for i in range(int(height/2)): #placing the interpolated pixels in the output image (w offset)
    h = i*2
    for j in range(int(width/2)):
        w = j*2+1
        output[h][w] = bicubic2(image,i,j)

for i in range(int(height/2)): #placing the interpolated pixels in the output image (h offset)
    h = i*2+1
    for j in range(int(width/2)):
        w = j*2
        output[h][w] = bicubic2(image,i,j)

opencv_image = cv2.resize(image,(450,450),interpolation=cv2.INTER_CUBIC)


cv2.imshow('my output',output)
cv2.imshow('opencv output',opencv_image)
cv2.imwrite('output.jpg',output)
cv2.waitKey()
