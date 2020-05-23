import matplotlib.pyplot as plt
import numpy as np
import random
import math
from scipy.optimize import fsolve

class graph():
	# creates values needed for the randomly generated supply curve
	def supply_curve():
		global supply_slope
		x_supply = np.linspace(0,50,100)
		supply_slope = random.random()*random.randrange(0,10)
		global supply_b
		supply_b = 25
		y_supply = supply_slope*x_supply + supply_b
		return (x_supply, y_supply)
	# creates values needed for the randomly generated demand curve
	def demand_curve():
		global demand_slope
		x_demand = np.linspace(0,50,100)
		demand_slope = -random.random()*random.randrange(1,10)
		global demand_b
		demand_b = 75
		y_demand = demand_slope*x_demand + demand_b
		return (x_demand, y_demand)
	# finds the intersection of the two lines
	def equilibrium_point(m1, b1, m2, b2):
		# finds the x value of the intersection pt by setting the equations equal to each other and solving
		coefs = [m1-m2, b1-b2]
		x_int = np.roots(coefs)
		# finds the y value of intersection by using one of the line's slope and y-intercept
		y_int = m1*x_int+b1
		return (x_int,y_int)
	def original_eq():
		# creates the initial supply and demand curves
		plt.plot(np.linspace(0,50),supply_slope*np.linspace(0,50)+supply_b,'-r', label ='Supply')
		plt.plot(np.linspace(0,50), demand_slope*np.linspace(0,50)+demand_b, 'b', label = 'Demand')
		# checks that the equilibrium point is within the bounds of the chosen boundaries (50 X 100)
		while graph.equilibrium_point(supply_slope, supply_b, demand_slope, demand_b)[0] >= 50 or graph.equilibrium_point(supply_slope, supply_b, demand_slope, demand_b)[1] >= 100 or (-supply_slope/demand_slope*(40.005-demand_b)+40.005) < 0 or (graph.equilibrium_point(supply_slope, supply_b, demand_slope, demand_b)[1] > 35 and graph.equilibrium_point(supply_slope, supply_b, demand_slope, demand_b)[1] < 45) or (40.005-demand_b)/demand_slope > 50:
		# if not, clears the plot and creates new lines by calling the supply and demand functions again
			plt.clf()
			plt.plot(graph.supply_curve()[0],graph.supply_curve()[1],'-r', label ='Supply')
			plt.plot(graph.demand_curve()[0], graph.demand_curve()[1], 'b', label = 'Demand')
		# checks that there will be an intersection point
		while supply_slope == 0 and demand_slope==0:
		# if not, clears the plot and creates new lines by calling the supply and demand functions again
			plt.clf()
			plt.plot(graph.supply_curve()[0],graph.supply_curve()[1],'-r', label ='Supply')
			plt.plot(graph.demand_curve()[0], graph.demand_curve()[1], 'b', label = 'Demand')
		# saves the value of the initial equilbrium point for reference
		global original_pt
		original_pt = graph.equilibrium_point(supply_slope, supply_b, demand_slope, demand_b)
	def current_equilibrium():
		# plots the equilibrium point
		plt.scatter(graph.equilibrium_point(supply_slope, supply_b, demand_slope, demand_b)[0], graph.equilibrium_point(supply_slope, supply_b, demand_slope, demand_b)[1], color='g')
		plt.text(graph.equilibrium_point(supply_slope, supply_b, demand_slope, demand_b)[0], graph.equilibrium_point(supply_slope, supply_b, demand_slope, demand_b)[1], '(' + str(graph.equilibrium_point(supply_slope, supply_b, demand_slope, demand_b)[0]) + ',' + str(graph.equilibrium_point(supply_slope, supply_b, demand_slope, demand_b)[1]) + ')')
		# draws lines from the the equilibrium point to the x and y axes
		plt.vlines(x=graph.equilibrium_point(supply_slope, supply_b, demand_slope, demand_b)[0], ymin = 0, ymax = graph.equilibrium_point(supply_slope, supply_b, demand_slope, demand_b)[1], color='g', linestyle = '--')
		plt.hlines(y=graph.equilibrium_point(supply_slope, supply_b, demand_slope, demand_b)[1], xmin = 0, xmax = graph.equilibrium_point(supply_slope, supply_b, demand_slope, demand_b)[0], color='g', linestyle = '--')
	def plotting():
		plt.xlabel('Quantity')
		plt.ylabel('Price')
		plt.xlim([0,50])
		plt.ylim([0,100])
		plt.grid()
		plt.legend()
		return
	# default option for a graph
	def surplus():
		# plots consumer surplus
		plt.fill_between(np.linspace(0,50), demand_slope*np.linspace(0,50)+demand_b, graph.equilibrium_point(supply_slope, supply_b, demand_slope, demand_b)[1], where= graph.equilibrium_point(supply_slope, supply_b, demand_slope, demand_b)[1] < demand_slope*np.linspace(0,50)+demand_b, interpolate = True, facecolor='skyblue')
		# plots producer surplus
		plt.fill_between(np.linspace(0,50), supply_slope*np.linspace(0,50)+supply_b, graph.equilibrium_point(supply_slope, supply_b, demand_slope, demand_b)[1], where= graph.equilibrium_point(supply_slope, supply_b, demand_slope, demand_b)[1] > supply_slope*np.linspace(0,50)+supply_b, interpolate = True, facecolor='lightcoral')
		return
	def apply_shift(type_of_shift, shift):
		# plots initial curves
		graph.original_eq()
		global supply_b
		global demand_b
		if type_of_shift == 'taxes':
			flip = random.randrange(0,2)
			# shifts the supply curve
			if flip == 0:
				supply_b += 10
				# plots new supply curve and horizontal/vertical lines from equilibrium points
				plt.plot(np.linspace(0,50), supply_slope*np.linspace(0,50)+supply_b,'m', label ='Supply After Taxes')
				plt.hlines(y=original_pt[1], xmin = 0, xmax = graph.equilibrium_point(supply_slope, supply_b, demand_slope, demand_b)[0], color='g', linestyle = '--')
				plt.hlines(y=graph.equilibrium_point(supply_slope, supply_b, demand_slope, demand_b)[1] - 10, xmin = 0, xmax = graph.equilibrium_point(supply_slope, supply_b, demand_slope, demand_b)[0], color='g', linestyle = '--')
				# shades in the deadweight loss
				plt.fill_between(np.linspace(0,50), demand_slope*np.linspace(0,50)+demand_b, supply_slope*np.linspace(0,50) + supply_b - 10, where= demand_slope*np.linspace(0,50)+demand_b > supply_slope*np.linspace(0,50) + supply_b - 10, interpolate = True, facecolor='springgreen')
				# shades in tax block
				plt.fill_between(np.linspace(0,graph.equilibrium_point(supply_slope, supply_b, demand_slope, demand_b)[0]), graph.equilibrium_point(supply_slope, supply_b, demand_slope, demand_b)[1] - 10, graph.equilibrium_point(supply_slope, supply_b, demand_slope, demand_b)[1], facecolor='violet')
				# shades in consumer surplus
				plt.fill_between(np.linspace(0,50), demand_slope*np.linspace(0,50)+demand_b, graph.equilibrium_point(supply_slope, supply_b, demand_slope, demand_b)[1], where= demand_slope*np.linspace(0,50)+demand_b > graph.equilibrium_point(supply_slope, supply_b, demand_slope, demand_b)[1], interpolate = True, facecolor='skyblue')
				# shades in producer surplus
				plt.fill_between(np.linspace(0,50), supply_slope*np.linspace(0,50)+supply_b-10, graph.equilibrium_point(supply_slope, supply_b, demand_slope, demand_b)[1] - 10, where= supply_slope*np.linspace(0,50)+supply_b -10 < graph.equilibrium_point(supply_slope, supply_b, demand_slope, demand_b)[1] - 10, interpolate = True, facecolor='lightcoral')
			# shifts the demand curve
			else:
				demand_b -= 10
				# plots new demand curve and horizontal/vertical lines from equilibrium points
				plt.plot(np.linspace(0,50), demand_slope*np.linspace(0,50)+demand_b, 'm', label = 'Demand After Taxes')
				plt.hlines(y=original_pt[1], xmin = 0, xmax = graph.equilibrium_point(supply_slope, supply_b, demand_slope, demand_b)[0], color='g', linestyle = '--')
				plt.hlines(y=graph.equilibrium_point(supply_slope, supply_b, demand_slope, demand_b)[1] + 10, xmin = 0, xmax = graph.equilibrium_point(supply_slope, supply_b, demand_slope, demand_b)[0], color='g', linestyle = '--')
				# shades in the deadweight loss
				plt.fill_between(np.linspace(0,50), demand_slope*np.linspace(0,50)+demand_b + 10, supply_slope*np.linspace(0,50) + supply_b, where= demand_slope*np.linspace(0,50)+demand_b + 10> supply_slope*np.linspace(0,50) + supply_b, interpolate = True, facecolor='springgreen')
				# shades in tax block
				plt.fill_between(np.linspace(0,graph.equilibrium_point(supply_slope, supply_b, demand_slope, demand_b)[0]), graph.equilibrium_point(supply_slope, supply_b, demand_slope, demand_b)[1], graph.equilibrium_point(supply_slope, supply_b, demand_slope, demand_b)[1] + 10, facecolor='violet')
				# shades in consumer surplus
				plt.fill_between(np.linspace(0,50), demand_slope*np.linspace(0,50)+demand_b + 10, graph.equilibrium_point(supply_slope, supply_b, demand_slope, demand_b)[1] + 10, where= demand_slope*np.linspace(0,50)+demand_b + 10 > graph.equilibrium_point(supply_slope, supply_b, demand_slope, demand_b)[1] + 10, interpolate = True, facecolor='skyblue')
				# shades in producer surplus
				plt.fill_between(np.linspace(0,50), supply_slope*np.linspace(0,50)+supply_b, graph.equilibrium_point(supply_slope, supply_b, demand_slope, demand_b)[1], where= supply_slope*np.linspace(0,50)+supply_b < graph.equilibrium_point(supply_slope, supply_b, demand_slope, demand_b)[1], interpolate = True, facecolor='lightcoral')
			# plots the new equilibrium point	
			graph.current_equilibrium()
		elif type_of_shift == 'long run':
			supply_b = shift
			plt.plot(np.linspace(0,50), supply_slope*np.linspace(0,50)+supply_b, 'm', label = 'Long Run Supply Curve')
			graph.current_equilibrium()
			graph.surplus()
		elif type_of_shift == 'complements':
			demand_b += shift
			plt.plot(np.linspace(0,50), demand_slope*np.linspace(0,50)+demand_b,'m', label = 'New Demand Curve')
			graph.current_equilibrium()
		return
	def price_regulation(type_of_reg):
		# generates a random price regulation
		gov_price = random.randrange(30,70)
		graph.original_eq()
		# plots the price regulation
		plt.hlines(y=gov_price, xmin=0, xmax=50, color = 'gold')
		if type_of_reg == 'ceiling':
			# checks to see if the price set by gov't is a binding price ceiling (aka gov't price is lower than equilibrium price)
			if gov_price < original_pt[1]:
				# plots the initial curves
				# finds the new quantity for equilibrium at the new price by setting the regulated price equal to the supply curve and solving
				coeff_supply = [supply_slope, supply_b - gov_price]
				new_eq_supply = np.roots(coeff_supply)
				plt.hlines(y=new_eq_supply[0]*demand_slope+demand_b, xmin=0, xmax=new_eq_supply[0],color = 'g', linestyle = '--')
				plt.vlines(x=new_eq_supply[0], ymin = 0, ymax = new_eq_supply[0]*demand_slope+demand_b, color = 'g', linestyle = '--')
				# plots the new equilibrium
				plt.scatter(new_eq_supply[0], gov_price, color='g')
				plt.text(new_eq_supply[0], gov_price, '(' + str(new_eq_supply[0]) + ',' + str(gov_price) + ')')
				# shades in the deadweight loss
				plt.fill_between(np.linspace(0,50), demand_slope*np.linspace(0,50)+demand_b, supply_slope*np.linspace(0,50)+supply_b, where = demand_slope*np.linspace(0,50) + demand_b > supply_slope*np.linspace(0,50) + supply_b, interpolate = True, facecolor = 'springgreen')
				#shades in the producer surplus
				plt.fill_between(np.linspace(0,50), gov_price, supply_slope*np.linspace(0,50)+supply_b, where= gov_price > supply_slope*np.linspace(0,50) + supply_b, interpolate = True, facecolor = 'lightcoral')
				# shades in the consumer surplus
				plt.fill_between(np.linspace(0,new_eq_supply[0]), gov_price, demand_slope*np.linspace(0,new_eq_supply[0])+demand_b, where= gov_price < demand_slope*np.linspace(0,new_eq_supply[0]) + demand_b, interpolate=True, facecolor = 'skyblue')
			# plots original graph but with the price regulation line on there (not binding price ceiling)
			else:
				graph.current_equilibrium()
				graph.surplus()
				return
		if type_of_reg == 'floor':
			if gov_price > original_pt[1]:
				# plots the initial curves
				# finds the new quantity for equilibrium at the new price by setting the regulated price equal to the demand curve
				coeff_supply = [demand_slope, demand_b - gov_price]
				new_eq_supply = np.roots(coeff_supply)
				plt.hlines(y=new_eq_supply[0]*supply_slope+supply_b, xmin=0, xmax=new_eq_supply[0],color = 'g', linestyle = '--')
				plt.vlines(x=new_eq_supply[0], ymin = 0, ymax = new_eq_supply[0]*demand_slope+demand_b, color = 'g', linestyle = '--')
				# plots the new equilibrium
				plt.scatter(new_eq_supply[0], gov_price, color='g')
				plt.text(new_eq_supply[0], gov_price, '(' + str(new_eq_supply[0]) + ',' + str(gov_price) + ')')
				# shades in the deadweight loss
				plt.fill_between(np.linspace(0,50), demand_slope*np.linspace(0,50)+demand_b, supply_slope*np.linspace(0,50)+supply_b, where = demand_slope*np.linspace(0,50) + demand_b > supply_slope*np.linspace(0,50) + supply_b, interpolate = True, facecolor = 'springgreen')
				# shades in the consumer surplus
				plt.fill_between(np.linspace(0,50), gov_price, demand_slope*np.linspace(0,50)+demand_b, where= gov_price < demand_slope*np.linspace(0,50) + demand_b, interpolate = True, facecolor = 'skyblue')	
				# shades in the producer surplus
				plt.fill_between(np.linspace(0,new_eq_supply[0]), supply_slope*np.linspace(0,new_eq_supply[0]) + supply_b, gov_price, where= gov_price > supply_slope*np.linspace(0,new_eq_supply[0]) + supply_b, interpolate=True, facecolor = 'lightcoral')
			# plots original graph but with the price regulation line on there (not binding price floor)
			else:
				graph.current_equilibrium()
				graph.surplus()
				return
		return
class firm():
	def get_mr_curve():
		return graph.equilibrium_point(supply_slope,supply_b, demand_slope, demand_b)[1]
	def plotting():
		plt.hlines(y=firm.get_mr_curve(), xmin=0, xmax = 50, color = 'g', label = 'D=MR')
		plt.plot(np.linspace(9,50), 5*np.exp(-np.linspace(9,50)+10)+0.1*(np.linspace(9,50)-10)**2+15, '-r', label = 'MC')
		plt.plot(np.linspace(10,42),0.15*(np.linspace(10,42)-26)*(np.linspace(10,42)-26)+40, 'b', label='ATC')
	def profit():
		def findIntersection(z):
			x=z[0]
			y=z[1]
			f=np.zeros(2)
			f[0]= -y + 5*np.exp(-x+10)+0.1*(x-10)**2+15
			f[1] = -y +firm.get_mr_curve()
			return f
		z = fsolve(findIntersection, [11, 1.0])
		# checks if we're at a loss
		if 0.15*(z[0]-26)**2+40 > 5*np.exp(-z[0]+10)+0.1*(z[0]-10)**2+15:
			plt.vlines(x = z[0], ymin=0, ymax = 0.15*(z[0]-26)**2+40, color = 'b', linestyle='--')
			plt.fill_between(np.linspace(0,z[0]), 0.15*(z[0]-26)**2+40, firm.get_mr_curve(), interpolate = True, color = 'red')
		# at a profit
		else:
			plt.vlines(x = z[0], ymin=0, ymax = 5*np.exp(-z[0]+10)+0.1*(z[0]-10)**2+15, color = 'b', linestyle='--')
			plt.fill_between(np.linspace(0,z[0]), 0.15*(z[0]-26)**2+40, firm.get_mr_curve(), interpolate = True, color = 'springgreen')
		plt.hlines(y = 0.15*(z[0]-26)**2+40, xmin = 0, xmax = z[0], color = 'b', linestyle = '--')
		firm.plotting()
	#probably should check if we're already in
	def long_run():
		long_run_q = np.roots([demand_slope, demand_b-40.005])
		new_b = np.roots([1, supply_slope*long_run_q-40.005])
		graph.apply_shift('long run', new_b[0])
		graph.plotting()
		plt.show()
		firm.plotting()
	def disequilibrium():
		graph.apply_shift('complements', 15)
		graph.plotting()
		plt.show()
		firm.long_run()
		graph.plotting()
		plt.show()
graph.supply_curve()
graph.demand_curve()

graph.original_eq()
graph.current_equilibrium()
graph.plotting()
# graph.surplus()
plt.show()

# graph.price_regulation('floor')
# graph.plotting()
# plt.show()

# graph.apply_shift('taxes', None)
# graph.plotting()
# plt.show()

firm.plotting()
graph.plotting()
plt.show()

firm.profit()
graph.plotting()
plt.show()

firm.long_run()
graph.plotting()
plt.show()

firm.disequilibrium()
