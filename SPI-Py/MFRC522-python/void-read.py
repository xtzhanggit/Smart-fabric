#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import socket
import time

continue_reading = True


# Capture SIGINT for cleanup when the script is aborted
def end_read(signal, frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()


# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print "Welcome to the MFRC522 data read example"
print "Press Ctrl-C to stop."

## 向ａ账户发送信号
def send_signal_a(x):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建socket对象
    # def connect():
    ip_port = ('192.168.1.10', 3145)  # 局域网server的ip，公共端口号
    s.connect(ip_port)
    s.send(x.encode())


## 向b账户发送信号
def send_signal_b(x):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建socket对象
    # def connect():
    ip_port = ('192.168.1.10', 3146)  # 局域网server的ip，公共端口号
    s.connect(ip_port)
    s.send(x.encode())


def detect():
    timekeeping=0
    # This loop keeps checking for chips. If one is near it will get the UID and authenticate
    while continue_reading:
        # Scan for cards
        (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        # If a card is found
        if status == MIFAREReader.MI_OK:
                print "Card detected"
                send_signal_a('1')
                send_signal_b('1')
                break

detect()




