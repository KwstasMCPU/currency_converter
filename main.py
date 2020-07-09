import requests
import tkinter as tk


def return_latest(from_currency, to_currency, amount):
    '''
    calculates the amount of a currency to another currency
    '''
    amount = int(amount)
    if from_currency != 'EUR':
        amount = amount / rates[from_currency]

    amount = round(amount * rates[to_currency], 2) # rounding with 2 decimal numbers
    show_amount_label = tk.Label(root, text=str(amount), bg='red')
    show_amount_label.pack()

###----------------GETTING CURRENCY RATES DATA FROM THE FIXER API--------- https://fixer.io/ 
url = 'http://data.fixer.io/api/'
LATEST =  'latest?access_key='
HISTORICAL_DATA = 'YYYY-MM-DD' # FORMAT
ACCESS_KEY = 'acde643bc15d7ce29bb0e1ec699715e2'
data = {}
data = requests.get(url+LATEST+ACCESS_KEY).json()
rates = data['rates']
####

###--------------------GUI CODE-----------------###
### SETTING THE WINDOW
root = tk.Tk()
root.minsize(300, 300)
root.title('Currency Converter')

# SETTING THE LABELS AND ENTRIES
from_currency_label = tk.Label(text='From Currency')
from_currency_entry = tk.Entry()

to_currency_label = tk.Label(text='To Currency')
to_currency_entry = tk.Entry()

amount_label = tk.Label(text='Amount')
amount_entry = tk.Entry()
# SETTING THE BUTTONS
calculate = tk.Button(text="Calculate", command=lambda: return_latest(from_currency_entry.get(), to_currency_entry.get(), amount_entry.get()))
quit = tk.Button(text="QUIT", fg="red", command=root.destroy)
# PACKING
from_currency_label.pack()
from_currency_entry.pack()
to_currency_label.pack()
to_currency_entry.pack()
amount_label.pack()
amount_entry.pack()
calculate.pack()
quit.pack()
root.mainloop()