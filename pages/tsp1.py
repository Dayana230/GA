import matplotlib.pyplot as plt
from itertools import permutations
import random
import numpy as np
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

# Function definitions
def initial_population(cities_list, n_population=250):
    population_perms = []
    possible_perms = list(permutations(cities_list))
    random_ids = random.sample(range(0, len(possible_perms)), n_population)
    for i in random_ids:
        population_perms.append(list(possible_perms[i]))
    return population_perms

def dist_two_cities(city_1, city_2):
    city_1_coords = city_coords[city_1]
    city_2_coords = city_coords[city_2]
    return np.sqrt(np.sum((np.array(city_1_coords) - np.array(city_2_coords))**2))

def total_dist_individual(individual):
    total_dist = 0
    for i in range(0, len(individual)):
        if i == len(individual) - 1:
            total_dist += dist_two_cities(individual[i], individual[0])
        else:
            total_dist += dist_two_cities(individual[i], individual[i + 1])
    return total_dist

def fitness_prob(population):
    total_dist_all_individuals = [total_dist_individual(ind) for ind in population]
    max_population_cost = max(total_dist_all_individuals)
    population_fitness = max_population_cost - total_dist_all_individuals
    population_fitness_sum = sum(population_fitness)
    population_fitness_probs = population_fitness / population_fitness_sum
    return population_fitness_probs

def roulette_wheel(population, fitness_probs):
    population_fitness_probs_cumsum = fitness_probs.cumsum()
    bool_prob_array = population_fitness_probs_cumsum < np.random.uniform(0, 1, 1)
    selected_individual_index = len(bool_prob_array[bool_prob_array == True]) - 1
    return population[selected_individual_index]

def crossover(parent_1, parent_2):
    n_cities_cut = len(cities_names) - 1
    cut = round(random.uniform(1, n_cities_cut))
    offspring_1 = parent_1[:cut] + [city for city in parent_2 if city not in parent_1[:cut]]
    offspring_2 = parent_2[:cut] + [city for city in parent_1 if city not in parent_2[:cut]]
    return offspring_1, offspring_2

def mutation(offspring):
    n_cities_cut = len(cities_names) - 1
    index_1 = round(random.uniform(0, n_cities_cut))
    index_2 = round(random.uniform(0, n_cities_cut))
    offspring[index_1], offspring[index_2] = offspring[index_2], offspring[index_1]
    return offspring

def run_ga(cities_names, n_population, n_generations, crossover_per, mutation_per):
    population = initial_population(cities_names, n_population)
    for _ in range(n_generations):
        fitness_probs = fitness_prob(population)
        parents_list = [roulette_wheel(population, fitness_probs) for _ in range(int(crossover_per * n_population))]
        
        offspring_list = []
        for i in range(0, len(parents_list), 2):
            offspring_1, offspring_2 = crossover(parents_list[i], parents_list[i + 1])
            if random.random() < mutation_per:
                offspring_1 = mutation(offspring_1)
            if random.random() < mutation_per:
                offspring_2 = mutation(offspring_2)
            offspring_list.extend([offspring_1, offspring_2])

        mixed_offspring = parents_list + offspring_list
        population = sorted(mixed_offspring, key=total_dist_individual)[:n_population]

    return population

# Run the GA and plot the best route
if st.button("Submit"):
    # Initial Population Plot
    initial_population = initial_population(cities_names, n_population=5)  # Limit initial routes for clarity
    fig1, ax1 = plt.subplots()
    for route in initial_population:
        x_route, y_route = zip(*(city_coords[city] for city in route + [route[0]]))
        ax1.plot(x_route, y_route, 'o-', label="Route")
    ax1.set_title("Initial Random Routes")
    fig1.set_size_inches(8, 6)
    st.pyplot(fig1)
    
    # GA Optimized Route Plot
    best_mixed_offspring = run_ga(cities_names, n_population, n_generations, crossover_per, mutation_per)
    total_dist_all_individuals = [total_dist_individual(ind) for ind in best_mixed_offspring]
    index_minimum = np.argmin(total_dist_all_individuals)
    minimum_distance = min(total_dist_all_individuals)
    
    shortest_path = best_mixed_offspring[index_minimum]
    x_shortest, y_shortest = zip(*(city_coords[city] for city in shortest_path))
    x_shortest, y_shortest = list(x_shortest) + [x_shortest[0]], list(y_shortest) + [y_shortest[0]]
    
    fig2, ax2 = plt.subplots()
    ax2.plot(x_shortest, y_shortest, '--go', label='Best Route', linewidth=2.5)
    ax2.set_title(f"TSP Best Route Using GA\nTotal Distance: {round(minimum_distance, 3)}")
    fig2.set_size_inches(8, 6)
    st.pyplot(fig2)
