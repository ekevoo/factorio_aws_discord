import traceback
from dataclasses import dataclass

from discord import Message, Client, User
from unsync import unsync, Unfuture

from factorio_aws_discord.bot import commands
from factorio_aws_discord.bot.settings import settings


# noinspection PyBroadException
@dataclass
class ReceivedMessage:
    """ Short-lived class that handles one message. """

    def __init__(self, bot: 'Bot', message: Message):
        self.bot = bot
        self.msg = message
        self.client: Client = bot.client
        self.text: str = message.content.strip()

    @unsync
    async def handle(self):
        if self.msg.author == self.bot.me:
            return  # I sent this message
        is_root = str(self.msg.author) in settings.root_member_names

        if self.msg.channel.is_private:
            # Got message privately; only accept from root users
            if not is_root:
                return
        else:
            # Got message in a channel
            if self.text.startswith(self.bot.mention):
                # Mentions me
                self.text = self.text[len(self.bot.mention):].strip()
            else:
                # Doesn't mention me
                return  # TODO: Chat tunneling

        if self.text.startswith('!'):
            if is_root:
                return await self._eval()
            else:
                return await self.react('🛑')

        await commands.dispatch(self, is_root)

    @unsync
    async def react(self, emoji):
        await self.client.add_reaction(self.msg, emoji)

    @unsync
    async def respond(self, text):
        future: Unfuture = self.client.send_message(self.msg.channel, text)
        await future

    @unsync
    async def _eval(self):
        try:
            expression = self.text[1:]
            value = eval(expression, globals(), locals())
            if not isinstance(value, str):
                value = repr(value)
            _ = self.respond(value)
            _ = self.react('✔')
        except Exception:
            _ = self.respond(traceback.format_exc())
            _ = self.react('💥')


class Bot:
    def __init__(self, client: Client):
        self.client: Client = client
        self.me: User = client.user
        self.mention: str = f'<@{self.me.id}>'
        print(f'We have logged in as {self.me}')

    @unsync
    async def quit(self):
        await self.client.logout()


@unsync
async def main():
    client = Client()

    @client.event
    async def on_ready():
        bot = Bot(client)

        @client.event
        async def on_message(message: Message):
            await ReceivedMessage(bot, message).handle()

    try:
        await client.start(settings.bot_token)
    except KeyboardInterrupt:
        await client.logout()


if __name__ == '__main__':
    __future: Unfuture = main()
    __future.result()
