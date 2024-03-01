import json


def load_reminders():
    try:
        with open('reminders.json', 'r') as file:
            reminders = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        reminders = []
        print("File not found")
    return reminders


def save_reminders(reminders):
    with open('reminders.json', 'w') as file:
        json.dump(reminders, file)


def add_reminder(reminders, new_reminder):
    reminders.append(new_reminder)
    save_reminders(reminders)


def remove_reminder(reminders, index):
    if 0 <= index < len(reminders):
        del reminders[index]
        save_reminders(reminders)


def clear_reminders(reminders):
    reminders.clear()

    with open('reminders.json', 'w') as file:
        json.dump(reminders, file)

    return reminders


def display_reminders(reminders):
    for i, reminder in enumerate(reminders, start=1):
        print(f"{i}. {reminder}")