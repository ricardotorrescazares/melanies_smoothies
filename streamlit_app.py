# Import python packages
import streamlit as st
import requests
# from snowflake.snowpark.context import get_active_session   -- ESTA LINEA SE COMENTA, SOLO SIRVE PARA SiS, NO PARA SniS
#Function COL
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your **custom Smoothie!**
  """
)


name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)


#option = st.selectbox(
#    "How would you like to be contacted?",
#    ("Email", "Home phone", "Mobile phone"),
#)

#st.write("You selected:", option)


#option = st.selectbox(
#    "What is your favorite fruit?",
#    ("Banana", "Strawberries", "Peaches"),
#    index=None,
#    placeholder="Select the fruit...",
#)

#st.write("Your favorite fruit is:", option)



# If the line session = get_active_session() appears in your code two times, delete one of the lines. 



##Se agrega éste bloque para su uso en GitHub (SniS)
cnx = st.connection("snowflake")
session = cnx.session()
##

#session = get_active_session()    -- ESTA LINEA SE COMENTA, SOLO SIRVE PARA SiS, NO PARA SniS

# Display the Fruit Options List in Your Streamlit in Snowflake (SiS) App. 
#my_dataframe = session.table("smoothies.public.fruit_options") st.dataframe(data=my_dataframe, use_container_width=True)  *This line selects all the columns of the table
#my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')) st.dataframe(data=my_dataframe, use_container_width=True) * This line use only selected columns

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect(
    'Chose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)


# Se whats going on in the background (LIST vs list);

if ingredients_list: #Si la lista tiene valores, muestrala, si no, no
    #st.write( ingredients_list)
    #st.text(ingredients_list)

    ingredients_string = ''  #Creates a variable to store the string of the list. Indentation is important


# Create a Place to Store Order Data (EXCECUTE IN WORKSHEET)

    for fruit_chosen in ingredients_list:  #Means: for each fruit_chosen in ingredients_list multiselect box: do everything below this line that is indented. 
        ingredients_string += fruit_chosen +  ' ' #The += operator means "add this to what is already in the variable" so each time the FOR Loop is repeated, a new fruit name is appended to the existing string. 
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    #st.write(ingredients_string) #The st.write() command should be part of the IF block but not part of the FOR Loop.


    #SQL Insert Statement
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+ """')"""

    #st.write(my_insert_stmt)
    #st.stop()  #Stop commant for troubleshooting. Get the SAL before the app tries to write to the database

    #Insert the Order into Snowflake
    
    #if ingredients_string:
    #    session.sql(my_insert_stmt).collect()
    #    
    #    st.success('Your Smoothie is ordered!', icon="✅")


    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered' + ', ' + name_on_order +'!', icon="✅")

# New section to display smoothiefroot nutrition information
# import requests --Line moved to the top of the code
# smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon") -- Line moved to the fruit_chosen block.
# st.text(smoothiefroot_response.json())
# sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)  -- Line moved to the fruit_chosen block.
