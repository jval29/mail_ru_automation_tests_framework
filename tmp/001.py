
dic = {1: "a", 2: "b", 3: "c", 4: "d", 5: "e", 6: 6}

for _ in dic.items():
    print(_)

a1 = str(dic)
print(a1)

print(type(eval(a1)))
