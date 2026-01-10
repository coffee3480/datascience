import networkx as nx
import matplotlib.pyplot as plt

with open('input3.txt') as file:
    text=file.read()
lines=text.split('\n')
n=int(lines[0].split()[0]) #значение n - количество узлов
m=int(lines[0].split()[1]) #значение m - количество рёбер
lines.pop(0)
v=lines[0].split()
for i in range(len(v)):
    v[i]=int(v[i]) #сохраняем веса узлов в массив v
lines.pop(0)
for i in range(len(lines)):
    lines[i]=lines[i].split()

# создаем граф
g=nx.Graph()

for i in range(n):
    j=str(i+1)
    g.add_node(j, weight=v[i]) # добавляем в граф узлы с весами из массива v

for i in range(m):
    g.add_edge(lines[i][0], lines[i][1]) # добавляем ребра по списку ребёр из файла input.txt

# метод поиска всех простых путей обхода графа (каждый узел и ребро обходятся 1 раз)
def find_paths(graph,start_node):
    paths=[]
    stack=[(start_node, [start_node])]
    while stack:
        (current_node, path)=stack.pop()
        paths.append(path)
        for neighbor in graph.neighbors(current_node):
            if neighbor not in path:
                stack.append((neighbor, path+[neighbor])) #Двойные скобки, так как нужен двойной массив
    return paths

values=[] # в массив values будем сохранять сумму весов узлов при обходе графа
for node in g: # из каждого узла графа получим все возможные пути обхода графа
    paths=find_paths(g, node)
    for p in paths:
        summ=0 # считаем сумму весов узлов для текущего маршрута обхода графа
        for node in p:
            summ+=v[int(node)-1]
        values.append(summ) # сохраняем сумму в массив values
print(max(values)) # выводим на экран максимальное значение
# отрисовка графа
nx.draw(g, with_labels=True)
plt.show()
