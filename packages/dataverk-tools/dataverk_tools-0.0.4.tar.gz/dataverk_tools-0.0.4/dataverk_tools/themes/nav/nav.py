from .._colormaps import _linear3color
from .colors import *

import plotly.graph_objects as go

sequential = _linear3color(navRod, navLysBla, navBla)
diverging = _linear3color(navRod, navLysBla, navBla)
sequentialminus = _linear3color(navRod, navLysBla, navBla)

colorscale = [[i/10,color] for i, color in enumerate(sequential)]
colorscale_diverging = [[i/10,color] for i, color in enumerate(sequential)]
colorscale_sequential = [[i/10,color] for i, color in enumerate(sequential)]
colorscale_sequentialminus = [[i/10,color] for i, color in enumerate(sequential)]


discrete = [navRod, navOransje, navLimeGronn, navGronn, navLilla, navDypBla,
            navBla, navLysBla, navMorkGra, navGra40]


font_family = "'Open Sans', 'Roboto', 'Helvetica Neue', 'sans-serif"
font_color  = '#2a3f5f'

linecolor = navGra20
gridcolor = navGra20
fillcolor = navRod

bgcolor = "white"

plotly_template  = go.layout.Template()
plotly_template.layout = {
    'font': {'color': font_color, 'family': font_family},
     'colorscale': {'diverging': colorscale_diverging,
                   'sequential': colorscale_sequential,
                   'sequentialminus': colorscale_sequentialminus},
    'colorway': discrete,
}


