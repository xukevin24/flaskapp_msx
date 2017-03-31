# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 00:14:30 2017

@author: xuke2
"""
from strategy import istrategy as istrategy
from strategy import random_strategy as random_strategy
from strategy import donchain_strategy as donchain_strategy
from strategy import bband_strategy as bband_strategy
from strategy import smacross_strategy as smacross_strategy
from strategy import test_strategy as test_strategy
from strategy import time_strategy
from strategy import ma_strategy
from strategy import mv_strategy

from trade import trade as Trade
import data_api
from simulate import simulate

class singleStockReq:
    def __init__(self, form):
        self.datas= data_api.KData()
        
        if not form.startDate.data:
            self.datas.init_data_from_db(str(form.stockId.data), index=False, end=str(form.endDate.data))
        else:
            self.datas.init_data_from_db(str(form.stockId.data), index=False, start=str(form.startDate.data), end=str(form.endDate.data))
        #test
#        flash(datas.datas[0])
#        return redirect(url_for('test'))
        #and form.validate_on_submit()
        if (form.strategy.data !='na') and (form.strategies.data==['na']):
            if form.strategy.data=='random_strategy':
                perct=form.randPerct.data
                s=random_strategy.Strategy(perct)
            if form.strategy.data=='smacross_strategy':
                shortD=form.smaShort.data
                longD=form.smaLong.data
                s=smacross_strategy.SMACrossStrategy(shortD,longD)
            if form.strategy.data=='bband_strategy':
                s=bband_strategy.BBandStrategy(form.bbandDay.data)
            if form.strategy.data=='donchain_strategy':
                shortD=form.donChianShort.data
                longD=form.donChianLong.data
                s=donchain_strategy.Strategy(longD,shortD)
            if form.strategy.data=='sma':
                Narr=[form.smaFirst.data, form.smaSecond.data, form.smaThird.data]
                s=ma_strategy.Strategy(Narr)
            if form.strategy.data == 'mv_strategy':
                mvDay=form.mvDay.data
                s=mv_strategy.Strategy(mvDay)
            self.account = simulate(self.datas, s, Trade.Trade)
        if (form.strategy.data =='na') and (form.strategies.data!=['na']):
            self.account=[]
            self.strategies=[]
            for strategy in form.strategies.data:
                if strategy=='random_strategy':
                    perct=form.randPerct.data
                    s=random_strategy.Strategy(perct)
                if strategy=='smacross_strategy':
                    shortD=form.smaShort.data
                    longD=form.smaLong.data
                    s=smacross_strategy.SMACrossStrategy(shortD,longD)
                if strategy=='bband_strategy':
                    s=bband_strategy.BBandStrategy(form.bbandDay.data)
                if strategy=='donchain_strategy':
                    shortD=form.donChianShort.data
                    longD=form.donChianLong.data
                    s=donchain_strategy.Strategy(longD,shortD)
                if strategy=='sma':
                    Narr=[form.smaFirst.data, form.smaSecond.data, form.smaThird.data]
                    s=ma_strategy.Strategy(Narr)
                if strategy == 'mv_strategy':
                    mvDay=form.mvDay.data
                    s=mv_strategy.Strategy(mvDay)
                self.account.append(simulate(self.datas, s, Trade.Trade))
                self.strategies.append(strategy)
    
    # 返回测试结果的重要 KPIs      
    def resultKPIs(self):
        if type(self.account) is not list:
            return [self.account.init_cash, self.account.cash, self.account.statistics.profit, self.account.statistics.totalProfit, self.account.statistics.totalLoss, 
                            self.account.statistics.profitRatio, self.account.statistics.num, self.account.statistics.fee, self.account.statistics.succRatio, self.account.statistics.profitRatio_single, self.account.statistics.profitRatio_compound]
        else:
            kpisMulti=[]
            for i, account in enumerate(self.account):
                kpisMulti.append([self.strategies[i], account.init_cash, account.cash, account.statistics.profit, account.statistics.totalProfit, account.statistics.totalLoss, 
                            account.statistics.profitRatio, account.statistics.num, account.statistics.fee, account.statistics.succRatio, account.statistics.profitRatio_single, account.statistics.profitRatio_compound])
            return kpisMulti
        
    # 返回K线数据
    def kdata(self):        
        kdata=[]
        for data in self.datas.datas:
            dt=[data[0], data[1], data[2], data[3], data[4], data[5]]
            kdata.append(dt)
        return kdata
    
    # 返回交易数据包括 【入场日期，入场价格，出场日期，出场价格，利润】
    def tradesInfo(self):
        trades_all=[]
        trades_enter=[]
        trades_exit=[]
        for i, trade in enumerate(self.account.trades):
            td_enter=[trade.enter_date, trade.enter_price]
            td_exit=[trade.exit_date, trade.exit_price]
            td_all=[i+1, trade.enter_date, trade.enter_price,trade.exit_date, trade.exit_price, int(trade.profit)]
            trades_enter.append(td_enter)
            trades_exit.append(td_exit)
            trades_all.append(td_all)
        return [trades_all, trades_enter, trades_exit]
        