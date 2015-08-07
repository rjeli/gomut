# GoMuT

Go-style multithreading for python.

```
c = chan()
c.put(1)
c.put(2)
c.close()

for elem in c:
  print(str(elem))
  
# prints:
# 1
# 2
```
