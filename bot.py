from faulthandler import disable
from logging import PlaceHolder
from select import select
from tkinter.tix import Select
from tkinter.ttk import Style
import discord
import time
import youtube_dl
import asyncio
import datetime
import random
import os
from msilib.schema import Component, File
from threading import activeCount
from discord import DMChannel 
from discord.ext import commands
from discord.ui import Button, View
from discord import FFmpegAudio
from discord import option

intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix="§", intents=intents)
musics = {}
ytdl = youtube_dl.YoutubeDL()
bot.remove_command('help')

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game('Hentai Heroes 💦'))
    print ('✅')



#-------------------------------------§HELP--------------------------------------------------------------------------#

#-------------------------Main Help-----------------------#

@bot.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(title = "Help", description = "Utilise **§help <commande>** pour avoir des détails")

    em.add_field(name = "Pixel Art 🧩", value = " §putin <:Putinapproves:955601443442806824> \n §shrek")
    em.add_field(name = "Musique 🎶", value = " §play 🔊\n §skip ⏩\n §pause ⏸️\n §resume ▶️\n §leave 🛑")
    em.add_field(name = "Divers ⚛️", value = " §test")

    await ctx.send(embed = em)

#------------------------Help Pixel Art------------------------#

@help.command()
async def putin(ctx):

    em = discord.Embed(title = "§Putin", description = "**§putin** *(Pixel Art 🧩)* \n Faire apparaitre un magnifique Putin en pixel art")
    em.add_field(name = "<:Putinapproves:955601443442806824>", value = "https://www.youtube.com/watch?v=FTl0Vkqmh3A")
    await ctx.send(embed = em)

@help.command()
async def shrek(ctx):

    em = discord.Embed(title = "§Shrek", description = "**§shrek** *(Pixel Art 🧩)* \n Faire apparaitre un magnifique Shrek en pixel art")
    em.add_field(name = "<:pepeHmm:829331008046104587>", value = "https://www.youtube.com/watch?v=HLQ1cK9Edhc")
    await ctx.send(embed = em)

#-----------------------Help Musique---------------------------#

@help.command()
async def play(ctx):

    em = discord.Embed(title = "§play", description = "**§play** <le lien de la musique> *(Musique 🎶)* \n Pour mettre de la musique avec le bot")
    em.add_field(name = "🔸🔊🔸­­", value = "**-------------------------------------------------**")
    await ctx.send(embed = em)

@help.command()
async def pause(ctx):

    em = discord.Embed(title = "§pause", description = "**pause** *(Musique 🎶)* \n Pour mettre en pause la musique")
    em.add_field(name = "🔸⏸️🔸", value = "**-------------------------------------------------**")
    await ctx.send(embed = em)

@help.command()
async def resume(ctx):
    
    em = discord.Embed(title = "§resume", description = "**§resume** *(Musique 🎶)* \n Pour reprendre la musique mise en pause")
    em.add_field(name = "🔸▶️🔸", value = "**-------------------------------------------------**")
    await ctx.send(embed = em)

@help.command()
async def skip(ctx):

    em = discord.Embed(title = "§skip", description = "**§skip** *(Musique 🎶)* \n Pour passer à la prochaine musique")
    em.add_field(name = "🔸⏩🔸", value = "**-------------------------------------------------**")
    await ctx.send(embed = em)

@help.command()
async def leave(ctx):

    em = discord.Embed(title = "§leave", description = "**§leave** *(Musique 🎶)* \n Pour faire deco le bot du voc")
    em.add_field(name = "🔸🛑🔸", value = "**-------------------------------------------------**")
    await ctx.send(embed = em)

#-------------------------------Divers------------------------#

@help.command()
async def test(ctx):

    em = discord.Embed(title = "test", description = "**§test** *(Divers ⚛️)* \n Pour faire un test de culture G (surtout parce que je savais pas quoi faire)")
    em.add_field(name = "🔸✅ 🔸 ❌🔸",  value = "**-------------------------------------------------------------------------------------------**")
    em_2 = discord.Embed(Title = "raccourcis_test", description = "**-----------------**\n ** Faire le test ? **\n**-----------------**")
    await ctx.send(embed = em)
    time.sleep(2)
    message = await ctx.send(embed = em_2)
    time.sleep(1)
    await message.add_reaction("✅")
    await message.add_reaction("❌")

@help.command()
async def PhP(ctx):

    em = discord.Embed(title = "php", description = "**§PhP** *(Divers ⚛️)* \n Affiche ma php en .png)")
    em.add_field(name = "(❤ ω ❤)",  value = discord.File('Discord.png'))
    await ctx.send(embed = em)
    time.sleep(1)
    await em.add_reaction("<:Discord:983752984670380052>")

#-------------------------------------------------Musique Code-----------------------------------------------------------#

class Video:
    def __init__(self, link):
        video = ytdl.extract_info(link, download=False)
        video_format = video["formats"][0]
        self.url = video["webpage_url"]
        self.stream_url = video_format["url"]

@bot.command()
async def leave(ctx):
    client = ctx.guild.voice_client
    await client.disconnect()
    musics[ctx.guild] = []

@bot.command()
async def resume(ctx):
    client = ctx.guild.voice_client
    if client.is_paused():
        client.resume()


@bot.command()
async def pause(ctx):
    client = ctx.guild.voice_client
    if not client.is_paused():
        client.pause()


@bot.command()
async def skip(ctx):
    client = ctx.guild.voice_client
    client.stop()


def play_song(client, queue, song):
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song.stream_url
        , before_options = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))

    def next(_):
        if len(queue) > 0:
            new_song = queue[0]
            del queue[0]
            play_song(client, queue, new_song)
        else:
            asyncio.run_coroutine_threadsafe(client.disconnect(), bot.loop)

    client.play(source, after=next)


@bot.command()
async def play(ctx, url):
    client = ctx.guild.voice_client

    if client and client.channel:
        video = Video(url)
        musics[ctx.guild].append(video)
    else:
        channel = ctx.author.voice.channel
        video = Video(url)
        musics[ctx.guild] = []
        client = await channel.connect()
        await ctx.send(f"J'ai mis : {video.url} bande de pd")
        play_song(client, musics[ctx.guild], video)


#--------------------------------------------------------------------------------------------------------------------#


@bot.command()
async def clear(ctx, nombre: int):
    message = await ctx.channel.history(limit=nombre + 1).flatten()
    for message in message:
        await message.delete()





class MyView69(discord.ui.View):

    @discord.ui.button(label="Tirer", row=0, style=discord.ButtonStyle.danger, emoji="💀")
    async def first_button_callback(self, button, interaction):        
            munition = (0,0,0,0,0,1)
            shoot = random.choice(munition)
            if shoot == 1:
                button.emoji = "💀"
                button.label= ""
                button.disabled = True
                await interaction.response.edit_message(view=self)
            else:
              button.emoji = "😇"
              button.label= ""
              button.disabled = True
              await interaction.response.edit_message(view=self)

@bot.slash_command(description="Roulette russe de chad") 
async def gun(ctx):
    em = discord.Embed(title = "Vous sortez votre **revolver** de votre poche...", description = "⚔| 💀 = **-10** Chadissme ▪▪▪▪ 😇 = **+2** Chadissme |⚔")
    await ctx.send (embed = em, view=MyView69())




@bot.slash_command()
async def game(ctx, jeu: discord.Option(str), lien: discord.Option(str)):

    if jeu == "chess" or "Chess":
     em = discord.Embed(title = f"Go sur Chess ♟", description = f"Le lien: {lien}", color=0x2ecc71)
     await ctx.send(embed = em)
     return

    if jeu == "JKLM" or "jklm" or "Jklm":
     em = discord.Embed(title = f"Go sur JKLM 🕹", description = f"Le lien: {lien}", color=0x9b59b6)
     await ctx.send(embed = em)
     return

    else: 
     em = discord.Embed(title = f"Go sur {jeu}", description = f"Le lien: {lien}", color=0x3498db)
     await ctx.send(embed = em)
     return
   




@bot.command() #test
async def test(ctx):


    
    em = discord.Embed(tittle = "intro", description = "Bienvenue sur le test de connerie")

    em.add_field(name = "Commencer", value = " ✅")
    em.add_field(name = "Arreter", value = " ❌")

    message = await ctx.send(embed = em)

    await message.add_reaction("✅")
    await message.add_reaction("❌")

    def checkEmoji_1(reaction,user):
        return ctx.message.author == user and message.id == reaction.message.id and (str(reaction.emoji) == "✅") or (str(reaction.emoji) == "❌")

    reaction, user = await bot.wait_for("reaction_add", check = checkEmoji_1)
    if reaction.emoji == "✅":
        await ctx.send("Question 1:")

    else:
        await ctx.send("test annulé")




@bot.command()
async def putin(ctx):
        await ctx.send(
"⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⢀⠄⡀⠄⡀⢀⠄⡀⡀⠠⢀⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄\n"
"⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⡀⠠⢀⠄⡅⢔⠰⡨⢢⢡⢑⠔⠅⠕⠄⠅⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄\n" 
"⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⡀⠅⢔⠨⢐⠅⡌⢆⢣⠪⡪⡘⡌⡮⡱⡡⣊⢌⢀⢀⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄\n"
"⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠠⡐⢄⠕⡡⡘⢔⢱⢨⢪⢪⢪⢪⡺⣪⢞⢮⢫⢮⢺⢔⢆⡢⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄\n"
"⠄⠄⠄⠄⠄⢀⠐⠈⠄⡠⡊⢌⠢⡑⡌⡆⡇⡇⡇⡇⣇⢗⣝⢮⡺⣪⡳⣹⡪⣞⢵⢝⡵⡝⣕⠡⢀⢂⠄⠄⠄⠄⠄⠄⠄⠄\n"
"⠄⠄⠄⠄⢠⢊⢂⠁⡔⡌⡢⢑⠌⡢⡱⡸⡸⡸⡪⡺⡸⣕⢵⡳⣝⢮⡺⣪⢞⣵⣫⡳⣕⢯⡺⡬⠄⠕⡕⡄⠄⠄⠄⠄⠄⠄\n"
"⠄⠄⠄⠄⡇⡇⡂⢢⢣⢣⠨⡂⡊⢔⢕⢱⡱⡝⣜⢝⡺⣜⡵⣝⢮⡳⡽⣵⣻⡺⣼⡺⡵⣳⢝⡮⡃⡕⡺⢄⠄⠄⠄⠄⠄⠄\n"
"⠄⠄⠄⢸⡱⡱⡨⢪⢪⢢⠡⢂⢊⠢⡱⡱⡱⡝⡮⡳⣝⢞⢮⢗⡯⣯⢯⣗⡯⣟⣮⢯⣟⢮⡳⣝⢇⢇⢎⢵⡀⠄⠄⠄⠄⠄\n"
"⠄⠄⠄⣕⢵⢣⢣⢑⢅⢆⢃⠢⠡⡡⡱⡱⡹⡪⡯⣺⢕⡯⣫⢯⢾⢽⢽⣺⢯⣗⡯⣗⣗⢗⣝⢮⡫⣏⢮⢒⢅⠄⠄⠄⠄⠄\n"
"⠄⠄⢀⠮⡪⢪⠪⠢⡃⡪⡂⠅⢕⠰⢱⢸⢸⡱⣝⢮⡳⡽⣪⢏⡯⡯⣟⡾⣽⣺⢽⣳⡳⣝⢮⡳⣫⣳⢳⡱⡱⠄⠄⠄⠄⠄\n"
"⠄⠄⢀⡃⡫⢔⢨⢕⢕⢔⢌⢌⠢⡑⡱⡘⢜⢜⢮⡳⣝⣞⢵⣫⢿⢽⣺⡽⡾⣾⢽⣳⢯⢮⡳⣝⣕⢗⢵⡑⡕⡀⠄⠄⠄⠄\n"
"⠄⠄⠐⠢⡱⡐⢕⢵⣑⡑⢕⢐⠕⠸⠰⡑⠕⢕⢕⠽⡕⣏⢗⢽⢝⢽⠺⠽⠽⢽⢻⢽⢽⢵⢽⡸⣪⢳⢱⢱⡱⡽⡡⡀⠄⠄\n"
"⠄⠄⠨⠈⢆⢊⢎⢖⢂⠃⠡⠐⠈⠈⠄⠄⠄⠄⠄⢑⢹⢘⣜⢕⠑⡈⠄⡈⣈⣐⠨⠘⡜⢕⡳⣝⢮⡳⡱⡱⡵⡯⡪⠂⠄⠄\n"
"⠄⠄⠄⠅⢂⠑⡕⡕⠄⡢⢀⠄⠠⠄⠁⠁⡌⠠⢠⠄⠸⣸⣺⡪⣐⠅⢢⢈⠄⢬⢍⣆⢧⣳⡽⡮⣺⡪⡺⣘⢼⣝⠆⠄⠄⠄\n"
"⠄⠄⠄⠨⡢⡢⡣⡳⢑⢰⢐⠠⡊⡪⣢⡣⡪⡰⠑⡀⠨⣪⢷⣝⡮⡫⡪⣪⢾⢝⣯⢾⣝⣗⡯⣟⢮⡪⡯⡷⣗⡯⠄⠄⠄⠄\n"
"⠄⠄⠄⠄⢕⠄⡇⡣⡑⠔⢅⠇⡇⡏⡖⡕⡕⣌⢂⠂⠌⢮⢷⡳⡯⡯⡾⡵⣫⢯⢞⣗⡷⡯⣯⡳⣱⢱⢝⡽⣺⠁⠄⠄⠄⠄\n"
"⠄⠄⠄⠄⠡⡡⢱⢐⠨⠨⠐⡡⢃⢇⢇⡏⡞⡔⡐⠠⢑⢽⢽⢽⢽⢽⢽⣝⢗⡯⣟⢾⢽⢝⡞⣜⢜⢜⣽⣺⠎⠄⠄⠄⠄⠄\n"
"⠄⠄⠄⠄⠄⠊⠃⠂⡐⠄⠅⡐⡈⡢⡃⢇⠕⡢⠄⠨⢘⢮⢯⢯⣳⡫⡗⣗⢽⢝⡮⡯⡮⡣⡏⣎⢎⠞⠺⠊⠄⠄⠄⠄⠄⠄\n"
"⠄⠄⠄⠄⠄⠄⠄⠄⠂⡁⢂⠐⡈⡢⢑⠅⡕⡐⠈⠨⡨⢯⣻⢽⣺⢺⡺⡪⣏⢷⢽⢕⣯⡫⣞⢜⢜⠄⠄⠄⠄⠄⠄⠄⠄⠄\n"
"⠄⠄⠄⠄⠄⠄⠄⠄⡁⠄⠄⠂⡂⠌⠄⢕⢐⠌⢄⠄⠨⠨⢘⢥⢅⡵⣝⣝⢮⡳⡽⣝⡮⣺⢪⢎⣗⠄⠄⠄⠄⠄⠄⠄⠄⠄\n"
"⠄⠄⠄⠄⠄⠄⠄⠄⠄⢂⢀⠡⠄⠌⠌⢂⢂⠪⠐⡌⢰⢰⢘⢼⢝⣞⢞⣞⡵⡯⣞⢵⣫⢮⡳⡣⡳⠄⠄⠄⠄⠄⠄⠄⠄⠄\n"
"⠄⠄⠄⠄⠄⠄⠄⠄⠈⡀⠐⠄⠊⠄⠨⠐⠠⠈⠌⠘⠜⠵⡢⢳⢹⢜⢕⠕⠱⡹⡪⡳⣕⣳⢹⡸⠅⠄⠄⠄⠄⠄⠄⠄⠄⠄\n"
"⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠈⢄⠡⠁⠠⠄⠄⡀⠄⠐⠔⠔⠔⡢⠦⣒⢎⣎⢦⢢⢩⡫⣎⢮⢣⠃⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄\n"
"⠄⠄⠄⠄⠄⠄⠄⠄⢰⣇⠄⠐⠠⠄⠁⠄⠡⢀⢂⢅⢔⢄⣆⣆⢕⢵⡹⣪⡳⣕⢵⢱⢕⢇⡇⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄\n"
"⠄⠄⠄⠄⠄⠄⠄⠄⠱⡿⣵⣀⠄⠄⠄⠈⠨⠨⡂⢇⢎⢕⢎⢞⡽⡵⣝⢮⢺⢸⠸⡘⣜⢼⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄\n"
"⠄⠄⠄⠄⠄⠄⠄⠄⠄⢹⣺⣳⣧⣄⡀⠄⠄⡀⠂⠌⡂⠕⢌⠊⢎⠪⠪⠪⡊⡆⣕⣕⢧⣓⣧⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄\n"
"⠄⠄⠄⠄⠄⠄⠄⠄⠄⠈⢪⢞⣾⡽⣷⣮⡄⠐⠄⡂⠌⢌⠢⢑⢐⢄⢅⢇⢇⣗⣕⢗⡵⣽⣿⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄\n"
"⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠙⡾⣽⣯⣷⣿⡿⣮⣰⢱⡱⣜⢔⡑⡜⣜⢮⣣⡳⣪⢷⣽⣿⣿⡀⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄\n"
"⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠘⡷⣿⣽⣿⣿⣿⣿⣿⣾⣮⣗⣽⢵⢕⣕⢮⡺⢝⣵⣿⣿⣿⣷⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄\n"
"⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠘⣯⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣵⣏⣾⣿⣿⣿⣿⣿⣿⣇⠄⠄⠄⠄⠄⠄⠄⠄⠄\n"
"⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠻⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠉⠄⠄⠄⠉⠻⢿⣿⣿⣿⣿⡀⠄⠄⠄⠄⠄⠄⠄⠄\n"
"⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⢻⣿⣿⣿⣿⣿⣿⣿⡟⠁⠄⠄⠁⠠⠄⠄⠄⠈⠽⣿⣿⣿⣷⠄⠄⠄⠄⠄⠄⠄⠄\n"
"⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠈⢿⣿⣿⣿⣿⣿⡵⣄⠄⠄⠄⠄⠁⠈⠄⠄⢸⣹⡪⣿⣿⣿⡂⠄⠄⠄⠄⠄⠄⠄\n"
"⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠈⢿⣿⣿⣻⣿⣿⣯⣿⣢⣄⠄⠄⠄⠑⠠⢸⣿⣿⣮⢞⣿⣧⠄⠄⠄⠄⠄⠄⠄\n"
"<:Putinapproves:955601443442806824>")

@bot.command()
async def shrek(ctx):
    await ctx.send(
"⢀⡴⠑⡄⠀⠀⠀⠀⠀⠀⠀⣀⣀⣤⣤⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀  \n"
"⠸⡇⠀⠿⡀⠀⠀⠀⣀⡴⢿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀  \n"
"⠀⠀⠀⠀⠑⢄⣠⠾⠁⣀⣄⡈⠙⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀  \n"
"⠀⠀⠀⠀⢀⡀⠁⠀⠀⠈⠙⠛⠂⠈⣿⣿⣿⣿⣿⠿⡿⢿⣆⠀⠀⠀⠀⠀⠀⠀  \n"
"⠀⠀⠀⢀⡾⣁⣀⠀⠴⠂⠙⣗⡀⠀⢻⣿⣿⠭⢤⣴⣦⣤⣹⠀⠀⠀⢀⢴⣶⣆  \n" 
"⠀⠀⢀⣾⣿⣿⣿⣷⣮⣽⣾⣿⣥⣴⣿⣿⡿⢂⠔⢚⡿⢿⣿⣦⣴⣾⠁⠸⣼⡿  \n"
"⠀⢀⡞⠁⠙⠻⠿⠟⠉⠀⠛⢹⣿⣿⣿⣿⣿⣌⢤⣼⣿⣾⣿⡟⠉⠀⠀⠀⠀⠀  \n"
"⠀⣾⣷⣶⠇⠀⠀⣤⣄⣀⡀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀  \n"
"⠀⠉⠈⠉⠀⠀⢦⡈⢻⣿⣿⣿⣶⣶⣶⣶⣤⣽⡹⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀  \n"
"⠀⠀⠀⠀⠀⠀⠀⠉⠲⣽⡻⢿⣿⣿⣿⣿⣿⣿⣷⣜⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀  \n"
"⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣷⣶⣮⣭⣽⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀  \n" 
"⠀⠀⠀⠀⠀⠀⣀⣀⣈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀  \n"
"⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀  \n"
"⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀  \n"
"⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠻⠿⠿⠿⠿⠛⠉ \n")



class MyView(discord.ui.View):
    @discord.ui.select(
        placeholder = "Choisis un son",
        min_values = 1,
        max_values = 1, 
        options = [ 
            discord.SelectOption(
                emoji="<:images:1010881342076104775>",
                label="Bara",
                description="Jouer Bara",
            ),
            discord.SelectOption(
                emoji="<:Putinapproves:955601443442806824>",
                label="Putin",
                description="Jouer Wide Putin"
            ),
            discord.SelectOption(
                emoji="<:pottis:1010881303882772540>",
                label="Pootis",
                description="Put dispenser here"
            ),
            discord.SelectOption(
                emoji="<:POGCHAMP:1010881399173161052>",
                label="Yamete Kudasai",
                description="Aaaaaa 💦"
            ),
            discord.SelectOption(
                emoji="<:dejavu:1010889324033740860>",
                label="Déjà Vu",
                description="Vroum",
            ),
            discord.SelectOption(
                emoji="<:Fortnite:1010889699998584863>",
                label="FoRtnItE",
                description="No Gaming",
            ),
            discord.SelectOption(
                emoji="<:jojo:1010889811734835201>",
                label="Giornos",
                description="Gay",
            ),
            discord.SelectOption(
                emoji="<:cutg:1010889906396090368>",
                label="I like your cut g",
                description="aaaaaaaaaaaaaaaaa",
            ),
            discord.SelectOption(
                emoji="🇫🇷",
                label="La Marseillaise",
                description="Meilleur empire qui es jamais existé",
            ),
            discord.SelectOption(
                emoji="<:chad:1010683821336830082>",
                label="Chad",
                description="Just a chad",
            )
        ]
    )
    async def select_callback(self, select, interaction):
        channel = bot.get_channel(742318777055707238)
        await channel.send(f"```SoundBoard: {select.values[0]} a été lancé```")
        Bara = "Bara"
        Putin = "Putin"
        Pootis = "Pootis"
        Yamete = "Yamete Kudasai"
        dejavu = "Déjà Vu"
        fortnite = "FoRtnItE"
        giornos = "Giornos"
        ilike = "I like your cut g"
        Marseillaise = "La Marseillaise"
        chad = "Chad"
        if select.values[0] == Bara:
         select.disabled = True
         await interaction.response.edit_message(view=self)
         if voice_channel != None:
                vc = await voice_channel.connect()
                vc.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg.exe", source=r"C:\Users\Martin\Desktop\Discord_Bobot\bara.mp3"))
                while vc.is_playing():
                    time.sleep(.1)
                await vc.disconnect()
                await message_soundboard.delete()
        if select.values[0] == Putin:
         select.disabled = True
         await interaction.response.edit_message(view=self)
         if voice_channel != None:
                vc = await voice_channel.connect()
                vc.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg.exe", source=r"C:\Users\Martin\Desktop\Discord_Bobot\putin.mp3"))
                while vc.is_playing():
                    time.sleep(.1)
                await vc.disconnect()
                await message_soundboard.delete()
        if select.values[0] == Pootis:
         select.disabled = True
         await interaction.response.edit_message(view=self)
         if voice_channel != None:
                vc = await voice_channel.connect()
                vc.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg.exe", source=r"C:\Users\Martin\Desktop\Discord_Bobot\pootis.mp3"))
                while vc.is_playing():
                    time.sleep(.2)
                await vc.disconnect()
                await message_soundboard.delete()
        if select.values[0] == Yamete:
         select.disabled = True
         await interaction.response.edit_message(view=self)
         if voice_channel != None:
                vc = await voice_channel.connect()
                vc.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg.exe", source=r"C:\Users\Martin\Desktop\Discord_Bobot\Yamete.mp3"))
                while vc.is_playing():
                    time.sleep(.1)
                await vc.disconnect() 
                await message_soundboard.delete()
        if select.values[0] == dejavu:
         select.disabled = True
         await interaction.response.edit_message(view=self)
         if voice_channel != None:
                vc = await voice_channel.connect()
                vc.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg.exe", source=r"C:\Users\Martin\Desktop\Discord_Bobot\dejavu.mp3"))
                while vc.is_playing():
                    time.sleep(.1)
                await vc.disconnect() 
                await message_soundboard.delete()
        if select.values[0] == fortnite:
         select.disabled = True
         await interaction.response.edit_message(view=self)
         if voice_channel != None:
                vc = await voice_channel.connect()
                vc.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg.exe", source=r"C:\Users\Martin\Desktop\Discord_Bobot\fortnite.mp3"))
                while vc.is_playing():
                    time.sleep(.1)
                await vc.disconnect()  
                await message_soundboard.delete()
        if select.values[0] == giornos:
         select.disabled = True
         await interaction.response.edit_message(view=self)
         if voice_channel != None:
                vc = await voice_channel.connect()
                vc.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg.exe", source=r"C:\Users\Martin\Desktop\Discord_Bobot\giornos.mp3"))
                while vc.is_playing():
                    time.sleep(.1)
                await vc.disconnect()  
                await message_soundboard.delete()
        if select.values[0] == ilike:
         select.disabled = True
         await interaction.response.edit_message(view=self)
         if voice_channel != None:
                vc = await voice_channel.connect()
                vc.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg.exe", source=r"C:\Users\Martin\Desktop\Discord_Bobot\ilike.mp3"))
                while vc.is_playing():
                    time.sleep(.1)
                await vc.disconnect()  
                await message_soundboard.delete()
        if select.values[0] == Marseillaise:
         select.disabled = True
         await interaction.response.edit_message(view=self)
         if voice_channel != None:
                vc = await voice_channel.connect()
                vc.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg.exe", source=r"C:\Users\Martin\Desktop\Discord_Bobot\LaMarseillaise.mp3"))
                while vc.is_playing():
                    time.sleep(.1)
                await vc.disconnect() 
                await message_soundboard.delete()
        if select.values[0] == chad:
         select.disabled = True
         await interaction.response.edit_message(view=self)
         if voice_channel != None:
                vc = await voice_channel.connect()
                vc.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/ffmpeg.exe", source=r"C:\Users\Martin\Desktop\Discord_Bobot\Gigachad.mp3"))
                while vc.is_playing():
                    time.sleep(.1)
                await vc.disconnect()  
                await message_soundboard.delete()


@bot.slash_command(description="Faire apparaitre une soundboard...")
async def sb(ctx):
    global voice_channel
    voice_channel = ctx.author.voice.channel
    global message_soundboard
    message_soundboard = await ctx.send("Une soundboard sauvage apparait...", view=MyView())


class MyView107(discord.ui.View):
    @discord.ui.select(
        placeholder = "Choisis un jeu",
        min_values = 1,
        max_values = 1, 
        options = [ 
            discord.SelectOption(
                emoji="<:tf2:1010996503252324452>",
                label="TF2",
                description="Jouer à TF2",
            ),
            discord.SelectOption(
                emoji="<:autopet:1010996489599852554>",
                label="Super Auto Pet",
                description="Jouer à auto pet"
            )
        ])
    async def select_callback(self, select, interaction):
        if select.values[0] == "TF2":
            os.startfile(r"steam://rungameid/440")
            await message_launcher.delete()


        if select.values[0] == "Super Auto Pet":
            os.startfile(r"steam://rungameid/1714040")
            await message_launcher.delete()

@bot.slash_command(description="Lancer des Jeux depuis discord (j'avais rien d'autre a foutre de ma vie)")
async def steam(ctx):
    user_id = ctx.user.id
    if user_id == 727600890793558176:
        global message_launcher
        message_launcher = await ctx.send("", view=MyView107())
    else:
        await ctx.send("Rip t'as pas le droit de faire la commande")

  


@bot.slash_command(description="Nombre de pompes entre 0-100")
async def pompes(ctx):
    user = ctx.user.mention
    push_up = list(range(0, 101))
    result = random.choice(push_up)
    print(result)
    await ctx.send(f"{user} doit faire {result} pompe(s)")


bot.run("token")

