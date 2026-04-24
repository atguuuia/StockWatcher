import akshare as ak
import pandas as pd
from datetime import datetime, timedelta

def get_realtime_quote(symbol: str):
    """获取实时行情（新浪源）"""
    try:
        df = ak.stock_zh_a_spot()
        row = df[df['代码'] == symbol]
        if row.empty:
            return None
        return {
            'code': symbol,
            'name': row['名称'].iloc[0],
            'price': row['最新价'].iloc[0],
            'change': row['涨跌幅'].iloc[0],
            'volume': row['成交量'].iloc[0],
            'amount': row['成交额'].iloc[0],
        }
    except Exception as e:
        print(f"实时行情失败: {e}")
        return None

def get_history(symbol: str, days=60):
    """获取历史日线（新浪源）"""
    try:
        df = ak.stock_zh_a_daily(symbol=symbol, adjust='qfq')
        df = df.sort_values('date')
        cutoff = df['date'].max() - pd.Timedelta(days=days)
        df = df[df['date'] >= cutoff]
        return df[['date', 'open', 'high', 'low', 'close', 'volume']].to_dict('records')
    except Exception as e:
        print(f"历史数据失败: {e}")
        return []
