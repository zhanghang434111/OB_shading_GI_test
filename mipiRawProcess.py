import numpy as np
import matplotlib.pylab as plt
import matplotlib.image as img
import os


# bayer raw 转 BMP
# 返回值：BMP图像数组
def bayerRaw2bmp(img_raw,bayerpattern = "B"):
    r = np.zeros((img_raw.shape),dtype=np.uint16)
    g = np.zeros((img_raw.shape),dtype=np.uint16)
    b = np.zeros((img_raw.shape),dtype=np.uint16)

    # BGGR
    # B G B G B
    # G R G R G
    # B G B G B
    # G R G R G
    if (bayerpattern == "B"):
        r[1::2, 1::2, :] = img_raw[1::2, 1::2]
        b[::2, ::2, :] = img_raw[1::2, ::2]
        g[::2, 1::2, :] = img_raw[::2, 1::2]
        g[1::2, ::2, :] = img_raw[1::2, ::2]

    # RGGB
    # R G R G R
    # G B G B G
    # R G R G R
    # G B G B G
    elif (bayerpattern == "R"):
        b[1::2, 1::2, :] = img_raw[1::2, 1::2]
        r[::2, ::2, :] = img_raw[::2, ::2]
        g[::2, 1::2, :] = img_raw[::2, 1::2]
        g[1::2, ::2, :] = img_raw[1::2, ::2]

    # GRBG
    # G R G R G
    # B G B G B
    # G R G R G
    # B G B G B
    elif (bayerpattern == "Gr"):
        g[1::2, 1::2, :] = img_raw[1::2, 1::2]
        g[::2, ::2, :] = img_raw[::2, ::2]
        r[::2, 1::2, :] = img_raw[::2, 1::2]
        b[1::2, ::2, :] = img_raw[1::2, ::2]

    # GBRG
    # G B G B G
    # R G R G R
    # G B G B G
    # R G R G R
    elif (bayerpattern == "Gb"):
        g[1::2, 1::2, :] = img_raw[1::2, 1::2]
        g[::2, ::2, :] = img_raw[::2, ::2]
        b[::2, 1::2, :] = img_raw[::2, 1::2]
        r[1::2, ::2, :] = img_raw[1::2, ::2]

    im_conv = np.stack((r, g, b), axis=2).astype("uint8")
    print(im_conv)
    return im_conv

    #img.imsave(r'C:\Users\herman\Desktop\py_raw_test\xxxx.bmp', im_conv)

# mipi raw 转Bayer raw
# 返回值：bayer raw image
def mipiRaw_2_Bayer(filepath,raw_size = "5M",raw_deepth="raw10"):
    if (raw_deepth == 'raw10'):
        size = os.path.getsize(filepath) #获得文件大小
        fo = open(filepath, 'rb+')
        a = np.zeros(size, dtype=int)
        for i in range(size):
            data = fo.read(1) #每次输出一个字节
            num = int.from_bytes(data, byteorder='big')
            a[i] = num
        print(a)
        '''
        p1 = (a[0] << 2) + (a[4] & 0x03)
        p2 = (a[1] << 2) + (a[4] & 0x0c)
        p3 = (a[2] << 2) + (a[4] & 0x30)
        p4 = (a[3] << 2) + (a[4] & 0xc0)
        '''
        b = []
        for c in range(size):
            if (c + 1) % 5 == 0:
                if c == 0:
                    b.append(a[c])
                continue
            else:
                b.append(a[c])
        print(b)
        k = np.array(b)
        print(k)
        m = k.reshape((1200, 1600))
        print(m)
        return m