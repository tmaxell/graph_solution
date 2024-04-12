import tkinter as tk
from tkinter import ttk
import networkx as nx
from collections import deque

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Поиск сокровища")

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
        if len(self.nodes) < 3 or not self.treasures:
            print("Недостаточно вершин или сокровищ для построения цикла")
            return

        start_node = self.nodes[0]  # Стартовая вершина
        visited = set()  # Множество посещенных вершин
        path = [start_node]  # Путь, который мы будем строить
        treasures_to_visit = set(self.treasures)  # Множество оставшихся для посещения сокровищ
        total_length = 0.0  # Общая длина пути

        def dfs(node):
            nonlocal total_length

            visited.add(node)  # Помечаем текущую вершину как посещенную
            if node in treasures_to_visit:  # Если текущая вершина содержит сокровище
                treasures_to_visit.remove(node)  # Удаляем сокровище из списка оставшихся для посещения
                # Добавляем длину ребра, если оно существует
                if (path[-1], node) in self.edges:
                    total_length += self.graph.edges[path[-1], node]['weight']

            for neighbor in self.graph.neighbors(node):  # Проходимся по соседям текущей вершины
                if neighbor not in visited:  # Если соседняя вершина не посещена
                    path.append(neighbor)  # Добавляем ее в путь
                    dfs(neighbor)  # Рекурсивно вызываем обход для соседней вершины

        dfs(start_node)  # Запускаем обход в глубину из стартовой вершины

        # Добавляем ребро, соединяющее последнюю вершину в пути с начальной, если оно существует
        if (path[-1], start_node) in self.edges:
            total_length += self.graph.edges[path[-1], start_node]['weight']
            path.append(start_node)

        print("Кратчайший путь с сокровищами:", path)
        print("Стоимость всего пути:", total_length)

        # Отображаем путь на холсте
        self.canvas.delete("cycle")
        for i in range(len(path) - 1):
            x1, y1 = map(int, path[i].strip("()").split(", "))
            x2, y2 = map(int, path[i + 1].strip("()").split(", "))
            self.canvas.create_line(x1, y1, x2, y2, fill="red", arrow=tk.LAST, tags="cycle")

        self.table.insert("", "end", values=("Итоговая стоимость пути:", "", f"{total_length:.2f}"))


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
