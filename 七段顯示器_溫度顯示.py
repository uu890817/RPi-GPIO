import os
import RPi.GPIO as GPIO
from time import sleep

#溫度計算

temp10 = 0
temp1 = 0

def tempNow():
    readTemp = os.popen("cat /sys/class/thermal/thermal_zone0/temp")
    temp = readTemp.readlines()
    temp = temp[0]
    return temp

def tempComp(temp):
    temp = int(temp / 1000)
    temp10 =int(temp /10)
    temp1 = int(temp - temp10 * 10)
    print (temp , temp10 , temp1)
    return [temp10 , temp1]

#GPIO

GPIO.cleanup()

#定義腳位
powerPin = 17
dataPin = 23
shiftPin = 24
STPin = 25

#BCM模式
GPIO.setmode(GPIO.BCM)

#使用輸出模式
GPIO.setup(powerPin , GPIO.OUT)
GPIO.setup(dataPin , GPIO.OUT)
GPIO.setup(shiftPin , GPIO.OUT)
GPIO.setup(STPin , GPIO.OUT)


#十位數資料
data_10 = [
[1,0,1,1,1,1,1,1],
[1,0,0,0,0,1,1,0],
[1,1,0,1,1,0,1,1],
[1,1,0,0,1,1,1,1],
[1,1,1,0,0,1,1,0],
[1,1,1,0,1,1,0,1],
[1,1,1,1,1,1,0,1],
[1,0,1,0,0,1,1,1],
[1,1,1,1,1,1,1,1],
[1,1,1,0,1,1,1,1]
]

#個位數資料
data_1 = [
[0,0,1,1,1,1,1,1],
[0,0,0,0,0,1,1,0],
[0,1,0,1,1,0,1,1],
[0,1,0,0,1,1,1,1],
[0,1,1,0,0,1,1,0],
[0,1,1,0,1,1,0,1],
[0,1,1,1,1,1,0,1],
[0,0,1,0,0,1,1,1],
[0,1,1,1,1,1,1,1],
[0,1,1,0,1,1,1,1]
]


#資料傳輸
def dataUpdate(dataIn):

    GPIO.output(STPin , 0)
    GPIO.output(shiftPin , 0)

    GPIO.output(dataPin , dataIn)
    GPIO.output(shiftPin , 1)
    GPIO.output(shiftPin , 0)
    GPIO.output(STPin , 1)

def dataPush_10(temp10):
    for db_10 in data_10[temp10]:
       # print (db_10)
        dataUpdate(db_10)

def dataPush_1(temp1):
    for db_1 in data_1[temp1]:
       # print (db_1)
        dataUpdate(db_1)


try:
    while True:
        temp = int(tempNow())
        tempFinal = tempComp(temp)
        temp10 = tempFinal[0]
        temp1 =tempFinal[1]
        dataPush_10(temp10)
        sleep(2)
        dataPush_1(temp1)
        sleep(2)
        print ("--------------------------")

except KeyboardInterrupt:
   GPIO.cleanup()
   pass




#GPIO.cleanup()


