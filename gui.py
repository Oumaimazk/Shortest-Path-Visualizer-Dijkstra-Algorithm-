import json
import customtkinter as ctk
from tkinter import messagebox
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Fonction pour charger les données du fichier JSON
def load_data():
    try:
        with open("all_paths.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        messagebox.showerror("Erreur", "Le fichier JSON n'a pas été trouvé. Exécutez le programme C pour le générer.")
        return None

# Fonction pour trouver le chemin entre deux lieux dans les données JSON
def find_path(data, source, destination):
    for item in data:
        if item["source"] == source and item["destination"] == destination:
            return item
    return None

# Classe principale pour l'application
class PathVisualizerApp:
    def __init__(self, root):
        ctk.set_appearance_mode("Dark")  # Mode sombre
        ctk.set_default_color_theme("blue")  # Thème de couleur

        self.root = root
        self.root.title("Chemin le plus court avec Dijkstra")
        self.root.geometry("1200x800")

        # Initialisation des attributs
        self.places = [
            "Boukhalef", "Achakar", "Mesnana", "Marjane", "SocoAlto",
            "MarinaBay", "Iberia", "Bnimakada", "Merchan", "TanjaBalia", "RiadTetouan"
        ]
        self.data = load_data()
        self.G = nx.DiGraph()
        self.canvas = None
        self.fig = None
        self.ax = None

        # Créer le graphe initial
        self.create_graph()

        # Créer les widgets
        self.create_widgets()

        # Afficher le graphe initial
        self.draw_graph()

    def create_graph(self):
        edges = [
            ("Boukhalef", "Achakar", 7.4), ("Boukhalef", "Mesnana", 4.7),
            ("Boukhalef", "Marjane", 5.6), ("Achakar", "SocoAlto", 12.3),
            ("Mesnana", "Marjane", 2.2), ("Mesnana", "SocoAlto", 4.9),
            ("Mesnana", "Iberia", 5.9), ("Marjane", "Bnimakada", 3.8),
            ("SocoAlto", "Iberia", 3.3), ("MarinaBay", "Iberia", 3.3),
            ("MarinaBay", "Merchan", 3.0), ("MarinaBay", "TanjaBalia", 6.7),
            ("MarinaBay", "RiadTetouan", 3.6), ("Iberia", "Bnimakada", 4.6),
            ("Iberia", "Merchan", 1.0), ("Iberia", "RiadTetouan", 2.7),
            ("Bnimakada", "RiadTetouan", 4.4), ("TanjaBalia", "RiadTetouan", 4.4)
        ]
        self.G.add_weighted_edges_from(edges)

    def create_widgets(self):
        # Cadre supérieur pour le contrôle
        control_frame = ctk.CTkFrame(self.root, corner_radius=10, fg_color="#1F1F1F")
        control_frame.pack(side=ctk.TOP, fill=ctk.X, pady=10, padx=10)

        # Widgets de sélection des lieux
        ctk.CTkLabel(control_frame, text="Lieu de départ:", font=("Arial", 14), text_color="white").pack(side=ctk.LEFT, padx=5)
        self.source_var = ctk.StringVar(value=self.places[0])
        source_menu = ctk.CTkOptionMenu(control_frame, variable=self.source_var, values=self.places, fg_color="#2E2E2E")
        source_menu.pack(side=ctk.LEFT, padx=5)

        ctk.CTkLabel(control_frame, text="Lieu de destination:", font=("Arial", 14), text_color="white").pack(side=ctk.LEFT, padx=5)
        self.destination_var = ctk.StringVar(value=self.places[1])
        destination_menu = ctk.CTkOptionMenu(control_frame, variable=self.destination_var, values=self.places, fg_color="#2E2E2E")
        destination_menu.pack(side=ctk.LEFT, padx=5)

        ctk.CTkButton(control_frame, text="Visualiser le chemin", command=self.calculate_path, fg_color="#0066CC").pack(side=ctk.LEFT, padx=10)

        # Widget pour afficher les informations sur le chemin
        self.info_frame = ctk.CTkFrame(self.root, corner_radius=10, fg_color="#1F1F1F")
        self.info_frame.pack(side=ctk.BOTTOM, fill=ctk.X, pady=10, padx=10)

        self.distance_label = ctk.CTkLabel(self.info_frame, text="Distance totale : N/A", font=("Arial", 14), text_color="red")
        self.distance_label.pack(anchor="w", padx=10, pady=5)

        self.path_label = ctk.CTkLabel(self.info_frame, text="Chemin suivi : N/A", font=("Arial", 14), text_color="white")
        self.path_label.pack(anchor="w", padx=10, pady=5)

        self.cost_label = ctk.CTkLabel(self.info_frame, text="Coût total : N/A", font=("Arial", 14), text_color="white")
        self.cost_label.pack(anchor="w", padx=10, pady=5)

        # Cadre pour afficher le graphe
        self.graph_frame = ctk.CTkFrame(self.root, corner_radius=10, fg_color="#1F1F1F")
        self.graph_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

        # Canvas matplotlib
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.fig.patch.set_facecolor('#1F1F1F')  # Couleur de fond pour le graphique
        self.ax.set_facecolor('#2E2E2E')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=ctk.BOTH, expand=True)

    def draw_graph(self, path=None):
        self.ax.clear()
        pos = nx.spring_layout(self.G, seed=42, k=3.0)

        nx.draw_networkx_edges(self.G, pos, ax=self.ax, edge_color='white')
        nx.draw_networkx_nodes(self.G, pos, ax=self.ax, node_color='#6699FF', node_size=3000)
        nx.draw_networkx_labels(self.G, pos, ax=self.ax, font_size=10, font_color='white')

        if path:
            path_edges = list(zip(path[:-1], path[1:]))
            nx.draw_networkx_edges(self.G, pos, edgelist=path_edges, edge_color='red', width=2.5, ax=self.ax)

        edge_labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels, ax=self.ax, font_size=8, font_color='black')

        self.canvas.draw()

    def calculate_path(self):
        source = self.source_var.get()
        destination = self.destination_var.get()

        if source == destination:
            messagebox.showwarning("Attention", "La source et la destination ne peuvent pas être les mêmes.")
            return

        if not self.data:
            return

        path_data = find_path(self.data, source, destination)

        if not path_data:
            self.distance_label.configure(text="Distance totale : Aucun chemin trouvé")
            self.path_label.configure(text="Chemin suivi : Aucun")
            self.cost_label.configure(text="Coût total : N/A")
            messagebox.showinfo("Information", f"Aucun chemin trouvé entre {source} et {destination}.")
            return

        self.draw_graph(path_data['path'])
        distance = path_data.get('distance', 'Inconnu')
        path = " --> ".join(path_data['path'])
        cost = distance * 4  # Exemple : coût de 5 unités par km

        self.distance_label.configure(text=f"Distance la plus courte entre {source} et {destination} est : {distance} km")
        self.path_label.configure(text=f"Chemin suivi : {path}")
        self.cost_label.configure(text=f"Coût total (petit taxi) : {cost} DH")

# Lancer l'application
if __name__ == "__main__":
    root = ctk.CTk()
    app = PathVisualizerApp(root)
    root.mainloop()
