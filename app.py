import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
import dash_table


app = dash.Dash()
server = app.server
df = pd.read_csv("data/NMEA_SUMMARY_V4.csv")

dfcolumns = list(df)


fig = px.line_mapbox(
    df,
    lat="latitude",
    lon="longitude",
    hover_name="altitude",
    hover_data=["altitude", "abs_time_ms"],
    zoom=12,
    height=800,
)
fig.update_layout(mapbox_style="stamen-terrain")  # "open-street-map")
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})


app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    dcc.Graph(id="mymap", figure=fig),
                    style={"width": "99%"},
                ),
                # html.Div(
                #    dash_table.DataTable(
                #        id="table",
                #        columns=[{"name": i, "id": i} for i in df.columns],
                #        data=df.to_dict("records"),
                #        fixed_rows={"headers": True},
                #        page_action="none",
                #        style_cell={"minWidth": 95, "maxWidth": 95, "width": 95},
                #        virtualization=True,
                #    ),
                #    style={"width": "49%"},
                # ),
            ]
        ),
        html.Div(
            [
                dcc.Dropdown(
                    id="color",
                    options=[{"label": i, "value": i} for i in ["abs_time_ms"]],
                    value="abs_time_ms",
                )
            ],
            style={"width": "99%", "display": "inline-block"},
        ),
        html.Div(
            [
                dcc.Graph(id="time-series"),
            ],
            style={"display": "inline-block", "width": "99%"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Dropdown(
                            id="x_column",
                            options=[{"label": i, "value": i} for i in ["abs_time_ms"]],
                            value="abs_time_ms",
                        )
                    ],
                    style={"width": "49%", "display": "inline-block"},
                ),
                html.Div(
                    [
                        dcc.Dropdown(
                            id="y_column",
                            options=[{"label": i, "value": i} for i in dfcolumns],
                            value="altitude",
                        ),
                    ],
                    style={"width": "49%", "float": "right", "display": "inline-block"},
                ),
            ],
            style={
                "borderBottom": "thin lightgrey solid",
                "backgroundColor": "rgb(250, 250, 250)",
                "padding": "10px 5px",
            },
        ),
    ],
    style={"textAlign": "center"},
)


def lineplot(x, y, title="", axis_type="Linear"):
    return {
        "data": [go.Scatter(x=x, y=y, mode="lines")],
    }


@app.callback(
    dash.dependencies.Output("time-series", "figure"),
    [
        dash.dependencies.Input("x_column", "value"),
        dash.dependencies.Input("y_column", "value"),
    ],
)
def update_timeseries(xaxis_column_name, yaxis_column_name):
    x = df[xaxis_column_name]
    y = df[yaxis_column_name]
    return lineplot(x, y)


app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

if __name__ == "__main__":
    app.run_server()
