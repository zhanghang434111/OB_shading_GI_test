import mipiRawProcess as mrp
import basicTest as bt
import numpy as np
import matplotlib.pylab as plt
import matplotlib.image as img

filepath = r'./raw/2_1600_1200.mipi_raw'
#filepath = r'C:\Users\herman\Desktop\OB test\D.mipi_raw'
#bayer_raw = mrp.mipiRaw_2_Bayer(filepath,width="2592",height="1944")
bayer_raw = mrp.mipiRaw_2_Bayer(filepath,width="1600",height="1200")
#np.savetxt('raw.txt',bayer_raw)
#img_bmp = mrp.bayerRaw2bmp(bayer_raw,bayerpattern="B")
#img.imsave("new.bmp",img_bmp)
#np.savetxt('1.txt', bayer_raw, fmt='%d')

img_bmp = mrp.bayerRaw2bmp(bayer_raw,bayerpattern="B")

img.imsave("new.bmp",img_bmp)

block_width = int(input("区域划分,横坐标block数："))
block_height = int(input("区域划分,纵坐标block数："))

#print(bt.GI_test(bayer_raw,block_width,block_height))
bt.blockData2Excel(bt.intensity_test(bayer_raw, block_width, block_height))
#print(bt.intensity_test(bayer_raw, block_width, block_height))




if __name__ == '__main__':
    print('End')

    b = []
    #a = np.fromfile(filepath, dtype='u1')  # u1 = uint8 ; u2 = uint16 ;
    a = np.arange(222)
    print("mipi raw原始数据", a)
    # b = np.array(a)
    # b = np.zeros(shape=img_hei*img_wid,dtype=np.uint16)
    for c in range(0, 220, 5):
        # b.append((a[c] << 2) + (a[c + 4] & 0x03))
        # b.append((a[c + 1] << 2) + (a[c + 4] & 0x0c))
        # b.append((a[c + 2] << 2) + (a[c + 4] & 0x30))
        # b.append((a[c + 3] << 2) + (a[c + 4] & 0xc0))
        b.append(np.left_shift(a[c],2) + ((a[c + 4] >> 0) & 0x03))
        b.append(np.left_shift(a[c+1], 2) + ((a[c + 4]>>2) & 0x0c))
        b.append(np.left_shift(a[c+2], 2) + ((a[c + 4]>>4) & 0x30))
        b.append(np.left_shift(a[c+3], 2) + ((a[c + 4] >>6)& 0xc0))
    print(b)
