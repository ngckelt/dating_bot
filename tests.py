

class Test:

    a = 1
    b = 2


t = Test()

t.__setattr__('c', 3)

print(t.c)

