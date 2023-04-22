# Based on discord.py's basic bot example: https://github.com/Rapptz/discord.py/blob/master/examples/basic_bot.py 
# TODO:
#   - set up logging
#   - write tests?
#   - test rolling code
#   - format output to remove trailing 0s
#   - comment ops
#   - massive roll protection
#   - edit descriptions for help command
#   - implement days to or days since
#   - implement poll

import discord
from discord.ext import commands
import random
import pathlib
import commons.operations.dice_roll as dr

description = '''This bot implements functionalities that may be interesting or useful for the horde'''

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command(description="Roll dice and calculate")
async def roll(ctx, expr: str):
    """Evaluates the expression, rolling any dice provided in NdN format
    Expression 

    Args:
        expr (str): A list of numbers and NdN expressions separated by +,-,*,/, or **. 
                    For example: (5d6-2*3/8+4)**2
    """
    try:
        exprAfterRoll, value = dr.rollAndCalculate(expr)
    except Exception as e:
        print(e)
        await ctx.send(str(e))
        return

    result = f'`{exprAfterRoll} = {value:g}`'
    await ctx.send(result)


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

bot.run(token)