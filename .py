#importing necessary modules
import smtplib
from rpilcd import LCD
from email.message import EmailMessage
from gpiozero import DistanceSensor, LED, Button, Buzzer
from time import sleep
import os

#start pigpiod daemon
os.system("sudo pigpiod")

# importing necessary pins factory for gpiozero
from gpiozero.pins.pigpio import PiGPIOFactory

#creating lcd object
lcd = LCD()

#echo_pin and trigger_pin for ultrasonic sensor
echo_pin = 21  # Connected from 'echopin' to 'echo_pin'
trigger_pin = 20  # Connected from 'triggerpin' to 'trigger_pin'

#red led object
redLED = LED(19)

#factory for gpiozero pins
myfactory = PiGPIOFactory()

#switch object
switch = Button(26)

#ultrasonic sensor object
ultrasonic = DistanceSensor(echo=echo_pin, trigger=trigger_pin, pin_factory=myfactory)

#buzzer object
buzzer = Buzzer(12)

#from email address and password
from_email_addr = "raspberrypi10110@gmail.com"
from_email_pass = "salrdorsckpnhirf"

#to email address
to_email_addr = "alexandra.eliana34@gmail.com"

# function to send warning email
def send_warning_email(distance):
    # establish connection to gmail smtp server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    
    # starttls encryption
    server.starttls()
    
    # login to gmail account
    server.login(from_email_addr, from_email_pass)
    
    # send email
    server.send_message(msg)
    
    # print success message
    print('Email sent')
    
    # terminate connection
    server.quit()

# function to flash red led
def ledflash():
    for i in range(5):
        redLED.on()
        sleep(0.5)
        redLED.off()
        sleep(0.5)

# function to monitor distance and trigger alerts if below threshold
def monitor_distance():
    threshold_distance = 10  # distance threshold set at 10cm
    
    while True:
        distance_cm = ultrasonic.distance * 100  # convert distance to centimeters
        lcd.text(f"Measured distance: {distance_cm:.1f} cm", 1)
        
        if distance_cm  threshold_distance:
            print("Something is close, triggering alerts...")
            buzzer.on()
            sleep(1)
            buzzer.off()
            ledflash()
            send_warning_email(distance_cm)
            lcd.clear()

# main execution block
if __name__ == "__main__":
    try:
        while True:
            if switch.is_pressed:
                monitor_distance()
    except KeyboardInterrupt:
        print("Program terminated.")
        buzzer.close()
        redLED.close()
