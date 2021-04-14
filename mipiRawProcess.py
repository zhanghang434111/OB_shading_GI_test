import numpy as np
import os


# bayer raw 转 BMP
# 返回值：BMP图像数组
def bayerRaw2bmp(img_raw,bayerpattern = "B"):
    r = np.zeros((img_raw.shape),dtype=np.uint8)
    g = np.zeros((img_raw.shape),dtype=np.uint8)
    b = np.zeros((img_raw.shape),dtype=np.uint8)
    # BGGR
    # B G B G B
    # G R G R G
    # B G B G B
    # G R G R G
    if (bayerpattern == "B"):
        r[1::2, 1::2] = img_raw[1::2, 1::2]
        b[::2, ::2] = img_raw[1::2, ::2]
        g[::2, 1::2] = img_raw[::2, 1::2]
        g[1::2, ::2] = img_raw[1::2, ::2]

    # RGGB
    # R G R G R
    # G B G B G
    # R G R G R
    # G B G B G
    elif (bayerpattern == "R"):
        # b[1::2, 1::2, :] = img_raw[1::2, 1::2]
        # r[::2, ::2, :] = img_raw[::2, ::2]
        # g[::2, 1::2, :] = img_raw[::2, 1::2]
        # g[1::2, ::2, :] = img_raw[1::2, ::2]

        b[1::2, 1::2] = img_raw[1::2, 1::2]
        r[::2, ::2] = img_raw[::2, ::2]
        g[::2, 1::2] = img_raw[::2, 1::2]
        g[1::2, ::2] = img_raw[1::2, ::2]

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
    #im_conv = np.array([r,g,b])
    #im_conv = r + g + b
    print(im_conv)
    return im_conv

    #img.imsave(r'C:\Users\herman\Desktop\py_raw_test\xxxx.bmp', im_conv)


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
        #a = np.fromfile(filepath, dtype=np.uint16)
        # fo = open(filepath, 'rb+')
        # a = np.zeros(size, dtype=np.uint16)
        # for i in range(size):
        #     data = fo.read(1) #每次输出一个字节
        #     num = int.from_bytes(data, byteorder=byteorder)
        #     a[i] = num

        a = np.fromfile(filepath,dtype='u1')   # u1 = uint8 ; u2 = uint16 ;
        print("mipi raw原始数据",a)
        '''
        p1 = (a[0] << 2) + (a[4] & 0x03)
        p2 = (a[1] << 2) + (a[4] & 0x0c)
        p3 = (a[2] << 2) + (a[4] & 0x30)
        p4 = (a[3] << 2) + (a[4] & 0xc0)
        
        p1 =( (b4>>6) & 0x3 ) + (b0 >>2));
        p2 =( (b4>>4) & 0x3 ) + (b1 >>2));
        p3 =( (b4>>2) & 0x3 ) + (b2 >>2));
        p4 =(  b4     & 0x3 ) + (b3 >>2));
        '''
        # b = np.array(a)
        b = np.zeros(shape=img_hei*img_wid,dtype=np.uint16)
        print(b.shape)
        #for c in range(size):
        for c in range(0, size-4, 5):

            b[c] = ((a[c] << 2) + (a[c+4] & 0x03))
            b[c+1] = ((a[c+1] << 2) + (a[c+4] & 0x0c))
            b[c+2] = ((a[c+2] << 2) + (a[c+4] & 0x30))
            b[c+3] = ((a[c+3] << 2) + (a[c+4] & 0xc0))

            # b[c] = a[c] + ((a[c + 4] & 0xc0)) << 2
            # b[c + 1] = a[c+1] + ((a[c + 4] & 0x30)) << 2
            # b[c + 2] = a[c+2] + ((a[c + 4] & 0x0c)) << 2
            # b[c + 3] = a[c+3] + ((a[c + 4] & 0x03)) << 2

        #print(b[3],b[4],b[5])
        # k = b[:(img_hei*img_wid)]
        # print("bayer raw数据转换为numpy数组：",k)
        m = b.reshape((img_hei, img_wid))
        print("bayer raw转置为对应尺寸图片数组：",m)


    # raw8
    # 单字节对齐
    # P1[7:0] --> P2[7:0] --> P3[7:0] --> P4[7:0]
    elif (raw_deepth == 'raw8'):
        size = os.path.getsize(filepath)  # 获得文件大小
        fo = open(filepath, 'rb+')
        a = np.zeros(size, dtype=int)
        for i in range(size):
            data = fo.read(1)  # 每次输出一个字节
            num = int.from_bytes(data, byteorder='big')
            a[i] = num
        print("mipi raw原始数据",a)
        k = np.array(a)
        print("bayer raw数据转换为numpy数组：",k)
        m = k.reshape((1200, 1600))
        print("bayer raw转置为对应尺寸图片数组：",m)

    # raw12
    # 3个byte存储2个pixel
    # P1[11:4] --> P2[11:4] --> P2[3:0] --> P1[3:0]
    elif (raw_deepth == 'raw12'):
        size = os.path.getsize(filepath) #获得文件大小
        fo = open(filepath, 'rb+')
        a = np.zeros(size, dtype=int)
        for i in range(size):
            data = fo.read(1) #每次输出一个字节
            num = int.from_bytes(data, byteorder='big')
            a[i] = num
        print("mipi raw原始数据",a)
        '''
        p1 = (a[0] << 4) + (a[2] & 0x0f)
        p2 = (a[1] << 4) + (a[2] & 0xf0)
        '''
        b = []
        for c in range(0,size,3):
            b.append((a[c] << 4) + (a[c+2] & 0x0f))
            b.append((a[c+1] << 4) + (a[c + 2] & 0xf0))

        print("转换为bayer raw数据：",b)
        k = np.array(b)
        print("bayer raw数据转换为numpy数组：",k)
        m = k.reshape((1200, 1600))
        print("bayer raw转置为对应尺寸图片数组：",m)

    return m