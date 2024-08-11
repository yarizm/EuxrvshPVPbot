# -*- coding: utf-8 -*-
import asyncio
import os
import botpy
from botpy import logging, BotAPI
from botpy.ext.cog_yaml import read
from botpy.ext.command_util import Commands
from botpy.message import GroupMessage, Message
from examples import game
from plugins import chat_api

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()

# 开始游戏
@Commands("/START","/start")
async def start(api: BotAPI, message: Message, params=None):
    _log.info(params)
    result = game.startgame(params)
    result = str(result)
    nowturn = game.turnnum()
    nowturn = int(nowturn)
    nowturn += 1
    await message.reply(content=f"启动！当前游戏玩家为{result},接下来请输入/PICK+您的id+您要选择的角色id来选择角色。\n\n"
                                f"若您不知道角色对应的id，请输入/ROLEID来查看。\n\n"
                                f"下个回合为第{nowturn}回合,在回合开始前，您可以输入/GIVEUP+玩家id来放弃回合。\n\n"
                                f"随后,您可以输入/OUT来输出当回合的结果！")

    return True

# 在游戏开始前选择角色
@Commands("/PICK","/pick")
async def pick(api: BotAPI, message: Message,params=None):
    params = params.split()
    _log.info(params)
    result = game.pickrole(params[0],params[1])
    await message.reply(content=f"{result}")

    return True

# 查看角色基本信息
@Commands("/ROLEID","/roleid")
async def roleid(api: BotAPI, message: Message,params=None):
    result = game.roleinfo()
    result = '\n'.join(str(elem) for elem in result)
    await message.reply(content=f"\n{result}")

    return True

# 使用计时功能
@Commands("/REMTIME","/remtime")
async def remtime(api: BotAPI, message: Message,params=None):
    params = params.split()
    result = game.timerem(params[0],params[1],params[2])
    await message.reply(content=f"\n{result}")

    return True
# 查看当前计时
@Commands("/TIMEINFO","/timeinfo")
async def timeinfo(api: BotAPI, message: Message,params=None):
    result = game.timeinfo()
    result = '\n\n'.join(str(elem) for elem in result)
    await message.reply(content=f"\n{result}")

    return True
# 手动修改计时
@Commands("/TIMESET","/timeset")
async def timeset(api: BotAPI, message: Message,params=None):
    params = params.split()
    result = game.remsubhand(params[0],params[1],params[2])
    await message.reply(content=f"\n{result}")

    return True

# 更改角色的HP
@Commands("/HPC","/hpc")
async def hpc(api: BotAPI, message: Message,params=None):
    params = params.split()
    _log.info(params)
    result = game.hp_change(params[0],params[1],params[2])
    await message.reply(content=f"{result}")

    return True
# 更改角色的ATK
@Commands("/ATKC","/atkc")
async def atkc(api: BotAPI, message: Message,params=None):
    params = params.split()
    _log.info(params)
    result = game.atk_change(params[0],params[1])
    await message.reply(content=f"{result}")

    return True
# 使用角色的一个技能
@Commands("/SKILL","/skill")
async def skill(api: BotAPI, message: Message,params=None):
    params = params.split()
    _log.info(params)
    result = game.skill_use(params[0],params[1])
    await message.reply(content=f"{result}")

    return True
# 更改角色的一个技能CD
@Commands("/CDC","/cdc")
async def cdc(api: BotAPI, message: Message,params=None):
    params = params.split()
    _log.info(params)
    result = game.cd_change(params[0],params[1],params[2])
    await message.reply(content=f"{result}")

    return True
# 更改角色的防御值
@Commands("/DEFC","/defc")
async def defc(api: BotAPI, message: Message,params=None):
    params = params.split()
    _log.info(params)
    result = game.def_change(params[0],params[1])
    await message.reply(content=f"{result}")

    return True
# 更改角色的攻击距离
@Commands("/DISC","/disc")
async def disc(api: BotAPI, message: Message,params=None):
    params = params.split()
    _log.info(params)
    result = game.distance_change(params[0],params[1])
    await message.reply(content=f"{result}")

    return True
# 查看玩家当前的信息
@Commands("/ROLEDATA","/roledata")
async def roledata(api: BotAPI, message: Message,params=None):
    result1 = game.turnend(0)
    result1 = '\n\n'.join(str(elem) for elem in result1)
    await message.reply(content=f"玩家的数据:\n\n"
                                f"{result1}")

    return True

# 前置放弃回合
@Commands("/BGIVEUP","/bgiveup")
async def bgiveup(api: BotAPI, message: Message, params=None):
    _log.info(params)
    result = game.beforegiveup(params)
    await message.reply(content=f"{result}")

    return True
# 后置放弃回合
@Commands("/LGIVEUP","/lgiveup")
async def lgiveup(api: BotAPI, message: Message, params=None):
    _log.info(params)
    result = game.latergiveup(params)
    await message.reply(content=f"{result}")

    return True


# 概率为66%的判定
@Commands("/RATE66","/rate66")
async def Rate66(api: BotAPI, message: Message, params=None):
    result = game.rate66()
    if result:
        await message.reply(content="判定成功")
    else:
        await message.reply(content="判定失败")

    return True
# 概率为50%的判定
@Commands("/RATE50","/rate50")
async def Rate50(api: BotAPI, message: Message, params=None):
    result = game.rate50()
    print(result)
    if result:
        await message.reply(content="判定成功")
    else:
        await message.reply(content="判定失败")

    return True
# 概率为75%的判定
@Commands("/RATE75","/rate75")
async def Rate75(api: BotAPI, message: Message, params=None):
    result = game.rate75()
    if result:
        await message.reply(content="判定成功")
    else:
        await message.reply(content="判定失败")

    return True
# 概率为25%的判定
@Commands("/RATE25","/rate25")
async def Rate25(api: BotAPI, message: Message, params=None):
    result = game.rate25()
    if result:
        await message.reply(content="判定成功")
    else:
        await message.reply(content="判定失败")

    return True
# 概率为33%的判定
@Commands("/RATE33","/rate33")
async def Rate33(api: BotAPI, message: Message, params=None):
    result = game.rate33()
    if result:
        await message.reply(content="判定成功")
    else:
        await message.reply(content="判定失败")

    return True
# 输出一个回合的结果
@Commands("/OUT","/out")
async def out(api: BotAPI, message: Message,params=None):

    game.resetdef()
    game.remsubauto()
    result1 = game.turnend(1)
    result = game.outprint()
    result1 = '\n\n'.join(str(elem) for elem in result1)
    result = '\n\n'.join(str(elem) for elem in result)
    nowturn = game.turnnum()
    nowturn = int(nowturn)
    nowturn += 1


    await message.reply(content=f"当前回合为第{nowturn-1}回合,玩家行动机会为：\n\n"
                                f"{result}\n\n"
                                f"若您本回合有行动机会，您可以输入/LGIVEUP+玩家id来放弃本回合\n\n"
                                f"玩家的数据:\n\n"
                                f"{result1}\n\n"
                                f"下个回合为第{nowturn}回合,在回合开始前，您可以输入/BGIVEUP+玩家id来放弃回合")

    return True


# 结束一局游戏
@Commands("/END","/end")
async def end(api: BotAPI, message: Message,params=None):

    nowturn = game.turnnum()
    nowturn = int(nowturn)
    game.remreset()
    result = game.endgame()
    print(result)
    await message.reply(content=f"游戏已经结束!\n\n"
                                f"游戏总进行回合为{nowturn}")
    return True
# 问AI
@Commands("/AI","/ai")
async def ai(api: BotAPI, message: Message,params=None):
    msg = params
    result = chat_api.chat_answer(text=msg)

    await message.reply(content=f"{result}")
    return True
# 指令格式帮助
@Commands("/HELP","/help")
async def help(api: BotAPI, message: Message,params=None):


    await message.reply(content="局内指令格式一览：\n\n"
                                "改变血量：/HPC + 玩家id + 改变数值(正加负减) + 改变类型(0为当前HP，1为最大HP) \n"
                                "改变ATK：/ATKC + 玩家id + 改变数值(正加负减) \n"
                                "改变DEF：/DEFC + 玩家id + 改变数值(正加负减) \n"
                                "改变CD：/CDC + 玩家id + 技能编号 + 改变数值(正加负减) \n"
                                "使用技能：/SKILL + 玩家id + 技能编号 \n"
                                "改变攻击距离：/DISC + 玩家id + 改变数值(正加负减)\n"
                                "使用计时功能：/REMTIME + 玩家id + 计时名(自定义) + 计时数\n"
                                "手动更改计时:/TIMESET + 玩家id + 计时名(自定义) + 改变数值(正加负减)\n"
                                "查看计时:/TIMEINFO")
    return True

class MyClient(botpy.Client):
    async def on_group_at_message_create(self, message: Message):

        # 注册指令handler
        handlers = [
            start,
            out,
            end,
            bgiveup,
            lgiveup,
            Rate50,
            Rate66,
            Rate25,
            Rate33,
            Rate75,
            ai,
            pick,
            roleid,
            disc,
            defc,
            atkc,
            hpc,
            cdc,
            skill,
            roledata,
            help,
            timeinfo,
            remtime,
            timeset,

        ]
        for handler in handlers:
            if await handler(api=self.api, message=message):
                return

if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    # intents = botpy.Intents.none()
    # intents.public_messages=True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], secret=test_config["secret"])