import os
from dotenv import load_dotenv
from openai import OpenAI
from io import BytesIO
import base64
import json

load_dotenv()

prompt = """
You are a browser automation assistant. Your job is to determine the next course of action for the task given to you. The set of actions that you are able to take are click, type, wait, error, or finish.
- Select click as the next action when you believe you need to click something on the screen to best proceed with the given task
- Select type as the next action when you believe you need to type something to best proceed with the given task
- Select finish as the next action when you believe the given task has been successfully accomplished
- Select error as the next action when you believe you have run into an unrecoverable error
- Select wait as the next action when you believe you need to wait - for example if the page is loading

You will be given a screenshot of the current page you are on. You will also be given the previous actions you have taken.

To determine the best next action, break down your internal thought process into the following steps:

## Step 1
Create a list of steps you need to take to accomplish the given task from the current page. Make sure each step is thoroughly broken down into the simplest set of steps you need to take from this page

## Step 2
Next, take the first step from the list you have generated and determine which action (click, type, wait, error, or finish) you need to conduct in order to move forward with the given task. 
If you need to click something on the page, determine the string inside the yellow box that is attached to the item you want to click on. Only determine the string in the yellow box, do not include any other strings.
If you need to type something on the page, determine what text you need to type.

## Step 3
Finally, take the action you have selected from step 2, an explanation of why you have selected this action (keep this very brief), the string inside the yellow box attached to the item you want to click on from step 2 (if needed), and the text (if needed) from step 2, and return them to the user in the following JSON format: [{ "action": "ACTION_GOES_HERE", "text": "VALUE_HERE", "explanation": "EXPLANATION_GOES_HERE" }]. All text (including the selected yellow character sequence can go into the text property of the json). You must return JSON only with no other fluff or bad things will happen. Do not return the JSON inside a code block.

Lastly, remember that in order to type something into an input, you must first select the input by clicking it. In this edge case when you need to follow up on an click action with a type action, return both actions in the array as follows: [{ "action": "click", "text": "VALUE_HERE", "explanation": "EXPLANATION_GOES_HERE" }, { "action": "type", "text": "VALUE_HERE", "explanation": "EXPLANATION_GOES_HERE" }]

As a reminder, never ever return anything except JSON. If you return stuff other than JSON, the world will catch on fire and humanity will die. NEVER return the internal steps you thought about to arrive at the JSON. Only return the JSON.
"""

def determine_next_action(task, screenshot, previous_actions):
    W, H = screenshot.size
    image = screenshot.resize((1080,  int(1080 * H  / W)))
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    encoded_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
    
    openAI = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    previous_actions_str = ""
    for action in previous_actions:
        previous_actions_str += f"The action: {action['action']}. Explanation of why you took that action: {action['explanation']}\n\n"
    
    messages = []
    messages.append({"role": "system", "content": prompt})
    messages.append({"role": "user", "content": [
        {"type": "text", "text": f"Your task is: {task}. The previous actions you took are: {previous_actions_str}\n Determine the next best action to take given a screenshot of the current page you are on. Remember to respond in JSON only or otherwise bad things will happen."},
        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
    ]})
    
    chat_response = openAI.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=messages,
        max_tokens=100
    )
    
    content = chat_response.choices[0].message.content
    print(content)
    print(f"Total number of tokens used: {chat_response.usage.total_tokens}")
    print(f"Number of prompt tokens: {chat_response.usage.prompt_tokens}")
    print(f"Number of completion tokens: {chat_response.usage.completion_tokens}")
    
    try:
        json_response = json.loads(content)
        return json_response
    except json.JSONDecodeError:
        print("Invalid json error")