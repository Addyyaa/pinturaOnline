import time

for i in range(5):
    print(f"Counting: {i}", end="\r")
    time.sleep(1)  # 等待1秒钟

print("Done!")
