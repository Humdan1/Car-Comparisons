import pandas as pd
import numpy as np
import math

class Catalogue:
    """A class that allows one to compare cars on different metrics
    """
    def __init__(self, path):
        """Initializes the dataframe of cars, row selection, column 
            selection, and the users daily commute
            Args: 
                path - the file containing the cars
            Returns:
                dataframe: file thats read in
                list: row selections
                list: column selections
                float: commute input
            """
        self.df = pd.DataFrame(pd.read_csv(path))
        self.row_selection = []
        self.col_selection = []
        self.daily_commute_dist = float()
    
    def row_select(self):
        """Prints the names of the cars
            Allows the user to select from the cars by index
            Splits the choices into a new list if the choice is an apt number
            Returns:
                list: row selections
            """
        names = self.df['Model Name']
        print(names)
        user_choice = input('\n--- Please enter the index numbers for the cars you would like to select separated by commas. ---\n')
        choice_raw = user_choice.split(',')
        choice = []
        for item in choice_raw:
            n_item = int(item.strip())
            if item.isdigit() and n_item <= len(names) - 1:
                choice.append(n_item)
            else:
                raise ValueError(item, 'Is not integer')
        for i in choice:
            self.row_selection.append(self.df.iloc[i])
    
    def col_select(self):
        """Allows the user to select which columns they want
            Chosen columns are added to a new list
            Returns:
                list: column selections
            """
        count = 0
        choice = []
        for col in self.df.columns:
            print("\n",col, count)
            count += 1
        user_choice = input('\n--- Please enter the index numbers for the columns you would like to select separated by commas. ---\n')
        choice_raw = user_choice.split(',')
        choice = []
        for item in choice_raw:
            n_item = int(item.strip())
            if n_item <= len(names) - 1 and item.isdigit():
                choice.append(n_item)
            else:
                raise ValueError(item, 'Is not integer')
        for i in choice:
            self.col_selection.append(str(self.df.columns[i]))
    
    def set_daily_commute_dist(self):
        """Prompts the user to enter their daily commute in kilometers
            Returns:
                float: daily commute input
        """
        float_value = input('\n--- Please enter the distance of your daily commute in kilometers(km) ---\n1 mile = 1.60934 km')
        if float_value.isdecimal() or float_value.isdigit():
            self.daily_commute_dist = float(float_value)
        else:
            raise ValueError('Is not float')
    
    def commuting_facts(self):
        """Calls set_daily_commute_dist
            Prompts user to choose cars
            Returns:
                String: the users total commutes and cost of gas
            """
        self.set_daily_commute_dist()
        names = self.df['Model Name']
        print(names)
        user_choice = input('\nPlease select your commuter vehicle by index number:\n')
        if user_choice.isdigit():
            miles_per_tank = float(self.df.iloc[user_choice]['MPG Combined'])*float(self.df.iloc[user_choice]['Tank Capacity (gal)'])
            kilometers_per_tank = miles_per_tank*1.60934
            print('\nYou commute:\n', self.daily_commute_dist, 'km every day\n', self.daily_commute_dist*7, 'km every week\n', self.daily_commute_dist*30, 'km every month\n', self.daily_commute_dist*365, 'km every year')
            print('\nYou will have to refil your tank every',"%.2f" % kilometers_per_tank, 'km, which is every',"%.2f" % (kilometers_per_tank/self.daily_commute_dist), 'days.\nThis means you will spend approximately $', "%.2f" % ((2.73*self.df.iloc[user_choice]['Tank Capacity (gal)'])*(365/(kilometers_per_tank/self.daily_commute_dist))), ' a year on gas for commuting purposes.')
        else:
            raise ValueError('Is not integer')
    
    def compare(self):
        """Prints out the comparison of the two cars based on the columns chosen
            Returns:
                String: Model names and respective specifications
        """
        self.row_select()
        self.col_select()
        for i in self.col_selection:
            for j in self.row_selection:
                print(j.loc["Model Name"], '\n---', i, ': ', j.loc[i],'---\n')
    
    def pollution_facts(self):
        """Uses daily commute input to compute emissions over different time lengths
            Returns:
                String: Pullution facts for each model name in selection
                String: Average pollution statistic
                String: Avergae forest sequestration
        """
        self.set_daily_commute_dist()
        self.row_select()
        for x in self.row_selection:
            if math.isnan(x.loc["CO2 Emissions gkm"]) == True:
                print(x.loc["Model Name"], "does not have emissions data.")
            else:
                dly_pollution = self.daily_commute_dist*x.loc["CO2 Emissions gkm"]
                print('\nPollution facts for ', x.loc["Model Name"], "in grams of CO2:\nDaily: ", dly_pollution, "\nWeekly: ", dly_pollution*7, "\nMonthly: ", dly_pollution*30, " or %.2f" %((dly_pollution*30)/907185), "tons \nAnually: ", dly_pollution*365, " or %.2f" %((dly_pollution*365)/907185), " tons")
        avg_pollution = self.daily_commute_dist*251
        print('\nAverage pollution facts in grams of CO2 for comparision:', "\nDaily: ", avg_pollution, "\nWeekly: ", avg_pollution*7, "\nMonthly: ", avg_pollution*30, "\nAnually: ", avg_pollution*365)
        print('\nOn average, one acre of new forest can sequester about 2.5 tons of carbon annually.')

    def race(self):
        """Begins a count and prints statistics for each sorted selection in row_select
            Returns:
                String: Lets race a 1/4 mile
                List: race_list
                String: Results are in
                String: Model name, 1/4 mile stats
        """
        cnt = 1
        print("Lets race a 1/4 mile!\n")
        self.row_select()
        race_list = sorted(self.row_selection, key=lambda x: x.loc["1/4 mile time (sec)"])
        print("\n --- RESUTS ARE IN ---\n")
        for x in race_list:
            print(cnt,": ", x.loc["Model Name"], "| 1/4 Mile Time:", x.loc["1/4 mile time (sec)"], "| 1/4 Mile Top Speed:", x.loc["1/4 mile speed (mph)"])
            cnt +=1
def begin():
    """Instantiates Catalogue into variable c with a path to the car catalog CSV
        Calls the comparison function based on the users choice
        Clears the row and col selections if invalid choice is selected
        Breaks the while loop if user is done with the program
        Returns:
            String: 
    """
    c = Catalogue("326.csv")
    while True:
        print("--- Welcome to Zack and Humdan's amazing car catalogue! ---\n")
        print("Available Comparisons:\n0: Commuting Facts\n1: Compare Stats\n2: Pollution Facts\n3: Race!\n")
        user = int(input("Please choose a comparison by number: "))
        if user == 0:
            c.commuting_facts()
        if user == 1:
            c.compare()
        if user == 2:
            c.pollution_facts()
        if user == 3:
            c.race()
        if user > 3 or user < 0:
            print("Your choice was invalid.")
        c.row_selection.clear()
        c.col_selection.clear()
        ans = int(input("Are you done with the program? Enter 0 if yes, 1 if no. "))
        if ans == 0:
            break
        if ans == 1:
            continue
        if ans != 0 or ans != 1:
            raise ValueError('Integer not 0 or 1')

if __name__ == '__main__':
    begin()