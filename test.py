bb = "xxxxxxx"
bb = bb.encode("utf-8")

# convert bytes to binary
x = bin(int.from_bytes(bb, "big"))[2:]

print(f"x: {x}")
