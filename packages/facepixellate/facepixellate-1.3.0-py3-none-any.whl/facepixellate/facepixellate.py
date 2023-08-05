import cv2

def findFace_SaveImage(img):
    face_xml_location = "./haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(face_xml_location)
    face_coordinates=[]
    try:
        #img = cv2.imread(image_file_name)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Image properties
        #Face detection
        face_coordinates = face_cascade.detectMultiScale(gray, 1.3, 5)

    except Exception as e:
        print("Error " + str(e))
    return face_coordinates

# ---------------------------------------------------------------- pixellate

def pixellate_face_box(img, pixel_size):
    if pixel_size < 2 : 
        pixel_size = 25
    h,w,ch=img.shape
    img_shrunk = cv2.resize(img,(int(w/pixel_size),int(h/pixel_size)),interpolation=cv2.INTER_NEAREST)
    img_enlarge = cv2.resize(img_shrunk,(w,h),interpolation=cv2.INTER_NEAREST)
    return img_enlarge

# ---------------------------------------------------------------- pixellate

def pixellate_face(img_path,pixel_size) : 
    """
     Takes in image path and returns a image array which is pixellated.
     Argument Input : image path, pixel size 
     Return : Image object
    """
    orig_img = cv2.imread(img_path)
    faces_coordinates_array= findFace_SaveImage(orig_img)

    for x,y,w,h in faces_coordinates_array:
        #cv2.rectangle(img, (x, y), (x + w, y + h), (88, 252, 244), 5)
        face_box= orig_img[y:y + h, x:x + w]
        imp_pix = pixellate_face_box(face_box,pixel_size)
        orig_img[y:y + h, x:x + w] = imp_pix
    
    return orig_img

# ---------------------------------------------------------------- End of functions
