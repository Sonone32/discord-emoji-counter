import asyncio
import logging
import os
import discord

# Logging set-up
logger = logging.getLogger('reactBot')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='reactBot.log', encoding='utf-8')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


# Client set-up
reactBot = discord.Client(max_messages=10000)
configStore = 'dataStore' # Filename to store min_vote and emoji to watch; must be present on start up
with open(configStore, 'r') as FILE: # Minimum amount of votes needed to initiate deletion
    min_vote, removePls = FILE.read().split()
    min_vote = int(min_vote)


# Chore
@reactBot.event
async def on_ready():
    logger.info('ReactBot online as %s with id %s', reactBot.user.name, reactBot.user.id)


# Reaction handling
@reactBot.event
async def on_reaction_add(reaction, user):
    args = [reaction.message.author.id, reaction.message.channel.name]

    # Return if the channel is not nsfw
    if not args[1].startswith('nsfw-'):
        return

    # Checks for relevant emojis, then checks if a deletion is needed
    if (reaction.emoji == removePls) and (reaction.count >= min_vote):
        # Tries at least three times to delete message if HTTPException occurs
        for i in range(3):
            try:
                await reactBot.delete_message(reaction.message)
                logger.info('Message from "%s" deleted in %s', *args)
                break
            except discord.Forbidden:
                logger.info('Not allowed to delete message from "%s" in %s', *args)
                break
            except discord.HTTPException:
                logger.info('HTTPException deleting message from "%s" in %s', *args)
                await asyncio.sleep(1)


# Config commands for mods, only available to one server as this is a proof of concept
@reactBot.event
async def on_message(message):
    # Returns if the message is not a command or the author is not an admin
    if (not message.content.startswith('%')) or (not message.author.server_permissions.administrator):
        return

    msg = message.content.split()
    global min_vote, removePls

    # %minvote command
    if message.content.startswith('%minvote'):

        if len(msg) == 1:
            await reactBot.send_message(message.channel, 'Current minimum vote count is {}.'.format(min_vote))
            return
        elif len(msg) != 2:
            await reactBot.send_message(message.channel, 'Invalid command format, try `%minvote [number]`.')
            return

        try:
            min_vote = int(msg[1])
            await reactBot.send_message(message.channel, 'Minimum vote has been changed to {}.'.format(min_vote))

            with open(configStore, 'w') as FILE:
                FILE.write(str(min_vote) + ' ' + removePls)
            logger.info('Minimum vote has been set to %s by %s.', min_vote, message.author.id)
        except ValueError:
            await reactBot.send_message(message.channel, 'Please enter a valid number!')
        except:
            await reactBot.send_message(message.channel, 'An error has occured and the minimum vote remains to be {}.'.format(min_vote))

    # %emoji command
    if message.content.startswith('%emoji'):

        if len(msg) == 1:
            await reactBot.send_message(message.channel, 'Currently monitoring {}.'.format(removePls))
            return
        elif len(msg) != 2:
            await reactBot.send_message(message.channel, 'Invalid command format, try `%emoji <emoji>`.')
            return

        try:
            removePls = msg[1]
            await reactBot.send_message(message.channel, 'Now monitoring {}.'.format(removePls))

            with open(configStore, 'w') as FILE:
                FILE.write(str(min_vote) + ' ' + removePls)
            logger.info('Monitoring %s per request of %s..', removePls, message.author.id)
        except:
            await reactBot.send_message(message.channel, 'An error has occured and the emoji monitored remains to be {}.'.format(removePls))

# Run the bot
reactBot.run(os.environ['DISCORD_TOKEN'])
