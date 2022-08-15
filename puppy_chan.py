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

lr = Servo(pin0)  # left rear
rr = Servo(pin1)  # right rear
lf = Servo(pin2)  # left front
rf = Servo(pin3)  # right front

# サーボホーンを垂直にしたときのキャリブレーション値
calib = [-8, 5, -2, 0]

# 左前, 右前, 左後, 右後 の角度を指定(-90～90)
# 負の値：前方、正の値：後方
def angle_all_set(servo1, servo2, servo3, servo4):
    # l[fr]は小さい方が前方, r[fr]は大きい方が前方
    lf.write_angle(90 + calib[0] + servo1)
    rf.write_angle(90 + calib[1] - servo2)
    lr.write_angle(90 + calib[2] + servo3)
    rr.write_angle(90 + calib[3] - servo4)

def go1():
    angle_all_set(90-10, 90+10, 90-30, 90+30)   # 前足を前へ
    sleep(80)
    angle_all_set(90-10, 90+10, 90+30, 90-30)   # 後ろ足を後へ
    sleep(80)
    angle_all_set(90+10, 90-10, 90+30, 90-30)   # 前足を後へ
    sleep(80)
    angle_all_set(90+10, 90-10, 90-30, 90+30)   # 後ろ足を前へ
    sleep(80)

def go():
    front_center = -15
    rear_center = +30
    angle_all_set(front_center - 20, front_center + 20, rear_center + 20, rear_center - 20)
    sleep(50)
    angle_all_set(front_center + 20, front_center + 20, rear_center + 20, rear_center - 20)
    sleep(50)
    angle_all_set(front_center + 20, front_center - 20, rear_center + 20, rear_center - 20)
    sleep(50)
    angle_all_set(front_center + 20, front_center - 20, rear_center - 20, rear_center - 20)
    sleep(50)
    angle_all_set(front_center + 20, front_center - 20, rear_center - 20, rear_center + 20)
    sleep(50)
    angle_all_set(front_center - 20, front_center - 20, rear_center - 20, rear_center + 20)
    sleep(50)
    angle_all_set(front_center - 20, front_center + 20, rear_center - 20, rear_center + 20)
    sleep(50)
    angle_all_set(front_center - 20, front_center + 20, rear_center + 20, rear_center + 20)
    sleep(50)

def rev():
    front_center = -30
    rear_center = +15
    angle_all_set(front_center - 20, front_center + 20, rear_center + 20, rear_center - 20)
    sleep(50)
    angle_all_set(front_center - 20, front_center + 20, rear_center + 20, rear_center + 20)
    sleep(50)
    angle_all_set(front_center - 20, front_center + 20, rear_center - 20, rear_center + 20)
    sleep(50)
    angle_all_set(front_center - 20, front_center - 20, rear_center - 20, rear_center + 20)
    sleep(50)
    angle_all_set(front_center + 20, front_center - 20, rear_center - 20, rear_center + 20)
    sleep(50)
    angle_all_set(front_center + 20, front_center - 20, rear_center - 20, rear_center - 20)
    sleep(50)
    angle_all_set(front_center + 20, front_center - 20, rear_center + 20, rear_center - 20)
    sleep(50)
    angle_all_set(front_center + 20, front_center + 20, rear_center + 20, rear_center - 20)
    sleep(50)

def puppy():
    angle_all_set(55, 60, 130, 120)
    sleep(100)
    angle_all_set(55, 160, 130, 120)
    sleep(100)
    angle_all_set(120, 130, 150, 60)
    sleep(100)
    angle_all_set(120, 130, 60, 60)
    sleep(100)
    angle_all_set(55, 130, 60, 60)
    sleep(100)
    angle_all_set(55, 60, 130, 30)
    sleep(100)


angle_all_set(0, 0, 0, 0)
sleep(3000)

running = True
reversed_time = running_time()
mode = "forward"

while True:
    if button_a.was_pressed():
        running = not running
    if running_time() - reversed_time > 5000:
        reversed = not reversed
        reversed_time = running_time()
    if running:
        if mode == "forward":
            go()
        elif mode == "reverse":
            rev()
        else:
            pass    #stop
