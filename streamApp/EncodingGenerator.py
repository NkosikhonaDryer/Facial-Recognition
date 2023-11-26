import cv2
import face_recognition
import pickle
import os



def findEncodings():
    #images = 'stramApp/images'
    print("Starting codings")
    images = 'media/streamApp/images'
    imagesPathList = os.listdir(images)

    imagesList =[]
    imageIdList = []

    
    for path in imagesPathList:
        imagesList.append(cv2.imread(os.path.join(images, path)))
        print("path: ",path)
        
        imageIdList.append(os.path.splitext(path)[0])
        
    
    encodingsList = []
    num =0
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]  
     
        num += 1
        encodingsList.append(encode)
    encodeListKnown = encodingsList
    encdogindWithImageIds = [encodeListKnown,imageIdList]
    file = open("encdogindWithImageIds.p","wb")
    pickle.dump(encdogindWithImageIds,file)
    file.close()
    print()
    print("coding end!")
    return encodingsList

print(findEncodings())

