from imports import *
# TODO: implement 2x = 2*x ???????


class LP:
	def __init__(self, minmax, function, constraints, **kwargs):
		dim = self.dim_of_str_eq(constraints)
		if dim <= 3:
			chars = sp.symbols("x, y, z")[:dim]
		else:
			chars = sp.symbols('x0:{}'.format(dim))
			
		constraints = self.programming_form(constraints)
		function = sp.sympify(function)
		
		self.A, self.b = sp.linear_eq_to_matrix(constraints, chars)
		self.C = np.array(sp.linear_eq_to_matrix([function], chars)[0]).astype(np.float64)
		
		if minmax == "max":
			self.C = self.C[0] * -1
		
		self.A = np.column_stack((np.array(self.A).astype(np.float64), np.eye(dim)))
		self.b = np.array(self.b).astype(np.float64)
		
		# self.base
		# self.nbase
		# self.cb
		# self.cn
		
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
			try:
				rhs = sp.sympify(equation[:k - bias])
				lhs = sp.sympify(equation[k + bias:])
			except sp.SympifyError:
				print("Try writing without implied multiplication, '2*x' instead of '2x'")
				raise
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
		

if __name__ == "__main__":
	lp = LP("max", "2*x+y", ["x-3*y<=5", "2*x-5*y>=10"])
	print(lp.A)
	print("b = ", lp.b)
	print("C =", lp.C)
