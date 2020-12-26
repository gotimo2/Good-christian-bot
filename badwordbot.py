# imports
import os
import discord
import re
import datetime
import random
import dotenv

#dotenv stuff
from dotenv import load_dotenv #import loading .env function
load_dotenv() #load .env
TOKEN = os.getenv("TOKEN") #get token from .env and define it

#set a token, define date and time + client and things to say when a banned word is said
now = datetime.datetime.now()
current = now.strftime("%Y-%m-%d %H:%M:%S")
deathquotes = [
    'they must die','to the forever box with them','their free trial of life has ended','destruction imminent','how dare they','nani','fuck that - wait','god will not have as much mercy as me','delete that','i will put a toaster in their bath','what in the name of gods green earth','death would not be enough of a punishment','what a sin','truly the worst kind of person','living was overrated anyway','turn up the gas in the oven','...','and no one asked for it','help they\'re making me write stupid things for a stupid bot to say i\'m located at' 
]
client = discord.Client()

badwordlist = open("badwordlist.txt", "r").read().split("\n")

@client.event
async def on_message(message):
    if message.author == client.user: #no real reason for this, the bot is never going to call itself, but it takes 5 seconds to implement so i might as well
        return
    if message.content == 'hello bot':
        response = f'hello human {message.author}'
        print(f'sent {response}')
        await message.channel.send(response)

    for word in badwordlist:
        #add 'eyes' reaction when a banned word is said and log it to file and console
        if word in message.content.lower():
            print(f'{message.author} said a bad word, {random.choice(deathquotes)}.')
            f = open("log.txt", "a")
            f.write(f'{datetime.datetime.now()}: {message.author.id} as {message.author} in server {message.guild} said a banned word in message \'{message.content}\'\n' )
            f.close()
            await message.add_reaction('\N{EYES}')
            return

    #check if message calls to swear counter
    if message.content.startswith('!swearcount'):
        sqid = message.content.lstrip('!swearcount ')
        if not message.mentions:    #check if message mentions a user
            await message.channel.send('invalid mention!')
        else:
            targ = message.mentions[0] #pick the first mention in the message and store it in 'targ'
            sqid = str(targ.id) #take 'targ' and get their ID so the bot can look it up in the logs
            file = open("log.txt", "r")
            data = file.read()
            occurrences = data.count(sqid) #count how often targ's ID is in the log file
            await message.channel.send(f'user {sqid} AKA {targ} has sworn {occurrences} times!') #return the amount of occurences in a message
            return

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)
