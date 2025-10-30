from pyb import UART, Pin

# Make a serial port object from the UART class
ser = UART(3, 115200)



# Deconfigure default pins
Pin(Pin.cpu.B11,  mode=Pin.ANALOG)     # Set pin modes back to default
Pin(Pin.cpu.B10,  mode=Pin.ANALOG)

# Configure the selected pins in coordination with the alternate function table
Pin(Pin.cpu.C4,  mode=Pin.ALT, alt=7) # Set pin modes to UART matching column 7 in alt. fcn. table
Pin(Pin.cpu.C5, mode=Pin.ALT, alt=7)
