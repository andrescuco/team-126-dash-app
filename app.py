from dash import Dash, dcc, html, Input, Output, no_update, ALL
import pandas as pd
import plotly.express as px
import json
import dash_bootstrap_components as dbc

# Components
from components.content import content
from components.content import main_view
from components.sidebar import sidebar
from components.sidebar import navbar
from components.jumbotron import jumbotron

# Pages
from pages.tourist_form import radios_input
from pages.perfiles import cards
from pages.crime_map import crime_map

# Model
from components.modeluse import use_model


app = Dash(__name__,
           external_stylesheets=[
               dbc.themes.LUX, dbc.icons.BOOTSTRAP], suppress_callback_exceptions=True,
           meta_tags=[{"name": "viewport",
                       "content": "width=device-width, initial-scale=1"}]
           )

app.title = "Turismo Bogotá"
token = "pk.eyJ1Ijoiam9yY2hlY2x1bmllIiwiYSI6ImNsNHRiOWQzZDE5YmkzamxwM2k2YTZiNGUifQ.a8403FjDkiW0wAO_bO4lLg"

server = app.server

# Load data
df = pd.read_csv("./data-cleaned/scattermap_points.csv")
# TODO: arreglar municipios aledanos
localidades_df = pd.read_csv("./data-cleaned/localidades_properties.csv")
with open("./data-cleaned/poligonos-localidades-min.json") as response:
    bogota_geojson = json.load(response)
crime = pd.read_csv("./data-cleaned/Delitos_x_localidad.csv")

app.layout = html.Div([dcc.Location(id="url"), navbar, sidebar, content])


# Builds logic that's on the main page
@app.callback(
    [Output("choropleth-map", "figure"),
     Output("kpi_crime", "children"),
     Output("kpi_mean_hotel_price", "children"),
     Output("kpi_number_of_touristic_attractions", "children")],
    [Input("localidad", "value"),
     Input("type", "value"),
     Input("all_localidades_checkbox", "value"),
     Input("url", "pathname")
     ])
def display_map(chosen_localidades, chosen_type, show_all_localidades, pathname):
    # Default KPI's when seeing the entire bogota map figure
    kpi_crime = "65.000 delitos reportados en Bogotá"
    kpi_mean_hotel_price = "$174.142 precio promedio en Bogotá"
    kpi_number_of_touristic_attractions = "440 atractivos turisticos en Bogotá"

    # Default values when the user is seeing the entire bogota map figure
    map_zoom = 9
    map_center = {"lat": 4.5500000, "lon": -74.1000000}
    marker_size = 6

    # Handle map if user hasn't selected a specific localidad
    all_localidades = [b for b in sorted(df['localidad'].unique())]
    if (show_all_localidades == ["on"]):
        chosen_localidades = all_localidades
    elif (show_all_localidades != ["on"] and chosen_localidades != None):
        # When there's a specific localidad selected, we adjust the center and the zoom values
        chosen_localidad_props = localidades_df[localidades_df['name']
                                                == chosen_localidades]
        map_zoom = chosen_localidad_props['zoom'].item()
        chosen_localidad_center = pd.eval(
            chosen_localidad_props['center_coordinates'].item())
        map_center = {"lat": chosen_localidad_center[0],
                      "lon": chosen_localidad_center[1]}
        marker_size = 10
        chosen_localidades = [chosen_localidades]

        # We also display the specific KPI's for the selected localidad
        kpi_crime = "{} delitos reportados en {}".format(
            chosen_localidad_props['kpi_crime'].item(), chosen_localidad_props['name'].item())
        kpi_number_of_touristic_attractions = "{} atractivos turisticos en {}".format(
            chosen_localidad_props['number_of_touristic_attractions'].item(), chosen_localidad_props['name'].item())
        kpi_mean_hotel_price = "{} precio promedio en {}".format(
            chosen_localidad_props['Hotel_mean_price'].item(), chosen_localidad_props['name'].item())
    else:
        chosen_localidades = [chosen_localidades]

    # Filter the dataframe to the selected localidad and scatter points
    filtered_df = df[(df['localidad'].isin(chosen_localidades))
                     & (df['type'].isin(chosen_type))]

    # Choropleth map exactly how you would do it on a jupyter notebook
    fig = px.choropleth_mapbox(filtered_df, geojson=bogota_geojson, color="localidad",
                               locations="localidad", featureidkey="properties.Nombre de la localidad",
                               color_discrete_sequence=['red'],
                               center=map_center,
                               zoom=map_zoom,
                               opacity=0.1)

    fig.add_scattermapbox(lat=filtered_df['latitude'],
                          lon=filtered_df['longitude'],
                          marker=dict(size=marker_size,
                                      color=filtered_df['color']),
                          hovertemplate=filtered_df['type'] +
                          ": " + filtered_df['name']
                          )

    fig.update_layout(mapbox_style="streets",
                      mapbox_accesstoken=token)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_layout(uirevision='foo')
    fig.update_layout(showlegend=False)
    return fig, kpi_crime, kpi_mean_hotel_price, kpi_number_of_touristic_attractions


# Shows or hide localidades dropdown depending on the checkbox to show all
# localidades
@app.callback(Output("localidad", "style"), [Input("all_localidades_checkbox", "value")])
def hide_dropdown(show_all_localidades):
    if (show_all_localidades == ["on"]):
        return {"display": "none"}
    else:
        return {"display": "block"}


# Handles the logic that's on the tourist_form page
@app.callback(
    [Output("submit_button", "disabled"),
     Output("submit_button", "style"),
     Output("error_message", "children"),
     Output("tourism-form-questions-count", "children"),
     Output("tourist-form-results", "style"),
     Output("tourist-form-text", "style"),
     Output("tourist-form-results-detail", "children")],
    [Input({'type': 'my-numeric-input', 'index': ALL}, 'value'),
     Input({'type': 'my-radio-input', 'index': ALL}, 'value'),
     Input('submit_button', 'n_clicks')],
)
def on_form_change(numerical_input_values, radio_button_values, submit_button_n_clicks):
    form_values = numerical_input_values + radio_button_values
    non_none_values_count = sum(
        x is not None for x in form_values)

    # Content
    error_message = ""
    questions_left_counter = "{}/15".format(non_none_values_count)
    results = "Default"

    # Styles
    show_component = {"display": "block"}
    hide_component = {"display": "none"}

    # Validate that the user has finished all the inputs on the form
    if (None in form_values):
        error_message = """
        Por favor completa todos los campos correctamente.
        """
        return True, no_update, error_message, questions_left_counter, no_update, no_update, no_update
    elif (submit_button_n_clicks == 1):
        results_df = pd.read_csv('./data-cleaned/recommendations_results.csv')

        # Call the model on button click
        result_group = use_model(form_values)
        recommendations = results_df[results_df['group']
                                     == result_group]

        recommendation_list = []

        for _, row in recommendations.iterrows():
            recommendation_list.append(html.Li("{} {}".format(
                row['recommendation_type'], row['recommendation'])))

        recommendations_container = dbc.ListGroup(recommendation_list)

        print(recommendations)

        # Hides the submit button and displays the results component
        return False, hide_component, error_message, questions_left_counter, show_component, hide_component, recommendations_container

    return False, no_update, error_message, questions_left_counter, no_update, no_update, no_update


# Handles routing for the pages, displays different content given a url
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    print(pathname)
    if pathname == "/":
        return main_view
    elif pathname == "/tu-perfil":
        return radios_input
    elif pathname == "/delincuencia":
        return html.Div(crime_map)
    elif pathname == "/sobre-nosotros":
        return html.Div(cards)
    # If the user tries to reach a different page, return a 404 message
    return jumbotron


if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
