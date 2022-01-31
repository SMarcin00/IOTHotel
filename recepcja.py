#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import tkinter
import time
import datetime
import re
import sys

broker = "192.168.10.4"

client = mqtt.Client()
window = tkinter.Tk()
uid_table = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
counter = 0
port = 8883
gatesList = []

errorFlag = False
# importy i setup dla platformy rzeczywistej
# from mfrc522 import MFRC522
# from datetime import datetime
# import neopixel
# import board

# read = False
# flag = False
# cardNumber = ""
# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
#
# led1 = 13
# led2 = 12
# led3 = 19
# led4 = 26
# GPIO.setup(led1, GPIO.OUT)
# GPIO.setup(led2, GPIO.OUT)
# GPIO.setup(led3, GPIO.OUT)
# GPIO.setup(led4, GPIO.OUT)
#
# buttonRed = 5
# buttonGreen = 6
# encoderLeft = 17
# encoderRight = 27
# GPIO.setup(buttonRed, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(buttonGreen, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(encoderLeft, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(encoderRight, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#
# buzzerPin = 23
# GPIO.setup(buzzerPin, GPIO.OUT)
# GPIO.output(buzzerPin, 1)
#
# ws2812pin = 8
#
# MIFAREReader = MFRC522()

# kod dla platformy rzeczywistej
# def off(pixels):
#     pixels[0] = (0, 0, 0)
#     pixels[1] = (0, 0, 0)
#     pixels[2] = (0, 0, 0)
#     pixels[3] = (0, 0, 0)
#     pixels[4] = (0, 0, 0)
#     pixels[5] = (0, 0, 0)
#     pixels[6] = (0, 0, 0)
#     pixels[7] = (0, 0, 0)
#     pixels.show()
#
#
# def buzzer(state):
#     GPIO.output(buzzerPin, not state)
#
#
# def rfidRead():
#     global read
#     global cardNumber
#
#     (status, tagName) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
#
#     if status == MIFAREReader.MI_OK:
#         (status, uid) = MIFAREReader.MFRC522_Anticoll()
#         if status == MIFAREReader.MI_OK:
#             read = True
#             buzzer(True)
#             print(datetime.now())
#             GPIO.output(led1, True)
#             time.sleep(0.2)
#             buzzer(False)
#             GPIO.output(led1, False)
#             num = 0
#             for i in range(0, len(uid)):
#                 num += uid[i] << (i * 8)
#
#             cardNumber = str(num)


def clean_frame(frame, flag=True):
    frame.pack_forget()
    if not flag:
        create_main_window()


def success_window(frame):
    clean_frame(frame)
    window.geometry("300x200")
    main_frame = tkinter.Frame(window)
    main_frame.pack()
    my_canvas = tkinter.Canvas(main_frame)
    intro_label = tkinter.Label(main_frame, text="System:", font=40, wraplength=300).pack()
    intro_label1 = tkinter.Label(main_frame, text="Karta zostala poprawnie skonfigurowana", font=40, wraplength=300).pack()
    button_4 = tkinter.Button(main_frame, text="Menu", wraplength=300,
                              command=lambda: clean_frame(main_frame, False))
    button_4.pack()
    for i in range(8):
        my_canvas.create_oval(70 + i*20, 20, 90 + i*20, 40, fill='green')
    my_canvas.pack()



def call_server_date(uid, room, endDate, guestId, frame):
    client.publish("reception", uid + "," + room + "," + endDate + "," + guestId)
    success_window(frame)

    
def create_main_window():
    window.geometry("300x200")
    window.title("Recepcja")
    main_frame = tkinter.Frame(window)
    main_frame.pack()

    intro_label = tkinter.Label(main_frame, text="Hotel IOT", font=40).grid(row=0,column=1)
    label_1 = tkinter.Label(main_frame, text="UID karty:").grid(row=1,column=0)
    entry_1 = tkinter.Entry(main_frame)
    entry_1.grid(row=1,column=1)
    label_2 = tkinter.Label(main_frame, text="Room IP:").grid(row=2,column=0)
    entry_2 = tkinter.Entry(main_frame)
    entry_2.grid(row=2,column=1)
    label_3 = tkinter.Label(main_frame, text="Data:").grid(row=3,column=0)
    entry_3 = tkinter.Entry(main_frame)
    entry_3.grid(row=3,column=1)
    label_4 = tkinter.Label(main_frame, text="Gosc ID:").grid(row=4,column=0)
    entry_4 = tkinter.Entry(main_frame)
    entry_4.grid(row=4,column=1)
    button_1 = tkinter.Button(main_frame, text="Odczytaj karte:",
                              command=lambda: call_server_date(entry_1.get(), entry_2.get(), entry_3.get(), entry_4.get(), main_frame))
    button_1.grid(row=5,column=1)


def on_connect(client,userdata,flags,rc):
    global errorFlag
    print("Connected flags", str(flags), "results code", str(rc))
    if rc != 0:
        errorFlag = True
        print("Authorization failed")


def connect_to_broker():
    global errorFlag
    client.tls_set('/home/pi/Projekt/ca.crt')
    client.tls_insecure_set(True)
    client.username_pw_set(username='recepcja', password='recepcja')
    client.on_connect = on_connect
    client.connect(broker, port)
#     client.on_message = process_message
    client.subscribe("reception")
    client.loop_start()
    time.sleep(3)
    if errorFlag:
        print("Authorization error")
        sys.exit()


def disconnect_from_broker():
    client.disconnect()
      
    
def run_sender():
    connect_to_broker()
    create_main_window()
    window.mainloop()
    disconnect_from_broker()


if __name__ == "__main__":
    run_sender()