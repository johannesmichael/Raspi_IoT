import hp206c
from collections import namedtuple, deque
from threading import Thread
import RPi.GPIO as GPIO
from time import sleep
from picamera import PiCamera
from datetime import utcnow


h= hp206c.hp206c()

ret=h.isAvailable()
if h.OK_HP20X_DEV == ret:
    print("HP20x_dev is available.")
else:
    print("HP20x_dev isn't available.")



temp=h.ReadTemperature()
pressure=h.ReadPressure()
altitude=h.ReadAltitude()


def sense_forever():
    while True:
        samples = deque(maxlen=5)
        pressure = h.ReadPressure()
        samples.append(pressure)
        # Show sample, number of samples, total and moving average
        N = len(samples)
        total = sum(samples)
        movingAvg = total/N
        print(f'value: {pressure}, num samples: {N}, total: {total}, moving average: {movingAvg}')
        sleep(1)
        sensor_data = namedtuple("sensor_data", ["pressure", "N", "total", "movingAvg"])
        return sensor_data(pressure, N, total, movingAvg)

sensor = Thread(target=sense_forever)
sensor.daemon = True
sensor.start()


#camera.start_preview()
#sleep(2)
#utcnow().strftime('%B %d %Y - %H:%M:%S')
#camera.capture('/home/pi/Data/Images/image'+ str(utcnow())'.jpg')
#camera.stop_preview()


# try:
#    while True:
#      if GPIO.input(PIR_PIN):
#        print("Motion Detected!")
#        t = Thread(target=light) # Create thread
#        t.start() # Start thread
#      time.sleep(0.5)
# except KeyboardInterrupt:
#    GPIO.cleanup()



# from threading import Thread
# import RPi.GPIO as GPIO
# import time

# GPIO.setmode(GPIO.BCM)
# PIR_PIN = 18
# GPIO.setup(PIR_PIN, GPIO.IN)
# LED_PIN = 17
# GPIO.setup(LED_PIN, GPIO.OUT)
# def light():
#     GPIO.output(LED_PIN, GPIO.input(PIR_PIN))
#     time.sleep(5)
#     GPIO.output(LED_PIN, False)
# try:
#    while True:
#      if GPIO.input(PIR_PIN):
#        print("Motion Detected!")
#        t = Thread(target=light) # Create thread
#        t.start() # Start thread
#      time.sleep(0.5)
# except KeyboardInterrupt:
#    GPIO.cleanup()

# import threading
# import time

# def sense_forever():
#     while True:
#         pressure = h.ReadPressure()
#         print('reading sensor')
#         time.sleep(5)

# sensor = threading.Thread(target=sense_forever)
# sensor.daemon = True
# sensor.start()

# while True:
#     print('This part of the program is not blocked by the sensor')
#     time.sleep(1)