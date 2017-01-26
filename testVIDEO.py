import numpy as np
import cv2
from PIL import Image

cap = cv2.VideoCapture('11_53_41.mp4')
cap2 = cv2.VideoCapture('11_53_412.mp4')
#out = cv2.VideoWriter('output.avi', -1, 20.0, (250,610))

def ImageTransform1(frame): # Делает перспективные преобразования изображения
    pts1 = np.float32([[415,0],[605,0],[600,768],[1330,740]])
    pts2 = np.float32([[0,0],[250,0],[0,500],[250,500]])
    M = cv2.getPerspectiveTransform(pts1,pts2)
    dst = cv2.warpPerspective(frame, M,(250,500))
    return dst

def ImageTransform2(frame): # С другими координатами рабочей области
    pts1 = np.float32([[550,0],[770,0],[640,768],[1340,768]])
    pts2 = np.float32([[0,0],[250,0],[0,225],[250,225]])
    M = cv2.getPerspectiveTransform(pts1,pts2)
    dst = cv2.warpPerspective(frame, M,(250,225))
    return dst

def Segmentation(px): # Сегментация
    if (px<50):
        p = 25
    elif (px>=50 and px<100):
        p = 75
    elif (px>=100 and px<150):
        p = 125
    elif (px>=150 and px<200):
        p = 175
    else:
        p = 225
    return p

##################### Морфологическая разность
ret1, fr1 = cap.read()
ret2, fr2 = cap2.read()
TransImg1 = ImageTransform1(fr1)
TransImg2 = ImageTransform2(fr2)
TransImg11 = Image.fromarray(TransImg1).convert('L') # К формату PIL и grayscale
TransImg22 = Image.fromarray(TransImg2).convert('L')
w1, h1 = TransImg11.size
w2, h2 = TransImg11.size
TransImg111 = TransImg11.crop((0,h1-100,w1,h1))
TransImg222 = TransImg22.crop((0,0,w2,100))
TransImg111.show()
TransImg222.show()
#####################

#cv2.imshow("TransImg1", TransImg1)
#cv2.imshow("TransImg2", TransImg2)
'''
while(cap.isOpened()): # Считывает, трансформирует, сшивает, выводит
    ret1, frame1 = cap.read()
    ret2, frame2 = cap2.read()
    if ret1==0:
        break
    dst1 = ImageTransform1(frame1)
    dst2 = ImageTransform2(frame2)
    dst11 = Image.fromarray(dst1)
    dst22 = Image.fromarray(dst2)
    img = Image.new('RGB', (250, 610))
    img.paste(dst11, (0,0))
    img.paste(dst22, (0,385))
    endimg = np.array(img)
    
#   out.write(cimg)
    cv2.imshow("endimg", endimg)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
'''
cap.release()
cap2.release()
#out.release()
cv2.destroyAllWindows()
