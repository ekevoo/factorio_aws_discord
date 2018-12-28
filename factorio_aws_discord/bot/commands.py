import traceback

from factorio_aws_discord.bot import bot


# noinspection PyBroadException
async def dispatch(msg: bot.ReceivedMessage, is_root: bool):
    command, *arguments = msg.text.split()
    handler = globals().get(f'_handle_{command}_command')
    if not handler:
        await msg.react('🤷')
        return
    try:
        result = await handler(msg, is_root, *arguments)
        if result is True:
            _ = msg.react('✔')
        elif result is False:
            _ = msg.react('🛑')
    except Exception:
        _ = msg.react('💥')
        if is_root:
            _ = msg.respond(traceback.format_exc())


async def _handle_help_command(msg: bot.ReceivedMessage, is_root: bool, *_):
    response = [
        f"Hi <@{msg.msg.author.id}>! I am {msg.bot.mention}, "
        "a bot created by <@241369752067506187>. I don't have very many commands just yet."
    ]
    if is_root:
        response.append(
            "Because you are root, you also have access to the following commands:"
            "\n`bot stop` - Please don't kill me 😢"
            # "\n`bot reload` - 🔄"
            "\n`!` 🐍 Debug any Python expression!"
        )
    await msg.respond('\n\n'.join(response))


async def _handle_bot_command(msg, is_root, argument=''):
    if not is_root:
        return False
    elif argument == 'stop':
        await msg.react('⚰')
        msg.bot.quit()
    else:
        msg.react('🤷')
