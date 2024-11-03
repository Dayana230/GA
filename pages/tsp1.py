import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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

# Header Row
col1.write("City (with Icon)")
col2.write("X-coordinate")
col3.write("Y-coordinate")

# Collect user input in each row
for i in range(1, 11):
    # Dropdown to select city name from predefined list
    city_name = col1.selectbox(
        f"City {i} name", 
        options=[""] + list(city_icons.keys()),  # Empty option for blank selection
        key=f"city_name_{i}"
    )
    
    # Show icon next to selected city name
    if city_name:
        city_icon = city_icons[city_name]
        col1.markdown(f"{city_icon} **{city_name}**")
    
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

    # --- Genetic Algorithm Functions ---
    # (Define or paste all GA functions here as they are in your code)

    # Run the genetic algorithm to find the best route
    best_mixed_offspring = run_ga(cities_names, n_population, n_generations, crossover_per, mutation_per)
    total_dist_all_individuals = [total_dist_individual(ind) for ind in best_mixed_offspring]
    index_minimum = np.argmin(total_dist_all_individuals)
    minimum_distance = min(total_dist_all_individuals)

    # Display the shortest path and total distance
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
