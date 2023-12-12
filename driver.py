import time
from PIL import Image
from playwright.sync_api import sync_playwright
from io import BytesIO

sleep_time = 2

class Driver:
    def __init__(self) -> None:
        context = sync_playwright().start().chromium.launch_persistent_context("", headless=False, ignore_https_errors=True, args=["--disable-extensions-except=./vimium-master", "--load-extension=./vimium-master"], record_video_dir="videos")
        self.page = context.new_page()
        self.page.on("console", self.handle_console_message)
        self.page.set_viewport_size({"width": 1080, "height": 720})
        
    def type(self, value):
        time.sleep(sleep_time)
        self.page.keyboard.type(value)
        
    def click(self, text):
        time.sleep(sleep_time)
        self.page.keyboard.type(text=text)
        
    def navigate(self, url):
        self.page.goto(url)
        
    def capture_screenshot(self):
        time.sleep(5)
        self.page.keyboard.press("Escape")
        self.page.keyboard.type("f")
        screencap = self.page.screenshot()
        screenshot = Image.open(BytesIO(screencap)).convert("RGB")
        return screenshot
    
    def execute_actions(self, actions):
        for action in actions:
            if action['action'] == 'click':
                self.click(action['text'])
            elif action['action'] == 'type':
                self.type(action['text'])
                
    def handle_console_message(self, message):
        if message.type == "log":
            print(f"Console.log: {message.text}")
        elif message.type == "warning":
            print(f"Console warning: {message.text}")
        elif message.type == "error":
            print(f"Console error: {message.text}")