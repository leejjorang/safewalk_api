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
    
    G = nx.read_gpickle('graph7.pkl')
    start_node = ox.nearest_nodes(G, start_point[0], start_point[1])
    arrive_node = ox.nearest_nodes(G, arrive_point[0], arrive_point[1])
    
    def custom_weight(u, v, data):
        length_weight = data.get('length')
        final_weight = data.get('final')
        return length_weight + final_weight
    
    route = nx.astar_path(G, start_node, arrive_node, weight=custom_weight)
    
    route_coords = [] #linestring에 있는 점들도 포함
    for i in range(len(route) - 1):
        u, v = route[i], route[i + 1]
        start_coord = G.nodes[u]['x'], G.nodes[u]['y']

        if 'geometry' in G[u][v]:
            line = list(G[u][v]['geometry'].coords)
            if start_coord != line[0]: #linstring 좌표 순서가 경로와 맞는지 확인
                line = line[::-1]
            del line[-1]
            for point in line:
                route_coords.append({'X': point[0], 'Y': point[1]})
        else:
            route_coords.append({'X': G.nodes[u]['x'], 'Y': G.nodes[u]['y']})
    #마지막노드 따로 추가
    route_coords.append({'X': G.nodes[route[-1]]['x'], 'Y': G.nodes[route[-1]]['y']})
    
    return jsonify({"route": route_coords})

if __name__ == '__main__':
    app.run(port=8000)