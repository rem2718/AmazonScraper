# AMAZON SCRAPER

A simple scraper with a simple GUI that extracts some data about a specific product from the original Amazon website.

## HOW TO RUN IT:

1.Download _AmazonScraper.zip_ file

2.Install all the requirements

```
 pip install -r requirements.txt
```

3.Download **FireFox** if you don't have it

4.Disable the cookies for **Amazon** on your **Firefox**

5.Go to file _GUI.py_ and run it.

## NOTES:

- This scraper work with Windows 10 or 11, if you face any problem, copy the header of your **Amazon** request on firefox and paste it on _AmazonScraper.py_ instead of the existing header.

- When you search make sure you write a specific name for a product.

  - **Do:** 'Uno Arduino', 'Micro HDMI', 'Wireless mouse'

  - **Don't:** 'Baby shoes', 'T-shirts', 'Phone cases'

- The results will show you two lists of products:

  - sorted by the lowest price.

  - sorted by the highest rate, reviews number.

- The product info: Name, Price, Rate, Reviews number(click on the row to open the link)

- You need to re-run the code each time you wanna search, otherwise the diagrams won't change.
  - I couldn't fix this problem :(

## THANK YOU!

Hope you enjoy this scraper :)

If you face any problems please contact me

Made by: _@rem2718_

For any suggestions/comments/questions email me at: rem.e2.718@gmail.com
