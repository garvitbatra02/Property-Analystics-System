import pandas as pd
import numpy as np

class SimpleDataAnalyser:

    def __recursiveBinarySearchForPropertyPrices(self,arr, target, low, high):
        if low <= high:
            mid = low + (high - low) // 2
            if arr[mid] == target:
                return True  # Element found, return its index
            elif arr[mid] < target:
                return self.__recursiveBinarySearchForPropertyPrices(arr, target, low, mid-1)
            else:
                return self.__recursiveBinarySearchForPropertyPrices(arr, target, mid+1, high)
        return False  # Element is not in the list

    def __init__(self):
        self.propertiesData = None

    def __suburbSummaryHelper(self,dataframe, suburb):
        # Here some metrics of average ,standard deviation,median, minimum and maximum are left

        targetSuburbSummary=[]
        dataFrameSize = len(dataframe)
        for i in range(dataFrameSize):
            propertyValue = dataframe.loc[i]
            if propertyValue['suburb'] == suburb:
                if not np.isnan(propertyValue['bedrooms']):
                    if not np.isnan(propertyValue['bathrooms']):
                        if not np.isnan(propertyValue['parking_spaces']):
                            targetSuburbSummary.append([propertyValue['bedrooms'],propertyValue['bathrooms'],propertyValue['parking_spaces']])

        targetSuburbSummarySize=len(targetSuburbSummary)
        if targetSuburbSummarySize == 0:
            raise Exception("No such suburb with the provided value provided exists in data")
        print(f"suburb : {suburb}")
        print(f"{'Bedrooms':<10}{'Bathrooms':<10}{'Parking Spaces':<15}")
        for summary in targetSuburbSummary:
            bedrooms, bathrooms, parking_spaces = summary
            print(f"{bedrooms:<10}{bathrooms:<10}{parking_spaces:<15}")


    def extract_property_info(self,file_path):
        propertiesDataFrame = None
        try:
            self.propertiesData = pd.read_csv(file_path)
            propertiesDataFrame = pd.DataFrame(self.propertiesData, columns=self.propertiesData.columns)
            print(f"Data loaded from {file_path}")
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        return propertiesDataFrame

    def currency_exchange(self,dataframe, exchange_rate):
        pricesConvertedList=[]
        for propertyPrice in dataframe['price']:
            if(not np.isnan(propertyPrice)):
                pricesConvertedList.append(propertyPrice*exchange_rate)
        pricesConvertedArray=np.array(pricesConvertedList)
        return pricesConvertedArray

    def avg_land_size(self,dataframe,suburb):
        averageLandSizeValue = 0
        countOfProperties = 0
        dataFrameSize = len(dataframe)
        try:
            for i in range(dataFrameSize):
                propertyValue = dataframe.loc[i]
                if propertyValue['suburb'] != suburb:
                    if suburb == 'All':
                        if propertyValue['land_size'] != -1:
                            actualPropertyValue = propertyValue['land_size']
                            if propertyValue['land_size_unit'] == 'ha':
                                actualPropertyValue *= 1000
                            averageLandSizeValue += actualPropertyValue
                            countOfProperties += 1
                else:
                    if propertyValue['land_size'] != -1:
                        actualPropertyValue = propertyValue['land_size']
                        if propertyValue['land_size_unit'] == 'ha':
                            actualPropertyValue *= 1000
                        averageLandSizeValue += actualPropertyValue
                        countOfProperties += 1

            if countOfProperties == 0:
                raise ZeroDivisionError("No properties meet the criteria.")

            result = averageLandSizeValue / countOfProperties

        except ZeroDivisionError as e:
            print(f"Error: {e}")
            result = 0  # Handle the case when countOfProperties is 0

        return result


    def locate_price(self,target_price,dataframe,target_suburb):
        targetSuburbPriceList=[]
        dataFrameSize = len(dataframe)
        for i in range(dataFrameSize):
                propertyValue = dataframe.loc[i]
                if propertyValue['suburb'] != target_suburb:
                    if target_suburb == 'All':
                        if not np.isnan(propertyValue['price']):
                            targetSuburbPriceList.append(propertyValue['price'])
                else:
                    if not np.isnan(propertyValue['price']):
                        targetSuburbPriceList.append(propertyValue['price'])
        
        priceListSize=len(targetSuburbPriceList)
        if priceListSize == 0:
            raise Exception("No such suburb with the given value provided exists in data")
        
        # code for reverse insertion sort
        for i in range(1, len(targetSuburbPriceList)):
            key = targetSuburbPriceList[i]
            j = i - 1
            while j >= 0 and key > targetSuburbPriceList[j]:
                targetSuburbPriceList[j + 1] = targetSuburbPriceList[j]
                j -= 1
            targetSuburbPriceList[j + 1] = key
        
        # #code for recursive binary search 
        whetherGivenPriceExistsOrNot=self.__recursiveBinarySearchForPropertyPrices(targetSuburbPriceList,target_price,0,priceListSize-1)
        return whetherGivenPriceExistsOrNot

    def suburb_summary(self,dataframe, suburb):
        # Do some sort of optimization over here
        #to remove recomputation
        
        if(suburb=="All"):
            suburbSet=set()
            for suburbValue in dataframe['suburb']:
                suburbSet.add(suburbValue)
            for suburbValue in suburbSet:
                self.__suburbSummaryHelper(dataframe,suburbValue)
        else:
            self.__suburbSummaryHelper(dataframe,suburb)
                
            




a=SimpleDataAnalyser()
b=a.extract_property_info("property_information.csv")
# c=a.currency_exchange(b,1)
# print(a.avg_land_size(b,"ab"))
# print(a.locate_price(881000,b,"Clayton"))
# a._suburbSummaryHelper(b,"Clayton")
a.suburb_summary(b,"All")