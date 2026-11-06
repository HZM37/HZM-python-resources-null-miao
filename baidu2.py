import time
import os
import requests

#这里请输入自己的cookie
MY_COOKIE = "" 

if MY_COOKIE == "":
    print("⚠️ 检测到你还没有配置 Cookie！")
    print("👉 请用浏览器打开百度图片，按 F12 复制 Cookie，粘贴到代码第 5 行的 MY_COOKIE = "" 里面。")
    exit()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "Referer": "https://image.baidu.com/",
    "Cookie": MY_COOKIE
}
if not os.path.exists("tupian"):
    os.mkdir("tupian")
url="https://image.baidu.com/search/acjson"
user_query=input("请输入抓取内容：")
user_count=input("请输入抓取数量:")
need_count=int(user_count)
count=1
history_urls = set()

for page in range(50):
    print(f"\n--- 正在抓取第 {page + 1} 页 ---")

    params = {
        "tn": "resultjson_com",
        "word": user_query,
        "ie": "utf-8",
        "pn": str(page * 60),
        "rn": "60"
    }

    response = requests.get(url, headers=headers, params=params, timeout=10)

    if response.status_code == 200:
        data = response.json()
        mini = data["data"]

        if len(mini) == 0:
            print("百度已经被榨干了，没有更多图片啦！")
            break

        for item in mini:
            if isinstance(item, dict):
                wi = item.get("thumbURL") or item.get("middleURL")

                if wi and wi not in history_urls:
                    try:
                        img_resp = requests.get(wi, headers=headers, timeout=10)

                        if img_resp.status_code == 200:
                            with open(f"tupian/tupian_{count}.jpg", "wb") as f:
                                f.write(img_resp.content)

                            print(f"✅ 成功保存第 {count} 张！")

                            count += 1
                            history_urls.add(wi)

                            if count > need_count:
                                break

                    except Exception as e:
                        print(f"💥 某张报错跳过: {e}")

                    time.sleep(0.25)

    if count > need_count:
        print(f"\n🎉 任务完成！已经成功抓够了 {user_count} 张图！")
        break

    time.sleep(1)

print("程序结束，快去 tupian 文件夹验收吧！")
