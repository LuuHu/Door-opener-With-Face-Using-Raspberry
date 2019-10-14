import RPi.GPIO as GPIO
import time
 
delay=0.0010 #delay 2ms
 
pin_4 = 4
pin_17 = 17
pin_23 = 23
pin_24 = 24
 
GPIO.setmode(GPIO.BCM) #设置引脚的编码方式
	
def init():
    GPIO.setwarnings(False)
    GPIO.setup(pin_4, GPIO.OUT)
    GPIO.setup(pin_17, GPIO.OUT)
    GPIO.setup(pin_23, GPIO.OUT)
    GPIO.setup(pin_24, GPIO.OUT)
 
def forward(delay):  
    setStep(1, 0, 0, 0)
    time.sleep(delay)
    setStep(1, 1, 0, 0)
    time.sleep(delay)
    setStep(0, 1, 0, 0)
    time.sleep(delay)
    setStep(0, 1, 1, 0)
    time.sleep(delay)
    setStep(0, 0, 1, 0)
    time.sleep(delay)
    setStep(0, 0, 1, 1)
    time.sleep(delay)
    setStep(0, 0, 0, 1)
    time.sleep(delay)
    setStep(1, 0, 0, 1)
    time.sleep(delay)

def back(delay):
    setStep(0, 0, 0, 1)
    time.sleep(delay)
    setStep(0, 0, 1, 1)
    time.sleep(delay)
    setStep(0, 0, 1, 0)
    time.sleep(delay)
    setStep(0, 1, 1, 0)
    time.sleep(delay)
    setStep(0, 1, 0, 0)
    time.sleep(delay)
    setStep(1, 1, 0, 0)
    time.sleep(delay)
    setStep(1, 0, 0, 0)
    time.sleep(delay)
    setStep(1, 0, 0, 1)
    time.sleep(delay)

def setStep(w1, w2, w3, w4):
  GPIO.output(pin_4, w1)
  GPIO.output(pin_17, w2)
  GPIO.output(pin_23, w3)
  GPIO.output(pin_24, w4)
#waittime second
def runforward(waittime):
    for i in range(int(waittime/delay/4)):
        forward(delay)

def runback(waittime):
    for i in range(int(waittime/delay/4)):
        back(delay)

def door():
    init() 		
    print("f")
    runback(2.4)
    time.sleep(2) 
    print("b")
    runforward(1.9)

# The parameter in function"runback" function"runforward" means the time you decide the moter to run
# time and "runback"/"runforward" to be put prior depend on how you installed your moter and the line