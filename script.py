import os
import json
from dotenv import load_dotenv
from typing import Union
import streamlit as st
import requests

load_dotenv()

API_KEY = os.getenv('RUNN_API_KEY')
API_URL = os.getenv('RUNN_API_URL')

def get_clients():
  url = f"{API_URL}/v0/clients"
  headers = {
      "Authorization": API_KEY,
      "Content-Type": "application/json"
  }
  return requests.get(url, headers=headers).json()

def get_roles():
  url = f"{API_URL}/v0/roles"
  headers = {
      "Authorization": API_KEY,
      "Content-Type": "application/json"
  }
  return requests.get(url, headers=headers).json()

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
          
    {json.dumps(data, indent=4)}

    And their types:

    name: {type(name)},
    default_hour_cost: {type(default_hour_cost) },
    standard_rate: {type(standard_rate)}
    ```
  """)

  return requests.post(url, json=data, headers=headers)


def render_role_form():
  st.text("This demonstrates passing a simple float or in to an endpoint")
  with st.form("role_form"):
    float_or_int = st.radio(
      "Do you want to use floats or ints for sending the cost to the API?",
      ["float", "int"])
  
    name = st.text_input("Role Name")

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
          

def create_project(*, name: str, client_id: str, role_id: str, hourly_rate: Union[float, int], budget: Union[float, int]):
  url = f"{API_URL}/v0/projects"
  headers = {
      "Authorization": API_KEY,
      "Content-Type": "application/json"
  }
  data = dict(name=name, client_id=client_id, role_id=role_id, project_rates=[dict(role_id=role_id, rate_hourly=hourly_rate)], budget=budget)

  # For reference, here's the data we're sending to the API
  st.info(f"""
    Data we're sending to the API:
          
    {json.dumps(data, indent=4)} 

    And their types:
    
    name: {type(name)},
    client_id: {type(client_id)},
    role_id: {type(role_id)},
    hourly_rate: {type(hourly_rate)},
    budget: {type(budget)}
    
  """)

  print(data)

  return requests.post(url, json=data, headers=headers)

def render_project_form():
  with st.form("project_form"):
    st.text("""
            This demonstrates more advanced usage, sending an list of values that
            contains a float or int. We're only sending a list of size one, only
            because I'm lazy and it was simple.
            """)
    clients = get_clients()
    roles = get_roles()
    
    float_or_int = st.radio(
      "Do you want to use floats or ints for sending the cost to the API?",
      ["float", "int"])
  
    name = st.text_input("Project Name")
    client_id = st.selectbox("Client", [client.get('id') for client in clients], format_func=lambda id: next(client.get('name') for client in clients if client.get('id') == id))
    role_id = st.selectbox("Role", [role.get('id') for role in roles], format_func=lambda id: next(role.get('name') for role in roles if role.get('id') == id))
    role =  next((role for role in roles if role.get("id") == role_id), None)

    is_float = float_or_int == "float"
    hourly_rate = st.number_input(f"Hourly_rate for {role.get('name') if role else '...'}", step = 0.01 if is_float else 1)
    budget = st.number_input("Project budges", step = 0.01 if is_float else 1)
    
    submitted = st.form_submit_button("Submit")
    if submitted:
        project_response = create_project(name=name, client_id=client_id, role_id=role_id, hourly_rate=hourly_rate, budget=budget)
        if project_response.status_code != 201:
          st.write(f"Error creating project: {project_response.json().get('error')}")
        else:
          id = project_response.json().get('id')
          st.write(f"Successfully created project with id '{id}'")


st.title('Runn POC')
with st.container():
  st.header('Create a role or project')
  st.text(f"Using API endpoint: {API_URL}")
  role_tab, project_tab = st.tabs(["Role", "Project"])
  with role_tab:
    render_role_form()

  with project_tab:
    render_project_form()