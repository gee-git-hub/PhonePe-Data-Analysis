import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector as sql
import pandas as pd
import requests
import json
import plotly.express as px
import time
from PIL import Image
import base64

# Connect to the database
mydb = sql.connect(host="localhost", user="root", password="root", database='phonepe')
print(mydb)
mycursor = mydb.cursor(buffered=True)

# Set page configuration
st.set_page_config(
    page_title="Phonepe Visualization",
    layout="wide",
    initial_sidebar_state="expanded"
)



# Sidebar with an option menu
with st.sidebar:
    st.image('plus.gif')
    selected = option_menu("Menu",
                           ["HOME", "EXPLORE", "INSIGHTS"],
                           icons=["house-door-fill", "tools", "card-text"],
                           default_index=0,
                           orientation="horizontal",
                           styles={"nav-link": {"font-size": "20px", "text-align": "center", "margin": "0px", "--hover-color": "#663399"},
                                   "icon": {"font-size": "30px"},
                                   "container": {"max-width": "6000px"},
                                   "nav-link-selected": {"background-color": "#663399"}})

if selected == 'HOME':
    
    st.markdown("<h1 style='text-align: center; color: #FFFFFF;'>PHONEPE DATA VISUALIZATION & EXPLORATION</h1>", unsafe_allow_html=True)
    #st.markdown('<h1 class="center-title">PHONEPE DATA VISUALIZATION & EXPLORATION</h1>', unsafe_allow_html=True)

    st.write(":iphone: PhonePe is India's premier digital payments platform, serving millions of users nationwide. Established in 2015, PhonePe has transformed the way people conduct transactions, making it easy, secure, and convenient to send and receive money, pay bills, recharge mobile phones, and more, all via smartphones.")

    st.write(":iphone: Processing over a billion transactions each month, PhonePe gathers extensive data that offers valuable insights into consumer behavior, spending patterns, and trends in the digital payments landscape. Our mission is to empower individuals, businesses, and policymakers with actionable insights from this data, fostering innovation and promoting financial inclusion across India.")
    
         # Read the image file and encode it to base64
    with open('C:\\Users\\LENOVO\\Desktop\\Guvi Proj\\Phonepe\\phonepe.gif', 'rb') as f:
        image_base64 = base64.b64encode(f.read()).decode()

    # Use HTML to center the image
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center;">
            <img src="data:image/gif;base64,{image_base64}" style="width: 50%;"/>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    #st.image('phonepe.gif', caption="PhonePe", use_column_width=True, output_format='PNG')

    st.markdown("<h1 style='text-align: center; color: #FFFFFF;'>TECHNOLOGIES USED</h1>", unsafe_allow_html=True)
    #st.subheader(":White[TECHNOLOGIES USED]")

    TECHNOLOGIES_USED = """
📱 Technologies utilized in this project include GitHub Cloning, Python, Pandas, 
   MySQL, mysql-connector-python, Streamlit, and Plotly.
   
📱 PhonePe Pulse is a project designed to visualize and explore data on various 
   metrics and statistics available in the PhonePe Pulse GitHub repository.

📱 The project's aim is to extract, process, and present the data in a 
   user-friendly format, providing valuable insights and information.

📱 This project is part of the Fintech domain, focusing on analyzing transaction
   data and user behavior.

📱 To get started, follow the instructions in the Problem Statement and Approach 
   sections.

📱 Discover the insights and visualizations offered by the dashboard!
    """

    def stream_data():
        for word in TECHNOLOGIES_USED.split(" "):
            yield word + " "
            time.sleep(0.02)

    if st.button("Click Here For details"):
        placeholder = st.empty()
        current_text = ""

        for word in stream_data():
            current_text += word
            placeholder.text(current_text)

    with open('C:\\Users\\LENOVO\\Desktop\\Guvi Proj\\Phonepe\\data.gif', 'rb') as f:
        image_base64 = base64.b64encode(f.read()).decode()

    # Use HTML to center the image
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center;">
            <img src="data:image/gif;base64,{image_base64}" style="width: 50%;"/>
        </div>
        """,
        unsafe_allow_html=True
    )
    #st.image('data.gif', use_column_width=True)
    
    
elif selected == "EXPLORE":
    
    st.markdown("<h1 class='center-title'>EXPLORE</h1>", unsafe_allow_html=True)

    select = option_menu(None, options=["AGGREGATED", "MAP", "TOP"], default_index=0, orientation="horizontal", styles={"container": {"width": "100%"}, "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px"}, "nav-link-selected": {"background-color": "#663399"}})

    if select == "AGGREGATED":
        tab1, tab2 = st.tabs(["TRANSACTION", "USER"])

        with tab1:
            col1, col2, col3 = st.columns([1, 2, 3])

            with col1:
                agg_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022', '2023', '2024'), key='agg_yr')
            with col2:
                agg_quarter = st.selectbox('**Select Quarter**', ('1st Quarter', '2nd Quarter', '3rd Quarter', '4th Quarter'), key='agg_quarter')
            with col3:
                agg_trans_type = st.selectbox('**Select Transaction type**', ('Recharge & bill payments', 'Peer-to-peer payments', 'Merchant payments', 'Financial Services', 'Others'), key='agg_trans_type')

            mycursor.execute(f"SELECT States, TransactionAmount FROM df_aggregated_transaction WHERE Years = '{agg_yr}' AND Quarter = '{agg_quarter}' AND TransactionType = '{agg_trans_type}';")

            transaction_query = mycursor.fetchall()

            agg_transpd = pd.DataFrame(transaction_query, columns=['State', 'Transaction_amount'])

            agg_tran_output = agg_transpd.set_index(pd.Index(range(1, len(agg_transpd) + 1)))

            agg_transpd.drop(columns=['State'], inplace=True)

            url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response = requests.get(url)
            data1 = json.loads(response.content)

            state_names_tra = [feature['properties']['ST_NM'] for feature in data1['features']]
            state_names_tra.sort()

            df_state_names_tra = pd.DataFrame({'State': state_names_tra})

            df_state_names_tra['Transaction_amount'] = agg_transpd

            df_state_names_tra.to_csv('agg_trans.csv', index=False)

            agg_data = pd.read_csv('agg_trans.csv')

            fig_user = px.choropleth(
                agg_data,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='State',
                color='Transaction_amount',
                color_continuous_scale='balance',
                title='Transaction Amount Analysis')
            fig_user.update_geos(fitbounds="locations", visible=False)

            fig_user.update_layout(title_font=dict(size=33), title_font_color='white', height=750, geo=dict(
                scope='asia',
                projection=dict(type='mercator'),
                lonaxis=dict(range=[65.0, 100.0]),
                lataxis=dict(range=[5.0, 40.0])))

            st.plotly_chart(fig_user, use_container_width=True)

            agg_tran_output['State'] = agg_tran_output['State'].astype(str)
            agg_tran_output['Transaction_amount'] = agg_tran_output['Transaction_amount'].astype(float)

            fig1 = px.sunburst(agg_tran_output,
                               path=['State', 'Transaction_amount'],
                               values='Transaction_amount',
                               color='Transaction_amount',
                               color_continuous_scale='magma',
                               title='Transaction Amount Chart',
                               height=700)

            fig1.update_layout(title_font=dict(size=33), title_font_color='#FFFFFF')

            st.plotly_chart(fig1, use_container_width=True)

        with tab2:
            col1, col2 = st.columns([1, 2])

            with col1:
                agg_user_yr = st.selectbox('Select Year', ['2018', '2019', '2020', '2021', '2022', '2023', '2024'], key='agg_user_yr')

            with col2:
                if agg_user_yr == '2022':
                    in_us_qtr = st.selectbox('Select Quarter', ['1st Quarter'], key='in_us_qtr')
                else:
                    in_us_qtr = st.selectbox('Select Quarter', ['1st Quarter', '2nd Quarter', '3rd Quarter', '4th Quarter'], key='in_us_qtr')

            mycursor.execute(f"SELECT States, SUM(TransactionCount) AS Total_Count FROM df_aggregated_user WHERE Years = '{agg_user_yr}' AND Quarter = '{in_us_qtr}' GROUP BY States;")
            query2 = mycursor.fetchall()
            agg_userpd = pd.DataFrame(query2, columns=['State', 'User Count'])
            agg_user_output = agg_userpd.set_index(pd.Index(range(1, len(agg_userpd) + 1)))

            agg_userpd.drop(columns=['State'], inplace=True)
            url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response = requests.get(url)
            data2 = json.loads(response.content)
            state_names_user = [feature['properties']['ST_NM'] for feature in data2['features']]
            state_names_user.sort()
            user_state_names = pd.DataFrame({'State': state_names_user})
            user_state_names['User Count'] = agg_userpd['User Count']

            user_state_names.to_csv('user.csv', index=False)

            datas_gd = pd.read_csv('user.csv')

            fig_user = px.choropleth(
                datas_gd,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='State',
                color='User Count',
                color_continuous_scale='oxy',
                title='User Count Analysis')

            fig_user.update_geos(fitbounds="locations", visible=False)

            fig_user.update_layout(title_font=dict(size=33), title_font_color='white', height=750, geo=dict(scope='asia',
                                                                                                          projection=dict(type='mercator'), lonaxis=dict(range=[65.0, 100.0]), lataxis=dict(range=[5.0, 40.0])))

            st.plotly_chart(fig_user, use_container_width=True)

            mycursor.execute(f"SELECT Brands, SUM(TransactionCount) AS User_Count FROM df_aggregated_user WHERE Years = '{agg_user_yr}' AND Quarter = '{in_us_qtr}' GROUP BY Brands;")
            avg_df_aggregated_user = mycursor.fetchall()
            avg_userpd = pd.DataFrame(avg_df_aggregated_user, columns=['Brand', 'User Count'])
            avg_output = avg_userpd.set_index(pd.Index(range(1, len(avg_userpd) + 1)))
            avg_output['Brand'] = avg_output['Brand'].astype(str)
            avg_output['User Count'] = avg_output['User Count'].astype(int)
            avg_fig = px.bar(
                avg_output,
                x='Brand',
                y='User Count',
                color='User Count',
                color_continuous_scale='purpor',
                title='User Count Chart',
                height=700)

            avg_fig.update_layout(title_font=dict(size=33), title_font_color='white')
            st.plotly_chart(avg_fig, use_container_width=True)

    if select == "MAP":
        tab3, tab4 = st.tabs(["TRANSACTION", "USER"])

        with tab3:
            col1, col2, col3 = st.columns(3)
            with col1:
                map_st = st.selectbox('**Select State**', (
                    'Andaman-&-nicobar-islands', 'Andhra-pradesh', 'Arunachal-pradesh',
                    'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                    'Dadra-&-nagar-haveli-&-daman-&-diu', 'Delhi', 'Goa',
                    'Gujarat', 'Haryana', 'Himachal-pradesh', 'Jammu-&-kashmir',
                    'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                    'Madhya-pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                    'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                    'Sikkim', 'Tamil-nadu', 'Telangana', 'Tripura', 'Uttar-pradesh',
                    'Uttarakhand', 'West-bengal'), key='st_tr_st')
            with col2:
                map_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022', '2023', '2024'), key='st_tr_yr')
            with col3:
                map_qr = st.selectbox('**Select Quarter**', ('1st Quarter', '2nd Quarter', '3rd Quarter', '4th Quarter'), key='st_tr_qtr')

            mycursor.execute(f"SELECT Districts, TransactionCount FROM df_map_transaction WHERE States = '{map_st}' AND Years = '{map_yr}' AND Quarter = '{map_qr}';")
            mapquery = mycursor.fetchall()
            maptrans_df = pd.DataFrame(mapquery, columns=['Districts', 'TransactionCount'])
            map_tran_output = maptrans_df.set_index(pd.Index(range(1, len(maptrans_df) + 1)))

            map_tran_output['TransactionCount'] = map_tran_output['TransactionCount'].astype(int)

            map_fig = px.bar(map_tran_output, y='TransactionCount', x='Districts', title='Transaction Count Analysis by Districts')

            map_fig.update_layout(title_font=dict(size=33), title_font_color='white', font=dict(size=14), height=700, width=800)

            st.plotly_chart(map_fig, use_container_width=True)

            mycursor.execute(f"SELECT Districts, TransactionAmount FROM df_map_transaction WHERE States = '{map_st}' AND Years = '{map_yr}' AND Quarter = '{map_qr}';")
            maptransamt = mycursor.fetchall()
            maptransamt_df = pd.DataFrame(maptransamt, columns=['Districts', 'Transaction_amount'])
            map_tran_amtoutput = maptransamt_df.set_index(pd.Index(range(1, len(maptransamt_df) + 1)))

            map_tran_amtoutput['Transaction_amount'] = map_tran_amtoutput['Transaction_amount'].astype(float)

            pie_chart_fig = px.pie(map_tran_amtoutput, values='Transaction_amount', names='Districts',
                                   title='Transaction Amount Analysis by District', hole=0.4)

            pie_chart_fig.update_layout(title_font=dict(size=33), title_font_color='white', font=dict(size=14), height=700, width=800)
            st.plotly_chart(pie_chart_fig, use_container_width=True)

        with tab4:
            col1, col2, col3 = st.columns(3)
            with col1:
                map_st = st.selectbox('**Select State**', (
                    'Andaman-&-nicobar-islands', 'Andhra-pradesh', 'Arunachal-pradesh',
                    'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                    'Dadra-&-nagar-haveli-&-daman-&-diu', 'Delhi', 'Goa',
                    'Gujarat', 'Haryana', 'Himachal-pradesh', 'Jammu-&-kashmir',
                    'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                    'Madhya-pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                    'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                    'Sikkim', 'Tamil-nadu', 'Telangana', 'Tripura', 'Uttar-pradesh',
                    'Uttarakhand', 'West-bengal'), key='map_st')
            with col2:
                mapuser_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022', '2023', '2024'), key='mapuser_yr')
            with col3:
                mapuser_qr = st.selectbox('**Select Quarter**', ('1st Quarter', '2nd Quarter', '3rd Quarter', '4th Quarter'), key='mapuser_qr')

            mycursor.execute(f"SELECT Districts, RegisteredUsers FROM df_map_user WHERE States = '{map_st}' AND Years = '{mapuser_yr}' AND Quarter = '{mapuser_qr}';")
            mapuserquery = mycursor.fetchall()
            mapuser_df = pd.DataFrame(mapuserquery, columns=['Districts', 'RegisteredUsers'])
            map_useroutput = mapuser_df.set_index(pd.Index(range(1, len(mapuser_df) + 1)))

            map_useroutput['RegisteredUsers'] = map_useroutput['RegisteredUsers'].astype(float)

            mapuser_fig = px.scatter(map_useroutput, x='Districts', y='RegisteredUsers', title='RegisteredUsers Analysis by District')

            mapuser_fig.update_layout(title_font=dict(size=33), title_font_color='white', font=dict(size=14), height=700, width=800)

            st.plotly_chart(mapuser_fig, use_container_width=True)

            mycursor.execute(f"SELECT Districts, AppOpens FROM df_map_user WHERE States='{map_st}' AND Years = '{mapuser_yr}' AND Quarter = '{mapuser_qr}';")
            mapuserquery = mycursor.fetchall()
            map_users_df = pd.DataFrame(mapuserquery, columns=['Districts', 'AppOpens'])
            map_tran_useroutput = map_users_df.set_index(pd.Index(range(1, len(map_users_df) + 1)))

            map_tran_useroutput['AppOpens'] = map_tran_useroutput['AppOpens'].astype(float)

            line_mapchart_fig = px.line(map_tran_useroutput, x='Districts', y='AppOpens', title='AppOpens Analysis by Districts')

            line_mapchart_fig.update_layout(title_font=dict(size=33), title_font_color='white', font=dict(size=14), height=700, width=800)

            st.plotly_chart(line_mapchart_fig, use_container_width=True)

    if select == "TOP":
        tab5, tab6 = st.tabs(["TRANSACTION", "USER"])

        with tab5:
            col1, col2, col3 = st.columns(3)
            with col1:
                top_st = st.selectbox('**Select State**', (
                    'Andaman-&-nicobar-islands', 'Andhra-pradesh', 'Arunachal-pradesh',
                    'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                    'Dadra-&-nagar-haveli-&-daman-&-diu', 'Delhi', 'Goa',
                    'Gujarat', 'Haryana', 'Himachal-pradesh', 'Jammu-&-kashmir',
                    'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                    'Madhya-pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                    'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                    'Sikkim', 'Tamil-nadu', 'Telangana', 'Tripura', 'Uttar-pradesh',
                    'Uttarakhand', 'West-bengal'), key='top_st')
            with col2:
                top_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022', '2023', '2024'), key='top_yr')
            with col3:
                top_qr = st.selectbox('**Select Quarter**', ('1st Quarter', '2nd Quarter', '3rd Quarter', '4th Quarter'), key='top_qr')

            mycursor.execute(f"SELECT Pincodes, TransactionCount FROM df_top_transaction WHERE States = '{top_st}' AND Years = '{top_yr}' AND Quarter = '{top_qr}';")
            topcountquery = mycursor.fetchall()
            toptrans_df = pd.DataFrame(topcountquery, columns=['Pincodes', 'TransactionCount'])
            toptrans_output = toptrans_df.set_index(pd.Index(range(1, len(toptrans_df) + 1)))

            toptrans_output['Pincodes'] = toptrans_output['Pincodes'].astype(float)
            toptrans_output['TransactionCount'] = toptrans_output['TransactionCount'].astype(int)

            toptrans_pie_fig = px.pie(toptrans_output, values='TransactionCount', names='Pincodes', color_discrete_sequence=px.colors.sequential.ice, title='Pincodes')

            toptrans_pie_fig.update_layout(title_font=dict(size=33), title_font_color='white', font=dict(size=14), height=700, width=800)

            st.plotly_chart(toptrans_pie_fig, use_container_width=True)

            mycursor.execute(f"SELECT States, SUM(TransactionAmount) FROM df_top_transaction WHERE Years = '{top_yr}' AND Quarter = '{top_qr}' GROUP BY States;")
            top_transc_query = mycursor.fetchall()
            df_top_transc_query = pd.DataFrame(top_transc_query, columns=['States', 'Transaction amount'])
            df_top_transc_result = df_top_transc_query.set_index(pd.Index(range(1, len(df_top_transc_query) + 1)))

            df_top_transc_query.drop(columns=['States'], inplace=True)

            url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response = requests.get(url)
            data5 = json.loads(response.content)

            top_state_names_use = [feature['properties']['ST_NM'] for feature in data5['features']]
            top_state_names_use.sort()

            df_state_names_use = pd.DataFrame({'State': top_state_names_use})

            df_state_names_use['Transaction amount'] = df_top_transc_query

            df_state_names_use.to_csv('State_tr_amt.csv', index=False)

            df_use = pd.read_csv('State_tr_amt.csv')

            top_fig_use = px.choropleth(df_use, geojson=data5, featureidkey='properties.ST_NM', locations='State', color='Transaction amount', color_continuous_scale='purpor', title='Transaction amount Analysis')

            top_fig_use.update_geos(fitbounds="locations", visible=False)

            top_fig_use.update_layout(title_font=dict(size=33), title_font_color='white', height=750, geo=dict(scope='asia',
                                                                                                             projection=dict(type='mercator'), lonaxis=dict(range=[65.0, 100.0]), lataxis=dict(range=[5.0, 40.0])))

            st.plotly_chart(top_fig_use, use_container_width=True)

        with tab6:
            col1, col2, col3 = st.columns(3)
            with col1:
                topuser_st = st.selectbox('**Select State**', (
                    'Andaman-&-nicobar-islands', 'Andhra-pradesh', 'Arunachal-pradesh',
                    'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                    'Dadra-&-nagar-haveli-&-daman-&-diu', 'Delhi', 'Goa',
                    'Gujarat', 'Haryana', 'Himachal-pradesh', 'Jammu-&-kashmir',
                    'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                    'Madhya-pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                    'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                    'Sikkim', 'Tamil-nadu', 'Telangana', 'Tripura', 'Uttar-pradesh',
                    'Uttarakhand', 'West-bengal'), key='topuser_st')
            with col2:
                topuser_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022', '2023', '2024'), key='topuser_yr')
            with col3:
                topuser_qr = st.selectbox('**Select Quarter**', ('1st Quarter', '2nd Quarter', '3rd Quarter', '4th Quarter'), key='topuser_qr')

            mycursor.execute(f"SELECT States, Pincodes, SUM(RegisteredUsers) as RegisteredUsers FROM df_top_user WHERE States='{topuser_st}' AND Years = '{topuser_yr}' AND Quarter = '{topuser_qr}' GROUP BY States, Pincodes;")
            top_user_query = mycursor.fetchall()
            df_top_user_query = pd.DataFrame(top_user_query, columns=['States', 'Pincodes', 'RegisteredUsers'])
            df_top_user_result = df_top_user_query.set_index(pd.Index(range(1, len(df_top_user_query) + 1)))

            topuser_fig = px.sunburst(df_top_user_result, path=['States', 'Pincodes', 'RegisteredUsers'], values='RegisteredUsers', color='RegisteredUsers', color_continuous_scale='gray', title='RegisteredUsers Chart', height=700, labels={'Pincodes': 'Pincode'})

            topuser_fig.update_layout(title_font=dict(size=33), title_font_color='white')

            st.plotly_chart(topuser_fig, use_container_width=True)

elif selected == 'INSIGHTS':
    st.toast('Created by Yabase Immanuel', icon='🤖')
    st.markdown("<h1 class='center-title'>INSIGHTS</h1>", unsafe_allow_html=True)

    options = ["--Select any of the Questions--",
               "1.Does the number of transactions vary based on different PIN codes?",
               "2.How does the Count vary by brand(e.g., Xiaomi, Samsung, Apple)?",
               "3.How did transaction percentages vary among different states in 2022?",
               "4.List the top 5 states in India with the highest transaction amount?",
               "5.What is the highest transaction amount recorded for the years 2018 and 2024?",
               "6.Which districts have the highest Transaction Count?",
               "7.Could you list the ten states with the fewest registered users and their respective PIN codes?",
               "8.What district had the most significant number of AppOpens?",
               "9.Among all the pin codes, which one has the lowest transaction count?",
               "10.What is the highest transaction amount recorded for each transaction type?"]

    select = st.selectbox("Select the option", options)

    if select == "1.Does the number of transactions vary based on different PIN codes?":
        mycursor.execute("SELECT Pincodes, AVG(TransactionCount) AS Avg_TransactionCount FROM df_top_transaction GROUP BY Pincodes")
        data = mycursor.fetchall()
        df = pd.DataFrame(data, columns=['Pincodes', 'Avg_TransactionCount'])
        fig = px.line(df, x='Pincodes', y='Avg_TransactionCount', title='Transaction Count Across Different Pincodes')
        fig.update_xaxes(type='category')
        st.plotly_chart(fig, use_container_width=True)

    elif select == "2.How does the Count vary by brand(e.g., Xiaomi, Samsung, Apple)?":
        mycursor.execute("SELECT Brands, SUM(TransactionCount)AS total_count FROM df_aggregated_user GROUP BY Brands;")
        data = mycursor.fetchall()
        df = pd.DataFrame(data, columns=['Brands', 'total_count'])
        ques2 = px.sunburst(df, path=['Brands', 'total_count'], values='total_count', color='total_count',
                            color_continuous_scale='gnbu', title='Brand Count Chart', height=700)
        ques2.update_layout(title_font=dict(size=33), title_font_color='#483D8B')
        st.plotly_chart(ques2, use_container_width=True)

    elif select == "3.How did transaction percentages vary among different states in 2022?":
        mycursor.execute("SELECT States, Years, MAX(Percentage) as Percentage FROM df_aggregated_user WHERE Years = 2022 GROUP BY States, Years ORDER BY States, Percentage DESC;")
        results = mycursor.fetchall()
        df = pd.DataFrame(results, columns=['State', 'Year', 'Percentage'])
        fig = px.scatter(df, x="State", y="Percentage", color="State", title="Percentage by State in 2022",
                         labels={"Percentage": "Percentage", "State": "State"},
                         category_orders={"State": sorted(df['State'].unique())})
        fig.update_traces(mode='markers+lines')
        st.plotly_chart(fig)

    elif select == "4.List the top 5 states in India with the highest transaction amount?":
        mycursor.execute("SELECT States, SUM(TransactionAmount) AS total_amount FROM df_map_transaction GROUP BY States ORDER BY total_amount DESC LIMIT 5;")
        results = mycursor.fetchall()
        df = pd.DataFrame(results, columns=['State', 'total_amount'])
        fig = px.histogram(df, x="State", y="total_amount", title="Top 5 States by Total Transaction Amount",
                           labels={"total_amount": "Total Transaction Amount", "State": "State"},
                           category_orders={"State": sorted(df['State'].unique())})
        st.plotly_chart(fig, use_container_width=True)

    elif select == "5.What is the highest transaction amount recorded for the years 2018 and 2024?":
        mycursor.execute("SELECT Years, TransactionType, MAX(TransactionAmount) as TransactionAmount FROM df_aggregated_transaction WHERE Years IN ('2018','2019','2020','2021','2022','2023','2024') GROUP BY Years, TransactionType;")
        results = mycursor.fetchall()
        df = pd.DataFrame(results, columns=['Years', 'TransactionType', 'TransactionAmount'])

        fig = px.scatter(df, x="TransactionAmount", y="TransactionType", animation_frame="Years", animation_group="Years",
                         color="TransactionType", hover_name="TransactionType", log_x=True,
                         range_x=[1, df['TransactionAmount'].max()],
                         labels={"TransactionAmount": "Transaction Amount", "Years": "Year"},
                         title="Highest Transaction Amount for 2018 and 2024 by Transaction Type")

        fig.update_yaxes(categoryorder='total ascending')
        st.plotly_chart(fig, use_container_width=True)

    elif select == "6.Which districts have the highest Transaction Count?":
        mycursor.execute("SELECT Districts,TransactionCount as Count FROM df_map_transaction ORDER BY TransactionCount DESC LIMIT 10;")
        data = mycursor.fetchall()
        df = pd.DataFrame(data, columns=['Districts', 'Count'])
        ques6 = px.sunburst(df, path=['Districts', 'Count'], values='Count', color='Count', color_continuous_scale='speed',
                            title='District Transaction Count Chart', height=700)
        ques6.update_layout(title_font=dict(size=33), title_font_color='#20B2AA')
        st.plotly_chart(ques6, use_container_width=True)

    elif select == "7.Could you list the ten states with the fewest registered users and their respective PIN codes?":
        mycursor.execute("SELECT States,Pincodes,SUM(RegisteredUsers)AS Users FROM df_top_user GROUP BY States,Pincodes ORDER BY Users ASC LIMIT 10;")
        data = mycursor.fetchall()
        df = pd.DataFrame(data, columns=['State', 'Pincodes', 'RegisteredUsers'])
        fig = px.bar(df, x='State', y='RegisteredUsers', color='Pincodes', title='Least 10 States and Pincodes based on Registered Users')
        st.plotly_chart(fig, use_container_width=True)

    elif select == "8.What district had the most significant number of AppOpens?":
        mycursor.execute("SELECT Districts, AVG(AppOpens)AS AvgAppOpens FROM df_map_user GROUP by Districts ORDER BY AvgAppOpens DESC LIMIT 15;")
        results = mycursor.fetchall()
        df = pd.DataFrame(results, columns=['Districts', 'AvgAppOpens'])
        fig = px.line(df, x='Districts', y='AvgAppOpens', title='Average App Opens by District')
        st.plotly_chart(fig, use_container_width=True)

    elif select == "9.Among all the pin codes, which one has the lowest transaction count?":
        mycursor.execute("SELECT Pincodes, MIN(TransactionCount) AS Least_Count FROM df_top_transaction GROUP BY Pincodes ORDER by Least_Count DESC LIMIT 15;")
        data = mycursor.fetchall()
        df = pd.DataFrame(data, columns=['Pincodes', 'Least_Count'])
        pie_chart = px.pie(df, values='Least_Count', names='Pincodes', title='Least Count Distribution by Pincodes')
        pie_chart.update_layout(title_font=dict(size=33), title_font_color='#F5F5F5')
        st.plotly_chart(pie_chart, use_container_width=True)

    elif select == "10.What is the highest transaction amount recorded for each transaction type?":
        mycursor.execute("SELECT TransactionType, MAX(TransactionAmount) AS Highest_amount FROM df_aggregated_transaction GROUP BY TransactionType ORDER by Highest_amount DESC;")
        lastqry = mycursor.fetchall()
        df = pd.DataFrame(lastqry, columns=['Transaction_type', 'Highest_amount'])
        st.dataframe(df)
        fig = px.bar(df, x='Transaction_type', y='Highest_amount', title='Highest Transaction Amount by Transaction Type', labels={'Transaction_type': 'Transaction Type', 'Highest_amount': 'Highest Amount'})
        fig.update_layout(xaxis_title='Transaction Type', yaxis_title='Highest Amount', title_font=dict(size=25), title_font_color='#0000CD')
        st.plotly_chart(fig, use_container_width=True)
