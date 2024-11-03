import matplotlib.pyplot as plt
from itertools import permutations, combinations
from random import shuffle
import random
import numpy as np
import statistics
import pandas as pd
import seaborn as sns
import streamlit as st

# Title
st.title("City Coordinates Input")
st.write("Enter up to 10 cities with their coordinates (x, y) in range 0 - 100.")

# Define city names with icons
city_icons = {
    "Gliwice": "♕",
    "Cairo": "♖",
    "Rome": "♗",
    "Krakow": "♘",
    "Paris": "♙",
    "Alexandria": "♔",
    "Berlin": "♚",
    "Tokyo": "♛",
    "Rio": "♜",
    "Budapest": "♝"
}

# Define empty lists to store city names and coordinates
cities_names = []
city_coords = {}

# Create a table-like layout in landscape format
col1, col2, col3 = st.columns([2, 1, 1])  # Define three columns

# Collect user input in each row
for i in range(1, 11):
    # Dropdown to select city name from predefined list
    city_name = col1.selectbox(
        f"City {i}",
        options=[""] + list(city_icons.keys()),  # Empty option for blank selection
        key=f"city_name_{i}"
    )
    
    # Input fields for x and y coordinates
    x_coord = col2.number_input(f"x-coordinate (City {i})", min_value=0, max_value=100, step=1, key=f"x_coord_{i}")
    y_coord = col3.number_input(f"y-coordinate (City {i})", min_value=0, max_value=100, step=1, key=f"y_coord_{i}")

    # Store data if the city name is provided
    if city_name:
        cities_names.append(city_name)
        city_coords[city_name] = (x_coord, y_coord)

# GA Parameters
n_population = 250
crossover_per = 0.8
mutation_per = 0.2
n_generations = 200

# Define color palette for city markers
colors = sns.color_palette("pastel", len(cities_names))

# "Submit" button to run the algorithm
if st.button("Submit"):
    # Plot initial city locations with connections
    fig, ax = plt.subplots()
    for i, (city, (city_x, city_y)) in enumerate(city_coords.items()):
        color = colors[i]
        ax.scatter(city_x, city_y, c=[color], s=1200, zorder=2)
        
        # Display icon with city name on the plot
        city_icon = city_icons.get(city, "")
        ax.annotate(f"{city_icon} {city}", (city_x, city_y), fontsize=12, ha='center', va='bottom')

        # Draw faint lines between each pair of cities
        for j, (other_city, (other_x, other_y)) in enumerate(city_coords.items()):
            if i != j:
                ax.plot([city_x, other_x], [city_y, other_y], color='gray', linestyle='-', linewidth=1, alpha=0.1)

    fig.set_size_inches(16, 12)
    st.pyplot(fig)

# Genetic Algorithm functions (same as provided earlier)
# (Define or paste all GA functions here as they are in your code)

best_mixed_offspring = run_ga(cities_names, n_population, n_generations, crossover_per, mutation_per)

total_dist_all_individuals = []
for i in range(0, n_population):
    total_dist_all_individuals.append(total_dist_individual(best_mixed_offspring[i]))

index_minimum = np.argmin(total_dist_all_individuals)
minimum_distance = min(total_dist_all_individuals)

# Shortest path
shortest_path = best_mixed_offspring[index_minimum]
st.write(shortest_path)

x_shortest = []
y_shortest = []
for city in shortest_path:
    x_value, y_value = city_coords[city]
    x_shortest.append(x_value)
    y_shortest.append(y_value)

x_shortest.append(x_shortest[0])
y_shortest.append(y_shortest[0])

fig, ax = plt.subplots()
ax.plot(x_shortest, y_shortest, '--go', label='Best Route', linewidth=2.5)
plt.legend()

for i in range(len(x_shortest)):
    for j in range(i + 1, len(x_shortest)):
        ax.plot([x_shortest[i], x_shortest[j]], [y_shortest[i], y_shortest[j]], 'k-', alpha=0.09, linewidth=1)

plt.title(label="TSP Best Route Using GA",
          fontsize=25,
          color="k")

str_params = f'\n{n_generations} Generations\n{n_population} Population Size\n{crossover_per} Crossover\n{mutation_per} Mutation'
plt.suptitle("Total Distance Travelled: " +
             str(round(minimum_distance, 3)) +
             str_params, fontsize=18, y=1.047)

for i, txt in enumerate(shortest_path):
    ax.annotate(f"{i+1}- {txt}", (x_shortest[i], y_shortest[i]), fontsize=20)

fig.set_size_inches(16, 12)
st.pyplot(fig)
