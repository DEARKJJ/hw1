import pandas as pd
import numpy as np
from bokeh.io import curdoc
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from bokeh.plotting import figure, output_notebook, show
from bokeh.models import ColumnDataSource,HoverTool,CustomJS,Slider,Select
from bokeh.layouts import layout, widgetbox,row,column
from sklearn.preprocessing import LabelEncoder


# In[2]:


df=pd.read_csv('nutrition_raw_anonymized_data.csv')
df1=df.replace(['No','Yes','Innie','Outie'],[False,True,False,True])
df2=df1[df.columns[1:]]
# for m in df2.columns.tolist():
#     df2[m]=LabelEncoder().fit_transform(df2[m])


# In[19]:


# acc=[]
# for i in df2.columns:
#     y_train=df2[i]
#     x_train=df2[df2.columns.drop(i)]
#     model=DecisionTreeClassifier()
#     model.fit(x_train,y_train)
#     predictions=model.predict(x_train)
#     accuracy=metrics.accuracy_score(predictions,y_train)
#     acc.append(accuracy)
#     print ("Accuracy:%s"%"{0:.10}".format(accuracy))
# feature

#controllers
y_map=df2.columns.tolist()
y_select=Select(title="y_select",options=y_map,value='cancer')
model_map=["DecisionTreeClassifier","RandomForestClassifier"]
model_select=Select(title="model_select",options=model_map,value="LogisticRegression")
pre_map={"0.1":0.1,"0.15":0.15,"0.2":0.2,"0.2":0.25,"0.3":0.3,"0.35":0.35,"0.4":0.4,"0.45": 0.45,"0.5": 0.5,"0.55": 0.55,"0.6": 0.6,"0.65": 0.65,"0.7": 0.7,"0.75":0.75,"0.8": 0.8,"0.85":0.85,"0.9": 0.9,"0.95":0.95}
pre_select=Select(title="train data percentange select",options=sorted(pre_map.keys()),value="0.1")

# predictor set up
train=df2.sample(frac=0.1, random_state=1)
test=df2.loc[~df.index.isin(train.index)]
y_train=train['cancer']
y_test=test['cancer']
le=LabelEncoder()
y_train_label=le.fit_transform(y_train)
y_test_label=le.fit_transform(y_test)
x_train=train[df2.columns.drop('cancer')]
x_test=test[df2.columns.drop('cancer')]
model=DecisionTreeClassifier()
model.fit(x_train,y_train_label)
predictions=model.predict(x_test)
accuracy=metrics.accuracy_score(predictions,y_test_label)
p=figure(x_range=(0,54),plot_height=500,plot_width=1000)
p.title.text= "accuracy %.10g"%accuracy
source1=ColumnDataSource(dict(x=y_test.index,y=predictions))
source2=ColumnDataSource(dict(x=y_test.index,y=y_test_label))
# p.circle(x=range(54),y=predictions,source=source1,size=3,color="red")
# p.square(x=range(54),y=y_train,source=source2,size=3,color="black")
# # layout=column(widgetbox(x_select, y_select),p)
# show(layout)


# In[22]:

def update(attrname, old, new):
    train=df2.sample(frac=pre_map[pre_select.value],random_state=1)
    test=df2.loc[~df.index.isin(train.index)]
    y_train=train[y_select.value]
    y_test=test[y_select.value]
    le=LabelEncoder()
    y_train_label=le.fit_transform(y_train)
    y_test_label=le.fit_transform(y_test)
    x_train=train[df2.columns.drop(y_select.value)]
    x_test=test[df2.columns.drop(y_select.value)]
    if model_select.value=="LogisticRegression":
        model=LogisticRegression()
    elif model_select.value=="DecisionTreeClassifier":
        model=DecisionTreeClassifier()
    elif model_select.value=="RandomForestClassifier":
        model=RandomForestClassifier()
    model.fit(x_train,y_train_label)
    predictions=model.predict(x_test)
    accuracy=metrics.accuracy_score(predictions,y_test_label)
    print(accuracy)
    p.title.text= "accuracy %.10g"% accuracy

    source1.data=dict(x=y_test.index,y=predictions)
    source2.data=dict(x=y_test.index,y=y_test_label)

    
    
# x_select.on_change('value',update）
y_select.on_change('value',update)
model_select.on_change('value',update)
pre_select.on_change('value',update)
p.circle(x=y_test.index,y=predictions,source=source1,legend="predictions",size=5,color="red")
p.square(x=y_test.index,y=y_test_label,source=source2,legend="test label",size=5,color="green")

# In[23]:

# update()
# controls=column(x_select, y_select)
# curdoc().add_root(column(y_select,p))
controls=column(model_select, y_select,pre_select)
curdoc().add_root(column(controls,p))
curdoc().title="Predictor"
