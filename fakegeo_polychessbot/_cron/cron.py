import aiocron


class FloodException(BaseException):
    message: str
    timeout: int

    def __init__(self, message: str):
        self.message = message


class Cron:
    def __init__(self, callback, cron_expression, timeout=600):
        self.callback = callback
        self.cron_expression = cron_expression
        self.timeout = timeout
        self.validate_cron_expression()
        self.job = None

    def validate_cron_expression(self):
        cron_parts = self.cron_expression.split()
        if len(cron_parts) < 5:
            raise ValueError("Invalid cron expression")

        mins = cron_parts[0]
        if mins == "*":
            raise FloodException("Cron schedule is too frequent")

        if "-" in mins or "," in mins or "/" in mins:
            min_values = []
            if "-" in mins:
                min_range = list(map(int, mins.split("-")))
                min_values = list(range(min_range[0], min_range[1] + 1))
            elif "," in mins:
                min_values = list(map(int, mins.split(",")))
            elif "/" in mins:
                min_step = int(mins.split("/")[1])
                min_values = list(range(0, 60, min_step))

            if any(
                t2 - t1 < self.timeout / 60
                for t1, t2 in zip(min_values, min_values[1:])
            ):
                raise FloodException("Cron schedule is too frequent")

    async def start(self):
        if self.job is None:
            self.job = aiocron.crontab(
                self.cron_expression, func=self.callback, start=True
            )

    async def stop(self):
        if self.job:
            self.job.stop()
            self.job = None
