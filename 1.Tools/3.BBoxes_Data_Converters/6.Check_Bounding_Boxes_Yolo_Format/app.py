import glob
import os
import cv2


IMG_DIR = "E:\\3.Research\\research\\13.YoloV7\yolov7\coco_fire_smoke_included_split\Out_Split_Imgs"
TXT_DIR = "E:\\3.Research\\research\\13.YoloV7\yolov7\coco_fire_smoke_included_split\Out_Split_Gts"
GT_MODE = True


imgPaths = glob.glob(os.path.join(IMG_DIR, "*"))
for imgPath in imgPaths:
    print(imgPath)
    img = cv2.imread(imgPath)

    gtPath = imgPath.replace(IMG_DIR, TXT_DIR).replace(".jpg", ".txt").replace(".jpeg", ".txt").replace(".png", ".txt")
    gt = open(gtPath, 'r')
    lines = gt.readlines()

    if lines:
        for line in lines:
            # print(line, end="")
            box = line.strip().split(" ")
            # Cls, cx, cy, w, h
            box = list(map(float, box))

            if GT_MODE:
                x0 = int((box[1] - box[3]/2) * img.shape[1])
                y0 = int((box[2] - box[4]/2) * img.shape[0])
                x1 = int((box[1] + box[3]/2) * img.shape[1])
                y1 = int((box[2] + box[4]/2) * img.shape[0])
            else:
                x0 = int((box[2] - box[4]/2) * img.shape[1])
                y0 = int((box[3] - box[5]/2) * img.shape[0])
                x1 = int((box[2] + box[4]/2) * img.shape[1])
                y1 = int((box[3] + box[5]/2) * img.shape[0])

            img = cv2.rectangle(img, (x0,y0), (x1,y1), (255,0,0), 2)

            img = cv2.putText(img, str(int(box[0])), (x0+10,y0+10), 1, 1, (0,0,255), 1, cv2.LINE_AA)



        cv2.imshow("Image", img)
        k = cv2.waitKey(0)
        if k == 27:
            exit()



