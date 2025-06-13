import matplotlib.pyplot as plt

def plot_route(route, cities, title="Best Route"):
    x = [cities[i][0] for i in route] + [cities[route[0]][0]]
    y = [cities[i][1] for i in route] + [cities[route[0]][1]]
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, marker='o', linestyle='-')
    for city in route:
        plt.text(cities[city][0], cities[city][1], str(city), fontsize=9, color='blue')
        
    plt.title(title)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.show()
