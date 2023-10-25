"""
Script to generate data for Tom is Tipsy question (LIFE113.1)
"""

import numpy as np
import matplotlib.pyplot as plt
from random import random
import os

def generate_data(fname, seed=0):
    """
    Generate a data set of time from midnight (hrs) and Blood Alcohol Content (BAC % mg).
    Relationship betwen BAC and time is linear.
    Need at least 10 data points between 0 and 5 hours.
    BAC should drop below 80 % mg after approx 12 hrs (+/- 2 hrs).
    """

    # Set random seed
    np.random.seed(seed)

    # Generate time data

    time = np.arange(0, 5.5, 0.5)

    # Generate BAC data
    BAC = np.zeros(len(time))
    BAC[0] = 140 + (random() - 0.5)*10
    for i in range(1, len(time)):
        BAC[i] = BAC[i-1] - 2

    # Add noise to BAC data
    BAC_noise = np.zeros(len(time))
    for i in range(len(time)):

        BAC_noise[i] = BAC[i] + (random() - 0.5)*3

    # Format BAC_noise data to 4 significant figures
    BAC_noise = np.around(BAC_noise, decimals=2)

    # Save data to file
    np.savetxt(fname, np.c_[time, BAC_noise], delimiter=',', header='Time (hrs), BAC (% mg)')

def solve_problem(fname):
    """
    Read data from file and solve problem.
    Fit a linear model to the data (y=mx+c)
    Use the model to calculate the exact time at which BAC = 80 % mg.
    Return answer in hours and minutes
    """
    
    # Read data from file
    data = np.loadtxt(fname, delimiter=',', skiprows=1)

    # Fit linear model to data
    m, c = np.polyfit(data[:,0], data[:,1], 1)

    # Calculate time at which BAC = 80 % mg
    time = (80 - c)/m

    # Convert time to hours and minutes
    hours = int(time)
    minutes = int((time - hours)*60)

    return time, hours, minutes

def save_list_of_dict(fname, dict):
    """
    Save a list of dictionaries to a csv file. Each key should be a column.
    """
    
    # Get all keys from dictionaries
    keys = dict[0].keys()

    # Open file for writing
    f = open(fname, 'w')

    # Write header
    header = ','.join(keys) + '\n'
    f.write(header)

    # Write data
    for d in dict:
        line = ','.join([str(d[k]) for k in keys]) + '\n'
        f.write(line)

    # Close file
    f.close()
    

if __name__ == '__main__':
    # Get all filenames from data directory
    filenames = os.listdir('data') 

    # Use solve_problem on each file and save results to a list of dictionaries
    results = []
    for fname in filenames:
        time, hours, minutes = solve_problem('data/'+fname)
        results.append({'filename':fname, 'decimal':time, 'hours':hours, 'minutes':minutes})

    # Save results to file
    save_list_of_dict('results.csv', results)
        



    