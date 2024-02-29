import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from statsmodels.tsa.arima.model import ARIMA

crime_data=pd.read_csv('District_wise_crimes_committed_IPC_2001_2012.csv')
odisha_crime_data=crime_data.loc[crime_data.STATE_UT=="ODISHA"]
odisha_copy=odisha_crime_data.copy()
odisha_crime_data=odisha_crime_data.set_index('DISTRICT')
odisha_crime_data=odisha_crime_data.drop(['STATE_UT','YEAR'],axis=1)
# Load the dataset
data = odisha_copy

# Define a function to create the ARIMA forecast plot
def create_arima_forecast_plot():
    # Assuming you want to forecast total IPC crimes for a specific district and year
    # Filter data for the desired district and group by year
    district_data = data[data['DISTRICT'] == 'SRP(CUTTACK)'].groupby('YEAR')['TOTAL_IPC_CRIMES'].sum()

    # Convert index to datetime
    district_data.index = pd.to_datetime(district_data.index, format='%Y')

    # Fit ARIMA model
    arima_model = ARIMA(district_data, order=(5,1,0))  # Example order, you may need to tune these parameters
    arima_result = arima_model.fit()

    # Forecast future values with ARIMA model
    arima_forecast = arima_result.forecast(steps=5)  # Example: forecast 5 years ahead

    # Create Plotly figure
    fig = go.Figure()

    # Add historical data
    fig.add_trace(go.Scatter(x=district_data.index, y=district_data.values, mode='lines+markers', name='Historical Data'))

    # Add ARIMA forecast
    fig.add_trace(go.Scatter(x=pd.date_range(start=district_data.index[-1], periods=6, freq='Y')[1:], y=arima_forecast, mode='lines+markers', name='ARIMA Forecast'))

    # Update layout
    fig.update_layout(title_text="ARIMA Forecast of Total IPC Crimes in YourDistrict", xaxis_title="Year", yaxis_title="Total IPC Crimes")

    return fig

# Create Streamlit web application
def main():
    # Set page title and description
    st.title('Crime Forecasting Application')
    st.write('This web application displays the ARIMA forecast of total IPC crimes in a specific district.')

    # Display the ARIMA forecast plot
    st.plotly_chart(create_arima_forecast_plot(), use_container_width=True)

# Run the web application
if __name__ == '__main__':
    main()
