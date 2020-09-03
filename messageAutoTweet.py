import tweepy
import discord
import asyncio
import requests
import os
from discord.ext.commands import Bot
from PIL import Image


# tokens

discord_token = 'DISCORD_TOKEN_HERE'

api_key = 'TWITTER_API_KEY_HERE'
api_secret = 'TWITTER_API_KEY_SECRET_HERE'
access_token = 'TWITTER_ACCESS_TOKEN_HERE'
access_token_secret = 'TWITTER_ACCESS_TOKEN_SECRET_HERE'

# Authenticate to Twitter
auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
# ----------------------



client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
	channels = ["NAME_OF_CHANNEL_HERE"]

	if str(message.channel) in channels:
	    # we do not want the bot to reply to itself
	    if message.author == client.user:
	        return


	    if message.attachments:
	        msg = 'Thank You {0.author.mention}, your success has been posted!'.format(message)
	        
	        discord_name = message.author.name
	        discord_url = message.attachments[0].url
	        print(discord_name)
	        print(discord_url)
	        await post_twitter(discord_url, discord_name)
	        await message.channel.send(msg)



async def post_twitter(url, name):
	# download temp image
	myfile = requests.get(url)
	open('temp.png', 'wb').write(myfile.content)
	# ---------------------

	tweet = "Success from {}".format(name)
	# post to twitter and delete temp image
	api.update_with_media('temp.png', tweet)
	os.remove("temp.png")
	# -----------------------


client.run(discord_token)
