# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 12:15:25 2017

@author: xuke2
"""
import sys
project_dir = '/home/pi/flaskapp/flaskapp_msx'

sys.path.insert(0, project_dir)

from flask import Flask, render_template, Response, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from main import inputForms
from main import singleStockReq
from main import stockInfoSearch
app = Flask(__name__)
basedir = '/'
bootstrap = Bootstrap(app)
app.secret_key = 'myverylongsecretkey'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/singleStock',methods=['GET', 'POST'])
def singleStock():
    form=inputForms.singleStockForm()
    if request.method == 'POST':
        ctrl=singleStockReq.singleStockReq(form)
        # 准备测试条件和结果表格所需数据
        test_assumptions=[form.stockId.data, form.strategy.data]
#        #test
#        flash(ctrl.resultKPIs())
#        return redirect(url_for('test'))

        templateData = {
        'test_assumptions': test_assumptions,
        'kpis_display': ctrl.resultKPIs(),
        'kdata': ctrl.kdata(),
        'trades_all': ctrl.tradesInfo()[0],
        'trades_enter': ctrl.tradesInfo()[1],
        'trades_exit': ctrl.tradesInfo()[2]
                }
        return render_template('singleStockResults.html', **templateData)
#        except:
#            error='cannot finish simulation test for this stock!'
#            return redirect('test.html', error=error)
    return render_template('singleStock.html', form=form)

@app.route('/stockInfo',methods=['GET', 'POST'])
def stockInfo():
    form=inputForms.stockInfoForm()
    if request.method == 'POST':
        ctrl=stockInfoSearch.Search(form)
        templateData = {
        'stockInfo': ctrl.info
                }
        return render_template('stockInfoSearchResults.html', **templateData)
    return render_template('stockInfo.html', form=form)


@app.route('/test')
def test():
    return render_template('test.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)