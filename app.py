from flask import Flask, request, jsonify
import networkx as nx
import osmnx as ox

app = Flask(__name__)

@app.route('/calculate_route', methods=['POST'])
def calculate_route():
    data = request.json
    start_point = data.get('start_point')
    arrive_point = data.get('arrive_point')
    
    G = nx.read_gpickle('graph5.pkl')
    start_node = ox.nearest_nodes(G, start_point[0], start_point[1])
    arrive_node = ox.nearest_nodes(G, arrive_point[0], arrive_point[1])
    
    route = nx.astar_path(G, start_node, arrive_node, weight='length')
    route_coords = [{'lat': G.nodes[n]['lat'], 'lon': G.nodes[n]['lon']} for n in route]
    
    return jsonify({"route": route_coords})

if __name__ == '__main__':
    app.run(port=5000, debug=True)