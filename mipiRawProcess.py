import numpy as np
import os
from PIL import Image
from skimage import img_as_ubyte
import cv2

# input
#
def read_img():
    filepath = "asd"

    return 0


# 用于将raw图 16位转位8位，保存为bmp用作预览
# bug问题：高亮条带
def uint16to8(bands, lower_percent=0.001, higher_percent=99.999):
    out = np.zeros_like(bands,dtype = np.uint8)
    n = bands.shape[0]
    for i in range(n):
        a = 0 # np.min(band)
        b = 255 # np.max(band)
        c = np.percentile(bands[i, :], lower_percent)
        d = np.percentile(bands[i, :], higher_percent)
        t = a + (bands[i, :] - c) * (b - a) / (d - c)
        t[t<a] = a
        t[t>b] = b
        out[i, :] = t
    return out

# 用于矩阵除法，数组内数据整体右移2位，实现16bit to 8bit
def uint16to8_new(raw):
    c = np.array(4)
    d = np.uint8(np.divide(raw, c))
    return  d

# bayer raw 转 BMP
# 返回值：BMP图像数组
def bayerRaw2bmp(img_raw,bayerpattern = "R"):
    #img_new = np.uint8(img_raw)
    #img_new = img_as_ubyte(img_raw)
    #img_new = cv2.convertScaleAbs(img_raw)         #不是线性压缩
    #img_new = uint16to8(img_raw)
    img_new = uint16to8_new(img_raw)
    r = np.zeros((img_raw.shape),dtype=np.uint8)
    g = np.zeros((img_raw.shape),dtype=np.uint8)
    b = np.zeros((img_raw.shape),dtype=np.uint8)
    # BGGR
    # B G B G B
    # G R G R G
    # B G B G B
    if (bayerpattern == "B"):
        r[1::2, 1::2] = img_new[1::2, 1::2]
        b[::2, ::2] = img_new[::2, ::2]
        g[::2, 1::2] = img_new[::2, 1::2]
        g[1::2, ::2] = img_new[1::2, ::2]

    # RGGB
    # R G R G R
    # G B G B G
    # R G R G R
    elif (bayerpattern == "R"):
        # b[1::2, 1::2] = img_raw[1::2, 1::2]
        # r[::2, ::2] = img_raw[::2, ::2]
        # g[::2, 1::2] = img_raw[::2, 1::2]
        # g[1::2, ::2] = img_raw[1::2, ::2]
        r[1::2, 1::2] = img_new[1::2, 1::2]
        b[::2, ::2] = img_new[::2, ::2]
        g[::2, 1::2] = img_new[::2, 1::2]
        g[1::2, ::2] = img_new[1::2, ::2]

    # GRBG
    # G R G R G
    # B G B G B
    # G R G R G
    ##########   待验证
    elif (bayerpattern == "Gr"):
        g[1::2, 1::2] = img_raw[1::2, 1::2]
        g[::2, ::2] = img_raw[::2, ::2]
        r[::2, 1::2] = img_raw[::2, 1::2]
        b[1::2, ::2] = img_raw[1::2, ::2]

    # GBRG
    # G B G B G
    # R G R G R
    # G B G B G
    ##########   待验证
    elif (bayerpattern == "Gb"):
        g[1::2, 1::2] = img_raw[1::2, 1::2]
        g[::2, ::2] = img_raw[::2, ::2]
        b[::2, 1::2] = img_raw[::2, 1::2]
        r[1::2, ::2] = img_raw[1::2, ::2]

    im_conv = np.stack((r, g, b), axis=2).astype("uint8")
    #im_conv = np.array([r,g,b])
    #im_conv = r + g + b
    #print(im_conv)
    return im_conv


# mipi raw 转Bayer raw
# 返回值：bayer raw image
def mipiRaw_2_Bayer(filepath,width = "2592",height = "1944",raw_deepth="raw10",byteorder="big"):
    size = os.path.getsize(filepath)  # 获得文件大小
    img_wid = int(width)
    img_hei = int(height)
    print(size)

    # raw10
    # 5个byte存储4个pixel,其中第5个byte分割成4个两位，分别补到前面四个pixel的低两位
    # P1[9:2] --> P2[9:2] --> P3[9:2] --> P4[9:2] --> P1[1:0] --> P2[1:0] --> P3[1:0] --> P4[1:0]
    if (raw_deepth == 'raw10'):
        # fo = open(filepath, 'rb+')
        # a = np.zeros(size, dtype=np.uint16)
        # for i in range(size):
        #     data = fo.read(1) #每次输出一个字节
        #     num = int.from_bytes(data, byteorder=byteorder)
        #     a[i] = num
        a = np.fromfile(filepath,dtype='u1')   # u1 = uint8 ; u2 = uint16 ;
        #print("mipi raw原始数据",a)
        # b = np.array(a)
        #b = np.zeros(shape=img_hei*img_wid,dtype=np.uint16)
        b = []
        for c in range(0, size, 5):
            b.append((a[c]<< 2) + ((a[c + 4] >> 0) & 0x03))
            b.append((a[c + 1]<< 2) + ((a[c + 4] >> 2) & 0x0c))
            b.append((a[c + 2]<< 2) + ((a[c + 4] >> 4) & 0x30))
            b.append((a[c + 3]<< 2) + ((a[c + 4] >> 6) & 0xc0))

        # for c in range(size):
        #     if (c + 1) % 5 == 0:
        #         continue
        #     else:
        #         b.append(a[c])

        k = np.array(b)
        #print("bayer raw数据转换为numpy数组：",k)
        m = k.reshape(img_hei, img_wid)
        #print("bayer raw转置为对应尺寸图片数组：",m)



    # raw8
    # 单字节对齐
    # P1[7:0] --> P2[7:0] --> P3[7:0] --> P4[7:0]
    elif (raw_deepth == 'raw8'):
        a = np.fromfile(filepath,dtype='u1')   # u1 = uint8 ; u2 = uint16 ;
        #print("mipi raw原始数据",a)
        k = np.array(a)
        #print("bayer raw数据转换为numpy数组：",k)
        m = k.reshape((img_hei, img_wid))
        #print("bayer raw转置为对应尺寸图片数组：",m)

    # raw12
    # 3个byte存储2个pixel
    # P1[11:4] --> P2[11:4] --> P2[3:0] --> P1[3:0]
    elif (raw_deepth == 'raw12'):
        a = np.fromfile(filepath,dtype='u1')   # u1 = uint8 ; u2 = uint16 ;
        #print("mipi raw原始数据",a)
        b = []
        for c in range(0,size,3):
            b.append((a[c] << 4) + (a[c+2] & 0x0f))
            b.append((a[c+1] << 4) + ((a[c+2] >> 4) & 0x0f))

        #print("转换为bayer raw数据：",b)
        k = np.array(b)
        #print("bayer raw数据转换为numpy数组：",k)
        m = k.reshape((img_hei, img_wid))
        #print("bayer raw转置为对应尺寸图片数组：",m)

    return m


# dothin raw 转 Bayer raw
# 返回值：bayer raw image
def dothinRaw_2_Bayer(filepath,width = "2592",height = "1944",raw_deepth="raw10",byteorder="big"):
    size = os.path.getsize(filepath)  # 获得文件大小
    img_wid = int(width)
    img_hei = int(height)
    print(size)

    # raw10
    # 2个byte存储1个pixel
    # P1[9:2] --> P2[9:2] --> P3[9:2] --> P4[9:2]
    if (raw_deepth == 'raw10'):

        a = np.fromfile(filepath,dtype='u2')   # u1 = uint8 ; u2 = uint16 ;
        np.savetxt("raw.txt",a)
        print(a)

        # b = []
        # for c in range(0, size, 5):
        #     b.append((a[c]<< 2) + ((a[c + 4] >> 0) & 0x03))
        #     b.append((a[c + 1]<< 2) + ((a[c + 4] >> 2) & 0x0c))
        #     b.append((a[c + 2]<< 2) + ((a[c + 4] >> 4) & 0x30))
        #     b.append((a[c + 3]<< 2) + ((a[c + 4] >> 6) & 0xc0))
        # k = np.array(b)
        k = np.array(a)
        m = k.reshape(img_hei, img_wid)
        print(m)




    # raw8
    # 单字节对齐
    # P1[7:0] --> P2[7:0] --> P3[7:0] --> P4[7:0]
    elif (raw_deepth == 'raw8'):
        a = np.fromfile(filepath,dtype='u1')   # u1 = uint8 ; u2 = uint16 ;
        print(a)
        k = np.array(a)
        m = k.reshape((img_hei, img_wid))


    # raw12
    # 3个byte存储2个pixel
    # P1[11:4] --> P2[11:4] --> P2[3:0] --> P1[3:0]
    elif (raw_deepth == 'raw12'):
        a = np.fromfile(filepath,dtype='u1')   # u1 = uint8 ; u2 = uint16 ;

        b = []
        for c in range(0,size,3):
            b.append((a[c] << 4) + (a[c+2] & 0x0f))
            b.append((a[c+1] << 4) + ((a[c+2] >> 4) & 0x0f))

        k = np.array(b)
        m = k.reshape((img_hei, img_wid))

    return m

