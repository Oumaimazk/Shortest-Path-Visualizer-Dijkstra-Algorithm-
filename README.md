# Shortest Path Visualizer (Dijkstra Algorithm) - Tangier 🚗

This project is a desktop application designed to find and visualize the shortest path between various landmarks in the city of **Tangier, Morocco**. It uses the **Dijkstra algorithm** for pathfinding, with a core logic implemented in C for efficiency and a modern GUI built in Python.

## 🌟 Features

- **Shortest Path Calculation**: Uses the Dijkstra algorithm to find the most efficient route between two points.
- **Interactive GUI**: A sleek, dark-themed interface built with `customtkinter`.
- **Graph Visualization**: Real-time visualization of the city's landmarks and routes using `networkx` and `matplotlib`.
- **Taxi Cost Estimation**: Automatically calculates the estimated fare (in DH) based on the distance.
- **All-Pairs Shortest Paths**: Pre-calculated data for all possible source-destination pairs for instant feedback.

## 🧮 Mathematical Foundation: Dijkstra's Algorithm

The core of this project is based on the **Dijkstra Algorithm**, a graph search algorithm that solves the single-source shortest path problem for a graph with non-negative edge path costs.

### 1. Formal Definition
Given a graph $G = (V, E)$ where:
- $V$ is a set of vertices (Landmarks like Boukhalef, Iberia).
- $E$ is a set of weighted edges $(u, v) \in E$ representing the distance between landmarks.
- $w(u, v) \geq 0$ is the weight (distance in km) of the edge from $u$ to $v$.

### 2. The Algorithm Logic
The algorithm maintains a set $S$ of vertices whose shortest-path distances from the source $s$ have already been determined. It repeatedly selects the vertex $u \in V - S$ with the minimum shortest-path estimate, adds $u$ to $S$, and relaxes all edges leaving $u$.

**The Relaxation Step:**
For each neighbor $v$ of $u$:
If $dist(u) + w(u, v) < dist(v)$, then:
$$dist(v) \leftarrow dist(u) + w(u, v)$$
$$parent(v) \leftarrow u$$

### 3. Complexity
- **Time Complexity**: $O(V^2)$ with the current adjacency matrix implementation in `shortest_path.c`, which is optimal for the dense connectivity of city landmarks.
- **Space Complexity**: $O(V)$ to store the distances and parent pointers.

## 🏗️ Architecture

The project consists of two main components:
1.  **Backend (C)**: Implements the Dijkstra algorithm. It processes a distance matrix of Tangier's landmarks and generates a JSON file (`all_paths.json`) containing the shortest paths and distances for every possible trip.
2.  **Frontend (Python)**: A GUI that reads the JSON data, allows user selection, and renders the graph visualization.

## 📍 Landmarks Included

- Boukhalef
- Achakar
- Mesnana
- Marjane
- SocoAlto
- MarinaBay
- Iberia
- Bnimakada
- Merchan
- TanjaBalia
- RiadTetouan

## 🛠️ Technologies Used

- **C**: Core algorithm implementation.
- **Python 3.x**: GUI and visualization.
- **CustomTkinter**: Modern UI components.
- **NetworkX**: Graph data structure and manipulation.
- **Matplotlib**: Graph rendering.
- **JSON**: Data exchange between C and Python.

## 🚀 How to Run

### 1. Generate the Path Data (C)
If you need to update the graph or distances, compile and run the C program:
```bash
gcc shortest_path.c -o shortest_path
./shortest_path
```
*Note: This will generate/update the `all_paths.json` file.*

### 2. Run the Visualization (Python)
Ensure you have the required dependencies installed:
```bash
pip install customtkinter networkx matplotlib
```
Then, run the GUI application:
```bash
python gui.py
```

## 📸 Preview

The application displays a graph where:
- **Nodes** represent city landmarks.
- **Edges** represent available routes with their distances in km.
- **Highlighted Red Path** shows the calculated shortest route.

---
*Created as part of an algorithm study on Dijkstra's shortest path.*
