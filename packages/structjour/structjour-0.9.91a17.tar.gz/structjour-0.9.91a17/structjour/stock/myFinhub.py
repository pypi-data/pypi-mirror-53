APIKEY = 'bm9spbnrh5rb24oaaehg'


example = 'https://finnhub.io/api/v1/stock/candle?symbol=AAPL&resolution=1&count=200&token=bm9spbnrh5rb24oaaehg'


def getApiKey():
    return APIKEY

def getLimits():
    limits= ('Most endpoints will have a limit of 60 requests per minute per api key. However,\n'
             '//scan endpoint have a limit of 10 requests per minute. If your limit is exceeded,\n'
             'you will receive a response with status code 429.\n\n'
             'Quote from docs-- see skeptical on my face')

def getParams(symbol, interfal, numCandles=None, start=None):
    params = {}
    

def getFh_intraday(symbol, start=None, end=None, minutes=5):
    base = 'https://finnhub.io/api/v1/stock/candle?'



