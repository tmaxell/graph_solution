import tkinter as tk
from tkinter import ttk
import networkx as nx
import math
import random

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Поиск кратчайшего гамильтонова цикла")

        self.graph = nx.Graph()
        self.nodes = {}
        self.edges = []
        self.start_node = None
        self.node_count = 1

        self.canvas = tk.Canvas(self.root, width=600, height=400)
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.add_node)
        self.canvas.bind("<Button-2>", self.start_edge)
        self.canvas.bind("<Double-Button-1>", self.set_treasure)  

        self.frame = ttk.Frame(self.root)
        self.frame.pack()

        self.find_cycle_button = ttk.Button(self.frame, text="Поиск цикла", command=self.find_cycle)
        self.find_cycle_button.grid(row=0, column=0)

        self.clear_button = ttk.Button(self.frame, text="Очистить полотно", command=self.clear_canvas)
        self.clear_button.grid(row=0, column=1)

        self.table = ttk.Treeview(self.frame, columns=("start", "end", "weight"), show="headings")
        self.table.heading("start", text="Начальная вершина")
        self.table.heading("end", text="Конечная вершина")
        self.table.heading("weight", text="Вес ребра")
        self.table.grid(row=1, column=0, columnspan=2)

    def add_node(self, event):
        x, y = event.x, event.y
        node = f"({x}, {y})"
        if node not in self.nodes:
            self.graph.add_node(node)
            self.nodes[node] = {'treasure': False, 'color': 'black', 'id': self.node_count}  
            self.table.insert("", "end", values=(node, "", ""))
            self.canvas.create_oval(x-5, y-5, x+5, y+5, fill=self.nodes[node]['color'])  
            self.canvas.create_text(x, y, text=str(self.node_count), fill="white")
            self.node_count += 1

    def start_edge(self, event):
        x, y = event.x, event.y
        closest_node = None
        min_distance = float('inf')
        for node in self.nodes.keys():
            nx, ny = map(int, node.strip("()").split(", "))
            distance = ((x - nx) ** 2 + (y - ny) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                closest_node = node
        if closest_node:
            if self.start_node is None:
                self.start_node = closest_node
            else:
                end_node = closest_node
                weight = min_distance
                if (self.start_node, end_node) not in self.edges and (end_node, self.start_node) not in self.edges:
                    self.graph.add_edge(self.start_node, end_node, weight=weight)
                    self.edges.append((self.start_node, end_node, weight))
                    self.table.insert("", "end", values=(self.start_node, end_node, f"{weight:.2f}"))
                    x1, y1 = map(int, self.start_node.strip("()").split(", "))
                    x2, y2 = map(int, end_node.strip("()").split(", "))
                    self.canvas.create_line(x1, y1, x2, y2, fill="blue")
                self.start_node = None

    def set_treasure(self, event):
        x, y = event.x, event.y
        closest_node = None
        min_distance = float('inf')
        for node, data in self.nodes.items():
            nx, ny = map(int, node.strip("()").split(", "))
            distance = ((x - nx) ** 2 + (y - ny) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                closest_node = node
        if closest_node:
            self.nodes[closest_node]['treasure'] = not self.nodes[closest_node]['treasure']
            if self.nodes[closest_node]['treasure']:
                self.nodes[closest_node]['color'] = 'gold'
            else:
                self.nodes[closest_node]['color'] = 'black'
            self.canvas.delete("all")
            self.redraw_graph()

    def find_cycle(self):
        if len(self.nodes) < 3:
            print("Недостаточно вершин для построения цикла")
            return

        start_node = next(iter(self.nodes))  # Начинаем с первой вершины в графе

        treasures = [node for node, data in self.nodes.items() if data['treasure']]  # Список вершин с сокровищами

        edge_subgraph = self.graph.edge_subgraph(self.edges)  # Подграф, содержащий только заданные ребра

        all_treasure_paths = {}
        for treasure in treasures:
            path = nx.shortest_path(edge_subgraph, start_node, treasure, weight='weight')
            all_treasure_paths[treasure] = path

        all_paths = [nx.shortest_path(edge_subgraph, path[-1], start_node, weight='weight') for path in all_treasure_paths.values()]

        shortest_length = float('inf')
        shortest_path = []

        for path in all_paths:
            length = sum(edge_subgraph[path[i]][path[i+1]]['weight'] for i in range(len(path) - 1))
            if length < shortest_length:
                shortest_length = length
                shortest_path = path

        print("Кратчайший путь с сокровищами:", shortest_path)
        print("Стоимость всего пути:", shortest_length)

        self.canvas.delete("cycle")
        for i in range(len(shortest_path) - 1):
            x1, y1 = map(int, shortest_path[i].strip("()").split(", "))
            x2, y2 = map(int, shortest_path[i+1].strip("()").split(", "))
            self.canvas.create_line(x1, y1, x2, y2, fill="red", arrow=tk.LAST, tags="cycle")
        x1, y1 = map(int, shortest_path[-1].strip("()").split(", "))
        x2, y2 = map(int, shortest_path[0].strip("()").split(", "))
        self.canvas.create_line(x1, y1, x2, y2, fill="red", arrow=tk.LAST, tags="cycle")

        self.table.insert("", "end", values=("Итоговая стоимость пути:", "", f"{shortest_length:.2f}"))

    def redraw_graph(self):
        for node, data in self.nodes.items():
            x, y = map(int, node.strip("()").split(", "))
            self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=data['color'])
            self.canvas.create_text(x, y, text=str(data['id']), fill="white")
        for edge in self.graph.edges():
            x1, y1 = map(int, edge[0].strip("()").split(", "))
            x2, y2 = map(int, edge[1].strip("()").split(", "))
            self.canvas.create_line(x1, y1, x2, y2, fill="blue")

    def clear_canvas(self):
        self.graph.clear()
        self.nodes.clear()
        self.edges.clear()
        self.canvas.delete("all")
        self.table.delete(*self.table.get_children())
        self.node_count = 1

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
