import numpy as np


class Player(object):
    '''
    updates this player's bets.

    '''

    def __init__(self, chips):
        self.chips = chips
        # 'Place' bets
        self.four = 0
        self.five = 0
        self.six = 0
        self.eight = 0
        self.nine = 0
        self.ten = 0
        # Other bets
        self.pass_ = 0
        self.pass_odds = 0
        self.dont_pass = 0
        self.dont_pass_odds = 0
        self.table_odds = '3-4-5X'

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"""\nLive Bets: 
                \npass: {self.pass_}, pass odds: {self.pass_odds},
                \ndon't pass: {self.dont_pass}, don't pass odds: {self.dont_pass_odds}
                \nTotal chips: {self.chips} 
                """
    ### Making the bet ###

    def place_bet(self, placement, amount):
        """pass/dont pass on a rollout
        """
        if self.chips - amount >= 0:
            try:
                if placement == 'pass' and not self.dont_pass:
                    self.pass_ += amount
                    self.chips -= amount
                elif placement == 'dont_pass' and not self.pass_:
                    self.dont_pass += amount
                    self.chips -= amount
            except:
                print("You can't bet on that, pal")
        else:
            print('Bet a smaller bid.')

    def take_odds(self, point_on):
        '''set pass odds

        '''
        if self.table_odds == '3-4-5X':
            # 5x
            if point_on in {6, 8}:
                amount = 5*self.pass_
                self._take_odds(amount)
            # 4x
            elif point_on in {9, 5}:
                amount = 4*self.pass_
                self._take_odds(amount)
            # 3x
            elif point_on in {4, 10}:
                amount = 3*self.pass_
                self._take_odds(amount)

        else:
            print("We don't play by those rules at this casino")

    def _take_odds(self, amount):
        if self.chips - amount >= 0:
            self.pass_odds = amount
            self.chips -= amount
            print(f"Taking full odds for {amount}")
        else:
            print('Skipping odds bet, not enough chips.')

    # TODO adjust
    def lay_odds(self, point_on):
        '''set don't pass odds at the maximum amount given the table_odds in use

        '''
        if self.table_odds == '3-4-5X':
            # 5x
            if point_on in {6, 8}:
                amount = 5*self.dont_pass
                self._lay_odds(amount)
            # 4x
            elif point_on in {9, 5}:
                amount = 4*self.dont_pass
                self._lay_odds(amount)
            # 3x
            elif point_on in {4, 10}:
                amount = 3*self.dont_pass
                self._lay_odds(amount)
        else:
            print("We don't play by those rules at this casino")

    def _lay_odds(self, amount):
        if self.chips - amount >= 0:
            self.dont_pass_odds = amount
            self.chips -= amount
            print(f"Laying full odds for {amount}")
        else:
            print('Skipping odds bet, not enough chips.')

    ### Wins/Losses ###
    def pass_wins(self, point_on=0):
        if self.pass_:
            win = 2*self.pass_
            win_odds = 0
            self.chips += win
            # pass odds TODO check these numbers
            if self.pass_odds:
                # 6:5
                if point_on in {6, 8}:
                    win_odds = 1.2*self.pass_odds + self.pass_odds
                    self.chips += win_odds
                # 3:2
                elif point_on in {9, 5}:
                    win_odds = 1.5*self.pass_odds + self.pass_odds
                    self.chips += win_odds
                # 2:1
                elif point_on in {4, 10}:
                    win_odds = 2*self.pass_odds + self.pass_odds
                    self.chips += win_odds
            print(f'Pass wins! Payout: {win + win_odds}')
            self.reset_bet('pass_')

    def pass_loses(self):
        print(f"Pass loses {self.pass_ + self.pass_odds}")
        self.reset_bet('pass_')

    def dont_pass_wins(self, point_on=0):
        if self.dont_pass:
            win = 2*self.dont_pass
            win_odds = 0
            self.chips += win
            if self.dont_pass_odds:
                # 5:6
                if point_on in {6, 8}:
                    win_odds = (5/6)*self.dont_pass_odds + self.dont_pass_odds
                    self.chips += win_odds
                # 2:3
                elif point_on in {9, 5}:
                    win_odds = (2/3)*self.dont_pass_odds + self.dont_pass_odds
                    self.chips += win_odds
                # 1:2
                elif point_on in {4, 10}:
                    win_odds = 0.5*self.dont_pass_odds + self.dont_pass_odds
                    self.chips += win_odds

            print(f'Dont pass wins! Pay out: {win + win_odds}')
            self.reset_bet('dont_pass')

    ### Table Cleaning ###
    def dont_pass_loses(self):
        print(f"Don't pass loses {self.dont_pass + self.dont_pass_odds}")
        self.reset_bet('dont_pass')

    def dont_pass_push(self):
        print("Don't Pass push!")
        self.chips += self.dont_pass
        self.dont_pass_ = 0

    def reset_bet(self, placement):
        if placement == 'pass_':
            self.pass_ = 0
            self.pass_odds = 0
        elif placement == 'dont_pass':
            self.dont_pass = 0
            self.dont_pass_odds = 0
