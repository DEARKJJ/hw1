
# coding: utf-8

# In[1]:


from bokeh.io import curdoc
import pandas as pd
import numpy as np
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.models import HoverTool,CustomJS, Slider, ColumnDataSource
from sklearn.metrics import mean_squared_error
from bokeh.models.widgets import Slider, Select, TextInput
from bokeh.layouts import layout, widgetbox,row,column
from bokeh.plotting import figure,show,output_file

origin=pd.read_csv('Wholesale customers data.csv')
missing=pd.read_csv('Wholesale customers data-missing.csv')


# In[2]:


a=missing.isnull().sum()
print(a)

missing1=missing.copy()
missing1.fillna(missing1.median() ,inplace=True)
rmsl1=np.sqrt(mean_squared_error(missing1,origin))
print(rmsl1)


missing2=missing.copy()
missing.fillna(method='ffill', inplace=True)
rmsl2=np.sqrt(mean_squared_error(missing,origin))
print(rmsl2)


# In[3]:


x_axis_map=['Fresh','Milk','Grocery','Frozen','Detergents_Paper','Delicassen'] 
y_axis_map=['Channel','Region']
x_axis_select=Select(title="X Axis",options=x_axis_map,value='Fresh')
y_axis_select=Select(title="Y Axis",options=y_axis_map,value='Channel')


# In[4]:


source=ColumnDataSource(dict(x1=origin['Fresh'],x2=missing['Fresh'],y1=origin['Channel'],y2=missing['Channel']))
source1=ColumnDataSource(dict(x1=origin['Fresh'],x2=missing1['Fresh'],y1=origin['Channel'],y2=missing1['Channel']))
source2=ColumnDataSource(dict(x1=origin['Fresh'],x2=missing2['Fresh'],y1=origin['Channel'],y2=missing2['Channel']))
# source = ColumnDataSource(origin,missing)
# x=origin['Fresh']
# y=origin['Channel']
# source = ColumnDataSource(dict(x=x,y=y))


# In[5]:


p=figure(plot_height=500,plot_width=1500,x_range=(0,120000),y_range=(0,3), title="origin data vs missing data")
p1=figure(plot_height=500,plot_width=1500,x_range=(0,120000),y_range=(0,3), title="")
p2=figure(plot_height=500,plot_width=1500,x_range=(0,120000),y_range=(0,3), title="")
p1.title.text= "origin data vs missing data filled with median and the error is %.10g " % rmsl1
p2.title.text= "origin data vs missing data filled with mean and the error is %.10g " % rmsl2




def update_data():
	# attrname, old, new
    p.xaxis.axis_label=x_axis_select.value
    p.yaxis.axis_label=y_axis_select.value 
    p1.xaxis.axis_label=x_axis_select.value
    p1.yaxis.axis_label=y_axis_select.value 
    p2.xaxis.axis_label=x_axis_select.value
    p2.yaxis.axis_label=y_axis_select.value 
    source.data=dict(x1=origin[x_axis_select.value],y1=origin[y_axis_select.value],x2=missing[x_axis_select.value],y2=missing[y_axis_select.value])
    source1.data=dict(x1=origin[x_axis_select.value],y1=origin[y_axis_select.value],x2=missing1[x_axis_select.value],y2=missing1[y_axis_select.value])
    source2.data=dict(x1=origin[x_axis_select.value],y1=origin[y_axis_select.value],x2=missing2[x_axis_select.value],y2=missing2[y_axis_select.value])


# In[8]:


x_axis_select.on_change('value',lambda attr, old, new: update_data())
y_axis_select.on_change('value',lambda attr, old, new: update_data())


# In[9]:


p.square("x1","y1",source=source,size=10, color="red", fill_alpha=0.5)
p.circle("x2","y2",source=source,size=5, color="black", fill_alpha=0.5)
p.add_tools(HoverTool(tooltips=[("number origin","@x1"),("Area origin","@y1"),("number missing","@x2"),("Area missing", "@y2")]))

p1.square("x1","y1",source=source1,size=10, color="red", fill_alpha=0.5)
p1.circle("x2","y2",source=source1,size=5, color="black", fill_alpha=0.5)
p1.add_tools(HoverTool(tooltips=[("number origin","@x1"),("Area origin","@y1"),("number missing","@x2"),("Area missing", "@y2")]))

p2.square("x1","y1",source=source2,size=10, color="red", fill_alpha=0.5)
p2.circle("x2","y2",source=source2,size=5, color="black", fill_alpha=0.5)
p2.add_tools(HoverTool(tooltips=[("number origin","@x1"),("Area origin","@y1"),("number missing","@x2"),("Area missing", "@y2")]))


# In[10]:


update_data()


# In[11]:


# controls = widgetbox(x_axis_select, y_axis_select)
# layout=column(controls,p,p1,p2)
# output_file("Wholesale customers data-missing.html", title="Wholesale customers data-missing")
# show(layout)
# l = layout([[column(p,p1,p2)]])
# curdoc().add_root(l, controls)
controls=column(x_axis_select, y_axis_select)
curdoc().add_root(column(controls,p,p1,p2))
curdoc().title = "Classification Demo"


# In[32]:


# p.add_tools(HoverTool(tooltips=[("(x,y)","(@x,@y)"),("label","$color:fill_color")]))

