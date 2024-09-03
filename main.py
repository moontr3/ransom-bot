from config import *
from log import *

import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from typing import *
import time

import styler

# loading token
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

bot = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all(), help_command=None)


# connection events

@bot.event
async def on_ready():
    log('Ready!')


# syncing tree

@bot.command(aliases=['st'])
async def synctree(ctx):
    '''
    Syncs slash command tree.
    '''
    print(ctx.author.id, ADMINS)
    if ctx.author.id not in ADMINS: return

    log(f'{ctx.author.id} requested tree syncing')
    embed = discord.Embed(
        title=f'Syncing...', color=discord.Color.yellow()
    )
    msg = await ctx.reply(embed=embed)
    
    synced = await bot.tree.sync()
    log(f'{ctx.author.id} synced tree with {len(synced)} commands', level=SUCCESS)
    embed = discord.Embed(
        title=f'✅ {len(synced)} commands synced!',
        color=discord.Color.green()
    )
    await msg.edit(embed=embed)


# ping

@bot.command()
async def ping(ctx:commands.Context):
    '''
    A ping command.
    '''
    ping = round(bot.latency*1000)

    embed = discord.Embed(
        color=discord.Color.green(),
        description=f'{ping} мс'
    )
    await ctx.reply(embed=embed)



@bot.hybrid_command(
    name='ransom',
    aliases=['generate'],
    description='Styles your text as a ransom note.'
)
@discord.app_commands.user_install()
@discord.app_commands.describe(
    text='Your text',
    styling='(🔘 - Default) Setup random styling',
    word_separation='(🔘 - Default) How to separate words',
    newline_separation='(🔘 - Default) How to separate lines',
    spacing_and_size='(🔘 - Default) Setup spacing between letters',
    letter_case='(🔘 - Default) Setup letter casing (upper- or lowercase)',
)
async def ransom(
    ctx:commands.Context,
    *,
    text:str,

    styling: Literal[
        '🔘 Style each letter individually'
        'Style each word individually',
    ]='default',

    word_separation: Literal[
        '🔘 Put each word on a new line (one newline)',
        'Put an empty line between each word (two newlines)',
        'Put 2 spaces between each word',
        'Put each word in a different codeblock',
    ]='default',

    newline_separation: Literal[
        '🔘 Put each line in a different codeblock',
        'As-is - put each line on its own line',
        'Put an empty line between each line (two newlines)',
    ]='default',

    spacing_and_size: Literal[
        'Put a space between each letter',
        'Letters are larger on left and right sides sometimes',
        '🔘 Both of the above',
        'None of the above',
    ]='default',

    letter_case: Literal[
        '🔘 Randomly choose between caps and lowercase',
        'Leave as-is',
        'All caps',
        'All lowercase',
    ]='default',
):
    '''
    Styles the text.
    '''
    log(f'{ctx.author.id} is generating {text}')

    # getting styling
    INDIVIDUAL_STYLING = {
        'default': 'letter',
        '🔘 Style each letter individually': 'letter',
        'Style each word individually':      'word',
    }[styling]

    WORD_SEPARATION = {
        'default': 'newline',
        '🔘 Put each word on a new line (one newline)':       'newline',
        'Put an empty line between each word (two newlines)': 'twonewlines',
        'Put 2 spaces between each word':                     'spaces',
        'Put each word in a different codeblock':             'codeblock',
    }[word_separation]

    NEWLINE_SEPARATION = {
        'default': 'codeblock',
        '🔘 Put each line in a different codeblock':          'codeblock',
        'As-is - put each line on its own line':              'newline',
        'Put an empty line between each line (two newlines)': 'twonewlines',
    }[newline_separation]

    SYMBOL_SEPARATION = {
        'default': 'both',
        'Put a space between each letter':                      'spacebetween',
        'Letters are larger on left and right sides sometimes': 'spacein',
        '🔘 Both of the above':                                 'both',
        'None of the above':                                    'none',
    }[spacing_and_size]

    CASE = {
        'default': 'random',
        '🔘 Randomly choose between caps and lowercase': 'random',
        'Leave as-is':                                   'asis',
        'All caps':                                      'allcaps',
        'All lowercase':                                 'alllower',
    }[letter_case]


    # generating text
    out = '```ansi\n'
    out += styler.style_text(
        text,
        individual_styling=INDIVIDUAL_STYLING,
        word_separation=WORD_SEPARATION,
        newline_separation=NEWLINE_SEPARATION,
        symbol_separation=SYMBOL_SEPARATION,
        case=CASE
    )
    out += '\n```'

    # sending message

    embed = discord.Embed(
        description='🖥 Right-click on message and copy the text'\
            '\n📱 Hold finger on message and copy the text'\
            '\n### ‼ **Colors may not display on mobile**',
        color=discord.Color.green()
    )

    # too long message
    if len(text) >= 2000:
        embed = discord.Embed(
            description='**The text is too long to send in one message!**'\
                '\n- Try using the command again'\
                '\n- Try changing some settings like spacing and size'\
                '\n- Try using a different shorter text',
            color=discord.Color.red()
        )
        await ctx.reply(embed=embed, ephemeral=True)
        return

    await ctx.reply(out, embed=embed)


## RUNNING BOT
bot.run(TOKEN)