try:
    5 + []
except Exception as exc:
    r = exc

print(r)
print(dir(r))
print(str(r))
print(r.message)
