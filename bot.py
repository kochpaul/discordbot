import discord 
from discord.utils import get

import time 
import os
import youtube_dl


class MyCliet(discord.Client):
    # login
    async def on_ready(self):
        print("SYSTEM: Bot is ready!")    

    async def on_message(self, message):   
        if message.content.startswith(".clear"):            
            if message.author.permissions_in(message.channel).manage_messages:
                args = message.content.split(" ")
                if len(args) == 2:
                    if args[1].isdigit():
                        limit = int(args[1])
                        await message.channel.purge(limit=limit)
    
        if message.content.startswith(".play"):        
            await message.delete()
            try:
                args = message.content.split()
                if len(args) == 3:                
                    url = args[2] # YouTube URL from song which wanted to play 
                    where = args[1] # Channel which used for playing the song 

                    # youtube downloading options

                    ydlOptions = {
                        'format': 'bestaudio/best',
                        'quiet': True,
                        'postprocessors':[{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],

                    }

                    # check if there is old data in song dir -> delete it
                    
                    
                    path = "/home/runner/discordBotpy"
                    
                    for x in os.listdir(path):
                        dataPath = path + "/" + x
                        if dataPath.endswith(".mp3"):
                            os.remove(dataPath)
                        else:
                            pass
                        

                    # try to catch given channel 

                    try:
                        channel = get(message.guild.channels, name=where)
                        print("Gettet server!")
                    
                    except:                     
                        print("ERROR: given channel doesn't exist!")
                        await message.channel.send("SYSTEM: Given channel doesn't exist!")
                    

                    # try to connect to channel (see above)

                    try:                
                        global voicechannel                    
                        voicechannel = await channel.connect()
                        print("connectet to channel!")
                    except TimeoutError:
                        print("\nERROR: Failed while connecting to given channel!\n")
                        await message.channel.send("SYSTEM: Failed while connecting to given channel! !")
                        

                    # download song with url from youtube
                    
                    try:
                        with youtube_dl.YoutubeDL(ydlOptions) as ydl:
                            print (f"SYSTEM: Downloading song right now!")
                            ydl.download([url])
                    except:
                        print(f"\nERROR: Couldn't download song by link!\n")
                        await message.channel.send("(SYSTEM): ERROR 1002")
                    
                    
                    # rename the downloaded file

                    for file in os.listdir(path):
                        if file.endswith(".mp3"):
                            name = file 
                            print (f"SYSTEM: Rename file: {file}")
                            os.rename(file, "song.mp3")
                    
                    # try to play downloaded song   

                    try:                    
                        voicechannel.play(discord.FFmpegPCMAudio("/home/runner/discordBotpy/song.mp3"))
                        await message.channel.send(f"{name} is playing!")
                    
                    except TimeoutError:
                        print(f"\nERROR: Cannot connect with channel!\n")
                        await message.channel.send("(SYSTEM): ERROR 1003")  
                    

                    print(f"SYSTEM: {name} is playing!")
                else:
                    print(f"\nERROR: Exactly 2 arguments are required!\n")
                    await message.channel.send("(SYSTEM): ERROR 1001")
            except:
                print("ERROR: music is allready playing!")
                await message.channel.send("ERROR: Music is allready playing, please first stop the music with '.stop' and try again!")

        if message.content.startswith(".pause"):
            await message.delete()
            if voicechannel.is_playing():
                voicechannel.pause()
                print("SYSTEM: Music pauses!")
                message.channel.send("SYSTEM: Music is paused!")
            
            else:
                print("ERROR: No music is playing!")
                await message.channel.send("ERROR: No music is playing!")
        
        if message.content.startswith(".resume"):
            await message.delete()
            if voicechannel.is_paused():
                voicechannel.resume()
                print("SYSTEM: Music resumed!")
            
            else:
                print("ERROR: error while resuming music!")
                await message.channel.send("ERROR: There is no music that could be resumed!")
        
        if message.content.startswith(".stop"):
            await message.delete()
            if voicechannel.is_playing or voicechannel.is_paused():
                voicechannel.stop()
                print("SYSTEM: Music stopped!")
            
            else:
                print("ERROR: error while stopping music!")
                await message.channel.send("ERROR: There is no music that could be stopped!")            

        if message.content.startswith(".leave"):
            await message.delete()
            if voicechannel.is_connected():
                await voicechannel.disconnect()
                print("SYSTEM: disconnected bot from channel")
                await message.channel.send("Bis dann ...")        

        if message.content.startswith(".ERRORCODES"):
            await message.delete()
            await message.channel.send("1001 - .play + CHANNEL + URL\n1002 - Wrong link inserted!\n1003 - Cannot connect with channel. Please insert existing channel!\n1004 - XXX\n")

