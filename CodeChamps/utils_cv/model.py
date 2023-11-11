import cv2
from PIL import Image
from ultralytics import YOLO
from CodeChamps.utils_cv.args import PATH_TO_MODEL1, PATH_TO_SAVE_PREDICTIONS, PATH_TO_MODEL2
import torch
from torchvision import ops
from CodeChamps.utils_cv.utils import *

#Загрузка моделей
best_model = YOLO(PATH_TO_MODEL1)
brave_model = YOLO(PATH_TO_MODEL2)
#model= YOLO("D:\\Projects\\Projects_Python\\hacks\\detect street traiders\\utils_cv\\best (14).pt")

#минимальная уверенность модели для детекции
MIN_BORDER_BEST_MODEL=0.3#0.45
MIN_BORDER_MODEL_1=0.3

#минимальный процент пересечения боксов для предиктов разных моделей для прохожденя проверки
IOU_COEF=0.75

#Минимальная уверенность модели для перманетнгого прохождения проверки
MIN_PERM_BORDER=0.85

#проверять каждый n кадр видео
CHECK_EVERY=100

#посчитать процент пересечения боксов для моделей
def check_IOU(box1,box2):
  box1=torch.tensor([box1.tolist()], dtype=torch.float)
  box2=torch.tensor([box2.tolist()], dtype=torch.float)
  iou = ops.box_iou(box1, box2)
  return iou.numpy()[0][0]

#ансаблирование моделей
def get_ansamble_predict(result1,result2):
  new_result=[]
  for r1, r2 in zip(result1,result2):
    for idx_box1 in range(len(r1.boxes.xyxy)):
      for idx_box2 in range(len(r2.boxes.xyxy)):

        box1=r1.boxes.xyxy[idx_box1]
        box2=r2.boxes.xyxy[idx_box2]

        conf1=r1.boxes.conf[idx_box1]
        conf2=r2.boxes.conf[idx_box2]

        IOU=check_IOU(box1,box2)
        if ((IOU>IOU_COEF) and ((conf1*conf2)>0.52)) or (conf1>MIN_PERM_BORDER) or (conf2>0.7):
          print('coefs------------------------------------')
          print(conf1,conf2)
          print(conf1*conf2)
          new_result.append(box1)
          continue

  return new_result




def analise_video2(path):
  create_data_dir(PATH_TO_SAVE_PREDICTIONS)

  cap = cv2.VideoCapture(path)
  
  # проверяем запустилось ли видео
  if (cap.isOpened()== False): 
    print("Error opening video stream or file")

  #берем количество кадров в видео
  frame_count = cap.get(7)
  print('Frame count : ', frame_count)
  for count in range(int(frame_count)):
    ret, frame = cap.read()
    if (count%CHECK_EVERY)==0:
      #ret, frame = cap.read()
      if ret == True:

        #дететим объекты
        print(f"--------------- IMAGE = {count} -------------------")
        results1 = best_model.predict(frame, agnostic_nms=True,conf=MIN_BORDER_BEST_MODEL)#,save=True)
        results2 = brave_model.predict(frame, agnostic_nms=True,conf=MIN_BORDER_MODEL_1)#,save=True)
        results=get_ansamble_predict(results1,results2)



        #выделяем боксы на фотке
        for box in results:
          frame = cv2.rectangle(frame, (int(box[0]),int(box[1])), (int(box[2]),int(box[3])),color = (0, 0, 255),thickness=10) 

        #если был обнаружен объект
        if len(results)!=0:
          #записываем результаты выделения в labels
          save_results_to_txt(results,count)
          #сохраняем фотку
          cv2.imwrite(f'{PATH_TO_SAVE_PREDICTIONS}/images/{count}.jpg', frame)
  cap.release()





def analise_stream(path):
  cap = cv2.VideoCapture(path)
  
  # Check if camera opened successfully
  if (cap.isOpened()== False): 
    print("Error opening video stream or file")

  #берем количество кадров в видео
  count=-1
  while True:
    count+=1
    ret, frame = cap.read()
    if (count%CHECK_EVERY)==0:
      #ret, frame = cap.read()
      if ret == True:

        #дететим объекты
        print(f"--------------- IMAGE = {count} -------------------")
        results1 = best_model.predict(frame, agnostic_nms=True,conf=MIN_BORDER_BEST_MODEL,save=True)
        results2 = brave_model.predict(frame, agnostic_nms=True,conf=MIN_BORDER_MODEL_1)#,save=True)
        results=get_ansamble_predict(results1,results2)

        
        

        #выделяем боксы на фотке
        for box in results:
          frame = cv2.rectangle(frame, (int(box[0]),int(box[1])), (int(box[2]),int(box[3])),color = (0, 0, 255),thickness=10) 

        #если был обнаружен объект
        if len(results)!=0:
          #записываем результаты выделения в labels
          save_results_to_txt(results,count)
          #сохраняем фотку
          cv2.imwrite(f'{PATH_TO_SAVE_PREDICTIONS}/images/{count}.jpg', frame)


        #cv2.imshow(',',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
          break

  cap.release()

  cv2.destroyAllWindows()

