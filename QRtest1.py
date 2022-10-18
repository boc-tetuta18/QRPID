from pickle import NONE
import cv2
import numpy as np
import RPi.GPIO as GPIO
import sys


#capsetup
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('H', '2', '6', '4'));
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 680)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
# initialize the cv2 QRCode detector
detector = cv2.QRCodeDetector()
test_data = "qr/2/1"
firstlookID = -1

while True:
    frame, img = cap.read()
    output_img = img.copy()
    #detect and decode to QR
    retval, decoded_info, points, staraight_qrcode = detector.detectAndDecodeMulti(img)
    data_list = []
    for i in decoded_info:
        #print(i)
        data_list.append(list(map(int, i.split())))
    #print(data_list)
    data_listex = [30, 2, 1] #rosからsubしたstuck_robotのID
    for i, data in enumerate(data_list):
        if data == []:
            continue
        if data[1] == data_listex[1]:
            print(points[i])
            if firstlookID == -1:
                firstlookID = data[2]

            if firstlookID == data[2]:
                S1 =  ((points[i][3][0]-points[i][1][0])*(points[i][0][1]-points[i][1][1])-(points[i][3][1]-points[i][1][1])*(points[i][0][0]-points[i][1][0]))/2
                S2 =  ((points[i][3][0]-points[i][1][0])*(points[i][1][1]-points[i][2][1])-(points[i][3][1]-points[i][1][1])*(points[i][1][0]-points[i][2][0]))/2
        
                C1_x = points[i][0][0] + (points[i][2][0]-points[i][0][0])*S1/(S1 + S2)
                C1_y = points[i][0][1] + (points[i][2][1]-points[i][0][1])*S1/(S1 + S2)
                print('hhhhhhhhhhhhhhhhhh')
                print(C1_x,C1_y)
               






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