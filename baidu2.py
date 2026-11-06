import time
import os
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "Referer": "https://image.baidu.com/",
    "Cookie":"BIDUPSID=1D8D367F790DEECC8F2D9EF348C79C8B; PSTM=1793477448; BAIDUID=1D8D367F790DEECC07F0DBE387C987B0:FG=1; BAIDUID_BFESS=1D8D367F790DEECC07F0DBE387C987B0:FG=1; ZFY=rh5swIU71jmtnEjlYWLFzkwyWVxwC6bkmbkgH7el45A:C; BA_HECTOR=85al2k2424al0520a18h0525ak858k1lemb8d29; BDRCVFR[I1GM4qgEDat]=-_EV5wtlMr0mh-8uz4WUvY; H_PS_PSSID=63148_74781_74967_75971_76046_76062_76115_76205_76233_76333_76340_76395_76432_76531_76510_76409_76557_76552_76469_76461_76566_76574_76569_76611_76614_76618_76625_76608_76607_76604_76598_76630_76380_76724_76726_76763; H_WISE_SIDS=74781_74967_76046_76062_76115_76205_76233_76395_76432_76531_76510_76409_76557_76552_76469_76461_76566_76574_76569_76611_76614_76618_76625_76608_76607_76604_76630_76380_76763; ab_sr=1.0.1_NzZlYzg5Yjk3NjYyNmM3YTEyMGI3NTQ1MTA2MjVlNjQ5MDhkMjhlNGFmZmYwYmY3Mzc0ZTE5YzhkNjNkY2JmNzRiZDAzNmYxMmI2YTM5MjE3YmVhN2YwZWQ5NmMxNzk2OTFmYjFiODllZGVkZjUxYjc0NDFjYWUxNmI5NDUxNTBlNTRjMmYyNjE5YzIwOGEyMDdiN2M1YTNiMDI1NDdlZg=="
}
if not os.path.exists("tupian"):
    os.mkdir("tupian")
url="https://image.baidu.com/search/acjson"
user_query=input("请输入抓取内容：")
user_count=input("请输入抓取数量:")
need_count=int(user_count)
count=1
history_urls = set()

# 4. 外层循环：翻页
for page in range(50):
    print(f"\n--- 正在抓取第 {page + 1} 页 ---")

    # 动态计算 pn (偏移量)
    params = {
        "tn": "resultjson_com",
        "word": user_query,
        "ie": "utf-8",
        "pn": str(page * 60),
        "rn": "60"
    }

    # 发请求拿数据
    response = requests.get(url, headers=headers, params=params, timeout=10)

    if response.status_code == 200:
        data = response.json()
        mini = data["data"]

        # 【防空大招】：如果百度返回空列表，直接砸碎翻页循环
        if len(mini) == 0:
            print("百度已经被榨干了，没有更多图片啦！")
            break

        # 5. 内层循环：提取并下载本页的图片
        for item in mini:
            # 防呆：只处理字典
            if isinstance(item, dict):
                wi = item.get("thumbURL") or item.get("middleURL")

                # 如果链接存在，且不在我们的记账本里（去重）
                if wi and wi not in history_urls:
                    try:
                        # 下载图片
                        img_resp = requests.get(wi, headers=headers, timeout=10)

                        if img_resp.status_code == 200:
                            # 存图片
                            with open(f"tupian/tupian_{count}.jpg", "wb") as f:
                                f.write(img_resp.content)

                            print(f"✅ 成功保存第 {count} 张！")

                            # 记账和加数
                            count += 1
                            history_urls.add(wi)

                            # 【刹车大招】：如果存够了，打破内层循环
                            if count > need_count:
                                break

                    except Exception as e:
                        print(f"💥 第{count}张报错跳过: {e}")

                    # 防封禁休息
                    time.sleep(0.25)

                    # 【外层刹车】：如果内层已经抓够了，打破外层翻页循环
    if count > need_count:
        print(f"\n🎉 任务完成！已经成功抓够了 {user_count} 张图！")
        break

    # 每抓完一页，多睡一会儿
    time.sleep(2)

print("程序结束，快去 tupian.1 文件夹验收吧！")