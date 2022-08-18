"""
from https://learn.sparkfun.com/tutorials/getting-started-with-micropython-and-the-sparkfun-inventors-kit-for-microbit/experiment-8-using-a-servo-motor
"""
from microbit import *


class Servo:
    def __init__(self, pin, freq=50, min_us=600, max_us=2400, angle=180):
        self.min_us = min_us
        self.max_us = max_us
        self.us = 0
        self.freq = freq
        self.angle = angle
        self.analog_period = 0
        self.pin = pin
        analog_period = round((1 / self.freq) * 1000)  # hertz to miliseconds
        self.pin.set_analog_period(analog_period)
        self.pin.write_analog(0)

    def write_us(self, us):
        us = min(self.max_us, max(self.min_us, us))
        duty = round(us * 1024 * self.freq // 1000000)
        self.pin.write_analog(duty)

    def write_angle(self, degrees=None):
        if degrees is None:
            degrees = math.degrees(radians)
        degrees = degrees % 360
        total_range = self.max_us - self.min_us
        us = self.min_us + total_range * degrees // self.angle
        self.write_us(us)


# pin3を使うため
display.off()

# [Servo, サーボホーンを垂直にしたときのキャリブレーション値]
left_front = [Servo(pin2), -15]  # left front
right_front = [Servo(pin3), 10]   # right front
left_rear = [Servo(pin0), -10]  # left rear
right_rear = [Servo(pin1), 5]   # right rear

# 左前, 右前, 左後, 右後 の角度を指定(-90～90)
# 負の値：前方、正の値：後方
def set_all_angle(servo1, servo2, servo3, servo4):
    # l[fr]は小さい方が前方, r[fr]は大きい方が前方
    left_front[0].write_angle(90 + left_front[1] + servo1)
    right_front[0].write_angle(90 + right_front[1] - servo2)
    left_rear[0].write_angle(90 + left_rear[1] + servo3)
    right_rear[0].write_angle(90 + right_rear[1] - servo4)

# 角度を設定
def set_angle(servo, angle):
    if servo == right_front or servo == right_rear:
        angle = -angle
    servo[0].write_angle(90 + servo[1] + angle)

def go():
    front_center = -15
    rear_center = +30
    set_angle(left_front, front_center + 20)
    sleep(50)
    set_angle(right_front, front_center - 20)
    sleep(50)
    set_angle(left_rear, rear_center - 20)
    sleep(50)
    set_angle(right_rear, rear_center + 20)
    sleep(50)
    set_angle(left_front, front_center - 20)
    sleep(50)
    set_angle(right_front, front_center + 20)
    sleep(50)
    set_angle(left_rear, rear_center + 20)
    sleep(50)
    set_angle(right_rear, rear_center - 20)
    sleep(50)

def rev():
    front_center = -30
    rear_center = +15

    set_angle(right_rear, rear_center + 20)
    sleep(50)
    set_angle(left_rear, rear_center - 20)
    sleep(50)
    set_angle(right_front, front_center - 20)
    sleep(50)
    set_angle(left_front, front_center + 20)
    sleep(50)
    set_angle(right_rear, rear_center - 20)
    sleep(50)
    set_angle(left_rear, rear_center + 20)
    sleep(50)
    set_angle(right_front, front_center + 20)
    sleep(50)
    set_angle(left_front, front_center - 20)
    sleep(50)

def puppy():
    set_all_angle(55, 60, 130, 120)
    sleep(100)
    set_all_angle(55, 160, 130, 120)
    sleep(100)
    set_all_angle(120, 130, 150, 60)
    sleep(100)
    set_all_angle(120, 130, 60, 60)
    sleep(100)
    set_all_angle(55, 130, 60, 60)
    sleep(100)
    set_all_angle(55, 60, 130, 30)
    sleep(100)


set_all_angle(0, 0, 0, 0)
sleep(3000)

running = True
reversed_time = running_time()
mode = "forward"

while True:
    if button_a.was_pressed():
        running = not running
    if running:
        if running_time() - reversed_time > 5000:
            mode = "reverse" if mode == "forward" else "forward"
            reversed_time = running_time()
        if mode == "forward":
            go()
        elif mode == "reverse":
            rev()
        else:
            pass    #stop
