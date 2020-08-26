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

    def __init__(self, player, n_trials):
        self.player = player  # TODO add multiplayer
        # Current Roll
        self.dice1 = 0
        self.dice2 = 0
        self.dice_sum = 0
        self.point_on = 0  # the point
        self.table_odds == '3-4-5X'
        ### Stats ###
        self.n_trials = n_trials
        self.rolls = []
        self.winning_bet = []
        self.bet_placed = []
        self.bet_amount = []  # list of dicts
        self.amount_won = []
        self.chips_report = []
        # meta
        # number of rounds, set at the beginning, determines # rows of resulting csv
        self.n_rounds = 0
        self.round = False

    def roll_dice(self):
        # sets the state of the most recent roll
        self.dice1 = np.random.randint(1, 7)
        self.dice2 = np.random.randint(1, 7)
        self.dice_sum = self.dice1 + self.dice2
        # self.n_rolls += 1
        self.rolls.append(self.dice_sum)
        print(
            f'You rolled a {self.dice1} and a {self.dice2}\nThe sum is {self.dice_sum}')

    def gen_bet(self):
        placement = np.random.choice([0, 1])
        amount = np.random.randint(self.player.chips)
        return placement, amount

    def ask_bet(self):
        """
        Simulation Version of the Game
        input an array like 2x1 of ints,
              indicating a placement (see encoding above) and an amount,
              assumes the source has checked its validity as ints

        """

        if not self.point_on:
            placement, amount = self.gen_bet()
            # bet = {placement: amount}
            self.bet_placed.append(placement)
            self.bet_amount.append(amount)
            self.player.place_bet(placement, amount)
            print('bet placed')

        elif self.point_on:
            if self.player.pass_ and not self.player.pass_odds:
                amount = self.player.take_odds(self.point_on)
                self.bet_placed.append(2)
                self.bet_amount.append(amount)
                print('bet placed take odds')
            elif self.player.dont_pass and not self.player.dont_pass_odds:
                amount = self.player.lay_odds(self.point_on)
                self.bet_placed.append(3)
                self.bet_amount.append(amount)
                print('bet placed lay odds')

    def write_csv(self):

        fields = ['dice_rolls',
                  'winning_bet', 'bet_placed', 'bet_amount', 'amount_won', 'chips_report']

        rows = zip(self.rolls, self.winning_bet, self.bet_placed,
                   self.bet_amount, self.amount_won, self.chips_report)

        filename = 'tmp.csv'

        with open(filename, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(fields)
            for row in rows:
                csvwriter.writerow(row)

    def new_shooter(self):
        for n in range(self.n_trials):
            self.chips_report.append(self.player.chips)
            self.round = True
            while self.round:
                print(self.player)
                print(f'round {n}')

                if self.player.chips:
                    self.ask_bet()
                print('\nNew Roll:')
                self.roll_dice()

                if not self.point_on:  # come out roll
                    # craps
                    if self.dice_sum in {2, 3, 12}:
                        self.player.pass_loses()
                        if self.dice_sum == 12:
                            self.player.dont_pass_push()
                            self.round = False
                        else:
                            if self.player.dont_pass:
                                self.update_win(1)

                    elif self.dice_sum in {7, 11}:
                        if self.player.pass_:
                            self.update_win(0)
                        elif self.player.dont_pass:
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
                                self.update_win(0)
                            elif self.player.dont_pass:
                                self.player.dont_pass_loses()
                            self.finish_round()
                        else:
                            self.winning_bet.append(-1)
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
                        if self.player.dont_pass:
                            amount = self.player.dont_pass_wins(self.point_on)
                            self.winning_bet.append(1)
                            if amount:
                                self.amount_won.append(amount)
                            else:
                                self.amount_won.append(0)

                        self.finish_round()
                    else:
                        self.winning_bet.append(-1)
        self.write_csv()

    def finish_round(self):
        self.point_on = 0
        self.round = False

    def update_win(self, pos, point=0):
        amount = 0
        if pos == 0:
            self.winning_bet.append(0)
            amount = self.player.pass_wins(point)
            self.winning_bet.append(0)
        if pos == 1:
            self.winning_bet.append(1)
            amount = self.player.dont_pass_wins(point)
            self.winning_bet.append(1)
        self.amount_won.append(amount)
