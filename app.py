from flask import Flask, request, jsonify
import networkx as nx
import osmnx as ox
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/calculate_route', methods=['POST'])
def calculate_route():
    data = request.json
    start_point = data.get('start_point')
    arrive_point = data.get('arrive_point')
    
    G = nx.read_gpickle('graph5.pkl')
    start_node = ox.nearest_nodes(G, start_point[0], start_point[1])
    arrive_node = ox.nearest_nodes(G, arrive_point[0], arrive_point[1])
    
    route = nx.astar_path(G, start_node, arrive_node, weight='length')
    
    route_coords = []
    for i in range(len(route) - 1): #엣지 linestring에 있는 점들까지 포함하도록
        u, v = route[i], route[i + 1]
        if 'geometry' in G[u][v][0]:
            line = list(G[u][v][0]['geometry'].coords)
            del line[-1]
            for point in line:
                route_coords.append({'X': point[0], 'Y': point[1]})
        else:
            route_coords.append({'X': G.nodes[u]['x'], 'Y': G.nodes[u]['y']})
    route_coords.append({'X': G.nodes[route[-1]]['x'], 'Y': G.nodes[route[-1]]['y']})
    
    return jsonify({"route": route_coords})

if __name__ == '__main__':
    app.run(port=8000)