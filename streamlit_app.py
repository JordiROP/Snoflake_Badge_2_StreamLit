import streamlit
import pandas
import snowflake.connector
import requests
from urllib.error import URLError

def get_fruityvice_data(fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  return pandas.json_normalize(fruityvice_response.json())

def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
    return my_cur.fetchall()

def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into pc_rivery_db.public.fruit_load_list VALUE(" + new_fruit + ")")
    return "Thanx for adding " + new_fruit

streamlit.title("My Parents New Healthy Dinner")

streamlit.header("Breakfast Favorites")
streamlit.text("🥣 Omega 3 & Blueberry Oatmeal")
streamlit.text("🥗 Kale, Spinach & Rocket Smoothie")
streamlit.text("🐔 Hard-Boiled Free-Range Egg")
streamlit.text("🥑🍞 Avocado Toast")

streamlit.header("🍌🥭 Build Your Own Fruit Smoothie 🥝🍇")

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')


fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ["Avocado", "Strawberries"])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
if not fruit_choice:
  streamlit.error('Please select a fruit to get information')
else:
  streamlit.write('The user entered ', fruit_choice)
  streamlit.dataframe(get_fruityvice_data(fruit_choice))

if streamlit.button('Get Fruit Load List'):
  streamlit.text("The fruitload list contains")
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  streamlit.dataframe(get_fruit_load_list())

try:
  add_fruit = streamlit.text_input('What fruit would you like information about?')
  if streamlit.button('Add Fruit to List'):
    if not add_fruit:
      streamlit.error('Please select a fruit to get information')
    else:
      my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
      streamlit.text(insert_row_snowflake(add_fruit))
except URLError as e:
  streamlit.error()
  #streamlit.write('The user added ', add_fruit)
  #my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values (" + add_fruit + ")")
