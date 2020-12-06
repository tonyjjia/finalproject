"""
@author: tonyjia
"""

import pandas as pd
import statsmodels.api as sm

df_original=pd.read_csv(r'/Users/tonyjia/Documents/GitHub/finalproject/finalproject/Final_Version_Dataframe.csv')

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












