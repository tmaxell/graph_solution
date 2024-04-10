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

# граф
graph = {
    'вход': ['комната1', 'комната2'],
    'комната1': ['комната3', 'коридор1'],
    'комната2': ['коридор1', 'комната4'],
    'комната3': ['коридор1', 'коридор2'],
    'комната4': ['коридор2', 'коридор3'],
    'коридор1': ['комната5'],
    'коридор2': ['коридор4'],
    'коридор3': ['выход'],
    'комната5': ['выход'],
    'коридор4': ['выход']
}

# Местоположение сокровищ
treasures = {'комната3', 'комната5'}

# Используем DFS для поиска оптимального пути
visited = set()
treasures_collected = set()
start_node = 'вход'
optimal_path = dfs(graph, start_node, visited, treasures_collected, [])

# результат
if optimal_path:
    print("Оптимальный путь для сбора сокровищ и возврата ко входу:", optimal_path)
else:
    print("Сокровища не могут быть собраны.")
