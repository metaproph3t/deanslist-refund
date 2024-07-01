# I've got a CSV file with the following columns:
# size, average_price, user_acct, side
# I want to calculate the loss for each user_acct
# The loss is calculated as follows:
# If the user_acct is a buyer, the loss is the difference between the average_price and the current price

import pandas as pd

csv_file = 'deanslist_evaluation.csv'
df = pd.read_csv(csv_file)

# Get the current price
current_price = 0.0025

def calculate_loss(row):
    if row['side'] == 'ASK':
        return (current_price - row['average_price']) * row['size']
    else:
        return (row['average_price'] - current_price) * row['size']

# Calculate the loss
df['loss'] = df.apply(calculate_loss, axis=1)

print(df)

# Group by user_acct and sum the loss
# loss = df.groupby('user_acct')['loss'].sum()

# now allocate 1,500,000 DEAN tokens according to the amount of loss they had.
# don't include those with negative losses
loss = df[df['loss'] > 0].groupby('user_acct')['loss'].sum()
total_loss = loss.sum()

# print the loss
print(loss)
print('Total loss: ', total_loss)

pd.set_option('display.float_format', lambda x: '%.2f' % x)

# allocate the tokens
total_tokens = 1_600_000
df['tokens'] = df.apply(lambda row: ((row['loss'] / total_loss) * total_tokens) if row['loss'] > 0 else 0, axis=1)


# print the tokens
print(df['tokens'].groupby(df['user_acct']).sum())
