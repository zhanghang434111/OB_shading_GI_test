import mipiRawProcess as mrp
import basicTest as bt
import numpy as np
import matplotlib.pylab as plt
import matplotlib.image as img

filepath = r'./raw/colorchart.mipi_raw'
#filepath = r'C:\Users\herman\Desktop\OB test\D.mipi_raw'
bayer_raw = mrp.mipiRaw_2_Bayer(filepath,width="2592",height="1944")

img_bmp = mrp.bayerRaw2bmp(bayer_raw,bayerpattern="R")
img.imsave("new.bmp",img_bmp)
#np.savetxt('1.txt', bayer_raw, fmt='%d')

#img_bmp = mrp.bayerRaw2bmp(bayer_raw,bayerpattern="R")
#np.savetxt('1.txt', img_bmp, fmt='%d')
#img.imsave("new.bmp",img_bmp)

block_width = int(input("区域划分,横坐标block数："))
block_height = int(input("区域划分,纵坐标block数："))

#print(bt.GI_test(bayer_raw,block_width,block_height))
bt.blockData2Excel(bt.intensity_test(bayer_raw, block_width, block_height))




if __name__ == '__main__':
    print('End')


