# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 20:38:19 2017

@author: xuke2
"""

from flask_wtf import Form
from wtforms import StringField, IntegerField, DateField, SelectField, SelectMultipleField      
from wtforms.validators import DataRequired

class singleStockForm(Form):
    choices=[('na', '无'),('random_strategy','随机'),('smacross_strategy', 'SMA交叉'),('sma','SMA策略'),('bband_strategy','布林格区间'),('donchain_strategy','唐奇安通道'),('mv_strategy','MV')]
    stockId = StringField('stockId', validators=[DataRequired()])
    initMoney = IntegerField('initMoney', validators=[DataRequired()])
    startDate = DateField('startDate', format = '%Y-%m-%d')
    endDate = DateField('endDate', format = '%Y-%m-%d')
    strategy = SelectField('strategy', choices=choices, validators=[DataRequired()], default=['na'])
    strategies = SelectMultipleField('strategy', choices=choices, validators=[DataRequired()], default=['na'])

    
    randPerct= IntegerField('randPerct', default=30)
    smaShort= IntegerField('smaShort', default=5)
    smaLong = IntegerField('smaLong', default=20)
    smaFirst= IntegerField('smaFirst', default=5)
    smaSecond= IntegerField('smaSecond', default=10)
    smaThird= IntegerField('smaThird', default=20)
    
    donChianShort = IntegerField('donChianShort', default=10)
    donChianLong = IntegerField('donChianLong', default=20)
    bbandDay = IntegerField('bbandDay', default=20)
    
    mvDay = IntegerField('mvDay', default=20)
    
class stockInfoForm(Form):
    stockId = StringField('stockId', validators=[DataRequired()])
    compName = StringField('compName')
    