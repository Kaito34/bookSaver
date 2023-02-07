import os
import img2pdf
from PIL import Image  # img2pdfと一緒にインストールされたPillowを使います
import glob
import re
import numpy as np
from tqdm import tqdm


def convert_to_jpeg(bookpath):
    """pngをpdfに変える

    Args:
        png_Folder ([type]): [description]
    """
    png_Folder = bookpath + '/'
    files = glob.glob(png_Folder + '*.png')
    match = re.compile("(png)")
    print(png_Folder + " convert start")
    for file_name in files:
        im = Image.open(file_name)
        im = im.convert("RGB")
        new_file_name = match.sub("jpeg", file_name)
        os.remove(file_name)
        im.save(new_file_name, quality=95, resolution=600)


def get_jpeg_list(bookpath):
    # jpegファイルを順番にリストに入れる
    jpeg_FileName = bookpath + '/*.jpeg'
    jpeg_list = []
    prev_im_arr = None
    prev_mse_loss = None
    same_img_count = 0
    for j in range(1, len(glob.glob(jpeg_FileName)) + 1):
        jpegname = bookpath + f'/page_{str(j).zfill(4)}.jpeg'
        im_arr = np.array(Image.open(jpegname))
        if prev_im_arr is None:
            prev_im_arr = im_arr

        mse_loss = (np.square(im_arr - prev_im_arr)).mean()
        # 偶数ページ前で終了を判断
        if j % 2 == 0:
            if prev_mse_loss is None:
                prev_mse_loss = mse_loss
            elif int(prev_mse_loss * 100) == int(mse_loss * 100):
                same_img_count += 1
                if same_img_count > 2:
                    break
            else:
                same_img_count = 0
        # print(prev_mse_loss, mse_loss, same_img_count)
        jpeg_list.append(jpegname)
        prev_mse_loss = mse_loss

    jpeg_list = jpeg_list[:-8]  # 8
    return jpeg_list


def save_pdf(bookpath, jpeg_list):
    pdf_FileName = bookpath + '.pdf'
    with open(pdf_FileName, "wb") as f:
        # 画像フォルダの中にあるPNGファイルを取得し配列に追加、バイナリ形式でファイルに書き込む
        f.write(img2pdf.convert([Image.open(j).filename for j in jpeg_list]))


def jpeg_to_pdf():
    for bookpath in tqdm(glob.glob("../data/*")):
        try:
            convert_to_jpeg(bookpath)
            jpeg_list = get_jpeg_list(bookpath)
            save_pdf(bookpath, jpeg_list)
        except:
            print("ERROR: ", bookpath)
    print('done')


def merge_two_into_pdf(name):
    bookpath1 = '../data/' + name
    bookpath2 = '../data/' + name + '2'
    jpeg_lists = []
    for bookpath in [bookpath1, bookpath2]:
        convert_to_jpeg(bookpath)
        jpeg_list = get_jpeg_list(bookpath)
        jpeg_lists.extend(jpeg_list)
    save_pdf(bookpath1, jpeg_lists)

    print('done')


jpeg_to_pdf()
