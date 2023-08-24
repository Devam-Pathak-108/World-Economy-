import streamlit as st
import pandas as pd

Nav=st.sidebar.radio('Navigation',["Home",'Normal Analysis','Compare Countries',"Get GDP","Get difference"])

#Reading the Data!
Raw_df=pd.read_csv("World_Bank.csv")
#Removing useless columns
Raw_df=Raw_df.iloc[:,:-1]

#Removing the nan values
for i in range(len(Raw_df)):
    Raw_df.iloc[i,4:]=Raw_df.iloc[i,4:].fillna(Raw_df.iloc[i,4:].mean())
    
#As this is GDP outliers Don't Exists
# Making Proper Data file

Data=Raw_df.drop(columns=['Country Code','Indicator Name','Indicator Code'])
# Row to Columns
Data=Data.T
# All countrys list
All_country=list(Data.iloc[0,:])
# Selecting the country

if Nav=="Home":
    st.header('Welcome to GDP Calculator')
    st.image('GDP.jpg')
    st.write('Normal Analysis   - Givies the Plots of Selected Countries GDP')
    st.write('Compare Countries - Gives the Mixed plots to Compare between Countries')
    st.write('Get difference    - Gives the Difference in same country according to time given')

if Nav=='Normal Analysis':

    selected_country=st.sidebar.selectbox("Select Country",All_country)
        
    # plot
    for i in range(len(All_country)):
        if selected_country==All_country[i]:
            st.write('### :blue[Line Chart]')
            st.line_chart(Data.iloc[1:,i])
            st.write("### :blue[ Bar Chart]")
            st.bar_chart(Data.iloc[1:,i])
            st.write("### :blue[Area Chart]")
            st.area_chart(Data.iloc[1:,i])
            
if Nav=='Compare Countries':
    
    #geting the Countries form user
    selected_country=st.sidebar.multiselect("Select Country",All_country)
    
    Country_df=pd.DataFrame({ })
    # select msg
    temp=st.empty()
    temp.write("# Select Countries")
    
    #makeing df to display
    for i in range(len(All_country)):
        for j in selected_country:
            if j==All_country[i]:
                Country_df.insert(len(Country_df.columns),j,Data.iloc[1:,i])
    #removing Select msg
    if len(Country_df)>0:
        temp.empty()
        
    #ploting all
    st.write('### :blue[Line Chart]')
    st.line_chart(Country_df)
    st.write("### :blue[ Bar Chart]")
    st.bar_chart(Country_df)
    st.write("### :blue[Area Chart]")
    st.area_chart(Country_df)
                
if Nav =="Get GDP":
    Country=st.selectbox('Country',Data.iloc[0,:])
    year1_raw=None
    year1_raw=st.text_input("Year 1")
    
    try:
        for i in range(len(Data)):
            if Data[i][0]==Country:
                Year1=Data.loc[[year1_raw],i]
        st.write('GDP :', str(Year1[0]))
    except:
        if year1_raw!=None:
            st.write("Enter Valid Value")

if Nav=='Get difference':
    
    Country=st.selectbox('Country',Data.iloc[0,:])
    year1_raw=st.text_input("Year 1")
    year2_raw=st.text_input('Year 2')
    
    if year1_raw and year2_raw:
        if int(year1_raw)<=int(year2_raw):
            if Country:
                st.write("The Difference between Year "+year1_raw+" and "+year2_raw+" GDP is:")
                try:
                    for i in range(len(Data)):
                        if Data[i][0]==Country:
                            Year1=Data.loc[[year1_raw],i]
                            Year2=Data.loc[[year2_raw],i]
                except:
                    st.error('Enter proper Values')
                        
                if Year1[0]-Year2[0]>=0:
                    st.metric(label="📈 GDP Growth",value=str(Year1[0]),delta=str(int(-(Year1[0]-Year2[0]/Year1[0]*100)))+'%')
                if Year1[0]-Year2[0]<0:
                    st.metric(label="📉 GDP Loss",value=str(Year1[0]),delta=str(int((Year1[0]-Year2[0]/Year1[0]*100)))+'%')
                
        else:
            st.error('Enter proper Format -> Year 1 < Year 2')
