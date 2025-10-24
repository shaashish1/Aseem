import ta
import pandas_ta as pta
import pandas as pd

close = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
high = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
low = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]

sma = ta.trend.SMAIndicator(pd.Series(close),14,False).sma_indicator().iloc[-1]
print(sma)

supertrend = pd.DataFrame(pta.supertrend(pd.Series(high), pd.Series(low), pd.Series(close),10,1))
sup = supertrend.iloc[:,0]
sup2 = sup.iloc[-1]
print(sup2)


#Answers: 13.5 and 18