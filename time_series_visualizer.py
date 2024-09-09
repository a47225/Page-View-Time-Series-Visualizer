import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv",index_col='date')

# Clean data
df = df.loc[(df['value']<df['value'].quantile(0.975)) & (df['value']>df['value'].quantile(0.025))]


def draw_line_plot():
    # Draw line plot
    fig = plt.figure(figsize=(20,10))
    df['value'].plot()
    plt.xlabel("Date",  size = 10)
    plt.ylabel("Page Views", size = 10)
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")





    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    # This includes the cleaned data, which explains why some dates are missing
    df_bar = df.copy()
    print(type(df_bar.index))

    df_bar['Years'] = pd.to_datetime(df_bar.index.values).year
    df_bar['Months'] = pd.DatetimeIndex(df_bar.index.values).month_name()

    df_bar = df_bar.groupby(['Years','Months'], sort=False, as_index=False).mean()

    df_bar['Months'] = pd.Categorical(df_bar.Months, categories=df_bar[df_bar.Years == 2017].Months, ordered=True)

    df_pivot = pd.pivot_table(
    	df_bar,
    	values="value",
    	index="Years",
    	columns="Months",
    )
    ax = df_pivot.plot(kind="bar")

    fig = ax.get_figure()

    fig.set_size_inches(7, 6)

    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")

    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box['year'] = pd.to_datetime(df_box.index.values).year
    df_box['month'] = pd.DatetimeIndex(df_box.index.values).month_name()
    print(df_box)

    months= ['January','February','March','April','May','June','July','August','September','October','November','December']

    df_box['month'] = pd.Categorical(df_box.month, categories = months, ordered=True) 

    df_box['month'] = df_box["month"].apply(lambda row: row[:3])
    print(df_box)


    # Draw box plots (using Seaborn)
    fig, axs = plt.subplots(1, 2, figsize=(18, 6))


    axs[0]=sns.boxplot(df_box,x="year",y="value",ax=axs[0])
    axs[0].set(xlabel="Year",ylabel="Page Views", title="Year-wise Box Plot (Trend)")

    axs[1]=sns.boxplot(df_box,x="month",y="value",ax=axs[1])
    axs[1].set(xlabel="Month",ylabel="Page Views", title="Month-wise Box Plot (Seasonality)")




    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
