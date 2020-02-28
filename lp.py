from imports import *
import time


class LP:
	def __init__(self, minmax, function, constraints, **kwargs):
		dim = self.dim_of_str_eq(constraints)
		if dim <= 3:
			chars = sp.symbols("x, y, z")[:dim]
		else:
			chars = sp.symbols('x0:{}'.format(dim))
			
		constraints = self.programming_form(constraints)
		while True:
			try:
				function = sp.sympify(function)
				break
			except sp.SympifyError:
				self.implied_multiplication(function)
		
		self.A, self.b = sp.linear_eq_to_matrix(constraints, chars)
		self.C = np.array(sp.linear_eq_to_matrix([function], chars)[0]).astype(np.float64)
		
		if minmax == "max":
			self.C = self.C[0] * -1
		
		self.A = np.array(self.A).astype(np.float64)
		self.b = np.array(self.b).astype(np.float64).T
		
		# self.base
		# self.nbase
		# self.cb
		# self.cn
	
	def simplex_solver(self):
		res = linprog(self.C, A_ub=self.A, b_ub=self.b, bounds=(0, None))
		return res
	
	@staticmethod
	def programming_form(equations):
		p_form = []
		for equation in equations:
			# equation = equation.split()[0]
			bias = 0
			scalar = 1
			k = equation.index("=")
			if equation[k-1] == "<" or equation[k-1] == ">":
				bias = 1
				if equation[k] == ">":
					scalar = -1
			rhs = equation[:k - bias]
			lhs = equation[k + bias:]
			while True:
				try:
					rhs = sp.sympify(rhs)
					lhs = sp.sympify(lhs)
					break
				except sp.SympifyError:
					rhs = LP.implied_multiplication(rhs)
					bias += 1
			p_form.append((rhs - lhs) * scalar)
		return p_form
	
	@staticmethod
	def dim_of_str_eq(equations):
		dim = [1 for i in range(len(equations))]
		for equation, j in zip(equations, range(len(equations))):
			for i in range(len(equation)):
				if equation[i] in ["+", "-"]:
					dim[j] += 1
		return max(dim)
	
	@staticmethod
	def implied_multiplication(equation):
		for i in range(1, len(equation)):
			if equation[i] in string.ascii_letters and equation[i - 1] != "*":
				equation = equation[:i] + "*" + equation[i:]
		return equation
	
	
class KleeMinty:
	def __init__(self, n, minmax="max", **kwargs):
		self.minmax = minmax
		self.C = self.get_function_km(n)
		self.A, self.b = self.get_constraints_km(n)
	
	@staticmethod
	def get_function_km(n):
		function = [0 for i in range(n)]
		for j in range(1, n+1):
			function[j-1] -= 10**(n-j)
		return np.array(function)
	
	@staticmethod
	def get_constraints_km(n):
		constraints = [[0 for j in range(n)] for i in range(n)]
		b = []
		for i in range(1, n+1):     # i for 1..n
			# calculate each constraints now
			for j in range(1, i):   # j for 1..i-1
				constraints[i-1][j-1] = 2 * (constraints[i-1][j-1] + 10**(i-j))
			constraints[i-1][i-1] += 1
			b.append(100**(i-1))
		return np.array(constraints), np.array(b)
	
	def pdata(self):
		return self.A, self.b, self.C
	
	def solve(self):
		return LP.simplex_solver(self)
	

if __name__ == "__main__":
	print(KleeMinty(3).pdata())
	start_time = time.time()
	res = KleeMinty(3).solve()
	print("--- %s seconds ---" % (time.time() - start_time))
	print(res)
	print('Optimal value:', res.fun, '\nX:', res.x)
	'''
	start_time = time.time()
	lp = LP("max", "x+y", ["x+2*y<=2", "3*x+y<=3/2"])
	print("--- %s seconds ---" % (time.time() - start_time))
	res = lp.simplex_solver()
	print('Optimal value:', res.fun, '\nX:', res.x)
	'''
