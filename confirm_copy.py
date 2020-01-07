#coding:utf-8
import os,shutil

#ファイルのコピー、入れ替え
src = 'templates/recipt.json'
scr_template = 'templates/recipt_template.json'
if os.path.isfile(src) and os.path.isfile(scr_template):
    print("コピー")
    shutil.copy('templates/recipt_template.json', 'templates/recipt.json')