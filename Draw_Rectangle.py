import os
from datetime import datetime

from PIL import Image, ImageDraw
from tqdm import tqdm

import utils.xml_open_save_dis


def XmlDrawRect(input_photo_path, input_xml_path, Width):
    # 获取输入
    photo_files = os.listdir(input_photo_path)
    xml_files = os.listdir(input_xml_path)
    now = datetime.now()
    time_string = now.strftime("%Y%m%d_%H%M%S")
    new_image_path = os.path.abspath(os.path.join(os.getcwd(), 'XmlDrawRect', time_string[2:]))
    if not os.path.exists(new_image_path):
        os.makedirs(new_image_path)
    print(new_image_path)
    for per_photo in tqdm(photo_files):
        files_path = os.path.join(input_photo_path, per_photo)
        rect_in_photo_object = []
        for per_xml in xml_files:
            if per_xml[:-4] == per_photo[:-4]:
                xml_path = os.path.join(input_xml_path, per_xml)
                rect_in_photo = utils.xml_open_save_dis.Get_Annotations(xml_path)
                rect_in_photo_object = rect_in_photo.get_data_object()
                break
        if len(rect_in_photo_object) != 0:
            open_image = Image.open(files_path)
            draw = ImageDraw.Draw(open_image)
            for per_rect_in_photo_object in rect_in_photo_object:
                name,x1, y1, x2, y2 = per_rect_in_photo_object
                draw.text((x1,y1-10),name)
                draw.rectangle([(x1, y1), (x2, y2)], outline="red", width=Width)

            new_image_pathandname = os.path.join(new_image_path, per_photo)
            open_image.save(new_image_pathandname)
        # print(files_path)
    print("ok")


if __name__ == '__main__':
    XmlDrawRect(r"D:\learn\photo_split\photo", r"D:\learn\photo_split\xmls", Width=10)
