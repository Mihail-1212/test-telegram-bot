from typing import List, Dict

from telebot.models import UserPoll
from telebot.services.services import CreatePollsAbstract


class NotFoundPollError(Exception):
    """
    Exception if poll was not found
    """
    pass


class PollExistError(Exception):
    """
    Exception if poll already exists
    """
    pass


class CreatePollsService(CreatePollsAbstract):
    def __init__(self):
        self._polls: Dict[str, UserPoll] = {}

    def get_poll_by_id(self, poll_id: str) -> UserPoll:
        try:
            search_poll: UserPoll = self._polls[poll_id]
            return search_poll
        except KeyError as _exc:
            raise NotFoundPollError()
        raise NotImplementedError()

    def create_user_poll(self, poll_id: str, question: str, options: List[str], owner_id: str) -> str:
        # Create new instance of polls
        user_poll = UserPoll(
            poll_id=poll_id,
            question=question,
            options=options,
            owner_id=owner_id
        )

        if poll_id in self._polls:
            raise PollExistError()

        # Append new poll to dict of polls
        self._polls[poll_id] = user_poll

        # Return poll id
        return poll_id
