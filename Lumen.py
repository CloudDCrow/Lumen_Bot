import openai
import random
import pyttsx3
import threading
import speech_recognition as sr

openai.api_key = ""
model = "text-davinci-002"
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
lumen_waiting = ["Dumbai dumbai dum", "br br", "Any questions?", "F.F f", "Zzz", "hyia hehehe"]
wait_counter = 0

# Sometimes saying "Lumen" is understood by the program as "woman" or "little man".
exit_inputs = ["goodbye lumen", "goodbye woman", "goodbye little man", "that will be all", "good night lumen",
               "good night woman", "good night little man", "go to sleep"]
initial_request = "From now on you are called Lumen, keep answers as short as possible."


def main():
    global wait_counter
    openai.api_key = input("API Key: ")
    lumen_speak(get_greeting())
    while True:
        if wait_counter > 1:
            lumen_speak("Ahhh, I'm bored, goodnight")
            break

        question = get_question()
        if question is None:
            wait_counter += 1
            continue
        if question in exit_inputs:
            lumen_speak(get_goodbye())
            print("Exiting program now")
            break
        elif "set" in question and "timer" in question:
            minutes_index = question.index("minutes")
            minutes = int(question[question.rfind(" ", 0, minutes_index-1) + 1:minutes_index])
            lumen_speak(f"Setting timer for {minutes} minutes")
            timer = threading.Timer(minutes*60, timer_callback)
            timer.start()
        else:
            prompt = initial_request + " " + question
            response, tokens_used = request(prompt)
            lumen_speak(response)
            print("Tokens used: " + str(tokens_used))
            wait_counter = 0


def request(question):
    response = openai.Completion.create(
        engine=model,
        prompt=question,
        max_tokens=100,
        temperature=1.0,
    )
    return str.strip(response['choices'][0]['text']), response['usage']['total_tokens']


def get_question():
    with mic as source:
        speech.adjust_for_ambient_noise(source, duration=0.6)
        print("listening")
        try:
            audio = speech.listen(source, timeout=5)
        except sr.WaitTimeoutError:
            print("speak")
            return None
        print("done listening")

    try:
        question = speech.recognize_google(audio)
        return question.lower()
    except sr.UnknownValueError:
        lumen_speak(get_waiting())
        return None
    except sr.RequestError as e:
        print("Error: {0}".format(e))
    return None


def lumen_speak(text):
    engine.say(text)
    engine.runAndWait()


def get_greeting():
    return random.choice(greetings)


def get_goodbye():
    return random.choice(goodbyes)


def get_waiting():
    return random.choice(lumen_waiting)


def timer_callback():
    lumen_speak("Ding Ding Ding Ding")


if __name__ == "__main__":
    main()
