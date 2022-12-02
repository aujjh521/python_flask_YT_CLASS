#%%
#import package
import torch
import torch.nn as nn
#from main import CNN #import model architecture from training portion (train裡面如果沒有變function會整個一起執行)
import torchvision.transforms as transforms
from PIL import Image

#%%
#define critical file path
pretrained_weight_path = './MLModelWeight/DogCatClassification/trained_model.pth'
target_img_path = 'IMG_8902.jpeg'

#%%
#load pretrained model weight
class CNN(nn.Module):
  def __init__(self):
    super(CNN, self).__init__()
    self.conv1 = nn.Sequential(         
        nn.Conv2d(
            in_channels=3,              
            out_channels=64,            
            kernel_size=3,              
            stride=1,                   
            padding=1,                  
        ),
        nn.BatchNorm2d(64),                              
        nn.ReLU(),                      
        nn.MaxPool2d(2, 2, 0),    
    )
    self.conv2 = nn.Sequential(         
        nn.Conv2d(64, 128, 3, 1, 1),  
        nn.BatchNorm2d(128),     
        nn.ReLU(),                      
        nn.MaxPool2d(2, 2, 0),                
    )

    self.conv3 = nn.Sequential(         
        nn.Conv2d(128, 256, 3, 1, 1),  
        nn.BatchNorm2d(256),     
        nn.ReLU(),                      
        nn.MaxPool2d(4, 4, 0),                
    )

    # fully connected layer, output 10 classes
    self.out = nn.Linear(256 * 8*8, 2)
  def forward(self, x):
      #print(f'1. {x.shape}')
      x = self.conv1(x)
      #print(f'2. {x.shape}')
      x = self.conv2(x)
      #print(f'3. {x.shape}')
      #print(x.shape)
      x = self.conv3(x)
      # flatten the output of conv2
      x = x.view(x.size(0), -1) 
      #print(f'4. {x.shape}')
      #print(x.shape)      
      output = self.out(x)
      #print(f'5. {x.shape}')
      return output

if __name__ == '__main__': 
    model = CNN()
    model.load_state_dict(torch.load(pretrained_weight_path,map_location=torch.device("cpu")))

    #%%
    #inference
    test_transform = transforms.Compose([transforms.Resize((128, 128)),
                        transforms.ToTensor()
                        ])

    img = Image.open(target_img_path)
    img = test_transform(img).unsqueeze(0) #增加一個維度for batch
    res = model(img)

    #把predict結果mapping回初始類別
    _, pred = torch.max(res, dim=1)
    label_encode_mapping = {1:'dog',
                0:'cat'
                }
    print(f'predict result is {label_encode_mapping[pred.numpy()[0]]}')