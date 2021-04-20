# -*- coding: utf-8 -*-
import rawProcess as rp
import basicTest as bt
import numpy as np
import matplotlib.pylab as plt
import matplotlib.image as img


#filepath = r'./raw/5025_dothin/raw8_colorchart.raw'
filepath = r'./raw/flatlight.mipi_raw'

bayer_raw = rp.mipiRaw_2_Bayer(filepath,width="2592",height="1944")
#bayer_raw = rp.dothinRaw_2_Bayer(filepath,width="2592",height="1944",raw_deepth="raw8")


# block_width = int(input("区域划分,横坐标block数："))
# block_height = int(input("区域划分,纵坐标block数："))





if __name__ == '__main__':
    print('End')

