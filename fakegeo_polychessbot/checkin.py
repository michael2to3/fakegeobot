import logging

from aiocron import crontab
from cronaction import CronAction
from user import User


class CheckIn:
    logger: logging.Logger
    _to_username = "@poly_chess_bot"

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def send_live_location(self, user: User):
        name = self._to_username
        return await CronAction.send_live_location(user, name)

    def run(self, user: User):
        cron = user._info._schedule
        name = self._to_username
        id = user._info._chat_id

        async def _cron_action():
            self.logger.debug(f"Trigger cron from {id} to {name}")
            await CronAction.send_live_location(user, name)

        return crontab(cron, func=_cron_action, start=True)

    def pass_cron(self):
        schedule = "30 18 * * 6"
        return crontab(schedule, start=False)
