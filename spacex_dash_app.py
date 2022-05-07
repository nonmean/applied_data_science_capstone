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

dropdown_option = [{'label': 'All Sites', 'value': 'ALL'}]
for i in spacex_df["Launch Site"].unique():
    dropdown_option.append({'label': i, 'value': i})

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                options=dropdown_option,
                                value='ALL',
                                placeholder="Select a Launch Site here",
                                searchable=True
                                ),

                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),

                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000,
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
            Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        filtered_df = spacex_df.groupby("Launch Site", as_index=False)["class"].sum()

        fig = px.pie(data_frame=filtered_df, values='class', 
        names='Launch Site', 
        title='Total Success Launches By Site')
        return fig
    else:
        filtered_df = spacex_df.loc[spacex_df['Launch Site'] == entered_site, :]
        n1 = filtered_df["class"].sum()
        n0 = filtered_df["class"].count() - n1

        pie_df = pd.DataFrame({"class": [1, 0], "count": [n1, n0]})

        fig = px.pie(data_frame=pie_df, values='count', 
        names='class', 
        title='Total Success Launches For Site %s' %(entered_site))
        return fig
        # return the outcomes piechart for a selected site


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
            Input(component_id='site-dropdown', component_property='value'),
            Input(component_id='payload-slider', component_property='value'))
def get_scatter_chart(entered_site, entered_payload):
    print(entered_payload)
    filtered_df = spacex_df.loc[spacex_df['Payload Mass (kg)'] >= entered_payload[0], :]

    if entered_site != 'ALL':
        filtered_df = filtered_df.loc[filtered_df['Launch Site'] == entered_site, :]

    fig = px.scatter(data_frame=filtered_df, y='class', 
    x='Payload Mass (kg)', color="Booster Version Category", 
    title='Correlation between Payload and Success for all sites')
    return fig
        # return the outcomes piechart for a selected site


# Run the app
if __name__ == '__main__':
    app.run_server()
