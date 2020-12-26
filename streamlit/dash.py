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

color_palette = ['#196A47' , '#f56343']
df_all = pd.read_pickle('processed.pickle')

df_success = df_all[df_all['state'] == 'successful']
df_fail = df_all[df_all['state'] == 'failed']

df_plot = df_all.groupby(['main_category', 'state']).size().reset_index().pivot(columns = 'state', 
                                                                                index = 'main_category', values = 0)
df_plot = df_plot[['successful', 'failed']]

plot1 = df_plot.hvplot(kind='bar', stacked=True, color = color_palette , 
               bar_width = 0.5, height = 500, title = 'Number of projects per category').opts(line_color = 'white', xrotation = 90)


cols = df_all['main_category'].value_counts().index
df_plot.sort_values(by = ['successful'], ascending= False , inplace= True)
df_plot_c = df_plot[['successful', 'failed']]
plot2 = df_plot_c.hvplot(kind = 'bar', stacked = True, color = color_palette, bar_width = 0.5, 
                 height = 400, title = 'Number of successful and failed projects per category'
                ).opts(line_color = 'white', xrotation = 90)


df_plot_c['sum'] = df_plot_c['successful'] + df_plot_c['failed'] #+ df_plot_c['canceled']
df_plot_c['successful'] = df_plot_c['successful'] / df_plot_c['sum'] * 100
df_plot_c['failed'] = df_plot_c['failed'] / df_plot_c['sum'] * 100

df_plot_c.drop(labels='sum', axis = 1, inplace= True)
plot3 = df_plot_c.hvplot(kind = 'bar', stacked = True, color = ['#196A47' , '#f56343'], 
                 bar_width = 0.5, height = 400, title = 'Success rate per category (percentage)').opts(line_color = 'white', xrotation = 90)



plot4 = df_success.hvplot(x='scaled_goal', y='duration', color = color_palette[0], kind = 'scatter', 
                       title = 'Successful projects' ).opts(size = 0.5, alpha = 0.5, width = 400, height = 400)
plot5 = df_fail.hvplot(x='scaled_goal', y='duration', color = color_palette[1] , kind = 'scatter',
                    title = 'Failed projects').opts(size = 0.5, alpha = 0.5, width = 400, height = 400)





# df_plot = df_all.groupby(['country', 'state']).size().reset_index().pivot(columns = 'state',
#                                                                           index = 'country', values = 0)
# df_plot = df_plot[['successful', 'failed']]

# df_plot['sum'] = df_plot['failed'] + df_plot['successful']
# df_plot['failed'] = df_plot['failed'] / df_plot['sum']
# df_plot['successful'] = df_plot['successful'] / df_plot['sum']
# df_plot_c = df_plot.drop(labels='sum', axis = 1, inplace=True)


#plot6 = df_plot.hvplot(kind='bar', stacked=True , color = color_palette, title = 'Success rate by country').opts(line_color = 'white', bar_width = 0.5)



df_success['counter'] = 1
df_plot = df_success[['main_category', 'usd_goal_real', 'usd_pledged_real', 'backers', 'counter']]
df_plot = df_plot.groupby(['main_category']).sum()
df_plot['usd_pledged_real'] = df_plot['usd_pledged_real'] - df_plot['usd_goal_real'] 
df_plot['usd_goal_real'] = df_plot['usd_goal_real'] / 10000000
df_plot['usd_pledged_real'] = df_plot['usd_pledged_real'] / 10000000

df_plot['backers'] = df_plot['backers'] / 200000

df_plot['new_ind'] = 0
cols = list(cols)
for i in range(len(cols)) :
    df_plot['new_ind'][cols[i]] = i
df_plot = df_plot.sort_values(by = 'new_ind')
df_plot = df_plot.drop(labels = 'new_ind', axis = 1)

df_plot_c = df_plot.copy()
for col in df_plot_c.columns:
    df_plot_c[col] = df_plot_c[col] / df_plot_c['counter']

df_plot_c['usd_goal_real'] = df_plot_c['usd_goal_real'] * 5000000
df_plot_c['usd_pledged_real'] = df_plot_c['usd_pledged_real'] * 5000000
df_plot_c['backers'] = df_plot_c['backers'] * 5000000

money_palette = ['#264653', '#2a9d8f']
g1 = df_plot.hvplot( y = 'backers', color = 'black', label = 'number of backers, not to scale').opts(line_dash ='dashed' )
g2 = df_plot.hvplot( bar_width = 0.5, y = ['usd_goal_real', 'usd_pledged_real'], 
                     kind='bar', stacked = True, color = money_palette, logy = False ).opts(line_color = 'white')

g3 = df_plot_c.hvplot( y = 'backers' ,color = 'black', 
                      label = 'average number of backers, not to scale').opts(line_dash ='dashed' )
g4 = df_plot_c.hvplot( bar_width = 0.5, y = ['usd_goal_real', 'usd_pledged_real'], 
                      kind='bar', stacked = True, color = money_palette,  logy = False ).opts(line_color = 'white')



plot7 = (g2 * g1).opts(height = 400, width = 900, xrotation = 90, title = 'Cumulative goal, pleddged amount and number of backers per category') 
plot8 = (g4 * g3).opts(height = 400, width = 900, xrotation = 90, title = 'Average goal, pleddged amount and number of backers per category')





cat_plots = (plot2 + plot3 + plot7 + plot8).opts(shared_axes=False).cols(1)
st.bokeh_chart(hv.render(cat_plots, backend='bokeh'))


#-----
# duration_plots = (plot5 + plot4).opts(shared_axes=False).cols(1)
# st.write('## duration vs goal')
# st.bokeh_chart(hv.render(duration_plots, backend='bokeh'))

# st.write(df_all['country'].unique())
#st.bokeh_chart(hv.render(plot2, backend='bokeh'))

