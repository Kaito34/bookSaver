import pyautogui as pg
import time
import os
import datetime
from tqdm import tqdm
from PIL import Image
import numpy as np
import random
import argparse
import yaml


def check_position():
    """キャプチャ座標計測
    """
    
    loc_dict = {}

    # 左上座標を取得
    print('キャプチャ範囲の左上座標にマウスカーソルを合わせる')
    time.sleep(3)
    loc = pg.position()
    print('左上座標：' + str(loc))
    
    loc_dict['x1'] = loc[0]
    loc_dict['y1'] = loc[1]

    # １秒待機
    time.sleep(1)

    # 右下座標を取得
    print('キャプチャ範囲の右下座標にマウスカーソルを合わせる')
    time.sleep(3)
    loc = pg.position()
    print('右下座標：' + str(loc))
    
    loc_dict['x2'] = loc[0]
    loc_dict['y2'] = loc[1]
       
    
    with open('tmp_data/key_loc.yaml','w') as f:
        yaml.dump(loc_dict, f)


def check_mac_error():
    # macの位置のずれを修正する
    print(pg.size())
    time.sleep(2)
    x, y = pg.position()

    # terminalの位置で検証
    x_, y_ = pg.locateCenterOnScreen('../data/terminal.png', grayscale=True, confidence=0.8)

    print(x/x_)
    print(y/y_)

    '''
    本来
    0.49981929887965304
    0.5006954102920723
    '''


def img_mse(prev_img_path, img_path):
    prev_img_arr = np.array(Image.open(prev_img_path))
    img_arr = np.array(Image.open(img_path))
    mse_loss = (np.square(prev_img_arr - img_arr)).mean()
    return mse_loss



def take_screen_shot(page=350, span=1, key_forward='right'):
    """_summary_

    Args:
        page (int, optional): ページ数. Defaults to 350.
        span (int, optional): スクショ間隔. Defaults to 1.
        key_forward (str, optional): どっち向きにページを進めるか. Defaults to 'right'.
    """

    with open('tmp_data/key_loc.yaml') as f:
        loc_dict = yaml.safe_load(f)
        
    # 取得範囲：左上座標
    x1, y1 = loc_dict['x1'], loc_dict['y1']
    # 取得範囲：右下座様
    x2, y2 = loc_dict['x2'], loc_dict['y2']
    # mac用に変換
    x1 = x1/0.5
    x2 = x2/0.5
    y1 = y1/0.5
    y2 = y2/0.5
    # 出力フォルダ頭文字
    h_foldername = "../data/"
    # 出力ファイル頭文字
    h_filename = "page"

    #########################
    # スクリーンショット取得処理
    #########################
    # 待機時間５秒
    # (この間にスクショを取得するウィンドウをアクティブにする)
    print('ウィンドウをアクティブにしてください')
    time.sleep(5)

    # 出力フォルダ作成(フォルダ名：頭文字_年月日時分秒)
    folder_name = h_foldername + "_" + str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    os.mkdir(folder_name)

    # ページ数分スクリーンショットをとる
    same_img_count = 0
    prev_mse_loss = None
    for p in tqdm(range(page)):

        # 出力ファイル名(頭文字_連番.png)
        out_filename = h_filename + "_" + str(p+1).zfill(4) + '.png'
        # 偶数ページ前で終了を判断
        if p == 0:
            prev_out_filename = h_filename + "_" + str(p+1).zfill(4) + '.png'
        elif p % 2 == 0:
            prev_out_filename = h_filename + "_" + str(p).zfill(4) + '.png'
        # スクリーンショット取得・保存処理
        # キャプチャ範囲： 左上のx座標, 左上のy座標, 幅, 高さ
        s = pg.screenshot(region=(x1, y1, x2-x1, y2-y1))
        # 出力パス： 出力フォルダ名 / 出力ファイル名
        s.save(folder_name + '/' + out_filename)

        mse_loss = img_mse(
            prev_img_path=folder_name + '/' + prev_out_filename,
            img_path=folder_name + '/' + out_filename)
        # 偶数ページ前で終了を判断
        if p % 2 == 0:

            if prev_mse_loss is None:
                prev_mse_loss = mse_loss
            elif int(prev_mse_loss * 100) == int(mse_loss * 100):
                same_img_count += 1
                print(prev_mse_loss, mse_loss, same_img_count)
                if same_img_count > 2:
                    break
            else:
                same_img_count = 0

            prev_mse_loss = mse_loss
        # 右矢印キー押下
        pg.keyDown(key_forward)
        # 次のスクリーンショットまで待機
        time.sleep(span+random.uniform(1, 3))

    print('done')


def main():
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--action')
    args = parser.parse_args()
    """
    check_position()
    take_screen_shot(page=4000, span=1, key_forward='enter')

if __name__ == '__main__':
    main()
