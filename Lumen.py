import openai
import random

openai.api_key = ""
model = "text-davinci-003"
rng = random.randint(0, 5)

greetings = ["Hey. What is on your mind?", "Good Day! How may I be of assistance", "Wats up?",
             "Yo", "Hello, how are you today?", "Hello there. How can I help you today?"]
goodbyes = ["Until next time", "Sayonara", "Glad to be of service", "Goodbye", "See you", "Bye"]
exit_inputs = ["Goodbye Lumen", "That will be all", "Goodnight Lumen", "Go to sleep"]
initial_request = ["From now on you are called Lumen, and everytime you generate a response you need to add"
                   "'I Am Lumen' at the end"]


def main():
    run()


def run():
    try:
        openai.api_key = input("API Key: ")
        question = input(greetings[rng])
        while True:
            if question in exit_inputs:
                print(goodbyes[rng])
                break
            else:
                (res, usage) = request(question)
                print(res)
                print("Tokens used: " + str(usage))
                question = input()

    except KeyboardInterrupt:
        print("Exiting Program")


def request(question):
    response = openai.Completion.create(
        engine=model,
        prompt=question,
        max_tokens=500,
        temperature=0.6,
    )
    return str.strip(response['choices'][0]['text']), response['usage']['total_tokens']


if __name__ == "__main__":
    main()