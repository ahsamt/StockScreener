import pandas as pd

def moving_average(series, window_size):
    
    windows = series.rolling(window_size)
    moving_avgs = windows.mean()
    return moving_avgs