# для составления плана
history = []

# цена единицы оборудования
price = 2000

# объем производимой продукции в период [t, t+1], C - коэффициент
def amount(t, C):
    if t == -1:
        return -10000
    elif t < 8:
        return C*(2 - t/4)
    else:
        return -10000

# доход в период [t, t+1], p - стоимость продажи 1 ед. продукции, r - себестоимость 1 ед. продукции, C из amount
def profit(t, p, r, C):
    return (p-r) * amount(t, C)

c = 0
def counter1(x):
    global c
    if x == 1:
        c = c + 1
    else:
        c = 0
    return c

g = 0
def counter2(x):
    global g
    if x == 1:
        g = g + 1
    else:
        g = 0
    return g

# оптимальная функция дохода, t - время жизни, k - оставшаяся длительность процесса, p и r из profit, C из amount
def profit_optim_func(t, k, p, r, C, d):
    q = counter1(1)
    if q == 1:
        for i in range(0, k):
            history.insert(i, {})

    if k == 1:
        hold = profit(t, p, r, C)
        change = profit(0, p, r, C) * d - price
    else:
        hold = profit(t, p, r, C) + profit_optim_func(t+1, k-1, p, r, C, d)
        change = profit(0, p, r, C) * d + profit_optim_func(0, k-1, p, r, C, d) - price

    w = counter2(1)
    if hold >= change:
        if k == 1:
            history[history.__len__() - k].update({"hold" + str(w): hold})
        else:
            history[history.__len__() - k].update({"hold" + str(w) + " -> " +
                list(history[history.__len__() - k + 1].keys())[len(history[history.__len__() - k]) * 2]: hold})
        return hold
    else:
        if k == 1:
            history[history.__len__() - k].update({"change" + str(w): change})
        else:
            history[history.__len__() - k].update({"change" + str(w) + " -> " +
                list(history[history.__len__() - k + 1].keys())[len(history[history.__len__() - k]) * 2 + 1]: change})
        return change

# изменение плана в случае срыва
def big_changes(badmoment, old_t, k, old_p, old_r, old_C, old_d, new_p, new_r, new_C, new_d, cause, plan):
    rest_k = k - badmoment + 1
    rest_plan = []
    binplan = []
    income = 0
    for letter in plan:
        if letter == "o":
            binplan.append(0)
        if letter == "c":
            binplan.append(1)

    if cause == "equipment failure":
        t = -1
        income = profit_optim_func(t, rest_k, old_p, old_r, old_C, old_d)
        rest_plan = list(history[0].keys())[0].replace("0", "").replace("1", "").replace("2", "").replace("3", ""). \
            replace("4", "").replace("5", "").replace("6", "").replace("7", "").replace("8", "").replace("9", "")
    elif cause == "changing vars":
        t = 0
        for i in range(0, badmoment):
            if binplan[i] == 0:
                t = t + 1
            else:
                t = 0
        income = profit_optim_func(t, rest_k, new_p, new_r, new_C, new_d)
        rest_plan = list(history[0].keys())[0].replace("0", "").replace("1", "").replace("2", "").replace("3", "").\
            replace("4", "").replace("5", "").replace("6", "").replace("7", "").replace("8", "").replace("9", "")

    counter = 0
    start_plan = ""
    for letter in plan:
        start_plan = start_plan + letter
        if letter == ">":
            counter = counter + 1
        if counter == badmoment - 1:
            break

    history.clear()
    counter1(0)
    counter2(0)
    print(income + profit_optim_func(old_t, badmoment - 1, old_p, old_r, old_C, old_d))
    return start_plan + " " + rest_plan


t = 0  # время, которое отработало оборудование
k = 10  # время, которое еще нужно работать
p = 40  # цена продажи
r = 15  # себестоимость
C = 100  # коэффициент производства
d = 0.7  # коэффициент задержки при замене оборудования

print("Доход от производства составит:")
history.clear()
counter1(0)
counter2(0)
print(profit_optim_func(t, k, p, r, C, d))
print("План на " + str(k) + " лет для машины, которая работает уже " + str(t) + " лет:")
plan = list(history[0].keys())[0].replace("0", "").replace("1", "").replace("2", "").replace("3", "").replace("4", "").\
    replace("5", "").replace("6", "").replace("7", "").replace("8", "").replace("9", "")
print(plan)

#for i in range(0, k):
#    print(history[i])

print()

# новые значения
new_p = 45  # цена продажи
new_r = 25  # себестоимость
new_C = 100  # коэффициент производства
new_d = 0.6  # коэффициент задержки при замене оборудования

badmoment = 5  # год, в который произошли изменения
cause = "equipment failure"  # equipment failure | changing vars - причина, по которой произошли изменения
history.clear()
counter1(0)
counter2(0)
print("Обновленный план на " + str(k) + " лет с изменениями на " + str(badmoment) + " году по причине " + cause + ".")
print(big_changes(badmoment, t, k, p, r, C, d, new_p, new_r, new_C, new_d, cause, plan))


# для теста на java
print()
history.clear()
counter1(0)
counter2(0)
t = 0  # время, которое отработало оборудование
k = 3  # время, которое еще нужно работать
p = 40  # цена продажи
r = 15  # себестоимость
C = 100  # коэффициент производства
d = 0.7  # коэффициент задержки при замене оборудования
print(profit_optim_func(t, k, p, r, C, d))
plan = list(history[0].keys())[0].replace("0", "").replace("1", "").replace("2", "").replace("3", "").replace("4", "").\
    replace("5", "").replace("6", "").replace("7", "").replace("8", "").replace("9", "")
print(plan)
