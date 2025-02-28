# goodluck reading the code

import os
from time import sleep

try:
    import discord
    from aioconsole import ainput
except:
    print("Installing required packages.")
    os.system('pip install --upgrade pip')
    sleep(0.5)
    os.system('pip install discord.py-self')
    sleep(0.5)
    os.system('pip install aioconsole')
    sleep(0.5)
    import discord
    from aioconsole import ainput

import logging
from sys import stdin

from colorama import Fore, Style, just_fix_windows_console
just_fix_windows_console()
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')
async def retinp():
    await ainput(f"\n{Fore.LIGHTBLACK_EX}Press [ENTER] to return.{Style.RESET_ALL}")
os.system('title CLICORD')
logging.disable(logging.CRITICAL)
cls()
joinedChannel = None
msgToSend = None
tokenToRun = None

with open('savedtoken.txt','r') as readfile:
    content = readfile.read()
    if content == '':
        tokenToRun = input(f"{Fore.LIGHTMAGENTA_EX}ACCOUNT TOKEN: {Fore.GREEN}")
        tokenSaveDilemma = input(f"{Style.RESET_ALL}Would you like to save this token so you don't need to log in manually again next time? ([y] to agree, [ENTER] to decline): ")
        if tokenSaveDilemma == 'y':
            with open('savedtoken.txt','w') as writefile:
                writefile.write(tokenToRun)
    else:
        continueConfirmation = input(f"Would you like to continue with your saved account? ([y] to agree, [ENTER] to decline): ")
        if continueConfirmation == 'y':
            tokenToRun = content
        else:
            tokenToRun = input(f"{Fore.LIGHTMAGENTA_EX}ACCOUNT TOKEN: {Fore.GREEN}")

cls()
print("Please wait...")

class MyClient(discord.Client):
    async def on_ready(self):
        sleep(1)
        while True:
            cls()
            print(f"""{Fore.LIGHTBLUE_EX}CLICORD{Style.RESET_ALL}

[1] Join Channel
[2] View Friendslist
[3] View Group DMs
[4] View Serverlist
[5] View Channels In Server
""")
            mainselection = await ainput(f"{Fore.LIGHTBLACK_EX}SELECTION: {Fore.YELLOW}")
            print(mainselection)
            
            if mainselection == '1':
                cls()
                global joinedChannel, msgToSend
                try:
                    channel_id = await ainput(f"{Fore.LIGHTBLACK_EX}TARGET CHANNEL ID: {Fore.YELLOW}")
                    joinedChannel = await client.fetch_channel(channel_id)
                except:
                    print(f"{Fore.RED}BAD CHANNEL ID:\nUnavailable{Style.RESET_ALL}")
                    await retinp()
                    continue
                cls()

                msghistory = [message async for message in joinedChannel.history(limit=int(50))]
                for hismsg in msghistory[::-1]:
                    print(f"{Fore.GREEN if hismsg.author.id == client.user.id else Fore.RED}{str(hismsg.author).replace('#0', '')}:{Style.RESET_ALL} {hismsg.content.replace(f'<@{str(client.user.id)}>', f'{Fore.LIGHTYELLOW_EX}@{client.user.name}{Style.RESET_ALL}')}")

                print(f"{Fore.CYAN}[CLICORD] You are now chatting. Type and press [ENTER] to send a message! Type '/c' to exit the chat.{Style.RESET_ALL}")

                while True:
                    msgToSend = await ainput(f"{Fore.YELLOW}")
                    stdin.flush()
                    if msgToSend == '/c':
                        joinedChannel = None
                        break
                    else:
                        await joinedChannel.send(msgToSend)
            elif mainselection == '2':
                cls()
                for relationship in client.relationships:
                    if relationship.type == discord.RelationshipType.friend:
                        friend = relationship.user
                        dm_channel = friend.dm_channel
                        if dm_channel is None:
                            dm_channel = await friend.create_dm()
                        print(f"{Fore.GREEN}USER: {friend.name}{Style.RESET_ALL} || {Fore.RED}ID: {friend.id}{Style.RESET_ALL} || {Fore.YELLOW}DM CHANNEL ID: {dm_channel.id}{Style.RESET_ALL}")
                await retinp()
            elif mainselection == '3':
                cls()
                group_chats = [channel for channel in client.private_channels if isinstance(channel, discord.GroupChannel)]
                for group in group_chats:
                    print(f"{Fore.GREEN}NAME: {group.name}{Style.RESET_ALL} || {Fore.YELLOW}ID: {group.id}{Style.RESET_ALL}")
                await retinp()
            elif mainselection == '4':
                cls()
                for guild in client.guilds:
                    print(f"{Fore.GREEN}{guild.name}{Style.RESET_ALL} || {Fore.RED}MEMBERS: {guild.member_count}{Style.RESET_ALL} || {Fore.YELLOW}ID: {guild.id}{Style.RESET_ALL}")
                await retinp()
            elif mainselection == '5':
                cls()
                serverIdToIterateChannels = await ainput(f"{Fore.LIGHTBLACK_EX}TARGET GUILD ID: {Fore.YELLOW}")
                serverTrgt = await client.fetch_guild(serverIdToIterateChannels)
                channels = await serverTrgt.fetch_channels()
                for channel in channels:
                    print(f"{Fore.GREEN}{channel.name}{Style.RESET_ALL} || {Fore.YELLOW}{channel.id}{Style.RESET_ALL}")
                await retinp()
            else:
                print(f"{Fore.RED}Invalid selection.{Style.RESET_ALL}")
                await retinp()

    async def on_message(self, msg):
        if msg.channel.id == joinedChannel.id and msg.author != client.user:
            print(f"{Fore.RED}{str(msg.author).replace('#0','')}:{Style.RESET_ALL} {msg.content}{Fore.YELLOW}")

client = MyClient()
client.run(tokenToRun)
