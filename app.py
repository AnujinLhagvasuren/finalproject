import pandas as pd
import plotly.express as px
import streamlit as st


df = pd.read_csv("mal_galzuu.csv")
st.dataframe(df)

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Animal Disease Dashboard", page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL ----
@st.cache
def get_data_from_excel():
    df = pd.read_excel(
        io="mal_galzuu.csv",
        engine="openpyxl",
        sheet_name="Disease",
        skiprows=3,
        usecols="B:R",
        nrows=1000,
    )
    # Add 'hour' column to dataframe
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

df = get_data_from_excel()

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
city = st.sidebar.multiselect(
    "Select the Province:",
    options=df["Province"].unique(),
    default=df["Province"].unique()
)

customer_type = st.sidebar.multiselect(
    "Select the Animal Type:",
    options=df["Animal_type"].unique(),
    default=df["Animal_type"].unique(),
)

gender = st.sidebar.multiselect(
    "Select the Age:",
    options=df["Age"].unique(),
    default=df["Age"].unique()
)

df_selection = df.query(
    "Province == @Аймаг & Animal_type ==@Амьтны төрөл & Age == @Сар"
)

# Check if the dataframe is empty:
if df_selection.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop()  # This will halt the app from further execution.

# ---- MAINPAGE ----
st.title(":bar_chart:  Animal Disease Dashboard")
st.markdown("##")

# TOP KPI's
total_number = int(df_selection["Гаралт"].sum())
average_sick = round(df_selection["Өвчилсөн"].mean(), 1)
star_rating = ":star:" * int(round(average_sick, 0))
average_number_by_location = round(df_selection["Гаралт"].mean(), 2)
