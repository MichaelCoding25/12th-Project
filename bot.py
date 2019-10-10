# bot.py
import os
import random

import discord
from discord.ext import commands

client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    print("Bot is ready")

@client.event
async def on_member_join(member):
    print(f'{member} has joined a server')

@client.event
async def on_member_remove(member):
    print(f'{member} has left a server')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ['It is certain.',
                 'It is decidedly so.',
                 'Yes.',
                 'Ask again later.',
                 'My sources say no.']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

client.run('NjI0MTg1MzgyMjM3MzcyNDIx.XZ8A-Q._bIKDzENFXvlOPnxOBKw9FOJgJE')
