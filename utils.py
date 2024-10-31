import pandas as pd
from Problem import *

def read_customers(file_path):
    df = pd.read_csv(file_path)
    customers = []
    for i in range(len(df)):
        id = int(df['CustomerID'][i])
        x, y = int(df["XCoord"][i]), int(df["YCoord"][i])
        d = int(df["Demand"][i])
        e, l = int(df["ReadyTime"][i]), int(df["DueTime"][i])
        s = int(df["ServiceTime"][i])
        customers.append(Customer(id, x, y, d, e, l, s))
    return customers

def read_vehicles(file_path):
    df = pd.read_csv(file_path)
    vehicles = []
    for i in range(len(df)):
        id = int(df['vehicle_id'][i])
        vehicle_type = int(df["vehicle_type"][i])
        capacity = int(df["capacity"][i])
        vehicles.append(Vehicle(id, vehicle_type, capacity))
    return vehicles

def read_periods(file_path):
    df = pd.read_csv(file_path)
    periods = []
    for i in range(len(df)):
        id = int(df['PeriodID'][i])
        start, end = int(df["Start"][i]), int(df["End"][i])
        periods.append([start, end])
    return periods

def read_distance_matrix(file_path):
    df = pd.read_csv(file_path, header=None)
    distance_matrix = [[0] * len(df) for _ in range(len(df))]
    
    for i in range(len(df)):
        for j in range(len(df)):
            distance_matrix[i][j] = df.iloc[i, j]
            
    return distance_matrix

def read_velocity(file_path):
    df = pd.read_csv(file_path)
    velocity = {}
    for i in range(len(df)):
        origin, destination, period = int(df["origin"][i]), int(df["destination"][i]), int(df["period"][i])
        velocity[origin, destination, period] = df["velocity"][i]
    return velocity

def read_risk_matrix(file_path):
    df = pd.read_csv(file_path)
    risk = {}
    for i in range(len(df)):
        origin, destination, period = int(df["origin"][i]), int(df["destination"][i]), int(df["period"][i])
        risk[origin, destination, period] = df["risk"][i]
    return risk

def read_parameters(file_path):
    df = pd.read_csv(file_path)
    parameters = {}
    for i in range(len(df)):
        parameters[df["parameter"][i]] = df["value"][i]
    return parameters

