import smtplib
from rpilcd import LCD
from email.message import EmailMessage
from gpiozero import DistanceSensor, LED, Button, Buzzer
from time import sleep
import os
os.system("sudo pigpiod")
from gpiozero.pins.pigpio import PiGPIOFactory

"""
This script is designed to monitor the distance of objects using an ultrasonic sensor
attached to a Raspberry Pi. When an object is detected within a defined threshold distance,
the script will trigger a visual and auditory alert, and send an email notification.
"""

lcd = LCD()

echo_pin = 21  # Connected from 'echopin' to 'echo_pin'
trigger_pin = 20  # Connected from 'triggerpin' to 'trigger_pin'
redLED = LED(19)
myfactory = PiGPIOFactory()

switch = Button(26)
ultrasonic = DistanceSensor(echo=echo_pin, trigger=trigger_pin, pin_factory=myfactory)
buzzer = Buzzer(12)

from_email_addr = "raspberrypi10110@gmail.com"
from_email_pass = "salrdorsckpnhirf"
to_email_addr = "alexandra.eliana34@gmail.com"

def send_warning_email(distance):
    """
    Sends a warning email with the specified distance of an object detected by the ultrasonic sensor.
    Arguments:
    distance -- The measured distance to the object in centimeters.
    """
    msg = EmailMessage()
    body = f"Hello from Raspberry Pi, something close at {distance:.1f} cm!"
    msg.set_content(body)
    msg['From'] = from_email_addr
    msg['To'] = to_email_addr
    msg['Subject'] = 'ALERT EMAIL: Object Detected Close'
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    print('starttls')
    server.login(from_email_addr, from_email_pass)
    print('login')
    server.send_message(msg)
    print('Email sent')
    server.quit()

def ledflash():
    """
    Flashes the red LED 5 times to signal the detection of an object.
    """
    for i in range(5):
        redLED.on()
        sleep(0.5)
        redLED.off()
        sleep(0.5)

def monitor_distance():
    """
Continuously monitors the distance to objects using the ultrasonic sensor.
    If an object is detected within the defined threshold, it triggers ledflash,
    buzzer, and sends a warning email.
"""
threshold_distance = 10  # Distance in centimeters.
    
    while True:
        distance_cm = ultrasonic.distance * 100  # Converts to centimeters.
        lcd.text(f"Measured distance: {distance_cm:.1f} cm", 1)
        
        if distance_cm < threshold_distance:
            print("Something is close, sending an email and sounding buzzer...")
            buzzer.on()
            sleep(1)
            buzzer.off()
            ledflash()
            send_warning_email(distance_cm)
            lcd.clear()

if __name__ == "__main__":
    """
    The main execution block of the script.
    """
    try:
        while True:
            if switch.is_pressed:
                monitor_distance()
    except KeyboardInterrupt:
        print("Program terminated.")
        buzzer.close()
        redLED.close()
