# facepixellate
Detect and pixellate faces in the picture, with varying pixel size 

![](https://github.com/tomtillo/facepixellate/blob/master/Screenshot%20from%202019-09-26%2019-45-30.png)
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