from numpy import array, zeros, average, linspace
from scipy.interpolate import interp1d, UnivariateSpline
from numpy.random import uniform
import sys

class Pylates(object):

	def __init__(self):
		self._coefficients = []		# linear default
		self._boundaries = []
		self._dilfunction = None
		self._Y = None
		self.reset_to_default()
		self._real_fitness_fun = None
		self._real_parallel_fitness_fun = None
		self._fitness_fun_name = ""


	def reset_to_default(self, use_spline=False):
		"""
			Resets the Dilation Function: the parameters are reverted to the normal semantics.
			Stated otherwise, the Dilator does not apply any dilation to the values.
		"""
		base = array([[0,0], [0.5, 0.5], [1,1]])
		self._coefficients = base.T[0]
		self._Y = base.T[1]
		if use_spline:
			self._dilfunction = UnivariateSpline(self._coefficients, self._Y)	
		else:
			self._dilfunction = interp1d(self._coefficients, self._Y, bounds_error=True, kind="linear")	

	def set_search_space(self, ss):
		self._boundaries = ss

	def specify_control_points(self, chi, use_spline=False):
		
		# step 0: extend coefficients with default points
		chi = [[0,0]]+chi
		chi = chi+[[1,1]]
		chi = array(chi)

		self._coefficients = chi.T[0]
		self._Y = chi.T[1]
		if use_spline:
			self._dilfunction = UnivariateSpline(self._coefficients, self._Y)	
		else:
			self._dilfunction = interp1d(self._coefficients, self._Y, bounds_error=True, kind="linear")	

	def plot_function(self):
		"""
			Service method for plotting the DF.
		"""
		X = self._coefficients
		Y = self._Y
		N = len(self._Y)
		fig, ax = subplots(1,2,figsize=(10,5))
		ax[0].scatter(self._coefficients, self._Y, color="green", label="Dilated function control points")
		ax[1].scatter(self._coefficients, self._boundaries[0][0]+self._Y*(self._boundaries[0][1]-self._boundaries[0][0]), color="green", label="Dilated function control points")
		for x,y in zip(self._coefficients, self._Y): ax[0].text(x,y,str(x))
		
		ax[0].plot(X, self._dilfunction(X), "-", color="lightgray", label="Dilated function")
		ax[1].plot(X, self._boundaries[0][0]+self._dilfunction(X)*(self._boundaries[0][1]-self._boundaries[0][0]), "-", color="lightgray", label="Dilated function")
		
		for (x,y) in zip (X,Y):
			ax[0].plot([x,x],[0,y], "--", color="yellow")
		ax[0].set_xlim(0,1)
		ax[0].set_ylim(0,1)
		ax[0].set_xlabel("Actual parameter value")
		ax[1].set_xlabel("Actual parameter value")
		ax[0].set_ylabel("Dilated parameter value (par 1)")
		ax[1].set_ylabel("Dilated parameter value (par 1) mapped in original space")
		ax[0].legend(loc="upper left")
		fig.tight_layout()
		sns.despine()
		show()

	def dilate_vector(self, V):
		"""	
			Once a Dilation Function is configured, this method can be used to 
			modify a vector of parameters (i.e., a candidate solution) according to
			the distortion defined by the Dilation Function itself.
		"""
		dil_temp = array([self._dilfunction(x) for x in V])
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
				evaluation = self._real_fitness_fun(candidate) 
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


	# trials:  dilation points to be tested
	# samples: how many individuals will be generated for each trial
	def linear_testing(self, trials=29, samples=100, initial=0.1, final=0.9, 
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
