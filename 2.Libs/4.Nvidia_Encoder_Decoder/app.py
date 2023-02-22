import cv2
from nvjpeg import NvJpeg
import time 
import numpy as np

nj = NvJpeg()

img = cv2.imread("test.jpg")
jpeg_bytes = cv2.imencode(".jpg", img)[1]

while True:
    startTime = time.time()

    # Read nvjpeg (faster x2 times)
    # img = nj.read("test.jpg")
    # Read opencv
    # img = cv2.imread("test.jpg")

    # Write nvjpeg (x3 times)
    nj.write("out_nj_test.jpg", img, 1000)
    # Write opencv
    cv2.imwrite("out_cv2_test.jpg", img)
    # exit()

    # Encode nvjpeg (faster x3 times)
    jpeg_bytes = nj.encode(img)
    print(jpeg_bytes)
    exit()
    # Encode opencv
    # jpeg_bytes = cv2.imencode(".jpg", img)

    # Decode nvjpeg (faster x2 times)
    # img = nj.decode(jpeg_bytes)
    # Decode opencv
    # Method 1 opencv
    # img = cv2.imdecode(jpeg_bytes, cv2.IMREAD_UNCHANGED)
    # Method 2 opencv
    # data = np.frombuffer(jpeg_bytes, dtype=np.uint8)
    # img = cv2.imdecode(data, cv2.IMREAD_UNCHANGED)

    print(time.time() - startTime)
    


