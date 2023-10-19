import pandas as pd
import numpy as np

class SimpleDataAnalyser:

    def __recursiveBinarySearchForPropertyPrices(self,arr, target, low, high):
        target=int(target)
        if low <= high:
            mid = low + (high - low) // 2
            if arr[mid] == target:
                return True  # Element found, return its index
            elif arr[mid] < target:
                return self.__recursiveBinarySearchForPropertyPrices(arr, target, low, mid-1)
            else:
                return self.__recursiveBinarySearchForPropertyPrices(arr, target, mid+1, high)
        return False  # Element is not in the list

    def __showAnalytics(self,analysisList):
        # Code to sort the given analysis list
        for i in range(1, len(analysisList)):
            key = analysisList[i]
            j = i - 1
            while j >= 0 and key < analysisList[j]:
                analysisList[j + 1] = analysisList[j]
                j -= 1
            analysisList[j + 1] = key

        listSum=0
        standardDeviation=0
        meanValue=0
        maxValue=0
        minValue=0
        medianValue=0

        analysisListSize=len(analysisList)
        # mean calculation
        for listData in analysisList:
            listSum+=listData
        meanValue=listSum/analysisListSize

        #Standard Deviation Calculation
        for listData in analysisList:
            standardDeviation+=(listData-meanValue)**2
        standardDeviation=np.sqrt(standardDeviation/analysisListSize)

        #median calculation
        if analysisListSize%2==1 :
            medianValue=analysisList[analysisListSize//2]
        else:
            medianValue=(analysisList[analysisListSize//2-1]+analysisList[analysisListSize//2])/2

        # Max value calculation
        maxValue=analysisList[analysisListSize-1]

        # Min Value Calculation
        minValue=analysisList[0]

        print(f"Standard Deviation: {standardDeviation:.2f}")
        print(f"Mean Value: {meanValue:.2f}")
        print(f"Maximum Value: {maxValue}")
        print(f"Minimum Value: {minValue}")
        print(f"Median Value: {medianValue:.2f}")

    def __init__(self):
        self.propertiesData = None

    def __suburbSummaryHelper(self,suburbMap, suburb):
        # Here some metrics of average ,standard deviation,median, minimum and maximum are left

        if suburb not in suburbMap:
            raise Exception("No such suburb with the provided value provided exists in data")
        totalBedrooms=[]
        totalBathrooms=[]
        totalParkingSpaces=[]
        targetSuburbSummary=suburbMap[suburb]
        targetSuburbSummarySize=len(targetSuburbSummary)
        print(f"suburb : {suburb}")
        print(f"{'Bedrooms':<10}{'Bathrooms':<10}{'Parking Spaces':<15}")
        for summary in targetSuburbSummary:
            bedrooms, bathrooms, parking_spaces = summary
            totalBedrooms.append(bedrooms)
            totalBathrooms.append(bathrooms)
            totalParkingSpaces.append(parking_spaces)
            print(f"{bedrooms:<10}{bathrooms:<10}{parking_spaces:<15}")
        print("\n")
        print("Analytics for Bedrooms : \n")
        self.__showAnalytics(totalBedrooms)
        print("\n")
        print("Analytics for Bathrooms : \n")
        self.__showAnalytics(totalBathrooms)
        print("\n")
        print("Analytics for Parking_Spaces : \n")
        self.__showAnalytics(totalParkingSpaces)
        print("\n\n")
        

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
                raise ZeroDivisionError("Provided Suburb Does Not Exists in data")

            result = averageLandSizeValue / countOfProperties

        except ZeroDivisionError as e:
            print(f"\nError: {e}")
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
            print("\nNo such suburb with the given value provided exists in data")
            return 2
        
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

    def suburb_summary(self,dataframe,suburb):
        suburbMap={}
        dataFrameSize = len(dataframe)
        for i in range(dataFrameSize):
            propertyValue = dataframe.loc[i]
            if not np.isnan(propertyValue['bedrooms']):
                if not np.isnan(propertyValue['bathrooms']):
                    if not np.isnan(propertyValue['parking_spaces']):
                        if propertyValue['suburb'] not in suburbMap:
                            suburbMap[propertyValue['suburb']] = []
                        suburbMap[propertyValue['suburb']].append([propertyValue['bedrooms'],propertyValue['bathrooms'],propertyValue['parking_spaces']])
        if(suburb=="All"):
            suburbSet=set()
            for suburbValue in dataframe['suburb']:
                suburbSet.add(suburbValue)
            for suburbValue in suburbSet:
                self.__suburbSummaryHelper(suburbMap,suburbValue)
        else:
            self.__suburbSummaryHelper(suburbMap,suburb)
                