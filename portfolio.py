import quantstats as qs
import pandas as pd

# extend pandas functionality with metrics, etc.
qs.extend_pandas()

# fetch the daily returns for a stock

price_alpha_50 = pd.read_csv('./alpha_50.csv',encoding='utf8')
price_alpha_100 = pd.read_csv('./alpha_100.csv',encoding='utf8')
price_alpha_200 = pd.read_csv('./alpha_200.csv',encoding='utf8')
price_alpha_500 = pd.read_csv('./alpha_500.csv',encoding='utf8')




def calc_portfolio(price,col,strategy):
    price['Close'] = price[col].pct_change()
    price['Date'] = pd.to_datetime(price['Date'],format='%d/%m/%Y')
    price= price.set_index('Date')
    stock=price['Close']

    qs.reports.html(stock,title=f"Portfolio Analysis {strategy}",output=f'output/full_report_{strategy}.html')


def calc_stock_value(price,col,newCol):
    price[newCol] = price[col].pct_change()
    price['Date'] = pd.to_datetime(price['Date'],format='%d/%m/%Y')
    price= price.set_index('Date')
    stock=price[newCol]

    return stock.squeeze() 
    

def calc_portfolio_comparison(price,col1,col2,strategy):
   stock_alpha = calc_stock_value(price,col1,'Close')
   stock_nifty = calc_stock_value(price,col2,'Close')

   qs.reports.html(stock_alpha,stock_nifty,title=f"Portfolio Analysis {strategy}",output=f'output/full_report_{strategy}.html')

# calc_portfolio(price_alpha_50,'Alpha_50_Close','alpha_50')
# calc_portfolio(price_alpha_100,'Alpha_100_Close','alpha_100')
# calc_portfolio(price_alpha_200,'Alpha_200_Close','alpha_200')
# calc_portfolio(price_alpha_500,'Alpha_500_Close','alpha_500')
    
calc_portfolio_comparison(price_alpha_50,'Alpha_50_Close','Nifty_50_Close','alpha50_vs_nifty50')
calc_portfolio_comparison(price_alpha_100,'Alpha_100_Close','Nifty_100_Close','alpha100_vs_nifty100')
calc_portfolio_comparison(price_alpha_200,'Alpha_200_Close','Nifty_200_Close','alpha200_vs_nifty200')
calc_portfolio_comparison(price_alpha_500,'Alpha_500_Close','Nifty_500_Close','alpha500_vs_nifty500')


# print(f"My Stocks Data \n",stock)
# qs.plots.daily_returns(stock,benchmark="None",ylabel="Daily Returns",savefig ='output/new_daily_returns.png')
# qs.reports.html(stock,title="Portfolio Analysis",output='output/full_report.html')