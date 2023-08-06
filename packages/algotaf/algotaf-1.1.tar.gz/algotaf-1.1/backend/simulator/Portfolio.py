from datetime import timedelta
from enum import Enum

from backend.simulator.Position import Position
from backend.simulator.config import TIME


def xstr(s):
    """
    Converts a None into an empty string
    :param s: String or None
    :return: String or empty string
    """

    if s is None:
        return ''
    else:
        return str(s)


class HistoryType(Enum):
    """
    Enum for portfolio history instances
    """

    PLACE_ORDER = 1
    EXCHANGE_ORDER = 2
    EXPIRE_ORDER = 3
    CANCEL_ORDER = 4
    DIVIDEND = 5
    SPLIT = 6


class Interval(Enum):
    """
    Enum for printing portfolio with interval differences
    """

    MINUTE1 = 1
    MINUTE5 = 2
    MINUTE10 = 3
    MINUTE15 = 4
    MINUTE30 = 5
    HOUR = 6
    DAY = 7
    WEEK = 8
    MONTH = 9
    YEAR = 10
    ALL = 11


class HistoryInstance:
    """
    HistoryInstance class for logging events in the portfolio
    """

    def __init__(self, history_type, message='', **kwargs):
        """
        :param history_type: HistoryType enum
        :param message: String to print
        :param kwargs: Keyword args of order values or position values
        """

        self.message = message
        self.history_type = history_type
        self.kwargs = kwargs

    def print_history(self):
        """
        Prints the message and values of instance
        """

        print(self.message)
        for key, val in self.kwargs.items():
            history = '{key: <20} | {val: <20}'.format(key=key, val=xstr(val))
            print(history)
        print()


class Portfolio:
    """
    Portfolio class for backtester containing funds, positions, orders, and history
    """

    def __init__(self, name):
        """
        :param name: Name of portfolio
        """

        self.name = name
        self.positions = {}
        self.orders = []
        self.history = {}
        self.funds = 0
        self.diff = 0
        self.total_equity = 0

    def add_to_history(self, history_type, message, ticker, order=None, position=None):
        """
        Creates and adds an instance to history
        :param history_type: HistoryType enum
        :param message: String to print
        :param ticker: Ticker name
        :param order: Order info
        :param position: Position info
        """

        if history_type == HistoryType.DIVIDEND:
            instance = HistoryInstance(HistoryType.DIVIDEND,
                                       message='Dividend Paid',
                                       ticker=position.ticker,
                                       shares=position.shares,
                                       dividend=position.dividend,
                                       total_amount=round(position.shares * position.dividend, 2),
                                       date=TIME.date)
        elif history_type == HistoryType.SPLIT:
            instance = HistoryInstance(HistoryType.SPLIT,
                                       message='Stock Split',
                                       ticker=position.ticker,
                                       shares=position.shares,
                                       split=position.split,
                                       cur_quote=position.cur_quote,
                                       date=TIME.date)
        else:
            instance = HistoryInstance(history_type,
                                       message=message,
                                       ticker=order.ticker,
                                       buy=order.buy,
                                       limit=order.limit,
                                       shares=order.shares,
                                       equity=round(order.equity, 2),
                                       cur_quote=order.cur_quote,
                                       time_placed=order.time_placed,
                                       time_expire=order.time_expire,
                                       time_exchanged=order.time_exchanged)

        instance.print_history()
        if ticker in self.history:
            if history_type in self.history[ticker]:
                self.history[ticker][history_type].append(instance)
            else:
                self.history[ticker][history_type] = [instance]
        else:
            self.history[ticker] = {history_type: [instance]}

    def deposit(self, funds):
        """
        Deposits funds in portfolio
        :param funds: Funds to add
        """

        self.funds += funds
        self.total_equity += funds

    def withdraw(self, funds):
        """
        Withdraws funds from portfolio
        :param funds: Funds to remove
        """

        if funds <= self.funds:
            self.funds -= funds
            self.total_equity -= funds

    def print_portfolio(self, interval):
        """
        Prints portfolio data at current timestamp
        :param interval: Timedelta interval
        """

        print('Portfolio - %s' % self.name)
        print('{key: <20} | {val: <20}'.format(key='funds', val=round(self.funds, 2)))
        print('{key: <20} | {val: <20}'.format(key='total_equity', val=round(self.total_equity, 2)))
        if len(self.positions) > 0:
            total_diff = 0
            total_percent = 0
            for ticker, position in self.positions.items():
                diff = 0
                if interval == Interval.ALL:
                    diff = position.cur_equity - position.init_equity
                percent = diff / position.cur_equity * 100
                total_diff += diff
                total_percent += percent

                print('{ticker: <20} | {diff: <20} | {percent}%'
                      .format(ticker=ticker, diff=round(diff, 2), percent=round(percent, 2)))

            total_percent /= len(self.positions)

            print('{key: <20} | {diff: <20} | {percent}%\n'
                  .format(key='total_diff', diff=round(total_diff, 2), percent=round(total_percent, 2)))

    def place_order(self, order):
        """
        Places order and adds to portfolio
        :param order: Order to add
        """

        if order.shares > 0:
            ticker = order.ticker
            if order.buy or (ticker in self.positions and order.shares <= self.positions[ticker].shares):
                order.set_quote()
                if order.cur_quote * order.shares <= self.funds:
                    self.orders.append(order)
                    self.add_to_history(HistoryType.PLACE_ORDER, 'Order Placed', order.ticker, order=order)
                else:
                    print('Invalid order: Not enough funds\n')
            else:
                print('Invalid order: Not enough owned shares to sell\n')
        else:
            print('Invalid order: Shares must be > 0\n')

    def expire(self, index, order):
        """
        Expires an order from portfolio
        :param index: Index of order
        :param order: Order info
        """

        self.orders.pop(index)
        self.add_to_history(HistoryType.EXPIRE_ORDER, 'Order Expired', order.ticker, order=order)

    def check_dividend_date(self, ticker):
        """
        Checks the date to make sure dividend should be paid
        :param ticker: Ticker name
        :return: Number of shares to pay out
        """

        shares = 0
        if ticker in self.history and HistoryType.EXCHANGE_ORDER in self.history[ticker]:
            for instance in self.history[ticker][HistoryType.EXCHANGE_ORDER]:
                if instance.kwargs['buy']:
                    if TIME.date - timedelta(days=30) <= instance.kwargs['time_exchanged'].date():
                        shares += instance.kwargs['shares']
                else:
                    shares -= instance.kwargs['shares']
        return shares

    def calc_dividends(self, ticker):
        """
        Calculates whether a dividend should be paid and pays it
        :param ticker: Ticker name
        """

        position = self.positions[ticker]
        if position.dividend > 0 and position.dividend_date != TIME.date:
            shares = self.check_dividend_date(ticker)
            if shares > 0:
                position.dividend_date = TIME.date
                payout = position.shares * position.dividend
                self.funds += payout
                self.total_equity += payout
                self.add_to_history(HistoryType.DIVIDEND, 'Dividend Paid', ticker, position=position)

    def calc_split(self, ticker):
        """
        Calculates the split of a stock if it exists for the date
        :param ticker: Ticker name
        """

        position = self.positions[ticker]
        if position.split_date != TIME.date:
            position.split_date = TIME.date
            position.shares *= position.split
            if position.split > 1:
                self.add_to_history(HistoryType.SPLIT, 'Stock Split', ticker, position=position)

    def get_exchange_dates(self, ticker):
        """
        Gets all the dates where a ticker was exchanged (Unused)
        :param ticker: Ticker name
        :return: Dict {datetime: shares}
        """

        dates = {}
        if ticker in self.history and HistoryType.EXCHANGE_ORDER in self.history[ticker]:
            for instance in self.history[ticker][HistoryType.EXCHANGE_ORDER]:
                if TIME.date == instance.kwargs['time_exchanged'].date():
                    if instance.kwargs['buy']:
                        dates[instance.kwargs['time_exchanged']] = instance.kwargs['shares']
                    else:
                        dates[instance.kwargs['time_exchanged']] = instance.kwargs['shares'] * -1
        return dates

    def buy_position(self, index, order, position):
        """
        Buys a position and adds it to portfolio
        :param index: Index of order
        :param order: Order info
        :param position: Position info
        :return:
        """

        self.orders.pop(index)
        self.funds -= position.shares * position.cur_quote
        ticker = position.ticker

        if ticker in self.positions:
            pos = self.positions[ticker]
            weight1 = position.avg_quote * position.shares
            weight2 = pos.avg_quote * pos.shares
            total_shares = position.shares + pos.shares

            pos.shares = total_shares
            pos.avg_quote = (weight1 + weight2) / total_shares
            pos.init_equity = (weight1 + weight2)
        else:
            self.positions[ticker] = position

        self.add_to_history(HistoryType.EXCHANGE_ORDER, 'Order Exchanged', order.ticker, order=order)

    def sell_position(self, index, order, position):
        """
        Sells a position and removes it from portfolio
        :param index: Index of order
        :param order: Order info
        :param position: Position info
        :return:
        """

        ticker = position.ticker
        if ticker in self.positions:
            pos = self.positions[ticker]
            if position.shares <= pos.shares:
                self.orders.pop(index)
                self.funds += position.shares * position.cur_quote
                pos.shares -= position.shares
                if pos.shares == 0:
                    del self.positions[ticker]

        self.add_to_history(HistoryType.EXCHANGE_ORDER, 'Order Exchanged', order.ticker, order=order)

    def update(self):
        """
        Updates all the orders and positions in portfolio
        """

        orders = self.orders.copy()
        for i, order in enumerate(orders):
            if TIME.timestamp > order.time_expire:
                self.expire(i, order)
            else:
                execute = order.update()
                if execute and order.buy:
                    position = Position(order)
                    self.buy_position(i, order, position)
                elif execute:
                    position = Position(order)
                    self.sell_position(i, order, position)
        self.total_equity = self.funds

        for ticker, position in self.positions.items():
            position.update_special()
            self.calc_split(ticker)
            self.calc_dividends(ticker)

            position.update()
            self.total_equity += position.cur_equity
