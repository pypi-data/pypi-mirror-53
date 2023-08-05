from collections import defaultdict
from typing import DefaultDict
from typing import List
from typing import Optional

from terminaltables import AsciiTable

from data.watchlist import ALL_REVERSED
from report.symbolhistory.symbolhistorycontext import SymbolHistoryContext
from report.symbolhistory.symbolhistoryevent import symbol_history_event_from_option_event
from report.symbolhistory.symbolhistoryevent import symbol_history_event_from_option_order
from report.symbolhistory.symbolhistoryevent import symbol_history_event_from_stock_order
from report.symbolhistory.symbolhistoryevent import SymbolHistoryEvent
from robinhood.lib.account.optionevent.optionevent import OptionEvent
from robinhood.lib.account.optionorder.optionorder import OptionOrder
from robinhood.lib.account.stockorder.stockorder import StockOrder
from robinhood.lib.helpers import format_optional_price
from robinhood.lib.helpers import format_price
from robinhood.lib.helpers import format_quantity
from robinhood.lib.robinhoodclient import rhc


class SymbolHistory(object):

    def __init__(
        self,
        stock_orders: List[StockOrder],
        option_orders: List[OptionOrder],
        option_events: List[OptionEvent],
    ) -> None:
        self._events_by_symbol = self._load_events_by_symbol(
            stock_orders=stock_orders,
            option_orders=option_orders,
            option_events=option_events,
        )

    def get_events(self, symbol: str) -> List[SymbolHistoryEvent]:
        return self._events_by_symbol[symbol]

    def show_positions(self, symbol: str) -> None:
        pass

    def show(self, symbol: str, last_n_events: Optional[int] = 10) -> None:
        data = self._gen_ascii_tbl_data(symbol=symbol)
        if last_n_events is None:
            applicable_data = data
        else:
            data_no_head = data[1:]
            applicable_data = [data[0]] + data_no_head[-last_n_events - 1:]
        t = AsciiTable(applicable_data)
        t.inner_column_border = True
        t.inner_footing_row_border = False
        t.inner_heading_row_border = True
        t.inner_row_border = False
        t.outer_border = False
        t.justify_columns = {
            0: 'center',
            1: 'center',
            2: 'center',
            3: 'right',
            4: 'right',
            5: 'right',
            6: 'right',
            7: 'right',
        }
        print(t.table)

    def show_holdings_by_events(self, symbol: str) -> None:
        events = self.get_events(symbol=symbol)
        for event in events:
            print(event.event_name)
            quantity = event.context.stock_holding.quantity
            avg_price = event.context.stock_holding.avg_unit_price
            print('>>> Stock Holding: {quantity} x {avg_price} = {total_value}'.format(
                quantity=format_quantity(quantity),
                avg_price=format_price(avg_price),
                total_value=format_price(quantity * avg_price),
            ))

            for _, item in event.context.option_buy_holding.items():
                print('>>> Option Buy Holding: {quantity} x {avg_price} = {total_value}'.format(
                    quantity=format_quantity(item.quantity),
                    avg_price=format_price(item.avg_unit_price),
                    total_value=format_price(item.quantity * item.avg_unit_price),
                ))

            for _, item in event.context.option_sell_holding.items():
                print('>>> Option Sell Holding: {quantity} x {avg_price} = {total_value}'.format(
                    quantity=format_quantity(item.quantity),
                    avg_price=format_price(item.avg_unit_price),
                    total_value=format_price(item.quantity * item.avg_unit_price),
                ))

            print()

    def _gen_ascii_tbl_data(self, symbol: str) -> List[List[str]]:
        data = [[
            'Date',
            'Event',
            'Symbol',
            'Quantity',
            'Price',
            '# of Shares',
            'Avg Price',
            'Cumulative Profit',
        ]]

        for event in self._events_by_symbol[symbol]:
            # could be option legs from vertical
            if event.context is None:
                continue

            data.append(
                [
                    event.formatted_ts,
                    event.event_name,
                    event.symbol,
                    format_quantity(event.quantity),
                    format_optional_price(event.unit_price),
                    format_quantity(event.context.stock_holding.quantity),
                    format_price(event.context.stock_holding.avg_unit_price),
                    format_price(event.context.profit),
                ],
            )

        return data

    def _load_events_by_symbol(
        self,
        stock_orders: List[StockOrder],
        option_orders: List[OptionOrder],
        option_events: List[OptionEvent],
    ) -> DefaultDict[str, List[SymbolHistoryEvent]]:
        events_by_symbol: DefaultDict[str, List[SymbolHistoryEvent]] = defaultdict(list)

        self._convert_stock_orders_to_symbol_history_events(
            stock_orders=stock_orders,
            events_by_symbol=events_by_symbol,
        )

        self._convert_option_orders_to_symbol_history_events(
            option_orders=option_orders,
            events_by_symbol=events_by_symbol,
        )

        self._convert_option_events_to_symbol_history_events(
            option_events=option_events,
            events_by_symbol=events_by_symbol,
        )

        for symbol, symbol_events in events_by_symbol.items():
            events_by_symbol[symbol] = sorted(symbol_events, key=lambda e: e.event_ts)

        for symbol, symbol_events in events_by_symbol.items():
            context = SymbolHistoryContext(symbol=symbol)
            for event in symbol_events:
                if event.event_name in ('SHORT PUT', 'SHORT CALL'):
                    assert event.unit_price is not None
                    assert event.option_order.num_of_legs == 1
                    leg = event.option_order.legs[0]
                    context.sell_to_open(
                        symbol=event.symbol,
                        quantity=int(event.quantity) * leg.ratio_quantity,
                        price=abs(event.unit_price),
                        option_instrument=leg.option_instrument,
                    )
                elif event.event_name in ('LONG PUT', 'LONG CALL'):
                    assert event.unit_price is not None
                    assert len(event.option_order.opening_legs) == 1
                    context.buy_to_open(
                        symbol=event.symbol,
                        quantity=int(event.quantity),
                        price=event.unit_price,
                        option_instrument=event.option_order.legs[0].option_instrument,
                    )
                elif event.event_name in {'ROLLING CALL', 'ROLLING PUT'}:
                    assert event.unit_price is not None
                    closing_option_instrument = event.option_rolling_order.closing_leg.option_instrument
                    unit_price = context.option_sell_holding[closing_option_instrument.symbol].avg_unit_price
                    context.buy_to_close(
                        symbol=closing_option_instrument.symbol,
                        quantity=int(event.quantity),
                        price=unit_price,
                    )

                    leg = event.option_rolling_order.opening_leg
                    context.sell_to_open(
                        symbol=leg.option_instrument.symbol,
                        quantity=int(event.quantity) * leg.ratio_quantity,
                        price=abs(event.unit_price) + unit_price,
                        option_instrument=leg.option_instrument,
                    )
                elif event.event_name == 'SHORT CALL SPREAD':
                    for leg in event.option_order.legs:
                        if leg.side == 'buy':
                            context.buy_to_open(
                                symbol=leg.option_instrument.symbol,
                                quantity=int(leg.quantity),
                                price=leg.price,
                                option_instrument=leg.option_instrument,
                            )
                        else:
                            context.sell_to_open(
                                symbol=leg.option_instrument.symbol,
                                quantity=int(leg.quantity),
                                price=leg.price,
                                option_instrument=leg.option_instrument,
                            )
                elif event.event_name == 'OPTION EXPIRATION':
                    context.option_expire(
                        symbol=event.symbol,
                        quantity=int(event.quantity),
                    )
                elif event.event_name == 'BUY TO CLOSE':
                    assert event.unit_price is not None
                    context.buy_to_close(
                        symbol=event.symbol,
                        quantity=int(event.quantity),
                        price=event.unit_price,
                    )
                elif event.event_name == 'SELL TO CLOSE':
                    assert event.unit_price is not None
                    context.sell_to_close(
                        symbol=event.symbol,
                        quantity=int(event.quantity),
                        price=event.unit_price,
                    )
                elif event.event_name == 'CALL ASSIGNMENT':
                    assert event.unit_price is not None
                    context.call_assignment(
                        symbol=event.symbol,
                        quantity=int(event.quantity),
                        price=event.unit_price,
                    )
                elif event.event_name == 'PUT ASSIGNMENT':
                    instrument = event.option_event.option_instrument
                    assert event.unit_price is not None
                    context.put_asignment(
                        symbol=event.symbol,
                        quantity=int(event.quantity),
                        price=event.unit_price,
                        strike_price=instrument.strike_price,
                    )
                elif event.event_name == 'OPTION EXERCISE':
                    option_instrument = event.option_event.option_instrument
                    option_avg_price = context.option_buy_holding[event.symbol].avg_unit_price
                    event.unit_price = option_instrument.strike_price + option_avg_price
                    context.call_exercise(
                        symbol=event.symbol,
                        quantity=int(event.quantity),
                        price=option_avg_price,
                        strike_price=option_instrument.strike_price,
                    )
                elif event.event_name in ('LIMIT BUY', 'MARKET BUY'):
                    assert event.unit_price is not None
                    context.limit_or_market_buy_stock(
                        quantity=int(event.quantity),
                        price=event.unit_price,
                    )
                elif event.event_name in ('LIMIT SELL', 'MARKET SELL'):
                    assert event.unit_price is not None
                    context.limit_or_market_sell_stock(
                        quantity=int(event.quantity),
                        price=event.unit_price,
                    )
                elif event.event_name in {
                    'FIG LEAF',
                    'LONG CALL SPREAD',
                    'LONG PUT SPREAD',
                    'SHORT PUT SPREAD',
                    'CUSTOM',
                    'IRON CONDOR',
                }:
                    for leg in event.option_order.legs:
                        quantity = int(event.option_order.processed_quantity) * leg.ratio_quantity
                        if leg.is_buy and leg.is_open:
                            context.buy_to_open(
                                symbol=leg.option_instrument.symbol,
                                quantity=quantity,
                                price=leg.price,
                                option_instrument=leg.option_instrument,
                            )
                        elif leg.is_buy and leg.is_close:
                            context.buy_to_close(
                                symbol=leg.option_instrument.symbol,
                                quantity=quantity,
                                price=leg.price,
                            )
                        elif leg.is_sell and leg.is_open:
                            context.sell_to_open(
                                symbol=leg.option_instrument.symbol,
                                quantity=quantity,
                                price=leg.price,
                                option_instrument=leg.option_instrument,
                            )
                        elif leg.is_sell and leg.is_close:
                            context.sell_to_close(
                                symbol=leg.option_instrument.symbol,
                                quantity=quantity,
                                price=leg.price,
                            )

                elif event.event_name in {
                    'FIG LEAF CLOSE',
                    'LONG CALL SPREAD CLOSE',
                    'LONG CALL CLOSE',
                    'LONG PUT CLOSE',
                    'LONG PUT SPREAD CLOSE',
                    'SHORT PUT SPREAD CLOSE',
                    'CUSTOM CLOSE',
                    'IRON CONDOR CLOSE',
                }:
                    for leg in event.option_order.legs:
                        if leg.side == 'buy':
                            context.buy_to_close(
                                symbol=leg.option_instrument.symbol,
                                quantity=int(event.option_order.processed_quantity) * leg.ratio_quantity,
                                price=leg.price,
                            )
                        else:
                            context.sell_to_close(
                                symbol=leg.option_instrument.symbol,
                                quantity=int(event.option_order.processed_quantity) * leg.ratio_quantity,
                                price=leg.price,
                            )
                else:
                    raise NotImplementedError(event.event_name)

                snapshot = context.take_snapshot()
                event.add_context(symbol_history_context_snapshot=snapshot)

        return events_by_symbol

    def _convert_stock_orders_to_symbol_history_events(
        self,
        stock_orders: List[StockOrder],
        events_by_symbol: DefaultDict[str, List[SymbolHistoryEvent]],
    ) -> None:
        for stock_order in stock_orders:
            if stock_order.instrument_id not in ALL_REVERSED:
                data = rhc.get_url(stock_order.instrument_url)
                for k, v in data.items():
                    print(f'{k}: {v}')

            symbol = ALL_REVERSED[stock_order.instrument_id]
            symbol_history_event = symbol_history_event_from_stock_order(
                symbol=symbol,
                stock_order=stock_order,
            )
            if symbol_history_event is not None:
                events_by_symbol[symbol].append(symbol_history_event)

    def _convert_option_orders_to_symbol_history_events(
        self,
        option_orders: List[OptionOrder],
        events_by_symbol: DefaultDict[str, List[SymbolHistoryEvent]],
    ) -> None:
        for option_order in option_orders:
            symbol = option_order.chain_symbol
            symbol_history_event = symbol_history_event_from_option_order(
                symbol=symbol,
                option_order=option_order,
            )
            if symbol_history_event is not None:
                events_by_symbol[symbol].append(symbol_history_event)

    def _convert_option_events_to_symbol_history_events(
        self,
        option_events: List[OptionEvent],
        events_by_symbol: DefaultDict[str, List[SymbolHistoryEvent]],
    ) -> None:
        for option_event in option_events:
            symbol = option_event.option_instrument.chain_symbol
            symbol_history_event = symbol_history_event_from_option_event(option_event=option_event)
            if symbol_history_event is not None:
                events_by_symbol[symbol].append(symbol_history_event)
