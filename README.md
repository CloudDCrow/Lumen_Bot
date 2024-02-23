# Lumen_Bot

A robot using OpenAI for communication.

## How it Works

Upon starting the program, the robot follows a sequence of actions:

1. **Greetings:**
   The robot initiates with a friendly greeting.

2. **Listening for Requests:**
   It then enters a listening mode, awaiting user input.

3. **Command Recognition:**
   The robot responds only to commands that include the keyword "Lumen".

   - For instance, to set a timer, the user would say, "Lumen, set a timer for 5 minutes."
   - The robot's response would be, "Setting timer for 5 minutes." It then awaits the next input.

5. **Custom Commands:**
   The robot is designed to perform specific custom commands, such as playing songs or setting timers.

   - Example: "Lumen, play a random song."
   - Example: "Lumen, set a timer for 10 minutes."

6. **General Knowledge Queries:**
   For any other inquiries, the robot utilizes the OpenAI API to fetch responses.

   - Example: "What is 20x20, Lumen?"
   - In this case, as it's not a custom command, the program consults OpenAI for the answer.

(For Lumen Bot for Raspberry Pi click here: https://github.com/CloudDCrow/lumen4raspberry)
