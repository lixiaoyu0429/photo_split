from datetime import datetime

from PIL import Image
import os

from tqdm import trange


def merge_images(folder1, folder2):
    # 获取文件夹中的文件列表
    files1 = os.listdir(folder1)
    files2 = os.listdir(folder2)

    now = datetime.now()
    time_string = now.strftime("%Y%m%d_%H%M%S")
    output_folder = os.path.abspath(os.path.join(os.getcwd(), 'CMP_IMG_Merging', time_string[2:]))
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    print(output_folder)

    # 确保文件夹1和文件夹2中的文件数目相同
    if len(files1) != len(files2):
        print("文件数目不匹配")
        return
    # 遍历文件列表
    for i in trange(len(files1)):
        # 构建文件路径
        file1 = os.path.join(folder1, files1[i])
        file2 = os.path.join(folder2, files2[i])
        # 打开两张图片
        image1 = Image.open(file1)
        image2 = Image.open(file2)
        # 创建新图片，将两张图片左右拼接
        new_image = Image.new('RGB', (image1.width * 2, image1.height))
        new_image.paste(image1, (0, 0))
        new_image.paste(image2, (image1.width, 0))
        # 保存合并后的图片
        output_filename = os.path.basename(file1)
        output_path = os.path.join(output_folder, output_filename)
        new_image.save(output_path)
        # 关闭当前打开的图片
        image1.close()
        image2.close()
        # print(i)
    print("图片合并完成！")

if __name__ == '__main__':
    merge_images(r"D:\learn\photo_split\230717_105739\merged\photo_merged", r"D:\learn\photo_split\XmlDrawRect\230717_110044")
