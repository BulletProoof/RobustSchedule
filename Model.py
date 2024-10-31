import gurobipy as gp
from gurobipy import GRB, quicksum

class Model:
    def __init__(self, instance):
        self.instance = instance
        self.model = gp.Model("HazMat_Schedule")
        self.add_variables()
        self.add_constraints()
        self.set_objective()

    def add_variables(self):
        self.X = {}
        for i in self.instance.N:
            for j in self.instance.N:
                self.X[i, j] = self.model.addVar(vtype=GRB.BINARY, name=f"self.X{i}_{j}")
        
        self.y = {}
        for i in self.instance.N:
            for j in self.instance.N:
                for h in self.instance.H:
                    self.y[i, j, h] = self.model.addVar(vtype=GRB.BINARY, name=f"self.y{i}_{j}_{h}")

        self.x = {}
        for i in self.instance.N:
            for j in self.instance.N:
                for h in self.instance.H:
                    for k in self.instance.K:
                        self.x[i, j, h, k] = self.model.addVar(vtype=GRB.BINARY, name=f"self.x{i}_{j}_{h}_{k}")

        self.d = {}
        for i in self.instance.N:
            for j in self.instance.N:
                for h in self.instance.H:
                    for k in self.instance.K:
                        self.d[i, j, h, k] = self.model.addVar(vtype=GRB.CONTINUOUS, name=f"self.d{i}_{j}_{h}_{k}")

        self.f = {}
        for i in self.instance.N:
            for j in self.instance.N:
                for h in self.instance.H:
                    self.f[i, j, h] = self.model.addVar(vtype=GRB.CONTINUOUS, name=f"self.f{i}_{j}_{h}")
          
    
    def add_constraints(self):
        # 约束条件
        # 约束（1）：每个客户只能被访问一次
        for j in range(1, self.instance.N):
            self.model.addConstr(quicksum(self.X[i, j] for i in range(0, self.instance.N)) == 1,"c1:visit_once_in_[%self.d]" % j)
            self.model.addConstr(quicksum(self.X[j, i] for i in range(0, self.instance.N)) == 1,"c1:visit_once_out_[%self.d]" % j)

        # 约束（2）：车辆流量平衡约束-车辆从配送中心出发必须返回配送中心
        for j in range(0, self.instance.N):
            for h in range(0, self.H):
                self.model.addConstr(
                    quicksum(self.y[i, j, h] for i in range(self.instance.N)) - quicksum(self.y[j, i, h] for i in range(self.instance.N)) == 0,
                    "c2:flow_balance_return_depot_[%d_%self.d]" % (j, h)
                )

        # 约束（3）：车辆流量平衡约束-车辆只允许离开配送中心一次，且不能重复使用
        for h in range(0, self.instance.self.H):
            self.model.addConstr(
                quicksum(self.y[0, j, h] for j in range(self.instance.N)) <= 1,

                "c3:flow_balance_use_once_[%d_%self.d]" % (j, h)
            )

        # 约束（4）：距离约束
        # 当车辆h在时段k不通过路段(i,j)时，x[i,j,h,k]必须为0;
        # 当车辆h在时段k通过路段(i,j),在(i,j)上的通行距离小于等于路段(i,j)的距离D_ij
        for i in range(self.instance.N):
            for j in range(self.instance.N):
                for h in range(self.instance.self.H):
                    for k in range(self.instance.K):
                        self.model.addConstr(
                            self.d[i, j, h, k] <= self.instance.distance_matrix[i][j] * self.x[i, j, h, k],
                            "c4:distance_lower_constraint_[%d_%d_%d_%self.d]" % (i, j, h, k)
                        )

        # 约束（5）：距离约束
        # 保证通行路段和车辆通行距离一致
        for i in range(self.instance.N):
            for j in range(self.instance.N):
                self.model.addConstr(
                    quicksum(self.d[i, j, h, k] 
                            for h in range(self.instance.self.H) 
                            for k in range(self.instance.K)) == self.X[i, j] * self.instance.distance_matrix[i][j],
                            "c5:distance_equal_constraint_[%d_%self.d]"% (i, j)
                )

        # 约束（6）：时间窗约束
        # 当车辆h在时段k在路段(i,j)的行驶时间要小于k时段的间隔
        for k in range(self.instance.K):
            for h in range(self.instance.self.H):
                self.model.addConstr(
                    quicksum(self.d[i, j, h, k] / self.instance.velocity[i][j][k] 
                            for i in range(self.instance.N) 
                            for j in range(self.instance.N)) <= self.instance.e[k] - self.instance.b[k],
                    "c6:time_window_constraint_lower_interval_[%d_%self.d]" % (k, h)
                )

        # 约束（7）：时间窗约束
        # 最大离开节点i的时间，e_m是一个大数，这里要优化一下e_m
        e_m = 100
        for i in range(self.instance.N):
            for j in range(self.instance.N):
                for h in range(self.instance.self.H):
                    for k in range(self.instance.K):
                        self.model.addConstr(
                            self.instance.l[i] <= self.instance.e[k] - self.d[i, j, h, k] / self.instance.velocity[i][j][k] + e_m * (1 - self.x[i, j, h, k]), 
                            "c7:time_window_constraint_max_leave_time_[%d_%d_%d_%self.d]" % (i, j, h, k)
                        )

        # 约束（8）：时间窗约束
        # 最小到达节点i的时间
        for i in range(self.instance.N):
            for j in range(self.instance.N):
                for h in range(self.instance.self.H):
                    for k in range(self.instance.K):
                        self.model.addConstr(
                            self.instance.a[j] >= self.instance.b[k] + self.d[i, j, h, k] / self.instance.velocity[i][j][k] - e_m * (1 - self.x[i, j, h, k]),
                            "c8:time_window_constraint_min_arrival_time01_[%d_%d_%d_%self.d]" % (i, j, h, k)
                        )
                self.model.addConstr(
                    self.instance.a[j] >= self.instance.l[j] + quicksum(self.d[i, j, h, k] / self.instance.velocity[i][j][k] 
                                                                for h in range(self.instance.self.H) 
                                                                for k in range(self.instance.K))
                                                        - e_m * (1 - self.X[i,j]),
                    "c8:time_window_constraint_min_arrival_time02_[%d_%d_%d_%self.d]" % (i, j, h, k)
                )

        # 约束（9）：时间窗约束
        # 最小离开时间
        for i in range(1, self.instance.N):
            self.model.addConstr(
                self.instance.a[i] + self.instance.service_times[i] <= self.instance.l[i],
                "c9:time_window_constraint_min_leave_time_[%self.d]" % i
            )

        # 约束（10）：时间窗约束
        # 返回配送中心的时间
        self.model.addConstr(self.instance.a[0] <= e_m, "c10:return_depot_time")


        # 约束（11）：顾客需求约束
        # 满足顾客的需求且消除子回路
        for j in range(1, self.instance.N):
            self.model.addConstr(
                quicksum(self.f[i, j, h]for i in range(self.instance.N) for h in range(self.instance.self.H)) 
                - quicksum(self.f[j, i, h]for i in range(self.instance.N) for h in range(self.instance.self.H))
                == self.instance.demands[j],
                "c11:customer_demand_constraint_[%self.d]" % j
            )

        # 约束（12）：车辆容量约束
        # 车辆最大装载约束
        for h in range(self.instance.self.H):
            for i in range(self.instance.N):
                for j in range(self.instance.N):
                    self.model.addConstr(
                        self.f[i, j, h]  <= self.instance.vehicle_capas[h] * self.y[i, j, h],
                        "c12:vehicle_capacity_constraint_[%d_%self.d]" % (h, i)
                    )

        # 约束（13）：车辆行驶时间约束
        # 每个车辆在每段时间内只能行驶一次
        for h in range(self.instance.self.H):
            for k in range(self.instance.K):
                self.model.addConstr(
                    quicksum(self.x[i, j, k, h] for i in range(self.instance.N) for j in range(self.instance.N))
                    <= 1,
                    "c13:vehicle_time_constraint_[%d_%self.d]" % (h, k)
                )

        # 约束（14）：决策变量之间的关系
        for i in range(self.instance.N):
            for j in range(self.instance.N):
                self.model.addConstr(
                    quicksum(self.y[i, j, h] for h in range(self.instance.self.H)) 
                    == self.model.self.X[i, j],
                    "c14:decision_variable_relation_[%d_%self.d]" % (i, j)
                )

        # 约束（15）（16）车辆h通过路段(i,j)与车辆h在时段k通过路段(i,j)的关系
        for i in range(self.instance.N):
            for j in range(self.instance.N):
                for h in range(self.instance.self.H):
                    for k in range(self.instance.K):
                        self.model.addConstr(
                            self.y[i, j, h] >= self.x[i, j, k, h],
                            "c15:vehicle_task_constraint_[%d_%d_%d_%self.d]" % (i, j, h, k)
                        )
                    self.model.addConstr(
                        self.y[i, j, h] <= quicksum(self.x[i, j, k, h] for k in range(self.instance.K)),
                        "c16:vehicle_task_constraint_[%d_%d_%self.d]" % (i, j, h)
                    )

    def set_objective(self):
        # 目标函数：最小化运输风险和运输距离
        # 设置权重
        self.alpha = 1.0  # 风险的权重
        self.beta = 0.0   # 距离的权重

        # 计算总运输风险
        self.total_risk = quicksum(self.self.x[i, j, h, k] * self.instance.risk_matrix[i][j][k] 
                      for i in range(self.instance.N) 
                      for j in range(self.instance.N) 
                      for h in range(self.instance.self.H) 
                      for k in range(self.instance.K))
        
        # 计算总运输距离
        self.total_distance = quicksum(self.d[i, j, h, k]
                          for i in range(self.instance.N) 
                          for j in range(self.instance.N) 
                          for h in range(self.instance.self.H) 
                          for k in range(self.instance.K))

        self.model.setObjective(self.alpha * self.total_risk + self.beta * self.total_distance, GRB.MINIMIZE)

    
    def show_result(self):
        # 输出结果
        if self.model.status == GRB.OPTIMAL:
            for i in range(self.instance.N):
                for j in range(self.instance.N):
                    for h in range(self.instance.self.H):
                        for k in range(self.instance.K):
                            if self.x[i, j, k, h].x > 0.5:
                                print("车辆%d在时段%d从%d到%d, 行驶%f, 运输%d" % (h, k, i, j, self.d[i, j, k, h].x, self.f[i, j, h].x))
        elif self.model.status == GRB.TIME_LIMIT:
            print("时间限制:")
            for i in range(self.instance.N):
                for j in range(self.instance.N):
                    for h in range(self.instance.self.H):
                        for k in range(self.instance.K):
                            if self.x[i, j, k, h].x > 0.5:
                                print("车辆%d在时段%d从%d到%d, 行驶%f, 运输%d" % (h, k, i, j, self.d[i, j, k, h].x, self.f[i, j, h].x))
        else:
            print("未找到可行解")