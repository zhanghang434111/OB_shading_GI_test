import mipiRawProcess
import basicTest
import matplotlib.pylab as plt
import matplotlib.image as img

filepath = r'C:\Users\herman\Desktop\OB test\D.mipi_raw'
bayer_raw = mipiRawProcess.mipiRaw_2_Bayer(filepath)
# img_bmp = mipiRawProcess.bayerRaw2bmp(bayer_raw,bayerpattern="B")
# img.imsave("new.bmp",img_bmp)

#imgsrc = plt.imread(r'C:\Users\herman\Desktop\OB test\D.mipi_raw')
block_width = int(input("区域划分,横坐标block数："))
block_height = int(input("区域划分,纵坐标block数："))

print(basicTest.GI_test(bayer_raw,block_width,block_height))
basicTest.blockData2Excel(basicTest.ob_test(bayer_raw, block_width, block_height))
img.imsave('new.jpg',basicTest.ob_test(bayer_raw,block_width,block_height))
plt.show()





if __name__ == '__main__':
    print('PyCharm')


