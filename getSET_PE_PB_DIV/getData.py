import requests
import bs4
from bs4 import BeautifulSoup


def getMktStat():
    # for some reason, SET.or.th is fail to verfied SSL
    requests.urllib3.disable_warnings()
    url = 'https://marketdata.set.or.th/mkt/marketsummary.do?language=th&country=TH'
    r = requests.get(url, verify=False)
    s = BeautifulSoup(r.text, 'lxml')
    sc = s.find_all('div', {'class': 'row info'})
    pe = (sc[2].find_all('div'))[1].text.strip()
    pb = (sc[3].find_all('div'))[1].text.strip()
    div = (sc[4].find_all('div'))[1].text.strip()
    return pe, pb, div


if __name__ == "__main__":
    pe, pb, div = getMktStat()
    print("PE :", pe)
    print("PB :", pb)
    print("Div :", div)
