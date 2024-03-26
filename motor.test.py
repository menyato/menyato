import wiringpi as wp
from time import sleep

in1 = 24 #for the first motor
in2 = 23 #for the first motor 
in3 = 5 #for the second motor
in4 = 6 #for the second motor 
en = 25
temp1 = 1

wp.wiringPiSetup()

wp.pinMode(in1, wp.GPIO.OUTPUT)
wp.pinMode(in2, wp.GPIO.OUTPUT)
wp.pinMode(in3, wp.GPIO.OUTPUT)
wp.pinMode(in4, wp.GPIO.OUTPUT)
wp.pinMode(en, wp.GPIO.OUTPUT)

wp.digitalWrite(in1, wp.GPIO.LOW)
wp.digitalWrite(in2, wp.GPIO.LOW)
wp.digitalWrite(in3, wp.GPIO.LOW)
wp.digitalWrite(in4, wp.GPIO.LOW)

p = wp.softPwmCreate(en, 0, 100)

print("\n")
print("The default speed & direction of the motor is LOW & Forward.....")
print("r-run s-stop rig-right lef-left f-forward b-backward l-low m-medium h-high e-exit")
print("\n")

while True:
    x = input()

    if x == 'r':
        print("run")
        if temp1 == 1:
            wp.digitalWrite(in1, wp.GPIO.HIGH)
            wp.digitalWrite(in2, wp.GPIO.LOW)
            wp.digitalWrite(in3, wp.GPIO.HIGH)
            wp.digitalWrite(in4, wp.GPIO.LOW)
            print("forward")
        else:
            wp.digitalWrite(in1, wp.GPIO.LOW)
            wp.digitalWrite(in2, wp.GPIO.HIGH)
            wp.digitalWrite(in3, wp.GPIO.LOW)
            wp.digitalWrite(in4, wp.GPIO.HIGH)
            print("backward")

    elif x == 's':
        print("stop")
        wp.digitalWrite(in1, wp.GPIO.LOW)
        wp.digitalWrite(in2, wp.GPIO.LOW)
        wp.digitalWrite(in3, wp.GPIO.LOW)
        wp.digitalWrite(in4, wp.GPIO.LOW)

    elif x == 'f':
        print("forward")
        wp.digitalWrite(in1, wp.GPIO.HIGH)
        wp.digitalWrite(in2, wp.GPIO.LOW)
        wp.digitalWrite(in3, wp.GPIO.HIGH)
        wp.digitalWrite(in4, wp.GPIO.LOW)
        temp1 = 1
    elif x == 'rig':
        print("right")
        wp.digitalWrite(in1, wp.GPIO.HIGH)
        wp.digitalWrite(in2, wp.GPIO.LOW)
        wp.digitalWrite(in3, wp.GPIO.LOW)
        wp.digitalWrite(in4, wp.GPIO.HIGH)
        temp1 = 1
    elif x == 'lef':
        print("left")
        wp.digitalWrite(in1, wp.GPIO.LOW)
        wp.digitalWrite(in2, wp.GPIO.HIGH)
        wp.digitalWrite(in3, wp.GPIO.HIGH)
        wp.digitalWrite(in4, wp.GPIO.LOW)
        temp1 = 1

    elif x == 'b':
        print("backward")
        wp.digitalWrite(in1, wp.GPIO.LOW)
        wp.digitalWrite(in2, wp.GPIO.HIGH)
        wp.digitalWrite(in3, wp.GPIO.LOW)
        wp.digitalWrite(in4, wp.GPIO.HIGH)
        temp1 = 0

    elif x == 'l':
        print("low")
        wp.softPwmWrite(en, 25)

    elif x == 'm':
        print("medium")
        wp.softPwmWrite(en, 50)

    elif x == 'h':
        print("high")
        wp.softPwmWrite(en, 75)

    elif x == 'e':
        print("Exiting...")
        wp.digitalWrite(in1, wp.GPIO.LOW)
        wp.digitalWrite(in2, wp.GPIO.LOW)
        wp.digitalWrite(in3, wp.GPIO.LOW)
        wp.digitalWrite(in4, wp.GPIO.LOW)
        wp.softPwmStop(en)
        break

    else:
        print("<<<  wrong data  >>>")
        print("Please enter the defined data to continue.....")
