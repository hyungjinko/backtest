import numpy as np
import pandas as pd

def discounted_sum(cash, n, rf):
    value = []
    for i in range(n):
        value.append(cash / (1+rf)**i)
    return np.sum(value)
    

def backtest(ret, risky_invested, rebal):
    value = []
    for i in range(len(ret)):
        if i % rebal == 0:
            value.append(risky_invested * np.exp(ret.iloc[i:]).cumprod())
    
    value = pd.concat(value, axis=1).sum(axis=1)
    return value


def VaR(r, level, freq):
    if freq == 'D':
        win = 252
    elif freq == 'Y':
        win = 1
    
    return np.percentile(r, level) * win

def ES(r, level, freq):
    if freq == 'D':
        win = 252
    elif freq == 'Y':
        win = 1

    return r.loc[r < VaR(r,5,freq=freq)/win].mean() * win 

def Omega(ret, threshold, freq):
    if freq == 'D':
        threshold = (threshold+1)**np.sqrt(1/252)-1
    
    excess_ret = ret - threshold
    pos_sum = excess_ret.loc[excess_ret>0].sum()
    neg_sum = excess_ret.loc[excess_ret<0].sum()
    
    return - pos_sum / neg_sum
        
def MDD(price):
    Roll_Max = price.rolling(252, min_periods=1).max()
    Daily_Drawdown = price/Roll_Max - 1.0
    Max_Daily_Drawdown = Daily_Drawdown.rolling(252, min_periods=1).min()
    
    return Max_Daily_Drawdown.min()

def AvDD(price):
    Roll_Max = price.rolling(252, min_periods=1).max()
    Daily_Drawdown = price/Roll_Max - 1.0
    
    return Daily_Drawdown.mean()