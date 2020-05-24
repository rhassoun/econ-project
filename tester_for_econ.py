import matplotlib.pyplot as plt
import numpy as np
import random
import math
from scipy.optimize import fsolve

class graph():
	def plotting():
		plt.xlabel('Quantity')
		plt.ylabel('Price')
		plt.xlim([0,50])
		plt.ylim([0,100])
		plt.grid()
		plt.legend()
		return
class market():
	def __init__(self):
		self.supply_slope = random.random()*random.randrange(0,10)
		self.supply_b = 25
		self.demand_slope = -random.random()*random.randrange(1,10)
		self.demand_b = 75
		self.eq_pts = list()
	# creates values needed for the randomly generated supply curve
	def supply_curve(self):
		x_supply = np.linspace(0,50,100)
		self.supply_slope = random.random()*random.randrange(0,10)
		y_supply = self.supply_slope*x_supply + self.supply_b
		return (x_supply, y_supply)
	# creates values needed for the randomly generated demand curve
	def demand_curve(self):
		x_demand = np.linspace(0,50,100)
		self.demand_slope = -random.random()*random.randrange(1,10)
		y_demand = self.demand_slope*x_demand + self.demand_b
		return (x_demand, y_demand)
	# finds the intersection of the two lines
	def equilibrium_point(m1, b1, m2, b2):
		# finds the x value of the intersection pt by setting the equations equal to each other and solving
		coefs = [m1-m2, b1-b2]
		x_int = np.roots(coefs)
		# finds the y value of intersection by using one of the line's slope and y-intercept
		y_int = m1*x_int+b1
		return (x_int,y_int)
	def original_eq(self):
		# creates the initial supply and demand curves
		plt.plot(np.linspace(0,50),self.supply_slope*np.linspace(0,50)+self.supply_b,'-r', label ='Supply')
		plt.plot(np.linspace(0,50), self.demand_slope*np.linspace(0,50)+self.demand_b, 'b', label = 'Demand')
		# checks that the equilibrium point is within the bounds of the chosen boundaries (50 X 100)
		while market.equilibrium_point(self.supply_slope, self.supply_b, self.demand_slope, self.demand_b)[0] >= 50 or market.equilibrium_point(self.supply_slope, self.supply_b, self.demand_slope, self.demand_b)[1] >= 100 or (-self.supply_slope/self.demand_slope*(40.005-self.demand_b)+40.005) < 0 or (market.equilibrium_point(self.supply_slope, self.supply_b, self.demand_slope, self.demand_b)[1] > 35 and market.equilibrium_point(self.supply_slope, self.supply_b, self.demand_slope, self.demand_b)[1] < 45) or (40.005-self.demand_b)/self.demand_slope > 50:
		# if not, clears the plot and creates new lines by calling the supply and demand functions again
			plt.clf()
			plt.plot(self.supply_curve()[0],self.supply_curve()[1],'-r', label ='Supply')
			plt.plot(self.demand_curve()[0], self.demand_curve()[1], 'b', label = 'Demand')
	def current_equilibrium(self):
		self.eq_pts.append(market.equilibrium_point(self.supply_slope, self.supply_b, self.demand_slope, self.demand_b))
		# plots the equilibrium point
		plt.scatter(self.eq_pts[-1][0], self.eq_pts[-1][1], color='g')
		plt.text(self.eq_pts[-1][0], self.eq_pts[-1][1], '(' + str(self.eq_pts[-1][0]) + ',' + str(self.eq_pts[-1][1]) + ')')
		# draws lines from the the equilibrium point to the x and y axes
		plt.vlines(x=self.eq_pts[-1][0], ymin = 0, ymax = self.eq_pts[-1][1], color='g', linestyle = '--')
		plt.hlines(y=self.eq_pts[-1][1], xmin = 0, xmax = self.eq_pts[-1][0], color='g', linestyle = '--')
	# default option for a graph
	def surplus(self):
		# plots consumer surplus
		plt.fill_between(np.linspace(0,50), self.demand_slope*np.linspace(0,50)+self.demand_b, self.eq_pts[-1][1], where= self.eq_pts[-1][1] < self.demand_slope*np.linspace(0,50)+self.demand_b, interpolate = True, facecolor='skyblue')
		# plots producer surplus
		plt.fill_between(np.linspace(0,50), self.supply_slope*np.linspace(0,50)+self.supply_b, self.eq_pts[-1][1], where= self.eq_pts[-1][1] > self.supply_slope*np.linspace(0,50)+self.supply_b, interpolate = True, facecolor='lightcoral')
		return
	def apply_shift(self,type_of_shift, shift):
		# plots initial curves
		self.original_eq()
		if type_of_shift == 'taxes':
			flip = random.randrange(0,2)
			# shifts the supply curve
			if flip == 0:
				self.supply_b += 10
				# plots the new equilibrium point	
				self.current_equilibrium()
				# plots new supply curve and horizontal/vertical lines from equilibrium points
				plt.plot(np.linspace(0,50), self.supply_slope*np.linspace(0,50)+self.supply_b,'m', label ='Supply After Taxes')
				plt.hlines(y=self.eq_pts[-1][1], xmin = 0, xmax = self.eq_pts[-1][0], color='g', linestyle = '--')
				plt.hlines(y=self.eq_pts[-1][1] - 10, xmin = 0, xmax = self.eq_pts[-1][0], color='g', linestyle = '--')
				plt.hlines(y=self.eq_pts[0][1], xmin=0, xmax = self.eq_pts[-1][0], color = 'g', linestyle='--')
				plt.vlines(x=self.eq_pts[-1][0], ymin= 0, ymax = self.eq_pts[-1][1], color = 'g', linestyle = '--')
				# shades in the deadweight loss
				plt.fill_between(np.linspace(self.eq_pts[-1][0],self.eq_pts[0][0]), self.demand_slope*np.linspace(self.eq_pts[-1][0],self.eq_pts[0][0])+self.demand_b, self.supply_slope*np.linspace(self.eq_pts[-1][0],self.eq_pts[0][0]) + self.supply_b - 10, where= self.demand_slope*np.linspace(self.eq_pts[-1][0],self.eq_pts[0][0])+self.demand_b > self.supply_slope*np.linspace(self.eq_pts[-1][0],self.eq_pts[0][0]) + self.supply_b - 10, interpolate = True, facecolor='springgreen')
				# shades in tax block
				plt.fill_between(np.linspace(0,self.eq_pts[-1][0]), self.eq_pts[-1][1] - 10, self.eq_pts[-1][1], facecolor='violet')
				# shades in consumer surplus
				plt.fill_between(np.linspace(0,50), self.demand_slope*np.linspace(0,50)+self.demand_b, self.eq_pts[-1][1], where= self.demand_slope*np.linspace(0,50)+self.demand_b > self.eq_pts[-1][1], interpolate = True, facecolor='skyblue')
				# shades in producer surplus
				plt.fill_between(np.linspace(0,50), self.supply_slope*np.linspace(0,50)+self.supply_b-10, self.eq_pts[-1][1] - 10, where= self.supply_slope*np.linspace(0,50)+self.supply_b -10 < self.eq_pts[-1][1] - 10, interpolate = True, facecolor='lightcoral')
			# shifts the demand curve
			else:
				self.demand_b -= 10
				# plots the new equilibrium point	
				self.current_equilibrium()
				# plots new demand curve and horizontal/vertical lines from equilibrium points
				plt.plot(np.linspace(0,50), self.demand_slope*np.linspace(0,50)+self.demand_b, 'm', label = 'Demand After Taxes')
				plt.hlines(y=self.eq_pts[-1][1], xmin = 0, xmax = self.eq_pts[-1][0], color='g', linestyle = '--')
				plt.hlines(y=self.eq_pts[-1][1] + 10, xmin = 0, xmax = self.eq_pts[-1][0], color='g', linestyle = '--')
				plt.hlines(y=self.eq_pts[0][1], xmin=0, xmax = self.eq_pts[-1][0], color = 'g', linestyle='--')
				plt.vlines(x=self.eq_pts[-1][0], ymin= 0, ymax = self.eq_pts[-1][1] + 10, color = 'g', linestyle = '--')
				# shades in the deadweight loss
				plt.fill_between(np.linspace(self.eq_pts[-1][0],self.eq_pts[0][0]), self.demand_slope*np.linspace(self.eq_pts[-1][0],self.eq_pts[0][0])+self.demand_b + 10, self.supply_slope*np.linspace(self.eq_pts[-1][0],self.eq_pts[0][0]) + self.supply_b, where= self.demand_slope*np.linspace(self.eq_pts[-1][0],self.eq_pts[0][0])+self.demand_b + 10> self.supply_slope*np.linspace(self.eq_pts[-1][0],self.eq_pts[0][0]) + self.supply_b, interpolate = True, facecolor='springgreen')
				# shades in tax block
				plt.fill_between(np.linspace(0,self.eq_pts[-1][0]), self.eq_pts[-1][1], self.eq_pts[-1][1] + 10, facecolor='violet')
				# shades in consumer surplus
				plt.fill_between(np.linspace(0,50), self.demand_slope*np.linspace(0,50)+self.demand_b + 10, self.eq_pts[-1][1] + 10, where= self.demand_slope*np.linspace(0,50)+self.demand_b + 10 > self.eq_pts[-1][1] + 10, interpolate = True, facecolor='skyblue')
				# shades in producer surplus
				plt.fill_between(np.linspace(0,50), self.supply_slope*np.linspace(0,50)+self.supply_b, self.eq_pts[-1][1], where= self.supply_slope*np.linspace(0,50)+self.supply_b < self.eq_pts[-1][1], interpolate = True, facecolor='lightcoral')
		elif type_of_shift == 'long run':
			self.supply_b = shift
			plt.plot(np.linspace(0,50), self.supply_slope*np.linspace(0,50)+self.supply_b, 'm', label = 'Long Run Supply Curve')
			self.current_equilibrium()
			self.surplus()
		elif type_of_shift == 'complements':
			self.demand_b += shift
			plt.plot(np.linspace(0,50), self.demand_slope*np.linspace(0,50)+self.demand_b,'m', label = 'New Demand Curve')
			self.current_equilibrium()
		return
	def price_regulation(self,type_of_reg):
		# generates a random price regulation
		gov_price = random.randrange(25,50)
		self.original_eq()
		# plots the price regulation
		plt.hlines(y=gov_price, xmin=0, xmax=50, color = 'gold')
		if type_of_reg == 'ceiling':
			# checks to see if the price set by gov't is a binding price ceiling (aka gov't price is lower than equilibrium price)
			if gov_price < self.eq_pts[0][1]:
				# plots the initial curves
				# finds the new quantity for equilibrium at the new price by setting the regulated price equal to the supply curve and solving
				coeff_supply = [self.supply_slope, self.supply_b - gov_price]
				new_eq_supply = np.roots(coeff_supply)
				plt.hlines(y=new_eq_supply[0]*self.demand_slope+self.demand_b, xmin=0, xmax=new_eq_supply[0],color = 'g', linestyle = '--')
				plt.vlines(x=new_eq_supply[0], ymin = 0, ymax = new_eq_supply[0]*self.demand_slope+self.demand_b, color = 'g', linestyle = '--')
				# plots the new equilibrium
				plt.scatter(new_eq_supply[0], gov_price, color='g')
				plt.text(new_eq_supply[0], gov_price, '(' + str(new_eq_supply[0]) + ',' + str(gov_price) + ')')
				# shades in the deadweight loss
				plt.fill_between(np.linspace(0,50), self.demand_slope*np.linspace(0,50)+self.demand_b, self.supply_slope*np.linspace(0,50)+self.supply_b, where = self.demand_slope*np.linspace(0,50) + self.demand_b > self.supply_slope*np.linspace(0,50) + self.supply_b, interpolate = True, facecolor = 'springgreen')
				#shades in the producer surplus
				plt.fill_between(np.linspace(0,50), gov_price, self.supply_slope*np.linspace(0,50)+self.supply_b, where= gov_price > self.supply_slope*np.linspace(0,50) + self.supply_b, interpolate = True, facecolor = 'lightcoral')
				# shades in the consumer surplus
				plt.fill_between(np.linspace(0,new_eq_supply[0]), gov_price, self.demand_slope*np.linspace(0,new_eq_supply[0])+self.demand_b, where= gov_price < self.demand_slope*np.linspace(0,new_eq_supply[0]) + self.demand_b, interpolate=True, facecolor = 'skyblue')
			# plots original graph but with the price regulation line on there (not binding price ceiling)
			else:
				self.current_equilibrium()
				self.surplus()
				return
		if type_of_reg == 'floor':
			if gov_price > self.eq_pts[0][1]:
				# plots the initial curves
				# finds the new quantity for equilibrium at the new price by setting the regulated price equal to the demand curve
				coeff_supply = [self.demand_slope, self.demand_b - gov_price]
				new_eq_supply = np.roots(coeff_supply)
				plt.hlines(y=new_eq_supply[0]*self.supply_slope+self.supply_b, xmin=0, xmax=new_eq_supply[0],color = 'g', linestyle = '--')
				plt.vlines(x=new_eq_supply[0], ymin = 0, ymax = new_eq_supply[0]*self.demand_slope+self.demand_b, color = 'g', linestyle = '--')
				# plots the new equilibrium
				plt.scatter(new_eq_supply[0], gov_price, color='g')
				plt.text(new_eq_supply[0], gov_price, '(' + str(new_eq_supply[0]) + ',' + str(gov_price) + ')')
				# shades in the deadweight loss
				plt.fill_between(np.linspace(0,50), self.demand_slope*np.linspace(0,50)+self.demand_b, self.supply_slope*np.linspace(0,50)+self.supply_b, where = self.demand_slope*np.linspace(0,50) + self.demand_b > self.supply_slope*np.linspace(0,50) + self.supply_b, interpolate = True, facecolor = 'springgreen')
				# shades in the consumer surplus
				plt.fill_between(np.linspace(0,50), gov_price, self.demand_slope*np.linspace(0,50)+self.demand_b, where= gov_price < self.demand_slope*np.linspace(0,50) + self.demand_b, interpolate = True, facecolor = 'skyblue')	
				# shades in the producer surplus
				plt.fill_between(np.linspace(0,new_eq_supply[0]), self.supply_slope*np.linspace(0,new_eq_supply[0]) + self.supply_b, gov_price, where= gov_price > self.supply_slope*np.linspace(0,new_eq_supply[0]) + self.supply_b, interpolate=True, facecolor = 'lightcoral')
			# plots original graph but with the price regulation line on there (not binding price floor)
			else:
				self.current_equilibrium()
				self.surplus()
				return
		return
class firm(market):
	def get_mr_curve(self):
		return self.eq_pts[-1][1]
	def plotting(self):
		plt.hlines(y=self.get_mr_curve(), xmin=0, xmax = 50, color = 'g', label = 'D=MR')
		plt.plot(np.linspace(9,50), 5*np.exp(-np.linspace(9,50)+10)+0.1*(np.linspace(9,50)-10)**2+15, '-r', label = 'MC')
		plt.plot(np.linspace(10,42),0.15*(np.linspace(10,42)-26)*(np.linspace(10,42)-26)+40, 'b', label='ATC')
	def profit(self):
		def findIntersection(z):
			x=z[0]
			y=z[1]
			f=np.zeros(2)
			f[0]= -y + 5*np.exp(-x+10)+0.1*(x-10)**2+15
			f[1] = -y +self.get_mr_curve()
			return f
		z = fsolve(findIntersection, [11, 1.0])
		# checks if we're at a loss
		if 0.15*(z[0]-26)**2+40 > 5*np.exp(-z[0]+10)+0.1*(z[0]-10)**2+15:
			plt.vlines(x = z[0], ymin=0, ymax = 0.15*(z[0]-26)**2+40, color = 'b', linestyle='--')
			plt.fill_between(np.linspace(0,z[0]), 0.15*(z[0]-26)**2+40, self.get_mr_curve(), interpolate = True, color = 'red')
		# at a profit
		else:
			plt.vlines(x = z[0], ymin=0, ymax = 5*np.exp(-z[0]+10)+0.1*(z[0]-10)**2+15, color = 'b', linestyle='--')
			plt.fill_between(np.linspace(0,z[0]), 0.15*(z[0]-26)**2+40, self.get_mr_curve(), interpolate = True, color = 'springgreen')
		plt.hlines(y = 0.15*(z[0]-26)**2+40, xmin = 0, xmax = z[0], color = 'b', linestyle = '--')
		self.plotting()
	#probably should check if we're already in
	def long_run(self):
		long_run_q = np.roots([self.demand_slope, self.demand_b-40.005])
		new_b = np.roots([1, self.supply_slope*long_run_q-40.005])
		self.apply_shift('long run', new_b[0])
		graph.plotting()
		plt.show()
		self.plotting()
	def disequilibrium(self):
		self.supply_slope = random.random()*random.randrange(1,5)
		self.demand_b = -(self.demand_slope*((40.005-self.supply_b)/self.supply_slope)-40.005)
		while (40.005-self.supply_b)/self.supply_slope > 50 or self.demand_b >90 or (-self.supply_slope/self.demand_slope*(40.005-(self.demand_b+10))+40.005) < 0:
			self.supply_slope = random.random()*random.randrange(1,5)
			self.demand_slope = -random.random()*random.randrange(1,5)
			self.demand_b = -(self.demand_slope*((40.005-self.supply_b)/self.supply_slope)-40.005)
		demand_b_temp = self.demand_b
		supply_b_temp = self.supply_b
		for counter in range(3):
			if counter == 0:
				self.current_equilibrium()
			plt.plot(np.linspace(0,50), self.supply_slope*np.linspace(0,50) + supply_b_temp, '-r', label = 'Long Run Supply')
			plt.plot(np.linspace(0,50), self.demand_slope*np.linspace(0,50) + demand_b_temp, 'b', label = 'Long Run Demand')
			if counter == 1:
				self.demand_b -= 10
				self.current_equilibrium()
				plt.plot(np.linspace(0,50), self.demand_slope*np.linspace(0,50) + self.demand_b, 'purple', label = 'New Demand')
			if counter == 2:
				plt.plot(np.linspace(0,50), self.demand_slope*np.linspace(0,50) + self.demand_b, 'purple', label = 'New Demand')
				self.supply_b = (-self.supply_slope/self.demand_slope*(40.005-self.demand_b)+40.005)
				self.current_equilibrium()
				plt.plot(np.linspace(0,50), self.supply_slope*np.linspace(0,50) + self.supply_b, 'lightcoral', label = 'New Long Run Supply')
			graph.plotting()
			plt.show()
			self.profit()
			graph.plotting()
			plt.show()
tester = firm()
tester.original_eq()
tester.current_equilibrium()
graph.plotting()
tester.surplus()
plt.show()
# tester.apply_shift('taxes', None)
# graph.plotting()
# plt.show()
# tester.price_regulation('floor')
# graph.plotting()
# plt.show()

tester.profit()
graph.plotting()
plt.show()
tester.long_run()
graph.plotting()
plt.show()
# tester.disequilibrium()
