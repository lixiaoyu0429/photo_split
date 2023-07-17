from PIL import Image
import os
from datetime import datetime
import utils.xml_open_save


# 切割图片
def Image_with_Labels_Split(folder_path, Have_Labels, n, m, overlap):
    image_path = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            image_path.append(file_path)
    # 保存路径
    folde_path = os.path.abspath(os.path.join(os.getcwd()))
    now = datetime.now()
    time_string = now.strftime("%Y%m%d_%H%M%S")
    save_path = folde_path + '\\' + time_string[2:]
    os.makedirs(os.path.join(save_path, 'photo_split'))
    if Have_Labels == True:
        os.makedirs(os.path.join(save_path, 'xml_split'))
    print(save_path)
    images_split_data = []
    # image_path下有k张图片
    for k in range(len(image_path)):
        original_image = Image.open(image_path[k])
        width, height = original_image.size
        sub_width = width // n
        sub_height = height // m
        count = 1
        # 横向分割为n张，纵向分割为m张
        for j in range(m):
            for i in range(n):
                left = i * sub_width - overlap
                upper = j * sub_height - overlap
                right = left + sub_width + 2 * overlap
                lower = upper + sub_height + 2 * overlap
                if (i == 0):
                    left = 0
                if (j == 0):
                    upper = 0
                if (i == n - 1):
                    right = width
                if (j == m - 1):
                    lower = height
                # 分割
                sub_image = original_image.crop((left, upper, right, lower))
                # 保存文件路径
                save_path_small = os.path.basename(image_path[k])
                save_path_small = save_path_small[:-4]
                # print(save_path_small)
                count_str = '{:05d}'.format(count)
                image_small_filename = save_path_small + '_' + count_str + ".jpg"
                sub_image.save(save_path + '\\' + 'photo_split' + '\\' + image_small_filename)
                # 暂存切割后的图片再原图片中的坐标
                image_small_split_data = [image_small_filename, left, upper, right, lower]
                if Have_Labels == True:
                    # 打开对应的xml文件
                    xml_path = os.path.abspath(os.path.join(os.getcwd(), 'xmls',
                                                            os.path.splitext(os.path.basename(image_path[k]))[
                                                                0] + '.xml'))
                    anno = utils.xml_open_save.Get_Annotations(xml_path)
                    data = anno.get_data_object()
                    dep_data = anno.get_data_depth()

                    # 创建新的xml文件
                    anno_new = utils.xml_open_save.GEN_Annotations(image_small_split_data[0])
                    anno_new.set_size(image_small_split_data[3] - image_small_split_data[1],
                                      image_small_split_data[4] - image_small_split_data[2], dep_data)
                    flag = 0
                    for split in data:
                        overlap_data = Iscoincide(split, image_small_split_data[1:])
                        if overlap_data != False:
                            anno_new.add_pic_attr(overlap_data[0], overlap_data[1], overlap_data[2], overlap_data[3])
                            flag += 1
                    if flag != 0:
                        newxml_path = os.path.join(save_path, 'xml_split', image_small_split_data[0][:-4] + '.xml')
                        anno_new.savefile(newxml_path)

                images_split_data.append(image_small_split_data)
                # print(image_small_filename)
                count += 1
    print("ok")
    print(images_split_data)
    return images_split_data


# 图片文件分组
def group_files(path):
    files = os.listdir(path)
    groups = {}
    for filename in files:
        filepath = os.path.join(path, filename)
        if os.path.isfile(filepath):
            basename = os.path.basename(filename)
            index = basename.rfind('_')
            if index != -1:
                group_key = basename[:index]
                if group_key in groups:
                    groups[group_key].append(basename)
                else:
                    groups[group_key] = [basename]
    return groups


# 组合图片
def Images_without_Labels_Merge(folder_path, Have_Labels, n, m, overlap):
    folde_path = os.path.join(folder_path, 'photo_split')
    # 将图片根据原图片分组
    group = group_files(folde_path)
    # 每一组为一个原图片，遍历每一组
    for tag in group:
        value = group[tag]
        image_paths = value
        # 获取第一张图片的长宽计算原图片的长宽
        open_img = os.path.join(folde_path, image_paths[0])
        first_image = Image.open(open_img)
        sub_width, sub_height = first_image.size
        sub_width -= overlap
        sub_height -= overlap
        width = sub_width * n
        height = sub_height * m
        merged_image = Image.new("RGB", (width, height))
        count = 0
        # 重新组合
        LabelSite_in_pri = []  # 存放原图片tag中的标签框
        Pri_depth = 0  # 存放原图片的深度
        for j in range(m):
            for i in range(n):
                # 计算图片在大图片中的位置
                left = i * sub_width
                upper = j * sub_height
                right = left + sub_width
                lower = upper + sub_height
                # 打开图片
                open_img_pre = os.path.join(folde_path, image_paths[count])
                sub_image = Image.open(open_img_pre)
                # 计算边框并裁减掉
                left_img = overlap
                upper_img = overlap
                if (i == 0):
                    left_img = 0
                if (j == 0):
                    upper_img = 0;
                right_img = left_img + sub_width
                lower_img = upper_img + sub_height
                sub_image1 = sub_image.crop((left_img, upper_img, right_img, lower_img))
                # 将切割图片的标签映射到原图片上
                if Have_Labels == True:
                    pri_xml_path = os.path.join(folder_path, 'xml_split', image_paths[count][:-4] + '.xml')
                    if os.path.exists(pri_xml_path):
                        # 计算带边框的图片在原图片上的位置
                        right_ = right + overlap
                        lower_ = lower + overlap
                        if (i == n - 1):
                            right_ = width
                        if (j == m - 1):
                            lower_ = height
                        pri_img_site = [left - left_img, upper - upper_img, right_, lower_]
                        # 读取小图片的xml文件
                        smallimg_xml = utils.xml_open_save.Get_Annotations(pri_xml_path)
                        smallimg_xml_data = smallimg_xml.get_data_object()
                        Pri_depth = smallimg_xml.get_data_depth()
                        # 计算每个标签框在原图片的位置
                        for per in smallimg_xml_data:
                            LabelSite_in_pri_per = [per[0] + pri_img_site[0], per[1] + pri_img_site[1],
                                                    per[2] + pri_img_site[0], per[3] + pri_img_site[1]]
                            LabelSite_in_pri.append(LabelSite_in_pri_per)

                # 将裁剪掉边框的图片粘贴到大图片上
                merged_image.paste(sub_image1, (left, upper))
                count += 1

        # 保存大图片
        save_path_pre = tag + '.jpg'
        save_path = os.path.join(folder_path, 'merged', 'photo_merged')
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        save_path = os.path.join(save_path, save_path_pre)
        merged_image.save(save_path)
        # 保存重新生成的xml
        if Have_Labels == True:
            savexml_path_pre = tag + '.xml'
            savexml_path = os.path.join(folder_path, 'merged', 'xml_merged')
            if not os.path.exists(savexml_path):
                os.makedirs(savexml_path)
            savexml_path = os.path.join(savexml_path, savexml_path_pre)
            savexml = utils.xml_open_save.GEN_Annotations(save_path_pre)
            savexml.set_size(width, height, Pri_depth)
            for per in LabelSite_in_pri:
                savexml.add_pic_attr(per[0], per[1], per[2], per[3])
            savexml.savefile(savexml_path)

    print("ok")
    return merged_image


def Iscoincide(original_data, new_data):
    # 判断是否原图中的框和切割后的图片是否重合
    if not (original_data[0] >= new_data[2] or new_data[0] >= original_data[2] or new_data[1] >= original_data[3] or
            original_data[1] >= new_data[3]):
        # 在原图片中框的左上角和右下角坐标
        overlap_data = [max(original_data[0], new_data[0]), max(original_data[1], new_data[1]),
                        min(original_data[2], new_data[2]), min(original_data[3], new_data[3])]
        # 在新图片中框的坐标
        overlap_data = [overlap_data[0] - new_data[0], overlap_data[1] - new_data[1], overlap_data[2] - new_data[0],
                        overlap_data[3] - new_data[1]]
        return overlap_data
    else:
        return False


def api(method, src_dir, Have_Labels, level, vertical, overlap):
    if method.__name__ in globals():
        dst_dir = globals()[method.__name__](src_dir, Have_Labels, level, vertical, overlap)
    else:
        raise ValueError(f"Function '{method.__name__}' not found in globals().")


if __name__ == "__main__":
    api(Image_with_Labels_Split, 'D:\learn\photo_split\photo', False, 9, 7, 10)
    # api(Images_without_Labels_Merge, '230705_170617', True, 3, 3, 10)
