import random
import sys
import time


class Card:
    def __init__(self, card_tpye, card_text, card_value):
        self.card_tpye = card_tpye
        self.card_text = card_text
        self.card_value = card_value


class Role:
    def __init__(self):
        self.cards = []

    # 向控制台打印手中所有的牌
    def show_card(self):
        for card in self.cards:
            print(card.card_tpye, card.card_text, sep='', end='')
        print()

    def get_value(self, min_or_max):
        sum2 = 0
        # 表示牌面中A的数量
        A = 0
        for card in self.cards:
            # 累计相加所有点数
            sum2 += card.card_value
            # 累加A的数量
            if card.card_text == 'A':
                A += 1

        if min_or_max == "max":
            # 通过循环减少A的数量，选择一个小于等于21的最大值
            for i in range(A):
                value = sum2 - i * 10
                if value <= 21:
                    return value
        return sum2 - A * 10

    def burst(self):
        # 判断是否爆牌，只需要判断最小值是否大于21点即可
        return self.get_value("min") > 21


class CardManager:
    def __init__(self):
        """初始化方法"""
        # 用来保存一整副52张扑克牌
        self.cards = []
        # 定义所有牌的花色类型
        all_card_type = "♥♠♣♦"
        all_card_text = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
        all_card_value = [11, 10, 10, 10, 10, 9, 8, 7, 6, 5, 4, 3, 2]

        # 对牌面类型、牌面值、牌面文本嵌套循环
        for card_type in all_card_type:
            for index, card_text in enumerate(all_card_text):
                card = Card(card_type, card_text, all_card_value[index])
                self.cards.append(card)

        # 洗牌
        random.shuffle(self.cards)

    # 发牌
    def send_card(self, role, num=1):
        for i in range(num):
            card = self.cards.pop()
            role.cards.append(card)


# 创建扑克牌管理器类
cards = CardManager()
# 创建电脑角色
computer = Role()
# 创建玩家角色
player = Role()

# 初始时，给庄家发1张牌，给玩家发两张牌
cards.send_card(computer)
cards.send_card(player, num=2)

# 显示庄家与玩家手中的牌
computer.show_card()
player.show_card()

# 询问玩家是否要牌，如果玩家要牌，则继续发牌，否则停牌
while (True):
    choice = input("是否在要一张牌？【y/n】")
    if choice == 'y':
        cards.send_card(player)
        # 发牌后显示庄家与玩家手中的牌
        computer.show_card()
        player.show_card()
        # 判断玩家是否爆牌
        if player.burst():
            print("玩家爆牌，您输了")
            sys.exit()
    else:
        break

# 玩家停牌之后庄家发牌，庄家在小于17之前必须要牌，在17~21之间停牌，大于21点爆牌
while (True):
    print("庄家发牌中……")
    # 因为庄家不需要询问是否发牌，所以建立时间间隔
    time.sleep(1)
    # 向庄家发牌
    cards.send_card(computer)
    # 显示庄家与玩家的牌
    computer.show_card()
    player.show_card()
    # 判断庄家是否爆牌
    if computer.burst():
        print("庄家爆牌，您赢了")
        sys.exit()
    # 如果没有爆牌，则判断庄家的牌面值
    elif computer.get_value("max") >= 17:
        break

# 如果庄家和玩家都没有爆牌则比较点数大小
player_value = player.get_value("max")
computer_value = computer.get_value("max")

# 比较大小，多者胜出
if player_value > computer_value:
    print("您赢了")
elif player_value == computer_value:
    print("和棋")
else:
    print('您输了')
