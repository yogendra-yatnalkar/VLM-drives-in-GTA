import json 
import numpy as np
import cv2
import pyautogui
import pydirectinput
import time
import boto3
import base64
import multiprocessing

from bedrock_utils import invoke_claude_3_multimodal
from prompt import driving_prompt_base

def get_coordinates():
    screen = np.array(pyautogui.screenshot())
    x0, y0, w, h = cv2.selectROI(screen)
    # returns the top-left corner coordinates and the width and height of the roi
    cv2.destroyAllWindows()
    x1 = x0 + w
    y1 = y0 + h
    return (x0, y0, x1, y1)

def get_selected_area(x0, y0, x1, y1):
    screen = np.array(pyautogui.screenshot())
    screen = screen[y0:y1, x0:x1]
    screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)

    return screen

def key_press_process(keys_to_press):
    while(True):
        for key in keys_to_press.split(","):
            pydirectinput.press(key)
        time.sleep(0.04)

if __name__ == "__main__":
   
    # Initialize the Amazon Bedrock runtime client
    client = boto3.client(
        service_name="bedrock-runtime", region_name="us-east-1"
    )

    top_left_x, top_left_y, bottom_right_x, bottom_right_y = get_coordinates()
    cnt = 5
    for i in range(5):
        print("Starting in: ", cnt)
        cnt -= 1
        time.sleep(1)

    previous_inputs = ["s,a","s,a","w,d","w","w"]
    previous_process = None
    cnt = 0
    while cnt < 300:
        screen = get_selected_area(top_left_x, top_left_y, bottom_right_x, bottom_right_y)

        cnt += 1
        print("cnt: ", cnt)

        # convert the grabbed screen to base64 image
        # Encode the image to base64
        _, im_arr = cv2.imencode('.jpg', screen)  # im_arr: image in Numpy one-dim array format.
        # im_bytes = im_arr.tobytes()
        base64_img = base64.b64encode(im_arr).decode()

        # update the driving prompt
        driving_prompt = driving_prompt_base.format(prev_presses = previous_inputs)

        # invoke the VLM
        output = invoke_claude_3_multimodal(client, prompt=driving_prompt, base64_image_data=base64_img)

        # key-to-press
        output_string =  output['content'][0]['text']
        print(output_string)

        json_string = "{" + output_string[output_string.find('{') + 1: output_string.rfind('}')] + "}"

        output_dict = json.loads(json_string)
        key_to_press = output_dict['output']
        print(key_to_press)

        # # press the key using pydirectinput
        # for i in range(3):
        #     for key in key_to_press.split(","):
        #         pydirectinput.press(key)

        # Stop the previous process if it exists
        if previous_process and previous_process.is_alive():
            previous_process.terminate()  # Terminate the previous process
            print(">>>>> Process terminated....")

        # Run key press logic in a separate process
        previous_process = multiprocessing.Process(target=key_press_process, args=(key_to_press,))
        previous_process.start()

        previous_inputs.pop(0)
        previous_inputs.append(key_to_press)
        print("updated list: ", previous_inputs)