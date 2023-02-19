import openai
import random
import pyttsx3

openai.api_key = ""
model = "text-davinci-003"
rng = random.randint(0, 5)

engine = pyttsx3.init()
voices = engine.getProperty('voices')
rate = engine.getProperty('rate')
engine.setProperty('voice', voices[2].id)
engine.setProperty('rate', 220)


greetings = ["Hey", "Good Day! How may I be of assistance", "What's up?",
             "Yo bro", "Hello, how are you today?", "Hello there. How can I help you today?"]
goodbyes = ["Until next time", "Sayonara", "Glad to be of service", "Goodbye", "See you", "Bye"]
exit_inputs = ["Goodbye Lumen", "That will be all", "Goodnight Lumen", "Go to sleep"]
initial_request = "From now on you are called Lumen, keep answers as short as possible."


def main():
    run()


def run():
    try:
        openai.api_key = input("API Key: ")
        engine.say(greetings[rng])
        engine.runAndWait()
        question = input(greetings[rng])
        while True:
            if question in exit_inputs:
                print(goodbyes[rng])
                engine.say(goodbyes[rng])
                engine.runAndWait()
                break
            else:
                (res, usage) = request(question, initial_request)
                print(res)
                engine.say(res)
                engine.runAndWait()
                print("Tokens used: " + str(usage))
                question = input()

    except KeyboardInterrupt:
        print("Exiting Program")


def request(question, init):
    prompt = init + question
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=500,
        temperature=1.0,
    )
    return str.strip(response['choices'][0]['text']), response['usage']['total_tokens']


if __name__ == "__main__":
    main()