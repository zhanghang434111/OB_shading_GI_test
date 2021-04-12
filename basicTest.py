import numpy as np
import matplotlib.pylab as plt
import matplotlib.image as img
import pandas as pd
import scipy.misc
import sys
import cv2
from scipy import misc

# ob test
# 返回值：blocks value mean
def ob_test(img_raw,block_x,block_y):
    hei = img_raw.shape[0]
    wid = img_raw.shape[1]
    #channel = img_raw.shape[2]
    OB_block_value = np.zeros((block_y, block_x), dtype=float)

    # 划分 17 * 13 个 blocks,多余行和列放入中间block
    block_hei = hei // block_y
    block_wid = wid // block_x
    mid_block_hei = block_hei + hei % block_y
    mid_block_wid = block_wid + wid % block_x
    print("block高：",block_hei, "block宽：",block_wid, "中心block高：",mid_block_hei, "中心block宽：",mid_block_wid)

    for row in range(0,block_y):
        for col in range(0,block_x):
            if (col <block_y//2 & row < block_y//2):
                OB_block_value[row, col] = np.mean(
                    img_raw[block_hei * row:block_hei * (row + 1), block_wid * col:block_wid * (col + 1)])
            elif (col < block_x//2 & row == block_y//2):
                    OB_block_value[row, col] = np.mean(
                        img_raw[block_hei * row:block_hei * row + mid_block_hei, block_wid * col:block_wid * (col+1)])
            elif (col < block_x//2 & row > block_y//2):
                    OB_block_value[row, col] = np.mean(
                        img_raw[block_hei * (row-1) + mid_block_hei:block_hei * row + mid_block_hei, block_wid * col:block_wid * (col+1)])


            elif (col == block_x//2 & row < block_y//2):
                OB_block_value[row, col] = np.mean(
                    img_raw[block_hei * row:block_hei * (row + 1), block_wid * col:block_wid * col + mid_block_wid])
            elif (col == block_x//2 & row == block_y//2):
                OB_block_value[row, col] = np.mean(
                    img_raw[block_hei * row:block_hei * row + mid_block_hei, block_wid * col:block_wid * col + mid_block_wid])
            elif (col == block_x//2 & row > block_y//2):
                OB_block_value[row, col] = np.mean(
                    img_raw[block_hei * (row-1) + mid_block_hei:block_hei * row + mid_block_hei, block_wid * col:block_wid * col + mid_block_wid])


            elif (col > block_x//2 & row < block_y//2):
                OB_block_value[row, col] = np.mean(
                    img_raw[block_hei * row:block_hei * (row + 1), block_wid * (col-1) + mid_block_wid:block_wid * col + mid_block_wid])
            elif (col > block_x // 2 & row == block_y // 2):
                OB_block_value[row, col] = np.mean(
                    img_raw[block_hei * row:block_hei * row + mid_block_hei,block_wid * (col - 1) + mid_block_wid:block_wid * col + mid_block_wid])
            elif (col > block_x//2 & row > block_y//2):
                    OB_block_value[row, col] = np.mean(
                        img_raw[block_hei * (row-1) + mid_block_hei:block_hei * row + mid_block_hei, block_wid * (col-1) + mid_block_wid:block_wid * col + mid_block_wid])
    return OB_block_value

#图片分通道
# 返回值：R、Gr、Gb、B四通道值，对应其它三个通道置0
def raw_channle(img_raw,bayerpattern):
    R_channle = np.copy(img_raw)
    Gr_channle = np.copy(img_raw)
    Gb_channle = np.copy(img_raw)
    B_channle = np.copy(img_raw)

    # BGGR
    # B G B G B G
    # G R G R G R
    # B G B G B G
    # G R G R G R
    if bayerpattern == "B":
        R_channle = img_raw[1::2, 1::2]
        Gr_channle = img_raw[1::2, ::2]
        Gb_channle = img_raw[::2, 1::2]
        B_channle = img_raw[::2, ::2]

    # RGGB
    # R G R G R
    # G B G B G
    # R G R G R
    # G B G B G
    if bayerpattern == "R":
        B_channle = img_raw[1::2, 1::2]
        Gb_channle = img_raw[1::2, ::2]
        Gr_channle = img_raw[::2, 1::2]
        R_channle = img_raw[::2, ::2]

    # GRBG
    # G R G R G
    # B G B G B
    # G R G R G
    # B G B G B
    if bayerpattern == "Gr":
        Gb_channle = img_raw[1::2, 1::2]
        B_channle = img_raw[1::2, ::2]
        R_channle = img_raw[::2, 1::2]
        Gr_channle = img_raw[::2, ::2]

    # GBRG
    # G B G B G
    # R G R G R
    # G B G B G
    # R G R G R
    if bayerpattern == "Gb":
        Gr_channle = img_raw[1::2, 1::2]
        R_channle = img_raw[1::2, ::2]
        B_channle = img_raw[::2, 1::2]
        Gb_channle = img_raw[::2, ::2]

    print(B_channle)
    return R_channle, Gr_channle, Gb_channle, B_channle



    # for ver in range(0, hei-1):
    #     for hor in range(0, wid-1):
    #         if ((0 == np.mod(ver, 2)) & (0 == np.mod(hor, 2))):
    #             bayerPadding[ver, hor] = img_raw[ver-1, hor-1, 0]
    #             # R 通道
    #         elif ((1 == np.mod(ver, 2)) & (1 == np.mod(hor, 2))):
    #             bayerPadding[ver, hor] = img_raw[ver-1, hor-1, 2]
    #             # B 通道
    #         else:
    #             bayerPadding[ver, hor] = img_raw[ver-1, hor-1, 1]
    #             # G 通道

#blocks 数据写入Excel
def blockData2Excel(imgBlockData):
    dataFrame = pd.DataFrame(imgBlockData,
                             columns=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15',
                                      '16', '17'],
                             index=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13'])  # 说明行和列的索引名

    with pd.ExcelWriter('test.xlsx') as writer: # 一个excel写入多页数据
        dataFrame.to_excel(writer, sheet_name='page1', float_format='%.6f')
        # dataFrame_15x15.to_excel(writer, sheet_name='page2', float_format='%.6f')

# GI test
# 返回值：blocks GI
def GI_test(imgraw,block_x,block_y):
    R, Gr, Gb, B = raw_channle(imgraw, "B")
    GIdata = np.zeros((block_y,block_x), dtype=float)
    Gr_data = ob_test(Gr,block_x,block_y)
    Gb_data = ob_test(Gb, block_x, block_y)
    GIdata = Gr_data / Gb_data - 1
    return GIdata







