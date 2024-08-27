#!/usr/bin/env python
# coding: utf-8

# In[1]:


import psycopg2
import csv
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# In[3]:


def merge_csv_files(input_files, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as out_file:
        writer = csv.writer(out_file)
        
        for index, input_file in enumerate(input_files):
            with open(input_file, 'r', newline='', encoding='utf-8-sig') as in_file:
                reader = csv.reader(in_file)
                if index != 0:
                    next(reader)
                writer.writerows(reader)

def main():
    input_files = ['/Users/kirillbogomolov/mestechko/finding_ways/poi/hotels.csv', '/Users/kirillbogomolov/mestechko/finding_ways/poi/poi.csv']
    output_file = '/Users/kirillbogomolov/mestechko/finding_ways/poi/all_points.csv'
    merge_csv_files(input_files, output_file)

if __name__ == "__main__":
    main()


# In[4]:


# бесплатный ключ доступа можно найти здесь https://account.mapbox.com
MAPBOX_ACCESS_TOKEN = "pk.eyJ1IjoiY3NpY3NhY3NvIiwiYSI6ImNsaWFpM3B2bzAzcTUzbXFwZ2ZjdnVpajEifQ.UY-B4Tg9KH0NXNC423X7Jg"


# In[5]:


data_hotels = pd.read_csv('/Users/kirillbogomolov/mestechko/finding_ways/poi/hotels.csv')
data_poi = pd.read_csv('/Users/kirillbogomolov/mestechko/finding_ways/poi/poi.csv')

data_hotels['is_hotel'] = True
data_poi['is_hotel'] = False

data_all = pd.concat([data_hotels, data_poi], ignore_index=True)

district_sum = data_all.groupby('district_id').size().reset_index(name='Плотность')
data_all = pd.merge(data_all, district_sum, on='district_id')

fig = px.scatter_mapbox(data_all, lat='latitude', lon='longitude',
                        hover_name='name', zoom=9,
                        mapbox_style='carto-positron',
                        color_discrete_sequence=['blue'],
                        )

fig.update_traces(marker=dict(color=data_all['is_hotel'].map({True: 'red', False: 'blue'})))
fig.show()

