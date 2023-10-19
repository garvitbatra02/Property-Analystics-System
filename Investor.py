from SimpleDataAnalyser import SimpleDataAnalyser
from DataVisualiser import DataVisualiser

class Investor:
    def __init__(self):
        self.propertiesData = None

    def display_menu(self):
        print("\nProperty Analysis Menu")
        print("1. Suburb Property Summary")
        print("2. Average Land Size for given Suburb")
        print("3. Property Value Distribution In Desired Currency")
        print("4. Sales Trend Obsevered Each Year")
        print("5. Identify a Property of a Specific Price in a Specific Suburb")
        print("6. Exit")

    def main(self):
        while True:
            self.display_menu()
            choice = input("Enter the number of your choice (1-6): ")
            dataAnalyser=SimpleDataAnalyser()
            dataVisualiser=DataVisualiser()
            if(choice<="6" and choice>="1"):
                dataFrame=dataAnalyser.extract_property_info("property_information.csv")

            if choice == "1":
                suburb=input("\nEnter the Suburb ,for which you want to extract information : ")
                dataAnalyser.suburb_summary(dataFrame,suburb)
            elif choice == "2":
                suburb=input("\nEnter the Suburb ,for which you want to get average land size : ")
                value=dataAnalyser.avg_land_size(dataFrame,suburb)
                print(f"Average land size for {suburb} suburb is {value}\n\n")
            elif choice == "3":
                suburb=input("\nEnter the Suburb ,for which you want to get visualize property distribution : ")
                currency=input("Enter the currency in which you want distribution : ")
                if currency=="":
                    print("Currency not provided hence taking AUD for showing details\n")
                    currency='AUD'
                dataVisualiser.prop_val_distribution(dataFrame,suburb,currency)
            elif choice == "4":
                dataVisualiser.sales_trend(dataFrame)
            elif choice == "5":
                price=input("\nEnter the price you want to locate : ")
                suburb=input("Enter the Suburb ,for which you want to locate price : ")
                boolval=dataAnalyser.locate_price(price,dataFrame,suburb)

                if boolval==True:
                    print(f"\nGiven value ${price} exists in given suburb {suburb}\n\n")
                elif boolval==False:
                    print(f"\nGiven value ${price} does not exists in given suburb {suburb}\n\n")

            elif choice == "6":
                print("\nGoodbye!")
                break
            else:
                input("\nInvalid choice. Press Enter to try again.\n\n")
