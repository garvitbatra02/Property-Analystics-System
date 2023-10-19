from Investor import Investor


def main():
    """
    Defining the main function for Property System

    This will implement all user functionalities including Analyser and Visualiser .
    This will basically use the Investor class which implements the user menu with each 
    menu leveraging specific functions implemented in SimpleDataAnalyser and DataVisualiser
    classes

    """
    investorApp=Investor()
    investorApp.main()

if __name__ == "__main__":
    main()