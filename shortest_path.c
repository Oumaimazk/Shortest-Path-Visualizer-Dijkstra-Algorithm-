#include <stdio.h>
#include <limits.h>
#include <string.h>

#define V 11 // Nombre de lieux
#define OUTPUT_FILE "all_paths.json" // Nom du fichier JSON

// Fonction pour trouver le sommet avec la plus petite distance
int minDistance(double dist[], int visited[]) {
    double min = INT_MAX;
    int min_index = -1;

    for (int v = 0; v < V; v++) {
        if (!visited[v] && dist[v] <= min) {
            min = dist[v];
            min_index = v;
        }
    }
    return min_index;
}

// Algorithme de Dijkstra
void dijkstra(double graph[V][V], int src, int dest, char places[V][30], char path[V][30], int *path_length, double *distance) {
    double dist[V];
    int visited[V] = {0};
    int parent[V];

    // Initialiser les distances et les parents
    for (int i = 0; i < V; i++) {
        dist[i] = INT_MAX;
        parent[i] = -1;
    }
    dist[src] = 0;

    // Calculer le plus court chemin
    for (int count = 0; count < V - 1; count++) {
        int u = minDistance(dist, visited);
        visited[u] = 1;

        for (int v = 0; v < V; v++) {
            if (!visited[v] && graph[u][v] && dist[u] != INT_MAX &&
                dist[u] + graph[u][v] < dist[v]) {
                dist[v] = dist[u] + graph[u][v];
                parent[v] = u;
            }
        }
    }

    // Construire le chemin
    int stack[V], top = -1;
    int current = dest;

    while (current != -1) {
        stack[++top] = current;
        current = parent[current];
    }

    *path_length = 0;

    // Remplir le chemin dans l'ordre correct
    while (top >= 0) {
        strcpy(path[(*path_length)++], places[stack[top--]]);
    }

    *distance = dist[dest];
}

// Générer tous les chemins pour toutes les paires (source, destination)
void generateAllPaths(double graph[V][V], char places[V][30]) {
    FILE *file = fopen(OUTPUT_FILE, "w");
    if (!file) {
        printf("Erreur : Impossible de créer le fichier JSON.\n");
        return;
    }

    fprintf(file, "[\n");

    // Parcourir toutes les paires (source, destination)
    for (int src = 0; src < V; src++) {
        for (int dest = 0; dest < V; dest++) {
            if (src != dest) {
                char path[V][30];
                int path_length;
                double distance;

                // Calculer le plus court chemin
                dijkstra(graph, src, dest, places, path, &path_length, &distance);

                // Ajouter les résultats au fichier JSON
                fprintf(file, "  {\n");
                fprintf(file, "    \"source\": \"%s\",\n", places[src]);
                fprintf(file, "    \"destination\": \"%s\",\n", places[dest]);
                fprintf(file, "    \"path\": [");

                for (int i = 0; i < path_length; i++) {
                    fprintf(file, "\"%s\"", path[i]);
                    if (i < path_length - 1) fprintf(file, ", ");
                }

                fprintf(file, "],\n");
                fprintf(file, "    \"distance\": %.2f\n", distance);
                fprintf(file, "  }");

                if (src < V - 1 || dest < V - 1) fprintf(file, ",");
                fprintf(file, "\n");
            }
        }
    }

    fprintf(file, "]\n");
    fclose(file);
    printf("Tous les chemins ont été générés dans %s\n", OUTPUT_FILE);
}

int main() {
    // Liste des lieux
    char places[V][30] = {
        "Boukhalef", "Achakar", "Mesnana", "Marjane", "SocoAlto",
        "MarinaBay", "Iberia", "Bnimakada", "Merchan", "TanjaBalia", "RiadTetouan"
    };

    // Matrice des distances (en km)
    double graph[V][V] = {
        {0, 7.4, 4.7, 5.6, 999, 999, 999, 999, 999, 999, 999},
        {7.4, 0, 999, 999, 12.3, 999, 999, 999, 999, 999, 999},
        {4.7, 999, 0, 2.2, 4.9, 999, 5.9, 999, 999, 999, 999},
        {5.6, 999, 2.2, 0, 999, 999, 999, 3.8, 999, 999, 999},
        {999, 12.3, 4.9, 999, 0, 999, 3.3, 999, 999, 999, 999},
        {999, 999, 999, 999, 999, 0, 3.3, 999, 3, 6.7, 3.6},
        {999, 999, 5.9, 999, 3.3, 3.3, 0, 4.6, 1, 999, 2.7},
        {999, 999, 999, 3.8, 999, 999, 4.6, 0, 999, 999, 4.4},
        {999, 999, 999, 999, 999, 3, 1, 999, 0, 999, 999},
        {999, 999, 999, 999, 999, 6.7, 999, 999, 999, 0, 4.4},
        {999, 999, 999, 999, 999, 3.6, 2.7, 4.4, 999, 4.4, 0}
    };

    // Générer tous les chemins
    generateAllPaths(graph, places);

    return 0;
}
