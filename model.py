#import facenet_pytorch
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image
import numpy
import torch
import cv2
import matplotlib.pyplot as plt
#from scipy import ndimage, misc
import os
import serial
import time
arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)

# python function to write data to the arduino through the serial


def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.5)
    return arduino.read(6)


resnet = InceptionResnetV1(pretrained='vggface2').eval()
resnet.last_bn = torch.nn.Identity()  # take away last 2 layers
resnet.logits = torch.nn.Identity()

resnet.classify = True

# If required, create a face detection pipeline using MTCNN:
capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
detector = MTCNN(image_size=96, margin=10)
count = 0

while capture.isOpened():
    ret, frame = capture.read()
  #   cv2.imshow('window-name', frame)
    x = 0
    result = detector.detect(frame)
    #img = numpy.array(result)
    coords, conf = result
    if coords is None:
        continue
    x1, y1, x2, y2 = [int(x) for x in coords[0]]
    #print(x1, y1, x2, y2)

    cv2.imshow('frame', frame[y1:y2, x1:x2])
    # cv2.imwrite("frame%d.jpg" % count, frame)
    count = count + 1
   # print(result)
    if (conf.any() > .98):

        outPath = r"C:\Users\rohan\Documents\Honors Lab\CV project\res"
        path = r"C:\Users\rohan\Documents\Honors Lab\CV project\images"
        img_embedding = result
    # iterate through the names of contents of the folder

        data = []
        paths = []
        for image in os.listdir(path):
            with Image.open(image) as im:

                img_cropped = detector(
                    im, save_path=r'C:\Users\rohan\Documents\Honors Lab\CV project\res\test.jpg')
                img_embedding = resnet(img_cropped.unsqueeze(0))

                img2 = frame[y1:y2, x1:x2]
                img2 = torch.from_numpy(img2).permute(
                    [2, 0, 1]).unsqueeze(0).float()
                img2_embedding = resnet(img2)
                dist = torch.cdist(img_embedding, img2_embedding, 1)
                data.append(dist)
                paths.append(image)

                dist = torch.cdist(img_embedding, img2_embedding, 1)
               # print(dist)
        closest_path = paths[torch.argmin(torch.tensor(data))]
        print(closest_path)
        val = torch.tensor([dist])
        num = val.item()
        # print(num)
        if (dist < 900):
            num = input("Enter your password: ")  # Taking input from user
            print(write_read(num))  # printing the value
        exit(0)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
model = InceptionResnetV1(pretrained='vggface2').eval()
cv2.destroyAllWindows()
