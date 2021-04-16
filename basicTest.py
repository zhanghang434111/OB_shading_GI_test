import numpy as np
import pandas as pd
import scipy.misc
import sys
import cv2


# ob test
# 返回值：blocks value mean
def intensity_test(img_raw,block_x,block_y):
    hei = img_raw.shape[0]
    wid = img_raw.shape[1]
    OB_block_value = np.zeros((block_y, block_x), dtype=np.float)

    # 划分 17 * 13 个 blocks,多余行和列放入中间block
    block_hei = hei // block_y
    block_wid = wid // block_x
    mid_block_hei = block_hei + hei % block_y
    mid_block_wid = block_wid + wid % block_x
    #print("block高：",block_hei, "block宽：",block_wid, "中心block高：",mid_block_hei, "中心block宽：",mid_block_wid)
    #np.set_printoptions(suppress=True)
    for row in range(block_y):
        for col in range(block_x):
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
def get_raw_channle(img_raw,bayerpattern):
    R_channle = np.zeros((img_raw.shape),dtype=np.uint16)
    Gr_channle = np.zeros((img_raw.shape),dtype=np.uint16)
    Gb_channle = np.zeros((img_raw.shape),dtype=np.uint16)
    B_channle = np.zeros((img_raw.shape),dtype=np.uint16)

    # BGGR
    # B G B G B G
    # G R G R G R
    # B G B G B G
    # G R G R G R
    if bayerpattern == "B":
        # R_channle[1::2, 1::2] = img_raw[1::2, 1::2]
        # Gr_channle[1::2, ::2] = img_raw[1::2, ::2]
        # Gb_channle[::2, 1::2] = img_raw[::2, 1::2]
        # B_channle[::2, ::2] = img_raw[::2, ::2]
        R_channle[1::2, 1::2] = img_raw[1::2, 1::2]
        Gr_channle[1::2, ::2] = img_raw[1::2, ::2]
        Gb_channle[::2, 1::2] = img_raw[::2, 1::2]
        B_channle[::2, ::2] = img_raw[::2, ::2]

    # RGGB
    # R G R G R
    # G B G B G
    # R G R G R
    # G B G B G
    if bayerpattern == "R":
        B_channle[1::2, 1::2] = img_raw[1::2, 1::2]
        Gb_channle[1::2, ::2] = img_raw[1::2, ::2]
        Gr_channle[::2, 1::2] = img_raw[::2, 1::2]
        R_channle[::2, ::2] = img_raw[::2, ::2]

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

    return R_channle, Gr_channle, Gb_channle, B_channle


#blocks 数据写入Excel
def blockData2Excel(imgBlockData,output = 'test.xlsx',page='GI'):
    dataFrame = pd.DataFrame(imgBlockData)

    # with pd.ExcelWriter('test.xlsx') as writer: # 一个excel写入多页数据
    #     dataFrame.to_excel(writer, sheet_name='page1', float_format='%.6f')
    writer = pd.ExcelWriter(output)  # 写入Excel文件
    dataFrame.to_excel(writer, page, float_format='%.6f')  # ‘page_1’是写入excel的sheet名
    writer.save()


# GI test
# 返回值：blocks GI
# 返回值 0
def GI_test(imgraw,block_x="17",block_y="13",bayerpattern="R"):
    R, Gr, Gb, B = get_raw_channle(imgraw, bayerpattern)
    if bayerpattern == "R":
        Gr_new = Gr[0::2,1::2]
        Gb_new = Gb[1::2,0::2]
    elif bayerpattern == "B":
        Gb_new = Gr[0::2,1::2]
        Gr_new = Gb[1::2,0::2]
    elif bayerpattern == "Gr":
        Gr_new = Gr[0::2,0::2]
        Gb_new = Gb[1::2,1::2]
    elif bayerpattern == "Gb":
        Gb_new = Gr[0::2, 0::2]
        Gr_new = Gb[1::2, 1::2]

    Gr_data = intensity_test(Gr_new,int(block_x),int(block_y))
    Gb_data = intensity_test(Gb_new,int(block_x),int(block_y))
    # print(Gr_data)
    # print(Gb_data)
    GIdata = ((Gr_data/Gb_data) -1)
    GI_mean = np.mean(GIdata)
    print(GI_mean)
    dataFrame = pd.DataFrame(GIdata)
    # with pd.ExcelWriter('test.xlsx') as writer: # 一个excel写入多页数据
    #     dataFrame.to_excel(writer, sheet_name='page1', float_format='%.6f')
    writer = pd.ExcelWriter('GI.xlsx')  # 写入Excel文件
    dataFrame.to_excel(writer, 'GI', float_format='%.6f')  # ‘page_1’是写入excel的sheet名
    writer.save()
    #return GIdata
    return 0

# OB & shading test
# 返回值 mean,R,Gr,Gb,B
# 返回值 0
# add WB test
def OB_shading_test(imgraw,block_x="17",block_y="13",bayerpattern="R"):
    R, Gr, Gb, B = get_raw_channle(imgraw, bayerpattern)
    if bayerpattern == "R":
        R_new = R[0::2, 0::2]
        B_new = B[1::2, 1::2]
        Gr_new = Gr[0::2, 1::2]
        Gb_new = Gb[1::2, 0::2]
    elif bayerpattern == "B":
        B_new = R[0::2, 0::2]
        R_new = B[1::2, 1::2]
        Gb_new = Gr[0::2, 1::2]
        Gr_new = Gb[1::2, 0::2]
    elif bayerpattern == "Gr":
        R_new = R[0::2, 1::2]
        B_new = B[1::2, 0::2]
        Gr_new = Gr[0::2, 0::2]
        Gb_new = Gb[1::2, 1::2]
    elif bayerpattern == "Gb":
        B_new = R[0::2, 1::2]
        R_new = B[1::2, 0::2]
        Gb_new = Gr[0::2, 0::2]
        Gr_new = Gb[1::2, 1::2]

    R_data = intensity_test(R_new, int(block_x), int(block_y))
    B_data = intensity_test(B_new, int(block_x), int(block_y))
    Gr_data = intensity_test(Gr_new, int(block_x), int(block_y))
    Gb_data = intensity_test(Gb_new, int(block_x), int(block_y))
    RG_data = (R_data / Gr_data)
    BG_data = (B_data / Gr_data)
    mean_data = intensity_test(imgraw, int(block_x), int(block_y))

    RG_mean = np.mean(RG_data)
    BG_mean = np.mean(BG_data)

    df_meam = pd.DataFrame(mean_data)
    df_R = pd.DataFrame(R_data)
    df_Gr = pd.DataFrame(Gr_data)
    df_Gb = pd.DataFrame(Gb_data)
    df_B = pd.DataFrame(B_data)
    df_RG = pd.DataFrame(RG_data)
    df_BG = pd.DataFrame(BG_data)

    # with pd.ExcelWriter('test.xlsx') as writer: # 一个excel写入多页数据
    #     dataFrame.to_excel(writer, sheet_name='page1', float_format='%.6f')
    writer = pd.ExcelWriter('block_value.xlsx')  # 写入Excel文件
    df_meam.to_excel(writer, "mean", float_format='%.6f')  # ‘page_1’是写入excel的sheet名
    df_R.to_excel(writer, "R", float_format='%.6f')
    df_Gr.to_excel(writer, "Gr", float_format='%.6f')
    df_Gb.to_excel(writer, "Gb", float_format='%.6f')
    df_B.to_excel(writer, "B", float_format='%.6f')
    df_RG.to_excel(writer, "R_G", float_format='%.6f')
    df_BG.to_excel(writer, "B_G", float_format='%.6f')
    writer.save()

    #return mean_data,R_data,B_data,Gr_data,Gb_data
    return 0







