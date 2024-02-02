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
    
    def plot_histogram(self, feature,title):
        plt.hist(feature)
        plt.title(label=title)
        plt.show()

    def plot_qq(self, feature):
        qqplot(feature , scale=1 ,line='q')
        plt.show()
