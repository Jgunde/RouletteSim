"""
Author: Jacob Gunderson
Date: August 10, 2021
Description: I wrote this program to prove to my roommate Andrew Souza that there is no possible strategy to roulette.
The "strategy" disproven here is this:
    You make a starting bet of say 2.
    Then if you win you start over and bet 2 again.
    If you loose then you double the bet to 4.
    You continue to double the bet until you win and recoup your money.
    Andrew suggested using another sequence like the Fibonacci numbers but it doesn't really make a difference.
"""

import random


def main():

    seq_gen = exp  # the sequence of bets you'll use
    starting_funds = 500000  # starting amount of money each epoch
    play_range = [50, 200]  # First number is the minimum number of times you'll play before quitting (because you'll want to play a few rounds at least). The second number is the maximum number of times you'll play (because you have to go home eventually).

    # NOTE: A bust is when you loose enough times in a row that your next bet (which you need to recoup your losses)
    #   is more than the current amount of money you have.
    #   Busting is the reason you loose. If you set no_bust to True, you can see that you gain money.
    #   If no_bust is False (which is like real life), then you loose money.
    #   Even though it seems unlikely to loose enough times in a row that you bust, it happens. And the looses from
    #   busts outweigh the gains from the wins.
    no_bust = False

    epochs = 10000  # we simulate this many times
    print_epochs = 10  # we only print the first X simulations

    ##############################

    total = 0  # running sum of net gain after each epoch
    bust_count = 0  # to count the number of busts

    # One epoch is like going to a casino one time.
    for epoch in range(epochs):
        # Initial conditions:
        money = starting_funds
        prev_money = money  # used to check if we just won
        seq = seq_gen()     # create a sequence generator
        bet = next(seq)     # get the first bet in the sequence
        busted = False      # a bust is if you're next bet is more than your current amount of money

        if epoch < print_epochs:
            print(f"\n##### Epoch: {epoch} #####\n")

        # This is where we implement the strategy and bet.
        for round in range(play_range[1]):
            if epoch < print_epochs:
                print(f"Round:   {round}")
                print(f"  Money: {money}")
                print(f"  Bet:   {bet}")

            if bet > money:  # if we can't afford the next bet we bust
                busted = True
                bust_count += 1
                if epoch < print_epochs:
                    print("--BUST--")
                break

            if round > play_range[0] and money >= prev_money:  # we quit after a win
                break

            rand_num = random.randint(-1, 36)  # generate a roulette number: -1 = 00, 0 = 0, 1 = 1 ...

            # on 00 and 0 (not red or black) we loose
            if rand_num == -1 or rand_num == 0 \
                    or rand_num % 2 != 0:  # on odd numbers we loose
                # loss:
                money -= bet
                bet = next(seq)
            else:  # on even numbers we win
                # win:
                money += bet
                seq = seq_gen()  # restart sequence
                bet = next(seq)

            prev_money = money

            if epoch < print_epochs:
                print()

        # Here's where we show why you eventually loose money. Try disabling busts and you gain money.
        if not no_bust or not busted:
            total += money - starting_funds
        else:
            pass
            # total += 0

        if epoch < print_epochs:
            print(f"\nRunning total: {total}\n")

    print(f"\n---------------\nAverage Net Gain: {total / epochs : .2f}")
    print(f"Bust Probability: {bust_count / epochs * 100 : .2f}%")



# TODO: Find a formula to get any nth fibonacci number.
# generates fibonacci numbers
def fib():
    # (we're ignoring 0)
    # a, b = 1, 1
    a, b = 2, 3  # lets start on 2
    while True:
        yield a
        a, b = b, a + b


# The next number in this sequence is the sum of the previous numbers in the sequence. So betting the next number will always recoup all your previous bets.
def exp():
    prev_num = 1
    while True:
        # nums = [1]
        # nums.append(sum(nums))
        # This is the same as summing the entire sequence:
        new_num = prev_num * 2
        prev_num = new_num
        yield new_num



if __name__ == '__main__':
    main()
