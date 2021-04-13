import mipiRawProcess as mrp
import basicTest as bt
import numpy as np
import matplotlib.pylab as plt
import matplotlib.image as img

filepath = r'C:\Users\herman\Desktop\raw\blk.mipi_raw'
#filepath = r'C:\Users\herman\Desktop\OB test\D.mipi_raw'
bayer_raw = mrp.mipiRaw_2_Bayer(filepath,width="2592",height="1944")
#bayer_raw = mrp.mipiRaw_2_Bayer(filepath,width="1600",height="1200")
# img_bmp = mipiRawProcess.bayerRaw2bmp(bayer_raw,bayerpattern="B")
# img.imsave("new.bmp",img_bmp)
#np.savetxt('1.txt', bayer_raw, fmt='%d')

img_bmp = mrp.bayerRaw2bmp(bayer_raw,bayerpattern="R")
#np.savetxt('1.txt', img_bmp, fmt='%d')
#img.imsave("new.bmp",img_bmp)

#imgsrc = plt.imread(r'C:\Users\herman\Desktop\OB test\D.mipi_raw')
block_width = int(input("区域划分,横坐标block数："))
block_height = int(input("区域划分,纵坐标block数："))

print(bt.GI_test(bayer_raw,block_width,block_height))
bt.blockData2Excel(bt.ob_test(bayer_raw, block_width, block_height))
#img.imsave('new.jpg',basicTest.ob_test(bayer_raw,block_width,block_height))
#plt.show()





if __name__ == '__main__':
    print('End')


