from datetime import datetime
from playsound import *
import tkinter as tk
import time
import numpy as np
import cv2, sys, os
from tkinter import messagebox as msg

Move_window = 0

#메세지박스
def messageBox(title, text):
    return msg.askquestion(title, text)

#촬영에 쓰이는 함수
def count(count):
    while count  > 0:
        for i in range(30):
            ret, frame = cam.read()
            frame = cv2.flip(frame, 1)
            cv2.putText(frame, str(count),(230, 300) , font, 7, (0,0,0), 3)
            cv2.imshow(title, frame)
            cv2.waitKey(30)                  
        count -= 1

def sec(num):
    global Move_window
    if num == 1:
        for i in range(30):
            ret, frame = cam.read()
            frame = cv2.flip(frame, 1)
            cv2.putText(frame, "Ready?" ,(180, 300) , font, 3, (0,0,0), 3)
            cv2.imshow(title, frame)
            if Move_window == 0:
                Move_window += 1
                cv2.moveWindow(title,430,-100)
            cv2.waitKey(30)
    else:
        for i in range(30):
            ret, frame = cam.read()
            frame = cv2.flip(frame, 1)
            cv2.imshow(title, frame)
            cv2.waitKey(30)

def PictureTake():
    global photo_list 
    sec(1)
    for i in range(4):
        count(3)
        ret,frame = cam.read()
        playsound(audio_file)
        frame = cv2.flip(frame, 1)
        photo_list.append(frame)
        sec(0)
    cv2.destroyWindow(title)
    
#트랙바
def onChange(value):
    pass

#tkinter 버튼에 쓰이는 함수
#radio button
def Func_check1():
    global Color, Gray
    if var1.get() == 1:
        Color = False
        Gray = True
    if var1.get() == 2:
        Color = True
        Gray = False
    
def Func_check2():
    global Day, textColor
    if var2.get() == 1:
        Day = True
        textColor = (255,255,255)
    elif var2.get() == 2:
        Day = True
        textColor = (0,0,0)
    elif var2.get() == 3:
        Day = False

def TorF(num):
    global frame_list
    for i in range(0,5):
        if i==num:
            frame_list[i] = True
        else:
            frame_list[i] = False

def Func_check3():
    global frame_list
    for i in range (1,6):
        if var3.get() == i:
            TorF(i-1)

#button
def Func_photoSave():
    global save_photo
    save_photo = True  

def Func_Original():
    global result_gray_photo_list, result_color_photo_list
    if Color:
        for i in range(4):
            result_color_photo_list[i] = photo_list[i]
    if Gray:
        for i in range(4):
            result_gray_photo_list[i] = photogray_list[i]

def Func_Bright():
    global result_gray_photo_list, result_color_photo_list
    if Color:
        array = np.full(result_color_photo_list[0].shape, (10,10,10),np.uint8)
        for i in range(4):
            result_color_photo_list[i] = cv2.add(result_color_photo_list[i], array)
    if Gray:
        for i in range(4):
            result_gray_photo_list[i] = cv2.add(result_gray_photo_list[i],10)

def Func_Dark():
    global result_gray_photo_list, result_color_photo_list
    if Color:
        array = np.full(result_color_photo_list[0].shape, (10,10,10),np.uint8)
        for i in range(4):
            result_color_photo_list[i] = cv2.subtract(result_color_photo_list[i], array)
    if Gray:
        for i in range(4):
            result_gray_photo_list[i] = cv2.subtract(result_gray_photo_list[i],10)

def Func_blur():
    global result_gray_photo_list,result_color_photo_list
    if Color:
        for i in range(4):
            result_color_photo_list[i] = cv2.bilateralFilter(result_color_photo_list[i],-1,5,5)
    if Gray:
        for i in range(4):
            result_gray_photo_list[i] = cv2.bilateralFilter(result_gray_photo_list[i],-1,5,5)

def Func_stretch():
    global result_gray_photo_list,result_color_photo_list
    if Color:
        for i in range(4):
            dst1 = cv2.cvtColor(result_color_photo_list[i], cv2.COLOR_BGR2YCrCb)
            y, cr, cb = cv2.split(dst1)
            dst2 = cv2.normalize(y, None, 0, 255, cv2.NORM_MINMAX)
            dst1 = cv2.merge([dst2, cr, cb])
            result_color_photo_list[i] = cv2.cvtColor(dst1, cv2.COLOR_YCrCb2BGR)
    if Gray:
        for i in range(4):
            result_gray_photo_list[i] = cv2.normalize(result_gray_photo_list[i] , None, 0, 255, cv2.NORM_MINMAX)

def Func_equal():
    global result_gray_photo_list,result_color_photo_list
    if Color:
        for i in range(4):
            dst1 = cv2.cvtColor(result_color_photo_list[i], cv2.COLOR_BGR2YCrCb)
            y, cr, cb = cv2.split(dst1)
            dst2 = cv2.equalizeHist(y)
            dst1 = cv2.merge([dst2, cr, cb])
            result_color_photo_list[i] = cv2.cvtColor(dst1, cv2.COLOR_YCrCb2BGR)
    if Gray:
        for i in range(4):
            result_gray_photo_list[i] = cv2.equalizeHist(result_gray_photo_list[i])

def Func_open():
    global result_gray_photo_list,result_color_photo_list
    if Color:
        for i in range(4):
            result_color_photo_list[i] = cv2.morphologyEx(result_color_photo_list[i], cv2.MORPH_OPEN,None)
    if Gray:
        for i in range(4):
            result_gray_photo_list[i] = cv2.morphologyEx(result_gray_photo_list[i], cv2.MORPH_OPEN,None)

def Func_close():
    global result_gray_photo_list,result_color_photo_list
    if Color:
        for i in range(4):
            result_color_photo_list[i] = cv2.morphologyEx(result_color_photo_list[i], cv2.MORPH_CLOSE,None)
    if Gray:
        for i in range(4):
            result_gray_photo_list[i] = cv2.morphologyEx(result_gray_photo_list[i], cv2.MORPH_CLOSE,None)

def Func_retake():
    global photo_list, result_color_photo_list,photogray_list,result_gray_photo_list
    photo_list.clear()
    result_color_photo_list.clear()
    photogray_list.clear()
    result_gray_photo_list.clear()
    PictureTake()
    for i in range(0,4):
        photo_list[i] = cv2.resize(photo_list[i], in_size)
        result_color_photo_list.append(photo_list[i])
        photogray_list.append(cv2.cvtColor(photo_list[i], cv2.COLOR_BGR2GRAY))
        result_gray_photo_list.append(photogray_list[i])

#프레임 선택
def frameADD():
    global Rphoto, RphotoGray
    if Gray:
        for i in range(0,5):
            if i == 0:
                if frame_list[i] == True:
                    RphotoGray[:] = gray
            elif frame_list[i] == True:
                RphotoGray[:] = 0
                RphotoGray =cv2.add(RphotoGray, frame_piclistGray[i-1])
    if Color:
        for i in range(0,5):
            if i == 0:
                if frame_list[i] == True:
                    Rphoto[:] = [b,g,r]
            elif frame_list[i] == True:
                Rphoto[:] = [0,0,0]
                Rphoto =cv2.add(Rphoto, frame_piclist[i-1])
#날짜 유무 및 색                
def dayADD():
    global RphotoGray, Rphoto
    if Day:
        if Gray:
            cv2.putText(RphotoGray, Today,(230,2250), font, 1.7, textColor, 5)
        if Color:
            cv2.putText(Rphoto, Today,(230,2250), font, 1.7, textColor, 5)

#사진 보여주기
def show():
    global Rphoto, RphotoGray
    frameADD()
    dayADD()
    if Gray:
        k=0
        for i in H_list:
            RphotoGray[i:i+h, 45:45+w] = result_gray_photo_list[k]
            k += 1
        dst = RphotoGray

    if Color:
        k=0
        for i in H_list:
            Rphoto[i:i+h, 45:45+w] = result_color_photo_list[k]
            k += 1
        dst = Rphoto

    cv2.imshow("photo", dst)

#웹캠 연결 및 촬영
cam=cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,600)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,450)
cam.set(cv2.CAP_PROP_AUTOFOCUS, 0)
if cam.isOpened() == False:
    raise Exception("connection failed")

font = cv2.FONT_HERSHEY_SIMPLEX

title = "photo shot"
photo_list = []                                 #원본 컬러 사진 리스트
result_color_photo_list = []                    #결과 컬러 사진 리스트
photogray_list = []                             #원본 흑백 사진 리스트
result_gray_photo_list = []                     #결과 흑백 사진 리스트
H_list = []                                     #사진을 붙일 높이를 저장

ans = messageBox(" ", "사진 찍을 준비 되셨나요?")
audio_file = os.path.dirname(__file__)+'/sound.mp3'

if ans == 'yes':
    PictureTake()
else:
    sys.exit()

#현재 날짜 저장
now = datetime.now()
Today = str(now.strftime('%Y.%m.%d'))
Today = Today[2::]

textColor = (255,255,255)   #텍스트 컬러 기본
in_size = (600,450)         #사진내부사이즈

#기본 배경 및 프레임 불러오기
Rphoto = np.zeros((2340,690,3),np.uint8)
RphotoGray = np.zeros((2340,690),np.uint8)
frame1 = cv2.imread('./Frame/FRAME1.jpg',cv2.IMREAD_COLOR)
frame1Gray= cv2.imread('./Frame/FRAME1.jpg',cv2.IMREAD_GRAYSCALE)
frame2 = cv2.imread('./Frame/ACME2.png',cv2.IMREAD_COLOR)
frame2Gray= cv2.imread('./Frame/ACME2.png',cv2.IMREAD_GRAYSCALE)
frame3= cv2.imread('./Frame/ZFRAME.png',cv2.IMREAD_COLOR)
frame3Gray = cv2.imread('./Frame/ZFRAME.png',cv2.IMREAD_GRAYSCALE)
frame4 = cv2.imread('./Frame/DFRAME.png',cv2.IMREAD_COLOR)
frame4Gray = cv2.imread('./Frame/DFRAME.png',cv2.IMREAD_GRAYSCALE)


frame_piclist = [frame1, frame2, frame3, frame4]
frame_piclistGray = [frame1Gray, frame2Gray, frame3Gray, frame4Gray]

(h,w) =(450,600)

for i in range(0,4):
    photo_list[i] = cv2.resize(photo_list[i], in_size)
    H_list.append(45*(i+1)+h*i)
    result_color_photo_list.append(photo_list[i])
    photogray_list.append(cv2.cvtColor(photo_list[i], cv2.COLOR_BGR2GRAY))
    result_gray_photo_list.append(photogray_list[i])

b = 0
g = 0
r = 0
gray=0

#배경 컬러 조절 트랙바
c_title = "Background color"
controller = np.zeros((1,500), np.uint8)
cv2.namedWindow(c_title)
colors = ["Blue", "Green", "Red", "Gray"]
for i in colors:
    cv2.createTrackbar(i, c_title, 0, 255, onChange)

#사진 세팅 변수
save_photo = False
Color = True
Gray = False
Day = True
ORIGIN = True
FRAME1 = False
FRAME2 = False
FRAME3 = False
FRAME4 = False
frame_list = [ORIGIN, FRAME1, FRAME2, FRAME3, FRAME4]

#사진 세팅 tkinter
window = tk.Tk()
window.title("photo setting")
var1 = tk.IntVar()
var2 = tk.IntVar()
var3 = tk.IntVar()

#재촬영 및 저장
saveButton = tk.Button(window, text = '편집 완료', command=Func_photoSave)
RetakeButton = tk.Button(window, text='재촬영', command=Func_retake)

#사진 컬러/ 흑백 버튼
grayButton = tk.Radiobutton(window, text = "흑백", value = 1, variable = var1,command = Func_check1, width= 8)
colorButton = tk.Radiobutton(window,text = "컬러", value = 2, variable = var1,command = Func_check1, width= 8)

#날짜 글씨 색
blackButton = tk.Radiobutton(window, text = '검정', value = 2, variable = var2, command = Func_check2, width= 8)
whiteButton = tk.Radiobutton(window, text = '흰색', value = 1, variable = var2, command = Func_check2, width= 8)
NoneButton = tk.Radiobutton(window, text = '날짜없음', value = 3, variable = var2, command = Func_check2, width= 8)

#프레임 선택 라디오 및 프레임 체크버튼
originalButton = tk.Radiobutton(window, text = "기본", value = 1, variable = var3,command = Func_check3, width= 8)
frame1Button = tk.Radiobutton(window, text = "에크미1", value = 2, variable = var3,command = Func_check3, width= 8)
frame2Button = tk.Radiobutton(window, text = "에크미2", value = 3, variable = var3,command = Func_check3, width= 8)
frame3Button = tk.Radiobutton(window, text = "지브리", value = 4, variable = var3,command = Func_check3, width= 8)
frame4Button = tk.Radiobutton(window, text = "디즈니", value = 5, variable = var3,command = Func_check3, width= 8)

#사진 밝기 연산
OriginButton = tk.Button(window, text='원본', command=Func_Original)
BrightButton = tk.Button(window, text='증가', command=Func_Bright)
DarkButton = tk.Button(window, text='감소', command=Func_Dark)

#사진 연산
BlurButton = tk.Button(window, text='블러', command=Func_blur)
StretchButton = tk.Button(window, text='스트레칭', command=Func_stretch)
EqualButton = tk.Button(window, text='평활화', command=Func_equal)
OpenButton = tk.Button(window, text='열림', command=Func_open)
CloseButton = tk.Button(window, text='닫힘', command=Func_close)

#텍스트
label1 = tk.Label(window, text ='▸ 사진 색상', font =("굴림",15), justify='left', width= 10)
label2 = tk.Label(window, text ='▸ 밝기 조절', font =("굴림",15), justify='left', width= 10)
label3 = tk.Label(window, text ='▸ 기타 설정', font =("굴림",15), justify='left', width= 10)
label4 = tk.Label(window, text ='▸ 날짜 색상', font =("굴림",15), justify='left', width= 10)
label5 = tk.Label(window, text ='▸ 프레임   ', font = ("굴림",15), justify='left', width= 10)

#버튼 위치 및 라벨 위치 지정
All_Button_list = [grayButton, colorButton,
                   DarkButton, OriginButton, BrightButton,
                   BlurButton, StretchButton, EqualButton, OpenButton, CloseButton,
                   whiteButton, blackButton, NoneButton, 
                   originalButton, frame1Button, frame2Button, frame3Button, frame4Button,
                   saveButton, RetakeButton,]

Button_list = [DarkButton, OriginButton, BrightButton, #어둡게, 원본, 밝게
               BlurButton, StretchButton, EqualButton, OpenButton, CloseButton, #블러, 스트레칭, 평활화, 열림, 닫힘
               saveButton,RetakeButton] # 저장, 재촬영 

for i in Button_list:
    i.config(width=5, height = 1, bg = 'white')

Location = [(2,1),(2,2),
            (4,1),(4,2),(4,3),
            (6,1),(6,2),(6,3),(6,4),(6,5),
            (8,1),(8,2),(8,3),
            (10,1),(10,2),(10,3),(10,4),(10,5),
            (11,1),(11,2)]

for (x,(y,z)) in zip(All_Button_list, Location):
    x.grid(row=y, column=z, pady=5, padx = 10)

label1.grid(row=1,column=1)
label2.grid(row=3,column=1)
label3.grid(row=5, column=1)
label4.grid(row=7, column=1)
label5.grid(row=9, column=1)

#기본값 정하기
var1.set(2)
var2.set(1)
var3.set(1)

show()
cv2.moveWindow("photo",350,-100)
cv2.imshow(c_title,controller)
cv2.moveWindow(c_title,600,-100)
window.geometry("550x400+600+200")

#사진 설정
while True:

    b=cv2.getTrackbarPos("Blue",c_title)
    g=cv2.getTrackbarPos("Green",c_title)
    r=cv2.getTrackbarPos("Red",c_title)
    gray=cv2.getTrackbarPos("Gray",c_title)

    window.update()
    show()
    
    if save_photo:
        break
    
    cv2.waitKey(10)

#사진 저장
ans = messageBox(" ", "저장할까요?")
now = now.strftime('%Y-%m-%d %H:%M:%S')
if ans == 'yes':
    para_png = [cv2.IMWRITE_PNG_COMPRESSION, 0]
    if Gray:
        cv2.imwrite("photo"+now+".png", RphotoGray)
    if Color:
        cv2.imwrite("photo"+now+".png", Rphoto)

cam.release()
cv2.destroyAllWindows()
window.destroy()