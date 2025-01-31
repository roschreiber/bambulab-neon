import time
import board
import displayio
import rgbmatrix
import framebufferio
import os
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font

'''
IMPORTANT:

This is just a web demo and it does not really do anything, its just here to show you the UI! 
Use the real code which you can find in my github repo:

https://github.com/roschreiber/bambulab-neon

'''

displayio.release_displays()
matrix = rgbmatrix.RGBMatrix(
    width=64, height=32, bit_depth=4,
    rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
    addr_pins=[board.A5, board.A4, board.A3, board.A2],
    clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1
)
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

font = bitmap_font.load_font("font5x8.bdf")
home_icon = displayio.OnDiskBitmap("gifs/unknown/frame_00.bmp")
splash = displayio.Group()
display.root_group = splash

def update_display(status, bed_temp, nozzle_temp):
    while len(splash) > 0:
        splash.pop()
    
    home_tilegrid = displayio.TileGrid(home_icon, pixel_shader=home_icon.pixel_shader, x=40, y=0)
    splash.append(home_tilegrid)
    
    status_text = label.Label(
        font,
        text=f"S:{status}",
        color=0xFFFFFF,
        x=2,
        y=8
    )
    splash.append(status_text)
    
    temp_text = label.Label(
        font,
        text=f"B{bed_temp}",
        color=0xFF0000,
        x=2,
        y=24
    )
    splash.append(temp_text)
    
    nozzle_text = label.Label(
        font,
        text=f"N{nozzle_temp}",
        color=0x00FF00,
        x=34,
        y=24
    )
    splash.append(nozzle_text)

if __name__ == '__main__':
    print('Starting Display Monitor')
    try:
        while True:
            status = "OK"
            bed_temp = 60
            nozzle_temp = 200
            
            update_display(status, bed_temp, nozzle_temp)
            display.refresh()
            
            print(f'Status: {status}, Bed: {bed_temp}, Nozzle: {nozzle_temp}')
            
            time.sleep(5)
    
    finally:
        print('Stopping Display Monitor')