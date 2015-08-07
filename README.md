# GoMuT

Go-style multithreading for python.

```
c = chan()
c.put(1)
c.put(2)
c.close()

for elem in c:
  print(elem)
# 1
# 2

def slowly_square(output, x):
  time.sleep(1)
  output.put(x*x)
  
result = chan()
go(slowly_square, result, 12) # does not block
print(result.get()) # blocks
# 144

go(slowly_square, result, 13)
go(slowly_square, result, 14)
for r in result:
  print(r)
# takes one second, not two

ch1, ch2 = chan(), chan()
def waiter(ch, sec):
  time.sleep(sec)
  ch.put(sec)
go(waiter, ch1, 1)
go(waiter, ch2, 2)

for i in range(0, 2):
  select({
    ch1: lambda x: print(x),
    ch2: lambda x: print(x),
  })
# takes 3 seconds
```
