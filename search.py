import os
import requests
import json
from concurrent.futures import ThreadPoolExecutor

# 不同搜索API的配置
SEARCH_APIS = {
    "google": {
        "url": "https://google.serper.dev/search",
        "headers": {
            "X-API-KEY": os.getenv("SERPER_API_KEY"),
            "Content-Type": "application/json"
        }
    },
    "duckduckgo": {
        "url": "https://api.duckduckgo.com",
        "params": {
            "q": "",
            "format": "json",
            "no_html": 1,
            "no_redirect": 1
        }
    }
}

def search_google(query):
    payload = json.dumps({"q": query})
    response = requests.post(
        SEARCH_APIS["google"]["url"],
        headers=SEARCH_APIS["google"]["headers"],
        data=payload
    )
    return [item.get("snippet", "") for item in response.json().get("organic", [])[:3]]

def search_duckduckgo(query):
    response = requests.get(
        SEARCH_APIS["duckduckgo"]["url"],
        params={"q": query, **SEARCH_APIS["duckduckgo"]["params"]}
    )
    return [result.get("Text", "") for result in response.json().get("RelatedTopics", [])[:3]]

def distributed_search(query):
    with ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(search_google, query): "google",
            executor.submit(search_duckduckgo, query): "duckduckgo"
        }
        
        results = {}
        for future in concurrent.futures.as_completed(futures):
            engine = futures[future]
            try:
                results[engine] = future.result()
            except Exception as e:
                print(f"{engine} search failed: {e}")
                
        return results

def meta_search(query):
    raw_results = distributed_search(query)
    
    # 合并和去重结果
    all_results = []
    seen = set()
    for engine in raw_results.values():
        for result in engine:
            if result and result not in seen:
                all_results.append(result)
                seen.add(result)
    
    # 结果排序策略
    return sorted(all_results, key=lambda x: len(x), reverse=True)[:5]