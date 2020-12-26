import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
pd.options.display.float_format = '{:.3f}'.format

import datetime
import holoviews as hv
import hvplot.pandas
from sklearn.preprocessing import StandardScaler

import streamlit as st

st.markdown(' ## 🚀 Kickstarter - Capstone Project Proposal')
st.info(''' ## Proposition
The 'failed' campaigns had pledged around 500MM that were not collected from backers - that's 25MM of unrealized profits for the Kickstarter platform, and a lot of heartbreak both for the creators and the backers of the failed projects - I'm excited to see if data science can save the day.

This ***data product*** will help the users to have an estimated success rate of their kickstarter campaign and adjust their stretegy. 
''')
st.success('Current dashboard is focused on the exploratory data analysis')

df_all = pd.read_pickle('processed.pickle')

st.write(df_all.head())

#st.bokeh_chart(hv.render(gv_combination, backend='bokeh'))

