import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from itertools import permutations
from random import shuffle
import random

# User Input Section
st.title("City Coordinates Input")
st.write("Enter up to 10 cities with their coordinates (x, y) in range 0 - 100.")

# Initialize city data storage
cities_names = []
city_coords = {}

# Dynamic input fields for up to 10 cities
for i in range(1, 11):
    city_name = st.text_input(f"City {i} name", key=f"city_name_{i}")
    x_coord = st.number_input(f"x-coordinate (City {i})", min_value=0.0, max_value=100.0, key=f"x_coord_{i}")
    y_coord = st.number_input(f"y-coordinate (City {i})", min_value=0.0, max_value=100.0, key=f"y_coord_{i}")
    
    if city_name:
        cities_names.append(city_name)
        city_coords[city_name] = (x_coord, y_coord)

# GA Parameters
n_population = 250
crossover_per = 0.8
mutation_per = 0.2
n_generations = 200

# Pastel Pallete for City Colors
colors = sns.color_palette("pastel", len(cities_names))

# Display button
if st.button("Submit"):
    # Plot the cities with their names
    fig, ax = plt.subplots()
    for i, (city, (city_x, city_y)) in enumerate(city_coords.items()):
        color = colors[i]
        ax.scatter(city_x, city_y, c=[color], s=1200, zorder=2)
        ax.annotate(city, (city_x, city_y), fontsize=12, ha='center', va='bottom')

        # Connect cities with opaque lines
        for j, (other_city, (other_x, other_y)) in enumerate(city_coords.items()):
            if i != j:
                ax.plot([city_x, other_x], [city_y, other_y], color='gray', linestyle='-', linewidth=1, alpha=0.1)

    fig.set_size_inches(16, 12)
    st.pyplot(fig)

    # Your genetic algorithm code will be executed here after button click

    # --- Genetic Algorithm Functions ---
    # (Define or place the remaining GA functions here as they are in your code)

    # Run GA to find shortest path
    best_mixed_offspring = run_ga(cities_names, n_population, n_generations, crossover_per, mutation_per)
    total_dist_all_individuals = [total_dist_individual(ind) for ind in best_mixed_offspring]
    index_minimum = np.argmin(total_dist_all_individuals)
    minimum_distance = min(total_dist_all_individuals)

    # Display the shortest path
    shortest_path = best_mixed_offspring[index_minimum]
    st.write("Shortest Path:", shortest_path)
    st.write("Total Distance:", round(minimum_distance, 3))

    # Plot the shortest route
    x_shortest = [city_coords[city][0] for city in shortest_path] + [city_coords[shortest_path[0]][0]]
    y_shortest = [city_coords[city][1] for city in shortest_path] + [city_coords[shortest_path[0]][1]]

    fig, ax = plt.subplots()
    ax.plot(x_shortest, y_shortest, '--go', label='Best Route', linewidth=2.5)
    plt.legend()

    for i in range(len(x_shortest) - 1):
        ax.annotate(f"{i+1} - {shortest_path[i]}", (x_shortest[i], y_shortest[i]), fontsize=12)

    plt.title("TSP Best Route Using GA")
    fig.set_size_inches(16, 12)
    st.pyplot(fig)
