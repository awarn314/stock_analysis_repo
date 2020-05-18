import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib
import os
from os import listdir
from os.path import isfile, join
from builtins import any as b_any
import yfinance as yf
yf.pdr_override()

stock_path='Stock_Data'
stock_plots='Stock_Plots'

fs= 20

if not os.path.exists(stock_plots):
    os.makedirs(stock_plots)
  
done_plots = [f for f in listdir(stock_plots) if isfile(join(stock_plots, f))]
Doneticks_plots=[i.split('.png', 1)[0] for i in done_plots]


Files_for_plotting= listdir(stock_path)
ticks=[]
companies=[]
lengths=[]
ups=[]
downs=[]
# for ff in Files_for_plotting:
#     t_c=ff.split('.csv', 1)[0]
#     tick=t_c.split('__', 1)[0]
#     company=t_c.split('__', 1)[1]
    
#     check=tick + '_'+company
    
#     csvname = stock_path+'/'+ff
#     df_data=pd.read_csv(csvname, skiprows=range(1, 15), encoding="ISO-8859-1")
    
#     if len(df_data)>10:
#         RSI_end=df_data['RSI'].iloc[-1]
#         v_end=df_data['Close'].iloc[-1]
#         v_ini=df_data['Close'].iloc[0]
#         if  (v_end > 1.18*v_ini) and v_end>1 and v_end<1000 and RSI_end<40:
#             ticks.append(tick)
#             companies.append(company)
#             lengths.append(len(df_data))
#             ups.append(len(df_data[(df_data['RSI']>=70)]))
#             downs.append(len(df_data[(df_data['RSI']<=30)]))
        
# rsi_df=pd.DataFrame()
# rsi_df['Tick']=ticks
# rsi_df['Company']=companies
# rsi_df['Total']=lengths
# rsi_df['Above 70']=ups
# rsi_df['Below 30']=downs

# rsi_df1=rsi_df[rsi_df['Above 70']>0]
# rsi_df2=rsi_df1[rsi_df1['Below 30']>0]
# rsi_df3=rsi_df2[rsi_df2['Total']>50]

     
Files_for_plotting= listdir(stock_path)
Files_for_plotting = Files_for_plotting[1:3]
for ff in Files_for_plotting:
    t_c=ff.split('.csv', 1)[0]
    tick=t_c.split('__', 1)[0]
    company=t_c.split('__', 1)[1]

    check=tick + '_'+company
    if not b_any(check in x for x in Doneticks_plots):
    
        csvname = stock_path+'/'+ff
        df_data=pd.read_csv(csvname, encoding="ISO-8859-1")
        x1=df_data['Count'].reset_index()
        x1=x1+(1260-np.max(x1))
        y1=df_data['Close'].reset_index()
        x1=x1.drop(['index'], axis=1)
        y1=y1.drop(['index'], axis=1)

        
        if len(x1)>30:
            x2=x1.tail(520)
            x3=x1.tail(260)
            x4=x1.tail(195)
            x5=x1.tail(130)
            x6=x1.tail(65)
            
            y2=y1.tail(520)
            y3=y1.tail(260)
            y4=y1.tail(195)
            y5=y1.tail(130)
            y6=y1.tail(65)
            y11=float(.98*np.min(y1))
            y22=float(1.02*np.max(y1))
            
            fname=stock_plots + '/'+ tick + '_'+company+'.png'
            fig = plt.figure()
            
            if x1.shape[0]>700:
                plt.subplot(212)                        
                matplotlib.rcParams.update({'font.size': fs})
                plt.plot(x1, y1, 'r',linewidth=3.0)
                plt.axvline(x=252, color='k',linewidth=3.0)
                plt.axvline(x=504, color='k',linewidth=3.0)
                plt.axvline(x=756, color='k',linewidth=3.0)
                plt.axvline(x=1008, color='k',linewidth=3.0)
                plt.xlim(0,1260)
                plt.ylim(y11,y22)
                plt.title('5 yr')
                plt.grid(True)
                plt.show()
                
            if x2.shape[0]>400:
                if x1.shape[0]<=700:
                    plt.subplot(212)
                else:
                    plt.subplot(244)                        
                matplotlib.rcParams.update({'font.size': fs})
                plt.plot(x2, y2, 'r',linewidth=3.0)
                plt.axvline(x=1008, color='k',linewidth=3.0)
                plt.xlim(750,1260)
                plt.ylim(y11,y22)
                plt.title('2 yr')
                plt.grid(True)
            
            if x3.shape[0]>200:
                plt.subplot(243)                        
                matplotlib.rcParams.update({'font.size': fs})
                plt.plot(x3, y3, 'r',linewidth=3.0)
                plt.axvline(x=1071, color='k',linewidth=3.0)
                plt.axvline(x=1134, color='k',linewidth=3.0)
                plt.axvline(x=1197, color='k',linewidth=3.0)
                plt.title('1 yr')
                plt.xlim(960,1260)
                plt.ylim(y11,y22)
                plt.grid(True)
                
            if x5.shape[0]>100:
                plt.subplot(242)                        
                matplotlib.rcParams.update({'font.size': fs})
                plt.plot(x5, y5, 'r',linewidth=3.0)
                plt.axvline(x=1197, color='k',linewidth=3.0)
                plt.xlim(1100,1260)
                plt.ylim(y11,y22)
                plt.title('6 month')
                plt.grid(True)
            
            if x6.shape[0]>50:
                plt.subplot(241)                        
                matplotlib.rcParams.update({'font.size': fs})
                plt.plot(x6, y6, 'r',linewidth=3.0)
                plt.xlim(1180,1260)
                plt.ylim(y11,y22)
                plt.title('3 month')
                plt.grid(True)
            fig.suptitle(tick + '  ' + company)
            fig.set_size_inches(30, 12)
            plt.savefig(fname)
            plt.close(fig)     