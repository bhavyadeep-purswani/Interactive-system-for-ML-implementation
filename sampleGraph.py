# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 15:14:11 2020

@author: lekha
"""
import matplotlib.pyplot as plt

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

ax = plt.subplot(111)
#ax.bar(trainData.species.values.tolist(),trainData.sepal_length.values.tolist(), width=0.2, color='b', align='center')
ax.bar(data.Id.values.tolist(),data.SalePrice.values.tolist(), width=0.2, color='#ff69b4', align='center')


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