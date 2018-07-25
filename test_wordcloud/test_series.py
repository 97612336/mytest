import pandas as pd

list1 = [1, 2, 3, 4, 5, 6, "123"]

s1 = pd.Series(list1)
print(s1)
print(type(s1))

d1 = pd.DataFrame(list1)
print(d1)
print(type(d1))

dict1 = {"1": 123, "2": 123, "3": 123}

s2 = pd.Series(dict1)
print(s2)
print(type(s2))

