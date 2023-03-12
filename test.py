x = 45

# convert int to bytes
x = x.to_bytes((x.bit_length() + 7) // 8, byteorder='big')

# convert bytes to int
x = int.from_bytes(x, byteorder='big')

print(x)