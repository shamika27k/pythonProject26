import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt

df = pd.read_csv("startup_cleaned.csv")
st.set_page_config(layout='wide', page_title='Startup Analysis')
st.title('Shamika Kadam')
st.title('FS23AI007')
df['date']=pd.to_datetime(df['date'],errors='coerce')
df['month']=df['date'].dt.month
df['year']=df['date'].dt.year

def load_investor_details(investor):
    st.title(investor)
    st.subheader('Most Recent Investments')
    last5_df = df[df['investors'].str.contains(investor, na=False)].head(5)[
        ['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.dataframe(last5_df)
    st.subheader('Maximum Investment')
    last5_dff = df[df['investors'].str.contains(investor, na=False)].groupby('startup')['amount'].sum().sort_values(
        ascending=False).head(1)
    st.dataframe(last5_dff)

    col1, col2, col3 = st.columns(3)
    with col1:
        big_series = df[df['investors'].str.contains(investor, na=False)].groupby('startup')[
            'amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')
        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)
        st.pyplot(fig)

    with col2:
        vertical_ser = df[df['investors'].str.contains(investor, na=False)].groupby('vertical')['amount'].sum()
        st.subheader('Sectors invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_ser, labels=vertical_ser.index, autopct="0.01f%%")

        st.pyplot(fig1)

    with col3:
        # Corrected the line below, changed square brackets to parentheses
        new_city = df[df['investors'].str.contains(investor, na=False)].groupby('city')['amount'].sum()
        st.subheader('City-Wise')
        fig2, ax2 = plt.subplots()
        ax2.pie(new_city, labels=new_city.index)

        st.pyplot(fig2)

    sub1 = df[df['investors'].str.contains(investor, na=False)].groupby('subvertical')['amount'].sum()
    col1.subheader('Subvertical Data')
    fig3, ax3 = plt.subplots()
    ax3.bar(sub1.index, sub1.values)
    col1.pyplot(fig3)

    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    sub2 = df[df['investors'].str.contains(investor, na=False)].groupby('year')['amount'].sum()
    col2.subheader('Yearly Investment')
    fig2, ax2 = plt.subplots()
    ax2.plot(sub2.index, sub2.values)
    col2.pyplot(fig2)


    rounds = df[df['investors'].str.contains('3one4 Capital', na=False)].groupby('round')['amount'].sum()
    col3.subheader('Round-Wise')
    fig3, ax3 = plt.subplots()
    ax3.bar(rounds.index, rounds.values)
    col3.pyplot(fig3)


def overall():
    st.title('Overall Analysis')

    total = round(df['amount'].sum())
    #max amount
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    avg_funding = df.groupby('startup')['amount'].sum().mean()
    num_startups = df['startup'].nunique()
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.metric('Total',str(total) + 'Cr')
    with col2:
        st.metric('Max',str(max_funding)+'Cr')
    with col3:
        st.metric('Avg',str(round(avg_funding))+'Cr')

    with col4:
        st.metric('Founded Startups',num_startups)


    st.header('MoM Chart')
    selected_option = st.selectbox('select type',[' Total','Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
    fig3,ax3 = plt.subplots()
    ax3.plot(temp_df['x_axis'],temp_df['amount'])

    st.pyplot(fig3)

    st.header('Sector Analysis')
    st.subheader("Top 3 Industries")
    top_verticals = df['vertical'].value_counts().head(3)
    fig, ax = plt.subplots()
    top_verticals.plot(kind='pie', ax=ax)
    st.pyplot(fig)



    st.header('City Wise funding')
    # Group by city and sum the investment amounts, filling missing values with 0
    total_investment_by_city = df.groupby('city')['amount'].sum().fillna(0)
    # Sorting the result by total investment amount
    total_investment_by_city = total_investment_by_city.sort_values(ascending=False)
    # Resetting index to make city a column again
    total_investment_by_city = total_investment_by_city.reset_index()


    # Streamlit code
    st.subheader('Total Investment by City')
    # Plotting a pie chart
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(total_investment_by_city['amount'], labels=total_investment_by_city['city'], autopct='%1.1f%%')
    ax.set_title('Total Investment by City')
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # Displaying the plot
    st.pyplot(fig)
    # Group by investors and find the maximum investment amount for each investor

    df['date'] = pd.to_datetime(df['date'])

    # Extract year from the date column
    df['year'] = df['date'].dt.year

    # Group by year and startup, summing the investment amounts, and finding the top startup each year
    top_startups_yearly = df.groupby(['year'])['startup'].agg(lambda x: x.value_counts().idxmax()).reset_index()


    # bar graph
    st.title('Top Startup Year-Wise Overall')
    # Plotting a bar graph
    fig, ax = plt.subplots()
    ax.bar(top_startups_yearly['year'], top_startups_yearly['startup'], color='skyblue')
    ax.set_xlabel('Year')
    ax.set_ylabel('Top Startup')
    ax.set_title('Top Startup Each Year Overall')
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    # Displaying the plot
    st.pyplot(fig)


    st.title("Top Investors")
    # Aggregate investment amounts for each investor
    investor_totals = df.groupby('investors')['amount'].sum().reset_index()
    # Rank investors based on total investment amount
    investor_totals = investor_totals.sort_values(by='amount', ascending=False)
    # Select top investors (e.g., top 10)
    top_investors = investor_totals.head(10)
    # Plotting the pie chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.pie(top_investors['amount'], labels=top_investors['investors'], autopct='%1.1f%%')
    ax.set_title('Top Investors')
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # Display the pie chart using Streamlit
    st.pyplot(fig)

    st.subheader('Funding Heatmap')
    heatmap_data_custom = df.pivot_table(values='amount', index='year', columns='month',
                                                aggfunc='sum')
    fig_heatmap_custom, ax_heatmap_custom = plt.subplots()
    cax_custom = ax_heatmap_custom.matshow(heatmap_data_custom, cmap='viridis')
    fig_heatmap_custom.colorbar(cax_custom)
    ax_heatmap_custom.set_xticks(range(len(heatmap_data_custom.columns)))
    ax_heatmap_custom.set_xticklabels(heatmap_data_custom.columns, rotation=45)
    ax_heatmap_custom.set_yticks(range(len(heatmap_data_custom.index)))
    ax_heatmap_custom.set_yticklabels(heatmap_data_custom.index)
    st.pyplot(fig_heatmap_custom)


def startup_details(startup_name):
    st.header('Founders:')
    # Filter the DataFrame to select rows where the 'startup' column
    old_df = df[df['startup'] == startup_name]
    # Print the names of investors in the startup
    int1 = old_df['investors']
    # Create a DataFrame from the 'investors' column
    investors_df = pd.DataFrame(int1, columns=['investors']).reset_index()
    # Display the DataFrame
    st.write(investors_df)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader('Industries invested in:')
        filtered_df = df[df['startup'].str.contains(startup_name, na=False)].dropna(subset=['vertical']).drop_duplicates(
            subset=['vertical'])

        # Resetting the index and printing only the 'lndustry' values
        a = filtered_df.reset_index(drop=True)['vertical'].tolist()
        for i in a:
            st.write(i)

    with col2:
        st.subheader('Sub-Industries invested in:')
        filtered_df = df[df['startup'].str.contains(startup_name, na=False)].dropna(subset=['subvertical']).drop_duplicates(
            subset=['subvertical'])

        # Resetting the index and printing only the 'Sublndustry' values
        a = filtered_df.reset_index(drop=True)['subvertical'].tolist()
        for i in a:
            st.write(i)

    with col3:
        st.subheader('City-Wise Investment:')
        filtered_df = df[df['startup'].str.contains(startup_name, na=False)].dropna(subset=['city']).drop_duplicates(
            subset=['city'])

        # Resetting the index and printing only the 'city' values
        a = filtered_df.reset_index(drop=True)['city'].tolist()
        for i in a:
            st.write(i)

    st.header('Funding Rounds')
    funding_rounds_info = df[['round', 'investors', 'date']].sort_values('date', ascending=False)
    st.dataframe(funding_rounds_info)





# st.dataframe(df)
st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select One', ['Overall Analysis', 'Startup', 'Investor'])

if option == 'Overall Analysis':
    overall()


elif option == 'Startup':
    st.title("Startup Analysis")
    select_start=selected_investor = st.sidebar.selectbox('Select One',
                                             sorted(set(df['startup'].astype(str).str.split(',').sum())))
    btn1 = st.sidebar.button('Find Startup Details')
    if btn1:
        st.title(select_start)
        startup_details(select_start)

else:
    st.title('Investor')
    selected_investor = st.sidebar.selectbox('Select One',
                                             sorted(set(df['investors'].astype(str).str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investors Details')
    if btn2:
        load_investor_details(selected_investor)
