from Problem import *
from utils import *
from Model import *
import time

customers = read_customers("./gurobi_data/customers.csv")
periods = read_periods("./gurobi_data/periods.csv")
vehicles = read_vehicles("./gurobi_data/vehicles.csv")
distance_matrix = read_distance_matrix("./gurobi_data/distances.csv")
velocity = read_velocity("./gurobi_data/velocity.csv")
risk_matrix = read_risk_matrix("./gurobi_data/risk.csv")
parameters = read_parameters("./gurobi_data/parameters.csv")

instance = Instance(customers, periods, vehicles, distance_matrix, velocity, risk_matrix, parameters)

model = Model(instance)
model.model.setParam('TimeLimit', 3600)
model.model.optimize()
model.show_result()

timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
model.model.write(f"./model/HazMat-{timestamp}.lp")

