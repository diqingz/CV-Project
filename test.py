#import facenet_pytorch
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image
import torch
import cv2

# If required, create a face detection pipeline using MTCNN:
#capture = cv2.VideoCapture(0)
#frame = capture.read()
mtcnn = MTCNN(image_size=96, margin=10)

# Create an inception resnet (in eval mode):
resnet = InceptionResnetV1(pretrained='vggface2').eval()
resnet.last_bn = torch.nn.Identity() #take away last 2 layers
resnet.logits = torch.nn.Identity()


img = Image.open(r'C:\Users\rohan\Documents\Honors Lab\CV project\sean.jpg')
img2 = Image.open(r'C:\Users\rohan\Documents\Honors Lab\CV project\download2.jpeg')

# Get cropped and prewhitened image tensor
img_cropped = mtcnn(img, save_path=r'C:\Users\rohan\Documents\Honors Lab\CV project\sean.jpg')
img2_cropped = mtcnn(img2, save_path=r'C:\Users\rohan\Documents\Honors Lab\CV project\test2.jpg')
#img2_cropped = torch.flip(img2_cropped, [2])
# Calculate embedding (unsqueeze to add batch dimension)
img_embedding = resnet(img_cropped.unsqueeze(0))
img2_embedding = resnet(img2_cropped.unsqueeze(0)) 
print(torch.cdist(img_embedding, img2_embedding, 1)) # b 512
dist = (img_embedding - img2_embedding).pow(3).sum(1).sqrt()
#print(dist)
# Or, if using for VGGFace2 classification
resnet.classify = True
img_probs = resnet(img_cropped.unsqueeze(0))

model = InceptionResnetV1(pretrained='vggface2').eval()















