import random
from animals import Animals

from telebot.services.services import RandomAnimalAbstract


class RandomAnimalService(RandomAnimalAbstract):
    async def get_random_animal_image_url(self) -> str:
        # List of available options
        options = ("cat", "dog", "panda", "kangaroo")
        # Get animal
        animal = Animals(random.choice(options))
        # Get animal image
        image = animal.image()
        return image


