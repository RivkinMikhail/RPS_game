import cv2
import numpy as np
from PIL import Image
import torchvision
import torch.nn.functional
import torch.nn as nn
from torchvision import transforms

def extract_user_move(frame):
    # This list will be used to map probabilities to class names, Label names are in alphabetical order.
    label_names = ['nothing', 'paper', 'rock', 'scissors']
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    model = torchvision.models.mobilenet_v3_small(pretrained=True)
    num_ftrs = model.classifier[3].in_features
    model.classifier[3] = nn.Linear(num_ftrs, 4)
    model.load_state_dict(torch.load('./src/rps_recognizer_.pth'))
    model.eval()
    model.to(device)
    preprocess = transforms.Compose([
        transforms.Resize([224, 224]),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    roi = Image.fromarray(frame)
    input = preprocess(roi)
    input = input.unsqueeze(0)
    # Get model's prediction.
    input = input.to(device)
    with torch.no_grad():
        pred = model(input)
    _, index = torch.max(pred, 1)

    res = 0
    if label_names[index[0]] == 'paper':
        res = 1
    elif label_names[index[0]] == 'rock':
        res = 0
    elif label_names[index[0]] == 'scissors':
        res = 2
    else:
        res = 'nothing'
    return res
