import requests
import os
import time
from tkinter import ttk
import tkinter as tk
import configparser
import json

configparse = configparser.ConfigParser()
configparse.read('config.ini')
AVAILABLE_CURRENCIES_STR = configparse['AVAILABLE_CURRENCIES']['choices']
AVAILABLE_CURRENCIES_LS = json.loads(AVAILABLE_CURRENCIES_STR)
ACCESS_KEY = configparse['KEY']['ACCESS_KEY']
URL = 'http://data.fixer.io/api/'

def make_request(URL, TYPE='latest'):
    global start_time
    '''
    Makes request to the fixer.io/api.
    the TYPE variable defines if a latest or a historic currency rate will be requested
    '''
    data = {}
    try:
        url_request = ''.join([URL, TYPE, '?access_key=', ACCESS_KEY])
        print(url_request)
        # measuring time in order to make a requests every 10 secs (since i am using the free key, i have limited amount of requests)
        start_time = time.time() 
        data = requests.get(url_request).json()
        print(data['date'])
        rates = data['rates']
    except KeyError:
        calculated_amount_label.config(text='Pass a valid date (YYYY-MM-DD)')
    except UnboundLocalError:
        calculated_amount_label.config(text='historical date from 1999-01-01')
    return rates

def update_latest_rates():
    latest_rates = make_request(URL)
    return latest_rates

def return_currency():
    '''
    calculates the amount of a currency to another currency
    if the date entry is left blank it gives the latest currency, 
    if not gives the historic one in the given date
    '''
    if len(date_entry.get())==0:
        global start_time
        end_time = time.time()
        if end_time - start_time > 10: # check time elapsed since previous request
            print(end_time - start_time)
            start_time = end_time
            count_of_latest_calculations = 0
            rates = update_latest_rates()
        else:
            rates = latest_rates
    else:
        date = date_entry.get()
        rates = make_request(URL, date)
    try:
        amount = int(amount_entry.get())
        if from_currency != 'EUR':
            amount = amount / rates[from_currency.get()]

        amount = abs(round(amount * rates[to_currency.get()], 4)) # rounding with 4 decimal numbers
        calculated_amount_label.config(text=str(amount))
    except ValueError:
        calculated_amount_label.config(text='Pass a valid amount')
    except KeyError:
        calculated_amount_label.config(text='Pass a valid currency')


if __name__=="__main__":
    latest_rates = make_request(URL)
    ###--------------------GUI CODE-----------------###
    ### SETTING THE WINDOW
    root = tk.Tk()
    root.minsize(300, 350)
    root.title('Currency Converter')

    # SETTING THE LABELS AND ENTRIES
    from_currency_label = tk.Label(root, text='From Currency')
    from_currency = ttk.Combobox(root, values=AVAILABLE_CURRENCIES_LS, width=20)
    from_currency.current(46)

    to_currency_label = tk.Label(root, text='To Currency')
    to_currency = ttk.Combobox(root, values=AVAILABLE_CURRENCIES_LS, width=20)
    to_currency.current(149)

    amount_label = tk.Label(root, text='Amount')
    amount_entry = tk.Entry(root, width=25)

    calculated_amount_label = tk.Label(root, text='', bg='red', width=25)

    date = tk.Label(root, text='Historical (YYYY-MM-DD)')
    date_entry = tk.Entry(root, width=25)

    # SETTING THE BUTTONS
    calculate = tk.Button(text="Calculate", command=return_currency)
    quit = tk.Button(text="QUIT", fg="red", command=root.destroy)

    # PACKING
    from_currency_label.pack()
    from_currency.pack()
    to_currency_label.pack()
    to_currency.pack()
    amount_label.pack()
    amount_entry.pack()
    date.pack()
    date_entry.pack()
    calculated_amount_label.pack(pady=20)
    calculate.pack()
    quit.pack(pady=20)

    # GUI MAIN LOOP
    root.mainloop()
