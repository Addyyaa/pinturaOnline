import threading
import time

def print_message(message):
    print(message)

def thread_function_1():
    for _ in range(5):
        print_message("Thread 1")
        time.sleep(1)

def thread_function_2():
    for _ in range(5):
        print_message("Thread 2")
        time.sleep(1)

if __name__ == "__main__":
    thread1 = threading.Thread(target=thread_function_1)
    thread2 = threading.Thread(target=thread_function_2)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
