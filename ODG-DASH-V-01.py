import psycopg2 as psy
import dash
import dash_core_components as dcc
import dash_html_components as html
import os
import glob
import pandas as pd
from dash.dependencies import Input, Output, State
from faker import Factory
import plotly.offline as py
import plotly.graph_objs as go
from IPython.display import Image
import sys
import logging
import dash_bootstrap_components as dbc
import base64

#image_filename = 'ufpb.png' # replace with your own image  

dict_raca= { 0:'Não quis declarar',
            1: 'Branca',
            2: 'Preta',
            3: 'Parda',
            4: 'Amarela',
            5: 'Indígena',
            9: 'Não dispõe'
   
}


#encoded_image = base64.b64encode(open(image_filename, 'rb').read())

dict_ies= { 0:'nd',
            1: 'Nassau JP',
            2: 'Nassau CG',
            3: 'IFPB',
            4: 'UFCG',
            5: 'UFPB',
            6: 'Unipe'
   
}



dict_raca= { 0:'Não quis declarar',
            1: 'Branca',
            2: 'Preta',
            3: 'Parda',
            4: 'Amarela',
            5: 'Indígena',
            9: 'Não dispõe'
   
}



dict_evasao= { 0:'Não quis declarar',
            1: 'Branca',
            2: 'Preta',
            3: 'Parda',
            4: 'Amarela',
            5: 'Indígena',
            9: 'Não dispõe'
   
}

mydb=psy.connect (
host='localhost',
user = 'ODG',
password='observatorio',
database='ODG')

mycursor=mydb.cursor()

anos = [2011,2012,2013,2014,2015,2016,2017]
external_stylesheets = ['https://codepen.io/amyoshino/pen/jzXypZ.css']

evadidos=['Quantidade integralizada',
'Por raca',
'Por sexo',
'Por deficiencia',
'Por idade']



app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.title = 'Plataforma_ODG'



app.layout = html.Div([
   

 #   html.Div
 #   ([html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))
 #       ], #className='two columns',
 #   style={
 #   #'position': 'relative',
 #   'float': 'right',
 #   #'right': '10px',
 #   #'height': '75px',
 #   'display':'inline-block',
 #   #'margin-left':'2%',
 #   #'padding-top': '10px',
 #   }
 #   ),
   

    html.Div([html.H1(children= 'ODG - Observatório De Dados Da Graduação'),
    ]
          ,

     style={
    'font-size': '5pt',
    'height': '75px',
    'margin': '0px -10px 10px',
    'background-color': '#ADD8E6',
    'border-radius': '2px',
    #'margin-left': '0',
    }
     ),

    html.Div([
    html.Div([


    dcc.RadioItems(
    options=[
        {'label': 'Evasão', 'value': 'evd'},
        {'label': 'Ingresso', 'value': 'ing'}
    ],
    id='escolher',
    labelStyle={'display': 'inline-block'}
    ),




html.Label('Censo'),
    dcc.Dropdown(
    id = 'variavel',
        options=[
            {'label': j, 'value': j} for j in anos
        ],
        value='2012',
        multi=False
    ),


    html.Div([
    html.Label('Alunos evadidos por'),
    dcc.Dropdown(
    id = 'tipo',
        options=[
            {'label': a, 'value': a} for a in evadidos
        ],
        value='Quantos alunos foram evadidos pela ...',
        multi=False,
    )],
    style = {'display': 'none'},
    id='evasao'
    ),



    ],
    style={
    'margin-top': '60px',
    #'background-color': '#add8e6',
    } ,
    className='three columns',
    ),

    html.Div([dcc.Graph(id = 'feature-graphic'),
    ]
          ,
    className='nine columns'
 
     ),

    #dcc.Graph(id = 'feature-graphic'),
   
    ],
    className='row'),

    html.Div([html.H5('Deixe sua sugestão de pergunta abaixo: ')]),


    dbc.Form(
    [
        dbc.FormGroup(
            [
                dbc.Label("Email", className="mr-2"),
                dbc.Input(id='email',type="email", placeholder="Ex.: odg@gmail.com"),
            ],
            className="mr-3",
        ),

        dbc.FormGroup(
            [
                dbc.Label("Sugestão", className="mr-2"),
                dbc.Input(id='sugestao',type="text", placeholder="Ex.: Quantos alunos..."),
            ],
            className="mr-3",
        ),

        html.Div([
        dbc.Button("Submit",id='submit-button', color="primary")],
        style={
        'margin-top': '10px',
    }),
    

    ],
    inline=True,
    ),

    html.Div(id='output'),

#    html.Div([
#        dcc.Input(id='emailzin',type='text',value='Ex.: odg@gmail.com'),
#        dcc.Input(id='my-id',  type="text",value='Ex.: Quantos alunos...'),
#        html.Button('Click Me', id='button'),
#        html.Div(id='my-div')
#    ]),



],className='row',  
style={'width': '100%',
    'background-color': '#ffffff',
        #'height' : '60%',
            'display': 'inline-block'})

app.suppress_callback_exceptions=True

@app.callback(
    dash.dependencies.Output('evasao', 'style'),
    [dash.dependencies.Input('escolher', 'value')])

def toggle_container(toggle_value):
    if toggle_value == 'evd':
        return {'display': 'block'}
    else:
        return {'display': 'none'}





@app.callback(
    Output(component_id='email', component_property='value'),

    [Input('submit-button', 'n_clicks')])

def update(am):
    if(am):
        return ''

@app.callback(
    Output(component_id='sugestao', component_property='value'),
    [Input('submit-button', 'n_clicks')])

def update(ama):
    if(ama):
        return ''

@app.callback(
    Output(component_id='output', component_property='children'),
    [Input('submit-button', 'n_clicks'),],
    state=[State(component_id='sugestao', component_property='value'),
    State(component_id='email', component_property='value')])

#@app.callback(
#    Output(component_id='my-div', component_property='children'),
#    [Input('button', 'n_clicks'),],
#    state=[State(component_id='my-id', component_property='value'),
#    State(component_id='emailzin', component_property='value')])


def update_output_div(n_clicks, input_value, emailzin):

    if(input_value and emailzin):

        mycursor.execute('''
                INSERT INTO sugestoes (email, sugestao)
                VALUES
                (%s,%s)
                ''',(emailzin, input_value))
        mydb.commit()
        return 'Sugestão enviada com sucesso, tentaremos um retorno o mais breve'
    else:
        if(n_clicks):
            return 'Campo invalido ou não preenchido, por favor corrigir.'




@app.callback(Output('feature-graphic', 'figure'),
    [Input('variavel', 'value'),
     Input('tipo','value')])

def update_graph(variavel,tipo):
    fake = Factory.create()
    fig=go.Figure()
    trace=[]
    buttons=[]
    if(tipo == 'Por sexo'):

        mycursor=mydb.cursor()

        mycursor.execute('''SELECT C.TP_SEXO, P.sk_ies
                        FROM dim_aluno AS C
                        JOIN fato_evasao AS P ON C.sk_aluno = P.sk_aluno
                            ''')

        myresult= mycursor.fetchall()
        colnames = [desc[0] for desc in mycursor.description]
       
        df = pd.DataFrame(data=myresult, columns=colnames )
        variables=list(set(df['sk_ies']))


        cores = ['#96D38C','#FEBFB3','#E1396C']
        for x in variables:
       
           
            a=df['sk_ies']==x
            b=df[a]
            classes_mais_votadas = b.tp_sexo.value_counts()

            fig.add_trace((go.Pie(labels = ['Masculino','Feminino'],
            values = classes_mais_votadas.values,
            marker = {'colors': cores,
            'line' : {'color':'#000000','width':2}
                            },
            hoverinfo='label+percent+value',
            direction='clockwise'
        )))
        for item in variables:
            flag=[x==item for x in variables]
            buttons.append(dict(label=dict_ies[item],        
            method="update",
            args=[{"visible": flag},
            {"title": 'Gráfico evasão por sexo da ' + dict_ies[item],      
            }]))
        fig.layout.update(
        updatemenus=[
        go.layout.Updatemenu(
        active=1,
        buttons=list(buttons),)])
             

    if(tipo== 'Por raca'):
   
        mycursor=mydb.cursor()

        mycursor.execute('''SELECT C.TP_COR_RACA, P.sk_ies
                        FROM dim_aluno AS C
                        JOIN fato_evasao AS P ON C.sk_aluno = P.sk_aluno
                            ''')

        myresult= mycursor.fetchall()
        colnames = [desc[0] for desc in mycursor.description]
       
        df = pd.DataFrame(data=myresult, columns=colnames )
        variables=list(set(df['sk_ies']))


        #cores = ['#96D38C','#FEBFB3','#E1396C']
        for x in variables:

           
            a=df['sk_ies']==x
            b=df[a]
            classes_mais_votadas = b.tp_cor_raca.value_counts()
            fig.add_trace((go.Pie(labels = [dict_raca[x] for x in classes_mais_votadas.index],
            values = classes_mais_votadas.values,
            marker = {
            'line' : {'color':'#000000','width':2}
                            },
            hoverinfo='label+percent+value',
            direction='clockwise'
        )))
        for item in variables:
            flag=[x==item for x in variables]
            buttons.append(dict(label=dict_ies[item],        
            method="update",
            args=[{"visible": flag},
            {"title": 'Gráfico evasão por raça da ' + dict_ies[item],      
            }]))
        fig.layout.update(
        updatemenus=[
        go.layout.Updatemenu(
        active=1,
        buttons=list(buttons),)])


    if(tipo== 'Quantidade integralizada'):
        mycursor=mydb.cursor()
        mycursor.execute('''SELECT qt_carga_horaria_integ, sk_ies
                        FROM fato_evasao''')  
        myresult= mycursor.fetchall()
        colnames = [desc[0] for desc in mycursor.description]
        df = pd.DataFrame(data=myresult, columns=colnames )
        variables= list(set(df['sk_ies']))
        #for var in variavel:
        #    fig.add_trace((go.Scatter(
        #    x=item['Tempo'],
        #    y=item[var],
        #    name = var + ' ' + nama,
        #    visible=True,
        #    cliponaxis=False,
        #    line = dict(color = fake.hex_color()),
        #    opacity = 0.8)))
        for x in variables:
            a=df['sk_ies']==x
            b=df[a]
            fig.add_trace((go.Histogram(
            x=b['qt_carga_horaria_integ'],
            name = dict_ies[x],
            visible=True,
            opacity = 0.8)))
        #for item in variables:
        #    flag=[x==item for x in variables]
        #    buttons.append(dict(label=dict_ies[item],        
        #    method="update",
        #    args=[{"visible": flag},
        #    {"title": "Gráfico da ",      
        #    }]))    
        fig.layout.update(
        updatemenus=[
        go.layout.Updatemenu(
        active=1,
        buttons=list(buttons),)])
        fig.layout.update(title=tipo,
        xaxis={'title': 'Horas Integralizadas'},
        yaxis={'title': 'Quantidade de alunos evadidos'})

    if(tipo == 'Por deficiencia'):
        mycursor=mydb.cursor()

        mycursor.execute('''SELECT C.TP_DEFICIENCIA, P.sk_ies
                        FROM dim_aluno AS C
                        JOIN fato_evasao AS P ON C.sk_aluno = P.sk_aluno
                            ''')

        myresult= mycursor.fetchall()
        colnames = [desc[0] for desc in mycursor.description]
       
        df = pd.DataFrame(data=myresult, columns=colnames )
        variables=list(set(df['sk_ies']))


        cores = ['#96D38C','#FEBFB3','#E1396C']
        for x in variables:
       
           
            a=df['sk_ies']==x
            b=df[a]
            classes_mais_votadas = b.tp_deficiencia.value_counts()

            fig.add_trace((go.Pie(labels = classes_mais_votadas.index,
            values = classes_mais_votadas.values,
            marker = {'colors': cores,
            'line' : {'color':'#000000','width':2}
                            },
            hoverinfo='label+percent+value',
            direction='clockwise'
        )))
        for item in variables:
            flag=[x==item for x in variables]
            buttons.append(dict(label=dict_ies[item],        
            method="update",
            args=[{"visible": flag},
            {"title": 'Gráfico evasão por sexo da ' + dict_ies[item],      
            }]))
        fig.layout.update(
        updatemenus=[
        go.layout.Updatemenu(
        active=1,
        buttons=list(buttons),)])  

    if(tipo== 'Por idade'):
        mycursor=mydb.cursor()
       
        mycursor.execute('''SELECT P.sk_ies, (2019 - C.nu_ano_nascimento) as idade
                FROM dim_aluno AS C
                JOIN fato_evasao AS P ON C.sk_aluno = P.sk_aluno
                    ''')
        myresult= mycursor.fetchall()
        colnames = [desc[0] for desc in mycursor.description]
        df = pd.DataFrame(data=myresult, columns=colnames )
        variables= list(set(df['sk_ies']))
        #for var in variavel:
        #    fig.add_trace((go.Scatter(
        #    x=item['Tempo'],
        #    y=item[var],
        #    name = var + ' ' + nama,
        #    visible=True,
        #    cliponaxis=False,
        #    line = dict(color = fake.hex_color()),
        #    opacity = 0.8)))
        for x in variables:
            a=df['sk_ies']==x
            b=df[a]
            fig.add_trace((go.Histogram(
            x=b['idade'],
            name = dict_ies[x],
            visible=True,
            opacity = 0.8)))
        #for item in variables:
        #    flag=[x==item for x in variables]
        #    buttons.append(dict(label=dict_ies[item],        
        #    method="update",
        #    args=[{"visible": flag},
        #    {"title": "Gráfico da ",      
        #    }]))    
        fig.layout.update(
        updatemenus=[
        go.layout.Updatemenu(
        active=1,
        buttons=list(buttons),)])

        fig.layout.update(title=tipo,
        xaxis={'title': 'Idade'},
        yaxis={'title': 'Quantidade de alunos evadidos'})





    return go.Figure(fig)











if(__name__ == '__main__'):

    app.run_server(debug=True) 