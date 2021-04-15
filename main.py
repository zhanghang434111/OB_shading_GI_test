import mipiRawProcess as mrp
import basicTest as bt
import numpy as np
import matplotlib.pylab as plt
import matplotlib.image as img


filepath = r'./raw/flatlight.mipi_raw'
#filepath = r'C:\Users\herman\Desktop\OB test\D.mipi_raw'
bayer_raw = mrp.mipiRaw_2_Bayer(filepath,width="2592",height="1944")
#bayer_raw = mrp.mipiRaw_2_Bayer(filepath,width="1600",height="1200")
#np.savetxt('raw.txt',bayer_raw)

#img_bmp = mrp.bayerRaw2bmp(bayer_raw,bayerpattern="R")
#img.imsave("new.bmp",img_bmp)


block_width = int(input("区域划分,横坐标block数："))
block_height = int(input("区域划分,纵坐标block数："))

#print(bt.GI_test(bayer_raw,block_width,block_height))
bt.blockData2Excel((bt.GI_test(bayer_raw, block_width, block_height)),page='mean')
#bt.blockData2Excel((bt.intensity_test(bayer_raw, block_width, block_height)),page='R')
#print(bt.intensity_test(bayer_raw, block_width, block_height))




if __name__ == '__main__':
    print('End')

