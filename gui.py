# Import the important libraries 
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import webbrowser
import AmazonScraper as asc

sc = asc.AmazonScraper(5)#it scrapes up to 5 pages
min_price = []
max_rate = []
data_headings = ['Name', 'Price $', 'Rate', 'Reviews']

sg.theme('lightBlue 3')
#GUI elements
img1 = sg.Image('logos images\py_logo.png', pad=10)#
img2 = sg.Image('logos images\Amazon_logo.png', pad=10)
img3 = sg.Image('logos images\psu_logo.png', pad=10)
title = sg.Text('AMAZON SCRAPER', font=('Terminal', 35, 'bold'))
enter = sg.Text('Enter your product name:', font=('Terminal', 13))
input = sg.InputText(key='-PRODUCT-', expand_x=True)
search =  sg.Button(button_text='SEARCH', s=(10,1), font=('Terminal'))
clear = sg.Button(button_text='CLEAR', s=(10,1),  font=('Terminal'))
tableTitle1 = sg.Text('Cheapest products:', font=('Terminal', 10))
tableTitle2 = sg.Text('\t\t\t\t\t\t\t    Highest rate products:', justification='center', font=('Terminal', 10))
table1 = sg.Table(values=[], font=('Terminal', 11), num_rows=10, vertical_scroll_only=False, headings=data_headings, max_col_width=65, col_widths=[43,12,9,12], auto_size_columns=False, justification='center',enable_events =True, key='-PRICE-')
table2 =  sg.Table(values=[], font=('Terminal', 11), num_rows=10, vertical_scroll_only=False, headings=data_headings, max_col_width=65, col_widths=[43,12,9,12], auto_size_columns=False, justification='center',enable_events =True,  key='-RATE-')
canvas1 = sg.Canvas(key='-CANVAS1-', expand_x=True)
canvas2 = sg.Canvas(key='-CANVAS2-', expand_x=True)
frame1 = sg.Frame('',[[canvas1]], expand_x=True, size=(500,300))
frame2 = sg.Frame('', [[canvas2]], expand_x=True, size=(500,300))

#Main layout for the window
layout = [  
          [sg.Column([[img1, img2, img3]], justification='center')],
          [sg.Column([[title]], justification='center', pad=(10,10))],
          [enter, input, search, clear],
          [sg.Column([[tableTitle1, tableTitle2]])],
          [table1, table2],
          [sg.Column([[frame1, frame2]], justification='center')] 
        ]

window = sg.Window('Amazon Scraper', layout, margins=(10, 10), finalize=True, resizable=True)

def draw_figs():
    """
        This function call the visualize() and draw the two figures inside their canvases
    """
    fig1, fig2 = sc.visualize()
    fig1_cnvs = FigureCanvasTkAgg(fig1, window['-CANVAS1-'].TKCanvas)
    fig1_cnvs.get_tk_widget().pack(side='bottom', fill='both', expand=1)
    fig1_cnvs.draw()
    fig2_cnvs = FigureCanvasTkAgg(fig2, window['-CANVAS2-'].TKCanvas)
    fig2_cnvs.get_tk_widget().pack(side='bottom', fill='both', expand=1)
    fig2_cnvs.draw()
   
        
def update_table():
    """
        This function sorts the df by the cheapest prices and stores the results in min_price,
        and sorts it again by the highest rate and reviews count then stores the results in max_rate
    """
    global min_price 
    min_price = df.sort_values(by = ['Price']).iloc[:20]
    global max_rate
    max_rate = df.sort_values(by = ['Reviews No', 'Rate'], ascending=False).iloc[:20]
    window['-PRICE-'].update(values=min_price.values.tolist())
    window['-RATE-'].update(values=max_rate.values.tolist())
     
        
while True:             
    event, values = window.read()#start the window
    if event == sg.WIN_CLOSED:#If user clicks exit button
        break
    elif event == 'SEARCH':#If user clicks search button
        product = values['-PRODUCT-']
        df = sc.scrape(product)#Start scraping
        draw_figs()
        update_table()
    elif event == '-PRICE-':#If user clicks on a row in the price table
        elem = values['-PRICE-'][0]
        urls = min_price['Link']
        webbrowser.open(urls.iloc[elem])#Open the link for the row's product  
    elif event == '-RATE-':#If user clicks on a row in the rate table
        elem = values['-RATE-'][0]
        urls = max_rate['Link']
        webbrowser.open(urls.iloc[elem])#Open the link for the row's product   
    elif event == 'CLEAR':#If user clicks clear button
        sc.df.drop(df.index, inplace=True)#Clear all dataframes 
        min_price.drop(df.index, inplace=True)
        max_rate.drop(df.index, inplace=True)
        window['-PRICE-'].update(values=[])#Delete the tables' contents
        window['-RATE-'].update(values=[])
        for canvas in [window['-CANVAS1-'].TKCanvas, window['-CANVAS2-'].TKCanvas]:
            if canvas.children:
                for child in canvas.winfo_children():
                    child.destroy()
        window.refresh()
        
window.close()        
        

