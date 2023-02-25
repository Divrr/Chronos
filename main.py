import hikari
import lightbulb
import secret
import time

bot = lightbulb.BotApp(token=secret.token())

class Timer:
    def __init__(self):
        self.timers = {}

    def start_timer(self, user_id):
        if user_id not in self.timers:
            self.timers[user_id] = time.monotonic()

    def check_timer(self, user_id):
        if user_id in self.timers:
            time_elapsed = time.monotonic() - self.timers[user_id]
            return time_elapsed
        return None

    def stop_timer(self, user_id):
        if user_id in self.timers:
            time_elapsed = time.monotonic() - self.timers[user_id]
            del self.timers[user_id]
            return time_elapsed
        return None

timer = Timer()

@bot.command
@lightbulb.command('timer', 'start/stop a personal timer')
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def timer_command(ctx):
    pass

@timer_command.child
@lightbulb.command('start', 'start timer')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def start_timer(ctx):
    """Starts the timer."""
    timer.start_timer(ctx.author.id)
    await ctx.respond("Timer started.")

@timer_command.child
@lightbulb.command('check', 'check timer')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def check_timer(ctx):
    """Stops the timer and reports the elapsed time."""
    time_elapsed = timer.check_timer(ctx.author.id)
    if time_elapsed is None:
        await ctx.respond("Timer not started.")
    else:
        await ctx.respond(f"Time elapsed: {time_elapsed:.2f} seconds.")

@timer_command.child
@lightbulb.command('stop', 'stop timer')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def stop_timer(ctx):
    """Stops the timer and reports the elapsed time."""
    time_elapsed = timer.stop_timer(ctx.author.id)
    if time_elapsed is None:
        await ctx.respond("Timer not started.")
    else:
        await ctx.respond(f"Time elapsed: {time_elapsed:.2f} seconds.")

bot.run()
