import spidev
import time
'''
import pigpio

pi = pigpio.pi() # connect to pi
CS1 = 4 #GPIO pin 4
CS2 = 27
CS3 = 22
CS4 = 5
CS5 = 6
CS6 = 26
CS7 = 25
CS8 = 24

pi.set_mode(CS1, pigpio.OUTPUT)
pi.set_mode(CS2, pigpio.OUTPUT)
pi.set_mode(CS3, pigpio.OUTPUT)
pi.set_mode(CS4, pigpio.OUTPUT)
pi.set_mode(CS5, pigpio.OUTPUT)
pi.set_mode(CS6, pigpio.OUTPUT)
pi.set_mode(CS7, pigpio.OUTPUT)
pi.set_mode(CS8, pigpio.OUTPUT)

# set all gpio CS to HIGH (inactive)
pi.write(CS1, 1)
pi.write(CS2, 1)
pi.write(CS3, 1)
pi.write(CS4, 1)
pi.write(CS5, 1)
pi.write(CS6, 1)
pi.write(CS7, 1)
pi.write(CS8, 1)
'''

# BITMAPS
zero = [0b00011000, 0b00100100, 0b01001010, 0b01001010, 0b01010010, 0b01010010, 0b00100100, 0b00011000]
one = [0b00000100, 0b00001100, 0b00010100, 0b00000100, 0b00000100, 0b00000100, 0b00000100, 0b00111110]
two = [0b00011000, 0b00100100, 0b00000100, 0b00001000, 0b00010000, 0b00100000, 0b00100000, 0b00111100]
three = [0b00111000, 0b00000100, 0b00000100, 0b00011100, 0b00011100, 0b00000100, 0b00000100, 0b00111000]
four = [0b01000100, 0b01000100, 0b01000100, 0b00110100, 0b00001100, 0b00000100, 0b00000100, 0b00000100]
five = [0b00111100, 0b01000000, 0b01000000, 0b00111100, 0b00000010, 0b00000010, 0b00000010, 0b00111100]
six = [0b00011000, 0b00100000, 0b00100000, 0b00111100, 0b00100010, 0b00100010, 0b00100100, 0b00011000]
seven = [0b01111110, 0b00000010, 0b00000100, 0b00000100, 0b00001000, 0b00001000, 0b00010000, 0b00010000]
eight = [0b00011000, 0b00100100, 0b01000010, 0b00111110, 0b01111100, 0b01000010, 0b00100100, 0b00011000]
nine = [0b00011100, 0b00100100, 0b01000010, 0b01000010, 0b00111110, 0b00000010, 0b00000100, 0b00111000]

# TEST MATRIX FUNCTION

def testMatrix():
    spi = spidev.SpiDev()
    spi.open(0,0)
    spi.max_speed_hz = 10000000
    
    #pi.write(CS1, 0)
    spi.xfer([0x0c, 0x01]) # disables shutdown mode
    #pi.write(CS1, 1)
    #pi.write(CS1, 0)
    spi.xfer([0x0f, 0x00]) # disables display test
    #pi.write(CS1, 1)
    #pi.write(CS1, 0)
    spi.xfer([0x09, 0x00]) # disables decode mode
    #pi.write(CS1, 1)
    #pi.write(CS1, 0)
    spi.xfer([0x0b, 0x07]) # sets scan limit to 7
    #pi.write(CS1, 1)
    #pi.write(CS1, 0)
    spi.xfer([0x0a, 0x09]) # sets brightness, minimum 0x00, max 0x0f
    #pi.write(CS1, 1)
    #pi.write(CS1, 0)
    
    rows = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08]
    bitmap = zero
    
    for i in range(8):
        #pi.write(CS1, 0)
        spi.xfer([rows[i], bitmap[i]])
        #pi.write(CS1, 1)
        time.sleep(0.1)
    
    time.sleep(3)
    
    for i in range(8):
        #pi.write(CS1, 0)
        spi.xfer([rows[i], 0b00000000])
        #pi.write(CS1, 1)
        time.sleep(0.1)
    time.sleep(1)
    spi.close()
    
testMatrix() # commented out for now
#print("hello world")
'''
# MATRIX CLASS DEFINITION
class matrix:
    def __init__(self, bus, port, CS):
        self.spi = spidev.SpiDev() # creates spi object
        self.rows = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08] # addresses for rows
        self.spi.open(bus, port) # opens the  spi port
        self.spi.max_speed_hz = 10000000 #same max speed (10MHz) for all MAX7219 displays
        self.cs = CS
        print(f"chip select is {self.cs}")
    
    def startup(self):
        pi.write(self.cs, 0)
        time.sleep(0.01)
        self.spi.xfer([0x0c, 0x01]) # disables shutdown mode
        self.spi.xfer([0x0f, 0x00]) # disables display test
        self.spi.xfer([0x09, 0x00]) # disables decode mode
        self.spi.xfer([0x0b, 0x07]) # sets scan limit to 7
        self.spi.xfer([0x0a, 0x09]) # sets brightness, minimum 0x00, max 0x0f
        self.clearDisplay() #clears the display
        time.sleep(0.01)
        pi.write(self.cs, 1)
    
    def setDisplay(self, bitmap):
        pi.write(self.cs, 0)
        time.sleep(0.01)
        for i in range(8):
            self.spi.xfer([self.rows[i], bitmap[i]])
        time.sleep(0.01)
        pi.write(self.cs,1)
    
    def clearDisplay(self):
        pi.write(self.cs, 0)
        time.sleep(0.01)
        for i in range(8):
            self.spi.xfer([self.rows[i], 0b00000000])
        time.sleep(0.01)
        pi.write(self.cs,1)
        
'''
'''
mat1 = matrix(0,0, CS1)
mat2 = matrix(0,0, CS2)
#mat3 = matrix(0,0, CS3)
#mat4 = matrix(0,0, CS4)
#mat5 = matrix(0,0, CS4)
#mat6 = matrix(0,0, CS5)
#mat7 = matrix(0,0, CS6)
#mat8 = matrix(0,0, CS7)

mat1.startup()
mat2.startup()
#mat3.startup()
#mat4.startup()
#mat5.startup()
#mat6.startup()
#mat7.startup()
#mat8.startup()

mat1.setDisplay(zero)
mat2.setDisplay(one)
#mat3.setDisplay(two)
'''

print("program end reached")