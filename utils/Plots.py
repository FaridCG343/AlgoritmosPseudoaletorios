import numpy as np


def plot_scatter(data, ax=None, key='ri'):
    ri_values = [float(dic[key]) for dic in data if key in dic]
    ax.scatter(range(len(ri_values)), ri_values, color="#00E5EE")


def plot_run_sequence(data, ax=None, key='ri'):
    runs = []
    directions = []  # 1 up, -1 down

    for i in range(1, len(data)):
        if data[i][key] > data[i - 1][key]:
            runs.append(data[i - 1][key])
            directions.append(1)  # Up
        elif data[i][key] < data[i - 1][key]:
            runs.append(data[i - 1][key])
            directions.append(-1)  # Down

    # Add the last value
    runs.append(data[-1][key])
    if directions[-1] == 1:
        directions.append(1)
    else:
        directions.append(-1)

    # Convert to numpy arrays
    runs = np.array(runs)
    directions = np.array(directions)

    # Plot the runs
    for i in range(len(runs) - 1):
        if directions[i] == 1:
            ax.plot([i, i + 1], [runs[i], runs[i + 1]], 'g-')  # Verde para arriba
        else:
            ax.plot([i, i + 1], [runs[i], runs[i + 1]], 'r-')  # Rojo para abajo

    # Set the title and labels
    ax.set_title('Corrida Arriba/Abajo')
    ax.set_xlabel('Índice')
    ax.set_ylabel('Valor')

    # Set the grid
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)


def plot_box(data, ax=None, key='ri'):
    ri_values = [float(dic[key]) for dic in data if key in dic]
    boxprops = dict(linestyle='-', linewidth=3, color='#00E5EE')
    flierprops = dict(marker='o', color='#00E5EE', markersize=8)
    ax.boxplot(ri_values, boxprops=boxprops, flierprops=flierprops)


def plot_variance(data, ax=None, key='ri'):
    ri_values = [float(dic[key]) for dic in data if key in dic]
    ax.plot(range(len(ri_values)), ri_values, color="#00E5EE")


def plot_histogram(data, ax=None, key='ri'):
    ri_values = [float(dic[key]) for dic in data if key in dic]
    ax.hist(ri_values, bins=10, color="#00E5EE")
