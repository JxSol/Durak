import random as r


# from operator import itemgetter, attrgetter

class DurakTheGame:
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
        'ng_1': ('Starting new game...', 'Начинается новая игра...'),
        'ng_2': ('The trump card is', 'Козырь -'),
        'sp_1': ('Type number of players from 2 to 6.', 'Введите количество игроков от 2 до 6.'),
        'sp_2': ('Type number from 2 to 6.', 'Введите число от 2 до 6.'),
        'pr_1': ('Would you like to throw in some cards 1/0?', 'Подкинете ещё карт 1/0?'),
        'a_1': ('This card cannot be used at the moment.', 'В данный момент эту карту нельзя использовать.'),
        'a_2': ('Would you like to choose another card 1/0?', 'Выбрать ещё одну карту 1/0?'),
        'd_1': ('Will you try to defend 1/0?', 'Вы будете отбиваться 1/0?'),
        'd_2': ('Your opponent abandoned the defense, would you like to throw in some cards 1/0?',
                'Соперник берёт; подкинете ещё карт?'),
        'd_3': ('This card cannot beat the card from the table.',
                'Эта карта не сможет отбить выбранную карту со стола.'),
        'eg_1': ('became a durak!', 'остался в дураках!'),
        'eg_2': ('Draw!', 'Ничья!'),
        'error': ('Input Error.', 'Ошибка ввода.')
    }
    full_hand = 6

    def __init__(self):
        self.table = {'pending': [], 'beaten': []}
        self.deck = Deck()
        self.trump = None
        self.attacker = None
        self.defender = None
        self.durak = None
        self.lang = DurakTheGame.languages[self.choose_language()]
        print()
        self.players = self.set_players()
        print()
        self.new_game()
        self.end_game()

    def new_game(self):
        print(f"{DurakTheGame.lang_dict['ng_1'][self.lang]}")
        self.table = {'pending': [], 'beaten': []}
        self.deck = Deck('36')
        self.deck.shuffle()
        for player in self.players:
            player.get_to_full_hand(self.deck, DurakTheGame.full_hand)
            for s in player.count_suits().values():
                if s >= 5:
                    self.del_players_cards()
                    self.new_game()
                    return
        self.trump = self.deck.cards[0]
        print(f"{DurakTheGame.lang_dict['ng_2'][self.lang]}", self.trump)
        self.deck.set_trump(self.trump.suit)
        min_trump = Card(self.trump.suit, 'A')
        # Choose player for first move
        for player in self.players:
            for c in player.hand:
                if c.trump and c <= min_trump:
                    min_trump = c
                    self.attacker = player
                    self.defender = self.players[(self.players.index(player) + 1) % len(self.players)]
        if self.attacker:
            while self.durak is None:
                self.play_round()
        else:
            self.new_game()

    def play_round(self):
        print(f'{self.attacker}, Ваш ход.')
        self.table['pending'].extend(self.attacker.attack(self.table, len(self.defender.hand)))
        self.table = self.defender.defend(self.table, self.attacker)
        if len(self.defender.hand):
            print(f"{DurakTheGame.lang_dict['pr_1'][self.lang]}")
            if input():
                self.play_round()
                return
        # Поочерёдный добор карт игроками
        self.attacker.get_to_full_hand(self.deck, DurakTheGame.full_hand)
        self.players.remove(self.defender)
        for player in self.players:
            player.get_to_full_hand(self.deck, DurakTheGame.full_hand)
        self.players.append(self.defender)
        self.defender.get_to_full_hand(self.deck, DurakTheGame.full_hand)
        # Фильтр: у кого нет карт - выходит из игры
        self.players = [player for player in self.players if player.hand]
        # Проверка: остались ли игроки для продолжения игры?
        if len(self.players) < 2:
            self.durak += self.players
            return
        # Выбор следующей пары соперников
        if any([x for x in self.table.values()]):
            self.table = {'pending': [], 'beaten': []}
            self.attacker = self.defender
        else:
            self.attacker = self.players[(self.players.index(self.defender) + 1) % len(self.players)]
        self.defender = self.players[(self.players.index(self.attacker) + 1) % len(self.players)]

    def end_game(self):
        if self.durak:
            print(f"{self.durak[0]}, {DurakTheGame.lang_dict['eg_1'][self.lang]}")
        else:
            print(f"{DurakTheGame.lang_dict['eg_2'][self.lang]}")

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

    def set_players(self):
        print()
        print(f"{DurakTheGame.lang_dict['sp_1'][self.lang]}")
        try:
            nop = int(input())
            if 2 <= nop <= 6:
                pass
            else:
                print(f"{DurakTheGame.lang_dict['sp_2'][self.lang]}")
                return self.set_players()
        except NameError:
            print(f"{DurakTheGame.lang_dict['error'][self.lang]}")
            return self.set_players()
        return [Player('player_' + str(i + 1)) for i in range(nop)]

    def del_players_cards(self):
        for player in self.players:
            player.hand = []


class Player:
    def __init__(self, name, deck=None, n=0):
        self.name = name
        if deck is None:
            self.hand = []
        else:
            self.hand = [deck.pop() for _ in range(n)]

    def __repr__(self):
        return self.name

    def sort_cards(self):
        self.hand.sort(key=lambda c: (c.trump, Deck.suit_list.index(c.suit), Deck.rank_list.index(c.rank)))

    def count_suits(self):
        suits = {'s': 0, 'h': 0, 'c': 0, 'd': 0}
        for c in self.hand:
            suits[c.suit] += 1
        return suits

    def get_to_full_hand(self, deck, n):
        while len(self.hand) < n and len(deck):
            self.hand.append(deck.pop())

    def choose_card_from_hand(self):
        self.sort_cards()
        print(self.hand)
        return self.hand.pop(int(input()) - 1)

    def attack(self, table, len_enemy_hand):
        table_ranks = [c.rank for lst in table.values() for c in lst]
        chosen = []
        card_check = False
        if chosen == table_ranks == []:
            chosen.append(self.choose_card_from_hand())
        else:
            while card_check is False:
                card = self.choose_card_from_hand()
                if card.rank in [c.rank for c in chosen] or card.rank in table_ranks:
                    card_check = True
                    chosen.append(card)
                else:
                    print(f"{DurakTheGame.lang_dict['a_1'][1]}")
                    self.hand.append(card)
        if len(chosen) + len(table['pending']) < len_enemy_hand:
            print(f"{DurakTheGame.lang_dict['a_2'][1]}")
            if int(input()):
                chosen += self.attack(table, len_enemy_hand)
        return chosen

    def defend(self, table, attacker):
        print(f"{DurakTheGame.lang_dict['d_1'][1]}")
        if input() == '0':
            print(f"{DurakTheGame.lang_dict['d_2'][1]}")
            if input():
                table['pending'].extend(attacker.attack(table, len(self.hand)))
            self.hand.extend(table['pending'] + table['beaten'])  # В отбитых нужно раскрыть пары
            return {'pending': [], 'beaten': []}
        while table['pending']:
            print(table['pending'])
            pending_card = table['pending'].pop(int(input()) - 1)
            hand_card = self.choose_card_from_hand()
            if hand_card < pending_card:
                print(f"{DurakTheGame.lang_dict['d_3'][1]}")
                return self.defend(table, attacker)
            table['beaten'].append((pending_card, hand_card))
        return table


class Deck:
    suit_list = ('s', 'h', 'c', 'd')
    rank_list = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k', 'a')

    def __init__(self, volume=None):
        decks = {
            '54': [Card(s, v) for s in Deck.suit_list for v in Deck.rank_list].extend(
                [Card('black', 'joker'), Card('red', 'joker')]),
            '52': [Card(s, v) for s in Deck.suit_list for v in Deck.rank_list],
            '36': [Card(s, v) for s in Deck.suit_list for v in Deck.rank_list[4:]],
            '24': [Card(s, v) for s in Deck.suit_list for v in Deck.rank_list[7:]]
        }
        if volume is None:
            self.cards = []
        else:
            self.cards = decks[volume]

    def __repr__(self):
        return str(self.cards)

    def __iter__(self):
        return iter(self.cards)

    def __len__(self):
        return len(self.cards)

    def shuffle(self):
        r.shuffle(self.cards)

    def pop(self, i=-1):
        return self.cards.pop(i)

    def sort(self):
        self.cards.sort(key=lambda c: (c.trump, Deck.suit_list.index(c.suit), Deck.rank_list.index(c.rank)))

    def set_trump(self, trump_suit):
        for c in self.cards:
            if c.suit == trump_suit:
                c.trump = True


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.trump = False

    def __repr__(self):
        return DurakTheGame.lang_dict[self.rank][1].capitalize() + ' ' + DurakTheGame.lang_dict[self.suit][
            1].capitalize()

    def __lt__(self, other):
        if self.trump == other.trump:
            return self.rank < other.rank and other.suit == self.suit
        return not self.trump and other.trump

    def __le__(self, other):
        if self.trump == other.trump:
            return self.rank <= other.rank and other.suit == self.suit
        return not self.trump and other.trump

    def __eq__(self, other):
        return other.rank == self.rank and other.suit == self.suit

    def __ne__(self, other):
        return other.rank != self.rank or other.suit != self.suit

    def __gt__(self, other):
        if self.trump == other.trump:
            return self.rank > other.rank and other.suit == self.suit
        return self.trump and not other.trump

    def __ge__(self, other):
        if self.trump == other.trump:
            return self.rank >= other.rank and other.suit == self.suit
        return self.trump and not other.trump


DurakTheGame()
