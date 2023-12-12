import time
from vision import determine_next_action
from driver import Driver

def run_agent():
    driver = Driver()
    driver.navigate("https://app.aiqualify.io/auth/sign-in/")
    current_action = "start"
    actions = []
    
    while current_action != "finish" and current_action != "error":
        time.sleep(1.5)
        screenshot = driver.capture_screenshot()
        
        task = """
        Your task is to follow the following series of steps:
        1. Sign into the service. The email is "info@usenucleus.io". The password is "123password".
        2. Once you are signed into the service, click the Inbound tab on the left. 
        3. Next change the greeting to "Hey there, is the QA GPT writing this greeting. How can I help you?"
        4. Lastly, click the Save button. After you have completed this step, your task is complete.
        """
        
        next_actions = determine_next_action(
            task=task,
            screenshot=screenshot,
            previous_actions=actions
        )
        driver.execute_actions(actions=next_actions)
        
        current_action = next_actions[len(next_actions) - 1]["action"]
        actions.extend(next_actions)


if __name__ == "__main__":
    run_agent()