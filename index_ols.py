"""
@author: tonyjia
"""

import pandas as pd
import statsmodels.api as sm

df_original=pd.read_csv(r'/Users/tonyjia/Documents/GitHub/finalproject/finalproject/Final_Version_Dataframe.csv')

#df_original=pd.read_csv(r'/Users/YIHAOLI/Desktop/Github/finalproject/Final_Version_Dataframe.csv')

def reg_model(race):
    race=race.lower()
    X=df_original['Pct_'+str(race)]
    Y=df_original['college_readiness_index']
    X=sm.add_constant(X)
    ols_model=sm.OLS(Y,X).fit()
    print(ols_model.summary())

black_data=reg_model('black')
hispanic_data=reg_model('hispanic')
white_data=reg_model('white')
asian_data=reg_model('asian')

'''
Even though the R-square for all 4 results are quite low, there exists a distinctive difference
between the four summary tables. For African American students, one unit (here, in percentage point)
increase of the African American students is related to a negative 0.6 unit change of the College
Readiness Index. This result implies a crucial problem that African American students from Chicago high schools
are currently facing (no enough academic resources to help them get ready for college education)
'''




# generate binary values using get_dummies
dum_df = pd.get_dummies(df_original, columns=["School_Type"], prefix=["Type_"])

def reg_model(race1,race2):
    race1=race1.lower()
    race2=race2.lower()
    X=dum_df[['Pct_'+str(race1), 
                   'Pct_'+str(race2),
                   'Type__Career academy',
                   'Type__Charter',
                   'Type__Contract',
                   'Type__Magnet',
                   'Type__Military academy',
                   'Type__Neighborhood',
                   'Type__Selective enrollment',]]
    Y=df_original['college_readiness_index']
    X=sm.add_constant(X)
    ols_model=sm.OLS(Y,X).fit()
    print(ols_model.summary())
    
reg_model('black','white')

'''
According the principle component analysis we have conducted, only including
the percentage of white and African American students is sufficient to find the
relationship between other student ethinicies, such as Asian and Hispanic, and
a school's performance on preparing its students being ready for college.
After we put control on school types in the regression, observations generated
from the regression without control on school types still hold. A school's higher
percentage of African American students is associated with an decrease in 
College Readiness Index, and a higher percentage of White students is associaed
with an increase of College Readiness Index. For school types, being a magnet
school, a school located in neighborhoods, or a contract school also associate
with a decrease in College Readiness Index.
'''









