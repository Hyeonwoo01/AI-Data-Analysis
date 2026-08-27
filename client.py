import time
import requests
import pandas as pd
from multiprocessing import Pool as ProcessPool
from multiprocessing.dummy import Pool as ThreadPool

BASE = "http://127.0.0.1:5000/item/{}"
URLS = [BASE.format(i) for i in range(1, 61)]      #

def fetch(url):
    r = requests.get(url, timeout=10)
    return r.json()["id"]

def main():
    rows = []

    st = time.time()
    for u in URLS:
        fetch(u)
    sec = round(time.time() - st, 2)
    rows.append({"방식": "순차", "워커": 1, "초": sec})
    print(f"순차            {sec:6.2f}초")

    for n in (1, 3, 5, 10):
        st = time.time()
        with ThreadPool(n) as pool:
            pool.map(fetch, URLS)
        sec = round(time.time() - st, 2)
        rows.append({"방식": "스레드", "워커": n, "초": sec})
        print(f"스레드  워커 {n:2d}  {sec:6.2f}초")

    for n in (1, 3, 5, 10):
        st = time.time()
        with ProcessPool(n) as pool:
            pool.map(fetch, URLS)
        sec = round(time.time() - st, 2)
        rows.append({"방식": "프로세스", "워커": n, "초": sec})
        print(f"프로세스 워커 {n:2d}  {sec:6.2f}초")

    df = pd.DataFrame(rows)
    df.to_csv("bench.csv", index=False, encoding="utf-8-sig")
    
    print("\n=== 측정 결과 DataFrame ===")
    print(df)

if __name__ == "__main__":
    main()


'''
이번 테스트처럼 응답 대기 시간이 긴 I/O 바운드 작업에서는 스레드 방식이 네트워크 대기 중 GIL 해제 효과를 받아 빠르고 효율적으로 작동합니다. 
반면 프로세스 방식은 독립된 메모리를 할당하고 데이터를 직렬화하여 복사하는 등 풀 생성 비용이 크기 때문에, 
단순 대기 작업에서는 오히려 비효율적입니다.
'''