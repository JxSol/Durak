@@ -1,2 +1,157 @@
import random as r


# from operator import itemgetter, attrgetter

class Game:
    languages = {'english': 0, 'russian': 1}
    lang_dict = {
        's': ('spades', 'пики'),
        'h': ('hearts', 'червы'),
        'c': ('clubs', 'трефы'),
        'd': ('diamonds', 'бубны'),
        '6': ('6', '6'),
        '7': ('7', '7'),
        '8': ('8', '8'),
        '9': ('9', '9'),
        '10': ('10', '10'),
        'j': ('jack', 'валет'),
        'q': ('queen', 'дама'),
        'k': ('king', 'король'),
        'a': ('ace', 'туз'),
        'mm_1': ('Starting new game...', 'Начинается новая игра...'),
        'mm_2': ('The trump card is', 'Козырь -'),
        'snop_1': ('Type number of players from 2 to 6.', 'Введите количество игроков от 2 до 6.'),
        'snop_2': ('Type number from 2 to 6.', 'Введите число от 2 до 6.'),
        'error': ('Input Error.', 'Ошибка ввода.')
    }

    def __init__(self):
        self.lang = Game.languages[self.choose_language()]
        print()
        self.number_of_players = self.set_number_of_players()
        print()
        print(f"{Game.lang_dict['mm_1'][self.lang]}")
        self.deck = Deck('durak')
        self.player_1 = Player(self.deck)
        self.player_2 = Player(self.deck)
        self.discard_pile = []
        self.table = []
        self.trump = self.deck.pop(0)
        print('— * —   ' * 10)
        print(f"{Game.lang_dict['mm_2'][self.lang]}", self.trump)
        print('— * —   ' * 10)
        self.attacker = self.player_1
        while self.attacker.hand:
            self.play_round(self.attacker)

    def play_round(self, attacker):
        print(f'{attacker}, Ваш ход.')
        self.table.extend([[card, None] for card in attacker.turn()])
        print(*self.table, sep=' | ')



    def choose_language(self):
        print()
        print('Choose the language. | Выберите язык.')
        print('Type "En" for English. | Введите "Рус" для русского.')
        language = input().lower().strip(' .,')
        if language in {'en', 'eng', 'english', 'англ', 'английский'}:
            return 'english'
        elif language in {'ru', 'rus', 'russian', 'ру', 'рус', 'русский'}:
            return 'russian'
        else:
            print('Input Error. | Ошибка ввода.')
            return self.choose_language()

    def set_number_of_players(self):
        print()
        print(f"{Game.lang_dict['snop_1'][self.lang]}")
        nop = input()
        try:
            if 2 <= int(nop) <= 6:
                return nop
            else:
                print(f"{Game.lang_dict['snop_2'][self.lang]}")
                return self.set_number_of_players()
        except NameError:
            print(f"{Game.lang_dict['error'][self.lang]}")
            return self.set_number_of_players()

class Player:
    def __init__(self, deck):
        self.hand = [deck.pop() for _ in range(6)]

    def turn(self):  # Добавить проверку для добавления второй карты
        print()
        print(self.hand)
        print()
        to_put = []
        card = input()
        while card != 'x' and len(to_put) == 0:
            if card == 'x':
                pass
            else:
                to_put.append(self.hand[int(card) - 1])
            card = input()
        for card in to_put:
            self.hand.remove(card)
        return to_put

    # def sort(self, trump_suit):
    #     trump_cards = []
    #     for card in self.hand:
    #         if card.suit == trump_suit:
    #             trump_cards.append(card)
    #     for card in trump_cards:
    #         self.hand.remove(card)
    #     self.hand.sort()
    #     self.hand.extend(sorted(trump_cards))


class Deck:
    suit_list = ('s', 'h', 'c', 'd')
    value_list = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k', 'a')

    def __init__(self, game=None):
        games = {'durak': self.durak}
        if game is None:
            self.cards = []
        else:
            games[game]()

    def __repr__(self):
        return str(self.cards)

    def __iter__(self):
        return iter(self.cards)

    def durak(self):
        self.cards = [Card(s, v) for s in Deck.suit_list for v in Deck.value_list[4:]]
        self.shuffle()

    def shuffle(self):
        r.shuffle(self.cards)

    def pop(self, i=-1):
        return self.cards.pop(i)

    # def sort(self):
    #     self.deck.sort(key=lambda x: Deck.suit_list.index(x))


class Card:
    pass
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return Game.lang_dict[self.value][1].capitalize() + ' ' + Game.lang_dict[self.suit][1].capitalize()


a = Deck('durak')
print(a)
# a.sort()
# print(a)
Game()