# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

name_on_order=st.text_input('Name on Smoothie:')
st.write('Name on smoothie will be',name_on_order)
cnx=st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
pd_df=my_dataframe.to_pandas()
# st.dataframe(data=my_dataframe,use_container_width=True)
# st.stop()

ingredients_list=st.multiselect('Choose up to 5 ingdredients',my_dataframe,max_selections=5)

if ingredients_list:
    ingredients_string=''
    for f in ingredients_list:
        ingredients_string+=f+' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME']==f,'SEARCH_ON'].iloc[0]
        st.write('The search value for ',f,' is ',search_on,' .')
        st.subheader(f+' Nutrition information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+search_on)
        sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
        
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order +"""')"""
    time_to_insert=st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered,"name_on_order"!', icon="✅")
        


