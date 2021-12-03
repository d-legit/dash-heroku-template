%%capture
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])

mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')

mark1 = '''
The gender wage gap is the difference in pay between men and women of the same occupation. 
In general, men are paid more to do the same type of work that a woman does. 
On average, women are paid 82% the wages of men. 
This was obtained from a 2018 study comparing the median wages of men to women.
source: https://americanprogress.org/article/quick-facts-gender-wage-gap/
'''

mark2 = '''

The GSS aka General Social Survey is a survey collecting data to observe trends in opinions, attitudes, and behaviors.
Some of the data collected includes: group membership, voting, personal psychological evaluations, measures of
happiness, misanthropy, life satisfaction, spending priorities, and attitudinal questions on such public issues as
abortion, crime and punishment, race relations, gender roles.
sources: http://www.gss.norc.org/About-The-GSS, https://www.nsf.gov/pubs/2007/nsf0748/nsf0748_3.pdf
'''

# Question 2
gss2 = gss_clean.groupby('sex', as_index = False).agg(({'income': 'mean', 'job_prestige': 'mean',
                                      'socioeconomic_index': 'mean', 'education': 'mean'}))
gss2 = gss2.rename(columns={'income':'avg_income','job_prestige':'avg_job_prestige',
                    'socioeconomic_index': 'avg_soc_index', 'education': 'avg_years_education'})
gss2 = gss2.round(2)

table = ff.create_table(gss2)
table.show()

#question 3
fig3 = px.bar(gss_clean, x = 'male_breadwinner', color = 'sex',
            barmode = 'group')
fig3.show()

#question 4
fig4 = px.scatter(gss_clean, x='job_prestige', y='income', 
                 height=600, width=600,
                 color = 'sex',
                 trendline = 'ols',
                 hover_data=['education', 'socioeconomic_index'])
fig4.show()

#question 5
fig5a = px.box(gss_clean, x='income', color = 'sex')
fig5a.show()

fig5b = px.box(gss_clean, x='job_prestige', color = 'sex')
fig5b.show()

#Question 7
app = JupyterDash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        html.H1("Exploring different aspects of General Social Survey"),  
        dcc.Markdown(children = mark1),
        
        
        dcc.Markdown(children = mark2),
        dcc.Graph(figure = table),
        dcc.Graph(figure = fig3),
        
        html.H2("Placeholder title for figure 4"),  

        dcc.Graph(figure = fig4),
        
        html.Div([
            
            html.H2("figure 5a placeholder title"),
            
            dcc.Graph(figure=fig5a)
            
        ], style = {'width':'48%', 'float':'left'}),
        
        html.Div([
            
            html.H2("figure 5b placeholder title"),
            
            dcc.Graph(figure=fig5b)
            
        ], style = {'width':'48%', 'float':'right'})
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True, port = 8051)
