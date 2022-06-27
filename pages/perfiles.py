import dash_bootstrap_components as dbc
from dash import html

andresCuellar={
    'foto':'/img/Andres_Cuellar.jpeg',
    'nombre':'Andres Cuellar',
    'descripcion':'Después de tratar por dos años seguidos de entrar a DS4A por fin',
    'contacto':'andrescuellar@team126.com'
}

albertoRamirez={
    'foto':'../img/Alberto_Ramirez.jpeg',
    'nombre':'Alberto Ramirez',
    'descripcion':'Después de tratar por dos años seguidos de entrar a DS4A por fin',
    'contacto':'albertoramirez@team126.com'
}

carmenDelgado={
    'foto':'../img/Carmen_Delgado.jpeg',
    'nombre':'Carmen Delgado',
    'descripcion':'Después de tratar por dos años seguidos de entrar a DS4A por fin',
    'contacto':'carmendelgado@team126.com'
}

juanDiaz={
    'foto':'../img/Juan_Diaz.jpeg',
    'nombre':'Juan Felipe Diaz',
    'descripcion':'Después de tratar por dos años seguidos de entrar a DS4A por fin',
    'contacto':'juandiaz@team126.com'
}

juanHurtado={
    'foto':'../img/Juan_Hurtado.jpeg',
    'nombre':'Juan Fernando Hurtado',
    'descripcion':'Después de tratar por dos años seguidos de entrar a DS4A por fin',
    'contacto':'juanhurtado@team126.com'
}

diegoMoreno={
    'foto':'../img/Diego_Moreno.jpeg',
    'nombre':'Diego Alejandro Moreno',
    'descripcion':'Después de tratar por dos años seguidos de entrar a DS4A por fin',
    'contacto':'diegomoreno@team126.com'
}



def card_perfil(foto, nombre, descripcion, contacto):
    card=dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.CardImg(
                        src=foto,
                        className="img-fluid rounded-start",
                    ),
                    className="col-md-4",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H4(nombre, className="card-title"),
                            html.P(descripcion,
                                className="card-text",
                            ),
                            html.Small(contacto,
                                className="card-text text-muted",
                            ),
                        ]
                    ),
                    className="col-md-8",
                ),
            ],
            className="g-0 d-flex align-items-center",
        )
    ],
    className="mb-3",
    style={"maxWidth": "540px"},
    )
    return card



row_1 = dbc.Row(
    [
        dbc.Col(dbc.Card(card_perfil(**andresCuellar), color="primary", outline=True)),
        dbc.Col(dbc.Card(card_perfil(**albertoRamirez), color="secondary", outline=True)),
    ],
    className="mb-4",
)

row_2 = dbc.Row(
    [
        dbc.Col(dbc.Card(card_perfil(**carmenDelgado), color="success", outline=True)),
        dbc.Col(dbc.Card(card_perfil(**juanDiaz), color="warning", outline=True)),
    ],
    className="mb-4",
)

row_3 = dbc.Row(
    [
        dbc.Col(dbc.Card(card_perfil(**juanHurtado), color="info", outline=True)),
        dbc.Col(dbc.Card(card_perfil(**diegoMoreno), color="danger", outline=True)),
    ],
    className="mb-4",
)

cards = html.Div([row_1, row_2, row_3])
