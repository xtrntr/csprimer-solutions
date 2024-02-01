import csv
import datetime
import math
import time
import functools


def average_age(payload):
    total = 0
    ages, _ = payload
    return sum(ages) / len(ages)


def average_payment_amount(payload):
    _, payments = payload
    return sum(payments) / len(payments)


def stddev_payment_amount(payload):
    ages, payments = payload
    mean = average_payment_amount(payload)
    squared_diffs = 0
    count = 0
    for p in payments:
        diff = p - mean
        squared_diffs += diff * diff
    return math.sqrt(squared_diffs / len(payments))


def load_data():
    ages = []
    payments = []
    with open('users.csv') as f:
        for line in csv.reader(f):
            uid, _, age, _, _ = line
            ages.append(int(age))
    with open('payments.csv') as f:
        for line in csv.reader(f):
            amount, _, uid = line
            payments.append(float(amount) / 100)
    return (ages, payments)


if __name__ == '__main__':
    t = time.perf_counter()
    payload = load_data()
    print(f'Data loading: {time.perf_counter() - t:.3f}s')
    t = time.perf_counter()
    assert abs(average_age(payload) - 59.626) < 0.01
    assert abs(stddev_payment_amount(payload) - 288684.849) < 0.01
    assert abs(average_payment_amount(payload) - 499850.559) < 0.01
    print(f'Computation {time.perf_counter() - t:.3f}s')
