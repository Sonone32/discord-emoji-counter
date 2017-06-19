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
removePls = '❌' # Use this emoji to vote for deletion
countStore = 'voteCount' # Filename to store min_vote; must be present on start up
with open(countStore, 'r') as FILE: # Minimum amount of votes needed to initiate deletion
    min_vote = int(FILE.read())


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
    if (reaction.emoji == removePls) and reaction.count >= min_vote:
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
    if (not message.content.startswith('%minvote')) or (not message.author.server_permissions.administrator):
        return

    global min_vote
    msg = message.content.split()
    if len(msg) == 1:
        await reactBot.send_message(message.channel, 'Current minimum vote count is {}.'.format(min_vote))
        return
    elif len(msg) != 2:
        await reactBot.send_message(message.channel, 'Invalid command format, try `%minvote [number]`.')
        return

    try:
        min_vote = int(msg[1])
        await reactBot.send_message(message.channel, 'Minimum vote has been changed to {}.'.format(min_vote))

        with open(countStore, 'w') as FILE:
            FILE.write(str(min_vote))
        logger.info('Minimum vote has been set to %s by %s.', min_vote, message.author.id)
    except ValueError:
        await reactBot.send_message(message.channel, 'Please enter a valid number!')
    except:
        await reactBot.send_message(message.channel, 'An error has occured and the minimum vote remains to be {}.'.format(min_vote))

# Run the bot
reactBot.run(os.environ['DISCORD_TOKEN'])
