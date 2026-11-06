
import plotly.express as px


# --------------------------------------------------
# COMMON CHART THEME
# --------------------------------------------------

CHART_TEMPLATE = "plotly_dark"

CHART_LAYOUT = {
    "template": CHART_TEMPLATE,
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font": {
        "family": "Arial",
        "size": 12
    },
    "margin": {
        "l": 40,
        "r": 30,
        "t": 60,
        "b": 40
    },
    "legend_title_text": ""
}


# --------------------------------------------------
# 1. BAR CHART
# --------------------------------------------------

def create_bar_chart(
    df,
    x,
    y,
    title,
    color=None,
    orientation="v"
):
    fig = px.bar(
        df,
        x=x,
        y=y,
        color=color,
        title=title,
        orientation=orientation,
        text_auto=True
    )

    fig.update_layout(**CHART_LAYOUT)
    fig.update_yaxes(tickformat=",")
    fig.update_xaxes(tickformat=",")

    return fig


# --------------------------------------------------
# 2. LINE CHART
# --------------------------------------------------

def create_line_chart(
    df,
    x,
    y,
    title,
    color=None,
    markers=True
):
    fig = px.line(
        df,
        x=x,
        y=y,
        color=color,
        title=title,
        markers=markers
    )

    fig.update_layout(**CHART_LAYOUT)

    return fig


# --------------------------------------------------
# 3. DONUT CHART
# --------------------------------------------------

def create_donut_chart(
    df,
    names,
    values,
    title
):
    fig = px.pie(
        df,
        names=names,
        values=values,
        title=title,
        hole=0.55
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    fig.update_layout(**CHART_LAYOUT)

    return fig


# --------------------------------------------------
# 4. SCATTER CHART
# --------------------------------------------------

def create_scatter_chart(
    df,
    x,
    y,
    title,
    color=None,
    size=None
):
    fig = px.scatter(
        df,
        x=x,
        y=y,
        color=color,
        size=size,
        title=title,
        hover_data=df.columns.tolist()
    )

    fig.update_layout(**CHART_LAYOUT)

    return fig


# --------------------------------------------------
# 5. CHARGING STATION MAP
# --------------------------------------------------

def create_station_map(
    df,
    latitude="latitude",
    longitude="longitude",
    color=None,
    hover_data=None
):
    fig = px.scatter_map(
        df,
        lat=latitude,
        lon=longitude,
        color=color,
        hover_data=hover_data,
        zoom=3.5,
        height=600,
        title="EV Charging Stations Across India"
    )

    fig.update_layout(
        map_style="carto-darkmatter",
        **CHART_LAYOUT
    )

    return fig
