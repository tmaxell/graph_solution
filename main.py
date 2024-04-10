import tkinter as tk
from tkinter import ttk
import networkx as nx
import math
import random
import itertools
from collections import deque

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Поиск кратчайшего гамильтонова цикла")

        self.graph = nx.Graph()
        self.nodes = []
        self.edges = []
        self.start_node = None
        self.treasures = []

        self.canvas = tk.Canvas(self.root, width=600, height=400)
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.add_node)
        self.canvas.bind("<Double-Button-1>", self.set_treasure)
        self.canvas.bind("<Button-2>", self.start_edge)

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

        self.node_count = 1

    def add_node(self, event):
        x, y = event.x, event.y
        node = f"({x}, {y})"
        if node not in self.nodes:
            self.graph.add_node(node)
            self.nodes.append(node)
            self.table.insert("", "end", values=(node, "", ""))
            self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="black")
            self.canvas.create_text(x, y, text=str(self.node_count), fill="white")
            self.node_count += 1

    def set_treasure(self, event):
        x, y = event.x, event.y
        closest_node = None
        min_distance = float('inf')
        for node in self.nodes:
            nx, ny = map(int, node.strip("()").split(", "))
            distance = ((x - nx) ** 2 + (y - ny) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                closest_node = node
        if closest_node:
            if closest_node not in self.treasures:
                self.treasures.append(closest_node)
                self.canvas.create_text(x, y, text="T", fill="red")

    def start_edge(self, event):
        x, y = event.x, event.y
        closest_node = None
        min_distance = float('inf')
        for node in self.nodes:
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

    def find_cycle(self):
        if len(self.nodes) < 3:
            print("Недостаточно вершин для построения цикла")
            return

        edge_subgraph = self.graph.edge_subgraph([(edge[0], edge[1]) for edge in self.edges])  # Подграф, содержащий только заданные ребра

        shortest_length = float('inf')
        shortest_path = []

        for perm in itertools.permutations(self.treasures):  # Перебираем все возможные порядки сокровищ
            start_node = next(iter(self.nodes))  # Начинаем с первой вершины в графе
            current_path = [start_node]  # Текущий путь
            current_length = 0  # Длина текущего пути
            visited = set()  # Множество посещенных вершин

            for treasure in perm:
                queue = deque([(start_node, [])])  # Очередь для поиска в ширину
                found = False
                while queue:
                    current_node, path = queue.popleft()
                    if current_node == treasure:  # Нашли сокровище
                        current_path.extend(path)  # Добавляем путь до сокровища к текущему пути
                        current_length += sum(edge_subgraph[path[i]][path[i+1]]['weight'] for i in range(len(path) - 1) if (path[i], path[i+1]) in edge_subgraph.edges)  # Обновляем длину текущего пути
                        visited.update(path)  # Обновляем посещенные вершины
                        current_path.append(current_node)  # Добавляем сокровище к текущему пути
                        current_length += sum(edge_subgraph[current_node][next_node]['weight'] for next_node in edge_subgraph.neighbors(current_node))  # Обновляем длину текущего пути
                        start_node = current_node  # Обновляем начальную вершину для следующего поиска
                        found = True
                        break
                    if current_node not in visited:
                        visited.add(current_node)
                        for neighbor in edge_subgraph.neighbors(current_node):
                            if neighbor in path:
                                continue
                            queue.append((neighbor, path + [current_node]))

                if not found:
                    break

            if not found:
                continue

            current_path.append(next(iter(self.nodes)))  # Добавляем возвращение в начальную вершину
            current_length += sum(edge_subgraph[current_path[i]][current_path[i+1]]['weight'] for i in range(len(current_path) - 1) if (current_path[i], current_path[i+1]) in edge_subgraph.edges)  # Обновляем длину текущего пути

            if current_length < shortest_length:  # Если текущий путь короче кратчайшего найденного пути
                shortest_length = current_length  # Обновляем кратчайшую длину
                shortest_path = current_path  # Обновляем кратчайший путь

        print("Кратчайший путь с сокровищами:", shortest_path)
        print("Стоимость всего пути:", shortest_length)

        self.canvas.delete("cycle")
        for i in range(len(shortest_path) - 1):
            x1, y1 = map(int, shortest_path[i].strip("()").split(", "))
            x2, y2 = map(int, shortest_path[i+1].strip("()").split(", "))
            self.canvas.create_line(x1, y1, x2, y2, fill="red", arrow=tk.LAST, tags="cycle")

        self.table.insert("", "end", values=("Итоговая стоимость пути:", "", f"{shortest_length:.2f}"))

    def clear_canvas(self):
        self.graph.clear()
        self.nodes.clear()
        self.edges.clear()
        self.treasures.clear()
        self.canvas.delete("all")
        self.table.delete(*self.table.get_children())
        self.node_count = 1

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
