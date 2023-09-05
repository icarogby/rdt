def intToByteConverter(n):
    return bin(n)[2:].zfill(8)

tes = b"Hello"
tes += tes
print(tes)
print(type(tes))
for i in tes:
    print(i)