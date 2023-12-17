import requests
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from tqdm import tqdm
import json
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from collections import Counter

tsv_file_path = 'data/imdb_basics_1200.tsv'

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

def extract_titles_from_tsv(file_path):
    titles = []
    with open(file_path, 'r') as file:
        for line in file:
            columns = line.split('\t')
            if len(columns) > 2:
                titles.append(columns[2])  
    return titles

        
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

def plot_3D(movie_graph):
    pos = nx.spring_layout(movie_graph, dim=3, seed=42)

    x_nodes = [pos[node][0] for node in movie_graph.nodes()]  
    y_nodes = [pos[node][1] for node in movie_graph.nodes()]  
    z_nodes = [pos[node][2] for node in movie_graph.nodes()]  

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(x_nodes, y_nodes, z_nodes)

    for edge in movie_graph.edges():
        x_edge = [pos[edge[0]][0], pos[edge[1]][0]]  
        y_edge = [pos[edge[0]][1], pos[edge[1]][1]]  
        z_edge = [pos[edge[0]][2], pos[edge[1]][2]] 
        ax.plot(x_edge, y_edge, z_edge, color='grey')

    # Set labels and title
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    plt.title('3D Graph Visualization')

    # Show the plot
    plt.show()

def plot_graph(G, option):
    if option == 1:
        nx.draw(G, with_labels=True)
    elif option == 2:
        nx.draw_circular(G, with_labels=True)
    plt.show()


def build_graph():
    G = nx.Graph()
    # movie_titles = ['The Great Nickel Robbery', 'The Great Water Peril', ]
    titles = extract_titles_from_tsv(tsv_file_path)
    for title in titles:
        movie_data = fetch_movie_data(title)
        if 'Title' in movie_data:  
            add_movie_to_graph(G, movie_data)
    return G 

def cache_movie_data(titles):   
    movie_data_cache = {}
    for title in tqdm(titles, desc="Fetching movie data"):
        movie_data = fetch_movie_data(title)
        if 'Title' in movie_data:  # Check if valid data was returned
            movie_data_cache[title] = movie_data
    with open('data/movie_data_cache.json', 'w') as json_file:
        json.dump(movie_data_cache, json_file, indent=4)

def build_graph_from_cache(titles):
    with open('data/movie_data_cache.json', 'r') as json_file:
        cached_movie_data = json.load(json_file)
    G = nx.Graph()
    for title, movie_data in cached_movie_data.items():
        add_movie_to_graph(G, movie_data)
    return G

def plot_director_genre_freq():
    with open('data/movie_data_cache.json', 'r') as file:
        movies = json.load(file)

    director_count = Counter()
    genre_count = Counter()

    for movie in movies.values():
        if 'Director' in movie:
            directors = movie['Director'].split(', ')
            for director in directors:
                director_count[director] += 1

        if 'Genre' in movie:
            genres = movie['Genre'].split(', ')
            for genre in genres:
                genre_count[genre] += 1

    directors, director_freq = zip(*director_count.most_common())
    genres, genre_freq = zip(*genre_count.most_common())

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=directors,
        y=director_freq,
        name='Directors',
        marker_color='indianred'
    ))

    fig.add_trace(go.Bar(
        x=genres,
        y=genre_freq,
        name='Genres',
        marker_color='lightsalmon'
    ))

    fig.update_layout(
        title='Director and Genre Frequency',
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='Frequency',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15, 
        bargroupgap=0.1 
    )

    fig.show()    

def get_node_degree(graph, node):
    try:
        return graph.degree[node]
    except KeyError:
        return None
    
def print_node_degree(movie_graph, node_name):
    degree = get_node_degree(movie_graph, node_name)

    if degree is not None:
        print(f"The degree of the node '{node_name}' is: {degree}")
    else:
        print(f"The node '{node_name}' does not exist in the graph.")

def main():
    # cache_movie_data(titles)
    print('Welcome')
    print('1. Print a 2D plot showing the graph structure')
    print('2. Print a 3D plot showing the graph structure')
    print('3. Plot the frequencies of each directors and genres')
    print('4. Know the degree of one node')
    while True:
        choice = input('Your choice [1/2/3/4/q]: ')
        if choice == '1':
            titles = extract_titles_from_tsv(tsv_file_path)
            G = build_graph_from_cache(titles)
            plot_with_plotly(G)
        elif choice == '2':
            titles = extract_titles_from_tsv(tsv_file_path)
            G = build_graph_from_cache(titles)
            plot_3D(G)
        elif choice == '3':
            plot_director_genre_freq()
        elif choice == '4':
            titles = extract_titles_from_tsv(tsv_file_path)
            G = build_graph_from_cache(titles)
            node_name = input('Input the film title or an actor name: ')
            print_node_degree(G, node_name)
        elif choice == 'q':
            print('Come again next time :)')
            break
        else:
            print('Invalid input! Please try again >_<')



if __name__ == "__main__":
    main()