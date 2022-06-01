import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

url_confirmed = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
url_death = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
url_active = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'

###--------Create Dataframes---------###
confirmed = pd.read_csv(url_confirmed)
death = pd.read_csv(url_death)
recovered = pd.read_csv(url_active)

###---------Unpivot DataFrames-------###
date1 = confirmed.columns[4:]
total_confirmed = confirmed.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], value_vars=date1,
                                 var_name='date', value_name='confirmed')
date2 = death.columns[4:]
total_death = death.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], value_vars=date2, var_name='date',
                         value_name='death')
date3 = recovered.columns[4:]
total_recovered = recovered.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], value_vars=date3,
                                 var_name='date', value_name='recovered')

###---------Merge Dataframes--------###
covid_data = total_confirmed.merge(right=total_death, how='left',
                                   on=['Province/State', 'Country/Region', 'Lat', 'Long', 'date'])
covid_data = covid_data.merge(right=total_recovered, how='left',
                              on=['Province/State', 'Country/Region', 'Lat', 'Long', 'date'])
print(covid_data.head())

###----Converting date column from string to proper date format-------###
covid_data['date'] = pd.to_datetime(covid_data['date'])

###-------Check for missing values----------###
print(covid_data.isna().sum())

###-------Replace NaN with 0----------------###
covid_data['recovered'] = covid_data['recovered'].fillna(0)
# covid_data['Province/State'] = covid_data['Province/State'].fillna(0)
# covid_data['Lat'] = covid_data['Lat'].fillna(0)
# covid_data['Long'] = covid_data['Long'].fillna(0)

###--------Create new column with active stats----------###
covid_data['active'] = covid_data['confirmed'] - covid_data['death'] - covid_data['recovered']

app = dash.Dash(__name__, )
app.layout = html.Div([
    html.Div([
        html.Div([
            html.Img(src=app.get_asset_url('logo1.jpg'),
                     id = 'corona-image',
                     style={'height': '60px',
                            'width': 'auto',
                            'margin-bottom': '25px'})

        ], className='one-third column'),

        html.Div([
            html.H2('Covid - 19',style={'margin-bottom': '0px', 'color': 'white'}),
            html.H5('Track Covid - 19 Cases', style={'margin-bottom': '0px', 'color': 'white'})

        ], className='one-half column', id='title'),

        html.Div([
            html.H6('Last Updated: ' + str(covid_data['date'].iloc[-1].strftime('%B %d %Y') + ' 00:01 (UTC)'),
                    style={'color': 'orange'})

        ], className='one-third column', id='title1')


    ], id='header', className='row flex-display', style={'margin-bottom': '25px'}),
    html.Div([
        html.Div([

        ], className='card_container four columns')

    ], className='row flex display')

], id='mainContainer', style={'display': 'flex', 'flex-direction': 'column'})

if __name__ == '__main__':
    app.run_server(debug=True)
