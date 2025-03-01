# Share trading information
Using Python and some extra libraries to scrape information off websites, these programs display information about shares on the terminal
as well as producing a CSV file with this information. 

The websites used to obtain data for these programs are: \
https://www.marketindex.com.au/asx-listed-companies (to determine the top 200 ASX companies) \
https://www.marketindex.com.au/upcoming-dividends \
https://au.finance.yahoo.com/quote/CBA.AX/history/ (amongst other companies)

Currently provides information for a "dividend stripping" strategy - outputs companies with upcoming ex-dividend dates and collects information
about their franking percentage, dividend yield.
Also calculates a 210 day moving average for a "momentum" based strategy.
Program only collects data off websites but does not execute trades, this is left to the user and their own strategy.
