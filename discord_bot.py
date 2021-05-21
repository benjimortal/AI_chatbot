# bot.py
import os
import random

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='99',
             help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)


@bot.command(name='SW',
             help='Responds with a random quote from Star Wars')
async def star_wars(ctx):
    star_wars_quotes = [
        'Help me, Obi-Wan Kenobi. You’re my only hope.',
        'I find your lack of faith disturbing.',
        'The Force will be with you. Always.',
        'Why, you stuck-up, half-witted, scruffy-looking nerf herder!',
        'Never tell me the odds!',
        'Do. Or do not. There is no try.',
        'No. I am your father.'
        'When gone am I, the last of the Jedi will you be.'
        ' The Force runs strong in your family. Pass on what you have learned.',
        'I’ll never turn to the dark side. '
        'You’ve failed, your highness. I am a Jedi, like my father before me.',
        'Now, young Skywalker, you will die.',
        'Just for once, let me look on you with my own eyes.',
        'There’s always a bigger fish.',
        'In time, the suffering of your people will persuade'
        ' you to see our point of view.',
        'You can’t stop the change, '
        'any more than you can stop the suns from setting.',
        'Fear is the path to the dark side. '
        'Fear leads to anger; anger leads to hate; hate leads to suffering.'
        ' I sense much fear in you',
        'Well, if droids could think, there’d be none of us here, would there?',
        'We must keep our faith in the Republic. '
        'The day we stop believing democracy can work is the day we lose it.',
        'I’m just a simple man trying to make my way in the universe.',
        'What if I told you that the Republic was now under the control '
        'of a Dark Lord of the Sith?',
        'The dark side of the Force is a pathway to '
        'many abilities some consider to be unnatural.',
        'Power! Unlimited power!',
        'So this is how liberty dies. With thunderous applause.',
        'You were my brother, Anakin. I loved you.',
    ]

    response = random.choice(star_wars_quotes)
    await ctx.send(response)


@bot.command(name='roll_dice',
             help='Simulates rolling dice. '
                  'ie. to roll a D6 twice write "!roll_dice 2 6"')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1 )))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))


bot.run(TOKEN)
