import datetime
import time

import cv2
import matplotlib.pyplot as plt
import numpy as np
import statistics
import os

def send():
    os.system(f"curl http://127.0.0.1:5040/new_image")

def update_heatmap(bounding_boxes, heatmap):
    for box in bounding_boxes:
        x, y, w, h = box
        midpoint = (x + w//2, y + h//2)
        heatmap[midpoint[1], midpoint[0]] += 1

def detect_and_filter_contours(binary_image):
    # Find contours in the binary image
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) < 2:
        return []
    # Calculate the aspect ratios of the contours
    aspect_ratios = [cv2.boundingRect(contour)[2:][0]/cv2.boundingRect(contour)[2:][1] for contour in contours]
    areas = [cv2.boundingRect(contour)[2:][0]*cv2.boundingRect(contour)[2:][1] for contour in contours]
    if len(aspect_ratios) < 2 or len(areas) < 2:
        return []
    # Calculate the median and standard deviation of the aspect ratios
    median_aspect_ratio = statistics.median(aspect_ratios)
    std_dev = statistics.stdev(aspect_ratios)*2
    median_area = statistics.median(areas)
    std_dev_area = statistics.stdev(areas)
    bounding_boxes = []
    for contour in contours:
        # Compute the bounding box for the contour
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / h
        area = w * h
        # Filter bounding boxes by standard deviation of median aspect ratio
        if median_aspect_ratio - std_dev <= aspect_ratio <= median_aspect_ratio + std_dev:
            if area > median_area*10:
                bounding_boxes.append((x, y, w, h))

    return bounding_boxes
def reduce_bits(frame):
    return frame / 2

def process(frame):
    dilatation_size = 2

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = reduce_bits(gray)

    #dilatation_dst = cv2.dilate(gray, element)
    #kernel = np.ones((3, 3), np.float32)
    #blur = cv2.filter2D(gray, -1, kernel)
    # Calculate the Scharr gradient
    grad_x = cv2.Scharr(gray, cv2.CV_64F, 1, 0)
    grad_y = cv2.Scharr(gray, cv2.CV_64F, 0, 1)

    # Convert back to 8 bit unsigned integers
    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)

    # Combine the two gradients with equal weight
    result = cv2.addWeighted(abs_grad_x, 0.8, abs_grad_y, 0.2, 0)
    _,binary_image = cv2.threshold(result, 130, 255, cv2.THRESH_BINARY)

    laplacian = cv2.Laplacian(binary_image,cv2.CV_64F)
    kernel = np.ones((2, 2), np.float32)*32
    blur = cv2.filter2D(laplacian, -1, kernel)
    #sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 1, ksize=5)
    return binary_image


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Unable to read camera feed")
_init = 0
last = None
diff = None
mplist = []
medlist = []
maxx = 0
minn =  0
while True:
    ret, frame = cap.read()
    cp_frame = frame

    if ret:
        if last is not None:
            frame = process(frame)
            #last = process(last)
            #diff = cv2.absdiff(frame , last)
            contours = detect_and_filter_contours(frame)
            for cont in contours:
                x,y,w,h = cont
                cv2.rectangle(frame, (x,y),(x+w,y+h), (255,120,0))
            mplist.append(len(contours))
            if len(mplist) > 100:
                medlist.append(statistics.median(mplist[-100:]))
            if len(mplist) > 1024:
                del mplist[0]

            maxx = max(maxx, statistics.median(mplist[-100:]))
            print(minn, maxx, abs(minn-maxx))

            if abs(maxx-minn) > 8:
                cv2.imwrite(f"{int(time.time())}.jpg", cp_frame);
                send()
                minn = maxx
            #cv2.imshow('Webcam Feed', frame)

            # Press 'q' on keyboard to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        last = cp_frame
    else:
        break

# When everything done, release the VideoCapture object

plt.plot(medlist)
plt.plot(mplist)
plt.show()
cap.release()

# Close all the frames
cv2.destroyAllWindows()
