---
layout:     post
title:      相对强弱指数的算法交易策略 
subtitle:   使用Python对相对强弱指数策略进行模拟交易
date:       2018-02-27
author:     Sylvia
header-img: img/post-bg-ios9-web.jpg
catalog: true
tags:
    - Python
    - Trading
---

##### 1. 算法交易
读书的时候上过一门算法交易的课程，讲的就是如何使用各种算法进行股票以及期货(指)的投资。投资算法五花八门，在真实的交易中一般需要参考各种因素选择一种或多种投资策略进行交易。然而这还远远不够，记得那门课的教授当时说过"In Chinese stock market, monkey would earn more than a professional trader（在中国股票市场，猴子有可能比专业交易员赚的还多哦）"，所以说，本文仅供娱乐，无任何投资参考价值。  
在本文中，我使用搜狐的接口获取一定时间内特定股票的数据，[API地址](http://q.stock.sohu.com/hisHq?code=cn_000001&start=20180223&end=20180224&stat=1&order=D&period=d&callback=historySearchHandler&rt=jsonp)，源代码地址： [https://github.com/missweetcxx/algo_trading](https://github.com/missweetcxx/algo_trading)。

##### 2. 相对强弱指数
相对强弱指数（[Relative Strength Index](https://en.wikipedia.org/wiki/Relative_strength_index)，以下简称RSI）最初由经济学家J.Welles Wilder在上世纪七十年代提出。作为计量超买超卖状况的“警示符”，RSI在证券投资领域十分常用，下面就和大家介绍一下RSI。   
RSI主要衡量某股(指)了近期涨幅与跌幅的比例，它的计算公式如下：

```
RSI = 100 - 100/(1+RS)
其中，RS = 近n天收盘价上涨的指数移动平均/近n天收盘价下跌的指数移动平均
```
由于指数移动平均的计算比较麻烦，而采用简单移动平均(SMA)方法的卡特勒相对强弱指数（Culter's RSI）由于计算结果与其差别并不显著，所以我们采用后者来进行分析，即 `RS = SMA(up_trend)/SMA(down_trend)`。

举个栗子吧，某股票在14天内的价格趋势如下：
![ ](https://upload-images.jianshu.io/upload_images/7208479-48bf673db7f00e48.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

1.首先将上涨的数据累加再除天数14，得到16/14=1.143；  
2.再将下跌的数据累加除以天数14，得到23/14=1.643；  
3.那么，RS=1.143/1.1643=0.696,  
4.RSI = 100 - 100/(1+0.696)=41.038。  

所以这14天的相对强弱指数就是41.038。

上代码(price_list为所选区间内的收盘价集合)： 

```
rise_sum, down_sum = 0, 0
for i in range(len(price_list) - 1):
    balance = price_list[i + 1] - price_list[i]
    if balance > 0:
        rise_sum += balance
    else:
        down_sum -= balance
if (rise_sum + down_sum) != 0:
    rsi = 100 * rise_sum / (rise_sum + down_sum)
else:
    rsi = 50    # 防止除数为零
```

##### 3. 交易策略
J.Welles Wilder采用14天RSI提出以下交易策略：当RSI低于30时，该股票处于“超卖状态”，此时是买入的好时机；而当RSI高于70时，该股处于“超买状态”，此时应当酌情卖出。  
根据这一交易策略，我直接将沪指(000001.SS)这只股票作为实验对象，交易跨度为2018年2月23日的前100个交易日至2018年2月23日，当其14日RSI高于70时卖出100股，低于30时买入100股（均以收盘价为准），在不考虑手续费以及平仓的情况下，我的收益是1498元。   

我打算改进一下我的交易策略，首先在牛市和熊市中，应该使用不同的交易策略；其次，70和30的界限太过单一，我觉得可以根据RSI的值确定买入以及卖出的量，比如30买入100股，20买入150股，40买入50股...  

首先，该如何确定是牛市还是熊市呢，网上众说纷纭，而我的策略是得出14日以及200日沪指的简单移动平均（SMA），若SMA(5)>SMA(200)则是牛市，反之则是熊市，可能有些不太精准，暂且这样吧。  

其次，要定下卖出（买入）的量与RSI的公式: 
```volume = int((RSI-50)/20) * basic_volume * alpha```   
其中basic_volume是用户输入的基本交易单位（这里我输入100），alpha是市场系数，暂且定为熊市卖0.9买1，牛市卖1买0.9，贴代码（其中MarketStatus即为牛熊市）：

```
def rsi_strategy_executor(date, volume):
    market_status = StockMarket.market_status(date)
    rsi = StockIndex.rsi(date)
    grades = int((rsi - 50) / 10)/2
    if market_status == MarketStatus.BEAR:
        if grades >= 0:
            TradeUtil.sell(volume * grades * 0.9, date)
        else:
            TradeUtil.buy(volume * grades, date)
    elif market_status == MarketStatus.BULL:
        if grades >= 0:
            TradeUtil.sell(volume * grades, date)
        else:
            TradeUtil.buy(volume * grades * 0.9, date)
```
再次计算发现收益为2562，居然赚了，简直不敢相信。

##### 4. 开挂的RSI2
2008年11月，恰逢经济危机，而正在此时Larry Connors提出了RSI2的观点，并通过历史数据验证RSI2比RSI更加有效，并且更加适用于高频交易。Larry Connors的交易策略主要为以下四步：  

1. 确定牛熊市  
在这里，Larry Connors将价格高于SMA(200)的时刻判断为牛市，低于SMA(200)的时刻判断为熊市，这里似乎不应称为牛熊市，但我也想不出其它更贴切的词了。

2. 确定买入、卖出时机  
Connors认为RSI在[0,10]的区间是非常好的买入机会，且越低收益越大；而[90,100]的区间则应当沽空，且越高持仓的风险越大。

3. 收盘价 or 开盘价？  
对于股市中的算法交易，一般由两种操作方式，在收盘前买入/卖出，或是在开盘后集合竞价后买入/卖出，这两种方式更有利弊，在这里我选择第一种操作方式，且不考虑交易确认的时间。

4. 设定’退出点‘  
股市有风险，入市需谨慎。设定’退出点‘才能有效把控风险，从而止损。Connors认为当股价高于SMA(5)时多头看跌，应及时停止买入，而当股价低于SMA(5)时空头看跌，及时停止卖出。

根据Connors的RSI2交易策略，我尝试着对100天的沪指进行了模拟交易，其中我还是根据RSI2的值以及市场形势定了购买量。牛市alpha为1，熊市alpha为0.9。
```volume = （(RSI2 - 90) / 10 + 1）* basic_volume * alpha```

贴代码，其中MarketCondition即为上述‘退出点’：

```
def rsi2_strategy_executor(date, volume):
    market_status = StockMarket.connors_market_status(date)
    exit_point = StockMarket.connors_exit_condition(date)
    rsi_2 = StockIndex.rsi_2(date)

    if rsi_2 > 90 and exit_point != MarketCondition.LONG:
        alpha = 0.9 if market_status == MarketStatus.BULL else 1
        grade = (rsi_2 - 90) / 10 + 1
        TradeUtil.sell(volume * grade * alpha, date)
    elif rsi_2 < 10 and exit_point != MarketCondition.SHORT:
        alpha = 1 if market_status == MarketStatus.BULL else 0.9
        grade = (10 - rsi_2) / 10 + 1
        TradeUtil.buy(volume * grade * alpha, date)
```

很无奈地发现，居然没有赚。不知道是不是因为界限设的太高，调整了一下代码继续操作，当RSI2在[80,90)以及(10,20]间时买入/卖出量呈线性增长，RSI2高于90或低于10时则呈指数增长：

```
def rsi2_strategy_executor(date, volume):
    market_status = StockMarket.connors_market_status(date)
    exit_point = StockMarket.connors_exit_condition(date)
    rsi_2 = StockIndex.rsi_2(date)

    if rsi_2 > 80 and exit_point != MarketCondition.LONG:
        alpha = 0.8 if market_status == MarketStatus.BULL else 1
        grade = (rsi_2 - 80) / 10 if rsi_2 < 90 else pow((rsi_2 - 80) / 10, 2)
        TradeUtil.sell(volume * grade * alpha, date)
    elif rsi_2 < 20 and exit_point != MarketCondition.SHORT:
        alpha = 1 if market_status == MarketStatus.BULL else 0.8
        grade = (20 - rsi_2) / 10 if rsi_2 > 10 else pow((20 - rsi_2) / 10, 2)
        TradeUtil.buy(volume * grade * alpha, date)
```
赚了，但比银行利率还少，问题出在哪里，我也不知道。


##### 参考资料
1. [How I Trade With Only 2-Period RSI](https://www.tradingsetupsreview.com/trade-2-period-rsi/), by Galen Woods 
2. [RSI2](http://stockcharts.com/school/doku.php?id=chart_school:trading_strategies:rsi2), from www.stockcharts.com
3. [Testing the RSI 2 Trading Strategy On US Stocks](http://jbmarwood.com/rsi-2-trading-strategy/), by JB Marwood
4. [Connors 2-Period RSI Update For 2014](http://systemtradersuccess.com/connors-2-period-rsi-update-2014/), by Jeff Swanson