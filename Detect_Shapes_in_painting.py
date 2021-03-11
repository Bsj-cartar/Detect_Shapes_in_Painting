import cv2
import tkinter
from tkinter import *
from PIL import Image, ImageTk, ImageGrab
import numpy as np


def setLabel(image, str, contour):
    (text_width, text_height), baseline = cv2.getTextSize(str, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 1)
    x,y,width,height = cv2.boundingRect(contour)
    pt_x = x+int((width-text_width)/2)
    pt_y = y+int((height+text_height)/2)
    cv2.rectangle(image, (pt_x, pt_y+baseline), (pt_x+text_width, pt_y-text_height), (200, 200, 200), cv2.FILLED)
    cv2.putText(image, str, (pt_x, pt_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 1, 8)


def location(x, y, w, h):
    rect = [[x, y], [x+w, y], [x, y+h], [x+w, y+h]]


def convert_to_tkimage():
    globals()
    src = cv2.imread("capture.png")
    dst = src.copy()
    img = cv2.cvtColor(src, cv2.COLOR_BGR2RGB)

    img = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=img)

    label = tkinter.Label(window, image=imgtk)
    label.pack(side="top")

    gray = ~cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    ungray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    img = Image.fromarray(binary)
    imgtk = ImageTk.PhotoImage(image=img)

    label.config(image=imgtk)
    label.image = imgtk

    for cnt in contours:
        cv2.drawContours(src, [cnt], 0, (255, 0, 0), 3)  # blue

    cv2.imshow("result", src)

    cv2.waitKey(0)

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        print("외곽 경계선 좌표")
        print(x, y, w, h)
        location(x, y, w, h)
        cv2.rectangle(src, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("result", src)

    cv2.waitKey(0)

    for cnt in contours:
        flag = 0
        size = len(cnt)
        print("컨투어 구성 개수")
        print(size)

        epsilon = 0.03 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        size = len(approx)
        print("컨투어를 직선으로 근사화 후 컨투어 구성 개수")
        print(size)

        cv2.line(src, tuple(approx[0][0]), tuple(approx[size-1][0]), (0, 255, 0), 3)
        for k in range(size-1):
            cv2.line(src, tuple(approx[k][0]), tuple(approx[k+1][0]), (0, 255, 0), 3)

        if size == 3:
            setLabel(src, "triangle", cnt)
            flag = 1
        elif size == 4:
            setLabel(src, "rectangle", cnt)
            flag = 1
        elif size == 5:
            setLabel(src, "pentagon", cnt)
            flag = 1
        elif size == 6:
            setLabel(src, "hexagon", cnt)
            flag = 1
        else:
            setLabel(src, str(size), cnt)

        cv2.imshow('result', src)
        cv2.waitKey(0)
    if flag == 0:
        circles = cv2.HoughCircles(ungray, cv2.HOUGH_GRADIENT, 1, 100, param1=250, param2=10, minRadius=80, maxRadius=120)

        for i in circles[0]:
            cv2.circle(dst, (int(i[0]), int(i[1])), int(i[2]), (255, 0, 0), 5, None, None)
            print(i[0])
        cv2.imshow('result', dst)
        cv2.waitKey(0)


def save():
    x = window.winfo_rootx()  # 창의 왼쪽 위의 x 좌표
    y = window.winfo_rooty()  # 창의 왼쪽 위의 y 좌표
    w = window.winfo_width() + x
    h = window.winfo_height() + y - 55

    box = (x, y, w, h)
    canvas_image = ImageGrab.grab(box)  # 창의 크기만큼만 이미지저장
    saveas = 'capture.png'
    canvas_image.save(saveas)  # 이미지를 파일로 저장


window = None
canvas = None

x1, y1 = None, None


def mouseMove(event):
    global x1, y1
    x1 = event.x
    y1 = event.y
    canvas.create_oval(x1, y1, x1+1, y1+1, width=10, fill = "blue")


window = Tk()
window.title("그림판2")

canvas = Canvas(window, height = 300, width = 300)
canvas.bind("<B1-Motion>", mouseMove)


button = tkinter.Button(window, text="도형 인식", command=convert_to_tkimage)
button.pack(side="bottom", expand=True, fill='both')

button2 = tkinter.Button(window, text="저장", command=save)
button2.pack(side="bottom", expand=True, fill='both')

canvas.pack()
window.mainloop()