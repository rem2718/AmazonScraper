# Import the important libraries 
import requests
from bs4 import BeautifulSoup
from matplotlib.figure import Figure
from matplotlib import style
import numpy as np
import pandas as pd



class AmazonScraper:
    """ 
        This class scrapes the original Amazon website for a specific product
        it scrapes the following: product name, price, rate, reviews number, link
    """ 
    headers = { #Request header
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
    }
    params = { #Request parameters
        'k': '',
        'page': '1',
        'language': 'en_US',
    }
    
    def __init__(self, pg):
        """Constructor
        Args:
            pg (int): number of pages that is scraped
        """
        self.MAX_PAGE_NO = pg
        self.df = pd.DataFrame(columns = ['Name', 'Price', 'Rate', 'Reviews No', 'Link' ]) #Main dataframe that store all the data
    
        
    def extract(self, res):
        """This function extracts the data from the result div 

        Args:
            res (HTML element): the div that contains the result 

        Returns:
            list: the row that contains all the data that extracted from the div
        """
        #Extracting the name
        name = res.find('span', attrs = {'class':"a-size-medium a-color-base a-text-normal"}).text
        #Extracting the price
        elem = res.find('span', attrs = {'class':"a-offscreen"})
        price = float((elem.text)[1:]) if elem else None
        #Extracting the rate
        elem = res.find('span', attrs = {'class':"a-icon-alt"})
        rate = float(elem.text.split(' ')[0]) if elem else None
        #Extracting the reviews number
        elem = res.find('span', attrs = {'class':"a-size-base puis-light-weight-text s-link-centralized-style"})
        elem = elem if elem else res.find('span', attrs = {'class':"a-size-base s-underline-text"}) 
        reviews_no = int(elem.text.replace(',', '')) if elem else None
        # Extracting the link
        elem = res.find('a', attrs = {'class':"a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})
        href = "https://www.amazon.com" + elem['href'] if elem else None
        return [name, price, rate, reviews_no, href]
        
        
    def scrape(self, product):
        """This is the main function for scraping it sends a request for each page,
        and extracts all the results
        
        Args:
            product (string): the name of the product

        Returns:
            dataframe: df after all the rows are added
        """        
        for page in range(1, self.MAX_PAGE_NO + 1):
            self.params['k'] = product
            self.params['page'] = str(page)
            r = requests.get('https://www.amazon.com/s', params=self.params, headers=self.headers)
            if r.status_code != 200:#if the page is not found
                print('Error!')
                continue
            soup = BeautifulSoup(r.content, 'html5lib')# html5lib is the parser here
            results = soup.findAll('div', attrs = {'data-component-type':"s-search-result"})
            for res in results:
                row = self.extract(res)
                self.df.loc[len(self.df)] = row
            print(f"Page: {page} done!")               
        return self.df 
    
    
    def visualize(self):
        """This is the main function for the result visualization 

        Returns:
            Figure: the two figures that is displayed on the gui
        """
        style.use('dark_background')
        fig1 = self.price_hist()
        fig2 = self.rate_chart()
        return fig1, fig2
    
    
    def price_hist(self):
        """this function plots a histogram representing the frequency of the product's prices 

        Returns:
            Figure: The figure of the histogram
        """
        fig = Figure(figsize=(4,4), dpi=150, edgecolor= 'black', tight_layout=True)
        pr = self.df['Price'].copy().dropna()
        ax = fig.add_subplot(1,1,1)
        ax.hist(pr, bins=5)
        ax.set_title('Average Prices', fontsize=5)
        ax.set_xlabel('Price $', fontsize=5)
        ax.set_ylabel('Number of Products', fontsize=5)
        ax.tick_params(axis='both', which='major', labelsize=5)
        ax.tick_params(axis='x')
        ax.plot(bins=5)
        return fig


    def rate_chart(self):
        """this function plots a bar chart representing number of the reviews of each rate

        Returns:
            Figure: The figure of the bar chart
        """
        fig = Figure(figsize=(4,4), dpi=150, edgecolor= 'black', tight_layout=True)
        sd = self.df[['Rate','Reviews No']].copy().dropna()
        sd['Rate'] = np.around(sd['Rate'].astype(np.double))
        sd = sd.groupby(['Rate']).sum()
        ax = fig.add_subplot(1,1,1)
        ax.bar(sd.index, sd.iloc[:,0])
        ax.set_title('Rating', fontsize=5)
        ax.set_xlabel('Rate', fontsize=5)
        ax.set_ylabel('Number of Reviews', fontsize=5)
        ax.tick_params(axis='both', which='major', labelsize=5)
        ax.tick_params(axis='x')
        ax.plot()
        return fig  
    





