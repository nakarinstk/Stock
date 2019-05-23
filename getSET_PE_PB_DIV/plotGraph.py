import pandas as pd
import matplotlib.pyplot as plt
import datetime as datetime
from getData import getMktStat
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

URL = {'pe': 'https://www.set.or.th/static/mktstat/Table_PE.xls?004', 'pb': 'https://www.set.or.th/static/mktstat/Table_PBV.xls?005', 'div': 'https://www.set.or.th/static/mktstat/Table_Yield.xls?003'
       }


def createDateTimeVar(timeFrame):
    global currentMonth, currentYear, startDate, startYear, endDate
    global getPE, getPB, getDiv
    if(timeFrame > 0 and type(timeFrame) == int):
        currentYear = datetime.datetime.now().year
        currentMonth = datetime.datetime.now().month
        if currentYear - timeFrame < 1920:
            startYear = 1920
            print('Given time frame is over limit. Start Year is set to 1920.')
        else:
            startYear = currentYear - timeFrame
        startDate = datetime.datetime(startYear, 1, 1)
        endDate = datetime.datetime(currentYear, currentMonth, 1)
        getPE, getPB, getDiv = getMktStat()
    else:
        raise ValueError('Time Frame must be positive integer')


def getGraph(info, timeFrame=5):  # Main Function
    infoLower = info.lower()
    if infoLower not in ('pe', 'pb', 'div'):
        raise ValueError('Type is invalid (PE,PB,DIV)')
    createDateTimeVar(timeFrame)
    if infoLower == 'pe':
        plotGraph('pe', getPE, timeFrame)
    elif infoLower == 'pb':
        plotGraph('pb', getPB, timeFrame)
    elif infoLower == 'div':
        plotGraph('div', getDiv, timeFrame)


def plotGraph(infoType, value, givenTimeFrame):
    df = pd.read_html(
        URL[infoType], header=0)
    df = df[1]
    df.drop(['SET50', 'SET100', 'sSET', 'SETHD', 'mai'],
            axis=1, inplace=True)
    df['Month-Year'] = pd.to_datetime(df['Month-Year'])
    df.set_index('Month-Year', inplace=True)
    df2 = df.loc[(df.index >= str(startYear)) & (df.index < '2019')]
    _ = df2.describe()
    avg = _["SET"][1]
    std = _["SET"][2]
    avgx = float("%.2f" % avg)
    stdx = float("%.2f" % std)
    add1SD = float("%.2f" % (avgx + stdx))
    min1SD = float("%.2f" % (avgx - stdx))
    add2SD = float("%.2f" % (avgx + (2*stdx)))
    min2SD = float("%.2f" % (avgx - (2*stdx)))
    plt.axhline(y=avg+(2*std), color='0', linestyle='--',
                label="{:>7}".format('+2SD = ')+"{:3}".format(add2SD), alpha=0.7)  # +2SD
    plt.axhline(y=avg+std, color='0.3', linestyle='--',
                label="{:>8}".format('+SD = ')+"{:3}".format(add1SD), alpha=0.7)  # +SD
    plt.axhline(y=avg, color='b', linestyle='--',
                label="{:>8}".format('AVG = ')+"{:3}".format(avgx), alpha=0.5)  # AVG
    plt.axhline(y=float(value), linestyle='-.',
                color='r', label="Current : " + value)
    plt.axhline(y=avg-std, color='0.3', linestyle='--',
                label="{:>9}".format('-SD = ')+"{:3}".format(min1SD), alpha=0.7)  # -SD
    plt.axhline(y=avg-(2*std), color='0', linestyle='--',
                label="{:>8}".format('-2SD = ')+"{:6}".format(min2SD), alpha=0.7)  # -2SD
    plt.xlim(startDate, endDate)
    plt.xticks(rotation=30)
    plt.title(
        f'{infoType.upper()} [{startDate.year} - {endDate.year}]', fontsize='20')
    plt.plot(df2["SET"], "-", alpha=0.3, color='g')
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.1)
    plt.gcf().set_size_inches(8, 5)
    plt.tight_layout()
    plt.show()
