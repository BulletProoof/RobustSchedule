class Customer:
    def __init__(self, customer_id, x_coor, y_coor, demand, ready_time, due_time, service_time):
        self.id = customer_id
        self.x_coor = x_coor
        self.y_coor = y_coor
        self.demand = demand
        self.ready_time = ready_time
        self.due_time = due_time
        self.service_time = service_time

class Vehicle:
    def __init__(self, vehicle_id,vehicle_type, capacity):
        self.id = vehicle_id
        self.vehicle_type = vehicle_type
        self.capacity = capacity

class Period:
    def __init__(self, period_id, begin_time, end_time):
        self.id = period_id
        self.begin_time = begin_time
        self.end_time = end_time
  
class Instance:
    def __init__(self, customers, periods, vehicles, distance_matrix, velocity, risk_matrix, parameters):
        self.N = len(customers) # 顾客数量，包括仓库0
        self.q = [] # 顾客需求
        self.service_times = [] # 服务时间
        self.customers_coor = [] # 顾客坐标
        self.distance_matrix = distance_matrix # 距离矩阵

        self.velocity = velocity # 时变速度
        self.risk_matrix = risk_matrix # 时变风险矩阵

        self.K = len(periods) # 时间段数量
        self.b = [period.begin_time for period in periods] # 时间段起始时间
        self.e = [period.end_time for period in periods] # 时间段结束时间

        self.H = len(vehicles) # 车辆数量
        self.L = [vehicle.capacity for vehicle in vehicles] # 车辆容量

        for customers in customers:
            self.q.append(customers.demand)
            self.service_times.append(customers.service_time)
            self.customers_coor.append([customers.x_coor, customers.y_coor])
        
        for vehicles in vehicles:
            self.L.append(vehicles.capacity)

        for periods in periods:
            self.b.append(periods.begin_time)
            self.e.append(periods.end_time)
            
        self.parameters = parameters
        self.M = 100 # 一个很大的数，用于约束


    