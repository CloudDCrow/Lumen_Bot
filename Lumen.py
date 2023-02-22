import openai
import random
import pyttsx3
import speech_recognition as sr

openai.api_key = ""
model = "text-davinci-003"
rng = random.randint(0, 5)

engine = pyttsx3.init()
voices = engine.getProperty('voices')
rate = engine.getProperty('rate')
engine.setProperty('voice', voices[2].id)
engine.setProperty('rate', 190)

speech = sr.Recognizer()
mic = sr.Microphone(device_index=1)

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
        while True:
            with mic as source:
                speech.adjust_for_ambient_noise(source, duration=0.8)
                print("listening")
                audio = speech.listen(source)
                print("done listening")

            try:
                question = speech.recognize_google(audio)
            except (sr.UnknownValueError, sr.RequestError) as e:
                print("Error: {0}".format(e))
                continue

            if question.lower() in [x.lower() for x in exit_inputs]:
                print(goodbyes[rng])
                print("Exiting program now")
                engine.say(goodbyes[rng])
                engine.runAndWait()
                break
            else:
                (res, usage) = request("\n" + question, initial_request)
                print(res)
                engine.say(res)
                engine.runAndWait()
                print("Tokens used: " + str(usage))

    except KeyboardInterrupt:
        print("Exiting Program")


def request(question, init):
    prompt = init + question
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=100,
        temperature=1.0,
    )
    return str.strip(response['choices'][0]['text']), response['usage']['total_tokens']


if __name__ == "__main__":
    main()
