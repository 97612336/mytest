class Card:
    def __init__(self, card_tpye, card_text, card_value):
        """初始化方法
        Parameters
        ---------
        card_type:str
            牌的类型：（红桃，黑桃，梅花，方片）
        card_text:str
            牌面显示的文本（A,K,Q,J）
        card_value:int
            牌面的真实值（例如A为1点或11点，K为10点）
        """
        self.card_tpye = card_tpye  # 牌的类型
        self.card_text = card_text  # 牌的文本
        self.card_value = card_value  # 牌的真实值


def get_value(cards, min_or_max):
    sum2 = 0
    # 表示牌面中A的数量
    A = 0
    for card in cards:
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
