from nonebot import on_command, on_message
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import (
    GroupMessageEvent,
    Bot,
    Message,
    MessageSegment
)
from nonebot.adapters.onebot.v11.permission import GROUP

from src.plugins.song_guess.data_source import generate_problem
from src.plugins.song_guess.plugins.guess.player import (
    Player,
    get_player,
    add_player,
    remove_player
)
from src.plugins.song_guess.model import check_answer, get_alias_list


async def timeout_reaction(player: Player):
    bot = player.server_bot
    event = player.event
    await bot.send(event, MessageSegment.record(player.original))
    message = f"超时啦！答案是{player.answer}！\n"
    message += "这些答案也同样正确：\n"
    message += "\n".join(await get_alias_list(player.answer)) + "\n"
    message += "如果您认为您回答的结果也是正确答案，可以联系bot管理员添加歌曲别名哦~"
    await bot.send(event, message, at_sender=True)
    await remove_player(player)


async def start_guess_rule(event: GroupMessageEvent):
    return event.is_tome() and (await get_player(event.get_user_id()) is None)


start_guess = on_command("猜歌", rule=start_guess_rule, aliases={"guess",}, priority=5, permission=GROUP, block=True)


@start_guess.handle()
async def _(bot: Bot, event: GroupMessageEvent, args: Message=CommandArg()):
    answer, original, instrumental = await generate_problem(10)
    player = Player(event, bot, 1, answer, original, instrumental)
    await start_guess.send(MessageSegment.record(instrumental))
    await start_guess.send("这段音乐对应哪首歌呢，请@小步梦并回答该歌曲的名称或者别名~（不必考虑标点符号和英文字符的大小写），您有一分钟时间思考和回答~", at_sender=True)
    player.timer_start()
    await add_player(player)


async def do_guess_rule(event: GroupMessageEvent):
    return event.is_tome() and (await get_player(event.user_id) is not None)


do_guess = on_message(rule=do_guess_rule, priority=10, permission=GROUP)


@do_guess.handle()
async def _(event: GroupMessageEvent):
    player_answer = event.get_plaintext()
    player = await get_player(event.user_id)
    if await check_answer(player_answer, player.answer):
        await do_guess.send(MessageSegment.record(player.original))
        message = f"猜对啦！答案就是{player.answer}！\n"
        message += "这些答案也同样正确：\n"
        message += "\n".join(await get_alias_list(player.answer))
        await do_guess.send(message, at_sender=True)
        player.timer_stop()
        await remove_player(player)
    else:
        await do_guess.send(f"不对哦！再想想吧！", at_sender=True)