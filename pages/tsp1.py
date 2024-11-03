import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from itertools import permutations
import random

# Input form for city names and coordinates
st.title("City Coordinates Input")
st.write("Enter up to 10 cities with their coordinates (x, y) in range 0 - 100.")

# Initialize lists for cities and coordinates
city_names = []
x_coords = []
y_coords = []

# Add input fields for up to 10 cities
for i in range(10):
    city_name = st.text_input(f"City {i + 1}", key=f"city_name_{i}")
    x_coord = st.number_input(f"x-coordinate (City {i + 1})", min_value=0.0, max_value=100.0, step=0.1, key=f"x_coord_{i}")
    y_coord = st.number_input(f"y-coordinate (City {i + 1})", min_value=0.0, max_value=100.0, step=0.1, key=f"y_coord_{i}")
    
    if city_name:
        city_names.append(city_name)
        x_coords.append(x_coord)
        y_coords.append(y_coord)

# Check if at least two cities are provided
if len(city_names) >= 2:
    city_coords = dict(zip(city_names, zip(x_coords, y_coords)))

    # Genetic Algorithm Parameters
    n_population = 250
    crossover_per = 0.8
    mutation_per = 0.2
    n_generations = 200

    # Pastel Palette
    colors = sns.color_palette("pastel", len(city_names))

    # Plot the city map
    fig, ax = plt.subplots()
    ax.grid(False)

    for i, (city, (city_x, city_y)) in enumerate(city_coords.items()):
        color = colors[i]
        ax.scatter(city_x, city_y, c=[color], s=1200, zorder=2)
        ax.annotate(city, (city_x, city_y), fontsize=12, ha='center', va='center', zorder=3)

        for j, (other_city, (other_x, other_y)) in enumerate(city_coords.items()):
            if i != j:
                ax.plot([city_x, other_x], [city_y, other_y], color='gray', linestyle='-', linewidth=1, alpha=0.1)

    fig.set_size_inches(10, 6)
    st.pyplot(fig)

    # (Include the rest of the Genetic Algorithm implementation here...)
else:
    st.write("Please enter at least two cities with valid coordinates to proceed.")
