#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 02:49:41 2021

@author: junaid
"""

import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
import matplotlib.pyplot as plt
plt.style.use('seaborn-white')

data = pd.read_csv("/home/junaid/Downloads/survey_results_public - survey_results_public.csv")
data = data.replace('NaN', np.nan) #replace empty cells with np.null

framework_desired_dotnet= data['WebframeDesireNextYear'].str.contains('ASP.NET Core', na= False)
years_dotnet = data[framework_desired_dotnet]['YearsCode']

framework_desired_angular = data['WebframeDesireNextYear'].str.contains('Angular.js', na=False) 
years_angular = data[framework_desired_angular]['YearsCode'] 

framework_desired_django = data['WebframeDesireNextYear'].str.contains('Django', na=False)
years_django = data[framework_desired_django]['YearsCode'] 

years_dotnet = years_dotnet.dropna()
years_angular = years_angular.dropna()
years_django = years_django.dropna()

years_dotnet = years_dotnet.replace('Less than 1 year', .5)
years_dotnet = years_dotnet.replace('More than 50 years', 55)

years_angular = years_angular.replace('Less than 1 year', .5)
years_angular = years_angular.replace('More than 50 years', 55)

years_django = years_django.replace('Less than 1 year', .5)
years_django = years_django.replace('More than 50 years', 55)

years_dotnet = pd.to_numeric(years_dotnet)
years_django = pd.to_numeric(years_django)
years_angular = pd.to_numeric(years_angular)

years_dotnet = years_dotnet[years_dotnet > 0]
years_django = years_django[years_django > 0]
years_angular = years_angular[years_angular > 0]


print(years_dotnet.describe())
print(years_dotnet.median())
print(years_dotnet.mode())

print(years_django.describe())
print(years_django.median())
print(years_django.mode())

print(years_angular.describe())
print(years_angular.median())
print(years_angular.mode())


result = stats.levene(years_dotnet, years_django, years_angular)
print(result)
print("\n")

if(result.pvalue<0.05):
    print("Comment: Variances of population is different. Anova assumption is violated")
else:
    print("Comment: Homeogeneity of variances in population is not violated")
    
    

# Rejecting outliers for dot net users

l=years_dotnet.quantile(.25)
u= years_dotnet.quantile(.75)
IQR=u-l
upper_limit= u+1.5*IQR
lower_limit= l-1.5*IQR
years_dotnet=years_dotnet[(years_dotnet<=upper_limit) & (years_dotnet>=lower_limit)]

# Rejecting outliers for angular users

l=years_angular.quantile(.25)
u= years_angular.quantile(.75)
IQR=u-l
upper_limit= u+1.5*IQR
lower_limit= l-1.5*IQR
years_angular=years_angular[(years_angular<=upper_limit) & (years_angular>=lower_limit)]

# Rejecting outliers for django users

l=years_django.quantile(.25)
u= years_django.quantile(.75)
IQR=u-l
upper_limit= u+1.5*IQR
lower_limit= l-1.5*IQR
years_django=years_django[(years_django<=upper_limit) & (years_django>=lower_limit)]







sm.qqplot(np.sqrt(years_dotnet), line='r')
sm.qqplot(np.sqrt(years_angular), line='r')
sm.qqplot(np.sqrt(years_django), line='r')

#plt.hist(np.sqrt(years_dotnet))
#plt.hist(np.sqrt(years_angular))
#plt.hist(np.sqrt(years_django))



F, p = stats.f_oneway(years_dotnet, years_django, years_angular)
#F, p = stats.f_oneway(np.sqrt(years_dotnet), np.sqrt(years_angular), np.sqrt(years_django))
# Seeing if the overall model is significant
print('F-Statistic = %.3f, p = %.3f' % (F, p))
if(p<0.05): 
    print("Comment: Null Hypothesis is Rejected")

data.head()