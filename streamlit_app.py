# Import python packages
import streamlit as st
import os
from snowflake.snowpark.functions import col,when_matched

# Write directly to the app
st.title(f"Custom Your Smoothie")
st.write("Choose the fruits you want in your custom smoothie")


name_on_order = st.text_input("Name on Smoothie:")
st.write("The Name on your Smoothie will be", name_on_order)


cnx=st.connection("snowflake")
session=cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    "Choose upto 5 ingridents:",
    my_dataframe,
    max_selections=5    
)

if ingredients_list:
   ingredient_string=''

   for fruit_chosen in ingredients_list:
        ingredient_string+=fruit_chosen+' '
   # st.write(ingredient_string)

   my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                        values ('""" + ingredient_string + """','""" + name_on_order + """')"""

   time_to_insert=st.button('Submit Order')


                        

   if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")

import requests

smoothiefroot_response = requests.get(
    "https://my.smoothiefroot.com/api/fruit/watermelon"
)
sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
   



        

