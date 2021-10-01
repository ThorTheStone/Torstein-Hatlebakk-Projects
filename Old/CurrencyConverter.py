import PySimpleGUI as sg
from forex_python.converter import CurrencyRates, CurrencyCodes

#Warning - Not all country codes are compatible, if forex does not have the information available, the program crashes


#This colour scheme reminds me of you, so I picked it special just for you ;)
sg.theme('LightBrown5')

#Constructors for forex functions
cr = CurrencyRates()
cd = CurrencyCodes()

#Layout set-up for pySimpleGUI window
layout = [  [sg.Text('Fill in Currency Amount and Exchange Currencies, Then Press Convert')],
            [sg.Text('Convert from'), sg.InputText('NOK')],
            [sg.Text('Amount'), sg.InputText('100')],
            [sg.Text('Convert to'), sg.InputText('EUR')],
            [sg.Checkbox('Use Currency Symbols Instead of Currency Codes in Result', default=False)],
            [sg.Button('Convert'), sg.Button('Quit')] ]

#Create the window
window = sg.Window('Currency Converter', layout)

#Check for convert and quit input
while True:
    event, values = window.read()
    if event in (None, 'Quit'):	# if user closes window or clicks cancel
        break

#Get input values
    c1 = values[0]
    c2 = values[2]
    a1 = values[1]

#Does the math
    rate = cr.get_rate(values[0], values[2])
    result = int(values[1])*rate

#Switch between symbols and names based on input
    try:
        if values[3] == True:
            sg.Popup(a1 + " " + cd.get_symbol(c1) + " is " + str(round(result, 2)) + " " + cd.get_symbol(c2), title='Result')
        else:
            sg.Popup(a1 + " " + cd.get_currency_name(c1) + " is " + str(round(result, 2)) + " " + cd.get_currency_name(c2), title='Result')
    except:
        print('Country not available')

#Window close if quit is clicked
window.close()

