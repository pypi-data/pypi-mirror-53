from numpy import array, zeros, average, linspace
from scipy.interpolate import interp1d, UnivariateSpline
from numpy.random import uniform
import sys
from copy import deepcopy


class MultiPylates(object):

	def __init__(self):
		self._coefficients_matrix = []		
		self._boundaries = []
		self._dilfunctions = None
		self._Ys = None
		# self.reset_to_default()
		self._real_fitness_fun = None
		self._real_parallel_fitness_fun = None
		self._fitness_fun_name = ""
		self._good_to_go = False

	def set_search_space(self, ss):
		""" 
			Sets the boundaries of the original optimization problem.
		"""
		self._boundaries = ss


	def reset_to_default(self, use_spline=False):
		"""
			Resets the Dilation Functions: all parameters are reverted to the common semantics.
			Stated otherwise, the dilation functions do not apply any dilations to the parameters.
		"""
		base = array([[0,0], [0.5, 0.5], [1,1]])

		D = len(self._boundaries)
		# print (" * %d-dimensional search space detected" % D)

		self._coefficients_matrix = []
		self._Ys = []
		self._dilfunctions = []
		for _ in range(D):
			self._coefficients_matrix.append( deepcopy( base.T[0] ))
			self._Ys.append( deepcopy( base.T[1] ))

		for i in range(D):
			if use_spline:
				self._dilfunctions.append( UnivariateSpline(self._coefficients_matrix[i], self._Ys[i]) )
			else:
				self._dilfunctions.append( interp1d(self._coefficients_matrix[i], self._Ys[i], bounds_error=True, kind="linear" ))


	def specify_control_points(self, chi_M, use_spline=False):

		if use_spline:
			print (" * Interpolating dilation functions with splines")

		D = len(self._boundaries)

		self._dilfunctions = []

		for i in range(D):

			# step 0: extend coefficients with default points
			chi = [[0,0]]+chi_M[i]
			chi = chi+[[1,1]]
			chi = array(chi)

			self._coefficients_matrix[i] = chi.T[0]
			self._Ys[i] = chi.T[1]
			if use_spline:
				self._dilfunctions.append( UnivariateSpline(self._coefficients_matrix[i], self._Ys[i]) )
			else:
				self._dilfunctions.append( interp1d(self._coefficients_matrix[i], self._Ys[i], bounds_error=True, kind="linear") )

	def plot_function(self, n):
		"""
			Service method for plotting a DF.
		"""

		from matplotlib.pyplot import subplots, show
		import seaborn as sns

		X = self._coefficients_matrix[n]
		Y = self._Ys[n]
		N = len(self._Ys[n])
		fig, ax = subplots(1,2,figsize=(10,5))
		ax[0].scatter(self._coefficients_matrix[n], self._Ys[n], color="green", label="Dilated function control points")
		ax[1].scatter(self._coefficients_matrix[n], self._boundaries[n][0]+self._Ys[n]*(self._boundaries[n][1]-self._boundaries[n][0]), color="green", label="Dilated function control points")
		for x,y in zip(self._coefficients_matrix[n], self._Ys[n]): ax[0].text(x,y,str(x))
		
		ax[0].plot(X, self._dilfunctions[n](X), "-", color="lightgray", label="Dilated function")
		ax[1].plot(X, self._boundaries[n][0]+self._dilfunctions[n](X)*(self._boundaries[n][1]-self._boundaries[n][0]), "-", color="lightgray", label="Dilated function")
		
		for (x,y) in zip (X,Y):
			ax[0].plot([x,x],[0,y], "--", color="yellow")
		ax[0].set_xlim(0,1)
		ax[0].set_ylim(0,1)
		ax[0].set_xlabel("Actual parameter value")
		ax[1].set_xlabel("Actual parameter value")
		ax[0].set_ylabel("Dilated parameter value (par %d)" % n)
		ax[1].set_ylabel("Dilated parameter value (par %d) mapped in original space" % n)
		ax[0].legend(loc="upper left")
		fig.tight_layout()
		sns.despine()
		show()

	def dilate_vector(self, V):
		"""	
			Once a Dilation Function is configured, this method can be used to 
			modify a vector of parameters (i.e., a candidate solution) according to
			the distortion defined by the Dilation Functions.
		"""
		# dil_temp = array([self._dilfunction(x) for x in V])
		dil_temp = []

		for dil, x in zip(self._dilfunctions, V):
			dil_temp.append( dil(x) )
		N = len(dil_temp)
		res = zeros(N)
		for i in range(N):
			res[i] = self._boundaries[i][0]+dil_temp[i]*(self._boundaries[i][1]-self._boundaries[i][0])
		return res

	def set_real_fitness(self, fitness):
		"""
			This method binds an external fitness function to the Dilation Function object.
		"""
		self._real_fitness_fun = fitness
		try:
			self._fitness_fun_name = str(fitness.__name__)
		except:
			self._fitness_fun_name = "unnamed function"

	def evaluator(self, X, arguments=None):
		"""
			This method evaluates the external fitness function on the dilated 
			vector of parameters.
		"""
		dilated_vector = self.dilate_vector(X)
		if arguments is not None:
			fitness_value = self._real_fitness_fun(dilated_vector, kwargs)
		else:
			fitness_value = self._real_fitness_fun(dilated_vector)
		return fitness_value

	def average_of_sampling(self, samples=100, arguments=None):
		ret = []
		all_samples = [uniform(0,1,len(self._boundaries)) for _ in range(samples) ]
		if self._real_parallel_fitness_fun is not None:
			ret = self.parallel_evaluator(all_samples, arguments)
		else:
			for candidate in all_samples:
				evaluation = self.evaluator(candidate) 
				ret.append(evaluation)
		return average(ret)

#####################################                #####################################
##################################### PARALLEL STUFF #####################################
#####################################                #####################################

	def set_real_parallel_fitness(self, fitness):
		"""
			This method binds an external fitness function to the Dilation Function object.
			The function must be 'parallel', i.e., must accept a whole population and 
			is supposed to return all fitness values.
		"""
		self._real_parallel_fitness_fun = fitness
		self._fitness_fun_name = str(fitness.__name__)

	def parallel_evaluator(self, V_X, arguments):
		"""
			This method evaluates the external fitness function on the dilated 
			vector of parameters.
		"""
		dilated_vectors = [self.dilate_vector(x) for x in V_X]
		if arguments is not None:
			fitness_values = self._real_parallel_fitness_fun(dilated_vectors, arguments)
		else:
			fitness_values = self._real_parallel_fitness_fun(dilated_vectors)
		return fitness_values


	def sobol_testing(self, trials=100, samples_per_trial=30, arguments=None):
		"""
			Use quasi-random sequences to explore the search space, looking for 
			optimal dilations.
		"""
		D = len(self._boundaries)


		MPL = self
		MPL.reset_to_default()
		
		"""
		baseline = MPL.average_of_sampling(samples=10, arguments=arguments)
		print ( " * Baseline average fitness: %f" % baseline)
		""" 

		O = 1e-2
		minimum = sys.float_info.max
		best_df = None
		best_sample = None

		import sobol_seq
		sequence = sobol_seq.i4_sobol_generate(D, trials)
		for ntrial, sample in enumerate(sequence):
			#print (sample)
			putative = [ [[0.001, y-O], [0.999, y+O]] for y in sample] #[[y, 0.49], [y+.7, 0.51]]
			#print (putative)
			MPL.specify_control_points(putative)
			result = MPL.average_of_sampling(samples=samples_per_trial, arguments=arguments)
			print ( " * New fitness with putative DF (%d-th trial): %f" % (ntrial, result), end="")
			if minimum>result:
				minimum = result
				best_df = array(putative)
				best_sample = array(sample)
				print(" <<<")
			else:
				print ("")
		print ( " * Best DF for this function: ", best_df, minimum)

		from matplotlib.pyplot import scatter, show, plot

		scatter(sequence.T[0], sequence.T[1])
		plot(best_sample.T[0], best_sample.T[1], "o", color="red")
		show()
		
		exit()


	# trials:  dilation points to be tested
	# samples: how many individuals will be generated for each trial
	def linear_testing(self, trials=1000, samples=30, initial=0.1, final=0.9, 
		plotta=False, arguments=None):

		D = self

		print (" * Performing linear testing: %d trials, %d samples per trial" % (trials, samples))
		D.reset_to_default()
		baseline = D.average_of_sampling(samples=trials, arguments=arguments)	
		print (" * Baseline (i.e., random population without DF): %e" % baseline)

		best = None
		bestaverage = sys.float_info.max

		res = []
		for n,y in enumerate(linspace(initial, final, trials)):
			putative = [[0.001, y-1e-2], [0.999, y+1e-2]] #[[y, 0.49], [y+.7, 0.51]]
			D.specify_control_points(putative)
			result = D.average_of_sampling(samples=samples, arguments=arguments)
			print (" * Trial DF %d/%d: %f" % (n+1, trials, y))
			print ("   %s\t%e" %(putative, result)),
			if result<bestaverage:
				print (" >>> New optimal DF: %f" % (y))
				best = y
				bestaverage = result
			else:
				print
			res.append([y, result])
		if plotta:
			fig, ax = subplots(1,1,figsize=(10,10))
			res= array(res)
			yscale("symlog")
			axhline(baseline, linestyle="--", color="red", label="Baseline")
			plot(res.T[0], res.T[1], "o-", label="Trials")
			plot(best, bestaverage, "*", markersize=15, color="lime", label="Best guess")
			legend()
			title("%d trials - %d samples for trial" % (trials, samples	))
			xlabel("Center of dilation")
			ylabel("Average fitness")
			tight_layout()
			savefig("%s%d.pdf" % (D._fitness_fun_name, arguments['fun']))
			
		return [[0.01, best-1e-2], [0.99, best+1e-2]], bestaverage


def test (x):
	from numpy import prod
	return prod(x**2)


if __name__ == '__main__':
	
	MD = MultiPylates()
	MD.set_search_space([[-100, 100], [-100, 100]])
	MD.reset_to_default()
	MD.specify_control_points( [[[0, 0], [0.1, 0.9], [1, 1]], [[0,0], [0.5, 0.5], [1,1]]] )
	MD.set_real_fitness(test)
	MD.sobol_testing()