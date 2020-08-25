import numpy as np
import csv

"""
Bet placement Encoding:
    0 : 'Pass'
    1 : 'Don't Pass'
        ...
    4 : ...

"""


class Table:
    '''Defines the current state of the table with 1 player

    '''
    table_odds = ''

    def __init__(self, player):
        self.player = player  # TODO add multiplayer
        self.dice1 = 0
        self.dice2 = 0
        self.dice_sum = 0
        self.point_on = 0  # the point
        self.roll = False
        self.table_odds == '3-4-5X'
        self.n = 0
        self.round = []

    def roll_dice(self):
        # sets the state of the most recent roll
        self.dice1 = np.random.randint(1, 7)
        self.dice2 = np.random.randint(1, 7)
        self.dice_sum = self.dice1 + self.dice2
        self.n += 1
        self.round.append(self.dice_sum)
        print(
            f'You rolled a {self.dice1} and a {self.dice2}\nThe sum is {self.dice_sum}')

    def ask_bet_sim(self, bet):
        """
        Simulation Version of the Game
        input an array like 2x1 of ints, 
              indicating a placement (see encoding above) and an amount, 
              assumes the source has checked its validity as ints

        """
        if not self.point_on:
            placement = bet[0]
            amount = bet[1]
            self.player.place_bet(placement, amount)
        elif self.point_on:
            if self.player.pass_ and not self.player.pass_odds:
                self.player.take_odds(self.point_on)
            elif self.player.dont_pass and not self.player.dont_pass_odds:
                self.player.lay_odds(self.point_on)

    def new_shooter_sim(self):
        self.roll = True
        while self.roll:
            print(self.player)

            if self.player.chips:
                self.ask_bet(self.player)
            print('\nNew Roll:')
            self.roll_dice()

            if not self.point_on:  # come out roll
                # craps
                if self.dice_sum in {2, 3, 12}:
                    self.player.pass_loses()
                    if self.dice_sum == 12:
                        self.player.dont_pass_push()
                    else:
                        self.player.dont_pass_wins()

                elif self.dice_sum in {7, 11}:
                    self.player.pass_wins()
                    self.player.dont_pass_loses()

                elif self.dice_sum in {4, 5, 6, 8, 9, 10}:
                    # set the point
                    self.point_on = self.dice_sum
                    print(f'Point set to {self.point_on}')

            elif self.point_on:  # same point
                print(f'The point is on {self.point_on}')
                if self.dice_sum in {4, 5, 6, 8, 9, 10}:
                    if self.point_on == self.dice_sum:
                        if self.player.pass_:
                            self.player.pass_wins(self.point_on)
                        elif self.player.dont_pass:
                            self.player.dont_pass_loses()
                        self.finish_round()
                # payout for various bets (TODO after mvp is working)
                #                     if self.dice_sum == 4:
                #                         pass
                #                     elif self.dice_sum == 5:
                #                         pass
                #                     elif self.dice_sum == 6:
                #                         pass
                #                     elif self.dice_sum == 8:
                #                         pass
                #                     elif self.dice_sum == 9:
                #                         pass
                #                     elif self.dice_sum == 10:
                #                         pass
                elif self.dice_sum == 7:
                    self.player.pass_loses()
                    self.player.dont_pass_wins(self.point_on)
                    self.finish_round()

    def ask_bet(self, player) -> dict:
        """
        CLI version of the game
        """
        # check if player has money to play this round
        amount_valid = 0
        placement_valid = ''
        # if not player.chips:
        #     print("sorry you need more cash to play this round")
        # else:
        # rollout
        if not self.point_on:
            # placement
            print("What bet would you like to place? pass (p) or don't pass (dp)?")
            placement_input = input(
                "(Enter 'p' to bet on Pass Line or 'dp' to bet on Dont Pass Line): ")
            if placement_input in {'p', "P"}:
                placement_valid = 0  # pass
            elif placement_input in {'dp', "DP"}:
                placement_valid = 1  # don't pass
            else:
                print('invalid bet placement')
            # amount
            print("How much would you like to bet?")
            while True:
                amount_input = input(
                    "(Enter the dollar amount you'd like to bet) ")
                try:
                    amount_valid = int(amount_input)
                    break
                except:
                    print("You can only but dollars (integers, please)")
            # check
            if placement_valid and amount_valid:
                player.place_bet(placement_valid, amount_valid)
            else:
                print("something went wrong placing the bet")

        elif self.point_on:
            if self.player.pass_ and not self.player.pass_odds:
                self.player.take_odds(self.point_on)

            elif self.player.dont_pass and not self.player.dont_pass_odds:
                self.player.lay_odds(self.point_on)

    def new_shooter(self):
        '''Most of the game logic of each 'round', for the CLI version

        '''
        self.roll = True
        while self.roll:
            print(self.player)

            if self.player.chips:
                self.ask_bet(self.player)
            print('\nNew Roll:')
            self.roll_dice()

            if not self.point_on:  # come out roll
                # craps
                if self.dice_sum in {2, 3, 12}:
                    self.player.pass_loses()
                    if self.dice_sum == 12:
                        self.player.dont_pass_push()
                    else:
                        self.player.dont_pass_wins()

                elif self.dice_sum in {7, 11}:
                    self.player.pass_wins()
                    self.player.dont_pass_loses()

                elif self.dice_sum in {4, 5, 6, 8, 9, 10}:
                    # set the point
                    self.point_on = self.dice_sum
                    print(f'Point set to {self.point_on}')

            elif self.point_on:  # same point
                print(f'The point is on {self.point_on}')
                if self.dice_sum in {4, 5, 6, 8, 9, 10}:
                    if self.point_on == self.dice_sum:
                        if self.player.pass_:
                            self.player.pass_wins(self.point_on)
                        elif self.player.dont_pass:
                            self.player.dont_pass_loses()
                        self.finish_round()
                # payout for various bets (TODO after mvp is working)
                #                     if self.dice_sum == 4:
                #                         pass
                #                     elif self.dice_sum == 5:
                #                         pass
                #                     elif self.dice_sum == 6:
                #                         pass
                #                     elif self.dice_sum == 8:
                #                         pass
                #                     elif self.dice_sum == 9:
                #                         pass
                #                     elif self.dice_sum == 10:
                #                         pass
                elif self.dice_sum == 7:
                    self.player.pass_loses()
                    self.player.dont_pass_wins(self.point_on)
                    self.finish_round()

    def finish_round(self):
        self.point_on = 0
        print(f'\nRound completed in {self.n} rolls')
        self.n = 0
        summary = np.array(self.round)
        print(summary)
        return summary
        # TODO what else?
