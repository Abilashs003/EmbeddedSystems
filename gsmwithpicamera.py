from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import sys
import serial



SERIAL_PORT= "/dev/ttyS0"
ser=serial.Serial(SERIAL_PORT,baudrate=9600,timeout=5)
ser.write(str.encode("AT+CMGF=1\r")) 
sleep(3)
ser.write(str.encode("AT+CMGD=1,3\r"))
sleep(3)
reply = ser.read(ser.in_waiting)
textMessage="Hi Web Camera captured pictures please look into mail\x1A\r\n"
cmgfCommand="AT+CMGF=1\r"
messageCommand='AT+CMGS="+919880358583"\r'
deleteCommand="AT+CMGD=1,3\r"


#camera and GPIO initialization
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.IN)
GPIO.setup(27, GPIO.IN)
#GPIO.setup(18, GPIO.OUT,initial=GPIO.LOW)
camera=PiCamera()



#mail initialization
fromaddr = "arunmukrambi289@gmail.com"
toaddr = "arunmukrambi289@gmail.com"
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "crafttech360"
body = "Images sent throuh application"
msg.attach(MIMEText(body, 'plain'))
files = "/home/pi/Desktop/Photos/"



while True:
    ser.write(str.encode("AT+CMGL\r"))
    sleep(4)
    reply=ser.read(ser.in_waiting)
    print(reply)
    
    if (('Status' in str(reply) and ('9880358583' in str(reply))) or GPIO.input(17) or GPIO.input(27)):
        camera.start_preview()
        sleep(1)
              
        for x in range(4):
            camera.capture(files + "image"+str(x) +'.jpeg')
            sleep(1)
        filenames = [os.path.join(files, f) for f in os.listdir(files)]
        
        
        #coding  mail
        for file in filenames:
            print(str(file))
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(file, 'rb').read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % file)
            msg.attach(part)
            camera.stop_preview()
            
        #mail sending code
            
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "Rain@997")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
              
        
        #message sending code
        ser.write(str.encode(cmgfCommand))      
        sleep(1)
        ser.write(str.encode(messageCommand))
        sleep(1)
        ser.write(str.encode(textMessage))
        sleep(2)       
        print("Completed")
    
    print(ser.write(str.encode(deleteCommand)))   
    sleep(2)
        
        
        
        
        
    
    
    
    
    
    



