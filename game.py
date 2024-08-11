import math
import random

import mysql.connector

# 确定玩家数量，赋初值


db = mysql.connector.connect(
    host="localhost",  # MySQL服务器地址
    user="root",  # 用户名
    password="yarizm75",  # 密码
    database="euxpvp"  # 数据库名称
)

# 创建游标对象，用于执行SQL查询
cursor = db.cursor()

x_values = []
isWin = []
isdiff = []
isgive = []
totalturn = []
giveturn = []
initial_probability_X = []
play_num = 0

# 后置放弃
def latergiveup(id):
    res = []
    query = "SELECT iswin FROM euxrate WHERE id = %s"
    value = (id,)
    cursor.execute(query,value)
    result = cursor.fetchall()
    for row in result:
        havewin = row[0]
        havewin = int(havewin)
        if(havewin == 1):
            query1 = "UPDATE euxrate SET iswin = %s,x_value = %s,isdiff = %s,winrate = %s WHERE id = %s"
            value1 = (0,0,0,0.75,id)
            cursor.execute(query1,value1)
            db.commit()
            print(f"玩家{id}已经在判定结束后放弃,该名玩家下次获得行动机会的概率为0.8")
            res = [f"玩家{id}已经在判定结束后放弃,该名玩家下次获得行动机会的概率为0.8"]
        else:
            print(f"玩家{id}没有行动机会，不能放弃回合！")
            res = [f"玩家{id}没有行动机会，不能放弃回合！"]
    return res
# 前置放弃
def beforegiveup(id):
    #将数据表中的isgive变更为1
    turn = 0
    query = "UPDATE euxrate SET isgive = %s WHERE id = %s"
    value = (1,id)
    cursor.execute(query,value)
    db.commit()

    query1 = "SELECT giveturn FROM euxrate WHERE id = %s"
    value1 = (id,)
    cursor.execute(query1,value1)
    result = cursor.fetchall()
    for row in result:
        turn = row[0]
    turn += 1
    print(f"玩家{id}已经在判定开始前放弃")
    res = [f"玩家{id}已经在判定开始前放弃,当前已连续放弃{turn}个回合"]

    return res
# 游戏内概率判定
def rate50():
    return random.random() < 0.5
def rate66():
    return random.random() < 0.66
def rate33():
    return random.random() < 0.33
def rate75():
    return random.random() < 0.75
def rate25():
    return random.random() < 0.25

# 启动游戏
def startgame(params):
    #获取游戏人数
    play_num = int(params)
    #将游戏人数上传到表中
    query = "UPDATE playnum SET play_num = %s"
    values = (params,)
    cursor.execute(query,values)
    # 提交更改到数据库
    db.commit()
    x_values.clear()
    isWin.clear()
    isdiff.clear()
    isgive.clear()
    totalturn.clear()
    giveturn.clear()
    initial_probability_X.clear()


    return play_num
    # for i in range(play_num):
    #     query = "SELECT winrate,isdiff,iswin,x_value FROM euxrate Where id = %s"
    #     values = (i+1,)
    #     cursor.execute(query,values)
    #     results = cursor.fetchall()
    #     for row in results:
    #         initial_probability_X[i] = row[0]
    #         isdiff[i] = row[1]
    #         isWin[i] = row[2]
    #         x_values[i] = row[3]


    # for i in range(play_num):
    #     x_values.append(0)
    #     isWin.append(None)
    #     isdiff.append(0)
    #     initial_probability_X.append(0.5)
    # return str(play_num)
# 选择游戏角色
def pickrole(id,rid):
    query = "SELECT player,name FROM role WHERE id = %s"
    value = (rid,)
    cursor.execute(query,value)
    result = cursor.fetchall()
    for row in result:
        ispick = row[0]
        rolename = row[1]
        if(ispick):
            res = f"角色：{rolename}已被其他玩家使用！请重新选择"
            return res
        else:
            query1 = "UPDATE role SET player = %s WHERE id = %s"
            value1 = (id,rid)
            cursor.execute(query1, value1)
            db.commit()
            res = f"玩家{id},您已成功选择角色：{rolename}"
            return res
# 获取所有角色的信息
def roleinfo():
    res = []
    query1 = "SELECT id,name,artinfo FROM roleora ORDER BY id ASC"
    cursor.execute(query1)
    result = cursor.fetchall()
    res = result
    print(res)
    return res
# 生命值变动
def hp_change(id,value,type):
    res = []
    type = int(type)
    value = int(value)
    if(type == 0):
        query1 = "SELECT nowhp FROM role WHERE player = %s"
        value1 = (id,)
        cursor.execute(query1,value1)
        result = cursor.fetchall()
        for row in result:
            nowhp = int(row[0])
            nowhp += value
            query2 = "UPDATE role SET nowhp = %s WHERE player = %s"
            value2 = (nowhp,id)
            cursor.execute(query2,value2)
            db.commit()
            res = f"玩家{id}的当前HP已变更为：{nowhp}"
    elif(type == 1):
        query1 = "SELECT maxhp FROM role WHERE player = %s"
        value1 = (id,)
        cursor.execute(query1, value1)
        result = cursor.fetchall()
        for row in result:
            maxhp = int(row[0])
            maxhp += value
            query2 = "UPDATE role SET maxhp = %s WHERE player = %s"
            value2 = (maxhp, id)
            cursor.execute(query2, value2)
            db.commit()
            res = f"玩家{id}的最大HP已变更为：{maxhp}"
    return res
# 使用技能
def skill_use(id,value):
    res = []
    query1 = f"SELECT art{value},id FROM role WHERE player = %s"
    value1 = (id,)
    cursor.execute(query1, value1)
    result = cursor.fetchall()
    for row in result:
        nowcd = row[0]
        roid = row[1]
        if(nowcd == 0):
            query1 = f"SELECT art{value} FROM roleora WHERE id = %s"
            value1 = (roid,)
            cursor.execute(query1, value1)
            result = cursor.fetchall()
            for row1 in result:
                cdnum = row1[0]
                print(cdnum)
                nowcd += cdnum
                query2 = f"UPDATE role SET art{value} = %s WHERE player = %s"
                value2 = (nowcd,id)
                cursor.execute(query2,value2)
                db.commit()
                res = f"玩家{id}的技能{value}已使用，当前cd为{nowcd}"
        else:
            res = f"玩家{id}的技能{value}还在cd中!，当前cd为{nowcd}"
    return res
# cd变动
def cd_change(id,value,num):
    res = []
    num = int(num)
    query1 = f"SELECT art{value} FROM role WHERE player = %s"
    value1 = (id,)
    cursor.execute(query1, value1)
    result = cursor.fetchall()
    for row in result:
        nowcd = int(row[0])
        if (nowcd == 0):
            res = f"玩家{id}的技能{value}尚未处在cd中，无法进行更改！"
        else:
            nowcd += num
            query2 = f"UPDATE role SET art{value} = %s WHERE player = %s"
            value2 = (nowcd, id)
            cursor.execute(query2, value2)
            db.commit()
            res = f"玩家{id}的技能{value}的cd已更改，当前cd为{nowcd}"
    return res
# 回合结束自然cd变动以及输出数据
def turnend(sign):
    res = []
    tres = []
    play_num = playnum()
    for i in range(play_num):
        art = []
        tart = []
        query1 = "SELECT art1,art2,art3,art4,art5,art6,art7,art8,art9,art10 FROM role WHERE player = %s"
        value1 = (i+1,)
        cursor.execute(query1,value1)
        result1 = cursor.fetchall()
        for row in result1:
            for j in range(10):
                art.append(row[j])
                if(art[j] and art[j] != 0):
                    if(sign == 1):
                        art[j] -= 1
                    tart.append(j+1)
                    query2 = f"UPDATE role SET art{j+1} = %s WHERE player = %s"
                    value2 = (art[j],i+1)
                    cursor.execute(query2,value2)
                    db.commit()
        la = len(tart)
        query3 = "SELECT maxhp,nowhp,turndef,totaldef,atk,distance FROM role WHERE player = %s"
        value3 = (i+1,)
        cursor.execute(query3,value3)
        result3 = cursor.fetchall()
        result4 = []
        for t in range(la):
            query4 = f"SELECT art{tart[t]} FROM role WHERE player = %s"
            value4 = (i+1,)
            cursor.execute(query4,value4)
            result5 = cursor.fetchall()
            for row5 in result5:
                rsq = f"玩家{i+1}的技能{tart[t]}当前的cd为：{row5[0]} \n"
                result4.append(rsq)
        res.append(result3)

        for x in res[i]:
            qres = f"玩家{i+1}最大hp为：{x[0]}，当前hp为：{x[1]}，当前护甲为：{x[2]}，总护甲为：{x[3]}，当前ATK为：{x[4]}，当前攻击距离为：{x[5]}。 \n\n"
            le = len(result4)
            for q in range(le):
                qres = qres+result4[q]

            tres.append(qres)
    return tres
# 计时功能
def timerem(id,word,value):
    turntime = turnnum()
    value = int(value)
    rem = []
    query1 = "SELECT rem_1,rem_2,rem_3,rem_4 FROM remtime WHERE player = %s"
    value1 = (id,)
    cursor.execute(query1, value1)
    result1 = cursor.fetchall()
    for row in result1:
        for j in range(4):
            rem.append(row[j])
            if (rem[j] == None):
                query2 = f"UPDATE remtime SET rem_{j + 1} = %s,rem_{j + 1}_word = %s WHERE player = %s"
                value2 = (value,word,id)
                cursor.execute(query2, value2)
                db.commit()
                break
    res = f"玩家{id}已经添加了名为：{word}；持续时间为：{value}回合的计时！该计时将在第{turntime+value}回合结束！"
    return res

# 计时自然减少
def remsubauto():
    play_num = playnum()
    for i in range(play_num):
        rem = []
        query1 = "SELECT rem_1,rem_2,rem_3,rem_4 FROM remtime WHERE player = %s"
        value1 = (i + 1,)
        cursor.execute(query1, value1)
        result1 = cursor.fetchall()
        for row in result1:
            for j in range(4):
                rem.append(row[j])
                if (rem[j] and rem[j] != 0):
                    rem[j] -= 1
                    query2 = f"UPDATE remtime SET rem_{j + 1} = %s WHERE player = %s"
                    value2 = (rem[j], i + 1)
                    cursor.execute(query2, value2)
                    db.commit()
                elif rem[j] == 0:
                    query3 = f"UPDATE remtime SET rem_{j + 1} = %s,rem_{j+1}_word = %s WHERE player = %s"
                    value3 = (None,None,i + 1)
                    cursor.execute(query3, value3)
                    db.commit()
    return True

# 计时手动减少
def remsubhand(id,word,value):
    value = int(value)
    query1 = "SELECT rem_1,rem_2,rem_3,rem_4,rem_1_word,rem_2_word,rem_3_word,rem_4_word FROM remtime WHERE player = %s"
    value1 = (id,)
    cursor.execute(query1, value1)
    result1 = cursor.fetchall()
    rem = []
    wo = []
    for row in result1:
        for j in range(4):
            rem.append(row[j])
            wo.append(row[j+4])
            if(rem[j] and rem[j] != 0 and wo[j] == word):
                print(wo[j],word)
                rem[j] += value
                query2 = f"UPDATE remtime SET rem_{j + 1} = %s WHERE player = %s"
                value2 = (rem[j],id)
                cursor.execute(query2, value2)
                db.commit()
                res = f"玩家{id}的名为:{word}的计时已经更改！当前为：{rem[j]}!"
                return res

# 重置计时
def remreset():
    query2 = f"UPDATE remtime SET rem_1 = %s,rem_2 = %s,rem_3 = %s,rem_4 = %s,rem_1_word = %s,rem_2_word = %s,rem_3_word = %s,rem_4_word = %s"
    value2 = (None,None,None,None,None,None,None,None)
    cursor.execute(query2, value2)
    db.commit()
    return True

# 查看计时信息
def timeinfo():
    play_num = playnum()
    res = []

    for i in range(play_num):
        rem = []
        wo = []
        cam = []
        query1 = "SELECT rem_1,rem_2,rem_3,rem_4,rem_1_word,rem_2_word,rem_3_word,rem_4_word FROM remtime WHERE player = %s"
        value1 = (i+1,)
        cursor.execute(query1, value1)
        result1 = cursor.fetchall()
        for row in result1:
            for j in range(4):
                rem.append(row[j])
                wo.append(row[j+4])
                if(rem[j] and rem[j] != 0):
                    cam.append(f"计时:{wo[j]},当前还有：{rem[j]}回合! \n")
        req = f"玩家{i+1}的计时一览: \n"
        for j in range(len(cam)):
            req += cam[j]
        res.append(req)

    return res



# 护甲变动
def def_change(id,value):
    res = []
    value = int(value)
    query1 = "SELECT turndef FROM role WHERE player = %s"
    value1 = (id,)
    cursor.execute(query1, value1)
    result = cursor.fetchall()
    for row in result:
        turndef = int(row[0])
        turndef += value
        query2 = "UPDATE role SET turndef = %s WHERE player = %s"
        value2 = (turndef,id)
        cursor.execute(query2, value2)
        db.commit()
        res = f"玩家{id}的当回合护甲已变更为：{turndef}"
    return res
# ATK变动
def atk_change(id,value):
    res = []
    value = int(value)
    query1 = "SELECT atk FROM role WHERE player = %s"
    value1 = (id,)
    cursor.execute(query1, value1)
    result = cursor.fetchall()
    for row in result:
        atk = int(row[0])
        atk += value
        query2 = "UPDATE role SET atk = %s WHERE player = %s"
        value2 = (atk,id)
        cursor.execute(query2, value2)
        db.commit()
        res = f"玩家{id}的ATK已变更为：{atk}"
    return res
# ATK距离变动
def distance_change(id,value):
    res = []
    value = int(value)
    query1 = "SELECT distance FROM role WHERE player = %s"
    value1 = (id,)
    cursor.execute(query1, value1)
    result = cursor.fetchall()
    for row in result:
        distance = int(row[0])
        distance += value
        query2 = "UPDATE role SET distance = %s WHERE player = %s"
        value2 = (distance, id)
        cursor.execute(query2, value2)
        db.commit()
        res = f"玩家{id}的ATK距离已变更为：{distance}"
    return res

# 重置回合护甲
def resetdef():
    play_num = playnum()
    for i in range(play_num):
        query1 = "SELECT id,turndef,totaldef FROM role WHERE player = %s"
        value1 = (i+1,)
        cursor.execute(query1, value1)
        result1 = cursor.fetchall()
        for row1 in result1:
            id = row1[0]
            nowdef = row1[1]
            totaldef = row1[2]
            query2 = "SELECT turndef FROM roleora WHERE id = %s"
            value2 = (id,)
            cursor.execute(query2,value2)
            result2 = cursor.fetchall()
            for row2 in result2:
                turndef = row2[0]
                if(nowdef < turndef):
                    if(totaldef-turndef >= 0):
                        dif = turndef - nowdef
                        nowdef = turndef
                        totaldef -= dif
                    else:
                        nowdef = turndef-totaldef
                        totaldef = 0
                    query3 = "UPDATE role SET turndef = %s,totaldef = %s WHERE player = %s"
                    value3 = (nowdef,totaldef,i+1)
                    cursor.execute(query3,value3)
                    db.commit()
    return True
# 计算当前回合数
def turnnum():
    query = "SELECT totalturn FROM euxrate WHERE id = %s"
    value = (1,)
    cursor.execute(query,value)
    result = cursor.fetchall()
    for row in result:
        turn = row[0]
        return turn
# 结束游戏
def endgame():
    #将数据表中的数据重置为初值
    query = "SELECT play_num FROM playnum"
    cursor.execute(query)
    result = cursor.fetchall()
    for row in result:
        play_num = row[0]
        for i in range(play_num):
            query1 = ("UPDATE euxrate SET winrate = %s,isdiff = %s,iswin = %s,x_value = %s,isgive = %s,totalturn = %s,"
                      "giveturn = %s WHERE id = %s")
            values1 = (0.5,0,None,0,0,0,0,i+1)
            cursor.execute(query1, values1)
            db.commit()
            query2 = "SELECT id FROM role WHERE player = %s"
            values2 = (i+1,)
            cursor.execute(query2,values2)
            result2 = cursor.fetchall()
            for row2 in result2:
                rid = row2[0]
                query3 = "SELECT id,maxhp,nowhp,turndef,totaldef,atk,distance FROM roleora WHERE id = %s"
                values3 = (rid,)
                cursor.execute(query3, values3)
                result3 = cursor.fetchall()
                for row3 in result3:
                    id = row3[0]
                    maxhp = row3[1]
                    nowhp = row3[2]
                    turndef = row3[3]
                    totaldef = row3[4]
                    atk = row3[5]
                    distance = row3[6]
                    query4 = ("UPDATE role SET maxhp = %s,nowhp = %s,turndef = %s,totaldef = %s,atk = %s,distance = %s,player = %s,"
                              "art1 = %s,art2 = %s,art3 = %s,art4 = %s,art5 = %s,art6 = %s,art7 = %s WHERE id = %s")
                    values4 = (maxhp,nowhp,turndef,totaldef,atk,distance,None,0,0,0,0,0,0,0,id)
                    cursor.execute(query4,values4)
                    db.commit()
    return True
# 计算玩家总数
def playnum():
    # 从数据表中获取玩家人数
    query = "SELECT play_num FROM playnum"
    cursor.execute(query)
    result = cursor.fetchall()
    for row in result:
        play_num = row[0]
        return play_num
# 输出一次结果
def outprint():
    #返回一个集合
    res = []
    #从数据表中获取玩家人数
    query = "SELECT play_num FROM playnum"
    cursor.execute(query)
    result = cursor.fetchall()
    for row in result:
        play_num = row[0]
        print(play_num)
        for i in range(play_num):
            # 从数据表中获取玩家的各项数据
            query = "SELECT winrate,isdiff,iswin,x_value,isgive,totalturn,giveturn FROM euxrate Where id = %s"
            values = (i + 1,)
            cursor.execute(query, values)
            results = cursor.fetchall()
            print(results)
            for row in results:
                initial_probability_X.append(row[0])
                # isdiff[i] = row[1]
                isdiff.append(row[1])
                isWin.append(row[2])
                x_values.append(row[3])
                isgive.append(row[4])
                totalturn.append(row[5])
                giveturn.append(row[6])
                # isWin[i] = row[2]
                # x_values[i] = row[3]
                print(initial_probability_X[i],isdiff[i],isWin[i],x_values[i],isgive[i],totalturn[i],giveturn[i])

            if(isgive[i] == 0):
                Haveturn = event_occurs(initial_probability_X[i])
                if (Haveturn):
                    if (isWin[i] != None and isWin[i] != Haveturn):
                        isdiff[i] = 1
                    else:
                        isdiff[i] = 0
                    isWin[i] = Haveturn
                    calculate_probability_Y(i)
                    totalturn[i] += 1
                    print(
                        f"玩家{i + 1}有行动机会,下一次玩家{i + 1}的获胜概率为{initial_probability_X[i]},{isdiff},{x_values},{isWin}")
                    str = f"玩家{i + 1}有行动机会,下一次玩家{i + 1}的获胜概率为{initial_probability_X[i]}"
                    res.append(str)

                else:
                    if (isWin[i] != None and isWin[i] != Haveturn):
                        isdiff[i] = 1
                    else:
                        isdiff[i] = 0
                    isWin[i] = Haveturn
                    calculate_probability_Y(i)
                    totalturn[i] += 1
                    print(
                        f"玩家{i + 1}没有行动机会,下一次玩家{i + 1}的获胜概率为{initial_probability_X[i]},{isdiff},{x_values},{isWin}")
                    str = f"玩家{i + 1}没有行动机会,下一次玩家{i + 1}的获胜概率为{initial_probability_X[i]}"
                    res.append(str)
                giveturn[i] = 0
            else:
                isdiff[i] = 0
                isWin[i] = 0
                x_values[i] = 0
                totalturn[i] += 1
                giveturn[i] += 1
                calculate_score(giveturn[i],totalturn[i],i)
                print(f"玩家{i+1}已经放弃了回合,下一次玩家{i+1}的获胜概率为{initial_probability_X[i]}")
                str = f"玩家{i+1}已经放弃了回合,下一次玩家{i+1}的获胜概率为{initial_probability_X[i]}"
                res.append(str)
                isgive[i] = 0

            # 将更改之后的数据存放回数据表中
            query1 = "UPDATE euxrate SET winrate = %s,isdiff = %s,iswin = %s,x_value = %s,isgive = %s,totalturn = %s,giveturn = %s WHERE id = %s"
            values1 = (initial_probability_X[i], isdiff[i], isWin[i], x_values[i],isgive[i],totalturn[i],giveturn[i],i + 1)
            cursor.execute(query1, values1)
            db.commit()

    #返回列表
    x_values.clear()
    isWin.clear()
    isdiff.clear()
    isgive.clear()
    totalturn.clear()
    giveturn.clear()
    initial_probability_X.clear()
    return res
# 计算当前获胜概率
def calculate_probability_Y(i):
        if(isWin[i] == True):
            if (isdiff[i] == 0):
                x_values[i] += 1
                initial_probability_X[i] = 0.5
            else:
                x_values[i] = 0
                initial_probability_X[i] = 0.5
            # initial_probability_X[i] = initial_probability_X[i] - 0.5 * (1 - math.exp(-0.1 * abs(x_values[i])))
        else:
            if (isdiff[i] == 0):
                x_values[i] += 1
                initial_probability_X[i] = 0.5
            else:
                x_values[i] = 0
                initial_probability_X[i] = 0.5
            initial_probability_X[i] = initial_probability_X[i] + 0.5 * (1 - math.exp(-0.1 * abs(x_values[i])))
# 概率公式
def calculate_score(x,y,i):
    # 定义公式
    formula = (0.5 + 0.25 * (x ** 0.1) - 0.25 ** (y ** 0.2) +
               0.05 * (y ** 0.1) * ((x - 1) ** 2.4))
    # 返回计算结果
    initial_probability_X[i] = formula
# 判定是否获胜
def event_occurs(probability_Y):
    return random.random() < probability_Y