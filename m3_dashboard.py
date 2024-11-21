# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
launch_sites = spacex_df['Launch Site'].unique()  # Get unique launch site names

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(
    children=[
        html.H1(
            'SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36','font-size': 40}
        ),

        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        dcc.Dropdown(
            id='site-dropdown',
            options=[
                {'label':'All Sites', 'value':'ALL'},
            ] + [{'label': site, 'value': site} for site in launch_sites],  # Dynamically generated options
            value='ALL', #with default dropdown value to be ALL (meaning all sites are selected)
            placeholder='Select a Launch Site here', #show a text description about this input area
            searchable=True # so we can enter keywords to search launch sites
        ),
        html.Br(), # (just a line break)

        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(
            dcc.Graph(
                id='success-pie-chart',
                figure={} # Initial empty figure, will be updated via callback
                # This is dynamically updated by the `update_pie_chart` function
            )
        ),
        html.Br(),
        html.P("Payload range (Kg):"),

        # TASK 3: Add a slider to select payload range
        dcc.RangeSlider(
            id='payload-slider',
            min=0,
            max=10000,
            step=1000,
            marks={i: str(i) for i in range(0, 10001, 1000)},
            value=[min_payload,max_payload]
        ),

        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(dcc.Graph(id='success-payload-scatter-chart')),
    ]
)

# TASK 2: Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(
    Output(
        component_id='success-pie-chart',
        component_property='figure'
    ),
    Input(
        component_id='site-dropdown',
        component_property='value'
    )
)
def get_pie_chart(entered_site):
    print(f"Entered site: {entered_site}")  # Debugging line to print selected site
    if entered_site == 'ALL':
        data = spacex_df.groupby('Launch Site')['class'].sum().reset_index()
        fig = px.pie(
            data,
            values='class',
            names='Launch Site',
            title='Launch site success distribution'
        )
    else:
        data1=spacex_df[spacex_df['Launch Site']==entered_site]
        data=data1['class'].value_counts().reset_index()
        # return the outcomes piechart for a selected site
        fig = px.pie(
            data,
            values='class',
            names='index',
            title='Success distribution for ' + entered_site
        )
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(
        component_id='success-payload-scatter-chart',
        component_property='figure'
    ),
    [Input(
        component_id='site-dropdown',
        component_property='value'
    ),
    Input(
        component_id='payload-slider',
        component_property='value'
    )]
)
def get_scatter_plot(entered_site,entered_payload_range):
    if entered_site == 'ALL':
        fig = px.scatter(
            data_frame = spacex_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',  # Color points based on 'category' column
            title="Success vs payload for all sites",
            labels={"x": "Payload mass in kg", "y": "Sucess or Failure", "category": "Booster Version Category"}
        )
    else:
        data = spacex_df[spacex_df['Launch Site']==entered_site]
        fig = px.scatter(
            dataframe = data,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title="Success vs payload for " + entered_site,
            labels={"x": "Payload mass in kg", "y": "Sucess or Failure", "category": "Booster Version Category"}
        )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
