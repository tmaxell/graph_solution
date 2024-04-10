import tkinter as tk
from tkinter import messagebox

# DFS
def dfs(graph, node, visited, treasures_collected, path):
    visited.add(node)
    path.append(node)

    if node in treasures:
        treasures_collected.add(node)
        if len(treasures_collected) == len(treasures):
            return path  # Вернуть путь, если все сокровища собраны

    for neighbor in graph[node]:
        if neighbor not in visited:
            new_path = dfs(graph, neighbor, visited, treasures_collected, path.copy())
            if new_path:
                return new_path
    
    return None

def draw_edge(canvas, start, end):
    x1, y1 = nodes[start]
    x2, y2 = nodes[end]
    canvas.create_line(x1, y1, x2, y2)

def click_node(event):
    global current_node
    for node, (x, y) in nodes.items():
        if abs(event.x - x) < node_radius and abs(event.y - y) < node_radius:
            current_node = node
            if current_node not in treasures:
                treasures.add(current_node)
                canvas.create_oval(x - treasure_radius, y - treasure_radius, x + treasure_radius, y + treasure_radius, fill='yellow')

def double_click_node(event):
    global current_node
    for node, (x, y) in nodes.items():
        if abs(event.x - x) < node_radius and abs(event.y - y) < node_radius:
            current_node = node
            messagebox.showinfo("Сокровище", "Сокровище установлено в вершине: " + current_node)

def add_edge(event):
    global edge_start
    global edge_end
    for node, (x, y) in nodes.items():
        if abs(event.x - x) < node_radius and abs(event.y - y) < node_radius:
            if edge_start is None:
                edge_start = node
                return
            elif edge_end is None:
                edge_end = node
                draw_edge(canvas, edge_start, edge_end)
                if edge_start not in graph:
                    graph[edge_start] = []
                if edge_end not in graph:
                    graph[edge_end] = []
                graph[edge_start].append(edge_end)
                graph[edge_end].append(edge_start)
                edge_start = None
                edge_end = None
                return

def calculate_path():
    # Используем DFS для поиска оптимального пути
    visited = set()
    treasures_collected = set()
    start_node = 'вход'
    optimal_path = dfs(graph, start_node, visited, treasures_collected, [])

    # Результат
    if optimal_path:
        messagebox.showinfo("Оптимальный путь", "Оптимальный путь для сбора сокровищ и возврата ко входу: " + str(optimal_path))
        for i in range(len(optimal_path)-1):
            draw_edge(canvas, optimal_path[i], optimal_path[i+1])
    else:
        messagebox.showinfo("Ошибка", "Сокровища не могут быть собраны.")

# Местоположение сокровищ
treasures = set()
current_node = None
edge_start = None
edge_end = None
graph = {}

# Создание окна
root = tk.Tk()
root.title("Сбор сокровищ")

# Создание холста
canvas = tk.Canvas(root, width=800, height=600, bg="white")
canvas.pack(expand=True, fill="both")

# Рисование вершин
node_radius = 20
treasure_radius = 10
nodes = {}

# Обработка кликов по вершинам
canvas.bind("<Button-1>", click_node)
canvas.bind("<Double-1>", double_click_node)

# Обработка кликов правой кнопкой мыши для добавления ребра
canvas.bind("<Button-3>", add_edge)

# Кнопка для расчета пути
calculate_button = tk.Button(root, text="Рассчитать путь", command=calculate_path)
calculate_button.pack()

root.mainloop()
