# Python - creating a role in Runn

This example repo exists only to show both a Python `int` and `float` being passed
through to Runn's API where the API docs show that the incoming data must be of type
`float`. It uses [Streamlit](https://streamlit.io/) to make the process of building
the UI simple. 

## Running

### Create and enter a virtual environment 

You don't have to do this but I  it.

```
python3 -m venv venv

source venv/bin/activate
```

### Install deps

```
pip install -r requirements.txt
```

### Sort out your env vars

Copy the sample variables

```
cp .env.sample .env
```

And change the values to be correct (the sample uses a localdev server, the production
API for Runn is `https://app.runn.io/api`). You'll need to get your API Key from the
UI

## Run it

In your terminal:

```
streamlit run script.py
``````

