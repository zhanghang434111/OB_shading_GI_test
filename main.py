import mipiRawProcess
import basicTest
import matplotlib.pylab as plt
import matplotlib.image as img

imgsrc = plt.imread(r'C:\Users\herman\Desktop\raw\02m1_source.bmp')
block_width = int(input("区域划分,横坐标block数："))
block_height = int(input("区域划分,纵坐标block数："))

print(basicTest.GI_test(imgsrc))
#print('%.2f%%' % (GI_test(imgsrc) * 100))

#R,Gr,Gb,B = raw_channle(imgsrc,"B")

basicTest.blockData2Excel(basicTest.ob_test(imgsrc, block_width, block_height))

#img.imsave('B.jpg',B)
img.imsave('new.jpg',basicTest.ob_test(imgsrc,block_width,block_height))
#plt.imshow(imSrc)
plt.show()

filepath = r'C:\Users\herman\Desktop\raw\2_1600_1200.mipi_raw'
bayer_raw = mipiRawProcess.mipiRaw_2_Bayer(filepath)
img_bmp = mipiRawProcess.bayerRaw2bmp(bayer_raw,bayerpattern="B")
img.imsave("new.bmp",img_bmp)


if __name__ == '__main__':
    print('PyCharm')


