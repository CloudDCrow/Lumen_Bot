import openai
import pyttsx3
import threading
import speech_recognition as sr

from actions.music_player import *
from actions.reminders import *

# OpenAPI key is needed to ask Lumen question.
# Not needed for requests.
openai.api_key = ""
model = "text-davinci-002"

# Text-to-speech
engine = pyttsx3.init()
voices = engine.getProperty('voices')
rate = engine.getProperty('rate')
engine.setProperty('voice', voices[2].id)
engine.setProperty('rate', 210)

# Speech-recognizer
speech = sr.Recognizer()
mic = sr.Microphone(device_index=1)

# Music-player
pygame.init()

# Random number, used to get a random greeting/goodbye from Lumen.
rng = random.randint(0, 5)

# Words that are needed in a sentence for Lumen to respond
# Sometimes it hears "woman" or something else instead of "Lumen"
recognition_keywords = ["lumen", "woman", "human", "little man",
                        "two men", "blue and", "blue man", "newman",
                        "aluminum", "roman"]

# Lumen's greetings and goodbyes
greetings = ["Hey", "Good Day! How may I be of assistance", "What's up?",
             "Yo bro", "Hello, how are you today?", "Hello there. How can I help you today?"]
goodbyes = ["Until next time", "Sayonara", "Glad to be of service", "Goodbye", "See you", "Bye"]

# Saying "Lumen" and one of the exit_inputs shuts down the program.
exit_inputs = ["goodbye", "that will be all", "good night", "shutdown"]

# Prompt for AI
initial_request = "From now on you are called Lumen, keep answers as short as possible."


def main():
    lumen_speak(get_greeting())
    playlist_on = False

    while True:
        if playlist_on and not check_if_playing():
            play_random_song("songs/")

        question = get_question()

        # Checks input question
        if question is None:
            continue
        if question in exit_inputs:
            lumen_speak(get_goodbye())
            print("Exiting program now")
            break
        elif "set" in question and "timer" in question:
            if "minutes" in question:
                minutes_index = question.index("minutes")
                minutes = int(question[question.rfind(" ", 0, minutes_index-1) + 1:minutes_index])
                lumen_speak(f"Setting timer for {minutes} minutes")
                print("Timer set")
                timer = threading.Timer(minutes*60, timer_callback)
                timer.start()
            elif "minute" in question:
                lumen_speak("Setting timer for one minute")
                print("Timer set")
                timer = threading.Timer(60, timer_callback)
                timer.start()
            elif "seconds" in question:
                seconds_index = question.index("seconds")
                seconds = int(question[question.rfind(" ", 0, seconds_index-1) + 1:seconds_index])
                lumen_speak(f"Setting timer for {seconds} seconds")
                print("Timer set")
                timer = threading.Timer(seconds, timer_callback)
                timer.start()
        elif "play" in question and "random" in question:
            lumen_speak("Playing a random song")
            folder_path = "songs/"
            play_random_song(folder_path)
            print("Playing song")
        elif "stop" in question and "playlist" in question:
            lumen_speak("Stopping a playlist")
            playlist_on = not playlist_on
            print("Playlist off")
            stop_song()
        elif "playlist" in question:
            lumen_speak("Playing a playlist")
            playlist_on = not playlist_on
            print("Playlist on")
        elif "add reminder" in question:
            new_reminder = question[12:]
            reminders_list = load_reminders()
            add_reminder(reminders_list, new_reminder)
            lumen_speak(new_reminder + ", added to reminders")
        elif "remove reminder" in question:
            reminders_list = load_reminders()
            remove_reminder(reminders_list, 0)
            lumen_speak("Reminder removed")
        elif "clear" in question and "reminders" in question:
            reminders_list = load_reminders()
            clear_reminders(reminders_list)
            lumen_speak("Reminders cleared")
        elif "reminders" in question:
            reminders_list = load_reminders()
            if len(reminders_list) == 0:
                lumen_speak("No reminders")
            lumen_speak(reminders_list)
        else:
            prompt = initial_request + " " + question
            try:
                response, tokens_used = request(prompt)
                lumen_speak(response)
            except openai.error.AuthenticationError:
                lumen_speak("No API key")
                continue
            print("Tokens used: " + str(tokens_used))


def get_question():
    audio = None
    with mic as source:
        speech.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening")
        try:
            audio = speech.listen(source, timeout=8, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            print("Timeout occurred while listening.")
        except sr.UnknownValueError:
            print("Unable to recognize speech.")
        except sr.RequestError as e:
            print(f"Error: {str(e)}")

        print("Done Listening")

    if audio is None:
        return None

    try:
        question = speech.recognize_google(audio)
        print(question)
        for keyword in recognition_keywords:
            if keyword in question.lower():
                return question.lower().replace(keyword, "").strip()
        if "stop please" in question.lower():
            stop_song()
            return None
        else:
            return None
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print("Error: {0}".format(e))
    return None


def lumen_speak(text):
    engine.startLoop(False)
    engine.say(text)
    engine.iterate()
    engine.endLoop()


def request(question):
    response = openai.Completion.create(
        engine=model,
        prompt=question,
        max_tokens=100,
        temperature=1.0,
    )
    return str.strip(response['choices'][0]['text']), response['usage']['total_tokens']


def get_greeting():
    return random.choice(greetings)


def get_goodbye():
    return random.choice(goodbyes)


def timer_callback():
    lumen_speak("Ding Ding Ding Ding, Ding Ding Ding Ding, Timer is done!")


if __name__ == "__main__":
    main()
