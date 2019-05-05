from one_task import hello

res = hello.delay()

print(res.ready())
print(res.result)
print(res.get())
