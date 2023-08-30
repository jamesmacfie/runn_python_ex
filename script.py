import os
from dotenv import load_dotenv
from typing import Union
import streamlit as st
from streamlit_modal import Modal
import requests

load_dotenv()

API_KEY = os.getenv('RUNN_API_KEY')
API_URL = os.getenv('RUNN_API_URL')


def create_role(*, name: str, default_hour_cost: Union[float, int], standard_rate: Union[float, int]):
  url = f"{API_URL}/v0/roles"
  headers = {
      "Authorization": API_KEY,
      "Content-Type": "application/json"
  }
  data = dict(name=name, default_hour_cost=default_hour_cost, standard_rate=standard_rate)

  # For reference, here's the data we're sending to the API
  st.info(f"""
    Data we're sending to the API:
    ```json
    {{
      name: {name},
      "default_hour_cost": {default_hour_cost},
      "standard_rate": {standard_rate}
    }} 
    ```

    And their types:
    ```json
    {{
      name: {type(name)},
      "default_hour_cost": {type(default_hour_cost) },
      "standard_rate": {type(standard_rate)}
    }} 
    ```
  """)

  return requests.post(url, json=data, headers=headers)

def render_form():
  id = None

  with st.form("my_form"):
    float_or_int = st.radio(
      "Do you want to use floats or ints for sending the cost to the API?",
      ["float", "int"])
  
    name = st.text_input("Name")

    is_float = float_or_int == "float"
    default_hour_cost = st.number_input("Default hour cost", step = 0.01 if is_float else 1)
    standard_rate = st.number_input("Standard rate", step = 0.01 if is_float else 1)
    

    submitted = st.form_submit_button("Submit")
    if submitted:
        role_response = create_role(name=name, default_hour_cost=default_hour_cost, standard_rate=standard_rate)
        if role_response.status_code != 201:
          st.write(f"Error creating role: {role_response.json().get('error')}")
        else:
          id = role_response.json().get('id')
          st.write(f"Successfully created role with id '{id}'")
          

st.title('Runn POC')
with st.container():
  st.header('Create a role')
  st.text(f"Using API endpoint: {API_URL}")
  render_form()
