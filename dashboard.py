import streamlit as st 
import plotly.express as px 
import pandas as pd 
import os 
import warnings 
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Analysis!!!", page_icon=":bar_chart:", layout="wide")

st.title(" :bar_chart: GenHealth Claims_Analysis EDA")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>' ,unsafe_allow_html=True)

fl = st.file_uploader(":file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename, encoding= "ISO-8859-1")
else:
    os.chdir(r"C:\Users\sh0556\OneDrive - Generation Health\Desktop\school documents\Africa Data School\Project")
    df=pd.read_csv("Analysis.csv", encoding= "ISO-8859-1")
    
col1, col2 = st.columns((2))
df["AssessDate"]= pd.to_datetime(df["AssessDate"])

# Getting the min and max date
startDate = pd.to_datetime(df["AssessDate"]).min()
endDate = pd.to_datetime(df["AssessDate"]).max()

with col1:
    date1=pd.to_datetime(st.date_input("Start Date", startDate))
    
with col2:
    date2=pd.to_datetime(st.date_input("End Date", endDate))
    
df = df[(df["AssessDate"] >= date1) & (df["AssessDate"] <= date2)].copy()

# Create for plan
st.sidebar.header("Choose your filter: ") 
plan = st.sidebar.multiselect("Choose Plan Name", df["Option Name"].unique())
if not plan:
    df2 = df.copy()
else:
    df2 = df[df["Option Name"].isin(plan)]

# Create for benefit 
benefit = st.sidebar.multiselect("Choose Benefit Name", df2["Base Benefit Description"].unique())
if not benefit:
    df3 = df2.copy()
else:
     df3 = df2[df["Base Benefit Description"].isin(benefit)]

# Create for provider
provider = st.sidebar.multiselect("Choose the Provider", df3["Provider Name"].unique())

# Filter the data based on Product Plan, Benefit and Provider 

if not plan and not benefit and not provider:
    filtered_df = df
elif not benefit and not provider:
    filtered_df = df[df["Option Name"].isin(plan)]
elif not plan and not provider:
    filtered_df = df[df["Base Benefit Description"].isin(benefit)]
elif benefit and provider:
    filtered_df = df3[df["Base Benefit Description"].isin(benefit) & df3["Provider Name"].isin(provider)]     
elif plan and provider:
    filtered_df = df3[df["Option Name"].isin(plan) & df3["Provider Name"].isin(provider)]  
elif plan and benefit:
    filtered_df = df3[df["Option Name"].isin(plan) & df3["Base Benefit Description"].isin(benefit)]  
elif provider:
    filtered_df = df3[df3["Provider Name"].isin(provider)]
else:
    filtered_df = df3[df3["Option Name"].isin(plan) & df3["Base Benefit Description"].isin(benefit) & df3["Provider Name"].isin(provider)]

category_df = filtered_df.groupby(by = ["Category"], as_index = False)["TotalPaid"].sum()


with col1:
    st.subheader("Claims per age")
    fig = px.bar(category_df, x ="Category", y = "TotalPaid", text = ['${:,.0f}'.format(x) for x in category_df["TotalPaid"]], template="seaborn")
    st.plotly_chart(fig,use_container_width=True, height = 200) 
    

with col2:
    st.subheader("Claims per benefit")
    fig = px.pie(filtered_df, values = "TotalPaid", names = "Option Name", hole = 0.5)
    fig.update_traces(text = filtered_df["Option Name"], textposition= "inside")
    st.plotly_chart(fig,use_container_width=True)

cl1, cl2 =st.columns(2)
with cl1:
    with st.expander("Category_ViewData"):
         st.write(category_df.style.background_gradient(cmap="Blues"))
         csv= category_df.to_csv(index = False).encode('utf-8')
         st.download_button("Download Data", data=csv, file_name = "Category.csv", mime = "text/csv",
                           help = 'Click here to download the data as a CSV file')
        
with cl2:
    with st.expander("Option Name_ViewData"):
         plan = filtered_df.groupby(by = "Option Name", as_index = False)["TotalPaid"].sum()
         st.write(plan.style.background_gradient(cmap="Oranges"))
         csv= category_df.to_csv(index = False).encode('utf-8')
         st.download_button("Download Data", data=csv, file_name = "Option Name.csv", mime = "text/csv",
                           help = 'Click here to download the data as a CSV file')
    
filtered_df["assessed_year"]= filtered_df["AssessDate"].dt.to_period("M")
st.subheader('Time series Analysis')

linechart = pd.DataFrame(filtered_df.groupby(filtered_df["assessed_year"].dt.strftime("%Y : %b"))["TotalPaid"].sum()).reset_index()
fig2 = px.line(linechart, x = "assessed_year", y= "TotalPaid", labels = {"TotalPaid": "Amount"}, height=500, width = 1000, template="gridon")
st.plotly_chart(fig2, use_container_width=True)

with st.expander("View Data of Time Series:"):
    st.write(linechart.T.style.background_gradient(cmap="Blues"))
    csv = linechart.to_csv(index=False).encode("utf-8")
    st.download_button('Downlaod Data', data = csv, file_name = "TimeSeries.csv", mime = 'text/csv')

# Create a treem based on Plan, Category and Benefit
# st.subheader("Hierarchial view os Claims Using TreeMap")
# fig3= px.treemap(filtered_df, path =["Option Name", "Category", "Paper/ Edi" ], values = "Total Paid",hover_data = ["Total Paid"],
#                  color = "Option Name")
# fig3.update_layout(width =800, height =650)
# st.plotly_chart(fig3, use_container_width=True )


# chart1, chart2 = st.columns (3)
# with chart1:
#     st.subheader("Claims per provider")
#     fig = px.pie(filtered_df, values = "TotalPaid", names = "Base Benefit Description", template = "plotly_dark")
#     fig.update_traces(text = filtered_df["Base Benefit Description"], textposition= "inside")
#     st.plotly_chart(fig,use_container_width=True)

category_df = filtered_df.groupby(by = ["Category"], as_index = False)["Amount Claimed"].sum()

col1, col2 = st.columns (2)
with col1:
    st.subheader("Amounts claimed per age")
    fig = px.bar(category_df, x ="Category", y = "Amount Claimed", text = ['${:,.0f}'.format(x) for x in category_df["Amount Claimed"]], template="seaborn")
    st.plotly_chart(fig,use_container_width=True, height = 200) 
    

with col2:
    st.subheader("Claimed amounts per plan")
    fig = px.pie(filtered_df, values = "Amount Claimed", names = "Option Name", hole = 0.5)
    fig.update_traces(text = filtered_df["Option Name"], textposition= "inside")
    st.plotly_chart(fig,use_container_width=True)


