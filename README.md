## Brief

Snippet created for discord servers. Allows users to vote and delete contents instead of waiting for a moderator to respond to it. Responds to the ❌ emoji reaction by default.

## Commands

- Use `%minvote` to see the minimum amount of a certain reaction needed to delete a message.
- Use `%minvote <number>` to set the aforementioned minimum amount.
- Use `%emoji` to see the currently monitored emoji reaction.
- Use `%emoji <emoji>` to set the currently monitored emoji reaction. Note that the bot only checks for a character(which is what an emoji is) so if you entered an invalid emoji but a valid character the bot will malfunction; this can be easily fixable by resetting the emoji to watch out for.


## Improvements Needed

- The message deque is topped at 10k messages meaning reactions need to happen before the message exits the deque which might be too short of a time.
- The configuration is global, meaning multiple servers will share the same minimum vote count value.
- The commands are primitive and ugly at the moment.
- Pylint cries a lot on this script.
- Many more uncountable things...
