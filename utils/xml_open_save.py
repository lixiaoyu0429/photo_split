from xml.etree import ElementTree as etree
import xml.dom.minidom


def remove_first_line(text):
    lines = text.split('\n', 1)
    if len(lines) > 1:
        return lines[1]
    else:
        return ''


def add_tab_to_lines(text):
    lines = text.splitlines()
    modified_lines = [lines[0]] + ['\t' + line for line in lines[1:]]
    return '\n'.join(modified_lines)


class Get_Annotations:
    def __init__(self, filepath):
        self.root = etree.parse(filepath).getroot()

    def get_data_object(self):
        data = []
        for obj in self.root.iter('object'):
            x0 = int(obj.find('bndbox/xmin').text)
            y0 = int(obj.find('bndbox/ymin').text)
            x1 = int(obj.find('bndbox/xmax').text)
            y1 = int(obj.find('bndbox/ymax').text)
            data_pre = [x0, y0, x1, y1]
            data.append(data_pre)
        return data
    def get_data_depth(self):
        for dep in self.root.iter('size'):
            dep_data = int(dep.find('depth').text)
        return dep_data


class GEN_Annotations:
    def __init__(self, filename=None):
        self.root = etree.Element("annotation")

        child1 = etree.SubElement(self.root, "folder")
        child1.text = "driving_annotation_dataset"

        child2 = etree.SubElement(self.root, "filename")
        child2.text = filename

    def set_size(self, witdh, height, channel):
        size = etree.SubElement(self.root, "size")
        widthn = etree.SubElement(size, "width")
        widthn.text = str(witdh)
        heightn = etree.SubElement(size, "height")
        heightn.text = str(height)
        channeln = etree.SubElement(size, "depth")
        channeln.text = str(channel)

    def savefile(self, filepath):
        tree = etree.ElementTree(self.root)
        xml_string = etree.tostring(self.root, encoding="utf-8")
        dom = xml.dom.minidom.parseString(xml_string)
        # print(xml_string)
        declaration = dom.createProcessingInstruction("xml", 'version="1.0" encoding="utf-8"')
        dom.insertBefore(declaration, dom.firstChild)
        xml_formatted = dom.toprettyxml(indent="\t")
        xml_formatted = remove_first_line(xml_formatted)
        xml_formatted = add_tab_to_lines(xml_formatted)
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(xml_formatted)

    def add_pic_attr(self, xmin, ymin, xmax, ymax):
        object = etree.SubElement(self.root, "object")
        namen = etree.SubElement(object, "name")
        namen.text = 'propy'
        namen = etree.SubElement(object, "pose")
        namen.text = 'Unspecified'
        namen = etree.SubElement(object, "truncated")
        namen.text = '0'
        namen = etree.SubElement(object, "difficult")
        namen.text = '0'
        bndbox = etree.SubElement(object, "bndbox")
        xminn = etree.SubElement(bndbox, "xmin")
        xminn.text = str(xmin)
        yminn = etree.SubElement(bndbox, "ymin")
        yminn.text = str(ymin)
        xmaxn = etree.SubElement(bndbox, "xmax")
        xmaxn.text = str(xmax)
        ymaxn = etree.SubElement(bndbox, "ymax")
        ymaxn.text = str(ymax)


# class Append_Annotations:
#     def __init__(self, append_xml_path):
#         self.root = etree.parse(append_xml_path).getroot()
#         self.append_xml_path = append_xml_path
#
#     def append_pic_attr(self, xmin, ymin, xmax, ymax):
#         xml_string = etree.tostring(self.root, encoding="utf-8")
#         # print(type(xml_string))
#         # print(xml_string)
#         string_to_add = '\n\t\t<object>\n\t\t\t<name>propy</name>\n\t\t\t<pose>Unspecified</pose>\n\t\t\t<truncated>0</truncated>\n\t\t\t<difficult>0</difficult>'
#         string_to_add = string_to_add + "\n\t\t\t<bndbox>\n\t\t\t\t<xmin>" + str(xmin) + "</xmin>"
#         string_to_add = string_to_add + "\n\t\t\t\t<ymin>" + str(ymin) + "</ymin>"
#         string_to_add = string_to_add + "\n\t\t\t\t<xmax>" + str(xmax) + "</xmax>"
#         string_to_add = string_to_add + "\n\t\t\t\t<ymax>" + str(ymax) + "</ymax>"
#         string_to_add = string_to_add + "\n\t\t\t</bndbox>\n\t\t</object>"
#
#         dom = xml.dom.minidom.parseString(xml_string)
#         xml_formatted = dom.toprettyxml(indent="", newl= '')
#         # print(type(xml_formatted))
#         # print(xml_formatted)
#
#         # lines = text.split('\n')  # 将文本拆分成行列表
#         # penultimate_line_index = -2  # 倒数第二行的索引
#         # lines.insert(penultimate_line_index, string_to_add)  # 在索引处插入字符串
#         # updated_text = '\n'.join(lines)  # 将行列表重新组合成文本
#
#
#
# # def savefile(self):
# #     # 将 XML 结构转换为字符串
# #     xml_string = etree.tostring(self.root, encoding="utf-8")
# # 将字符串写入文件
# # print(type(xml_string))
# # print(xml_string)
# # dom = xml.dom.minidom.parseString(xml_string)
# # xml_formatted = dom.toprettyxml(indent="\t", newl= '')
# # print(type(xml_formatted))
# # print(xml_formatted)
#
# # with open(self.append_xml_path, "w", encoding="utf-8") as file:
# #     file.write(xml_string)


if __name__ == '__main__':
    # filename = "000001.jpg"
    # anno = GEN_Annotations(filename)
    # anno.set_size(1280, 720, 3)
    # for i in range(3):
    #     xmin = i + 1
    #     ymin = i + 10
    #     xmax = i + 100
    #     ymax = i + 100
    #     anno.add_pic_attr(xmin, ymin, xmax, ymax)
    # anno.savefile("00001.xml")
    anno = Get_Annotations("D:\learn\photo_split\example.xml")
    data = anno.get_data_depth()
    print(data)
    # anno = Append_Annotations(r'D:\learn\photo_split\430482常宁市001.xml')
    # anno.append_pic_attr(0, 0, 0, 0)
    # anno.savefile()
    print(1)
