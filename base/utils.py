import datetime
import random

def get_background():
    images = [f'bg{n}.jpg' for n in range(1, 9)]
    index = get_index(len(images))
    background_image = images[index]

    button_gradients = {
        'bg1.jpg': 'linear-gradient(90deg, #b07fa5, #c29ab6)',
        'bg2.jpg': 'linear-gradient(90deg, #7c9bb2, #9ab1c4)',
        'bg3.jpg': 'linear-gradient(90deg, #5f7e5c, #7a9b74)',
        'bg4.jpg': 'linear-gradient(90deg, #4a6177, #6a7e94)',
        'bg5.jpg': 'linear-gradient(90deg, #8e6e61, #a6897c)',
        'bg6.jpg': 'linear-gradient(90deg, #9b6d8c, #b58da5)',
        'bg7.jpg': 'linear-gradient(90deg, #6f8b68, #90a88a)',
        'bg8.jpg': 'linear-gradient(90deg, #92775d, #aa947b)',
    }

    button_gradient = button_gradients.get(background_image, 'linear-gradient(90deg, #007BFF, #4a90e2)')
    return background_image, button_gradient


def return_motto():
        HEADLINES = [
        "Let’s get started",
        "Today is a good day to grow",
        "Small steps, every day",
        "Build your routine",
        "Keep the streak alive",
        "Make today count",
        "You’re doing great",
        "Stay on track",
        "Progress starts now",
        "One habit at a time",
        "Consistency is key",
        "Let’s make progress",
        "Finish strong today",
        "Focus on what matters",
        "Keep going",
        "Show up for yourself",
        "You’ve got this",
        "Daily progress, daily power",
        "Discipline over motivation",
        "A better YOU starts today",
        "Memento vivente",
        "Memento mori"
    ]
        return HEADLINES[get_index(len(HEADLINES))]



def get_index(n=8):
    now = datetime.datetime.now()
    x = now.day + now.month + now.year
    return x%n