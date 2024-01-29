import csv
import datetime
import math
import time


def average_age(users):
    total = 0
    for u in users:
        total += u[0]
    return total / len(users)


def average_payment_amount(users):
    amount = 0
    count = 0
    for payments in users:
        payments = payments[1:]
        count += len(payments)
        amount += sum(payments)
    return float(amount) / count / 100


def stddev_payment_amount(users):
    mean = average_payment_amount(users)
    squared_diffs = 0
    count = 0
    for payments in users:
        payments = payments[1:]
        count += len(payments)
        for p in payments:
            diff = p - mean * 100
            squared_diffs += diff * diff
    return math.sqrt(squared_diffs / count / 10000)


def load_data():
    users = {}
    ids = []
    with open('users.csv') as f:
        for line in csv.reader(f):
            uid, _, age, _, _ = line
            users[int(uid)] = [int(age)]
            ids.append(int(uid))
    with open('payments.csv') as f:
        for line in csv.reader(f):
            amount, _, uid = line
            users[int(uid)].append(int(amount))
    ids.sort()
    rtn = []
    for i in ids:
        rtn.append(users[i])
    return rtn


if __name__ == '__main__':
    t = time.perf_counter()
    users = load_data()
    print(f'Data loading: {time.perf_counter() - t:.3f}s')
    t = time.perf_counter()
    assert abs(average_age(users) - 59.626) < 0.01
    assert abs(stddev_payment_amount(users) - 288684.849) < 0.01
    assert abs(average_payment_amount(users) - 499850.559) < 0.01
    print(f'Computation {time.perf_counter() - t:.3f}s')
