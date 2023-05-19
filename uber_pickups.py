import numpy as np
import pandas as pd
import streamlit as st

DATE_COLUMN = 'date/time'
DATA_URL = 'https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz'


@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    data.rename(lambda x: x.lower(), axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


st.title('Uber pickups in NYC')

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text('Loading data... Done!')

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
st.bar_chart(hist_values)

hour_to_filter = st.slider('hour', 0, 24, 17)
st.subheader(f'Map of pickups at hour {hour_to_filter}:00')
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.map(filtered_data)
