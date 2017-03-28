# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 21:20:06 2017

@author: xuke2
"""

import code_api

class Search():
    def __init__(self, form):
        self.datas= code_api.Code()
        if form.stockId.data:
            self.stockId=str(form.stockId.data)
        else:
            self.compName=str(form.compName.data)
            self.stockId=self.datas.getCode('%s'%self.compName)
        self.info=self.datas.getDataSet(self.stockId)