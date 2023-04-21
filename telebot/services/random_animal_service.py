import animality

from telebot.services.services import RandomAnimalAbstract


class RandomAnimalService(RandomAnimalAbstract):
    async def get_random_animal_image_url(self) -> str:
        response = await animality.random()
        image = response.image
        return image


