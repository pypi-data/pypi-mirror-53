# facepixellate
Detect and pixellate faces in the picture, with varying pixel size 

## Environment
python 3.6
opencv

## Installation
`pip install facepixellate`

## Usage 

### 1. Inside python code - 
#### Sample code  
```
import facepixellate 
import cv2 

img_p = facepixellate.pixellate_face("test_face.jpg", 0)
cv2.imwrite("output.jpg",img_p)
```

P.S :Check homepage ( github ) for detailed description