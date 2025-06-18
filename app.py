# app.py
from flask import Flask, render_template, request, jsonify, url_for
import pandas as pd
import networkx as nx
import os
import plotly.graph_objects as go
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


app = Flask(__name__)

# Load data and build graph
df = pd.read_csv('routes.csv')
G = nx.DiGraph()
for _, row in df.iterrows():
    G.add_edge(row['Source'], row['Destination'], weight=row['Distance'])

cities = sorted(set(df['Source']) | set(df['Destination']))

@app.route('/')
def index():
    return render_template('index.html', cities=cities)

@app.route('/route', methods=['POST'])
def route():
    source = request.form['source']
    destination = request.form['destination']

    try:
        path = nx.dijkstra_path(G, source, destination, weight='weight')
        distance = nx.dijkstra_path_length(G, source, destination, weight='weight')

        # Create interactive Plotly graph
        pos = nx.spring_layout(G, seed=42)
        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x += [x0, x1, None]
            edge_y += [y0, y1, None]

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1, color='#888'),
            hoverinfo='none',
            mode='lines')

        node_x = []
        node_y = []
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=[node for node in G.nodes()],
            marker=dict(
                color='skyblue',
                size=20,
                line_width=2))

        fig = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            title='Airline Route Graph',
                            titlefont_size=20,
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20,l=5,r=5,t=40)))

        fig_path = os.path.join('templates', 'graph.html')
        fig.write_html(fig_path)

        return render_template('index.html', cities=cities, path=' → '.join(path), distance=distance, show_graph=True)

    except nx.NetworkXNoPath:
        return render_template('index.html', cities=cities, error="No route found between selected cities.")
    except nx.NodeNotFound:
        return render_template('index.html', cities=cities, error="Invalid source or destination.")

if __name__ == '__main__':
    app.run(debug=True)