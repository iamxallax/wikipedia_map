from dash import Dash, html
import dash_cytoscape as cyto

from main import main

app = Dash(__name__)

def create_graph(connections:list):
    elements = [{'data': {'id': '1', 'label': '1'}}]
    
    for tup in connections[:100]:
        home_id, home_name = str(tup[0][0]), tup[0][1]
        branch_id, branch_name = str(tup[1][0]), tup[1][1]
        if not any(d.get('data', {}).get('id') == branch_id for d in elements):
            elements.append({'data': {'id': branch_id, 'label': branch_name}})
        elements.append({'data': {'source': home_id, 'target': branch_id}})

    print(elements)

    app.layout = html.Div([
        html.P("Dash Cytoscape:"),
        cyto.Cytoscape(
            id='cytoscape',
            elements=elements,
            layout={'name': 'breadthfirst'},
            style={'width': '2000px', 'height': '1000px'}
        )
    ])

    app.run(debug=True)

create_graph(main())