import discord
import os
import requests
import json
import random
from dotenv import load_dotenv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time
from keepAlive import keep_alive

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

analyzer = SentimentIntensityAnalyzer()

thank_you_words = [
    "thank you","thanks","thx","ty","tysm","tq","thank u",
    "thankyou","thanx","appreciate it","thanks a lot"
]

thank_you_replies = [
"You're very welcome! 😊",
"Anytime! Always happy to help.",
"Glad I could help!",
"No problem at all!",
"Happy to assist anytime.",
"You're always welcome here!",
"Anytime — that's what I'm here for!",
"You're welcome! Hope it helped.",
"My pleasure!",
"Always happy to help out.",
"Of course! Glad I could help.",
"No worries at all.",
"You're most welcome!",
"Happy to help! 😊",
"Glad it made things easier.",
"Anytime you need!",
"Always here if you need help.",
"You're welcome — keep going!",
"Happy I could help you out.",
"That's what friends are for!",
"You're welcome! Have a great day!",
"No problem — glad it helped!",
"Always happy to assist.",
"Anytime! Just ask.",
"Glad I could be useful.",
"You got it!",
"Happy to help, truly!",
"You're welcome — stay awesome!",
"Helping you made my day too!",
"Anytime at all!",
"You're welcome! Keep smiling 😊",
"Glad I could make things easier.",
"No problem — happy to help.",
"Of course! Always here.",
"Anytime you need a hand!",
"You're welcome! Keep up the good work.",
"My pleasure helping you.",
"Glad I could support you.",
"You're welcome! Don't hesitate to ask again.",
"Always here to help out!",
"You're welcome! Stay amazing.",
"Happy to be of help!",
"Anytime, friend!",
"You're welcome — glad it helped!",
"Helping is what I do!",
"Of course! Anytime.",
"You're welcome! 😊 Hope you have a great day.",
"Always happy to help where I can.",
"Glad I could be useful today.",
"You're welcome — take care!"
]


def getQuote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote


def is_sad(text):
    score = analyzer.polarity_scores(text)
    return score["compound"] < -0.4

# def is_positive(text):
#     score = analyzer.polarity_scores(text)
#     return score["compound"] > 0.5


@client.event
async def on_ready():
    print(f"Bot is online as {client.user}")


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    msg = message.content.lower()

    if msg.startswith("$inspire"):
        quote = getQuote()
        await message.channel.send(quote)
        return

    if any(word in msg for word in thank_you_words):
        await message.channel.send(random.choice(thank_you_replies))
        return

    if is_sad(msg):
        quote = getQuote()
        await message.channel.send(quote)

keep_alive()

while True:
    try:
        client.run(TOKEN)
    except Exception as e:
        print("Bot crashed, restarting in 5 seconds:", e)
        time.sleep(5)