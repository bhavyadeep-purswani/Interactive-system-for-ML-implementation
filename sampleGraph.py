# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 15:14:11 2020

@author: lekha
"""
import matplotlib.pyplot as plt,mpld3

import json
import pandas as pd
import numpy as np
from bokeh.palettes import Spectral11
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource
output_file('temp.html')
p = figure(width=500, height=300) 

df=pd.DataFrame(trainData[['sepal_length','sepal_width']]).values.tolist()
d=dict(
       x=trainData.sepal_length.values.tolist(),
       y=trainData.species.values.tolist())
source = ColumnDataSource(d)


p.vbar(x='x',
                top='y',
                
                width=5,source=source,color="#121AA1")
show(p)

import random
r = lambda: random.randint(0,255)
s='#%02X%02X%02X' % (r(),r(),r())


fig,ax = plt.subplots()
ax.bar(data.MSSubClass.values.tolist(),data.SalePrice.values.tolist(), width=0.8, color='b',label='MSSubClass')
ax.bar(data.Id.values.tolist(),data.SalePrice.values.tolist(), width=0.8, color='g',label='Id')
plt.legend(loc="upper right")
plt.ylabel('Sale Price')
d=mpld3.fig_to_html(fig)

plt.show()
plt.bar(df,trainData.species.values.tolist())
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
from datetime import datetime
from bokeh.palettes import Spectral3

output_file('temp.html')

df = pd.DataFrame.from_dict({'dates': ["1-1-2019", "2-1-2019", "3-1-2019", "4-1-2019", "5-1-2019", "6-1-2019", "7-1-2019", "8-1-2019", "9-1-2019", "10-1-2019"], 'windspeed': [10, 15, 20,30 , 25, 5, 15, 30, 35, 25]})
df['dates'] = pd.to_datetime(df['dates'])
source = ColumnDataSource(df)
p = figure(x_axis_type="datetime")
p.line(x=df.dates, y=df.windspeed, line_width=2, source=source)

show(p)