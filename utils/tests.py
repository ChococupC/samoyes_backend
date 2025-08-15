c = [1,2,3]

def a(topic):
    topic.append(4)

def b(topic):
    topic.append(5)

b(c)
a(c)
print(c)