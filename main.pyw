from urllib import request
import datetime
import os
import ctypes
import shutil


# '''https://himawari8-dl.nict.go.jp/himawari.asi/img/D531106/1d/550/2019/07/01/124000_0_0.png
# https://himawari8-dl.nict.go.jp/himawari.asia/img/D531106/1d/550/2019/07/01/021000_0_0.png
# https://himawari8-dl.nict.go.jp/himawari.asia/img/D531106/1d/550/2019/06/30/234000_0_0.png
# https://himawari8-dl.nict.go.jp/himawari.asia/img/D531106/1d/550/2019/06/29/045000_0_0.png'''

folder_name = '\\tmp_img\\'
url = 'http://himawari8-dl.nict.go.jp/himawari8/img/D531106/1d/550/'
# Задержка в часах
delay = 24 # (3-4 часа ночи по Мск - полная земля)

def del_imgs(file_path):
    try:
        if (len(os.listdir(file_path))) >= 12:
            shutil.rmtree(file_path)
    except:
        pass

def ensure_dir(file_path):
    if not os.path.exists(file_path):
        os.makedirs(file_path)

def data_with_delay(data):
    new_data = data
    new_data['H'] -= delay
    while new_data['H'] < 0:
        new_data['H'] += 24
        new_data['D'] -= 1
        if new_data['D'] <= 0:
            new_data['D'] += 29
            new_data['M'] -= 1
            if new_data['M'] <= 0:
                new_data['M'] += 12
                new_data['Y'] -= 1
    return new_data

def dl_img(file_path,file_name,new_data):
    full_path = file_path + file_name
    full_url = url + '/'.join(['{:04d}'.format(new_data['Y']), '{:02d}'.format(new_data['M']), '{:02d}'.format(new_data['D'])]) +\
         '/' + '{:02d}'.format(new_data['H'])+'{:02d}'.format(new_data['m'])[0]+ '000_0_0.png'
    # print(full_url)
    request.urlretrieve(full_url, full_path)

def set_background(file_path, file_name):
    if os.path.exists(file_path + file_name):
        ctypes.windll.user32.SystemParametersInfoW(20, 0, file_path + file_name , 0)


def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path =dir_path + folder_name
    now = datetime.datetime.now()
    data = {'Y':now.year, 'M':now.month, 'D':now.day, 'H': now.hour, 'm':now.minute}
    # Название изображения Земли в зависимости от текущего времени.
    file_name = '_'.join(['{:04d}'.format(data['Y']), '{:02d}'.format(data['M']), '{:02d}'.format(data['D'])]) +\
            '_' + '{:02d}'.format(data['H'])+'{:02d}'.format(data['m'])[0]+ '000_0_0.png' 

    del_imgs(file_path)
    ensure_dir(file_path)
    new_data = data_with_delay(data)
    dl_img(file_path, file_name, new_data)
    set_background(file_path, file_name)

main()