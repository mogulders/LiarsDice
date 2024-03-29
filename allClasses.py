import random


class Dice:

    def __init__(self):
        self.rolled_number = 0

    def roll_one_dice(self):
        self.rolled_number = random.randint(1, 6)


"""do I need to make copy lists and swap them out, it is both etiquitte and probably the best way to do this"""
class Player:

    def __init__(self):
        self.quantity_wager = 0
        self.die_wager = 0
        self.player_hand = []

        # number of die in players hand this is for computer purposes
        self.number_of_die_inHand = 0
        # required minimum quantity wager this is for computer purposes
        self.minimum_quantity_wager = 0
        # percent of the unsure dice that must be applicable to wager this is for computer purposes
        self.percent_of_unsure_must_be_applicable = 0.000

    def fill_hand(self):
        while len(self.player_hand) < 4:
            dice = Dice()
            self.player_hand.append(dice)

    def roll_hand(self):
        for dice in self.player_hand:
            dice.roll_one_dice()

    def call_bullshit(self, game):
        dice_on_table_list = []

        print(f'{self.name} called bullshit')

        for player in game.players:
            for dice in player.player_hand:
                if dice.rolled_number == game.die_wager:
                    game.die_wager_counter += 1
                dice_on_table_list.append(dice.rolled_number)

        for player in game.active_players:
            for dice in player.player_hand:
                if dice.rolled_number == game.die_wager:
                    game.die_wager_counter += 1
                dice_on_table_list.append(dice.rolled_number)

        print('The dice on the table are:')
        print(*dice_on_table_list)

        if game.quantity_wager > game.die_wager_counter:
            bullshitter = game.active_players[0]
            bullshitter.player_hand.pop(0)
            print(f'{bullshitter.name} loses a dice')
        elif game.quantity_wager <= game.die_wager_counter:
            wageree = game.active_players[1]
            wageree.player_hand.pop(0)
            print(f'{wageree.name} loses a dice')

        game.reset_players_lists()
        game.clear_wagers()
        print('')
        # for player in game.players:
        #     player.clear_player_wagers()


    def clear_player_wagers(self):

        self.die_wager = 0
        self.quantity_wager = 0

class UserPlayer(Player):

    def __init__(self, name):
        self.name = name
        super().__init__()

    def display_dice(self):
        hand = []
        print(f'{self.name} dice: ')
        for dice in self.player_hand:
            hand.append(dice.rolled_number)
        print(*hand)

    def wager(self, game):

        if game.quantity_wager == 0 and game.die_wager == 0:
            self.display_dice()

        ok_wager = False

        while ok_wager == False:

            quantity_wager = int(input("You will enter the die next. What quantity would you like to wager?"))
            die_wager = int(input("What die would you like to wager?"))

            if quantity_wager > game.quantity_wager:
                game.quantity_wager = quantity_wager
                game.die_wager = die_wager
                self.quantity_wager = quantity_wager
                self.die_wager = die_wager
                print(f'{self.name} quantity wager: {game.quantity_wager}')
                print(f'{self.name} die wagered: {game.die_wager}')
                ok_wager = True
            elif quantity_wager < game.quantity_wager:
                print('Quantity is not higher than previously wagered quantity. Try again')
            elif quantity_wager == game.quantity_wager:
                if die_wager > game.die_wager:
                    game.quantity_wager = quantity_wager
                    game.die_wager = die_wager
                    self.quantity_wager = quantity_wager
                    self.die_wager = die_wager
                    print(f'{self.name} quantity wager: {game.quantity_wager}')
                    print(f'{self.name} die wagered: {game.die_wager}')
                    ok_wager = True
                elif die_wager <= game.die_wager:
                    print('The die wager is not larger than previously wagered die. Try again')

        game.add_next_active_player()


    def wager_or_bullshit(self, game):
        self.display_dice()
        redo_answer = True
        while redo_answer:
            response = input("Would you like to Wager or call Bullshit? Enter w for wager Enter b for bullshit")
            if response.lower() == 'b':
                self.call_bullshit(game)
                redo_answer = False
            elif response.lower() == 'w':
                self.wager(game)
                redo_answer = False
            else:
                print("Invalid answer choose either w for wager or b for bullshit.")

    def clear_die_counter(self):
        # this is here so it can be called on all instances of player maybe I should put it in Parent class
        pass


class ComputerPlayer(Player):

    def __init__(self, name):

        # computer name
        self.name = name

        # creates a list of die lists, each die has a number of die, a weighted value, and the number
        self.die1 = [0, 0, 1]
        self.die2 = [0, 0, 2]
        self.die3 = [0, 0, 3]
        self.die4 = [0, 0, 4]
        self.die5 = [0, 0, 5]
        self.die6 = [0, 0, 6]


        # list of die lists
        self.die_list = [self.die1, self.die2, self.die3, self.die4, self.die5, self.die6]

        # threshold percentage for wager
        self.threshold_percent = 0.45

        # initializes everything from the parent class Player
        super().__init__()

    def count_dice(self):
        self.number_of_die_inHand = 0
        # self.die1 = [0, 0, 1]
        # self.die2 = [0, 0, 2]
        # self.die3 = [0, 0, 3]
        # self.die4 = [0, 0, 4]
        # self.die5 = [0, 0, 5]
        # self.die6 = [0, 0, 6]
        # counts the number of each dice in the hand
        # put in decimals to add value to a 6 (ie. wager on a six before a 1)
        for dice in self.player_hand:

            self.number_of_die_inHand += 1
            if dice.rolled_number == 1:
                self.die1[0] += 1
                self.die1[1] += 1.01
            elif dice.rolled_number == 2:
                self.die2[0] += 1
                self.die2[1] += 1.02
            elif dice.rolled_number == 3:
                self.die3[0] += 1
                self.die3[1] += 1.03
            elif dice.rolled_number == 4:
                self.die4[0] += 1
                self.die4[1] += 1.04
            elif dice.rolled_number == 5:
                self.die5[0] += 1
                self.die5[1] += 1.05
            elif dice.rolled_number == 6:
                self.die6[0] += 1
                self.die6[1] += 1.06

    def find_max(self):

        die_counter_list = []
        for die in self.die_list:
            die_counter_list.append(die[1])

        max_counter = max(die_counter_list)
        for die in self.die_list:
            if die[1] == max_counter:
                return die

    def calculate_the_minimum_wager_quantity(self, game):
        max_die = self.find_max()
        if game.die_wager == 0 and game.quantity_wager == 0:
            self.minimum_quantity_wager = game.quantity_wager + 1
        elif max_die[2] > game.die_wager:
            self.minimum_quantity_wager = game.quantity_wager
        elif max_die[2] <= game.die_wager:
            self.minimum_quantity_wager = game.quantity_wager + 1

    def calculate_odds_of_required_wager(self, game):
        # The die object that the computer has the most of
        max_die = self.find_max()
        # The total amount of dice on the table
        total_dice = game.total_dice_on_table
        # The number of dice that it posses applicable to the wager
        number_of_applicable_dice = max_die[0]
        # the number of dice it has in its hand
        number_of_possessed_dice = self.number_of_die_inHand
        # required quantity wager for wager
        minimum_quantity_wager = self.minimum_quantity_wager
        # Number of dice the computer is unsure about on the table
        unsure_dice = total_dice - number_of_possessed_dice
        # The min quanity - applicable dice
        cover_amount = minimum_quantity_wager - number_of_applicable_dice
        # percent of dice on the table required to be of applicable
        percent_of_unsure_must_be_applicable = cover_amount/unsure_dice
        self.percent_of_unsure_must_be_applicable = percent_of_unsure_must_be_applicable

    def clear_die_counters(self):
        for die in self.die_list:
            die[0] = 0
            die[1] = 0

    def wager(self, game):
        self.calculate_the_minimum_wager_quantity(game)
        self.calculate_odds_of_required_wager(game)
        # The die object that the computer will use as wager
        max_die = self.find_max()
        # required quantity wager for wager
        minimum_quantity_wager = self.minimum_quantity_wager

        # setting the game quantity wager to the cover amount
        game.quantity_wager = minimum_quantity_wager
        self.quantity_wager = minimum_quantity_wager
        print(f'{self.name} quantity wager: {minimum_quantity_wager}')

        # setting the game die wager to the number of the dice the comp poses the most of
        game.die_wager = max_die[2]
        self.die_wager = max_die[2]
        print(f'{self.name} die wager: {max_die[2]}')

        self.clear_die_counters()
        game.add_next_active_player()

    def decide(self, game):

        if self.percent_of_unsure_must_be_applicable >= self.threshold_percent:
            self.call_bullshit(game)
        elif self.percent_of_unsure_must_be_applicable < self.threshold_percent:
            self.wager(game)

    def wager_or_bullshit(self, game):

        self.count_dice()
        self.calculate_the_minimum_wager_quantity(game)
        self.calculate_odds_of_required_wager(game)
        self.decide(game)


class Game:

    def __init__(self):
        self.total_dice_on_table = 0
        self.quantity_wager = 0
        self.die_wager = 0
        self.die_wager_counter = 0
        self.players = []
        self.active_players = []

    def fill_players(self):
        player_names_list = ['Bugs Bunny', 'Daffy Duck', 'Marvin The Martian']
        while len(self.players) < 1:
            username = input('What is your name?')
            player = UserPlayer(username)
            self.players.append(player)
        while len(self.players) < 4:
            for player_name in player_names_list:
                player = ComputerPlayer(player_name)
                self.players.append(player)

    def fill_players_hands(self):
        for player in self.players:
            player.fill_hand()

    # done every round
    def all_players_roll(self):
        # all players roll dice
        for player in self.players:
            player.roll_hand()

    # does there need to be a method to reset the lists, this is presumably why you use a copy of lists smh
    def calculate_dice_left(self):
        for player in self.players:
            for dice in player.player_hand:
                self.total_dice_on_table += 1
        for player in self.active_players:
            for dice in player.player_hand:
                self.total_dice_on_table += 1
        print(f'{self.total_dice_on_table} dice are on the table')

    def check_players_elgibility(self):
        for player in self.players:
            if len(player.player_hand) == 0:
                print(f'{player.name} is out of dice')
                self.players.remove(player)

    def choose_active_players(self):

        while len(self.active_players) < 2:
            popped_player = self.players.pop(0)
            self.active_players.append(popped_player)

    def add_next_active_player(self):
        if len(self.players) > 0:
            while len(self.active_players) < 3:
                popped_player = self.players.pop(0)
                self.active_players.append(popped_player)
        elif len(self.players) <= 0:
            popped_player = self.active_players.pop(0)
            self.active_players.append(popped_player)

    def remove_old_active_player(self):
        while len(self.active_players) > 2:
            popped_player = self.active_players.pop(0)
            self.players.append(popped_player)

    def reset_players_lists(self):

        while len(self.active_players) > 0:
            popped_player = self.active_players.pop(0)
            self.players.append(popped_player)

    def set_first_wager(self, game):
        if self.die_wager == 0 and self.quantity_wager == 0:
            player = self.active_players[0]
            player.wager(game)
            if len(self.players) <= 0:
                self.add_next_active_player()

    def play_out_round(self, game):

        while self.die_wager != 0 or self.quantity_wager != 0:
            active_player = self.active_players[1]
            previous_active_player = self.active_players[0]
            active_player.wager_or_bullshit(game)
            if previous_active_player.quantity_wager < active_player.quantity_wager and len(self.players) > 0:
                self.remove_old_active_player()
            elif previous_active_player.quantity_wager == active_player.quantity_wager and len(self.players) > 0:
                if previous_active_player.die_wager < active_player.die_wager:
                    self.remove_old_active_player()


    def play_round(self, game):

        self.check_players_elgibility()
        self.all_players_roll()
        self.choose_active_players()
        self.calculate_dice_left()
        self.set_first_wager(game)
        self.play_out_round(game)
        self.check_players_elgibility()
        self.clear_variables_in_players()


    def clear_wagers(self):
        self.quantity_wager = 0
        self.die_wager = 0
        self.total_dice_on_table = 0
        self.die_wager_counter = 0

    def clear_variables_in_players(self):

        for player in self.players:
            player.number_of_die_inHand = 0
            player.minimum_quantity_wager = 0
            player.percent_of_unsure_must_be_applicable = 0


    def play_game(self, game):

        while len(self.players) > 1:
            self.play_round(game)
            # for player in self.players:
            #     player.clear_die_counter()
        for player in self.players:
            print(f'{player.name} won the game!')