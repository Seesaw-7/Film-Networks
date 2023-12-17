# Film-Networks
## How to run

An API key is embeded into the program.
run with `python3 main.py`
When a user input is prompted, enter 1 to display a 2D plot, enter 2 to display a 3D plot, enter 3 to display frequency counts, enter 4 to query the degree of a node, and enter q to quit.
You could interact with 1~3 plots with popped windows. 

## Data Structure
The data structure used is networkx.Graph(). 
Movie titles, Actors and crew are presented as nodes. An edge between a title and a human being indicates that the human contributes to that film.
