# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.async_support.binance import binance


class binancecoinm(binance):

    def describe(self):
        return self.deep_extend(super(binancecoinm, self).describe(), {
            'id': 'binancecoinm',
            'name': 'Binance COIN-M',
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/117738721-668c8d80-b205-11eb-8c49-3fad84c4a07f.jpg',
            },
            'options': {
                'defaultType': 'delivery',
            },
            # https://www.binance.com/en/fee/deliveryFee
            'fees': {
                'trading': {
                    'tierBased': True,
                    'percentage': True,
                    'taker': self.parse_number('0.000500'),
                    'maker': self.parse_number('0.000100'),
                    'tiers': {
                        'taker': [
                            [self.parse_number('0'), self.parse_number('0.000500')],
                            [self.parse_number('250'), self.parse_number('0.000450')],
                            [self.parse_number('2500'), self.parse_number('0.000400')],
                            [self.parse_number('7500'), self.parse_number('0.000300')],
                            [self.parse_number('22500'), self.parse_number('0.000250')],
                            [self.parse_number('50000'), self.parse_number('0.000240')],
                            [self.parse_number('100000'), self.parse_number('0.000240')],
                            [self.parse_number('200000'), self.parse_number('0.000240')],
                            [self.parse_number('400000'), self.parse_number('0.000240')],
                            [self.parse_number('750000'), self.parse_number('0.000240')],
                        ],
                        'maker': [
                            [self.parse_number('0'), self.parse_number('0.000100')],
                            [self.parse_number('250'), self.parse_number('0.000080')],
                            [self.parse_number('2500'), self.parse_number('0.000050')],
                            [self.parse_number('7500'), self.parse_number('0.0000030')],
                            [self.parse_number('22500'), self.parse_number('0')],
                            [self.parse_number('50000'), self.parse_number('-0.000050')],
                            [self.parse_number('100000'), self.parse_number('-0.000060')],
                            [self.parse_number('200000'), self.parse_number('-0.000070')],
                            [self.parse_number('400000'), self.parse_number('-0.000080')],
                            [self.parse_number('750000'), self.parse_number('-0.000090')],
                        ],
                    },
                },
            },
        })

    async def fetch_trading_fees(self, params={}):
        await self.load_markets()
        marketSymbols = list(self.markets.keys())
        fees = {}
        accountInfo = await self.dapiPrivateGetAccount(params)
        #
        # {
        #      "canDeposit": True,
        #      "canTrade": True,
        #      "canWithdraw": True,
        #      "feeTier": 2,
        #      "updateTime": 0
        #      ...
        #  }
        #
        feeTier = self.safe_integer(accountInfo, 'feeTier')
        feeTiers = self.fees['trading']['tiers']
        maker = feeTiers['maker'][feeTier][1]
        taker = feeTiers['taker'][feeTier][1]
        for i in range(0, len(marketSymbols)):
            symbol = marketSymbols[i]
            fees[symbol] = {
                'info': {
                    'feeTier': feeTier,
                },
                'symbol': symbol,
                'maker': maker,
                'taker': taker,
            }
        return fees
