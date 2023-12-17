import requests
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# API_KEY = 'f9e81bc7'

def fetch_movie_data(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey=d6bb16df"
    data = requests.get(url).json()
    return data

def add_movie_to_graph(graph, movie_data):
    title = movie_data['Title']
    actors = movie_data['Actors'].split(', ')
    # Add more attributes as needed
    graph.add_node(title)
    for actor in actors:
        graph.add_edge(title, actor)

# def plot_with_plotly(G):
#     pos =   (G)
#     edge_x, edge_y, node_x, node_y = [], [], [], []

#     for edge in G.edges():
#         x0, y0 = pos[edge[0]]
#         x1, y1 = pos[edge[1]]
#         edge_x.extend([x0, x1, None])
#         edge_y.extend([y0, y1, None])

#     edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=0.5, color='#888'), mode='lines')

#     for node in G.nodes():
#         x, y = pos[node]
#         node_x.append(x)
#         node_y.append(y)

#     node_trace = go.Scatter(x=node_x, y=node_y, mode='markers', marker=dict(size=10, color='blue'), text=list(G.nodes()))

#     fig = go.Figure(data=[edge_trace, node_trace])
#     fig.show()
        
def plot_with_plotly(G):
    pos = nx.spring_layout(G)  # This computes the position of nodes using the spring layout algorithm
    edge_x, edge_y, node_x, node_y = [], [], [], []

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=0.5, color='#888'), mode='lines')

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(x=node_x, y=node_y, mode='markers', marker=dict(size=10, color='blue'), text=list(G.nodes()))

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.show()

# G = nx.Graph()
# movie_titles = ['The Great Nickel Robbery', 'The Great Water Peril'] # Replace with actual movie titles
# for title in movie_titles:
#     data = fetch_movie_data(title)
#     print(data)
#     add_movie_to_graph(G, data)

# nx.draw(G, with_labels=True)
# plt.show()

def plot_graph(G, option):
    if option == 1:
        nx.draw(G, with_labels=True)
    elif option == 2:
        # Different type of graph representation
        nx.draw_circular(G, with_labels=True)
    # Add more options for different graph types or data representations
    plt.show()

# def main():
#     G = nx.Graph()  # Your graph should be built here
#     while True:
#         print("Choose an option for data presentation:")
#         print("1. Basic Graph")
#         print("2. Circular Graph")
#         print("3. Exit")
#         choice = input("Enter your choice (1/2/3): ")
#         if choice == '3':
#             break
#         plot_graph(G, int(choice))
    

def main():
    G = nx.Graph()
    movie_titles = ['The Great Nickel Robbery', 'The Great Water Peril', ]
    for title in movie_titles:
        data = fetch_movie_data(title)
        print(data)
        add_movie_to_graph(G, data)

    plot_with_plotly(G)


if __name__ == "__main__":
    main()