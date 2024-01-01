from bs4 import BeautifulSoup
import requests
from collections import deque
from concurrent.futures import ThreadPoolExecutor
import time
import signal
import threading

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
}

priceDict = {}
stopped_event = threading.Event()


def getValue(symbol:str):
    try:
        url = f'https://finance.yahoo.com/quote/{symbol.upper()}.NS'
        soup = BeautifulSoup(requests.get(url, headers=headers).content, "html.parser")
        div = soup.find('div',{'class':'D(ib) Mend(20px)'})
        val = div.findChild().get('value')
        return float(val)
    except Exception as e:
        print(e)
        stopped_event.set()


def updateStockValue(STOCKNAME):
    while not stopped_event.is_set():
        try:
            val = getValue(STOCKNAME)
            priceDict[STOCKNAME].append(val)
        except KeyboardInterrupt:
            stopped_event.set()
            break 

def printPrice():
    while not stopped_event.is_set():
        try:
            print(priceDict)
            time.sleep(10)
        except KeyboardInterrupt:
            stopped_event.set()
            break

def signal_handler(signal_number, frame):
    stopped_event.set()  # Signal for termination
    executor.shutdown(wait=True)  # Wait for threads to finish

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    try:
        f = open('stocks.txt','r')
        arr = (f.read()).split('\n')
        n = len(arr)
        
        for i in range(n):
            priceDict[arr[i]]  = deque([])
        
        with ThreadPoolExecutor(max_workers=(len(arr)+1)) as executor:
            executor.map(updateStockValue, arr)
            executor.submit(printPrice)

            while not stopped_event.is_set():
                pass
            
    except Exception as e:
        print(e)
        stopped_event.set()

# print(getValue('sbin'))


