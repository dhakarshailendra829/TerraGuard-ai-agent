import os
from datetime import datetime

class AlertDispatcher:
    def __init__(self):
        base_path = os.path.dirname(os.path.dirname(__file__))
        self.log_file = os.path.join(base_path, "logs", "alerts.log")

    def dispatch(self, message, risk_data):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        full_message = f"""
Time: {timestamp}
Level: {risk_data['level']}
Score: {risk_data['score']}

{message}
"""
        print(full_message)

        # Save to log
        # Change the open line to include encoding="utf-8"
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(full_message + "\n")