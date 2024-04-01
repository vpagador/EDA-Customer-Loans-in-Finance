import pandas as pd
import matplotlib.pyplot as plt
from plotly import express as px
from statsmodels.graphics.gofplots import qqplot

class Plotter():

    def __init__(self):
        pass


    def plot_null_percentages(self, null_info_df:pd.DataFrame):
        null_info_df_transposed = null_info_df.T
        column_names = null_info_df_transposed.columns
        for index,column in enumerate(column_names):
            plt.figure(index)
            null_info_df_transposed[1:].plot(kind='pie',y=column,
                                        figsize=(5, 5),autopct='%1.1f%%',
                                        legend=False,subplots=True,
                                        ylabel='')
            my_circle=plt.Circle( (0,0), 0.5, color='white')
            p=plt.gcf()
            p.gca().add_artist(my_circle)
            plt.title(column)
        plt.show()
    
    def plot_histogram(self, data, title, color = "skyblue",figsize=[3,3],
                        edgecolor = "gold"):
        plt.figure(figsize=figsize)
        plt.hist(data, color = color, edgecolor = edgecolor)
        plt.title(label=title)
        plt.show()

    def plot_box_whisker(self, data, title,size=[400,400]):
        fig = px.box(data,title,width=size[0],height=size[1])
        fig.show()
    
    def plot_multiple_histograms(self, df, columns):
        fig = plt.figure(figsize = (15,15))
        ax = fig.gca()
        df[columns].hist(ax=ax, color = "skyblue", edgecolor = "gold")
        plt.show()

    def plot_qq(self, data, title):
        qqplot(data , scale=1 ,line='q')
        plt.title(label=title)
        plt.show()

def plot_outliers(data, column):
    plot = Plotter()
    plot.plot_histogram(data[column],column)
    plot.plot_box_whisker(data[column],column)

def plot_post_transformation_comparisons(df, column_list, transformed_array_list,
                                          colour_list = ['CornflowerBlue','Crimson',
                                                         'DarkSeaGreen','DarkOrchid',
                                                         'IndianRed']):
    
    comparison_df_list = []
    for column, transformed_array in zip(column_list, transformed_array_list):
        comparison_dataframe = pd.DataFrame({column:df[column],
                                    f'{column}_transformed':transformed_array})    
        comparison_df_list.append(comparison_dataframe)

    for comparision_df,color in zip(comparison_df_list,colour_list):
        print(f"ORIGINAL SKEW:{comparision_df[comparision_df.keys()[0]].skew()}," 
            f"TRANSFORMED SKEW: {comparision_df[comparision_df.keys()[1]].skew()}" )
        comparision_df.hist(figsize=(10,5), color = color, edgecolor = "gold")
        plt.show()