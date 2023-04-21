from typing import List


class UserPoll:
    type: str = "poll"

    def __init__(self, poll_id, question, options, owner_id):
        self.poll_id: str = poll_id             # ID опроса
        self.question: str = question           # Текст вопроса
        self.options: List[str] = [*options]    # "Распакованное" содержимое массива m_options в массив options
        self.owner_id: str = owner_id           # Владелец опроса
