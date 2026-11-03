import dis

# all opcodes, sorted by number
for num in range(256):
    name = dis.opname[num]
    if not name.startswith("<"):
        print(f"{num:3d}  {name}")
