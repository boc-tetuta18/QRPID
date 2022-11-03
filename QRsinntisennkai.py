from pickle import NONE
import cv2
import numpy as np
import RPi.GPIO as GPIO
import sys
from matplotlib import pyplot as plt
from numpy.random import *
import time


#initialize PID parameter

goal = 340 #cener of capture_img
dt = 1
e = 0 #error
e1 = 0 #pre error
acc = 0 #accumulation
dif = 0 #deviation
Kp = 50/300
Ki = 0.1
Kd = 0.1

t= 100

count_time = 0

#graff
x_list = []
y_list = []

def tic():
    global start_time_tictoc
    start_time_tictoc = time.time()

def toc(tag="elapsed time"):
    if "start_time_tictoc" in globals():
        print("{}: {:.9f} [sec]".format(tag, time.time() - start_time_tictoc))
    else:
        print("tic has not been called")


duty = 85

#GPIO initial set
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)




p1 = GPIO.PWM(27, 10000) #50Hz
p2 = GPIO.PWM(22, 10000) #50Hz
p3 = GPIO.PWM(23, 10000) #50Hz
p4 = GPIO.PWM(24, 10000) #50Hz

p1.start(0)
p2.start(0)
p3.start(0)
p4.start(0)


#capsetup
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('H', '2', '6', '4'));
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 680)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
# initialize the cv2 QRCode detector
detector = cv2.QRCodeDetector()
test_data = "qr/2/1"
firstlookID = -1

print(dir(GPIO))

while True:
    frame, img = cap.read()
    output_img = img.copy()
    #detect and decode to QR
    retval, decoded_info, points, staraight_qrcode = detector.detectAndDecodeMulti(img) #decoded_info:(('str'),('str'),...)
    data_list = [] #
    for i in decoded_info:
        #print(i)
        data_list.append(list(map(int, i.split()))) #decoded_info[i]'s str are splited to int type and list type then append to data_list
    
    data_listex = [30, 2, 1] #rosからsubしたstuck_robotのID
    for i, data in enumerate(data_list): #data youso toridasi,  data_list:(('int,int,int'),('int,int,int'),...),  data:('int,int,int')
        if data == []:
            continue
        if data[1] == data_listex[1]:
            #print(points[i])
            if firstlookID == -1: #when camera look ID first time, lookID is changed 
                firstlookID = data[2]

            if firstlookID == data[2]: #when camera look ID first time, get center of QR's points
                S1 =  ((points[i][3][0]-points[i][1][0])*(points[i][0][1]-points[i][1][1])-(points[i][3][1]-points[i][1][1])*(points[i][0][0]-points[i][1][0]))/2
                S2 =  ((points[i][3][0]-points[i][1][0])*(points[i][1][1]-points[i][2][1])-(points[i][3][1]-points[i][1][1])*(points[i][1][0]-points[i][2][0]))/2
        
                C1_x = points[i][0][0] + (points[i][2][0]-points[i][0][0])*S1/(S1 + S2)
                C1_y = points[i][0][1] + (points[i][2][1]-points[i][0][1])*S1/(S1 + S2)
                #print('hhhhhhhhhhhhhhhhhh')
                #print(C1_x,C1_y)

                #Pcontrol
                
                e = goal - C1_x
                acc = acc + e*i
                dif = (e - e1) / i
                #print(C1_x)

                output = Kp * e
                e1 = e

                duty_out = abs(np.clip(output,-50,50))
                duty_in = np.clip(duty_out,20,50)
                #print(duty_out)
                x_list.append(i)
                y_list.append(output)

                

                if 0 < C1_x < 320:
                    p1.ChangeDutyCycle(duty_out)
                    p2.ChangeDutyCycle(0)
                    p3.ChangeDutyCycle(0)
                    p4.ChangeDutyCycle(0)

                    count_time = 0
                


                    
                elif 320 <= C1_x <= 360:
                    count_time = count_time + 1
                    p1.ChangeDutyCycle(0)
                    p2.ChangeDutyCycle(0)
                    p3.ChangeDutyCycle(0)
                    p4.ChangeDutyCycle(0)
                    print(count_time)
                    
                    if count_time > 20:
                        p1.ChangeDutyCycle(duty_out)
                        p2.ChangeDutyCycle(0)
                        p3.ChangeDutyCycle(duty_out)
                        p4.ChangeDutyCycle(0)
                        


                elif 360 < C1_x < 680:
                    p1.ChangeDutyCycle(0)
                    p2.ChangeDutyCycle(0)
                    p3.ChangeDutyCycle(duty_out)
                    p4.ChangeDutyCycle(0)

                    count_time = 0





               






    #data_list = list(map(int, decoded_info_list.split()))
    #print(data_list)
    #data_list = list(map(int, decoded_info_list))
    
   

    #if not len(data_list) == 0: #QR読み取れている時
        #for p in zip(points):
            #print(p)
            #print('/n')
         #if data_list[1] == data_listex[1]: #stuck_robotのIDと読み取ったQRのIDが一致している際
            #points=points.astype(int).reshape(-1,2)
            #print(points)
            #print(data_list)
            #cv2.putText(output_img, decoded_info, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 5, cv2.LINE_AA)

            #QRcoordinate
                

            #for i in range(4):
                #cv2.line(output_img, tuple(points[i]), tuple(points[(i+1)%len(points)]), (0, 0, 255), 4)

    cv2.imshow("QRCODEscanner", output_img)    
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

GPIO.cleanup(27)
GPIO.cleanup(22)
GPIO.cleanup(23)
GPIO.cleanup(24)