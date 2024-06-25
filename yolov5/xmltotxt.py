import xml.etree.ElementTree as ET
import os

# 根據需要修改這裡的分類名稱對應到類別ID
class_mapping = {
    'licence': 0,
    # 添加更多類別
}

def convert_xml_to_txt(file_list):
    for i in file_list:
        file_name = i.split(".")[0]
        try:
            xml_file=open('/Users/chickensoup/vscode/license_plate/val_xml/%s.xml'%(file_name),encoding='UTF-8')
        except:
            print(file_name)
            continue
        tree = ET.parse(xml_file)
        root = tree.getroot()
        # 獲取圖片的寬度和高度
        size = root.find('size')
        width = int(size.find('width').text)
        height = int(size.find('height').text)

        with open('/Users/chickensoup/vscode/license_plate/val_txt/%s.txt'%(file_name),'w') as f:
            for obj in root.findall('object'):
                class_name = obj.find('name').text
                class_id = class_mapping[class_name]

                bndbox = obj.find('bndbox')
                xmin = int(bndbox.find('xmin').text)
                ymin = int(bndbox.find('ymin').text)
                xmax = int(bndbox.find('xmax').text)
                ymax = int(bndbox.find('ymax').text)

                # 轉換為YOLO格式
                x_center = (xmin + xmax) / 2.0 / width
                y_center = (ymin + ymax) / 2.0 / height
                bbox_width = (xmax - xmin) / width
                bbox_height = (ymax - ymin) / height

                f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {bbox_width:.6f} {bbox_height:.6f}\n")

# 調用函數進行轉換
file_list = os.listdir("/Users/chickensoup/vscode/license_plate/val_xml")
file_list = [i for i in file_list if i]
convert_xml_to_txt(file_list)
