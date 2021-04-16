import mipiRawProcess as mrp
import basicTest as bt
import numpy as np
import matplotlib.pylab as plt
import matplotlib.image as img


filepath = r'./raw/02m1_dothin/raw10_colorchart.raw'

#filepath = r'C:\Users\herman\Desktop\OB test\D.mipi_raw'
#bayer_raw = mrp.mipiRaw_2_Bayer(filepath,width="2592",height="1944")
bayer_raw = mrp.dothinRaw_2_Bayer(filepath,width="1600",height="1200",raw_deepth="raw10")
#bayer_raw = mrp.mipiRaw_2_Bayer(filepath,width="1600",height="1200")


img_bmp = mrp.bayerRaw2bmp(bayer_raw,bayerpattern="B")
img.imsave("new.bmp",img_bmp)


# block_width = int(input("区域划分,横坐标block数："))
# block_height = int(input("区域划分,纵坐标block数："))

#bt.OB_shading_test(bayer_raw,block_width,block_height)
# bt.OB_shading_test(bayer_raw)
# bt.GI_test(bayer_raw)



if __name__ == '__main__':
    print('End')

