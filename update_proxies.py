import requests
import threading

# --- CONFIGURATION ---
TEST_TIMEOUT = 5
SAVE_FILE = "proxies.txt"
PROXY_SOURCE = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"

working_proxies = []

def test_proxy(proxy):
    try:
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
        # Use a reliable site to test
        res = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=TEST_TIMEOUT)
        if res.status_code == 200:
            working_proxies.append(proxy)
    except:
        pass

def main():
    print("Fetching proxies...")
    try:
        raw_list = requests.get(PROXY_SOURCE).text.splitlines()
    except:
        return

    threads = []
    # Test top 100 proxies for speed
    for p in raw_list[:100]:
        t = threading.Thread(target=test_proxy, args=(p,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    if working_proxies:
        with open(SAVE_FILE, "w") as f:
            f.write("\n".join(working_proxies))
        print(f"Saved {len(working_proxies)} proxies.")

if __name__ == "__main__":
    main()
