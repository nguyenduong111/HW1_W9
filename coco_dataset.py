from pycocotools.coco import COCO
import random
import urllib.request
import os
# save dir
DATA_ROOT = r"D:\AI\AI_Thay_Cuong\data_test"
NUM = 300
# Đường dẫn đến tệp annotations của tập coco
dataDir=r'D:\AI\AI_Thay_Cuong'
dataType='val2017'
annFile='{}/annotations/instances_{}.json'.format(dataDir,dataType)

def makeDir(dir):
    if not os.path.isdir(dir):
        os.mkdir(dir)
    return dir
def getLabelData(annotations, image_id, size):
    width, height = size
    print(size)
    result = ["{} {} {} {} {}\n".format(
        item['category_id'], 
        (item['bbox'][0]+item['bbox'][2]/2)/width, 
        (item['bbox'][1]+item['bbox'][3]/2)/height, 
        item['bbox'][2]/width, 
        item['bbox'][3]/height) 
        for item in annotations if item['image_id'] == image_id]
    return "".join(result)

imgs_dir = makeDir(DATA_ROOT + "\\images")
lables_dir = makeDir(DATA_ROOT + "\\labels")
# Tạo một đối tượng COCO để làm việc với tập dữ liệu
coco=COCO(annFile)

# Lấy danh sách các hình ảnh chứa người
catIds = coco.getCatIds(catNms=['person'])
imgIds = coco.getImgIds(catIds=catIds)
if len(imgIds)> NUM:
    imgIds = imgIds[:NUM]

annIds = coco.getAnnIds(imgIds=imgIds, catIds=catIds, iscrowd=None)
annotations = coco.loadAnns(annIds)


# # Save images
for inx, imgId in enumerate(imgIds):
    # Image
    img = coco.loadImgs(imgId)[0]
    img_name = img['coco_url'].split("/")[-1]
    urllib.request.urlretrieve(img['coco_url'], f"{imgs_dir}\\{img_name}")

    # label
    label_data = getLabelData(annotations, img['id'], (img['width'], img['height']))
    f = open(lables_dir + "\\" + img_name.split(".")[0] + ".txt", "w")
    f.write(label_data)
    f.close()
    
    print(f"Saved {inx+1}")



# Tải hình ảnh từ URL và hiển thị


