# Based on discord.py's basic bot example: https://github.com/Rapptz/discord.py/blob/master/examples/basic_bot.py 
# TODO:
#   - write tests?
#   - edit descriptions for help command
#   - implement days to or days since
#   - implement poll

import discord
from discord.ext import commands
import random
import pathlib
import logging
import commons.operations.dice_roll as dr

discord.utils.setup_logging()
LOGGER = logging.getLogger(__name__)
MAX_OUTPUT_LENGTH = 2000

description = '''This bot implements functionalities that may be interesting or useful for the horde'''

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)


@bot.event
async def on_ready():
    LOGGER.info(f'Logged in as {bot.user} (ID: {bot.user.id})\n------')


@bot.command(description="Roll dice and calculate")
async def roll(ctx, expr: str):
    """Evaluates the expression, rolling any dice provided in NdN format
    Expression 

    Args:
        expr (str): A list of numbers and NdN expressions separated by +,-,*,/, or **. 
                    For example: (5d6-2*3/8+4)**2
    """
    try:
        exprAfterRoll, value = dr.rollAndCalculate(expr, MAX_OUTPUT_LENGTH)
        result = formatOutput(exprAfterRoll, value)
    except Exception as e:
        LOGGER.exception(e)
        await ctx.send(str(e))
        return
    
    await ctx.send(result)

def formatOutput(label: str, value):
    value = str(value)
    valLength = len(value)
    # -10 => formatting + extra space for ... if expression doesn't fit
    maxLabelLength = MAX_OUTPUT_LENGTH - valLength -10
    if maxLabelLength<0:
        LOGGER.warning('Result too big to show in Discord! This will be truncated: ', value)
        return f'`... = {value[:maxLabelLength]}...`'
    truncatedLabel = label if len(label) <= maxLabelLength else label[:maxLabelLength] + '...'
    return f'`{truncatedLabel} = {value}`'
    

@bot.command(description="Can't choose? Let me do it!")
async def choose(ctx, *choices: str):
    """Chooses randomly between multiple choices. 
    """
    await ctx.send(random.choice(choices))

# Get token

tokenPath = pathlib.Path(__file__).parent / 'horde_bot.token'
with open(tokenPath, 'r', encoding="utf-8") as tokenFile:
    token = tokenFile.readline()

# Run and connect    

bot.run(token, log_handler=None)