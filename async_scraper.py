import asyncio
import httpx
import time
from bs4 import BeautifulSoup

async def fetch(client, url, sem):
    async with sem: 
        print('요청 시작', url) 
        
        r = await client.get(url) 
        await asyncio.sleep(0.7)  
        r.raise_for_status()      
        
        soup = BeautifulSoup(r.text, 'html.parser')
        quote = soup.select_one("span.text")
        text = quote.text if quote else ""
        
        return (url, text)

async def main():
    urls = [f"https://quotes.toscrape.com/page/{i}/" for i in range(1, 11)]
    
    limits = httpx.Limits(max_connections=3)
    sem = asyncio.Semaphore(3)
    
    st = time.time()
    
    async with httpx.AsyncClient(limits=limits, timeout=10) as client: 
        tasks = [fetch(client, url, sem) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
    print('\n총 소요시간: %.2f초'%(time.time() - st)) 
    
    print('='*50)
    for result in results:
        if type(result) == tuple:
            url, text = result
            print(f"성공: [{url}] {text[:15]}...")
        else:
            print(f"오류 발생: {result}")

if __name__ == '__main__':
    asyncio.run(main())


'''
요청 시작 https://quotes.toscrape.com/page/1/
요청 시작 https://quotes.toscrape.com/page/2/
요청 시작 https://quotes.toscrape.com/page/3/
요청 시작 https://quotes.toscrape.com/page/4/
요청 시작 https://quotes.toscrape.com/page/5/
요청 시작 https://quotes.toscrape.com/page/6/
요청 시작 https://quotes.toscrape.com/page/7/
요청 시작 https://quotes.toscrape.com/page/8/
요청 시작 https://quotes.toscrape.com/page/9/
요청 시작 https://quotes.toscrape.com/page/10/

총 소요시간: 6.71초
==================================================
성공: [https://quotes.toscrape.com/page/1/] “The world as w...
성공: [https://quotes.toscrape.com/page/2/] “This life is w...
성공: [https://quotes.toscrape.com/page/3/] “I love you wit...
성공: [https://quotes.toscrape.com/page/4/] “The more that ...
성공: [https://quotes.toscrape.com/page/5/] “A reader lives...
성공: [https://quotes.toscrape.com/page/6/] “There is nothi...
성공: [https://quotes.toscrape.com/page/7/] “That's the pro...
성공: [https://quotes.toscrape.com/page/8/] “If I had a flo...
성공: [https://quotes.toscrape.com/page/9/] “Anyone who has...
성공: [https://quotes.toscrape.com/page/10/] “The truth." Du...
'''