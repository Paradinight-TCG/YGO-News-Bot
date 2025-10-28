import discord
from discord.ext import commands, tasks
import requests
from bs4 import BeautifulSoup

import os
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = 1391796864646516896  # ID du salon où tu veux poster les tweets

intents = discord.Intents.default()
intents.message_content = True  # nécessaire pour lire les messages
bot = commands.Bot(command_prefix="!", intents=intents)

last_tweet = None  # garde le dernier tweet déjà posté


def get_latest_tweet():
    """Récupère le dernier tweet de YGOrganization depuis Nitter"""
    url = "https://nitter.net/ygorganization"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")
    tweet = soup.find("div", class_="timeline-item")
    if not tweet:
        return None
    link = tweet.find("a", class_="tweet-link")
    if link:
        return "https://x.com" + link["href"]
    return None


@bot.event
async def on_ready():
    print(f"{bot.user} est connecté !")
    check_tweets.start()


@tasks.loop(minutes=5)
async def check_tweets():
    """Vérifie les nouveaux tweets toutes les 5 minutes"""
    global last_tweet
    tweet_url = get_latest_tweet()
    if tweet_url and tweet_url != last_tweet:
        last_tweet = tweet_url
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            await channel.send(f"Nouveau post de @ygorganization : {tweet_url}")


bot.run(TOKEN)
