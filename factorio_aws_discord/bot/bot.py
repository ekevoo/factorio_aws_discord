import traceback
from dataclasses import dataclass

from discord import Message, Client, User
from unsync import unsync

from factorio_aws_discord.bot.settings import settings

restart = True


# noinspection PyBroadException
@dataclass
class MessageHandler:
    """ Short-lived class that handles one message. """

    def __init__(self, bot: 'Bot', message: Message):
        self.bot = bot
        self.msg = message
        self.c: Client = bot.client
        self.t: str = message.content.strip()

    @unsync
    async def handle(self):
        if self.msg.author == self.bot.me:
            return  # I sent this message
        is_root = str(self.msg.author) in settings.root_member_names

        if self.msg.channel.is_private:
            # Got message privately; only accept from root users
            if not is_root:
                return await self._react('⛔')
        else:
            # Got message in a channel
            if self.t.startswith(self.bot.mention):  # Mentions me
                self.t = self.t[len(self.bot.mention):].strip()
            else:  # Doesn't mention me
                return  # This is where chat tunneling will reside

        command, *arguments = self.t.split()
        if is_root:
            if command.startswith('!'):
                return await self._eval()
            elif command == 'quit':
                return await self.c.close()
            elif command == 'restart':
                global restart
                restart = True
                return await self.c.close()

    @unsync
    async def _react(self, emoji):
        await self.c.add_reaction(self.msg, emoji)

    @unsync
    async def _respond(self, text):
        await self.c.send_message(self.msg.channel, text)

    @unsync
    async def _eval(self):
        try:
            expression = self.t[1:]
            value = eval(expression, globals(), locals())
            if not isinstance(value, str):
                value = repr(value)
            _ = self._respond(value)
            _ = self._react('✔')
        except Exception:
            _ = self._respond(traceback.format_exc())
            _ = self._react('❌')


class Bot:
    def __init__(self, client: Client):
        self.client: Client = client
        self.me: User = client.user
        self.mention: str = f'<@{self.me.id}>'
        print(f'We have logged in as {self.me}')


@unsync
async def main():
    client = Client()

    @client.event
    async def on_ready():
        bot = Bot(client)

        @client.event
        async def on_message(message: Message):
            await MessageHandler(bot, message).handle()

    try:
        await client.start(settings.bot_token)
    except KeyboardInterrupt:
        await client.logout()


if __name__ == '__main__':
    while restart:
        restart = False
        main().result()
