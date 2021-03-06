import pandas as pd
import numpy as np

    
def load_and_process(path):
    
    # Method Chain 1(Load data, fix column names and remove missing values)
    
    df1 = (
            pd.read_csv(path)
            .rename(columns = {"age" : "Age", "sex" : "Sex", "bmi" : "BMI", "children" : "Children", "smoker" : "Smoker", "region" : "Region", "charges" : "Insurance Cost"})
            .dropna()
        )
    
    # Method Chain 2(Round BMI and Insurance Cost, sort data by increasing Insurance Cost and re-number rows.)
    
    df2 = (
            df1
            .round({"BMI" : 1, "Insurance Cost" : 2})
            .sort_values("Insurance Cost", ascending = True)
            .reset_index(drop = True)
            
        )
    
    # Method Chain 3(Add new column "weight_class" displaying appropriate weight class for each row by using function 'check_weight_class'. Rename it to "Weight Class")
    
    df3 = (
            df2
            .assign(weight_class = check_weight_class(df2['BMI']))
            .assign(age_group = check_age_group(df2['Age']))
            .rename(columns = {"weight_class" : "Weight Class", "age_group" : "Age Group"})
        )

    return df3

def check_weight_class(BMI):
    
    # Checks BMI of person and returns the correct Weight class based on where it falls on the BMI scale.
    # Takes in BMI column, creates a list with corresponding weight classes, and returns the list
    
    weight_class_list = []
    for i in range(0, len(BMI)):
        if BMI[i] > 30.0:
            weight_class_list.append("Obese")
        elif BMI[i] >=25 and BMI[i] < 30.0:
            weight_class_list.append("Overweight")
        elif BMI[i] >=18.5 and BMI[i] < 25.0:
            weight_class_list.append("Normal")
        else:
            weight_class_list.append("Underweight")
            
    
    return weight_class_list

def check_age_group(Age):
    
    # Checks Age of person and returns the correct Age group.
    # Takes in Age column, creates a list with corresponding Age groups, and returns the list
    
    age_group_list = []
    for i in range(0, len(Age)):
        if Age[i] > 60:
            age_group_list.append("Senior")
        elif Age[i] > 24:
            age_group_list.append("Adult")
        elif Age[i] > 14:
            age_group_list.append("Youth")
        else:
            age_group_list.append("Child")
            
    
    return age_group_list

def insurance_avg_by_weight(df_old):
    df_new = (
            df_old
            .groupby('Weight Class')
            .mean()
            .sort_values(by = 'Insurance Cost')
            .drop(columns = {'Age', 'BMI', 'Children'})
    )
    
    return df_new

def insurance_avg_by_child(df_bad):
    df_good = (
            df_bad
            .groupby('Children')
            .mean()
            .sort_values(by = 'Insurance Cost')
            .drop(columns = {'Age', 'BMI'})
    )
    
    return df_good

def insurance_avg_by_region(df_reg):
    df_final = (
            df_reg
            .groupby('Region')
            .mean()
            .sort_values(by = 'Insurance Cost')
            .drop(columns = {'Age', 'BMI','Children'})
    )
    
    return df_final
     