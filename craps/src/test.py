import table as tb
import player as pl
import pandas as pd

p = pl.Player(100)
t = tb.Table(p, 10)

# t.roll_dice()
# t.ask_bet(p)

# print(p.pass_)
t.new_shooter()

df = pd.read_csv('tmp.csv')
print(df)
