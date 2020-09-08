import requests
import os
from tkinter import ttk
import tkinter as tk

###----------------GETTING CURRENCY RATES DATA FROM THE FIXER API--------- https://fixer.io/
url = 'http://data.fixer.io/api/'
ACCESS_KEY = os.environ.get('FIXER_API_KEY') # <---- PASTE HERE YOUR ACCESS KEY
count_of_latest_calculations = 0 # this variable is used to determine when to update the latest_rates value

def make_request(url, TYPE='latest'):
    '''
    the TYPE variable defines if latest or historic rate date will be requested
    '''
    data = {}
    try:
        data = requests.get(url+TYPE+'?access_key='+ACCESS_KEY).json()
        print(data['date'])
        rates = data['rates']
    except KeyError:
        calculated_amount_label.config(text='Pass a valid date (YYYY-MM-DD)')
    except UnboundLocalError:
        calculated_amount_label.config(text='historical date from 1999-01-01')
    return rates

latest_rates = make_request(url)

def update_latest_rates():
    '''
    since we do not make request everytime for the latest rates and we store them in a value,
    they should be updated in order to get the latest
    '''
    latest_rates = make_request(url)
    return latest_rates

def return_currency():
    '''
    calculates the amount of a currency to another currency
    if the date entry is left blank it gives the latest currency, if not gives the historic one in the given date
    '''
    if len(date_entry.get())==0:
        global count_of_latest_calculations
        count_of_latest_calculations += 1
        if count_of_latest_calculations > 10: # every 10 calculation we request new data 
            count_of_latest_calculations = 0
            rates = update_latest_rates()
        else:
            rates = latest_rates
    else:
        date = date_entry.get()
        rates = make_request(url, date)
    try:
        amount = int(amount_entry.get())
        if from_currency != 'EUR':
            amount = amount / rates[from_currency.get()]

        amount = round(amount * rates[to_currency.get()], 2) # rounding with 2 decimal numbers
        calculated_amount_label.config(text=str(amount))
    except ValueError:
        calculated_amount_label.config(text='Pass a valid amount')
    except KeyError:
        calculated_amount_label.config(text='Pass a valid currency')
####----list of available currencies-----------------------------------------------------####
choices = ['AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AWG', 'AZN', 'BAM', 
'BBD', 'BDT', 'BGN', 'BHD', 'BIF', 'BMD', 'BND', 'BOB', 'BRL', 'BSD', 'BTC', 'BTN', 'BWP', 
'BYN', 'BYR', 'BZD', 'CAD', 'CDF', 'CHF', 'CLF', 'CLP', 'CNY', 'COP', 'CRC', 'CUC', 'CUP', 
'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD', 'EGP', 'ERN', 'ETB', 'EUR', 'FJD', 'FKP', 'GBP', 
'GEL', 'GGP', 'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL', 'HRK', 'HTG', 'HUF', 
'IDR', 'ILS', 'IMP', 'INR', 'IQD', 'IRR', 'ISK', 'JEP', 'JMD', 'JOD', 'JPY', 'KES', 'KGS', 
'KHR', 'KMF', 'KPW', 'KRW', 'KWD', 'KYD', 'KZT', 'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LTL', 
'LVL', 'LYD', 'MAD', 'MDL', 'MGA', 'MKD', 'MMK', 'MNT', 'MOP', 'MRO', 'MUR', 'MVR', 'MWK', 
'MXN', 'MYR', 'MZN', 'NAD', 'NGN', 'NIO', 'NOK', 'NPR', 'NZD', 'OMR', 'PAB', 'PEN', 'PGK', 
'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'RON', 'RSD', 'RUB', 'RWF', 'SAR', 'SBD', 'SCR', 'SDG', 
'SEK', 'SGD', 'SHP', 'SLL', 'SOS', 'SRD', 'STD', 'SVC', 'SYP', 'SZL', 'THB', 'TJS', 'TMT', 
'TND', 'TOP', 'TRY', 'TTD', 'TWD', 'TZS', 'UAH', 'UGX', 'USD', 'UYU', 'UZS', 'VEF', 'VND', 
'VUV', 'WST', 'XAF', 'XAG', 'XAU', 'XCD', 'XDR', 'XOF', 'XPF', 'YER', 'ZAR', 'ZMK', 'ZMW', 'ZWL'
]

###--------------------GUI CODE-----------------###
### SETTING THE WINDOW
root = tk.Tk()
root.minsize(300, 350)
root.title('Currency Converter')

# SETTING THE LABELS AND ENTRIES
from_currency_label = tk.Label(root, text='From Currency')
from_currency = ttk.Combobox(root, values=choices, width=20)
from_currency.current(46)

to_currency_label = tk.Label(root, text='To Currency')
to_currency = ttk.Combobox(root, values=choices, width=20)
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
