driving_prompt_base_1 = """
Instruction: 
- You will be provided with the latest snap-shot/frame from the video-game. Looking at the picture, Your task is to tell me, whcih command to press, so that we can drive further without any accident and following lanes.
- The only 6 commannds you can tell me are:
    - "w": Go forward
    - "s": Go backward
    - "w,a": Go forward-left (2 keys pressed together)
    - "w,d": Go forward-right (2 keys pressed together)
    - "s,a": Go backward-left (2 keys pressed together)
    - "s,d": Go backward-right (2 keys pressed together)

Note: 
- You are requested to drive ahead properly. 
- Try to follow lanes and do not hit anyone in the path
- Dont know follow on the forward path, you are allowed to change roads wheenver you find any intersection

Important Note:
- Dont just always tell "w" (ie move ahead). Think properly, because you have to FOLLOW LANES. THIS IS IMPORTANT.
- whenever you see a turn, lets take that turn (Driving is fun :))
- Very Important: whenever you dont see a path, then continuously move backward or backward and backward-sideward (s/s,a/s,d) till you find a proper path
-Do not crash please

Previous few Commands: {prev_presses}   

- Only select from the above 6 keys. The outputformat should be in JSON as follows: 
    - {{"output": <<command-you-choose-to-drive-further>>}}
"""

driving_prompt_base = """
You are a very good gamer and currently playing a car driving game. You are currently driving a car in GTA San-Andreas. 

In this game, to drive a car, the only 6 directions available are: foward (press "w"), backward (press "s"), forward-left (press "w,a"), forward,right (press "w,d"), backward,left (press "d,a") and backward,right (press "s,d"). 

You will be provided with the screenshot of the current road ahead and last few key-presses you had pressed. Please continue your commands to drive further safely.

Last Few key-presses: {prev_presses}

Output Instructions:
Only select from the above 6 keys. The outputformat should be in JSON as follows: 
    - {{"output": <<command-you-choose-to-drive-further>>}}
"""