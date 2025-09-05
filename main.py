from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
import uinput
import json
import os
import sys

events = (
    # d-pad (Directional Pad)
    uinput.BTN_DPAD_UP,
    uinput.BTN_DPAD_DOWN,
    uinput.BTN_DPAD_LEFT,
    uinput.BTN_DPAD_RIGHT,
    
    # action buttons (A, B, X, Y)
    uinput.BTN_A,
    uinput.BTN_B,
    uinput.BTN_X,
    uinput.BTN_Y,
    
    # shoulder buttons (LB and RB)
    uinput.BTN_TL, # Left Bumper (LB)
    uinput.BTN_TR, # Right Bumper (RB)
    
    # triggers (LT and RT)
    uinput.ABS_Z + (0, 255, 0, 0),  # Left Trigger (LT)
    uinput.ABS_RZ + (0, 255, 0, 0),  # Right Trigger (RT)
    
    # thumb buttons (clicking the analog sticks)
    uinput.BTN_THUMBL,
    uinput.BTN_THUMBR,
    
    # start and back buttons
    uinput.BTN_START,
    uinput.BTN_SELECT,
    
    # left analog stick
    uinput.ABS_X + (0, 255, 0, 0),
    uinput.ABS_Y + (0, 255, 0, 0),
    
    # right analog stick
    uinput.ABS_RX + (0, 255, 0, 0),
    uinput.ABS_RY + (0, 255, 0, 0),
)

try:
    device = uinput.Device(events, vendor=0x045E, product=0x028E, version=0x110, name="Microsoft Xbox 360 Controller")
    print("Virtual Xbox 360 Controller created successfully.")
except Exception as e:
    print(f"Error creating uinput device: {e}")
    sys.exit(1)

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket connection established.")

    try:
        while True:
            text = await websocket.receive_text()
            data = json.loads(text)

            # d-pad
            device.emit(uinput.BTN_DPAD_UP, data["btn_dpad_up"])
            device.emit(uinput.BTN_DPAD_DOWN, data["btn_dpad_down"])
            device.emit(uinput.BTN_DPAD_LEFT, data["btn_dpad_left"])
            device.emit(uinput.BTN_DPAD_RIGHT, data["btn_dpad_right"])

            # action buttons
            device.emit(uinput.BTN_A, data["btn_a"])
            device.emit(uinput.BTN_B, data["btn_b"])
            device.emit(uinput.BTN_X, data["btn_x"])
            device.emit(uinput.BTN_Y, data["btn_y"])
            
            # shoulder buttons
            device.emit(uinput.BTN_TL, data["btn_tl"])
            device.emit(uinput.BTN_TR, data["btn_tr"])
            
            # triggers
            device.emit(uinput.ABS_Z, data["abs_z"])
            device.emit(uinput.ABS_RZ, data["abs_rz"])
            
            # start / back buttons
            device.emit(uinput.BTN_START, data["btn_start"])
            device.emit(uinput.BTN_SELECT, data["btn_select"])

            # left stick
            device.emit(uinput.ABS_X, data["abs_x"])
            device.emit(uinput.ABS_Y, data["abs_y"])

            # right stick
            device.emit(uinput.ABS_RX, data["abs_rx"])
            device.emit(uinput.ABS_RY, data["abs_ry"])
            
            print(data)

    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        print("WebSocket connection closed.")

app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

# sudo .venv/bin/python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
