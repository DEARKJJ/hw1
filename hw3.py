
# coding: utf-8

# In[1]:


from bokeh.io import curdoc
import pandas as pd
import numpy as np
from sklearn import neighbors
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from bokeh.plotting import figure, output_notebook, show
from bokeh.models import ColumnDataSource,HoverTool,CustomJS,Slider,Select
from bokeh.palettes import Spectral6
from bokeh.layouts import layout, widgetbox,row,column


# In[2]:


df=pd.read_csv('Wholesale customers data.csv')
X=df[["Milk","Fresh"]].values
Milk=df["Milk"]
Fresh=df["Fresh"]
n_map={"one": 1,"two": 2,"three":3,"four":4,"five":5}


# In[3]:


# cluster_slider = Slider(title="min_bad_teeth released", start=1, end=6, value=1, step=1)
kmeans=KMeans(n_clusters=1)
kmeans.fit(X)
predict=kmeans.predict(X)
source=ColumnDataSource(dict(x=Milk,y=Fresh,pre=predict))
cluster_s=Select(title="",options=sorted(n_map.keys()),value="one")
p=figure(plot_width=800, plot_height=800, title="clustering with keans",x_axis_label="milk",y_axis_label="Fresh") 
p.circle(Milk,Fresh,size=10,source=source,color=Spectral6[0])


# In[4]:


def update(attrname, old, new):
# def update():
    n=n_map[cluster_s.value]
    print(n)
    kmeans=KMeans(n_clusters=n)
    kmeans.fit(X)
    predict=kmeans.predict(X)
    source=ColumnDataSource(dict(x=Milk,y=Fresh,pre=predict))
    co=np.array([Spectral6])
    co=[Spectral6[i] for i in predict]
    source.data=(dict(x=Milk,y=Fresh,ccc=co,pre=predict))
    p.circle(Milk,Fresh,fill_color=co,line_color="black",size=10,source=source) 
    p.add_tools(HoverTool(tooltips=[("(x,y)","(@x,@y)"),("Type","@pre")]))

# cluster_slider.on_change('value',lambda attr, old, new: update())
# cluster_s.on_change('value',lambda attr, old, new: update())
cluster_s.on_change('value',update)
# update()
# p.circle(Milk,Fresh,color=co,size=8,source=source)
p.add_tools(HoverTool(tooltips=[("(x,y)","(@x,@y)"),("Type","@pre")]))
# layout=row(cluster_slider,p)
# show(layout)


# In[5]:


p2=figure(plot_width=500, plot_height=500, title="no clustering",x_axis_label="milk",y_axis_label="Fresh") 
p2.circle(Milk,Fresh,size=10,color="red",source=source)
p2.add_tools(HoverTool(tooltips=[("(x,y)","(@x,@y)")]))


# In[6]:


pca=PCA(n_components=2)
pca.fit(X)
reduction=pca.fit_transform(X)

x1=reduction[:,0]
y1=reduction[:,1]
source=ColumnDataSource(dict(x=Milk,y=Fresh,pre=predict,pcax=x1,pcay=y1))
p1=figure(plot_width=500, plot_height=500, title="clustering with PCA",x_axis_label="milk",y_axis_label="Fresh") 
p1.circle(reduction[:,0], reduction[:,1],size=10,color="red",source=source)
p1.add_tools(HoverTool(tooltips=[("(x,y)","(@pcax,@pcay)")]))
curdoc().add_root(column(column(cluster_s,p),row(p1,p2)))
# curdoc().add_root(row(cluster_s,p)) 

      

