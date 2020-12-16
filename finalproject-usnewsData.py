#usnews data scrapping
#Author Weixuan Tony Jia
import requests
import bs4
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import csv
import pandas as pd
import urllib.request

"""
General grading comments:
- Be consistent with your spaces, according to PEP8, e.g. no spaces around = signs in function call arguments, but use spaces for assignment or tests of equality.

"""

url_list=['https://www.usnews.com/education/best-high-schools/search?state-urlname=illinois&district-id=110570&ranked=true&national-rank-range-min=1&national-rank-range-max=13345',
          'https://www.usnews.com/education/best-high-schools/search?state-urlname=illinois&district-id=110570&ranked=true&national-rank-range-min=1534&national-rank-range-max=13345',
          'https://www.usnews.com/education/best-high-schools/search?state-urlname=illinois&district-id=110570&ranked=true&national-rank-range-min=5050&national-rank-range-max=13345',
          'https://www.usnews.com/education/best-high-schools/search?state-urlname=illinois&district-id=110570&ranked=true&national-rank-range-min=8386&national-rank-range-max=13345']
result_name=[]
result_indices=[]
def scrap_data(urls):
    for url_link in urls:
        headers={'user-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1 RuxitSynthetic/1.0 v7444458819 t1099441676816697146 ath9b965f92 altpub cvcv=2'}
        request1=requests.get(url_link,headers=headers)
        soup=bs(request1.text,'lxml')
        contents_name=soup.find_all('h2', attrs={'class':'Heading__HeadingStyled-sc-1w5xk2o-0-h2 gKdQWF Heading-sc-1w5xk2o-1 jFucEe'})
        for x in contents_name:
            result_name.append(x.get_text()) #JL: this should be performed on a local instead of a global, and then returned from the function
            contents_indices=soup.find_all('div', attrs={'class':"DetailCardHighSchools__StatsColumn-zfywu8-2 hPwSiE pt0 pr1 pb1 pl1 md-pt2 md-pr2 md-pb0 md-pl2 lg-pt2 lg-pr2 lg-pb0 lg-pl2"})
            for y in contents_indices:
                result_indices.append(y.get_text()) #JL: this should also be on a local
                result_indices_readiness=[]
                for i in range(len(result_indices)) :
                    for word in result_indices[i].split():
                        result_indices_readiness.append(word)
                        i+=1 #JL: i is cycling by 1 automatically with every iteration of the outer loop. I don't think this is doing what you think it's doing, but at the least it should be explained in a comment because it's odd behavior
    return result_indices_readiness

result_indices_readiness=scrap_data(url_list)
               
result_indices_readiness2=[x for x in result_indices_readiness if "Enrollment" in x] #JL: you can put two conditions in a list comp by using "or"
result_indices_readiness2=[x for x in result_indices_readiness2 if "Readiness" in x]
result_indices_readiness2=[r.replace('Readiness', '') for r in result_indices_readiness2] #JL: you can also chain two replace commands, e.g. r.replace(...).replace(...)
result_indices_final=[r.replace('Enrollment', '') for r in result_indices_readiness2]
result_name_indices=pd.DataFrame(list(zip(result_name, result_indices_final)),columns =['School Name', 'College Readiness Index'])         

result_name_indices.to_csv("/Users/tonyjia/Documents/GitHub/finalproject/finalproject/data_college_readiness.csv", index=False) #JL: a path should be defined at the top, not hard-coded at the bottom






