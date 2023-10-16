from SimpleDataAnalyser import SimpleDataAnalyser
import matplotlib.pyplot as plt
import numpy as np

class DataVisualiser:

    def __init__(self):
        self.propertiesData = None
    
    def prop_val_distribution(self,dataframe,suburb,target_currency):
        currency_dict = {"AUD": 1, "USD": 0.66, "INR": 54.25, "CNY": 4.72, "JPY": 93.87, "HKD": 5.12, "KRW": 860.92, "GBP": 0.51, "EUR": 0.60, "SGD": 0.88}

        dataAnalyser=SimpleDataAnalyser()
        priceList=[]
        currencyUsed=target_currency
        if target_currency not in currency_dict:
            print("Given target currency does not exist in data present, hence using AUD")
            priceList=dataAnalyser.currency_exchange(dataframe,currency_dict['AUD'])
            currencyUsed='AUD'

        elif suburb=='All' :
            priceList=dataAnalyser.currency_exchange(dataframe,currency_dict[target_currency])

        else:
            targetSuburbPriceList=[]
            dataFrameSize = len(dataframe)
            for i in range(dataFrameSize):
                    propertyValue = dataframe.loc[i]
                    if propertyValue['suburb'] == suburb:
                        if not np.isnan(propertyValue['price']):
                            targetSuburbPriceList.append(propertyValue['price']*currency_dict[target_currency])
            priceListSize=len(targetSuburbPriceList)
            if priceListSize == 0:
                print("No such suburb with the given value provided exists in data")
                priceList=dataAnalyser.currency_exchange(dataframe,currency_dict['AUD'])
            else:
                priceList=targetSuburbPriceList
        
        bin_edges = np.histogram_bin_edges(priceList, bins='auto')

        # Create the histogram
        hist, bins = np.histogram(priceList, bins=bin_edges)

        # Create the histogram plot
        plt.bar(bins[:-1], hist, width=np.diff(bins))

        # Customizing the plot parameters
        plt.xlabel(f'Price Ranges In {currencyUsed}')
        plt.ylabel('Frequency')
        plt.title('Histogram showing plot of prices of property sold')

        # Saving the chart as an image locally
        plt.savefig('priceForGivenCurrencyAndSuburb.png')

        # Show the plot
        plt.show()

    def sales_trend(self,dataframe):
        yearCountMap={}
        dataFrameSize=len(dataframe)
        for i in range(dataFrameSize):
            propertyValue = dataframe.loc[i]
            if not isinstance(propertyValue['sold_date'], float):
                dateValue=propertyValue['sold_date']
                day, month, year = dateValue.split('-')
                year = int(year)
                if year not in yearCountMap:
                    yearCountMap[year]=0
                yearCountMap[year]+=1

        yearsList=[]
        numberOfHousesSold=[]

        for yearValue,soldCount in yearCountMap.items():
            yearsList.append(yearValue)
            numberOfHousesSold.append(soldCount)

        plt.figure(figsize=(10, 6))  # Set the figure size
        plt.plot(yearsList, numberOfHousesSold, marker='o', linestyle='-')
        plt.title('Number of Houses Sold Each Year')
        plt.xlabel('Year')
        plt.ylabel('Number of Houses Sold')
        plt.grid(True)

        # Saving the chart as an image locally
        plt.savefig('houses_sold_chart.png')

        # Show the chart 
        plt.show()
