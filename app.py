
import pandas as pd  
import plotly.express as px  
import streamlit as st 

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Animal Disease Dashboard", page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL ----
@st.cache_data
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
    st.stop() # This will halt the app from further execution.

# ---- MAINPAGE ----
st.title(":bar_chart:  Animal Disease Dashboard")
st.markdown("##")

# TOP KPI's
total_number = int(df_selection["Гаралт"].sum())
average_sick= round(df_selection["Өвчилсөн"].mean(), 1)
star_rating = ":star:" * int(round(average_sick, 0))
average_number_by_location = round(df_selection["Гаралт"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("""---""")

# SALES BY PRODUCT LINE [BAR CHART]
sales_by_product_line = df_selection.groupby(by=["Product line"])[["Total"]].sum().sort_values(by="Total")
fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# SALES BY HOUR [BAR CHART]
sales_by_hour = df_selection.groupby(by=["hour"])[["Total"]].sum()
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Sales by hour</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template="plotly_white",
)
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
