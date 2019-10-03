import mlrose
import timeit
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
matplotlib.use('TkAgg')
import datetime

from mlrose.generators import TSPGenerator

"""
The Travelling Salesman Problem, TSP:
"Given a list of cities and the distances between each pair of cities, what is the shortest possible route that visits each city and returns to the origin city?"

Citation: WR Hamilton and Thomas Kirkman (1800's) per https://en.wikipedia.org/wiki/Travelling_salesman_problem
"""

num_cities = 22
iterations_range = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
OUTPUT_DIRECTORY = './Experiments/TSP'

# Generate the fitness problem and the optimization function
problem = TSPGenerator.generate(seed=17, number_of_cities=num_cities, area_height= 100, area_width=100)

def plot_fitness_single_algo(title, iterations, fitness, algorithm):
	plt.title(title)
	plt.xlabel("Number of Iterations")
	plt.ylabel("Fitness, ie Total Travel Distance")
	plt.plot(iterations, fitness, 'o-', color="r", label=algorithm)
	plt.legend(loc="best")
	plt.savefig(title + " - Fitness.png")

def plot_time_single_algo(title, iterations, time, algorithm):
	plt.title(title)
	plt.xlabel("Number of Iterations")
	plt.ylabel("Convergence Time (seconds)")
	plt.plot(iterations, time, 'o-', color="b", label=algorithm)
	plt.legend(loc="best")
	plt.savefig(title + " - Time.png")

#========== Random Hill Climb ==========#
time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
print("Starting Random Hill Climbing at: " + time)
# Optimize the algorithm parameters (Manual)
def opt_rhc_params():
	rhc = mlrose.runners.RHCRunner(problem=problem,
								   experiment_name='Optimal Params for TSP RHC',
								   output_directory=OUTPUT_DIRECTORY,
								   seed=17,
								   iteration_list=2 ** np.arange(1,12),
								   max_attempts=5000,
								   restart_list=[0, 5, 20, 30, 45, 60, 75])
	rhc_df_run_stats, rhc_df_run_curves = rhc.run()
	ideal_rs = rhc_df_run_stats[['current_restart']].iloc[rhc_df_run_stats[['Fitness']].idxmin()] # from the output of the experiment above
	return rhc_df_run_stats, rhc_df_run_curves, ideal_rs

# # Done on a complex example then  hard coded optimized parameter value(s).
# rhc_df_run_stats, rhc_df_run_curves, ideal_rs = opt_rhc_params()

ideal_rs = 75  # this came from the results of the experiment commented out, above.

rhc_best_state = []
rhc_best_fitness = []
rhc_convergence_time = []
for iter in iterations_range:
	start_time = timeit.default_timer()
	best_state, best_fitness = mlrose.random_hill_climb(problem=problem, max_iters=iter, max_attempts=500,
														restarts=ideal_rs)
	end_time = timeit.default_timer()
	convergence_time = (end_time - start_time)  # seconds
	rhc_best_state.append(best_state)
	rhc_best_fitness.append(best_fitness)
	rhc_convergence_time.append(convergence_time)

print('The fitness at the best state found using Random Hill Climbing is: ', min(rhc_best_fitness))

#========== Genetic Algorithms ==========#
time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
print("Starting Genetic Algorithms at: " + time)
# Optimize the algorithm parameters (Manual)
def opt_ga_params():
	ga = mlrose.runners.GARunner(problem=problem,
								 experiment_name='Optimal Params for TSP GA',
								 output_directory=OUTPUT_DIRECTORY,
								 seed=17,
								 iteration_list=2 ** np.arange(1,12),
								 max_attempts=1000,
								 population_sizes=[10, 50, 100, 200, 300],
								 mutation_rates=[0.2, 0.4, 0.6, 0.8, 1])
	ga_df_run_stats, ga_df_run_curves = ga.run()
	ideal_pop_size = ga_df_run_stats[['Population Size']].iloc[ga_df_run_stats[['Fitness']].idxmin()]  # from the output of the experiment above
	ideal_mutation_rate = ga_df_run_stats[['Mutation Rate']].iloc[ga_df_run_stats[['Fitness']].idxmin()]  # from the output of the experiment above
	return ga_df_run_stats, ga_df_run_curves, ideal_pop_size, ideal_mutation_rate

# Done on a complex example then  hard coded optimized parameter value(s).
# ga_df_run_stats, ga_df_run_curves, ideal_pop_size, ideal_mutation_rate = opt_ga_params()

ideal_pop_size = 175  # this came from the results of the experiment commented out, above.
ideal_mutation_rate = 0.6  # this came from the results of the experiment commented out, above.

ga_best_state = []
ga_best_fitness = []
ga_convergence_time = []
for iter in iterations_range:
	start_time = timeit.default_timer()
	best_state, best_fitness = mlrose.genetic_alg(problem=problem, mutation_prob = ideal_mutation_rate,
												  max_attempts = 500, max_iters = iter, pop_size=ideal_pop_size)
	end_time = timeit.default_timer()
	convergence_time = (end_time - start_time)  # seconds
	ga_best_state.append(best_state)
	ga_best_fitness.append(best_fitness)
	ga_convergence_time.append(convergence_time)

print('The fitness at the best state found using Genetic Algorithms is: ', min(ga_best_fitness))

#========== Simulated Annealing ==========#
time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
print("Starting Simulated Annealing at: " + time)
# Optimize the algorithm parameters (Manual)
def opt_sa_params():
	sa = mlrose.runners.SARunner(problem=problem,
								 experiment_name='Optimal Params for TSP SA',
								 output_directory=OUTPUT_DIRECTORY,
								 seed=17,
								 iteration_list=2 ** np.arange(12),
								 max_attempts=5000,
								 temperature_list=[1, 10, 50, 100, 250, 500, 1000, 2500, 5000, 10000])
	sa_df_run_stats, sa_df_run_curves = sa.run()
	ideal_temp = sa_df_run_stats[['Temperature']].iloc[sa_df_run_stats[['Fitness']].idxmin()]  # from the output of the experiment above
	return sa_df_run_stats, sa_df_run_curves, ideal_temp

# Done on a complex example then  hard coded optimized parameter value(s).
# sa_df_run_stats, sa_df_run_curves, ideal_initial_temp = opt_sa_params()

ideal_initial_temp = 1  # this came from the results of the experiment commented out, above.
sa_best_state = []
sa_best_fitness = []
sa_convergence_time = []
for iter in iterations_range:
	start_time = timeit.default_timer()
	best_state, best_fitness = mlrose.simulated_annealing(problem=problem, max_attempts = 500,
									max_iters = iter,
									schedule=mlrose.GeomDecay(init_temp=ideal_initial_temp))
	end_time = timeit.default_timer()
	convergence_time = (end_time - start_time)  # seconds
	sa_best_state.append(best_state)
	sa_best_fitness.append(best_fitness)
	sa_convergence_time.append(convergence_time)

print('The fitness at the best state found using Simulated Annealing is: ', min(sa_best_fitness))

#========== Mutual-Information-Maximizing Input Clustering (MIMIC) ==========#
time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
print("Starting MIMIC at: " + time)
# Optimize the algorithm parameters (Manual)
def opt_mimic_params():
	mmc = mlrose.runners.MIMICRunner(problem=problem,
									 experiment_name='Optimal Params for TSP MIMIC',
									 output_directory=OUTPUT_DIRECTORY,
									 seed=17,
									 iteration_list=2 ** np.arange(13),
									 max_attempts=5000,
									 keep_percent_list=[0.1, 0.25, 0.5, 0.75])
	mmc_df_run_stats, mmc_df_run_curves = mmc.run()
	ideal_keep_prcnt = mmc_df_run_stats[['Keep Percent']].iloc[mmc_df_run_stats[['Fitness']].idxmin()]  # from the output of the experiment above
	return mmc_df_run_stats, mmc_df_run_curves, ideal_keep_prcnt

# Done on a complex example then  hard coded optimized parameter value(s).
# mmc_df_run_stats, mmc_df_run_curves, ideal_keep_prcnt = opt_mimic_params()

ideal_keep_prcnt = 0.5  # this came from the results of the experiment commented out, above.

mimic_best_state = []
mimic_best_fitness = []
mimic_convergence_time = []
for iter in iterations_range:
	start_time = timeit.default_timer()
	best_state, best_fitness = mlrose.mimic(problem=problem, keep_pct=ideal_keep_prcnt,
											max_attempts=5000, max_iters=iter, pop_size=ideal_pop_size)
	end_time = timeit.default_timer()
	convergence_time = (end_time - start_time)  # seconds
	mimic_best_state.append(best_state)
	mimic_best_fitness.append(best_fitness)
	mimic_convergence_time.append(convergence_time)

print('The fitness at the best state found using MIMIC is: ', min(mimic_best_fitness))

#======= Plots for all individual learners==========#
# Random Hill Climbing
plt.figure(1)
plot_fitness_single_algo(title="Travelling Salesman, Tuned Random Hill Climbing",
						 iterations=iterations_range, fitness=rhc_best_fitness, algorithm='RHC - Fitness')
plt.figure(2)
plot_time_single_algo(title="Travelling Salesman, Tuned Random Hill Climbing",
						 iterations=iterations_range, time=rhc_convergence_time, algorithm='RHC - Time')

# Genetic Algorithms
plt.figure(3)
plot_fitness_single_algo(title="Travelling Salesman, Tuned Genetic Algorithm",
						 iterations=iterations_range, fitness=ga_best_fitness, algorithm='Genetic - Fitness')
plt.figure(4)
plot_time_single_algo(title="Travelling Salesman, Tuned Genetic Algorithm",
						 iterations=iterations_range, time=ga_convergence_time, algorithm='Genetic - Time')

# Simulated Annealing
plt.figure(5)
plot_fitness_single_algo(title="Travelling Salesman, Tuned Simulated Annealing",
						 iterations=iterations_range, fitness=sa_best_fitness, algorithm='Simulated Annealing - Fitness')
plt.figure(6)
plot_time_single_algo(title="Travelling Salesman, Tuned Simulated Annealing",
						 iterations=iterations_range, time=sa_convergence_time, algorithm='Simulated Annealing - Time')

# MIMIC
plt.figure(7)
plot_fitness_single_algo(title="Travelling Salesman, Tuned Mutual-Information-Maximizing Input Clustering (MIMIC)",
						 iterations=iterations_range, fitness=mimic_best_fitness, algorithm='MIMIC - Fitness')
plt.figure(8)
plot_time_single_algo(title="Travelling Salesman, Tuned Mutual-Information-Maximizing Input Clustering (MIMIC)",
					  iterations=iterations_range, time=mimic_convergence_time, algorithm='MIMIC - Time')

#======= Comparison of all four optimization algorithms ==========#
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
fig.suptitle('Comparison of Random Search Optimizers: Fitness and Convergence Time')

ax1.set(xlabel="Number of Iterations", ylabel="Fitness, ie Total Travel Distance")
ax1.grid()
ax1.plot(iterations_range, rhc_best_fitness, 'o-', color="r", label='Random Hill Climbing')
ax1.plot(iterations_range, ga_best_fitness, 'o-', color="b", label='Genetic Algorithms')
ax1.plot(iterations_range, sa_best_fitness, 'o-', color="m", label='Simulated Annealing')
ax1.plot(iterations_range, mimic_best_fitness, 'o-', color="g", label='MIMIC')
ax1.legend(loc="best")

ax2.set(xlabel="Number of Iterations", ylabel="Convergence Time (in seconds)")
ax2.grid()
ax2.plot(iterations_range, rhc_convergence_time, 'o-', color="r", label='Random Hill Climbing')
ax2.plot(iterations_range, ga_convergence_time, 'o-', color="b", label='Genetic Algorithms')
ax2.plot(iterations_range, sa_convergence_time, 'o-', color="m", label='Simulated Annealing')
ax2.plot(iterations_range, mimic_convergence_time, 'o-', color="g", label='MIMIC')
ax2.legend(loc="best")

plt.show()
print("you are done!")
