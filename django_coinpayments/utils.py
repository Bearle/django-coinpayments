from django.conf import settings

BCH = "BCH"
BLK = "BLK"
BTC = "BTC"
DASH = "DASH"
DCR = "DCR"
DGB = "DGB"
DOGE = "DOGE"
ETC = "ETC"
ETH = "ETH"
EXP = "EXP"
GAME = "GAME"
LSK = "LSK"
LTC = "LTC"
MAID = "MAID"
NAV = "NAV"
NEO = "NEO"
POT = "POT"
SBD = "SBD"
STEEM = "STEEM"
STRAT = "STRAT"
VTC = "VTC"
XEM = "XEM"
XMR = "XMR"
XRP = "XRP"
XVG = "XVG"
CURRENCY_CHOICES = (
    (BCH, 'Bitcoin Cash'),
    (BLK, 'BlackCoin'),
    (BTC, 'Bitcoin'),
    (DASH, 'Dash'),
    (DCR, 'Decred'),
    (DGB, 'DigiByte'),
    (DOGE, 'Dogecoin'),
    (ETC, 'Ether Classic'),
    (ETH, 'Ether'),
    (EXP, 'Expanse'),
    (GAME, 'GameCredits'),
    (LSK, 'LISK'),
    (LTC, 'Litecoin'),
    (MAID, 'MaidSafeCoin'),
    (NAV, 'NAV Coin'),
    (NEO, 'NEO'),
    (POT, 'PotCoin'),
    (SBD, 'Steem Dollars'),
    (STEEM, 'STEEM'),
    (STRAT, 'Stratis'),
    (VTC, 'Vertcoin'),
    (XEM, 'NEM'),
    (XMR, 'Monero'),
    (XRP, 'Ripple'),
    (XVG, 'VERGE'),
)


def get_coins_list():
    coins = getattr(settings, 'COINPAYMENTS_ACCEPTED_COINS', None)
    if not coins:
        coins = CURRENCY_CHOICES
    return coins
