import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
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
    
    def plot_histogram(self, data, title, figsize=[2,2],
                       color = "skyblue", edgecolor = "gold"):
        plt.figure(figsize=figsize)
        plt.hist(data, color = color, edgecolor = edgecolor)
        plt.title(label=title)
        plt.show()

    def plot_qq(self, data, title):
        qqplot(data , scale=1 ,line='q', fit=True)
        plt.title(label=title)
        plt.show()

    def plot_box_whisker(self, data, title):
        plt.boxplot(data)
        plt.title(label=title)
        plt.show()