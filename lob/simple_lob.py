import numpy as np

lob_dim = 20
start_book_depth = 110.
start_midPrice = 100.
tick_size = 5.
lob = start_book_depth + np.zeros(lob_dim)
num_step =20

print_diagnostics = True

ord_range = (lob_dim - 1)//2

ord_load = 115

order = ['S', ord_load]

buy_range = range(ord_range + 1, lob_dim + 1)
sell_range = range(ord_range, -1, -1)

def extrinRange(lob, the_range):
    for k in the_range:
        if lob[k] > 0:
            return k
    return -1

def midPrice(lob, buy_range, sell_range, ord_range = ord_range):
    buy_min = start_midPrice + tick_size * (extrinRange(lob, buy_range) - ord_range)
    sell_max = start_midPrice - tick_size * (ord_range - extrinRange(lob, sell_range))
    if print_diagnostics:
        print('extr in sell range', extrinRange(lob, sell_range))
        print('sell_max', sell_max)
        print('extr in buy range',extrinRange(lob, buy_range))
        print('buy_min', buy_min)
    return (buy_min + sell_max)/2.


def lob_order(lob, the_range, ord_residual):
    for k in the_range:
        lob_new =  lob[k] - ord_residual
        ord_hold =  - lob_new
        lob[k] = max(0, lob_new)
        if ord_hold <= 0. :
            break
        ord_residual = ord_hold
    if print_diagnostics:
        print(lob)
    return lob


if order[0] == 'B':
    the_range = buy_range
else:
    the_range = sell_range


def market_run(lob = lob, test_range = num_step, buy_range = buy_range, sell_range = sell_range, ord_load = ord_load)  :
    mids = []
    for i in range(test_range):
        if (i <test_range/3 or i > 3*test_range/4):
            the_range = sell_range
        else:
            the_range = buy_range
        lob = lob_order(lob, the_range, ord_load)
        mid = midPrice(lob, buy_range, sell_range)
        if print_diagnostics:
            print('mid', mid)
        mids.append(mid)
    return mids



import matplotlib.pyplot as plt
def show_mids(mids):
    plt.plot(mids)
    plt.ylabel('stock price')
    plt.xlabel('time')
    plt.title("Limit order book trading")
    plt.ylim(80,120)
    plt.show()

if __name__ == "__main__":
    mids = market_run(lob, num_step, buy_range, sell_range)
    show_mids(mids=mids)














