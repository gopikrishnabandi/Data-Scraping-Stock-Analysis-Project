import numpy as np
import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import seaborn as sns
import time


class StockAnalysis:

    def __init__(self):
        pass

    def closing_prices(self):
        # path=os.getcwd()
        # print(path)
        # csv_files=glob.glob(os.path.join(path,"*.csv"))
        csv_files = glob.glob("*.csv")
        df_dict={}
        for file in csv_files:
            stock_name=file.replace('.csv','').upper()
            df_dict[stock_name] = pd.read_csv(file)
            df_dict[stock_name]['Date']=df_dict[stock_name]['Date'].astype('datetime64[ns]')
            df_dict[stock_name] = df_dict[stock_name].rename(columns={'Close/Last': 'Close'})
            df_dict[stock_name]['Close'] = df_dict[stock_name]['Close'].astype('float')
            df_dict[stock_name]['Volume'] = df_dict[stock_name]['Volume'].astype('int64')
            df_dict[stock_name]['Open'] = df_dict[stock_name]['Open'].astype('float')
            df_dict[stock_name]['High'] = df_dict[stock_name]['High'].astype('float')
            df_dict[stock_name]['Low'] = df_dict[stock_name]['Low'].astype('float')
            # print(df.dtypes)
            # print(df.info())
            df_dict[stock_name]=df_dict[stock_name].set_index('Date')
            # not using plt.figure(figsize=(20,10)) as it will create new plot for each stock in loop , we want only one plot
            plt.title('Closing Prices Trend for stocks', fontsize=16, fontname="Times New Roman")
            plt.xlabel('Date', fontsize=14, fontname="Times New Roman")
            plt.ylabel('Closing Price', fontsize=14, fontname="Times New Roman")
            # plt.xticks(rotation="vertical")
            plt.xticks(fontsize=14, fontname="Times New Roman")
            plt.yticks(fontsize=14, fontname="Times New Roman")
            df_dict[stock_name]['Close'].plot(figsize=(15,10))
            plt.legend(df_dict.keys())


        plt.savefig('Closing Prices')
        plt.close()


    def close_vs_moving_average(self):
        csv_files = glob.glob("*.csv")
        days = int(input("Enter first set of Moving Average No of Days to plot for :"))
        days2 = int(input("Enter second set of  Moving Average No of Days to plot for :"))
        days3 = int(input("Enter third set of  Moving Average No of Days to plot for :"))
        for file in csv_files:
            stock_name = file.replace('.csv', '').upper()
            df=pd.read_csv(file)
            df=df.rename(columns={'Close/Last':'Close'})
            df['Date'] = df['Date'].astype('datetime64[ns]')
            df['Close'] = df['Close'].astype('float')
            df['Volume'] = df['Volume'].astype('int64')
            df['Open'] = df['Open'].astype('float')
            df['High'] = df['High'].astype('float')
            df['Low'] = df['Low'].astype('float')
            df=df.set_index('Date')
            df[str(days)+' day moving_avg']=df['Close'].rolling(days).mean()
            df[str(days2) + ' day moving_avg'] = df['Close'].rolling(days2).mean()
            df[str(days3) + ' day moving_avg'] = df['Close'].rolling(days3).mean()
            df[['Close',str(days)+' day moving_avg',str(days2) + ' day moving_avg',str(days3) + ' day moving_avg']].plot(legend=True,figsize=(15,10))
            plt.xlabel('Date')
            plt.ylabel('Closing Price')
            title="Closing Price and Moving Average of "+str(days)+","+str(days2)+","+str(days3)+" days for "+str(stock_name)
            plt.title(title)
            filename = 'ClosingVsMoving_' + str(days) +"_"+str(days2)+"_"+str(days3)+"_" +str(stock_name)
            plt.savefig(filename)
            plt.close()

    def daily_returns(self):

        # daily_rets = df.copy()
        # print(df[1:])
        # print(df[:-1])
        # daily_rets[1:] = (df[1:] / df[:-1].values) - 1
        # print(daily_rets)
        # daily_rets.iloc[0] = 0
        # daily_rets = daily_rets[1:]
        # print(daily_rets['Close'])

        csv_files = glob.glob("*.csv")
        df_dict={}
        for file in csv_files:
            stock_name=file.replace(".csv","").upper()
            df_dict[stock_name]=pd.read_csv(file)
            df_dict[stock_name]['Date']=df_dict[stock_name]['Date'].astype('datetime64[ns]')
            df_dict[stock_name] = df_dict[stock_name].rename(columns={"Close/Last": "Close"})
            df_dict[stock_name]['Close'] = df_dict[stock_name]['Close'].astype('float')
            df_dict[stock_name]['Volume'] = df_dict[stock_name]['Volume'].astype('int64')
            df_dict[stock_name]['Open'] = df_dict[stock_name]['Open'].astype('float')
            df_dict[stock_name]['High'] = df_dict[stock_name]['High'].astype('float')
            df_dict[stock_name]['Low'] = df_dict[stock_name]['Low'].astype('float')
            df_dict[stock_name]=df_dict[stock_name].set_index('Date')
            df_dict[stock_name]['daily_return'] = df_dict[stock_name]['Close'].pct_change()
            df_dict[stock_name]['daily_return'].plot(figsize=(20,10))
            # we can also plot distribution of daily returns using sns.distplot
            #plt.ylabel('Probability Density Value')
            # sns.distplot(df_dict['daily_return'].dropna(), bins = 100, color = 'red') #
            plt.xlabel('Date')
            plt.ylabel('Daily Returns')
            plt.title('Daily Returns for stocks')

        plt.legend(df_dict.keys())
        plt.savefig('Daily Returns of stocks')

    def correlation(self):
        csv_files = glob.glob("*.csv")
        df1 = pd.DataFrame()
        for file in csv_files:
            stock_name = file.replace('.csv', '').upper()
            df = pd.read_csv(file)
            df = df.drop(columns={'Volume', 'Open', 'High', 'Low'})
            df = df.rename(columns={'Close/Last': 'Close'})
            df['Date'] = df['Date'].astype('datetime64[ns]')
            df = df.set_index('Date')
            df1=df1.join(df,how="outer")
            df2=df1.merge(df,how="outer",left_index=True,right_index=True)

        print(df1)
        print(df2)
        # corr = (df1.dropna()).corr()
        # sns.heatmap(corr, annot=True)
        # plt.show()




if __name__ == "__main__":
    obj=StockAnalysis()
    obj.closing_prices()
    obj.close_vs_moving_average()
    obj.daily_returns()
    obj.correlation()
