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
            name = obj.find('name').text
            data_pre = [name, x0, y0, x1, y1]
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

    def add_pic_attr(self, name, xmin, ymin, xmax, ymax):
        object = etree.SubElement(self.root, "object")
        namen = etree.SubElement(object, "name")
        namen.text = name
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
