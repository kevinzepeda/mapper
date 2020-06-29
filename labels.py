import os
from os import listdir
from os.path import isfile, isdir
from tqdm import tqdm
from PIL import Image,ImageDraw, ImageFont

path_files = input(f"Ruta de los archivos? ({os.getcwd()}/out/): ")
if path_files == "":
    path_files = os.getcwd()+"/out/"

#Funcion para listar archivos
def ls(path):
    return [obj for obj in listdir(path) if isfile(path + obj) and ".~" not in obj[:2] and ".png" in obj[obj.find("."):]]

font = ImageFont.truetype("/home/kevin/Work/mapper/Montserrat/Montserrat-Bold.ttf",15)
font2 = ImageFont.truetype("/home/kevin/Work/mapper/Montserrat/Montserrat-Medium.ttf",10)

files=ls(path_files)
for file in tqdm(files):
    if file == 'vacio.png':
        no = 'Vacios'
    if file == 'ran-region-all.png':
        no = '1-9'
    else:
        no = file[11:file.find(".")]
    img = Image.open(path_files+file)
    draw = ImageDraw.Draw(img)
    draw.text((50, 350), "Región ",
    fill="black", font=font)
    draw.text((120, 350), no,
    fill="black", font=font)
    draw.text((50, 380), "--",
    fill="#04B404", font=font)
    draw.text((70, 385), "Golden 80 - 100",
    fill="black", font=font2)

    draw.text((50, 390), "--",
    fill="#5FB404", font=font)
    draw.text((70, 395), "Golden 60 - 80",
    fill="black", font=font2)

    draw.text((50, 400), "--",
    fill="#FFFF00", font=font)
    draw.text((70, 405), "Golden 40 - 60",
    fill="black", font=font2)

    draw.text((50, 410), "--",
    fill="#FF8000", font=font)
    draw.text((70, 415), "Golden 20 - 40",
    fill="black", font=font2)

    draw.text((50, 420), "--",
    fill="#B40404", font=font)
    draw.text((70, 425), "Golden 0  - 20",
    fill="black", font=font2)

    draw.text((50, 440), "O",
    fill="black", font=font)
    draw.text((70, 445), "Nodes: 25px per node",
    fill="black", font=font2)

    img.save(path_files+file)
    # img.show()
print(f"\nTotal: {len(files)} Archivos")
