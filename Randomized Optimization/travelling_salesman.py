import mlrose
import random
import timeit
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
matplotlib.use('TkAgg')

from mlrose.generators import TSPGenerator

"""
The Travelling Salesman Problem, TSP:
"Given a list of cities and the distances between each pair of cities, what is the shortest possible route that visits each city and returns to the origin city?"

Citation: WR Hamilton and Thomas Kirkman (1800's) per https://en.wikipedia.org/wiki/Travelling_salesman_problem
"""

num_cities = 22
random_search_algos = ["rhc", "sa", "ga", "mimic"]
iterations_range_short = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
iterations_range_long = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
OUTPUT_DIRECTORY = './Experiments'

# Generate the travelling sales problem and the fitness function
fitness_fxn = TSPGenerator.generate(seed=random.randint(0,100), number_of_cities=num_cities, area_height= 100, area_width=100)

def plot_fitness_single_algo(title, iterations, fitness, algorithm):
	plt.figure
	plt.title(title)
	plt.xlabel("Number of Iterations")
	plt.ylabel("Fitness, ie Total Travel Distance")
	plt.plot(iterations, fitness, 'o-', color="r", label=algorithm)
	plt.legend(loc="best")
	plt.show()

def plot_time_single_algo(title, iterations, time, algorithm):
	plt.figure
	plt.title(title)
	plt.xlabel("Number of Iterations")
	plt.ylabel("Convergence Time (seconds)")
	plt.plot(iterations, time, 'o-', color="b", label=algorithm)
	plt.legend(loc="best")
	plt.show()

#========== Random Hill Climb ==========#
# Optimize the algorithm parameters (Manual)
def opt_rhc_params():
	rhc = mlrose.runners.RHCRunner(problem=fitness_fxn,
						experiment_name='Optimal Params for TSP RHC',
						output_directory=OUTPUT_DIRECTORY,
						seed=random.randint(1, 100),
						iteration_list=2 ** np.arange(1,12),
						max_attempts=5000,
						restart_list=[0, 5, 20, 30, 45, 60, 75])
	rhc_df_run_stats, rhc_df_run_curves = rhc.run()
	ideal_rs = rhc_df_run_stats[['Restarts']].iloc[rhc_df_run_stats[['Fitness']].idxmin()] # from the output of the experiment above
	return rhc_df_run_stats, rhc_df_run_curves, ideal_rs

# # Done on a complex example then  hard coded optimized parameter value(s).
# rhc_df_run_stats, rhc_df_run_curves, ideal_rs = opt_rhc_params()

ideal_rs = 75  # this came from the results of the experiment commented out, above.
rhc_best_state = []
rhc_best_fitness = []
rhc_convergence_time = []
for iter in iterations_range_short:
	start_time = timeit.default_timer()
	best_state, best_fitness = mlrose.random_hill_climb(problem=fitness_fxn, max_iters=iter, max_attempts=500,
														restarts=ideal_rs)
	end_time = timeit.default_timer()
	convergence_time = (end_time - start_time)  # seconds
	rhc_best_state.append(best_state)
	rhc_best_fitness.append(best_fitness)
	rhc_convergence_time.append(convergence_time)

plot_fitness_single_algo(title="Travelling Salesman, Tuned Random Hill Climbing",
						 iterations=iterations_range_short, fitness=rhc_best_fitness, algorithm='RHC')
plot_time_single_algo(title="Travelling Salesman, Tuned Random Hill Climbing",
						 iterations=iterations_range_short, time=rhc_convergence_time, algorithm='RHC')


#========== Genetic Algorithms ==========#
# Optimize the algorithm parameters (Manual)
# Done on a complex example then  hard coded optimized parameter value(s).
def opt_ga_params():
	ga = mlrose.runners.GARunner(problem=fitness_fxn,
					  experiment_name='Optimal Params for TSP GA',
					  output_directory=OUTPUT_DIRECTORY,
					  seed=random.randint(1, 100),
					  iteration_list=2 ** np.arange(1,12),
					  max_attempts=1000,
					  population_sizes=[10, 50, 100, 200, 300],
					  mutation_rates=[0.2, 0.4, 0.6, 0.8, 1])
	ga_df_run_stats, ga_df_run_curves = ga.run()
	ideal_pop_size = ga_df_run_stats[['Population Size']].iloc[ga_df_run_stats[['Fitness']].idxmin()]  # from the output of the experiment above
	ideal_mutation_rate = ga_df_run_stats[['Mutation Rate']].iloc[ga_df_run_stats[['Fitness']].idxmin()]  # from the output of the experiment above
	return ga_df_run_stats, ga_df_run_curves, ideal_pop_size, ideal_mutation_rate

ga_df_run_stats, ga_df_run_curves, ideal_pop_size, ideal_mutation_rate = opt_ga_params()

ga_best_state = []
ga_best_fitness = []
ga_convergence_time = []
for iter in iterations_range_short:
	start_time = timeit.default_timer()
	best_state, best_fitness = mlrose.genetic_alg(problem=fitness_fxn, mutation_prob = ideal_mutation_rate,
					      max_attempts = 500, max_iters = iter, pop_size=ideal_pop_size)
	end_time = timeit.default_timer()
	convergence_time = (end_time - start_time)  # seconds
	ga_best_state.append(best_state)
	ga_best_fitness.append(best_fitness)
	ga_convergence_time.append(convergence_time)

plot_fitness_single_algo(title="Travelling Salesman, Tuned Genetic Algorithm",
						 iterations=iterations_range_short, fitness=ga_best_fitness, algorithm='Genetic')
plot_time_single_algo(title="Travelling Salesman, Tuned Genetic Algorithm",
						 iterations=iterations_range_short, time=ga_convergence_time, algorithm='Genetic')

# print('The best route found using genetic algorithms is: ', best_state)
# print('The fitness at the best route found using genetic algorithms is: ', best_fitness)

#========== Simulated Annealing ==========#
# Optimize the algorithm parameters (Manual)
# Done on a complex example then  hard coded optimized parameter value(s).
def opt_sa_params():
	sa = mlrose.runners.SARunner(problem=fitness_fxn,
				  experiment_name='Optimal Params for TSP SA',
				  output_directory=OUTPUT_DIRECTORY,
				  seed=random.randint(1, 100),
				  iteration_list=2 ** np.arange(12),
				  max_attempts=5000,
				  temperature_list=[1, 10, 50, 100, 250, 500, 1000, 2500, 5000, 10000])
	sa_df_run_stats, sa_df_run_curves = sa.run()
	ideal_temp = sa_df_run_stats[['Temperature']].iloc[sa_df_run_stats[['Fitness']].idxmin()]  # from the output of the experiment above
	return sa_df_run_stats, sa_df_run_curves, ideal_temp

sa_df_run_stats, sa_df_run_curves, ideal_temp = opt_sa_params()

sa_best_state = []
sa_best_fitness = []
sa_convergence_time = []
for iter in iterations_range_short:
	start_time = timeit.default_timer()
	best_state, best_fitness = mlrose.simulated_annealing(problem=fitness_fxn, max_attempts = 500,
														  max_iters = iter)
	end_time = timeit.default_timer()
	convergence_time = (end_time - start_time)  # seconds
	sa_best_state.append(best_state)
	sa_best_fitness.append(best_fitness)
	sa_convergence_time.append(convergence_time)

plot_fitness_single_algo(title="Travelling Salesman, Tuned Simulated Annealing",
						 iterations=iterations_range_short, fitness=sa_best_fitness, algorithm='Simulated Annealing')
plot_time_single_algo(title="Travelling Salesman, Tuned Simulated Annealing",
						 iterations=iterations_range_short, time=sa_convergence_time, algorithm='Simulated Annealing')


#========== Mutual-Information-Maximizing Input Clustering (MIMIC) ==========#
# Optimize the algorithm parameters (Manual)
# Done on a complex example then  hard coded optimized parameter value(s).

def opt_mimic_params():
	mmc = mlrose.runners.MIMICRunner(problem=fitness_fxn,
				  experiment_name='Optimal Params for TSP MIMIC',
				  output_directory=OUTPUT_DIRECTORY,
				  seed=random.randint(1, 100),
				  iteration_list=2 ** np.arange(12),
				  max_attempts=5000,
				  keep_percent_list=[0.1, 0.25, 0.5, 0.75])
	mmc_df_run_stats, mmc_df_run_curves = mmc.run()
	ideal_keep_prcnt = mmc_df_run_stats[['Keep Percent']].iloc[mmc_df_run_stats[['Fitness']].idxmin()]  # from the output of the experiment above
	return mmc_df_run_stats, mmc_df_run_curves, ideal_keep_prcnt

mmc_df_run_stats, mmc_df_run_curves, ideal_keep_prcnt = opt_mimic_params()

mimic_best_state = []
mimic_best_fitness = []
mimic_convergence_time = []
for iter in iterations_range_long:
	start_time = timeit.default_timer()
	best_state, best_fitness = mlrose.mimic(problem=fitness_fxn, pop_size=num_cities,
											keep_pct=ideal_keep_prcnt, max_attempts=1000, max_iters=iter)
	end_time = timeit.default_timer()
	convergence_time = (end_time - start_time)  # seconds
	mimic_best_state.append(best_state)
	mimic_best_fitness.append(best_fitness)
	mimic_convergence_time.append(convergence_time)

plot_fitness_single_algo(title="Travelling Salesman, Tuned Mutual-Information-Maximizing Input Clustering (MIMIC)",
						 iterations=iterations_range_long, fitness=mimic_best_fitness, algorithm='MIMIC')
plot_time_single_algo(title="Travelling Salesman, Tuned Mutual-Information-Maximizing Input Clustering (MIMIC)",
						 iterations=iterations_range_long, time=mimic_convergence_time, algorithm='MIMIC')



# Comparison of all four optimization algorithms
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
fig.suptitle('Comparison of Random Search Optimizers: Fitness and Convergence Time')

ax1.set(xlabel="Number of Iterations", ylabel="Fitness, ie Total Travel Distance")
ax1.grid()
ax1.plot(iterations_range_short, rhc_best_fitness, 'o-', color="r", label='Random Hill Climbing')
ax1.plot(iterations_range_short, ga_best_fitness, 'o-', color="b", label='Genetic Algorithms')
ax1.plot(iterations_range_short, sa_best_fitness, 'o-', color="o", label='Simulated Annealing')
ax1.plot(iterations_range_long, mimic_best_fitness, 'o-', color="g", label='MIMIC')
ax1.legend(loc="best")

ax2.set(xlabel="Number of Iterations", ylabel="Convergence Time (in seconds)")
ax2.grid()
ax2.plot(iterations_range_short, rhc_convergence_time, 'o-', color="r", label='Random Hill Climbing')
ax2.plot(iterations_range_short, ga_convergence_time, 'o-', color="b", label='Genetic Algorithms')
ax2.plot(iterations_range_short, sa_convergence_time, 'o-', color="o", label='Simulated Annealing')
ax2.plot(iterations_range_long, mimic_convergence_time, 'o-', color="g", label='MIMIC')
ax2.legend(loc="best")

plt.show()
print("you are done!")
