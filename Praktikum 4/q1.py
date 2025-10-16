k1  = bytes.fromhex("3c3f0193af37d2ebbc50cc6b91d27cf61197")
k21 = bytes.fromhex("ff76edcad455b6881b92f726987cbf30c68c")  # KEY2 ^ KEY1
k23 = bytes.fromhex("611568312c102d4d921f26199d39fe973118")  # KEY2 ^ KEY3
k1234 = bytes.fromhex("91ec5a6fa8a12f908f161850c591459c3887") # KEY4 ^ KEY1 ^ KEY3 ^ KEY2
f45 = bytes.fromhex("0269dd12fe3435ea63f63aef17f8362cdba8")   # FLAG ^ KEY4 ^ KEY5

bxor = lambda a,b: bytes(x ^ y for x,y in zip(a,b))

k2 = bxor(k1, k21)                          # KEY2 = (KEY2 ^ KEY1) ^ KEY1
k3 = bxor(k2, k23)                          # KEY3 = (KEY2 ^ KEY3) ^ KEY2
k4 = bxor(k1234, bxor(k1, bxor(k3, k2)))    # KEY4 = (KEY4^KEY1^KEY3^KEY2) ^ KEY1 ^ KEY3 ^ KEY2
k5 = bxor(f45, k4)                        # FLAG ^ KEY5 = f45 ^ KEY4

# ---- crib method ----
prefix = b"cry{"
k5_first = bxor(k5[:len(prefix)], prefix)
k5_full = (k5_first * ((len(k5)//len(k5_first))+1))[:len(k5)]
flag = bxor(k5, k5_full)

print(flag.decode(errors="ignore"))