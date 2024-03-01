import streamlit as st
import pandas as pd
from plotly import graph_objs as go
from statsmodels.tsa.arima.model import ARIMA

# Load the dataset
crime_data = pd.read_csv('District_wise_crimes_committed_IPC_2001_2012.csv')
odisha_crime_data = crime_data.loc[crime_data.STATE_UT == "ODISHA"]
odisha_copy = odisha_crime_data.copy()

# Define a function to create the ARIMA forecast plot
def create_arima_forecast_plot():
    # Filter data for the desired district and group by year
    district_data = odisha_copy[odisha_copy['DISTRICT'] == 'SRP(CUTTACK)'].groupby('YEAR')['TOTAL_IPC_CRIMES'].sum()

    # Convert index to datetime
    district_data.index = pd.to_datetime(district_data.index, format='%Y')

    # Fit ARIMA model
    arima_model = ARIMA(district_data, order=(5, 1, 0))
    arima_result = arima_model.fit()

    # Forecast future values with ARIMA model
    arima_forecast = arima_result.forecast(steps=5)

    # Create Plotly figure
    fig = go.Figure()

    # Add historical data
    fig.add_trace(go.Scatter(x=district_data.index, y=district_data.values, mode='lines+markers',
                             name='Historical Data', line=dict(color='royalblue')))

    # Add ARIMA forecast
    fig.add_trace(go.Scatter(x=pd.date_range(start=district_data.index[-1], periods=6, freq='Y')[1:],
                             y=arima_forecast, mode='lines+markers', name='ARIMA Forecast', 
                             line=dict(color='darkorange')))

    # Update layout
    fig.update_layout(title_text="Forecast of Total Crimes in ODISHA for 5 years",
                      xaxis_title="Year", yaxis_title="Total IPC Crimes",
                      plot_bgcolor='rgba(0, 0, 0, 0)',  # Set plot background color to transparent
                      paper_bgcolor='#222',  # Set paper background color to dark gray
                      font=dict(family="Arial, sans-serif", size=12, color="#eee"))  # Set font style, size, and color

    return fig

# Create Streamlit web application
def main():
    # Set page title and description
    st.title('Crime Forecasting Application')
    st.markdown(
        """
        <style>
        .title {
            color: #007BFF;
            text-align: center;
            font-size: 36px;
            padding-top: 20px;
            padding-bottom: 20px;
            font-weight: bold;
            font-family: 'Arial', sans-serif;
        }
        .subtitle {
            color: #6C757D;
            text-align: center;
            font-size: 20px;
            padding-bottom: 20px;
            font-family: 'Arial', sans-serif;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<p class="title">Crime Forecasting Application</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">This web application displays the ARIMA forecast of total IPC crimes in a specific district.</p>', unsafe_allow_html=True)

    # Display the ARIMA forecast plot
    st.plotly_chart(create_arima_forecast_plot(), use_container_width=True)

if __name__ == '__main__':
    main()
