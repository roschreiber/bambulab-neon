import time
import board
import displayio
import os
import rgbmatrix
import framebufferio
from adafruit_display_text import label
import bambulabs_api as bl
from adafruit_bitmap_font import bitmap_font

# from blinka_displayio_pygamedisplay import PyGameDisplay

'''
This part is for Bambu Printer Connection.
Enable LAN only Mode to find your Access Code & IP Address
Your Printer's Serial Number can be found under the "Device" tab
'''
IP = 'xxx.xxx.xxx.xxx'
SERIAL = 'xxxxxx'
ACCESS_CODE = 'xxxxxx'
env = os.getenv("env", "prod")

displayio.release_displays()
matrix = rgbmatrix.RGBMatrix(
    width=64, height=32, bit_depth=4,
    rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
    addr_pins=[board.A5, board.A4, board.A3, board.A2],
    clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1
)
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

framecount = 0

font = bitmap_font.load_font("font5x8.bdf")

splash = displayio.Group()
display.root_group = splash

homing_frames = []
for i in range(2):
    frame = displayio.OnDiskBitmap(f"gifs/homing/frame_{i:02d}.bmp")
    homing_frames.append(frame)

probing_frames = []
for i in range(8):
    frame = displayio.OnDiskBitmap(f"gifs/probing/frame_{i:02d}.bmp")
    probing_frames.append(frame)

printing_frames = []
for i in range(7):
    frame = displayio.OnDiskBitmap(f"gifs/printing/frame_{i:02d}.bmp")
    printing_frames.append(frame)

unknown_frames = []
for i in range(2):
    frame = displayio.OnDiskBitmap(f"gifs/unknown/frame_{i:02d}.bmp")
    unknown_frames.append(frame)

idle_frames = []
for i in range(6):
    frame = displayio.OnDiskBitmap(f"gifs/idle/frame_{i:02d}.bmp")
    idle_frames.append(frame)

cleaning_frames = []
for i in range(7):
    frame = displayio.OnDiskBitmap(f"gifs/cleaning/frame_{i:02d}.bmp")
    cleaning_frames.append(frame)

def update_display(status, bed_temp, nozzle_temp, is_homing, is_printing, is_probing, is_unknown, is_idle, is_cleaning):
    global framecount 
    while len(splash) > 0:
        splash.pop()
    
    status_text = label.Label(
        font,
        text=f"S:{status[:3]}",
        color=0xFFFFFF,
        x=2,
        y=8
    )
    splash.append(status_text)
    
    temp_text = label.Label(
        font,
        text=f"B{int(float(bed_temp))}",
        color=0xFF0000,
        x=2,
        y=24
    )
    splash.append(temp_text)
    
    nozzle_text = label.Label(
        font,
        text=f"N{int(float(nozzle_temp))}",
        color=0x00FF00,
        x=34,
        y=24
    )
    splash.append(nozzle_text)
    
    if is_homing:
        frame = homing_frames[framecount % len(homing_frames)]
        frame_tilegrid = displayio.TileGrid(frame, pixel_shader=frame.pixel_shader, x=40, y=0)
        splash.append(frame_tilegrid)
        framecount += 1
    elif is_probing:
        frame = probing_frames[framecount % len(probing_frames)]
        frame_tilegrid = displayio.TileGrid(frame, pixel_shader=frame.pixel_shader, x=40, y=0)
        splash.append(frame_tilegrid)
        framecount += 1
    elif is_printing:
        frame = printing_frames[framecount % len(printing_frames)]
        frame_tilegrid = displayio.TileGrid(frame, pixel_shader=frame.pixel_shader, x=40, y=0)
        splash.append(frame_tilegrid)
        framecount += 1
    elif is_idle:
        frame = idle_frames[framecount % len(idle_frames)]
        frame_tilegrid = displayio.TileGrid(frame, pixel_shader=frame.pixel_shader, x=40, y=0)
        splash.append(frame_tilegrid)
        framecount += 1
    elif is_cleaning:
        frame = cleaning_frames[framecount % len(cleaning_frames)]
        frame_tilegrid = displayio.TileGrid(frame, pixel_shader=frame.pixel_shader, x=40, y=0)
        splash.append(frame_tilegrid)
        framecount += 1
    elif is_unknown:
        frame = unknown_frames[framecount % len(unknown_frames)]
        frame_tilegrid = displayio.TileGrid(frame, pixel_shader=frame.pixel_shader, x=40, y=0)
        splash.append(frame_tilegrid)
        framecount += 1
    
    display.refresh()


if __name__ == '__main__':
    print('Starting Bambulab Display Monitor')
    printer = bl.Printer(IP, ACCESS_CODE, SERIAL)
    printer.connect()

    try:
        while True:
            raw_status = printer.get_state()
            status = bl.PrintStatus(raw_status) 
            status2 = printer.get_current_state()
            
            is_homing = status2 == bl.PrintStatus.HOMING_TOOLHEAD or status2 == bl.PrintStatus.SWEEPING_XY_MECH_MODE
            is_printing = status2 == bl.PrintStatus.PRINTING
            is_probing = status2 == bl.PrintStatus.AUTO_BED_LEVELING
            is_unknown = status == bl.PrintStatus.UNKNOWN
            is_idle = raw_status == "IDLE"
            is_cleaning = status2 == bl.PrintStatus.CLEANING_NOZZLE_TIP

            if is_idle:
                is_printing = False
            
            bed_temp = printer.get_bed_temperature()
            nozzle_temp = printer.get_nozzle_temperature()
            
            update_display(raw_status, bed_temp, nozzle_temp, is_homing, is_printing, is_probing, is_unknown, is_idle, is_cleaning)
            
            if env == "debug":
                print(f'Statuses: {status} | {status2}')
                print(f'Printer status: {raw_status}, Bed: {bed_temp}, Nozzle: {nozzle_temp}')
            
            time.sleep(5)
        
    finally:
        printer.disconnect()