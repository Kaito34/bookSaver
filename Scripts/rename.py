import os
import img2pdf
from PIL import Image  # img2pdfと一緒にインストールされたPillowを使います
import glob
import re
import numpy as np
from tqdm import tqdm

import pyocr
import pyocr.builders

# 1.OCRエンジンの取得
tools = pyocr.get_available_tools()
tool = tools[0]

# 2.原稿画像の読み込み
# ソースと同じフォルダに配置している画像ファイル
img_org = Image.open("../data/_20210813231615/page_0001.png")

# 3.ＯＣＲ実行
# tesseract_layout=3はディフォルト設定値となります。
# 5を設定した場合は、縦読みを実施できます。
builder = pyocr.builders.TextBuilder(tesseract_layout=3)
result = tool.image_to_string(img_org, lang="jpn", builder=builder)

# 結果出力
print("\n"+result)
