import pigpio

CS1 = 4
MISO = 9 # not used
MOSI = 10
SCLK = 11

pi = pigpio.pi()
if not pi.connected:
    print("pi not connected. exiting...")
    exit()
    
pi.bb_spi_open(CS1, MISO, MOSI, SCLK, 250000, 0)

bb_spi_xfer(CS1, [0b01010101])