# -*- coding: utf-8 -*-
import discord, urllib.request, time, datetime, fileinput, requests, ast, sys, contextlib, decimal, html, base64, math, itertools, re, asyncio, shutil, PIL.ImageOps, urllib, io, array, binascii, os, hashlib, traceback, subprocess, codecs, pokeapi, sqlite3, concurrent.futures as futures, math, wave, struct, discord.utils, numpy as np, random as modnar, html, dbl, logging, aiohttp, whois as wis, pycountry, socket
from twitch import TwitchClient
from bitstring import BitArray
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from io import StringIO
from discord.ext.commands import Bot
from discord.ext import commands
from discord import *
from urllib.request import urlopen,Request
from mcstatus import MinecraftServer
from difflib import SequenceMatcher
from PIL import Image
from sys import argv, executable
from tempfile import NamedTemporaryFile
from subprocess import check_output
from steampy.client import SteamClient, Asset
from steampy.utils import GameOptions
from pydub import AudioSegment
from googletrans import Translator
from discord.ext.commands import Paginator

AudioSegment.converter = "C:/Users/Administrator/Desktop/FFMPEG/ffmpeg-20180828-26dc763-win64-static/bin/ffmpeg.exe"

async def Paginator(message, x):
    current = 0
    botmsg = await message.channel.send(embed=x[current])
    await botmsg.add_reaction("⏪")
    await botmsg.add_reaction("◀")
    await botmsg.add_reaction("▶")
    await botmsg.add_reaction("⏩")
    await botmsg.add_reaction("⏹")
    await botmsg.add_reaction("\U0001F522")
    while(True):
        def change(reaction, user):
            return user == message.author

        try:
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=change)
        except futures.TimeoutError:
            await message.channel.delete_messages([botmsg])
            break
        else:
            if(str(reaction.emoji) == "▶"):
                try:
                    current += 1
                    await botmsg.edit(embed=x[current])
                    await botmsg.remove_reaction(reaction, message.guild.get_member(user.id))
                except IndexError:
                    current -= 1
                    await botmsg.remove_reaction(reaction, message.guild.get_member(user.id))
            elif(str(reaction.emoji) == "◀"):
                if(current > 0):
                    current -= 1
                    await botmsg.edit(embed=x[current])
                    await botmsg.remove_reaction(reaction, message.guild.get_member(user.id))
                else:
                    current += 1
                    await botmsg.remove_reaction(reaction, message.guild.get_member(user.id))
            elif(str(reaction.emoji) == "⏪"):
                current = 0
                await botmsg.edit(embed=x[current])
                await botmsg.remove_reaction(reaction, message.guild.get_member(user.id))
            elif(str(reaction.emoji) == "⏩"):
                current = len(x) - 1
                await botmsg.edit(embed=x[current])
                await botmsg.remove_reaction(reaction, message.guild.get_member(user.id))
            elif(str(reaction.emoji) == "⏹"):
                await botmsg.delete()
                break
            elif(str(reaction.emoji) == "\U0001F522"):
                msg = await client.wait_for('message', check=check)
                current = int(msg.content)
                if(current > 100):
                    current = 100
                elif(current < 1):
                    current = 1
                await botmsg.edit(embed=x[current])
                await botmsg.remove_reaction(reaction, message.guild.get_member(user.id))
                await msg.delete()
            continue

def robbd(s):
    s = base64.b64decode(s.encode('utf-8')).decode()
    s2 = ""
    if (len(s) < 5):
        for i in range(len(s)):
            s2 = s2 + "26364"[i]
    elif (len(s) > 5):
        while (len(s2) < len(s)):
            s2 = s2 + "26364"
        while (len(s2) != len(s)):
            s2 = list(s2)
            s2.pop(-1)
            s2 = ''.join(s2)
    out = ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s, s2))
    return out;

bot_prefix = "mb!"
client = commands.Bot(command_prefix=bot_prefix)

client.remove_command('help')
channel = ""
los = {}

dtupt = datetime.datetime.now()

@client.event
async def on_message(message):
    conn = sqlite3.connect('Prefixes.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Prefixes")
    user_id = message.author.id
    buffer = c.fetchall()
    data = [i[0] for i in buffer]
    c.close()
    conn.close()
    if(user_id in data):
        cprefix = buffer[data.index(user_id)][-1]
        if(message.content.startswith(cprefix) and not message.author.bot):
            payload = {"server_count": len(client.guilds)}
            async with aiohttp.ClientSession() as aioclient:
                await aioclient.post("https://discordbots.org/api/bots/" + str(client.user.id) + "/stats", data=payload, headers={"Authorization": open("DBL.txt").read()})
            x = 0
            for server in client.guilds:
                for user in server.members:
                    if(not user.bot):
                        x += 1
            payload = {"guilds": len(client.guilds), "users": x}
            async with aiohttp.ClientSession() as aioclient:
                await aioclient.post("https://discordbotlist.com/api/bots/" + str(client.user.id) + "/stats", data=payload, headers={"Authorization": open("DISCORDBOTLIST.COM.txt").read()})
            message.content = "mb!" + message.content[len(cprefix):]
            await client.process_commands(message)
    else:
        if(message.content.startswith("mb!") and not message.author.bot):
            payload = {"server_count": len(client.guilds)}
            async with aiohttp.ClientSession() as aioclient:
                await aioclient.post("https://discordbots.org/api/bots/" + str(client.user.id) + "/stats", data=payload, headers={"Authorization": open("DBL.txt").read()})
            x = 0
            for server in client.guilds:
                for user in server.members:
                    if(not user.bot):
                        x += 1
            payload = {"guilds": len(client.guilds), "users": x}
            async with aiohttp.ClientSession() as aioclient:
                await aioclient.post("https://discordbotlist.com/api/bots/" + str(client.user.id) + "/stats", data=payload, headers={"Authorization": open("DISCORDBOTLIST.COM.txt").read()})
            await client.process_commands(message)

@client.event
async def on_server_remove(server):
    game = discord.Game('for mb!help | Currently in ' + str(len(client.guilds) - 1) + ' servers!', type=discord.ActivityType.watching)
    await client.change_presence(activity=game)
    payload = {"server_count": len(client.guilds)}
    async with aiohttp.ClientSession() as aioclient:
        await aioclient.post("https://discordbots.org/api/bots/" + str(client.user.id) + "/stats", data=payload, headers={"Authorization": open("DBL.txt").read()})

@client.event
async def on_server_join(server):
    conn = sqlite3.connect('WTP.db')
    c = conn.cursor()
    for i in server.channels:
        try:
            if(type(i) == discord.channel.TextChannel):
                dcid = i.id
                c.execute("INSERT INTO WTP VALUES(?, ?, ?)", (str(dcid), "", str(server.id)))
        except:
            continue
    conn.commit()
    game = discord.Game('for mb!help | Currently in ' + str(len(client.guilds)) + ' servers!', type=discord.ActivityType.watching)
    await client.change_presence(activity=game)
    payload = {"server_count": len(client.guilds)}
    async with aiohttp.ClientSession() as aioclient:
        await aioclient.post("https://discordbots.org/api/bots/" + str(client.user.id) + "/stats", data=payload, headers={"Authorization": open("DBL.txt").read()})

@client.event
async def on_ready():
    print("Bot Online")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))
    game = discord.Game('for mb!help | Currently in ' + str(len(client.guilds)) + ' servers!', type=discord.ActivityType.watching)
    await client.change_presence(activity=game)
    payload = {"server_count": len(client.guilds)}
    async with aiohttp.ClientSession() as aioclient:
        await aioclient.post("https://discordbots.org/api/bots/" + str(client.user.id) + "/stats", data=payload, headers={"Authorization": open("DBL.txt").read()})

@client.command(pass_context=True)
async def setprefix(ctx, *args):
    prefix = ' '.join(args)
    conn = sqlite3.connect('Prefixes.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Prefixes")
    user_id = ctx.message.author.id
    data = [i[0] for i in c.fetchall()]
    if(user_id in data):
        c.execute("UPDATE Prefixes SET Prefix = ? WHERE ClientID = ?", (prefix, user_id))
        conn.commit()
        c.close()
        conn.close()
    else:
        c.execute("INSERT INTO Prefixes VALUES(?, ?)", (user_id, prefix))
        conn.commit()
        c.close()
        conn.close()
    await ctx.message.channel.send("Prefix set to ***__" + prefix + "__***!")

@client.command(pass_context=True, aliases=["lookup", "domain"])
async def whois(ctx, website):
    try:
        wi = wis.whois(website)
        if(wi['domain_name'] == None):
            await ctx.message.channel.send('Domain not found!')
        else:
            emb = (discord.Embed(colour=0xf7b8cf))
            ud = wi['updated_date']
            emb.set_author(name=website, url=('http://' + website if not website.startswith('http') else website))
            if(wi['registrar']):
                emb.add_field(name="Registrar", value=wi['registrar'])
            if(wi['creation_date']):
                if(type(wi['creation_date']) != type([])):
                    emb.add_field(name="Creation Date", value=wi['creation_date'].strftime("%A, %b %d, %Y at %I:%M:%S %p UTC"))
                else:
                    emb.add_field(name="Creation Date", value=wi['creation_date'][-1].strftime("%A, %b %d, %Y at %I:%M:%S %p UTC"))
            if(ud):
                emb.add_field(name="Updated Date", value=(ud.strftime("%A, %b %d, %Y at %I:%M:%S %p UTC") if type(ud) != type([]) else ud[-1].strftime("%A, %b %d, %Y at %I:%M:%S %p UTC")))
            if(wi['expiration_date']):
                emb.add_field(name="Expiration Date", value=(wi['expiration_date'].strftime("%A, %b %d, %Y at %I:%M:%S %p UTC") if type(wi['expiration_date']) != type([]) else wi['expiration_date'][-1].strftime("%A, %b %d, %Y at %I:%M:%S %p UTC")))
            if(wi['name']):
                emb.add_field(name="Name", value=wi['name'])
            if(wi['org']):
                emb.add_field(name="Organization", value=wi['org'])
            if(wi['address']):
                emb.add_field(name="Address", value=wi['address'])
            try:
                emb.add_field(name="Location", value=wi['city'] + ", " + wi['state'] + pycountry.countries.get(alpha_2=wi['country']).name + " " + ("" if len(wi['zipcode']) != 5 or zipcode == "00000" else wi['zipcode']))
            except:
                ' '
            await ctx.message.channel.send(embed=emb)
    except (socket.timeout, ConnectionResetError):
        await ctx.message.channel.send('Timeout occurred when connecting to ' + website)

@client.command(pass_context=True, aliases=["8ball", "8b"], description="Try your luck with the 8ball!", brief='<DESCRIPTION>')
async def eightball(ctx, *args):
    message = ' '.join(args)
    out = ""
    out += ":8ball: " + str(ctx.message.author.mention) + ": " + message + "\nMy Response: " + modnar.choice(["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes - definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.", "Reply hazy, try again", "Ask again later.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "My reply is no.", "My sources say no", "Outlook not so good.", "Very doubtful"])
    await ctx.message.channel.send(out)

def savepokemon(ctx):
    z = ['https://cdn.bulbagarden.net/upload/2/21/001Bulbasaur.png', 'https://cdn.bulbagarden.net/upload/7/73/002Ivysaur.png', 'https://cdn.bulbagarden.net/upload/a/ae/003Venusaur.png', 'https://cdn.bulbagarden.net/upload/7/73/004Charmander.png', 'https://cdn.bulbagarden.net/upload/4/4a/005Charmeleon.png', 'https://cdn.bulbagarden.net/upload/7/7e/006Charizard.png', 'https://cdn.bulbagarden.net/upload/3/39/007Squirtle.png', 'https://cdn.bulbagarden.net/upload/0/0c/008Wartortle.png', 'https://cdn.bulbagarden.net/upload/0/02/009Blastoise.png', 'https://cdn.bulbagarden.net/upload/5/5d/010Caterpie.png', 'https://cdn.bulbagarden.net/upload/c/cd/011Metapod.png', 'https://cdn.bulbagarden.net/upload/d/d1/012Butterfree.png', 'https://cdn.bulbagarden.net/upload/d/df/013Weedle.png', 'https://cdn.bulbagarden.net/upload/f/f0/014Kakuna.png', 'https://cdn.bulbagarden.net/upload/6/61/015Beedrill.png', 'https://cdn.bulbagarden.net/upload/5/55/016Pidgey.png', 'https://cdn.bulbagarden.net/upload/7/7a/017Pidgeotto.png', 'https://cdn.bulbagarden.net/upload/5/57/018Pidgeot.png', 'https://cdn.bulbagarden.net/upload/4/46/019Rattata.png', 'https://cdn.bulbagarden.net/upload/f/f4/020Raticate.png', 'https://cdn.bulbagarden.net/upload/8/8b/021Spearow.png', 'https://cdn.bulbagarden.net/upload/a/a0/022Fearow.png', 'https://cdn.bulbagarden.net/upload/f/fa/023Ekans.png', 'https://cdn.bulbagarden.net/upload/c/cd/024Arbok.png', 'https://cdn.bulbagarden.net/upload/0/0d/025Pikachu.png', 'https://cdn.bulbagarden.net/upload/8/88/026Raichu.png', 'https://cdn.bulbagarden.net/upload/9/9e/027Sandshrew.png', 'https://cdn.bulbagarden.net/upload/0/0b/028Sandslash.png', 'https://cdn.bulbagarden.net/upload/8/81/029Nidoran.png', 'https://cdn.bulbagarden.net/upload/c/cd/030Nidorina.png', 'https://cdn.bulbagarden.net/upload/b/bf/031Nidoqueen.png', 'https://cdn.bulbagarden.net/upload/4/4a/032Nidoran.png', 'https://cdn.bulbagarden.net/upload/9/9f/033Nidorino.png', 'https://cdn.bulbagarden.net/upload/c/c6/034Nidoking.png', 'https://cdn.bulbagarden.net/upload/f/f4/035Clefairy.png', 'https://cdn.bulbagarden.net/upload/a/a9/036Clefable.png', 'https://cdn.bulbagarden.net/upload/6/60/037Vulpix.png', 'https://cdn.bulbagarden.net/upload/0/05/038Ninetales.png', 'https://cdn.bulbagarden.net/upload/3/3e/039Jigglypuff.png', 'https://cdn.bulbagarden.net/upload/9/92/040Wigglytuff.png', 'https://cdn.bulbagarden.net/upload/d/da/041Zubat.png', 'https://cdn.bulbagarden.net/upload/0/0c/042Golbat.png', 'https://cdn.bulbagarden.net/upload/4/43/043Oddish.png', 'https://cdn.bulbagarden.net/upload/2/2a/044Gloom.png', 'https://cdn.bulbagarden.net/upload/6/6a/045Vileplume.png', 'https://cdn.bulbagarden.net/upload/d/d4/046Paras.png', 'https://cdn.bulbagarden.net/upload/8/80/047Parasect.png', 'https://cdn.bulbagarden.net/upload/a/ad/048Venonat.png', 'https://cdn.bulbagarden.net/upload/d/d3/049Venomoth.png', 'https://cdn.bulbagarden.net/upload/3/31/050Diglett.png', 'https://cdn.bulbagarden.net/upload/e/e5/051Dugtrio.png', 'https://cdn.bulbagarden.net/upload/d/d6/052Meowth.png', 'https://cdn.bulbagarden.net/upload/1/13/053Persian.png', 'https://cdn.bulbagarden.net/upload/5/53/054Psyduck.png', 'https://cdn.bulbagarden.net/upload/f/fe/055Golduck.png', 'https://cdn.bulbagarden.net/upload/4/41/056Mankey.png', 'https://cdn.bulbagarden.net/upload/9/9a/057Primeape.png', 'https://cdn.bulbagarden.net/upload/3/3d/058Growlithe.png', 'https://cdn.bulbagarden.net/upload/b/b8/059Arcanine.png', 'https://cdn.bulbagarden.net/upload/4/49/060Poliwag.png', 'https://cdn.bulbagarden.net/upload/a/a9/061Poliwhirl.png', 'https://cdn.bulbagarden.net/upload/2/2d/062Poliwrath.png', 'https://cdn.bulbagarden.net/upload/6/62/063Abra.png', 'https://cdn.bulbagarden.net/upload/9/97/064Kadabra.png', 'https://cdn.bulbagarden.net/upload/c/cc/065Alakazam.png', 'https://cdn.bulbagarden.net/upload/8/85/066Machop.png', 'https://cdn.bulbagarden.net/upload/8/8e/067Machoke.png', 'https://cdn.bulbagarden.net/upload/8/8f/068Machamp.png', 'https://cdn.bulbagarden.net/upload/a/a2/069Bellsprout.png', 'https://cdn.bulbagarden.net/upload/9/9f/070Weepinbell.png', 'https://cdn.bulbagarden.net/upload/b/be/071Victreebel.png', 'https://cdn.bulbagarden.net/upload/4/4e/072Tentacool.png', 'https://cdn.bulbagarden.net/upload/f/f6/073Tentacruel.png', 'https://cdn.bulbagarden.net/upload/9/98/074Geodude.png', 'https://cdn.bulbagarden.net/upload/7/75/075Graveler.png', 'https://cdn.bulbagarden.net/upload/f/f2/076Golem.png', 'https://cdn.bulbagarden.net/upload/3/3b/077Ponyta.png', 'https://cdn.bulbagarden.net/upload/3/3f/078Rapidash.png', 'https://cdn.bulbagarden.net/upload/7/70/079Slowpoke.png', 'https://cdn.bulbagarden.net/upload/8/80/080Slowbro.png', 'https://cdn.bulbagarden.net/upload/6/6c/081Magnemite.png', 'https://cdn.bulbagarden.net/upload/7/72/082Magneton.png', 'https://cdn.bulbagarden.net/upload/f/f8/083Farfetch%27d.png', 'https://cdn.bulbagarden.net/upload/5/54/084Doduo.png', 'https://cdn.bulbagarden.net/upload/9/93/085Dodrio.png', 'https://cdn.bulbagarden.net/upload/1/1f/086Seel.png', 'https://cdn.bulbagarden.net/upload/c/c7/087Dewgong.png', 'https://cdn.bulbagarden.net/upload/a/a0/088Grimer.png', 'https://cdn.bulbagarden.net/upload/7/7c/089Muk.png', 'https://cdn.bulbagarden.net/upload/4/40/090Shellder.png', 'https://cdn.bulbagarden.net/upload/1/1d/091Cloyster.png', 'https://cdn.bulbagarden.net/upload/c/ca/092Gastly.png', 'https://cdn.bulbagarden.net/upload/6/62/093Haunter.png', 'https://cdn.bulbagarden.net/upload/c/c6/094Gengar.png', 'https://cdn.bulbagarden.net/upload/9/9a/095Onix.png', 'https://cdn.bulbagarden.net/upload/3/3e/096Drowzee.png', 'https://cdn.bulbagarden.net/upload/0/0a/097Hypno.png', 'https://cdn.bulbagarden.net/upload/a/a7/098Krabby.png', 'https://cdn.bulbagarden.net/upload/7/71/099Kingler.png', 'https://cdn.bulbagarden.net/upload/d/da/100Voltorb.png', 'https://cdn.bulbagarden.net/upload/8/84/101Electrode.png', 'https://cdn.bulbagarden.net/upload/a/af/102Exeggcute.png', 'https://cdn.bulbagarden.net/upload/2/24/103Exeggutor.png', 'https://cdn.bulbagarden.net/upload/2/2a/104Cubone.png', 'https://cdn.bulbagarden.net/upload/9/98/105Marowak.png', 'https://cdn.bulbagarden.net/upload/3/32/106Hitmonlee.png', 'https://cdn.bulbagarden.net/upload/a/a3/107Hitmonchan.png', 'https://cdn.bulbagarden.net/upload/0/00/108Lickitung.png', 'https://cdn.bulbagarden.net/upload/1/17/109Koffing.png', 'https://cdn.bulbagarden.net/upload/4/42/110Weezing.png', 'https://cdn.bulbagarden.net/upload/9/9b/111Rhyhorn.png', 'https://cdn.bulbagarden.net/upload/4/47/112Rhydon.png', 'https://cdn.bulbagarden.net/upload/c/cd/113Chansey.png', 'https://cdn.bulbagarden.net/upload/3/3e/114Tangela.png', 'https://cdn.bulbagarden.net/upload/4/4e/115Kangaskhan.png', 'https://cdn.bulbagarden.net/upload/5/5a/116Horsea.png', 'https://cdn.bulbagarden.net/upload/2/26/117Seadra.png', 'https://cdn.bulbagarden.net/upload/7/7b/118Goldeen.png', 'https://cdn.bulbagarden.net/upload/6/6a/119Seaking.png', 'https://cdn.bulbagarden.net/upload/4/4f/120Staryu.png', 'https://cdn.bulbagarden.net/upload/c/cd/121Starmie.png', 'https://cdn.bulbagarden.net/upload/e/ec/122Mr._Mime.png', 'https://cdn.bulbagarden.net/upload/b/ba/123Scyther.png', 'https://cdn.bulbagarden.net/upload/7/7c/124Jynx.png', 'https://cdn.bulbagarden.net/upload/d/de/125Electabuzz.png', 'https://cdn.bulbagarden.net/upload/8/8c/126Magmar.png', 'https://cdn.bulbagarden.net/upload/7/71/127Pinsir.png', 'https://cdn.bulbagarden.net/upload/b/b8/128Tauros.png', 'https://cdn.bulbagarden.net/upload/0/02/129Magikarp.png', 'https://cdn.bulbagarden.net/upload/4/41/130Gyarados.png', 'https://cdn.bulbagarden.net/upload/a/ab/131Lapras.png', 'https://cdn.bulbagarden.net/upload/3/36/132Ditto.png', 'https://cdn.bulbagarden.net/upload/e/e2/133Eevee.png', 'https://cdn.bulbagarden.net/upload/f/fd/134Vaporeon.png', 'https://cdn.bulbagarden.net/upload/b/bb/135Jolteon.png', 'https://cdn.bulbagarden.net/upload/d/dd/136Flareon.png', 'https://cdn.bulbagarden.net/upload/6/6b/137Porygon.png', 'https://cdn.bulbagarden.net/upload/7/79/138Omanyte.png', 'https://cdn.bulbagarden.net/upload/4/43/139Omastar.png', 'https://cdn.bulbagarden.net/upload/f/f9/140Kabuto.png', 'https://cdn.bulbagarden.net/upload/2/29/141Kabutops.png', 'https://cdn.bulbagarden.net/upload/e/e8/142Aerodactyl.png', 'https://cdn.bulbagarden.net/upload/f/fb/143Snorlax.png', 'https://cdn.bulbagarden.net/upload/4/4e/144Articuno.png', 'https://cdn.bulbagarden.net/upload/e/e3/145Zapdos.png', 'https://cdn.bulbagarden.net/upload/1/1b/146Moltres.png', 'https://cdn.bulbagarden.net/upload/c/cc/147Dratini.png', 'https://cdn.bulbagarden.net/upload/9/93/148Dragonair.png', 'https://cdn.bulbagarden.net/upload/8/8b/149Dragonite.png', 'https://cdn.bulbagarden.net/upload/7/78/150Mewtwo.png', 'https://cdn.bulbagarden.net/upload/b/b1/151Mew.png', 'https://cdn.bulbagarden.net/upload/b/bf/152Chikorita.png', 'https://cdn.bulbagarden.net/upload/c/ca/153Bayleef.png', 'https://cdn.bulbagarden.net/upload/d/d1/154Meganium.png', 'https://cdn.bulbagarden.net/upload/9/9b/155Cyndaquil.png', 'https://cdn.bulbagarden.net/upload/b/b6/156Quilava.png', 'https://cdn.bulbagarden.net/upload/4/47/157Typhlosion.png', 'https://cdn.bulbagarden.net/upload/d/df/158Totodile.png', 'https://cdn.bulbagarden.net/upload/a/a5/159Croconaw.png', 'https://cdn.bulbagarden.net/upload/d/d5/160Feraligatr.png', 'https://cdn.bulbagarden.net/upload/c/c5/161Sentret.png', 'https://cdn.bulbagarden.net/upload/4/4b/162Furret.png', 'https://cdn.bulbagarden.net/upload/5/53/163Hoothoot.png', 'https://cdn.bulbagarden.net/upload/f/fa/164Noctowl.png', 'https://cdn.bulbagarden.net/upload/b/bb/165Ledyba.png', 'https://cdn.bulbagarden.net/upload/5/5b/166Ledian.png', 'https://cdn.bulbagarden.net/upload/7/75/167Spinarak.png', 'https://cdn.bulbagarden.net/upload/7/76/168Ariados.png', 'https://cdn.bulbagarden.net/upload/1/17/169Crobat.png', 'https://cdn.bulbagarden.net/upload/d/d9/170Chinchou.png', 'https://cdn.bulbagarden.net/upload/9/9b/171Lanturn.png', 'https://cdn.bulbagarden.net/upload/b/b9/172Pichu.png', 'https://cdn.bulbagarden.net/upload/e/e4/173Cleffa.png', 'https://cdn.bulbagarden.net/upload/4/4d/174Igglybuff.png', 'https://cdn.bulbagarden.net/upload/6/6b/175Togepi.png', 'https://cdn.bulbagarden.net/upload/1/11/176Togetic.png', 'https://cdn.bulbagarden.net/upload/5/5b/177Natu.png', 'https://cdn.bulbagarden.net/upload/f/f4/178Xatu.png', 'https://cdn.bulbagarden.net/upload/6/6b/179Mareep.png', 'https://cdn.bulbagarden.net/upload/6/6f/180Flaaffy.png', 'https://cdn.bulbagarden.net/upload/4/47/181Ampharos.png', 'https://cdn.bulbagarden.net/upload/c/cd/182Bellossom.png', 'https://cdn.bulbagarden.net/upload/4/42/183Marill.png', 'https://cdn.bulbagarden.net/upload/a/a5/184Azumarill.png', 'https://cdn.bulbagarden.net/upload/1/1e/185Sudowoodo.png', 'https://cdn.bulbagarden.net/upload/a/a4/186Politoed.png', 'https://cdn.bulbagarden.net/upload/f/f8/187Hoppip.png', 'https://cdn.bulbagarden.net/upload/4/4f/188Skiploom.png', 'https://cdn.bulbagarden.net/upload/5/5e/189Jumpluff.png', 'https://cdn.bulbagarden.net/upload/4/42/190Aipom.png', 'https://cdn.bulbagarden.net/upload/9/95/191Sunkern.png', 'https://cdn.bulbagarden.net/upload/9/98/192Sunflora.png', 'https://cdn.bulbagarden.net/upload/d/dd/193Yanma.png', 'https://cdn.bulbagarden.net/upload/7/78/194Wooper.png', 'https://cdn.bulbagarden.net/upload/a/a4/195Quagsire.png', 'https://cdn.bulbagarden.net/upload/a/a7/196Espeon.png', 'https://cdn.bulbagarden.net/upload/3/3d/197Umbreon.png', 'https://cdn.bulbagarden.net/upload/3/33/198Murkrow.png', 'https://cdn.bulbagarden.net/upload/e/e1/199Slowking.png', 'https://cdn.bulbagarden.net/upload/b/be/200Misdreavus.png', 'https://cdn.bulbagarden.net/upload/7/77/201Unown.png', 'https://cdn.bulbagarden.net/upload/1/17/202Wobbuffet.png', 'https://cdn.bulbagarden.net/upload/1/11/203Girafarig.png', 'https://cdn.bulbagarden.net/upload/0/0b/204Pineco.png', 'https://cdn.bulbagarden.net/upload/6/68/205Forretress.png', 'https://cdn.bulbagarden.net/upload/2/20/206Dunsparce.png', 'https://cdn.bulbagarden.net/upload/0/04/207Gligar.png', 'https://cdn.bulbagarden.net/upload/b/ba/208Steelix.png', 'https://cdn.bulbagarden.net/upload/7/7f/209Snubbull.png', 'https://cdn.bulbagarden.net/upload/b/b1/210Granbull.png', 'https://cdn.bulbagarden.net/upload/2/21/211Qwilfish.png', 'https://cdn.bulbagarden.net/upload/5/55/212Scizor.png', 'https://cdn.bulbagarden.net/upload/c/c7/213Shuckle.png', 'https://cdn.bulbagarden.net/upload/4/47/214Heracross.png', 'https://cdn.bulbagarden.net/upload/7/71/215Sneasel.png', 'https://cdn.bulbagarden.net/upload/e/e9/216Teddiursa.png', 'https://cdn.bulbagarden.net/upload/e/e9/217Ursaring.png', 'https://cdn.bulbagarden.net/upload/6/68/218Slugma.png', 'https://cdn.bulbagarden.net/upload/6/65/219Magcargo.png', 'https://cdn.bulbagarden.net/upload/b/b5/220Swinub.png', 'https://cdn.bulbagarden.net/upload/4/49/221Piloswine.png', 'https://cdn.bulbagarden.net/upload/f/fc/222Corsola.png', 'https://cdn.bulbagarden.net/upload/9/95/223Remoraid.png', 'https://cdn.bulbagarden.net/upload/c/cb/224Octillery.png', 'https://cdn.bulbagarden.net/upload/3/3f/225Delibird.png', 'https://cdn.bulbagarden.net/upload/c/c5/226Mantine.png', 'https://cdn.bulbagarden.net/upload/3/35/227Skarmory.png', 'https://cdn.bulbagarden.net/upload/5/53/228Houndour.png', 'https://cdn.bulbagarden.net/upload/5/51/229Houndoom.png', 'https://cdn.bulbagarden.net/upload/3/3c/230Kingdra.png', 'https://cdn.bulbagarden.net/upload/d/d3/231Phanpy.png', 'https://cdn.bulbagarden.net/upload/5/53/232Donphan.png', 'https://cdn.bulbagarden.net/upload/9/99/233Porygon2.png', 'https://cdn.bulbagarden.net/upload/5/50/234Stantler.png', 'https://cdn.bulbagarden.net/upload/9/92/235Smeargle.png', 'https://cdn.bulbagarden.net/upload/c/c7/236Tyrogue.png', 'https://cdn.bulbagarden.net/upload/9/94/237Hitmontop.png', 'https://cdn.bulbagarden.net/upload/0/0e/238Smoochum.png', 'https://cdn.bulbagarden.net/upload/5/5d/239Elekid.png', 'https://cdn.bulbagarden.net/upload/c/cb/240Magby.png', 'https://cdn.bulbagarden.net/upload/1/13/241Miltank.png', 'https://cdn.bulbagarden.net/upload/5/56/242Blissey.png', 'https://cdn.bulbagarden.net/upload/c/c1/243Raikou.png', 'https://cdn.bulbagarden.net/upload/f/f9/244Entei.png', 'https://cdn.bulbagarden.net/upload/d/da/245Suicune.png', 'https://cdn.bulbagarden.net/upload/7/70/246Larvitar.png', 'https://cdn.bulbagarden.net/upload/a/a1/247Pupitar.png', 'https://cdn.bulbagarden.net/upload/8/82/248Tyranitar.png', 'https://cdn.bulbagarden.net/upload/4/44/249Lugia.png', 'https://cdn.bulbagarden.net/upload/6/67/250Ho-Oh.png', 'https://cdn.bulbagarden.net/upload/e/e7/251Celebi.png', 'https://cdn.bulbagarden.net/upload/2/2c/252Treecko.png', 'https://cdn.bulbagarden.net/upload/e/ea/253Grovyle.png', 'https://cdn.bulbagarden.net/upload/3/3e/254Sceptile.png', 'https://cdn.bulbagarden.net/upload/9/91/255Torchic.png', 'https://cdn.bulbagarden.net/upload/2/29/256Combusken.png', 'https://cdn.bulbagarden.net/upload/9/90/257Blaziken.png', 'https://cdn.bulbagarden.net/upload/6/60/258Mudkip.png', 'https://cdn.bulbagarden.net/upload/2/27/259Marshtomp.png', 'https://cdn.bulbagarden.net/upload/b/b6/260Swampert.png', 'https://cdn.bulbagarden.net/upload/f/fc/261Poochyena.png', 'https://cdn.bulbagarden.net/upload/f/f1/262Mightyena.png', 'https://cdn.bulbagarden.net/upload/4/47/263Zigzagoon.png', 'https://cdn.bulbagarden.net/upload/f/f7/264Linoone.png', 'https://cdn.bulbagarden.net/upload/7/76/265Wurmple.png', 'https://cdn.bulbagarden.net/upload/e/ef/266Silcoon.png', 'https://cdn.bulbagarden.net/upload/4/4c/267Beautifly.png', 'https://cdn.bulbagarden.net/upload/a/a3/268Cascoon.png', 'https://cdn.bulbagarden.net/upload/3/34/269Dustox.png', 'https://cdn.bulbagarden.net/upload/e/ee/270Lotad.png', 'https://cdn.bulbagarden.net/upload/8/8b/271Lombre.png', 'https://cdn.bulbagarden.net/upload/f/ff/272Ludicolo.png', 'https://cdn.bulbagarden.net/upload/8/84/273Seedot.png', 'https://cdn.bulbagarden.net/upload/0/07/274Nuzleaf.png', 'https://cdn.bulbagarden.net/upload/f/f7/275Shiftry.png', 'https://cdn.bulbagarden.net/upload/e/e4/276Taillow.png', 'https://cdn.bulbagarden.net/upload/4/45/277Swellow.png', 'https://cdn.bulbagarden.net/upload/3/39/278Wingull.png', 'https://cdn.bulbagarden.net/upload/f/f2/279Pelipper.png', 'https://cdn.bulbagarden.net/upload/e/e1/280Ralts.png', 'https://cdn.bulbagarden.net/upload/0/00/281Kirlia.png', 'https://cdn.bulbagarden.net/upload/9/99/282Gardevoir.png', 'https://cdn.bulbagarden.net/upload/f/f6/283Surskit.png', 'https://cdn.bulbagarden.net/upload/0/0a/284Masquerain.png', 'https://cdn.bulbagarden.net/upload/d/d8/285Shroomish.png', 'https://cdn.bulbagarden.net/upload/d/de/286Breloom.png', 'https://cdn.bulbagarden.net/upload/d/d2/287Slakoth.png', 'https://cdn.bulbagarden.net/upload/6/61/288Vigoroth.png', 'https://cdn.bulbagarden.net/upload/7/71/289Slaking.png', 'https://cdn.bulbagarden.net/upload/9/90/290Nincada.png', 'https://cdn.bulbagarden.net/upload/7/76/291Ninjask.png', 'https://cdn.bulbagarden.net/upload/5/59/292Shedinja.png', 'https://cdn.bulbagarden.net/upload/6/6c/293Whismur.png', 'https://cdn.bulbagarden.net/upload/1/12/294Loudred.png', 'https://cdn.bulbagarden.net/upload/1/12/295Exploud.png', 'https://cdn.bulbagarden.net/upload/b/b6/296Makuhita.png', 'https://cdn.bulbagarden.net/upload/6/6f/297Hariyama.png', 'https://cdn.bulbagarden.net/upload/a/ac/298Azurill.png', 'https://cdn.bulbagarden.net/upload/8/89/299Nosepass.png', 'https://cdn.bulbagarden.net/upload/8/8a/300Skitty.png', 'https://cdn.bulbagarden.net/upload/f/f4/301Delcatty.png', 'https://cdn.bulbagarden.net/upload/d/d3/302Sableye.png', 'https://cdn.bulbagarden.net/upload/c/c0/303Mawile.png', 'https://cdn.bulbagarden.net/upload/b/bb/304Aron.png', 'https://cdn.bulbagarden.net/upload/b/bf/305Lairon.png', 'https://cdn.bulbagarden.net/upload/6/6d/306Aggron.png', 'https://cdn.bulbagarden.net/upload/7/71/307Meditite.png', 'https://cdn.bulbagarden.net/upload/0/05/308Medicham.png', 'https://cdn.bulbagarden.net/upload/4/47/309Electrike.png', 'https://cdn.bulbagarden.net/upload/b/bb/310Manectric.png', 'https://cdn.bulbagarden.net/upload/a/a3/311Plusle.png', 'https://cdn.bulbagarden.net/upload/e/e7/312Minun.png', 'https://cdn.bulbagarden.net/upload/d/d6/313Volbeat.png', 'https://cdn.bulbagarden.net/upload/5/55/314Illumise.png', 'https://cdn.bulbagarden.net/upload/f/f1/315Roselia.png', 'https://cdn.bulbagarden.net/upload/f/f0/316Gulpin.png', 'https://cdn.bulbagarden.net/upload/a/ad/317Swalot.png', 'https://cdn.bulbagarden.net/upload/9/98/318Carvanha.png', 'https://cdn.bulbagarden.net/upload/a/a8/319Sharpedo.png', 'https://cdn.bulbagarden.net/upload/7/71/320Wailmer.png', 'https://cdn.bulbagarden.net/upload/b/b9/321Wailord.png', 'https://cdn.bulbagarden.net/upload/c/c6/322Numel.png', 'https://cdn.bulbagarden.net/upload/7/7d/323Camerupt.png', 'https://cdn.bulbagarden.net/upload/3/3b/324Torkoal.png', 'https://cdn.bulbagarden.net/upload/9/9e/325Spoink.png', 'https://cdn.bulbagarden.net/upload/5/54/326Grumpig.png', 'https://cdn.bulbagarden.net/upload/8/8f/327Spinda.png', 'https://cdn.bulbagarden.net/upload/7/76/328Trapinch.png', 'https://cdn.bulbagarden.net/upload/a/af/329Vibrava.png', 'https://cdn.bulbagarden.net/upload/f/f1/330Flygon.png', 'https://cdn.bulbagarden.net/upload/1/12/331Cacnea.png', 'https://cdn.bulbagarden.net/upload/4/41/332Cacturne.png', 'https://cdn.bulbagarden.net/upload/9/99/333Swablu.png', 'https://cdn.bulbagarden.net/upload/d/da/334Altaria.png', 'https://cdn.bulbagarden.net/upload/d/d3/335Zangoose.png', 'https://cdn.bulbagarden.net/upload/d/d6/336Seviper.png', 'https://cdn.bulbagarden.net/upload/e/eb/337Lunatone.png', 'https://cdn.bulbagarden.net/upload/9/90/338Solrock.png', 'https://cdn.bulbagarden.net/upload/6/60/339Barboach.png', 'https://cdn.bulbagarden.net/upload/6/60/340Whiscash.png', 'https://cdn.bulbagarden.net/upload/3/3d/341Corphish.png', 'https://cdn.bulbagarden.net/upload/f/f4/342Crawdaunt.png', 'https://cdn.bulbagarden.net/upload/8/8b/343Baltoy.png', 'https://cdn.bulbagarden.net/upload/0/07/344Claydol.png', 'https://cdn.bulbagarden.net/upload/3/34/345Lileep.png', 'https://cdn.bulbagarden.net/upload/3/38/346Cradily.png', 'https://cdn.bulbagarden.net/upload/4/45/347Anorith.png', 'https://cdn.bulbagarden.net/upload/1/1d/348Armaldo.png', 'https://cdn.bulbagarden.net/upload/4/4b/349Feebas.png', 'https://cdn.bulbagarden.net/upload/3/36/350Milotic.png', 'https://cdn.bulbagarden.net/upload/f/f3/351Castform.png', 'https://cdn.bulbagarden.net/upload/5/50/352Kecleon.png', 'https://cdn.bulbagarden.net/upload/4/4b/353Shuppet.png', 'https://cdn.bulbagarden.net/upload/0/0a/354Banette.png', 'https://cdn.bulbagarden.net/upload/e/e2/355Duskull.png', 'https://cdn.bulbagarden.net/upload/1/12/356Dusclops.png', 'https://cdn.bulbagarden.net/upload/d/dd/357Tropius.png', 'https://cdn.bulbagarden.net/upload/e/e5/358Chimecho.png', 'https://cdn.bulbagarden.net/upload/0/00/359Absol.png', 'https://cdn.bulbagarden.net/upload/d/d0/360Wynaut.png', 'https://cdn.bulbagarden.net/upload/6/6b/361Snorunt.png', 'https://cdn.bulbagarden.net/upload/6/62/362Glalie.png', 'https://cdn.bulbagarden.net/upload/9/9f/363Spheal.png', 'https://cdn.bulbagarden.net/upload/f/f6/364Sealeo.png', 'https://cdn.bulbagarden.net/upload/6/61/365Walrein.png', 'https://cdn.bulbagarden.net/upload/1/11/366Clamperl.png', 'https://cdn.bulbagarden.net/upload/1/11/367Huntail.png', 'https://cdn.bulbagarden.net/upload/3/37/368Gorebyss.png', 'https://cdn.bulbagarden.net/upload/7/78/369Relicanth.png', 'https://cdn.bulbagarden.net/upload/1/1d/370Luvdisc.png', 'https://cdn.bulbagarden.net/upload/d/d2/371Bagon.png', 'https://cdn.bulbagarden.net/upload/a/a5/372Shelgon.png', 'https://cdn.bulbagarden.net/upload/4/41/373Salamence.png', 'https://cdn.bulbagarden.net/upload/d/d4/374Beldum.png', 'https://cdn.bulbagarden.net/upload/6/62/375Metang.png', 'https://cdn.bulbagarden.net/upload/0/05/376Metagross.png', 'https://cdn.bulbagarden.net/upload/a/aa/377Regirock.png', 'https://cdn.bulbagarden.net/upload/f/fe/378Regice.png', 'https://cdn.bulbagarden.net/upload/2/22/379Registeel.png', 'https://cdn.bulbagarden.net/upload/2/24/380Latias.png', 'https://cdn.bulbagarden.net/upload/5/52/381Latios.png', 'https://cdn.bulbagarden.net/upload/4/41/382Kyogre.png', 'https://cdn.bulbagarden.net/upload/7/70/383Groudon.png', 'https://cdn.bulbagarden.net/upload/e/e4/384Rayquaza.png', 'https://cdn.bulbagarden.net/upload/8/85/385Jirachi.png', 'https://cdn.bulbagarden.net/upload/e/e7/386Deoxys.png', 'https://cdn.bulbagarden.net/upload/5/5c/387Turtwig.png', 'https://cdn.bulbagarden.net/upload/5/53/388Grotle.png', 'https://cdn.bulbagarden.net/upload/d/df/389Torterra.png', 'https://cdn.bulbagarden.net/upload/7/76/390Chimchar.png', 'https://cdn.bulbagarden.net/upload/2/2e/391Monferno.png', 'https://cdn.bulbagarden.net/upload/f/fb/392Infernape.png', 'https://cdn.bulbagarden.net/upload/b/b1/393Piplup.png', 'https://cdn.bulbagarden.net/upload/d/df/394Prinplup.png', 'https://cdn.bulbagarden.net/upload/7/7f/395Empoleon.png', 'https://cdn.bulbagarden.net/upload/a/af/396Starly.png', 'https://cdn.bulbagarden.net/upload/f/f8/397Staravia.png', 'https://cdn.bulbagarden.net/upload/5/5e/398Staraptor.png', 'https://cdn.bulbagarden.net/upload/f/f5/399Bidoof.png', 'https://cdn.bulbagarden.net/upload/9/91/400Bibarel.png', 'https://cdn.bulbagarden.net/upload/3/33/401Kricketot.png', 'https://cdn.bulbagarden.net/upload/e/e5/402Kricketune.png', 'https://cdn.bulbagarden.net/upload/3/32/403Shinx.png', 'https://cdn.bulbagarden.net/upload/4/49/404Luxio.png', 'https://cdn.bulbagarden.net/upload/a/a7/405Luxray.png', 'https://cdn.bulbagarden.net/upload/d/d3/406Budew.png', 'https://cdn.bulbagarden.net/upload/0/05/407Roserade.png', 'https://cdn.bulbagarden.net/upload/c/cd/408Cranidos.png', 'https://cdn.bulbagarden.net/upload/8/8a/409Rampardos.png', 'https://cdn.bulbagarden.net/upload/e/e2/410Shieldon.png', 'https://cdn.bulbagarden.net/upload/b/bc/411Bastiodon.png', 'https://cdn.bulbagarden.net/upload/e/e1/412Burmy.png', 'https://cdn.bulbagarden.net/upload/b/b3/413Wormadam.png', 'https://cdn.bulbagarden.net/upload/1/18/414Mothim.png', 'https://cdn.bulbagarden.net/upload/b/b6/415Combee.png', 'https://cdn.bulbagarden.net/upload/2/2c/416Vespiquen.png', 'https://cdn.bulbagarden.net/upload/f/f4/417Pachirisu.png', 'https://cdn.bulbagarden.net/upload/8/83/418Buizel.png', 'https://cdn.bulbagarden.net/upload/b/bf/419Floatzel.png', 'https://cdn.bulbagarden.net/upload/a/a7/420Cherubi.png', 'https://cdn.bulbagarden.net/upload/2/25/421Cherrim-Overcast.png', 'https://cdn.bulbagarden.net/upload/7/72/422Shellos.png', 'https://cdn.bulbagarden.net/upload/1/18/423Gastrodon.png', 'https://cdn.bulbagarden.net/upload/8/86/424Ambipom.png', 'https://cdn.bulbagarden.net/upload/e/eb/425Drifloon.png', 'https://cdn.bulbagarden.net/upload/7/71/426Drifblim.png', 'https://cdn.bulbagarden.net/upload/a/a7/427Buneary.png', 'https://cdn.bulbagarden.net/upload/c/c9/428Lopunny.png', 'https://cdn.bulbagarden.net/upload/b/b4/429Mismagius.png', 'https://cdn.bulbagarden.net/upload/4/46/430Honchkrow.png', 'https://cdn.bulbagarden.net/upload/2/26/431Glameow.png', 'https://cdn.bulbagarden.net/upload/8/80/432Purugly.png', 'https://cdn.bulbagarden.net/upload/e/ed/433Chingling.png', 'https://cdn.bulbagarden.net/upload/7/75/434Stunky.png', 'https://cdn.bulbagarden.net/upload/b/bc/435Skuntank.png', 'https://cdn.bulbagarden.net/upload/c/c1/436Bronzor.png', 'https://cdn.bulbagarden.net/upload/a/aa/437Bronzong.png', 'https://cdn.bulbagarden.net/upload/e/e2/438Bonsly.png', 'https://cdn.bulbagarden.net/upload/3/37/439Mime_Jr.png', 'https://cdn.bulbagarden.net/upload/2/27/440Happiny.png', 'https://cdn.bulbagarden.net/upload/b/bf/441Chatot.png', 'https://cdn.bulbagarden.net/upload/8/8e/442Spiritomb.png', 'https://cdn.bulbagarden.net/upload/6/68/443Gible.png', 'https://cdn.bulbagarden.net/upload/9/9d/444Gabite.png', 'https://cdn.bulbagarden.net/upload/f/fa/445Garchomp.png', 'https://cdn.bulbagarden.net/upload/b/b2/446Munchlax.png', 'https://cdn.bulbagarden.net/upload/a/a2/447Riolu.png', 'https://cdn.bulbagarden.net/upload/d/d7/448Lucario.png', 'https://cdn.bulbagarden.net/upload/a/ab/449Hippopotas.png', 'https://cdn.bulbagarden.net/upload/5/5f/450Hippowdon.png', 'https://cdn.bulbagarden.net/upload/4/47/451Skorupi.png', 'https://cdn.bulbagarden.net/upload/1/13/452Drapion.png', 'https://cdn.bulbagarden.net/upload/f/fa/453Croagunk.png', 'https://cdn.bulbagarden.net/upload/8/8b/454Toxicroak.png', 'https://cdn.bulbagarden.net/upload/d/df/455Carnivine.png', 'https://cdn.bulbagarden.net/upload/4/45/456Finneon.png', 'https://cdn.bulbagarden.net/upload/f/f0/457Lumineon.png', 'https://cdn.bulbagarden.net/upload/b/bc/458Mantyke.png', 'https://cdn.bulbagarden.net/upload/d/d2/459Snover.png', 'https://cdn.bulbagarden.net/upload/3/3b/460Abomasnow.png', 'https://cdn.bulbagarden.net/upload/d/d2/461Weavile.png', 'https://cdn.bulbagarden.net/upload/5/53/462Magnezone.png', 'https://cdn.bulbagarden.net/upload/8/8e/463Lickilicky.png', 'https://cdn.bulbagarden.net/upload/d/d9/464Rhyperior.png', 'https://cdn.bulbagarden.net/upload/3/32/465Tangrowth.png', 'https://cdn.bulbagarden.net/upload/2/23/466Electivire.png', 'https://cdn.bulbagarden.net/upload/6/60/467Magmortar.png', 'https://cdn.bulbagarden.net/upload/8/87/468Togekiss.png', 'https://cdn.bulbagarden.net/upload/e/e6/469Yanmega.png', 'https://cdn.bulbagarden.net/upload/f/f5/470Leafeon.png', 'https://cdn.bulbagarden.net/upload/2/23/471Glaceon.png', 'https://cdn.bulbagarden.net/upload/a/ac/472Gliscor.png', 'https://cdn.bulbagarden.net/upload/d/d0/473Mamoswine.png', 'https://cdn.bulbagarden.net/upload/2/24/474Porygon-Z.png', 'https://cdn.bulbagarden.net/upload/5/58/475Gallade.png', 'https://cdn.bulbagarden.net/upload/a/a6/476Probopass.png', 'https://cdn.bulbagarden.net/upload/4/4f/477Dusknoir.png', 'https://cdn.bulbagarden.net/upload/a/a2/478Froslass.png', 'https://cdn.bulbagarden.net/upload/c/c5/479Rotom.png', 'https://cdn.bulbagarden.net/upload/e/ef/480Uxie.png', 'https://cdn.bulbagarden.net/upload/4/40/481Mesprit.png', 'https://cdn.bulbagarden.net/upload/d/d0/482Azelf.png', 'https://cdn.bulbagarden.net/upload/8/8a/483Dialga.png', 'https://cdn.bulbagarden.net/upload/6/66/484Palkia.png', 'https://cdn.bulbagarden.net/upload/b/b7/485Heatran.png', 'https://cdn.bulbagarden.net/upload/a/a1/486Regigigas.png', 'https://cdn.bulbagarden.net/upload/c/c5/487Giratina-Altered.png', 'https://cdn.bulbagarden.net/upload/4/4a/488Cresselia.png', 'https://cdn.bulbagarden.net/upload/7/72/489Phione.png', 'https://cdn.bulbagarden.net/upload/2/2e/490Manaphy.png', 'https://cdn.bulbagarden.net/upload/6/6d/491Darkrai.png', 'https://cdn.bulbagarden.net/upload/0/05/492Shaymin-Land.png', 'https://cdn.bulbagarden.net/upload/f/fc/493Arceus.png', 'https://cdn.bulbagarden.net/upload/6/60/494Victini.png', 'https://cdn.bulbagarden.net/upload/7/75/495Snivy.png', 'https://cdn.bulbagarden.net/upload/7/73/496Servine.png', 'https://cdn.bulbagarden.net/upload/b/b7/497Serperior.png', 'https://cdn.bulbagarden.net/upload/5/5b/498Tepig.png', 'https://cdn.bulbagarden.net/upload/e/e8/499Pignite.png', 'https://cdn.bulbagarden.net/upload/1/18/500Emboar.png', 'https://cdn.bulbagarden.net/upload/3/3b/501Oshawott.png', 'https://cdn.bulbagarden.net/upload/e/e4/502Dewott.png', 'https://cdn.bulbagarden.net/upload/b/b5/503Samurott.png', 'https://cdn.bulbagarden.net/upload/c/cb/504Patrat.png', 'https://cdn.bulbagarden.net/upload/3/3e/505Watchog.png', 'https://cdn.bulbagarden.net/upload/7/7e/506Lillipup.png', 'https://cdn.bulbagarden.net/upload/9/96/507Herdier.png', 'https://cdn.bulbagarden.net/upload/3/3e/508Stoutland.png', 'https://cdn.bulbagarden.net/upload/4/46/509Purrloin.png', 'https://cdn.bulbagarden.net/upload/0/09/510Liepard.png', 'https://cdn.bulbagarden.net/upload/6/6b/511Pansage.png', 'https://cdn.bulbagarden.net/upload/2/24/512Simisage.png', 'https://cdn.bulbagarden.net/upload/e/e1/513Pansear.png', 'https://cdn.bulbagarden.net/upload/7/7c/514Simisear.png', 'https://cdn.bulbagarden.net/upload/2/2f/515Panpour.png', 'https://cdn.bulbagarden.net/upload/8/83/516Simipour.png', 'https://cdn.bulbagarden.net/upload/6/61/517Munna.png', 'https://cdn.bulbagarden.net/upload/2/2d/518Musharna.png', 'https://cdn.bulbagarden.net/upload/c/c3/519Pidove.png', 'https://cdn.bulbagarden.net/upload/a/a3/520Tranquill.png', 'https://cdn.bulbagarden.net/upload/d/d0/521Unfezant.png', 'https://cdn.bulbagarden.net/upload/a/af/522Blitzle.png', 'https://cdn.bulbagarden.net/upload/a/a1/523Zebstrika.png', 'https://cdn.bulbagarden.net/upload/6/69/524Roggenrola.png', 'https://cdn.bulbagarden.net/upload/c/ce/525Boldore.png', 'https://cdn.bulbagarden.net/upload/5/59/526Gigalith.png', 'https://cdn.bulbagarden.net/upload/3/36/527Woobat.png', 'https://cdn.bulbagarden.net/upload/9/9d/528Swoobat.png', 'https://cdn.bulbagarden.net/upload/c/cf/529Drilbur.png', 'https://cdn.bulbagarden.net/upload/6/63/530Excadrill.png', 'https://cdn.bulbagarden.net/upload/f/f5/531Audino.png', 'https://cdn.bulbagarden.net/upload/6/69/532Timburr.png', 'https://cdn.bulbagarden.net/upload/a/ad/533Gurdurr.png', 'https://cdn.bulbagarden.net/upload/1/11/534Conkeldurr.png', 'https://cdn.bulbagarden.net/upload/c/c9/535Tympole.png', 'https://cdn.bulbagarden.net/upload/c/c9/536Palpitoad.png', 'https://cdn.bulbagarden.net/upload/3/35/537Seismitoad.png', 'https://cdn.bulbagarden.net/upload/7/74/538Throh.png', 'https://cdn.bulbagarden.net/upload/a/a8/539Sawk.png', 'https://cdn.bulbagarden.net/upload/4/4a/540Sewaddle.png', 'https://cdn.bulbagarden.net/upload/2/2b/541Swadloon.png', 'https://cdn.bulbagarden.net/upload/8/8e/542Leavanny.png', 'https://cdn.bulbagarden.net/upload/0/0e/543Venipede.png', 'https://cdn.bulbagarden.net/upload/b/bc/544Whirlipede.png', 'https://cdn.bulbagarden.net/upload/c/cb/545Scolipede.png', 'https://cdn.bulbagarden.net/upload/4/44/546Cottonee.png', 'https://cdn.bulbagarden.net/upload/a/a2/547Whimsicott.png', 'https://cdn.bulbagarden.net/upload/0/0b/548Petilil.png', 'https://cdn.bulbagarden.net/upload/2/21/549Lilligant.png', 'https://cdn.bulbagarden.net/upload/2/2f/550Basculin.png', 'https://cdn.bulbagarden.net/upload/2/26/551Sandile.png', 'https://cdn.bulbagarden.net/upload/d/d4/552Krokorok.png', 'https://cdn.bulbagarden.net/upload/e/e5/553Krookodile.png', 'https://cdn.bulbagarden.net/upload/4/4c/554Darumaka.png', 'https://cdn.bulbagarden.net/upload/4/40/555Darmanitan.png', 'https://cdn.bulbagarden.net/upload/3/35/556Maractus.png', 'https://cdn.bulbagarden.net/upload/6/6b/557Dwebble.png', 'https://cdn.bulbagarden.net/upload/1/19/558Crustle.png', 'https://cdn.bulbagarden.net/upload/d/dc/559Scraggy.png', 'https://cdn.bulbagarden.net/upload/e/e8/560Scrafty.png', 'https://cdn.bulbagarden.net/upload/6/67/561Sigilyph.png', 'https://cdn.bulbagarden.net/upload/a/a4/562Yamask.png', 'https://cdn.bulbagarden.net/upload/f/f8/563Cofagrigus.png', 'https://cdn.bulbagarden.net/upload/1/1a/564Tirtouga.png', 'https://cdn.bulbagarden.net/upload/d/d0/565Carracosta.png', 'https://cdn.bulbagarden.net/upload/a/a3/566Archen.png', 'https://cdn.bulbagarden.net/upload/1/14/567Archeops.png', 'https://cdn.bulbagarden.net/upload/e/e2/568Trubbish.png', 'https://cdn.bulbagarden.net/upload/c/c4/569Garbodor.png', 'https://cdn.bulbagarden.net/upload/2/2b/570Zorua.png', 'https://cdn.bulbagarden.net/upload/a/a6/571Zoroark.png', 'https://cdn.bulbagarden.net/upload/e/ec/572Minccino.png', 'https://cdn.bulbagarden.net/upload/9/94/573Cinccino.png', 'https://cdn.bulbagarden.net/upload/7/71/574Gothita.png', 'https://cdn.bulbagarden.net/upload/6/67/575Gothorita.png', 'https://cdn.bulbagarden.net/upload/3/38/576Gothitelle.png', 'https://cdn.bulbagarden.net/upload/1/1e/577Solosis.png', 'https://cdn.bulbagarden.net/upload/8/83/578Duosion.png', 'https://cdn.bulbagarden.net/upload/1/19/579Reuniclus.png', 'https://cdn.bulbagarden.net/upload/4/4b/580Ducklett.png', 'https://cdn.bulbagarden.net/upload/7/76/581Swanna.png', 'https://cdn.bulbagarden.net/upload/3/3f/582Vanillite.png', 'https://cdn.bulbagarden.net/upload/2/2f/583Vanillish.png', 'https://cdn.bulbagarden.net/upload/3/39/584Vanilluxe.png', 'https://cdn.bulbagarden.net/upload/6/68/585Deerling-Spring.png', 'https://cdn.bulbagarden.net/upload/8/8d/586Sawsbuck-Spring.png', 'https://cdn.bulbagarden.net/upload/b/b4/587Emolga.png', 'https://cdn.bulbagarden.net/upload/6/60/588Karrablast.png', 'https://cdn.bulbagarden.net/upload/6/63/589Escavalier.png', 'https://cdn.bulbagarden.net/upload/c/cc/590Foongus.png', 'https://cdn.bulbagarden.net/upload/1/13/591Amoonguss.png', 'https://cdn.bulbagarden.net/upload/8/88/592Frillish.png', 'https://cdn.bulbagarden.net/upload/5/5c/593Jellicent.png', 'https://cdn.bulbagarden.net/upload/1/10/594Alomomola.png', 'https://cdn.bulbagarden.net/upload/f/f8/595Joltik.png', 'https://cdn.bulbagarden.net/upload/7/7a/596Galvantula.png', 'https://cdn.bulbagarden.net/upload/2/28/597Ferroseed.png', 'https://cdn.bulbagarden.net/upload/6/6c/598Ferrothorn.png', 'https://cdn.bulbagarden.net/upload/e/ea/599Klink.png', 'https://cdn.bulbagarden.net/upload/8/80/600Klang.png', 'https://cdn.bulbagarden.net/upload/c/cf/601Klinklang.png', 'https://cdn.bulbagarden.net/upload/5/5e/602Tynamo.png', 'https://cdn.bulbagarden.net/upload/c/c7/603Eelektrik.png', 'https://cdn.bulbagarden.net/upload/6/6c/604Eelektross.png', 'https://cdn.bulbagarden.net/upload/f/fd/605Elgyem.png', 'https://cdn.bulbagarden.net/upload/2/2c/606Beheeyem.png', 'https://cdn.bulbagarden.net/upload/8/8e/607Litwick.png', 'https://cdn.bulbagarden.net/upload/a/a5/608Lampent.png', 'https://cdn.bulbagarden.net/upload/6/65/609Chandelure.png', 'https://cdn.bulbagarden.net/upload/5/5c/610Axew.png', 'https://cdn.bulbagarden.net/upload/0/05/611Fraxure.png', 'https://cdn.bulbagarden.net/upload/8/8f/612Haxorus.png', 'https://cdn.bulbagarden.net/upload/7/72/613Cubchoo.png', 'https://cdn.bulbagarden.net/upload/4/40/614Beartic.png', 'https://cdn.bulbagarden.net/upload/1/11/615Cryogonal.png', 'https://cdn.bulbagarden.net/upload/f/f6/616Shelmet.png', 'https://cdn.bulbagarden.net/upload/3/34/617Accelgor.png', 'https://cdn.bulbagarden.net/upload/d/d2/618Stunfisk.png', 'https://cdn.bulbagarden.net/upload/4/41/619Mienfoo.png', 'https://cdn.bulbagarden.net/upload/2/20/620Mienshao.png', 'https://cdn.bulbagarden.net/upload/a/ad/621Druddigon.png', 'https://cdn.bulbagarden.net/upload/a/ac/622Golett.png', 'https://cdn.bulbagarden.net/upload/6/68/623Golurk.png', 'https://cdn.bulbagarden.net/upload/9/9c/624Pawniard.png', 'https://cdn.bulbagarden.net/upload/7/74/625Bisharp.png', 'https://cdn.bulbagarden.net/upload/a/a4/626Bouffalant.png', 'https://cdn.bulbagarden.net/upload/b/bb/627Rufflet.png', 'https://cdn.bulbagarden.net/upload/c/cf/628Braviary.png', 'https://cdn.bulbagarden.net/upload/f/f2/629Vullaby.png', 'https://cdn.bulbagarden.net/upload/0/00/630Mandibuzz.png', 'https://cdn.bulbagarden.net/upload/b/b0/631Heatmor.png', 'https://cdn.bulbagarden.net/upload/1/1a/632Durant.png', 'https://cdn.bulbagarden.net/upload/f/f7/633Deino.png', 'https://cdn.bulbagarden.net/upload/a/a6/634Zweilous.png', 'https://cdn.bulbagarden.net/upload/3/3e/635Hydreigon.png', 'https://cdn.bulbagarden.net/upload/f/f4/636Larvesta.png', 'https://cdn.bulbagarden.net/upload/6/6b/637Volcarona.png', 'https://cdn.bulbagarden.net/upload/6/65/638Cobalion.png', 'https://cdn.bulbagarden.net/upload/a/ad/639Terrakion.png', 'https://cdn.bulbagarden.net/upload/7/79/640Virizion.png', 'https://cdn.bulbagarden.net/upload/0/08/641Tornadus.png', 'https://cdn.bulbagarden.net/upload/b/b8/642Thundurus.png', 'https://cdn.bulbagarden.net/upload/8/8d/643Reshiram.png', 'https://cdn.bulbagarden.net/upload/8/81/644Zekrom.png', 'https://cdn.bulbagarden.net/upload/b/bb/645Landorus.png', 'https://cdn.bulbagarden.net/upload/c/c3/646Kyurem.png', 'https://cdn.bulbagarden.net/upload/5/50/647Keldeo.png', 'https://cdn.bulbagarden.net/upload/a/a3/648Meloetta.png', 'https://cdn.bulbagarden.net/upload/4/46/649Genesect.png', 'https://cdn.bulbagarden.net/upload/c/ca/650Chespin.png', 'https://cdn.bulbagarden.net/upload/7/71/651Quilladin.png', 'https://cdn.bulbagarden.net/upload/1/18/652Chesnaught.png', 'https://cdn.bulbagarden.net/upload/3/3d/653Fennekin.png', 'https://cdn.bulbagarden.net/upload/0/09/654Braixen.png', 'https://cdn.bulbagarden.net/upload/2/21/655Delphox.png', 'https://cdn.bulbagarden.net/upload/1/18/656Froakie.png', 'https://cdn.bulbagarden.net/upload/f/fc/657Frogadier.png', 'https://cdn.bulbagarden.net/upload/6/67/658Greninja.png', 'https://cdn.bulbagarden.net/upload/7/70/659Bunnelby.png', 'https://cdn.bulbagarden.net/upload/3/34/660Diggersby.png', 'https://cdn.bulbagarden.net/upload/7/7e/661Fletchling.png', 'https://cdn.bulbagarden.net/upload/c/ce/662Fletchinder.png', 'https://cdn.bulbagarden.net/upload/a/ae/663Talonflame.png', 'https://cdn.bulbagarden.net/upload/d/d3/664Scatterbug.png', 'https://cdn.bulbagarden.net/upload/b/b7/665Spewpa.png', 'https://cdn.bulbagarden.net/upload/4/4c/666Vivillon.png', 'https://cdn.bulbagarden.net/upload/1/1f/667Litleo.png', 'https://cdn.bulbagarden.net/upload/7/70/668Pyroar.png', 'https://cdn.bulbagarden.net/upload/5/52/669Flab%C3%A9b%C3%A9.png', 'https://cdn.bulbagarden.net/upload/1/17/670Floette.png', 'https://cdn.bulbagarden.net/upload/3/37/671Florges.png', 'https://cdn.bulbagarden.net/upload/5/5d/672Skiddo.png', 'https://cdn.bulbagarden.net/upload/b/bc/673Gogoat.png', 'https://cdn.bulbagarden.net/upload/1/1c/674Pancham.png', 'https://cdn.bulbagarden.net/upload/0/08/675Pangoro.png', 'https://cdn.bulbagarden.net/upload/4/49/676Furfrou.png', 'https://cdn.bulbagarden.net/upload/0/09/677Espurr.png', 'https://cdn.bulbagarden.net/upload/a/a6/678Meowstic.png', 'https://cdn.bulbagarden.net/upload/3/35/679Honedge.png', 'https://cdn.bulbagarden.net/upload/e/ef/680Doublade.png', 'https://cdn.bulbagarden.net/upload/a/ad/681Aegislash.png', 'https://cdn.bulbagarden.net/upload/6/66/682Spritzee.png', 'https://cdn.bulbagarden.net/upload/d/d9/683Aromatisse.png', 'https://cdn.bulbagarden.net/upload/b/bf/684Swirlix.png', 'https://cdn.bulbagarden.net/upload/8/8d/685Slurpuff.png', 'https://cdn.bulbagarden.net/upload/7/70/686Inkay.png', 'https://cdn.bulbagarden.net/upload/e/e4/687Malamar.png', 'https://cdn.bulbagarden.net/upload/5/5b/688Binacle.png', 'https://cdn.bulbagarden.net/upload/4/48/689Barbaracle.png', 'https://cdn.bulbagarden.net/upload/4/4e/690Skrelp.png', 'https://cdn.bulbagarden.net/upload/a/a9/691Dragalge.png', 'https://cdn.bulbagarden.net/upload/f/fb/692Clauncher.png', 'https://cdn.bulbagarden.net/upload/d/d3/693Clawitzer.png', 'https://cdn.bulbagarden.net/upload/5/51/694Helioptile.png', 'https://cdn.bulbagarden.net/upload/f/f6/695Heliolisk.png', 'https://cdn.bulbagarden.net/upload/c/c3/696Tyrunt.png', 'https://cdn.bulbagarden.net/upload/8/8b/697Tyrantrum.png', 'https://cdn.bulbagarden.net/upload/2/2a/698Amaura.png', 'https://cdn.bulbagarden.net/upload/9/9e/699Aurorus.png', 'https://cdn.bulbagarden.net/upload/e/e8/700Sylveon.png', 'https://cdn.bulbagarden.net/upload/4/44/701Hawlucha.png', 'https://cdn.bulbagarden.net/upload/c/c9/702Dedenne.png', 'https://cdn.bulbagarden.net/upload/f/fa/703Carbink.png', 'https://cdn.bulbagarden.net/upload/2/28/704Goomy.png', 'https://cdn.bulbagarden.net/upload/9/95/705Sliggoo.png', 'https://cdn.bulbagarden.net/upload/d/df/706Goodra.png', 'https://cdn.bulbagarden.net/upload/0/04/707Klefki.png', 'https://cdn.bulbagarden.net/upload/7/72/708Phantump.png', 'https://cdn.bulbagarden.net/upload/4/4b/709Trevenant.png', 'https://cdn.bulbagarden.net/upload/d/df/710Pumpkaboo.png', 'https://cdn.bulbagarden.net/upload/8/88/711Gourgeist.png', 'https://cdn.bulbagarden.net/upload/c/c3/712Bergmite.png', 'https://cdn.bulbagarden.net/upload/0/04/713Avalugg.png', 'https://cdn.bulbagarden.net/upload/0/07/714Noibat.png', 'https://cdn.bulbagarden.net/upload/1/15/715Noivern.png', 'https://cdn.bulbagarden.net/upload/1/13/716Xerneas.png', 'https://cdn.bulbagarden.net/upload/5/54/717Yveltal.png', 'https://cdn.bulbagarden.net/upload/3/3a/718Zygarde.png', 'https://cdn.bulbagarden.net/upload/b/b3/719Diancie.png', 'https://cdn.bulbagarden.net/upload/f/fb/720Hoopa.png', 'https://cdn.bulbagarden.net/upload/4/44/721Volcanion.png', 'https://cdn.bulbagarden.net/upload/7/74/722Rowlet.png', 'https://cdn.bulbagarden.net/upload/1/1e/723Dartrix.png', 'https://cdn.bulbagarden.net/upload/a/a4/724Decidueye.png', 'https://cdn.bulbagarden.net/upload/0/0e/725Litten.png', 'https://cdn.bulbagarden.net/upload/d/dc/726Torracat.png', 'https://cdn.bulbagarden.net/upload/2/27/727Incineroar.png', 'https://cdn.bulbagarden.net/upload/d/d8/728Popplio.png', 'https://cdn.bulbagarden.net/upload/c/cd/729Brionne.png', 'https://cdn.bulbagarden.net/upload/8/89/730Primarina.png', 'https://cdn.bulbagarden.net/upload/1/15/731Pikipek.png', 'https://cdn.bulbagarden.net/upload/5/5c/732Trumbeak.png', 'https://cdn.bulbagarden.net/upload/7/78/733Toucannon.png', 'https://cdn.bulbagarden.net/upload/0/08/734Yungoos.png', 'https://cdn.bulbagarden.net/upload/b/ba/735Gumshoos.png', 'https://cdn.bulbagarden.net/upload/1/14/736Grubbin.png', 'https://cdn.bulbagarden.net/upload/e/ec/737Charjabug.png', 'https://cdn.bulbagarden.net/upload/4/4e/738Vikavolt.png', 'https://cdn.bulbagarden.net/upload/9/98/739Crabrawler.png', 'https://cdn.bulbagarden.net/upload/1/17/740Crabominable.png', 'https://cdn.bulbagarden.net/upload/e/ed/741Oricorio-Baile.png', 'https://cdn.bulbagarden.net/upload/f/fa/742Cutiefly.png', 'https://cdn.bulbagarden.net/upload/e/e4/743Ribombee.png', 'https://cdn.bulbagarden.net/upload/5/51/744Rockruff.png', 'https://cdn.bulbagarden.net/upload/1/14/745Lycanroc.png', 'https://cdn.bulbagarden.net/upload/1/18/746Wishiwashi-Solo.png', 'https://cdn.bulbagarden.net/upload/d/d3/747Mareanie.png', 'https://cdn.bulbagarden.net/upload/0/06/748Toxapex.png', 'https://cdn.bulbagarden.net/upload/1/12/749Mudbray.png', 'https://cdn.bulbagarden.net/upload/f/f7/750Mudsdale.png', 'https://cdn.bulbagarden.net/upload/2/29/751Dewpider.png', 'https://cdn.bulbagarden.net/upload/8/82/752Araquanid.png', 'https://cdn.bulbagarden.net/upload/1/10/753Fomantis.png', 'https://cdn.bulbagarden.net/upload/1/19/754Lurantis.png', 'https://cdn.bulbagarden.net/upload/c/c9/755Morelull.png', 'https://cdn.bulbagarden.net/upload/3/36/756Shiinotic.png', 'https://cdn.bulbagarden.net/upload/2/27/757Salandit.png', 'https://cdn.bulbagarden.net/upload/7/72/758Salazzle.png', 'https://cdn.bulbagarden.net/upload/e/e5/759Stufful.png', 'https://cdn.bulbagarden.net/upload/a/a4/760Bewear.png', 'https://cdn.bulbagarden.net/upload/a/a1/761Bounsweet.png', 'https://cdn.bulbagarden.net/upload/7/78/762Steenee.png', 'https://cdn.bulbagarden.net/upload/2/23/763Tsareena.png', 'https://cdn.bulbagarden.net/upload/c/c9/764Comfey.png', 'https://cdn.bulbagarden.net/upload/d/d8/765Oranguru.png', 'https://cdn.bulbagarden.net/upload/b/ba/766Passimian.png', 'https://cdn.bulbagarden.net/upload/e/ef/767Wimpod.png', 'https://cdn.bulbagarden.net/upload/b/b6/768Golisopod.png', 'https://cdn.bulbagarden.net/upload/f/f0/769Sandygast.png', 'https://cdn.bulbagarden.net/upload/3/32/770Palossand.png', 'https://cdn.bulbagarden.net/upload/4/4f/771Pyukumuku.png', 'https://cdn.bulbagarden.net/upload/f/fd/772Type_Null.png', 'https://cdn.bulbagarden.net/upload/b/be/773Silvally.png', 'https://cdn.bulbagarden.net/upload/9/90/774Minior.png', 'https://cdn.bulbagarden.net/upload/7/7d/775Komala.png', 'https://cdn.bulbagarden.net/upload/1/15/776Turtonator.png', 'https://cdn.bulbagarden.net/upload/5/5a/777Togedemaru.png', 'https://cdn.bulbagarden.net/upload/9/9b/778Mimikyu.png', 'https://cdn.bulbagarden.net/upload/9/92/779Bruxish.png', 'https://cdn.bulbagarden.net/upload/d/dc/780Drampa.png', 'https://cdn.bulbagarden.net/upload/2/2f/781Dhelmise.png', 'https://cdn.bulbagarden.net/upload/a/a0/782Jangmo-o.png', 'https://cdn.bulbagarden.net/upload/0/0d/783Hakamo-o.png', 'https://cdn.bulbagarden.net/upload/8/84/784Kommo-o.png', 'https://cdn.bulbagarden.net/upload/d/d0/785Tapu_Koko.png', 'https://cdn.bulbagarden.net/upload/4/4d/786Tapu_Lele.png', 'https://cdn.bulbagarden.net/upload/6/67/787Tapu_Bulu.png', 'https://cdn.bulbagarden.net/upload/6/66/788Tapu_Fini.png', 'https://cdn.bulbagarden.net/upload/1/17/789Cosmog.png', 'https://cdn.bulbagarden.net/upload/1/1b/790Cosmoem.png', 'https://cdn.bulbagarden.net/upload/5/57/791Solgaleo.png', 'https://cdn.bulbagarden.net/upload/9/9d/792Lunala.png', 'https://cdn.bulbagarden.net/upload/2/2c/793Nihilego.png', 'https://cdn.bulbagarden.net/upload/f/fa/794Buzzwole.png', 'https://cdn.bulbagarden.net/upload/c/c7/795Pheromosa.png', 'https://cdn.bulbagarden.net/upload/d/d2/796Xurkitree.png', 'https://cdn.bulbagarden.net/upload/8/89/797Celesteela.png', 'https://cdn.bulbagarden.net/upload/f/fe/798Kartana.png', 'https://cdn.bulbagarden.net/upload/4/47/799Guzzlord.png', 'https://cdn.bulbagarden.net/upload/4/44/800Necrozma.png', 'https://cdn.bulbagarden.net/upload/0/0a/801Magearna.png', 'https://cdn.bulbagarden.net/upload/8/89/802Marshadow.png', 'https://cdn.bulbagarden.net/upload/e/e5/803Poipole.png', 'https://cdn.bulbagarden.net/upload/d/de/804Naganadel.png', 'https://cdn.bulbagarden.net/upload/2/27/805Stakataka.png', 'https://cdn.bulbagarden.net/upload/a/a5/806Blacephalon.png', 'https://cdn.bulbagarden.net/upload/a/a7/807Zeraora.png']
    pepe = modnar.choice(z)
    name = ctx.message.author.name
    disc = ctx.message.author.discriminator
    r = requests.get(pepe, stream=True)
    img = Image.open(r.raw)
    datas = img.getdata()

    newData = []
    for item in datas:
        if(item[3] != 0):
            newData.append((0, 0, 0, 255))
        else:
            newData.append(item)

    img.putdata(newData)
    # Put 550, 550
    bg = Image.open("WhosThatPokemon.png")
    bg_w, bg_h = 1100, 1100
    baseheight = 500
    hpercent = (baseheight / float(img.size[1]))
    wsize = int((float(img.size[0]) * float(hpercent)))
    img = img.resize((wsize, baseheight), Image.ANTIALIAS)
    img_w, img_h = img.size
    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)

    datas = img.getdata()

    newData = []
    for item in datas:
        if item[3] == 0:
            newData.append((255, 255, 255, 255))
        else:
            newData.append(item)

    img.putdata(newData)

    bg.paste(img, offset)
    x = name + str(disc) + datetime.datetime.now().strftime("%Y%M%D%H").replace('/', '') + '.png'
    bg.save(x)
    return [x, pepe.split('.png')[0].split('/')[-1][3:]]

@client.command(pass_context=True, aliases=["whosthatpokemon"])
async def wtp(ctx, *args):
    if(args == ()):
        x = savepokemon(ctx)
        file = discord.File(open(x[0], "rb"))
        await ctx.message.channel.send(file=file)
        os.remove(x[0])
        conn = sqlite3.connect('WTP.db')
        c = conn.cursor()
        c.execute("UPDATE WTP SET Pokemon=? WHERE Channel=?", (x[1].replace('_', ' ').replace('-Overcast', '').replace('-Altered', '').replace('-Land', '').replace('-Spring', '').replace('-Baile', '').replace('-Solo', ''), str(ctx.message.channel.id)))
        conn.commit()
    else:
        p = ' '.join(args).replace('-Overcast', '').replace('-Altered', '').replace('-Land', '').replace('-Spring', '').replace('-Baile', '').replace('-Solo', '')
        conn = sqlite3.connect('WTP.db')
        c = conn.cursor()
        c.execute('SELECT * FROM WTP')
        data = c.fetchall()
        cpok = ""
        for i in data:
            if(i[0] == str(ctx.message.channel.id)):
                cpok = i[1]
        if(cpok == ""):
            await ctx.message.channel.send("There isn't a game yet! Type mb!wtp to get one started!")
        else:
            if(cpok.lower() == p.lower()):
                await ctx.message.channel.send("You got it!")
                c.execute("UPDATE WTP SET Pokemon=? WHERE Channel=?", ("", str(ctx.message.channel.id)))
                conn.commit()
            else:
                await ctx.message.channel.send("That's not quite right, try again!")

@client.command(pass_context=True, aliases=["shibe", "shiba", "shibainu", "inu"])
async def shib(ctx):
    x = requests.get('http://shibe.online/api/shibes?count=1&urls=true&httpsUrls=true').text
    url = x.split('"')[1]
    emb = (discord.Embed(colour=0xf7b8cf))
    emb.set_image(url=url)
    emb.set_footer(text="Shibe API: http://shibe.online/")
    await ctx.message.channel.send(embed=emb)

@client.command(pass_context=True)
async def purge(ctx, num: int):
    if(ctx.message.guild.get_member(ctx.message.author.id) == ctx.message.guild.owner):
        await ctx.message.channel.purge(limit=num+1)

@client.command(pass_context=True)
async def ban(ctx, user: discord.User):
    if (ctx.message.guild.get_member(ctx.message.author.id) == ctx.message.guild.owner):
        n = user.name
        d = user.discriminator
        await ctx.message.guild.ban(user)
        await ctx.message.channel.send("Banned " + str(n) + "#" + str(d) + "!")

@client.command(pass_context=True)
async def kick(ctx, user: discord.User):
    if (ctx.message.guild.get_member(ctx.message.author.id) == ctx.message.guild.owner):
        n = user.name
        d = user.discriminator
        await client.kick(user)
        await ctx.message.channel.send("Kicked " + str(n) + "#" + str(d) + "!")

@client.command(pass_context=True, aliases=["song"])
async def music(ctx, bpm, x):
    os.chdir("C:\\MewBot")
    x = subprocess.check_output(
        'C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python36\\python.exe nbmusic.py ' + bpm + ' "' + x + '" "' + ctx.message.author.discriminator + ctx.message.author.name + '"',
        shell=True)
    m = int(x.decode().replace('\r\n', ''))
    if(m == 1):
        await ctx.message.channel.send(file=discord.File(open(ctx.message.author.discriminator + ctx.message.author.name + "0.wav", "rb")))
    else:
        x = []
        for i in range(m):
            x.append(AudioSegment.from_wav(ctx.message.author.discriminator + ctx.message.author.name + str(i) + ".wav"))
        while(len(x) != 1):
            x[0] = x[0].overlay(x[-1])
            x.pop(-1)
        x[0].export("fin.wav", format="wav")
        await ctx.message.channel.send(file=discord.File(open("fin.wav", "rb")))
        for i in range(m):
            os.remove(ctx.message.author.discriminator + ctx.message.author.name + str(i) + ".wav")

@client.command(pass_context=True, aliases=["trans", "googletrans", "googletranslate"])
async def translate(ctx, lf, lt, *args):
    x = Translator()
    out = x.translate(' '.join(args), src=lf, dest=lt)
    emb = (discord.Embed(colour=0xf7b8cf))
    emb.set_author(name="Google Translate")
    emb.add_field(name=lf + " -> " + lt, value=out.text)
    await ctx.message.channel.send(embed=emb)

@client.command(pass_context=True)
async def e(ctx):
    await ctx.message.channel.send("venom is not gay american")

def isNum(x):
    try:
        x = float(x)
        return True
    except:
        return False

@client.command(pass_context=True, aliases=["twitchchannel"])
async def twitch(ctx, *args):
    x = list(args)[0]
    cl = TwitchClient(client_id=open("TWITCH.txt").read())
    if(not isNum(x)):
        y = requests.get("https://wind-bow.glitch.me/twitch-api/users/" + x)
        x = y.text.split('_id":')[1].split(',')[0]
    s = cl.streams.get_stream_by_user(x)
    c = cl.users.get_by_id(int(x))
    emb = (discord.Embed(colour=0xf7b8cf))
    emb.set_author(name=c.display_name, url="https://twitch.tv/" + c.name)
    emb.set_thumbnail(url=c.logo)
    emb.add_field(name="Bio", value=c.bio)
    emb.set_footer(text="Channel created at " + (c.created_at + datetime.timedelta(hours=-4)).strftime("%m-%d-%Y %H:%M:%S") + " EST")
    if(s == None):
        await ctx.message.channel.send(embed=emb)
    else:
        await ctx.message.channel.send(c.display_name + " is streaming!")
        emb.add_field(name="Followers", value=str(s.channel.followers))
        emb.add_field(name="Stream Name", value=s.channel.status)
        if(s.game == ''):
            game = "None"
        else:
            game = s.game
        emb.add_field(name="Game", value=game)
        emb.add_field(name="Viewers", value=str(s.viewers))
        st = (s.created_at + datetime.timedelta(hours=-4))
        y = str(datetime.datetime.now() - st).split('.')[0].split(":")
        y[0] += " hours"
        y[1] += " minutes"
        y[2] = "and " + y[2] + " seconds."
        if (y[-3] == "0 hours"):
            y.pop(-3)
        if (y[-2] == "00 minutes"):
            y.pop(-2)
        if (y[-1] == "and 00 seconds."):
            y.pop(-1)
        if (len(y) == 1):
            x = y[0].split("and ")[1]
            y[0] = x
        emb.add_field(name="Uptime", value=', '.join(y))
        emb.set_image(url="https://static-cdn.jtvnw.net/previews-ttv/live_user_" + c.name + "-320x180.jpg?r=223636")
        await ctx.message.channel.send(embed=emb)

@client.command(pass_context=True, aliases=["up"])
async def uptime(ctx):
    global dtupt
    y = str(datetime.datetime.now() - dtupt).split('.')[0].split(":")
    y[0] += " hours"
    y[1] += " minutes"
    y[2] = "and " + y[2] + " seconds."
    if(y[-3] == "0 hours"):
        y.pop(-3)
    if (y[-2] == "00 minutes"):
        y.pop(-2)
    if (y[-1] == "and 00 seconds."):
        y.pop(-1)
    if(len(y) == 1):
        x = y[0].split("and ")[1]
        y[0] = x
    await ctx.message.channel.send("MewBot has been online for " + ', '.join(y))

@client.command(pass_context=True)
async def demonlist(ctx):
    message = ctx.message
    current = 1
    botmsg = await message.channel.send(embed=getdemoninfo(current))
    await botmsg.add_reaction("⏪")
    await botmsg.add_reaction("◀")
    await botmsg.add_reaction("▶")
    await botmsg.add_reaction("⏩")
    await botmsg.add_reaction("⏹")
    await botmsg.add_reaction("\U0001F522")

    def isNum(x):
        try:
            l = int(x)
            return True
        except ValueError:
            return False

    def check(m):
        return isNum(m.content) and m.author == message.author and m.channel == message.channel

    while(True):
        def change(reaction, user):
            return user == message.author
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=change)
        except futures.TimeoutError:
            await message.channel.delete_messages([botmsg])
            break
        else:
            if(str(reaction.emoji) == "▶"):
                if(current < 100):
                    current += 1
                    await botmsg.edit(embed=getdemoninfo(current))
                    await botmsg.remove_reaction(reaction, message.guild.get_member(user.id))
                else:
                    current -= 1
                    await botmsg.remove_reaction(reaction, message.guild.get_member(user.id))
            elif(str(reaction.emoji) == "◀"):
                if(current > 0):
                    current -= 1
                    await botmsg.edit(embed=getdemoninfo(current))
                    await botmsg.remove_reaction(reaction, message.guild.get_member(user.id))
                else:
                    current += 1
                    await botmsg.remove_reaction(reaction, message.guild.get_member(user.id))
            elif(str(reaction.emoji) == "⏪"):
                current = 1
                await botmsg.edit(embed=getdemoninfo(current))
                await botmsg.remove_reaction(reaction, message.guild.get_member(user.id))
            elif(str(reaction.emoji) == "⏩"):
                current = 100
                await botmsg.edit(embed=getdemoninfo(current))
                await botmsg.remove_reaction(reaction, message.guild.get_member(user.id))
            elif(str(reaction.emoji) == "⏹"):
                await botmsg.delete()
                break
            elif(str(reaction.emoji) == "\U0001F522"):
                msg = await client.wait_for('message', check=check)
                current = int(msg.content)
                if(current > 100):
                    current = 100
                elif(current < 1):
                    current = 1
                await botmsg.edit(embed=getdemoninfo(current))
                await botmsg.remove_reaction(reaction, message.guild.get_member(user.id))
                await msg.delete()

def getdemoninfo(i):
    fin = []
    r = requests.get('https://pointercrate.com/api/v1/demons/' + str(i))
    x = ast.literal_eval(r.text.replace('false', 'False').replace('null', 'None').replace('true', 'True'))['data']
    creators = [i['name'] for i in x['creators']]
    verifier = x['verifier']['name']
    video = x['video']
    name = x['name']
    r = requests.get('https://pointercrate.com/demonlist/' + str(i))
    desc = html.unescape(r.text.split('<q>')[1].split('</q>')[0])
    finalemb = discord.Embed(colour=0xf7b8cf)
    if(video == None):
        finalemb.set_author(name=name + " - #" + str(i))
    else:
        finalemb.set_author(name=name + " - #" + str(i), url=video)
    finalemb.add_field(name="Description", value=desc)
    finalemb.add_field(name="Creators", value='`' + ', '.join(creators) + '`')
    finalemb.add_field(name="Verifier", value=verifier)
    return finalemb

def blurpled(im):
    im = im.convert("LA")
    x = im.load()
    [a, b] = im.size
    for i in range(a):
        for j in range(b):
            a1 = abs(x[i, j][0] - 0)
            a2 = abs(x[i, j][0] - 127)
            a3 = abs(x[i, j][0] - 255)
            if(a1 < a2 and a1 < a3):
                x[i, j] = (0, 255)
            elif(a2 < a1 and a2 < a3):
                x[i, j] = (127, 255)
            else:
                x[i, j] = (255, 255)
    im = im.convert("RGBA")
    data = np.array(im)
    red, green, blue, alpha = data.T
    black = (red == 0) & (blue == 0) & (green == 0) & (alpha == 255)
    data[..., :-1][black.T] = (78, 93, 148)
    grey = (red == 127) & (blue == 127) & (green == 127) & (alpha == 255)
    data[..., :-1][grey.T] = (114, 137, 218)
    im = Image.fromarray(data)
    return im

@client.command(pass_context=True)
async def blurple(ctx, *args):
    if(args == ()):
        m = ctx.message
        if(m.attachments != []):
            x = m.attachments[0].url
        else:
            x = ctx.message.author.avatar_url
    elif(args[0][:2] == "<@" and args[0][-1] == ">"):
        if(args[0][:3] == "<@!"):
            y = args[0].split("<@!")[1].split(">")[0]
        else:
            y = args[0].split("<@")[1].split(">")[0]
        x = await client.get_user_info(y)
        x = x.avatar_url
    elif(args[0][:1] != "h"):
        try:
            x = await client.get_user_info(args[0])
            x = x.avatar_url
        except:
            await ctx.message.channel.send("That is not a url!")
    else:
        x = (' '.join(args)).split(" ")[0]
    r = requests.get(x, stream=True)
    if(x.split(".")[-1].split("?")[0].lower() == "webp"):
        if (r.status_code == 200):
            with open("temp.webp", 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
        im = Image.open("temp.webp").convert("RGB")
        im.save("temp.png")
    else:
        if (r.status_code == 200):
            with open("temp.png", 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
    im = Image.open("temp.png")
    x = blurpled(im)
    x.save("temp.png")
    await ctx.message.channel.send("Here is your Blurplefied image!")
    await ctx.message.channel.send(file=discord.File(open("temp.png", "rb")))

@client.command(pass_context=True, aliases=["shinypokemon", "shiny", "spkmn", "shinypkmn", "spkmon"])
async def spokemon(ctx, *args):
    pokemon = ' '.join(args)
    if (isNum(pokemon)):
        pokemon = str(pokeapi.PokemonfromID(int(pokemon)))
    x = "https://pokemon.night.coffee/icons/shiny/" + pokemon.lower() + ".gif"
    x = requests.get(x)
    with open(str(ctx.message.author.id) + "_" + pokemon.lower() + ".gif", "wb") as f:
        for chunk in x.iter_content(1024):
            f.write(chunk)
    await ctx.message.channel.send(file=discord.File(open(str(ctx.message.author.id) + "_" + pokemon + ".gif", "rb")))
    os.remove(str(ctx.message.author.id) + "_" + pokemon.lower() + ".gif")

@client.command(pass_context=True, aliases=["pkmn", "pkmon"])
async def pokemon(ctx, *args):
    pokemon = ' '.join(args)
    if (isNum(pokemon)):
        pokemon = str(pokeapi.PokemonfromID(int(pokemon)))
    x = "https://pokemon.night.coffee/icons/normal/" + pokemon.lower() + ".gif"
    x = requests.get(x)
    with open(str(ctx.message.author.id) + "_" + pokemon.lower() + ".gif", "wb") as f:
        for chunk in x.iter_content(1024):
            f.write(chunk)
    await ctx.message.channel.send(file=discord.File(open(str(ctx.message.author.id) + "_" + pokemon + ".gif", "rb")))
    os.remove(str(ctx.message.author.id) + "_" + pokemon.lower() + ".gif")

@client.command(pass_context=True)
async def votemute(ctx, user: discord.User):
    with codecs.open("tms.txt", "r", encoding="utf8") as f:
            if(ctx.message.server.id + "\n" in f.readlines()):
                    if(ctx.message.server.id not in los.keys()):
                        await ctx.message.channel.send("Voting to mute " + str(user.mention) + "!\n1 vote!")
                        los[ctx.message.server.id] = [1, []]
                        los[ctx.message.server.id][1].append(ctx.message.author.id)
                    else:
                        if(user != None):
                            if (ctx.message.author.id in los[ctx.message.server.id][1]):
                                await ctx.message.channel.send("You've already voted!")
                            else:
                                los[ctx.message.server.id][1].append(ctx.message.author.id)
                                if(los[ctx.message.server.id][0] == 9):
                                    await ctx.message.channel.send("Muting " + str(user.mention))
                                    m = ctx.message.server.get_member(user.id)
                                    await client.server_voice_state(user, mute=True)
                                    del los[ctx.message.server.id]
                                else:
                                    los[ctx.message.server.id][0] += 1
                                    await ctx.message.channel.send(str(ctx.message.author.mention) + " votes to mute " + str(user.mention) + "! " + str(los[ctx.message.server.id][0]) + " votes!")
                        else:
                            await ctx.message.channel.send("There is already a vote going on!")
            else:
                await ctx.message.channel.send("Your Server is not toggled to allow for Vote Muting!")


@client.command(pass_context=True, aliases=["togglevotemute"])
async def tvotemute(ctx):
    if(ctx.message.server.get_member(ctx.message.author.id) == ctx.message.server.owner):
        x = False
        with codecs.open("tms.txt", "r", encoding="utf8") as f:
            for i in f.readlines():
                if(ctx.message.server.id in i):
                    x = True
            y = f.readlines()
        if(not x):
            with codecs.open("tms.txt", "a", encoding="utf8") as f:
                f.write(ctx.message.server.id + "\n")
        else:
            f = open("tms.txt", "r")
            y = f.readlines()
            f.close()
            for i in range(len(y)):
                if(ctx.message.server.id in y[i]):
                    y.pop(i)
            with codecs.open("tms.txt", "w", encoding="utf8") as f:
                f.write(''.join(y))

@client.command(pass_context=True, aliases=["saydelete"])
async def sayd(ctx, *args):
    x = ' '.join(args)
    await ctx.message.delete()
    await ctx.message.channel.send(x)

@client.command(pass_context=True)
async def otter(ctx):
    o = ["https://goo.gl/q9g11B", "https://goo.gl/GKhkV9", "https://goo.gl/YcWLdH", "https://goo.gl/fxGaKW", "https://goo.gl/rRvqvW", "https://goo.gl/FEFi5P", "https://goo.gl/2EnR7P", "https://goo.gl/ZzF7hf", "https://goo.gl/P152Pw", "https://goo.gl/8A5dd2", "https://goo.gl/c4qTVG", "https://goo.gl/cvdkVx", "https://goo.gl/co1Sqv", "https://goo.gl/5Df5sA", "https://goo.gl/LFcmV4", "https://goo.gl/5j6LkW", "https://goo.gl/786Xme", "https://goo.gl/GLdoVf", "https://goo.gl/Z6PCFS", "https://goo.gl/jFnzZg", "https://goo.gl/ctMSFg", "https://goo.gl/PM7GS6", "https://goo.gl/EiYwHS", "https://goo.gl/MZG9Cf", "https://goo.gl/3dRpV4", "https://goo.gl/tqJXxE", "https://goo.gl/CDbqrS", "https://goo.gl/ZZXVaV", "https://goo.gl/QTsNEk", "https://goo.gl/ka5B6h", "https://goo.gl/sEpfXg", "https://goo.gl/z4dVLZ", "https://goo.gl/6ER4Av", "https://goo.gl/66RwD5", "https://goo.gl/bK5QGZ", "https://goo.gl/rsrsxz", "https://goo.gl/gs8BkV", "https://goo.gl/P6ksoT", "https://goo.gl/DCCR5F"]
    await ctx.message.channel.send(str(ctx.message.author.mention) + ", Here is your otter\n" + modnar.choice(o))

@client.command(pass_context=True, aliases=["inv"])
async def invite(ctx):
    emb = (discord.Embed(colour=0xf7b8cf))
    emb.add_field(name="Invite Link", value="https://bit.ly/2wzmka1")
    emb.set_footer(text="Thanks for inviting MewBot!")
    await ctx.message.channel.send(embed=emb)

@client.command(pass_context=True)
async def setID(ctx, ID):
    f = open("ids.txt", "r")
    count = 0
    for line in f:
        if (ctx.message.author.id in line):
            count = line
    if (count == 0):
        f.close()
        f = open("ids.txt", "a")
        f.write(ctx.message.author.id + " " + ID + " 0\n")
        await ctx.message.channel.send("Account set!")
        f.close()
    else:
        f.close()
        f = open("ids.txt", "r")
        await ctx.message.channel.send("You have already set your ID! If you need it changed, contact me at Venom#8068")
    f.close()


@client.command(pass_context=True, aliases=["listservers"])
async def servers(ctx):
    fin = ""
    if (ctx.message.author.id == 190804082032640000):
        for server in client.guilds:
            a = ""
            a += str(server.name)
            i = len(server.members)
            a += " | " + str(i)
            try:
                x = await server.invites()
                a += " | " + str(x[-1].url)
            except:
                a += ""
            fin += a + "\n"
            x = [fin[idx:idx+2000] for idx,val in enumerate(fin) if idx%2000 == 0]
        fin += "Finished"
    else:
        x = ["You don't have high enough permissions!"]
    for i in x:
        await ctx.message.channel.send(i)

@client.command(pass_context=True)
async def info(ctx):
    x = 0
    for server in client.guilds:
        x += len(server.members)
    emb = (discord.Embed(colour=0xf7b8cf))
    emb.set_author(name="Bot Info")
    emb.add_field(name="Bot Name", value=client.user.name)
    emb.add_field(name="Server Count", value=str(len(client.guilds)))
    emb.add_field(name="Users", value=str(x))
    emb.add_field(name="Developer", value="Venom#8068")
    emb.add_field(name="Library", value="discord.py")
    await ctx.message.channel.send(embed=emb)

@client.command(pass_context=True, aliases=["stats", "about"])
async def botinfo(ctx):
    x = 0
    for server in client.guilds:
        for user in server.members:
            if(not user.bot):
                x += 1
    emb = (discord.Embed(colour=0xf7b8cf))
    emb.set_author(name="Bot Info")
    emb.add_field(name="Bot Name", value=client.user.name)
    emb.add_field(name="Server Count", value=str(len(client.guilds)))
    emb.add_field(name="Users", value=str(x))
    emb.add_field(name="Developer", value="Venom#8068")
    emb.add_field(name="Library", value="discord.py")
    await ctx.message.channel.send(embed=emb)

@client.command(pass_context=True, aliases=["emoji"])
async def bigletter(ctx, *args):
    f = list(' '.join(args))
    fin = ""
    for i in f:
        i = i.lower()
        if(i in list("abcdefghijklmnopqrstuvwxyz")):
            fin += ":regional_indicator_" + i + ":"
        elif(i in list("1234567890")):
            fin += ":" + i.replace('1', 'one').replace('2', 'two').replace('3', 'three').replace('4', 'four').replace('5', 'five').replace('6', 'six').replace('7', 'seven').replace('8', 'eight').replace('9', 'nine').replace('0', 'zero') + ":"
        else:
            fin += i
    emb = (discord.Embed(colour=0xf7b8cf))
    emb.add_field(name="Emoji String", value=fin)
    await ctx.message.channel.send(embed=emb)

@client.command(pass_context=True, aliases=["deepfry"])
async def df(ctx, *args):
    try:
        if (args == ()):
            m = ctx.message
            if (m.attachments != []):
                x = m.attachments[0].url
            else:
                x = ctx.message.author.avatar_url
        elif (args[0][:2] == "<@" and args[0][-1] == ">"):
            if (args[0][:3] == "<@!"):
                y = args[0].split("<@!")[1].split(">")[0]
            else:
                y = args[0].split("<@")[1].split(">")[0]
            x = await client.get_user_info(y)
            x = x.avatar_url
        elif (args[0][:1] != "h"):
            try:
                x = await client.get_user_info(int(args[0]))
                x = x.avatar_url
            except:
                await ctx.message.channel.send("That is not a url!")
        else:
            x = (' '.join(args)).split(" ")[0]
        r = requests.get(x, stream=True)
        if (x.split(".")[-1].split("?")[0].lower() == "webp"):
            if (r.status_code == 200):
                with open("temp.webp", 'wb') as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)
            im = Image.open("temp.webp").convert("RGB")
            im.save("temp.png")
        else:
            if (r.status_code == 200):
                with open("temp.png", 'wb') as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)
        im = Image.open("temp.png")
        factor = (259 * (255 + 255)) / (255 * (259 - 255))
        def contrast(c):
            return 128 + factor * (c-128)
        x = im.point(contrast)
        x.save("df.png")
        await ctx.message.channel.send(file=discord.File(open("df.png", "rb")))
    except:
        await ctx.message.channel.send("Image could not be found!")

@client.command(pass_context=True, aliases=["char"])
async def character(ctx, *args):
    s = list(' '.join(args))
    fin = ""
    for i in s:
        a = format(ord(i), '#04x').split('0x')[-1]
        url = "http://www.fileformat.info/info/unicode/char/" + a.lower()
        f = requests.get(url).text.split('title>')[1].split('</titl')[0].split("'")[1]
        fin = fin + '`\\U000000' + a.lower() + '`: **' + f + '** - ' + i + ' — ' + url + "\n"
    await ctx.message.channel.send(fin)

@client.command(pass_context=True, aliases=["prime"])
async def isprime(ctx, *args):
    s = int(''.join(args))
    emb = (discord.Embed(colour=0xf7b8cf))
    try:
            a = s > 1 and all(s % i for i in itertools.islice(itertools.count(2), int(math.sqrt(s) - 1)))
            emb.add_field(name="Is " + str(s) + " prime?",
                          value=str(s) + " is prime." if a else str(s) + " is not prime.")
    except(ValueError):
        emb.add_field(name="Is " + str(s) + " prime?", value=str(s) + " may be prime.")
    await ctx.message.channel.send(embed=emb)

@client.command(pass_context=True, aliases=["len"])
async def length(ctx, *args):
    s = len(list(' '.join(args)))
    emb = (discord.Embed(colour=0xf7b8cf))
    emb.add_field(name="Length of String", value=str(s))
    await ctx.message.channel.send(embed=emb)

@client.command(pass_context=True, aliases=["lower"])
async def lowercase(ctx, *args):
    s = ' '.join(args).lower()
    emb = (discord.Embed(colour=0xf7b8cf))
    emb.add_field(name="Lowercase String", value=s)
    await ctx.message.channel.send(embed=emb)

@client.command(pass_context=True, aliases=["upper"])
async def uppercase(ctx, *args):
    s = ' '.join(args).upper()
    emb = (discord.Embed(colour=0xf7b8cf))
    emb.add_field(name="Uppercase String", value=s)
    await ctx.message.channel.send(embed=emb)

@client.command(pass_context=True)
async def morsed(ctx, *args):
    s = ' '.join(args)
    mcd = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
               'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
               'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
               'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
               '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----', ',': '--..--', '.': '.-.-.-',
               '?': '..--..', '/': '-..-.', '-': '-....-', '(': '-.--.', ')': '-.--.-', ':': '---...', "'": '.----.',
               '"': ".-..-.", '@': '.--.-.', '=': '-...-'}
    fin = ""
    for i in s.split():
            if (i == "/"):
                fin += " "
            else:
                fin += [key for key, value in mcd.items() if value == i][0]
    emb = (discord.Embed(colour=0xf7b8cf))
    emb.add_field(name="Morse Decoded String", value=fin)
    await ctx.message.channel.send(embed=emb)

@client.command(pass_context=True)
async def morsee(ctx, *args):
    s = ' '.join(args)
    mcd = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
               'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
               'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
               'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
               '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----', ',': '--..--', '.': '.-.-.-',
               '?': '..--..', '/': '-..-.', '-': '-....-', '(': '-.--.', ')': '-.--.-', ':': '---...', "'": '.----.',
               '"': ".-..-.", '@': '.--.-.', '=': '-...-'}
    fin = ""
    for i in s:
            if i != " ":
                if (i == "!"):
                    i = "."
                fin += mcd[i.upper()] + " "
            else:
                fin += " / "
    emb = (discord.Embed(colour=0xf7b8cf))
    emb.add_field(name="Morse Encoded String", value=fin)
    await ctx.message.channel.send(embed=emb)

@client.command(pass_context=True, aliases=["hexadecimald", "hexdecode", "hexadecimaldecode"])
async def hexd(ctx, *args):
    s = ' '.join(args)
    emb = (discord.Embed(colour=0xf7b8cf))
    emb.add_field(name="Hex Decoded String", value=base64.b16decode(s.encode('utf-8')).decode())
    await ctx.message.channel.send(embed=emb)

@client.command(pass_context=True, aliases=["hexadecimale", "hexencode", "hexadecimalencode"])
async def hexe(ctx, *args):
    s = ' '.join(args)
    emb = (discord.Embed(colour=0xf7b8cf))
    emb.add_field(name="Hex Encoded String", value=base64.b16encode(s.encode('utf-8')).decode())
    await ctx.message.channel.send(embed=emb)

@client.command(pass_context=True, aliases=["levelpass"])
async def lpass(ctx, *args):
    id = ' '.join(args)
    url = "http://gdidthingpython.000webhostapp.com/thing2.php?id=" + id
    f = requests.get(url).text
    id = f.split(' 1:')[1].split(':')[0]
    url = "http://gdidthingpython.000webhostapp.com/thing.php?id=" + id
    f = requests.get(url).text
    x = f.split('65: ')[1].split('#')[0]
    if (x == "0" or x == "Aw==" or x == ""):
        await ctx.message.channel.send("There is no pass for the level __**" + f.split(':')[6].split("<")[0][1:] + "**__.")
    else:
        emb = (discord.Embed(colour=0xf7b8cf))
        emb.set_author(name=f.split('3:')[1].split('<')[0][1:])
        emb.add_field(name="Password:", value=robbd(x)[1:])
        await ctx.message.channel.send(embed=emb)

@client.command(pass_context=True)
async def level(ctx, *args):
    id = ' '.join(args)
    url = "http://gdidthingpython.000webhostapp.com/thing2.php?id=" + id
    f = requests.get(url).text
    id = f.split(':')[4]
    url = "http://gdidthingpython.000webhostapp.com/thing2.php?id=" + id
    f = requests.get(url).text
    emb = (discord.Embed(colour=0xf7b8cf))
    emb.set_author(name="Level Info")
    emb.add_field(name="Level Name", value=f.split(':')[6])
    if (f.split(':')[56].split('#')[1] != ""):
        emb.add_field(name="Level Author", value=f.split('#')[1].split(':')[1])
    else:
        emb.add_field(name="Level Author", value="-")
    emb.add_field(name="Level ID", value=f.split(':')[4])
    emb.add_field(name="Downloads", value=f.split(':')[16])
    emb.add_field(name="Likes", value=f.split(':')[22])
    b = "No"
    if (f.split(':')[34] != "0"):
        b = "Yes"
    emb.add_field(name="Epic?", value=b)
    a = "No"
    if (f.split(':')[32] != "0"):
        a = "Yes"
    emb.add_field(name="Featured?", value=a)
    emb.add_field(name="Stars", value=f.split(':')[30])
    c = "No Description Provided"
    if (f.split(':')[38] != ""):
        c = base64.b64decode(f.split(':')[38]).decode()
    emb.add_field(name="Description", value=c)
    emb.add_field(name="Number of Coins", value=f.split(':')[46])
    url = "http://gdidthingpython.000webhostapp.com/thing2.php?id=" + id
    f = requests.get(url).text
    if (f.split(':')[30] == "0"):
        if (f.split(':')[28] == ""):
            if (f.split(':')[14] == "10"):
                emb.set_thumbnail(url="https://i.imgur.com/Me0PbBA.png")
            elif (f.split(':')[14] == "20"):
                emb.set_thumbnail(url="https://i.imgur.com/RF8Ohrk.png")
            elif (f.split(':')[14] == "30"):
                emb.set_thumbnail(url="https://i.imgur.com/ZHEbA1V.png")
            elif (f.split(':')[14] == "40"):
                emb.set_thumbnail(url="https://i.imgur.com/0T6f1GN.png")
            elif (f.split(':')[14] == "50"):
                emb.set_thumbnail(url="https://i.imgur.com/lj4TsCh.png")
            elif (f.split(':')[14] == "0"):
                emb.set_thumbnail(url="https://i.imgur.com/VrQy39m.png")
        else:
            emb.set_thumbnail(url="https://i.imgur.com/jLKq8zv.png")
    await ctx.message.channel.send(embed=emb)

@client.command(pass_context=True, aliases=["sha512encode"])
async def sha512e(ctx, *args):
    m = ' '.join(args)
    emb = (discord.Embed(colour=0xf7b8cf))
    emb.add_field(name="SHA512 Hash", value=hashlib.sha512(m.encode('utf-8')).hexdigest())
    await ctx.message.channel.send(embed=emb)

@client.command(pass_context=True, aliases=["sha256encode"])
async def sha256e(ctx, *args):
    m = ' '.join(args)
    emb = (discord.Embed(colour=0xf7b8cf))
    emb.add_field(name="SHA256 Hash", value=hashlib.sha256(m.encode('utf-8')).hexdigest())
    await ctx.message.channel.send(embed=emb)

@client.command(pass_context=True, aliases=["md5encode"])
async def md5e(ctx, *args):
    m = ' '.join(args)
    emb = (discord.Embed(colour=0xf7b8cf))
    emb.add_field(name="MD5 Hash", value=hashlib.md5(m.encode('utf-8')).hexdigest())
    await ctx.message.channel.send(embed=emb)

@client.command(pass_context=True)
async def atbash(ctx, *args):
    x = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
         'v', 'w', 'x', 'y', 'z']
    z = ' '.join(args)
    s = list(z.lower())
    for i in range(len(s)):
        for j in range(len(x)):
            if (x[j] == s[i]):
                break
        if (s[i] in x):
            s[i] = x[25 - j]
        if (z[i] == z[i].upper()):
            s[i] = s[i].upper()
    emb = (discord.Embed(colour=0xf7b8cf))
    emb.add_field(name="Atbash Cipher", value=''.join(s))
    await ctx.message.channel.send(embed=emb)

@client.command(pass_context=True)
async def top10(ctx):
    url = "https://gdprofiles.com/_top100"
    emb = (discord.Embed(colour=0xf7b8cf))
    emb.set_author(name="Top 10")
    f = requests.get(url).text
    count = 0
    i = 0
    while (count < 10):
        i += 1
        if (f.split('list-unstyled">')[1].split('gdprofiles.com/')[i].split('"')[0] != "_mods"):
            emb.add_field(name="#" + str(count + 1),
                          value=f.split('list-unstyled">')[1].split('gdprofiles.com/')[i].split('"')[0].replace('-',
                                                                                                                ' '))
            count += 1
    await ctx.message.channel.send(embed=emb)

@client.command(pass_context=True, aliases=["gdprofile", "gdprofiles"])
async def gdprof(ctx, *args):
    url = "https://gdprofiles.com/" + '-'.join(args)
    emb = (discord.Embed(colour=0xf7b8cf))
    try:
        f = requests.get(url).text
        emb.set_thumbnail(url=f.split('id="playericon" src="')[1].split('"')[0])
        emb.add_field(name="Rank: ", value=f.split('class="rankicon">')[1].split('<')[0])
        emb.add_field(name="Stars: ", value=f.split('class="rankicon">')[1].split('center">')[1].split('<')[0])
        emb.add_field(name="Diamonds: ", value=f.split('class="rankicon">')[1].split('center">')[2].split('<')[0])
        emb.add_field(name="Coins: ", value=f.split('class="rankicon">')[1].split('center">')[3].split('<')[0])
        emb.add_field(name="User Coins: ", value=f.split('class="rankicon">')[1].split('center">')[4].split('<')[0])
        emb.add_field(name="Demons: ", value=f.split('class="rankicon">')[1].split('center">')[5].split('<')[0])
        try:
            emb.add_field(name="Creator Points: ",
                          value=f.split('class="rankicon">')[1].split("</tr>")[0].split('center">')[6].split('<')[
                              0])
        except:
            pass
        if ("modBadge_1.png" in f):
            emb.add_field(name="Mod Status", value="Mod")
        elif ("modBadge_2.png" in f):
            emb.add_field(name="Mod Status", value="Elder Mod")
        for i in range(4):
            try:
                a = f.split('''"_blank"
    href="''')[i + 1].split('"')[0]
                if ('youtube' in a):
                    try:
                        z = requests.get(a).text.split('name="title" content="')[1].split('"')[0]
                        emb.add_field(name="Youtube", value="[" + z + "](" + a + ")")
                    except:
                        pass
                elif ('twitch' in a):
                    emb.add_field(name="Twitch", value="[" + a.split('tch.tv/')[1] + "](" + a + ")")
                elif ('twitter' in a):
                    try:
                        z = requests.get(a).text
                        if ("errorpage" not in z):
                            z = z.split('title>')[1].split(' (@')[0]
                            emb.add_field(name="Twitter", value="[" + z + "](" + a + ")")
                    except:
                        pass
                elif ('newgrounds' in a):
                    try:
                        emb.add_field(name="Newgrounds",
                                      value="[" + a.split('http://')[1].split('.')[0] + "](" + a + ")")
                    except:
                        pass
            except:
                pass
    except:
        emb.add_field(name="404", value="That User hasn't linked their account with GDProfiles!")
    await ctx.message.channel.send(embed=emb)

@client.command(pass_context=True, aliases=["randomlevel"])
async def rlevel(ctx):
    fin = ""
    while (True):
        i = modnar.randint(0, 50000000)
        url = "http://gdidthingpython.000webhostapp.com/thing.php?id=" + str(i)
        f1 = requests.get(url)
        f = f1.text
        if ("Level Not Found" in str(f)):
            fin = fin
        else:
            fin = str(i)
            break
    c = f1.content
    soup = BeautifulSoup(c, 'html.parser').prettify()
    emb = (discord.Embed(colour=0xf7b8cf))
    emb.set_author(name="Random Level")
    emb.add_field(name="Level Name", value=soup.split("aaKL,,OAS")[1].split("aaKL,,OAS")[0])
    emb.add_field(name="Level ID", value=str(i))
    url = "http://gdidthingpython.000webhostapp.com/thing2.php?id=" + str(i)
    f = requests.get(url).text
    if (f.split(':')[57] != "0"):
        emb.add_field(name="Level Author", value=f.split(':')[57])
    else:
        emb.add_field(name="Level Author", value="-")
    a = soup.split("aaKL,,OAS")[3].split("aaKL,,OAS")[0]
    if(soup.split("aaKL,,OAS")[3].split("aaKL,,OAS")[0] == ""):
        a = "No Description Provided"
    emb.add_field(name="Level Description", value=a)
    await ctx.message.channel.send(embed=emb)

@client.command(pass_context=True, aliases=["randomsong"])
async def rsong(ctx):
    fin = ""
    while (True):
        i = modnar.randint(0, 1000000)
        url = "https://www.newgrounds.com/audio/listen/" + str(i)
        f1 = requests.get(url)
        f = f1.text
        if ("No Audio Project exists" in str(f) or "This audio was removed" in str(f)):
            fin = fin
        else:
            fin = str(i)
            break
    a = f.split('title>')[1].split('<')[0]
    emb = (discord.Embed(colour=0xf7b8cf))
    emb.set_author(name="Random Song")
    emb.add_field(name="Title", value=a)
    emb.add_field(name="ID", value=fin)
    b = f.split('"artist":"')[1].split('"')[0]
    emb.add_field(name="Author", value=b)
    d = f.split('id="author_comments">')[1].split('</div>')[0].replace('</p>', '').replace('<p>', '')[1:]
    emb.add_field(name="Description", value=d.replace("<br>", ""))
    c = f.split('href="/audio/browse/genre/')[1].split('<')[0].split('>')[1]
    emb.add_field(name="Genre", value=c)
    await ctx.message.channel.send(embed=emb)

@client.command(pass_context=True, aliases=["gjpdecode", "geometryjumppassworddecode", "geometryjumppasswordd"])
async def gjpd(ctx, *args):
    s = ' '.join(args)
    s = base64.b64decode(s.encode('utf-8')).decode()
    s2 = ""
    if (len(s) < 5):
        for i in range(len(s)):
            s2 = s2 + "37526"[i]
    elif (len(s) > 5):
        while (len(s2) < len(s)):
            s2 = s2 + "37526"
        while (len(s2) != len(s)):
            s2 = list(s2)
            s2.pop(-1)
            s2 = ''.join(s2)
    out = ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s, s2))
    emb = (discord.Embed(colour=0xf7b8cf))
    emb.add_field(name="GJP Decoded String:", value=out)
    await ctx.message.channel.send(embed=emb)

@client.command(pass_context=True, aliases=["gjpencode", "geometryjumppasswordencode", "geometryjumppassworde"])
async def gjpe(ctx, *args):
    s = ' '.join(args)
    if(len(s) > 5):
        s2 = ""
        if(len(s) < 5):
            for i in range(len(s)):
                s2 = s2 + "37526"[i]
        elif(len(s) > 5):
            while(len(s2) < len(s)):
                s2 = s2 + "37526"
            while(len(s2) != len(s)):
                s2 = list(s2)
                s2.pop(-1)
                s2 = ''.join(s2)
        out = ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s,s2))
        out = base64.b64encode(out.encode('utf-8'))
        print(out.decode())
        emb = (discord.Embed(colour=0xf7b8cf))
        emb.add_field(name="GJP Encoded String:", value=out.decode())
        await ctx.message.channel.send(embed=emb)
    else:
        await ctx.message.channel.send("Input not long enough! *(>=6 characters!)*")

@client.command(pass_context=True, aliases=["rtee", "rteencode", "robtopterribleencryptione", "robtopterribleencryptionencode", "robencode"])
async def robe(ctx, *args):
    s = ' '.join(args)
    s2 = ""
    if(len(s) >= 6):
        if(len(s) < 5):
            for i in range(len(s)):
                s2 = s2 + "26364"[i]
        elif(len(s) > 5):
            while(len(s2) < len(s)):
                s2 = s2 + "26364"
            while(len(s2) != len(s)):
                s2 = list(s2)
                s2.pop(-1)
                s2 = ''.join(s2)
        out = ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s,s2))
        out = base64.b64encode(out.encode('utf-8'))
        emb = (discord.Embed(colour=0xf7b8cf))
        emb.add_field(name="RTE Encoded String:", value=out.decode())
        await ctx.message.channel.send(embed=emb)
    else:
        await ctx.message.channel.send("Input not long enough! *(>=6 characters!)*")

@client.command(pass_context=True, aliases=["rted", "rtedecode", "robtopterribleencryptiond", "robtopterribleencryptiondecode", "robdecode"])
async def robd(ctx, *args):
    s = ' '.join(args)
    s = base64.b64decode(s.encode('utf-8')).decode()
    s2 = ""
    if (len(s) < 5):
        for i in range(len(s)):
            s2 = s2 + "26364"[i]
    elif (len(s) > 5):
        while (len(s2) < len(s)):
            s2 = s2 + "26364"
        while (len(s2) != len(s)):
            s2 = list(s2)
            s2.pop(-1)
            s2 = ''.join(s2)
    out = ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s, s2))
    emb = (discord.Embed(colour=0xf7b8cf))
    emb.add_field(name="RTE Decoded String:", value=out)
    await ctx.message.channel.send(embed=emb)

@client.command(pass_context=True, aliases=["mcserver", "minecraftserver"])
async def server(ctx, host):
    if(":" not in host):
        server = MinecraftServer.lookup(host + ":25565")
    else:
        server = MinecraftServer.lookup(host)
    statushow = server.status()
    await ctx.message.channel.send("There are " + str(statushow.players.online) + " people on " + host)

@client.command(pass_context=True)
async def ifunny(ctx):
    #<img class="media__image" src="
    resp = requests.get('https://ifunny.co/feeds/shuffle')
    page = resp.text
    thumbnail = str(page.split('<img class="media__image" src="')[1].split('"')[0])
    x = requests.get("https://ifunny.co" + str(page.split('<img class="media__image" src="')[0].split('href="')[-1].split('"')[0].split('?galler')[0])).text
    with codecs.open("ifunny.txt", "w", encoding="utf-8") as f:
        f.write(x)
    author = x.split('ontent_meta" href="/user/')[1].split('"')[0]
    tags = [i.split('<')[0] for i in x.split('"metapanel__copyright')[0].split('tag__name">')[1:]]
    likes = x.split('actionlink__text">')[1].split('<')[0]
    comments = x.split('actionlink__text">')[2].split('<')[0]
    emb = (discord.Embed(colour=0xf7b8cf))
    emb.set_author(name="Random Feature", url="https://ifunny.co" + str(page.split('<img class="media__image" src="')[0].split('href="')[-1].split('"')[0].split('?galler')[0]))
    emb.add_field(name="Author", value=author)
    emb.add_field(name="Tags", value="`" + ', '.join(tags) + '`')
    emb.add_field(name="Comments", value=comments)
    emb.add_field(name="Likes", value=likes)
    emb.set_image(url=thumbnail)
    await ctx.message.channel.send(embed=emb)

@client.command(pass_context=True, aliases=["ytsearch", "youtubesearch", "youtube"])
async def ysearch(ctx, *args):
    s = ' '.join(args)
    resp = requests.get('https://www.youtube.com:80/results?search_query=' + urllib.parse.quote(s))
    page = resp.text
    name = page.split('<h3 class="yt-lockup-title "><a href=')[1].split('>')[1].split('<')[0]
    link = "https://www.youtube.com:80" + page.split('<h3 class="yt-lockup-title "><a href=')[1].split('"')[1]
    thumbnail=str(page.split('<span class="yt-thumb-simple">')[1].split('src="')[1].split('"')[0])
    resp2 = requests.get(link)
    page2 = resp2.text
    desc = html.unescape(page2.split('<meta itemprop="description" content="')[1].split('"')[0])
    a = list(desc)
    emb = (discord.Embed(colour=0xf7b8cf))
    emb.set_author(name=html.unescape(str(name)), url=link)
    emb.set_thumbnail(url=thumbnail)
    if(desc != " "):
        emb.add_field(name="Description", value=desc)
    else:
        emb.add_field(name="Description", value="N/A")
    await ctx.message.channel.send(embed=emb)

@client.command(pass_context=True, aliases=["exec"])
async def execute(ctx, c):
    if(ctx.message.author.id == 190804082032640000):
        with codecs.open("thing.py", "w", encoding="utf8") as f:
            f.write(c)
        x = check_output(["py", "C:\\MewBot\\thing.py"], shell=True)
        emb = (discord.Embed(colour=0xf7b8cf))
        emb.add_field(name="Execute", value="```" + x.decode() + "```")
        await ctx.message.channel.send(embed=emb)
    else:
        await ctx.message.channel.send("You're not allowed.")
@client.command(pass_context=True, aliases=["bine", "binarye", "binencode", "binaryencode"])
async def binary(ctx, *args):
    s = ' '.join(args)
    emb = (discord.Embed(colour=0xf7b8cf))
    emb.add_field(name="Text to Binary", value=''.join([bin(ord(ch))[2:].zfill(8) for ch in s]))
    await ctx.message.channel.send(embed=emb)

@client.command(pass_context=True, aliases=["bind", "binaryd", "bindecode", "binarydecode"])
async def unbinary(ctx, *args):
    s = ' '.join(args)
    from textwrap import wrap
    z = wrap(s, 8)
    f = ""
    for i in range(len(z)):
        f = f + chr(int(z[i], 2))
    emb = (discord.Embed(colour=0xf7b8cf))
    emb.add_field(name="Binary to Text", value=f)
    await ctx.message.channel.send(embed=emb)

@client.command(pass_context=True, aliases=["a85decode", "ascii85d", "ascii85decode"])
async def a85d(ctx, *args):
    s = ' '.join(args)
    emb = (discord.Embed(colour=0xf7b8cf))
    if(s[:2] == "<~" and s[-2:] == "~>"):
        emb.add_field(name="Ascii85 Decoded Message", value=base64.a85decode(s.encode(), adobe=True).decode())
    else:
        emb.add_field(name="Ascii85 Decoded Message", value=base64.a85decode(s.encode()).decode())
    await ctx.message.channel.send(embed=emb)

@client.command(pass_context=True, aliases=["a85encode", "ascii85e", "ascii85encode"])
async def a85e(ctx, *args):
    s = ' '.join(args)
    emb = (discord.Embed(colour=0xf7b8cf))
    emb.add_field(name="Ascii85 Encoded Message", value=base64.a85encode(s.encode(), adobe=True).decode())
    await ctx.message.channel.send(embed=emb)

@client.command(pass_context=True, aliases=["user"])
async def userinfo(ctx, *args):
    if(args == ()):
        user = client.get_user(ctx.message.author.id)
    elif (args[0][:2] == "<@" and args[0][-1] == ">"):
        if (args[0][:3] == "<@!"):
            y = args[0].split("<@!")[1].split(">")[0]
        else:
            y = args[0].split("<@")[1].split(">")[0]
        user = await client.get_user_info(y)
    elif(isNum(args[0])):
        user = await client.get_user_info(args[0])
    emb = (discord.Embed(colour=0xf7b8cf))
    av = user.avatar_url
    member = ctx.message.guild.get_member(user_id=user.id)
    username = user.name
    nick = user.display_name
    disc = user.discriminator
    stat = str(member.status)
    eyedee = str(user.id)
    cr = (member.created_at + datetime.timedelta(hours=-5)).strftime("%m-%d-%Y %H:%M:%S")
    if(member.activity):
        E = list(str(member.activity.type).split('.')[-1])
        E[0] = E[0].upper()
        E = ''.join(E)
    else:
        E = ""
    emb = (discord.Embed(colour=0xf7b8cf))
    emb.set_thumbnail(url=av)
    emb.add_field(name="Username", value=str(username))
    emb.add_field(name="Nickname", value=nick)
    emb.add_field(name="Discriminator (tag)", value=disc)
    emb.add_field(name="Status", value=stat)
    emb.add_field(name="User ID", value=eyedee)
    if(E != ""):
        emb.add_field(name=E, value=member.activity.name)
    emb.set_footer(text="Created on " + cr + " EST")
    await ctx.message.channel.send(embed=emb)


@client.command(pass_context=True, aliases=["b64encode", "base64e", "base64encode"])
async def b64e(ctx, *args):
    m = ' '.join(args)
    m = base64.b64encode(m.encode())
    emb = (discord.Embed(colour=0xf7b8cf))
    emb.add_field(name="Encoded Base64 String", value=m.decode())
    await ctx.message.channel.send(embed = emb)

@client.command(pass_context=True, aliases=["b64decode", "base64d", "base64decode"])
async def b64d(ctx, *args):
    m = ' ' .join(args)
    m = base64.b64decode(m.encode())
    emb = (discord.Embed(colour=0xf7b8cf))
    emb.add_field(name="Decoded Base64 String", value=m.decode())
    await ctx.message.channel.send(embed = emb)

@client.command(pass_context=True, aliases=["reverse"])
async def flip(ctx, *args):
    m = ' '.join(args)
    f = []
    for i in range(len(m) - 1, -1, -1):
        f.append(m[i])
    emb = (discord.Embed(colour=0xf7b8cf))
    emb.add_field(name="Flipped Text", value=''.join(f))
    await ctx.message.channel.send(embed = emb)

@client.command(pass_context=True)
async def jeff(ctx, user: discord.User):
    await ctx.message.channel.send(file=discord.File(open("jeff.jpg", "rb"), filename="jeff.jpg"))
    await ctx.message.channel.send(str(user.mention) + ", You just got jeff'd by " + str(ctx.message.author.mention))

@client.command(pass_context=True, aliases=["coin"])
async def coinflip(ctx):
    p = [1, 2]
    choic = modnar.choice(p)
    if(choic == 1):
        emb = (discord.Embed(colour=0xf7b8cf))
        emb.add_field(name="Coinflip", value='You Got Tails!')
    else:
        emb = (discord.Embed(colour=0xf7b8cf))
        emb.add_field(name="Coinflip", value='You Got Heads!')
    await ctx.message.channel.send(embed=emb)

@client.command(pass_context=True)
async def say(ctx, *args):
    await ctx.message.channel.send(' '.join(args))

@client.command(pass_context=True)
async def daily(ctx):
    current = datetime.datetime.now()
    f = open("daily.txt", "r")
    x = str(ctx.message.author.id)
    ln = 0
    l = ""
    p = []
    count = 0
    for i, line in enumerate(f):
        if(x in line.split()):
            ln = i
            l = line
            count += 1
        p.append(line)
    f.close()
    if(count == 0):
        await ctx.message.channel.send("You haven't used the daily system before! Let me set you up with something.")
        f = open("daily.txt", "a")
        f.write(x + " " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        f.close()
        return
    z = p[ln].split()[1].split('-')
    y = p[ln].split()[1:3]
    if(datetime.datetime.now() > datetime.datetime.strptime(' '.join(y), '%Y-%m-%d %H:%M:%S') + datetime.timedelta(days=1)):
        x = str(ctx.message.author.id)
        aa = []
        l1 = 0
        c1 = ""
        count = 0
        file = open("aaa.txt", "r")
        for i, line in enumerate(file):
            if(x in line.split()):
                l1 = i
                c1 = line
                count += 1
            aa.append(line)
        file.close()
        if(count == 0):
            await ctx.message.channel.send("You don't have an account!")
            return
        for i in range(len(aa)):
            if(aa[i] == c1):
                aa[i] = aa[i].split()
                di = aa[i][0]
                z = int(aa[i][1])
                z += 50
                z = str(z)
                aa[i] = di + " " + z + "\n"
        p[ln] = x + " " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
        f = open("aaa.txt", "w")
        f.write(''.join(aa))
        f.close()
        f = open("daily.txt", "w")
        f.write(''.join(p))
        f.close()
        await ctx.message.channel.send("Daily Reward Claimed: $50!")
        return
    else:
        FMT = '%Y-%m-%d %H:%M:%S'
        apap = datetime.datetime.strptime(' '.join(y), '%Y-%m-%d %H:%M:%S') + datetime.timedelta(days=1) - datetime.datetime.now()
        apap = apap - datetime.timedelta(microseconds=apap.microseconds)
        x = "You have " + str(apap) + " left!"
        await ctx.message.channel.send(x)

@client.command(pass_context=True)
async def pay(ctx, user: discord.User, amount):
    if("." in list(amount) or int(amount) < 1):
        await ctx.message.channel.send("You can't do that!")
    else:
        x = str(ctx.message.author.mention)
        xx = str(user.mention)
        xi = str(ctx.message.author.id)
        xxi = str(user.id)
        l1 = 0
        l2 = 0
        c1 = 0
        c2 = 0
        f = open("aaa.txt", "r")
        x = []
        count1 = 0
        count2 = 0
        for i, line in enumerate(f):
            if(xi in line.split()):
                l1 = i
                c1 = line
                count1 += 1
            if(xxi in line.split()):
                l2 = i
                c2 = line
                count2 += 1
            x.append(line)
        f.close()
        if(count1 == 0):
            await ctx.message.channel.send("You don't have an account!")
            return
        if(count2 == 0):
            await ctx.message.channel.send(xx + " doesn't have an account!")
            return
        for i in range(len(x)):
            if(x[i] == c1):
                x[i] = x[i].split()
                di = x[i][0]
                z = int(x[i][1])
                if(z - int(amount) < 0):
                    x[i] = ' '.join(x[i])
                    await ctx.message.channel.send("You don't have the money to do that!")
                    break
                else:
                    await ctx.message.channel.send("Sent $" + amount + " to " + str(user.mention) + "!")
                    z -= int(amount)
                    z = str(z)
                    x[i] = di + " " + z + "\n"
            if(x[i] == c2):
                x[i] = x[i].split()
                di = x[i][0]
                z = int(x[i][1])
                z += int(amount)
                z = str(z)
                x[i] = di + " " + z + "\n"
        f = open("aaa.txt", "w")
        f.write(''.join(x))
        f.close()

@client.command(pass_context=True)
async def money(ctx, *args):
    if(not args):
        f = open("aaa.txt", "r")
        count = 0
        for line in f:
            if(str(ctx.message.author.id) in line):
                count = line
        if(count == 0):
            f.close()
            f = open("aaa.txt", "a")
            f.write(str(ctx.message.author.id) + " 0\n")
            await ctx.message.channel.send("You don't have an account, so I made one for you!")
            f.close()
        else:
            f.close()
            f = open("aaa.txt", "r")
            x = str(count).split()[1]
            await ctx.message.channel.send("You have $" + x + "!")
        f.close()
    else:
        f = open("aaa.txt", "r")
        count = 0
        for line in f:
            if(str(user.id) in line):
                count = line
        if(count == 0):
            f.close()
            f = open("aaa.txt", "a")
            f.write(str(user.id) + " 0\n")
            await ctx.message.channel.send(str(user.mention) + " doesn't have an account, so I made one for them!")
            f.close()
        else:
            f.close()
            f = open("aaa.txt", "r")
            x = str(count).split()[1]
            await ctx.message.channel.send(str(user.mention) + " has $" + x + "!")
        f.close()


@client.command(pass_context=True)
async def help(ctx, *args):
    x = list(args)
    if(x == []):
        emb = (discord.Embed(colour=0xf7b8cf))
        emb.set_author(name="Help Menu for " + str(client.user.name))
        emb.add_field(name="Links", value="Invite: https://bit.ly/2wzmka1\nYoutube: https://bit.ly/2LBCd6B\nTwitter: https://bit.ly/2IPFv8u", inline=True)
        emb.add_field(name="Help Commands", value="Fun: mb!help --fun\nEncryption: mb!help --encryption\nMoney: mb!help --money\nInfo: mb!help --info\nModeration: mb!help --mod", inline=True)
        await ctx.message.channel.send(embed = emb)
    elif(x[0] == "--fun"):
        emb = (discord.Embed(colour=0xf7b8cf))
        emb.set_author(name="Fun Commands")
        emb.add_field(name='mb!sugg DESCRIPTION', value="Suggest for something to be added to MewBot!\n`e.g. mb!sugg There should be a money system!`", inline=True)
        emb.add_field(name='mb!duel @MENTION', value="Duel someone, and see who wins!\n`e.g. mb!duel @Monstahhh`", inline=True)
        emb.add_field(name='mb!jeff @MENTION', value="Jeff someone!\n`e.g. mb!jeff @Monstahhh`", inline=True)
        emb.add_field(name='mb!coinflip', value="Flip a coin!\n`e.g. mb!coinflip`", inline=True)
        emb.add_field(name='mb!say DESCRIPTION', value="Have MewBot say something!\n`e.g. mb!say Hello, world!`", inline=True)
        emb.add_field(name='mb!emoji LETTERS', value="Turn a sentence into :regional_indicator_b: :regional_indicator_i: :regional_indicator_g:  :regional_indicator_l: :regional_indicator_e: :regional_indicator_t: :regional_indicator_t: :regional_indicator_e: :regional_indicator_r: :regional_indicator_s:!\n`e.g. mb!emoji big letters`", inline=True)
        emb.add_field(name='mb!bigletter LETTERS', value="Alias to mb!emoji\n`e.g. mb!bigletter big letters`", inline=True)
        emb.add_field(name='mb!df IMAGE', value="Deep fries an image!\n`e.g. mb!df https://bit.ly/2kzFWW9`", inline=True)
        emb.add_field(name='mb!otter', value="Displays an image of an otter! (Thanks Theeo)\n`e.g. mb!otter`", inline=True)
        emb.add_field(name='mb!sayd DESCRIPTION', value="Have MewBot say something, then delete your message!\n`e.g. mb!sayd Hello, world!`", inline=True)
        emb.add_field(name='mb!rlevel', value="Gives a random Geometry Dash Level!\n`e.g. mb!rlevel`", inline=True)
        emb.add_field(name='mb!rsong', value="Gives a random Newgrounds song!\n`e.g. mb!rsong`", inline=True)
        emb.add_field(name='mb!blurple IMAGE', value="Blurples an image!\n`e.g. mb!blurple https://bit.ly/2kzFWW9`", inline=True)
        emb.add_field(name='mb!lpass LEVEL', value="Gives the password to a level in GD!\n`e.g. mb!lpass Cataclysm`", inline=True)
        emb.add_field(name='mb!trade', value="WIP")
        emb.add_field(name='mb!music BPM FORMAT', value="Makes music!\n`e.g. mb!music 100 C4|C4|G4|G4|A4|A4|G4||F4|F4|E4|E4|D4|D4|C4||`", inline=True)
        emb.add_field(name='mb!translate LANGFROM LANGTO MESSAGE', value="Translates a message to the desired language from the desired language!\n`e.g. mb!translate en de Hello, world!`", inline=True)
        await ctx.message.channel.send(embed=emb)
    elif(x[0] == "--encryption"):
        emb = (discord.Embed(colour=0xf7b8cf))
        emb.set_author(name="Encryption Commands")
        emb.add_field(name="mb!flip STRING", value="Flips a string around!\n`e.g. mb!flip Hello, world!`", inline=True)
        emb.add_field(name="mb!b64e STRING", value="Converts a string into Base64\n`e.g. mb!b64e Hello, world!`", inline=True)
        emb.add_field(name="mb!b64d BASE64STRING", value="Converts a Base64 Encoded string back into normal!\n`e.g. mb!b64d SGVsbG8sIHdvcmxkIQ==`", inline=True)
        emb.add_field(name="mb!binary STRING", value="Converts a string into Binary\n`e.g. mb!binary Hello, world!`", inline=True)
        emb.add_field(name="mb!unbinary BINARYSTRING", value="Converts a Binary Encoded string back into normal!\n`e.g. mb!unbinary 01000010`", inline=True)
        emb.add_field(name="mb!a85e STRING", value="Converts a string into ASCII85\n`e.g. mb!a85e Hello, world!`", inline=True)
        emb.add_field(name="mb!a85d ASCII85STRING", value="Converts an ASCII85 encoded string back into normal!\n`e.g. mb!a85d 87cURD_*#TDfTZ)+T`", inline=True)
        emb.add_field(name="mb!gjpe STRING", value="Converts a string into a GJP!\n`e.g. mb!gjpe Hello, world!`", inline=True)
        emb.add_field(name="mb!gjpd GJPSTRING", value="Converts a GJP String into normal!\n`e.g. mb!gjpd e1JZXlkfF0JdRF9TFA==`", inline=True)
        emb.add_field(name="mb!isprime NUMBER", value="Tells if a number is prime or not!\n`e.g. mb!isprime 3301`", inline=True)
        emb.add_field(name="mb!length STRING", value="Tells the length of a string!\n`e.g. mb!length Hello, world!`", inline=True)
        emb.add_field(name="mb!lowercase STRING", value="Turns a string into all lowercase!\n`e.g. mb!lowercase Hello, WORLD!`", inline=True)
        emb.add_field(name="mb!uppercase STRING", value="Turns a string into all uppercase!\n`e.g. mb!uppercase hello, world!`", inline=True)
        emb.add_field(name="mb!morsee STRING", value="Converts a string into morse code!\n`e.g. mb!morsee Hello, world!`", inline=True)
        emb.add_field(name="mb!morsed STRING", value="Converts a Morse Encoded String into normal!\n`e.g. mb!morsed .... . .-.. .-.. --- .-.-.-`", inline=True)
        emb.add_field(name="mb!hexe STRING", value="Converts a string into Hexadecimal!\n`e.g. mb!hexe Hello, world!`", inline=True)
        emb.add_field(name="mb!hexd STRING", value="Converts a Hex encoded string into normal!\n`e.g. mb!hexd 48656C6C6F21`", inline=True)
        emb.add_field(name="mb!md5e STRING", value="Converts a string into an MD5 hash!\n`e.g. mb!md5e Hello, world!`", inline=True)
        emb.add_field(name="mb!sha256e STRING", value="Converts a string into a SHA-256 hash!\n`e.g. mb!sha256e Hello, world!`", inline=True)
        emb.add_field(name="mb!sha512e STRING", value="Converts a string into a SHA-512 hash!\n`e.g. mb!sha512e Hello, world!`", inline=True)
        emb.add_field(name="mb!atbash STRING", value="Runs a string through an atbash cipher!\n`e.g. mb!atbash Hello, world!`", inline=True)
        emb.add_field(name="mb!robe STRING", value="Converts a string using RobTop's Terrible Encryption (RTE)!\n`e.g. mb!robe Hello, world!`", inline=True)
        emb.add_field(name="mb!robd STRING", value="Converts a RTE Encoded string into normal!\n`e.g. mb!robd elNfWlseFkRZRl5SEg==`", inline=True)
        await ctx.message.channel.send(embed=emb)
    elif(x[0] == "--money"):
        emb = (discord.Embed(colour=0xf7b8cf))
        emb.set_author(name="Money Commands")
        emb.add_field(name="mb!daily", value="Collect your daily 50 bucks!\n`e.g. mb!daily`", inline=True)
        emb.add_field(name="mb!money", value="Get your balance!\n`e.g. mb!money`", inline=True)
        emb.add_field(name="mb!othermoney @MENTION", value="Get the balance of someone else!\n`e.g. mb!othermoney @Monstahhh`", inline=True)
        emb.add_field(name="mb!pay @MENTION AMOUNT", value="Pay someone some money!\n`e.g. mb!pay @Venom 50`", inline=True)
        await ctx.message.channel.send(embed=emb)
    elif(x[0] == "--info"):
        emb = (discord.Embed(colour=0xf7b8cf))
        emb.set_author(name="Info Commands")
        emb.add_field(name="mb!hs PLAYER", value="Get the Hypixel stats of a player!\n`e.g. mb!hs GDNewbie`", inline=True)
        emb.add_field(name="mb!csp SKIN", value="Get the Steam Listed Price of a CS:GO Skin!\n`e.g. mb!csp Gut Knife | Marble Fade (Factory New)`", inline=True)
        emb.add_field(name="mb!ping", value="Gets MewBot's ping!\n`e.g. mb!ping`", inline=True)
        emb.add_field(name="mb!userinfo @MENTION", value="Gets the info of a user!\n`e.g. mb!userinfo @Venom`", inline=True)
        emb.add_field(name="mb!ysearch STRING", value="Searches Youtube with your params!\n`e.g. mb!ysearch Geometry Dash Newbie`", inline=True)
        emb.add_field(name="mb!top10", value="Gets the Top 10 Players on the GD Leaderboard!\n`e.g. mb!top10`", inline=True)
        emb.add_field(name="mb!gdprof", value="Gets info on a GD Player thanks to https://gdprofiles.com\n`e.g. mb!gdprof Creator Newbie`", inline=True)
        emb.add_field(name="mb!character CHARS", value="Gets info on each of the characters you type in a string!\n`e.g. mb!character Hello`", inline=True)
        emb.add_field(name="mb!botinfo", value="Gets the info of MewBot!\n`e.g. mb!botinfo`", inline=True)
        emb.add_field(name="mb!invite", value="Gives the invite link for MewBot!\n`e.g. mb!invite`", inline=True)
        emb.add_field(name="mb!level LEVEL", value="Gets the info on a level in GD!\n`e.g. mb!level Cataclysm`", inline=True)
        emb.add_field(name="mb!pokemon POKEMON", value="Gets the info of a pokemon!\n`e.g. mb!pokemon Pikachu`", inline=True)
        emb.add_field(name="mb!twitch USER", value="Gets the info of a Twitch user!\n`e.g. mb!twitch depianoman`", inline=True)
        await ctx.message.channel.send(embed=emb)
    elif(x[0] == "--mod"):
        emb = (discord.Embed(colour=0xf7b8cf))
        emb.set_author(name="Mod Commands")
        emb.add_field(name="mb!purge AMOUNT", value="Purges a specific number of messages from chat!\n`e.g. mb!purge 4`", inline=True)
        emb.add_field(name="mb!kick @MENTION", value="Kicks a person from the server!\n`e.g. mb!kick @Monstahhh`", inline=True)
        emb.add_field(name="mb!ban @MENTION", value="Bans a person from the server!\n`e.g. mb!ban @Monstahhh`", inline=True)
        emb.add_field(name="mb!tvotemute", value="Toggles allowing people to vote mute someone!\n`e.g. mb!tvotemute`", inline=True)
        emb.add_field(name="mb!votemute @MENTION", value="Starts a vote to mute someone!\n`e.g. mb!votemute @Monstahhh`", inline=True)
        await ctx.message.channel.send(embed=emb)

@client.command(pass_context=True)
async def ping(ctx):
    channel = ctx.message.channel
    t1 = time.perf_counter()
    await channel.trigger_typing()
    t2 = time.perf_counter()
    embed = discord.Embed(colour=0xf7b8cf)
    embed.set_author(name="Ping")
    embed.add_field(name="{}".format(round((t2 - t1) * 1000)) + ".0 ms", value="{}".format(round(t2 - t1, 3)) + " sec")
    await ctx.message.channel.send(embed=embed)

@client.command(pass_context=True, aliases=["hypixel", "hypixels", "hstats", "hypixelstats"])
async def hs(ctx, s):
    try:
        fmsg = ""

        page = requests.get("https://plancke.io/hypixel/player/stats/" + s)
        data = page.content

        atad = str(data)

        name = atad.split('meta name="og:description" content="')[1].split('"')[0]
        if(name[0] == " "):
            fmsg += name[1:] + "\n"
        else:
            fmsg += name + "\n"
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(data, 'html.parser')
        x = 0
        for i in range(len(soup.find_all(text=True))):
            if(soup.find_all(text=True)[i] == "Multiplier:"):
                x = i
                break
        for i in range(x, x + 16):
            if(i == x + 14):
                z = 0
                while(str(soup.find_all('a')[z].get_text()) != str(soup.find_all('a')[z].get_text()).lower()):
                    z += 1
                fmsg += "Friends: " + str(soup.find_all('a')[z].get_text()) + "\n"
            elif(x % 2 == 0):
                if(i % 2 == 0):
                    p = str(soup.find_all(text=True)[i]) + str(soup.find_all(text=True)[i + 1])
                    fmsg += p + "\n"
            else:
                if(i % 2 != 0):
                    p = str(soup.find_all(text=True)[i]) + str(soup.find_all(text=True)[i + 1])
                    fmsg += p + "\n"
        await ctx.message.channel.send(fmsg)
    except:
        await ctx.message.channel.send("Player not found!")

@client.command(pass_context=True)
async def duel(ctx, user: discord.User):
    x = str(ctx.message.author.mention)
    xx = str(user.mention)
    z = await ctx.message.channel.send("{}".format(x) + " duels " + "{}".format(xx))
    time.sleep(1.5)
    y = await z.edit(content="⚔ Dueling.")
    time.sleep(.5)
    y = await z.edit(content="⚔ Dueling..")
    time.sleep(.5)
    y = await z.edit(content="⚔ Dueling...")
    time.sleep(.5)
    l = modnar.randint(1, 2)
    if(l == 1):
        await z.edit(content="{}".format(x) + " has won!")
    else:
        await z.edit(content="{}".format(xx) + " has won!")

@client.command(pass_context=True, aliases=["suggest", "sg"])
async def sugg(ctx, *args):
    sugg = ' '.join(args)
    swears = ['anal', 'anus', 'arse', 'ass', 'ballsack', 'balls', 'bastard', 'bitch', 'biatch', 'bloody', 'blowjob', 'blow', 'bollock', 'bollok', 'boner', 'boob', 'bugger', 'bum', 'butt', 'buttplug', 'clitoris', 'cock', 'coon', 'crap', 'cunt', 'damn', 'dick', 'dildo', 'dyke', 'fag', 'feck', 'fellate', 'fellatio', 'felching', 'fuck', 'fudgepacker', 'packer', 'flange', 'goddamn', 'damn', 'hell', 'homo', 'jerk', 'jizz', 'knobend', 'knob', 'end', 'labia', 'lmao', 'lmfao', 'muff', 'nigger', 'nigga', 'omg', 'penis', 'piss', 'poop', 'porn', 'prick', 'pube', 'pussy', 'queer', 'scrotum', 'sex', 'shit', 'sh1t', 'slut', 'smegma', 'spunk', 'tit', 'tosser', 'turd', 'twat', 'vagina', 'wank', 'whore', 'wtf', 'negro', 'succ', 'retard', 'shiet', 'gay', 'dong', 'killyourself']
    x = sugg
    count = 0
    for i in range(len(swears)):
        if(swears[i] in ''.join(args)):
            count += 1
    with codecs.open("sugg.txt", "r", encoding="utf8") as f:
        a = f.readlines()[-1].split(" - ")[0]
        if(SequenceMatcher(None, a, sugg).ratio() >= 0.8):
            count += 1
    if(count > 0):
        await ctx.message.channel.send("Your suggestion looked like spam, so it wasn't sent!")
    else:
        f = codecs.open("sugg.txt", "a", encoding="utf-8")
        f.write(x + " - Suggested by " + str(ctx.message.author) + "\n")
        f.close()
        me = await client.get_user_info(190804082032640000)
        emb = (discord.Embed(colour=0xf7b8cf))
        emb.add_field(name=str(ctx.message.author), value=x)
        emb.set_footer(text="Sent at " + datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S") + " EST")
        await me.send(embed=emb)
        await ctx.message.channel.send("Suggestion sent!")

@client.command(pass_context=True, aliases=["csgoprice", "csprice", "counterstrikeglobaloffensiveprice"])
async def csp(ctx, *args):
    s = ' '.join(args)
    try:
        if("knife" in s.lower() or "bayonet" in s.lower() and s[0] != "★"):
            s = "★ " + s
        if("stattrak" in s.lower()):
            s = s.replace("StatTrak", "StatTrak™")
        y = urllib.parse.quote_plus(s)
        response = urllib.request.urlopen("http://steamcommunity.com/market/priceoverview/?currency=1&appid=730&market_hash_name=" + y)
        html = response.read()
        html = html.decode("utf-8")
        html1 = html.split('"lowest_price":"$')[1]
        html1s = html1.split('"')[0]
        html1s = html1s.replace(',', '')
        float1 = float(html1s)
        await ctx.message.channel.send("The price for " + s + " is $" + str(float1) + "!")
    except:
        await ctx.message.channel.send("Skin not Found!")

@client.command(pass_context=True)
async def xor(ctx, s1, s2):
    await ctx.message.channel.send(''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2)))

client.run(open("TOKEN.txt").read())
