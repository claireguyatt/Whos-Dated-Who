# Whos-Dated-Who

## About
A data science project to determine who's dating who, or, more accurately, who's dating **how many**. 
This project involved [webscraping the Who's Dated Who site](https://github.com/claireguyatt/Whos-Dated-Who/blob/master/src/collect_data.py) by [iteratively adding names](https://github.com/claireguyatt/Whos-Dated-Who/blob/master/src/get_names.py) based off of a small starting list of 50 celebrities. 
The starter list had 25 men and 25 women spread evenly across 5 disciplines: actors; musicians; masterminds (business/science/technology); athletes; and world leaders, to get a representative group.
Once the data was collected it was then time for the fun of cleaning & preprocessing, exploring & plotting, and finally, of running a linear regression to determine the factors
that affect the number of relationships: https://github.com/claireguyatt/Whos-Dated-Who/blob/master/WDW.ipynb.

## Tech Stack
Python (BeautifulSoup, Pandas, sklearn)
Jupyter Noetbook
