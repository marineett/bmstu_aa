import time

read_queue = []
extract_queue = []
store_queue = []

class Task:
    def __init__(self, task_type, data):
        self.task_type = task_type
        self.data = data
        self.created_time = time.time()  

    def get_wait_time(self):
        return time.time() - self.created_time  
    
def add_task_to_queue(queue, task):
    queue.append(task)

def calculate_average_wait_time(queue):
    total_wait_time = 0
    task_count = len(queue)
    
    for task in queue:
        total_wait_time += task.get_wait_time()
    
    return total_wait_time / task_count if task_count > 0 else 0

def print_table():
    read_avg_wait = calculate_average_wait_time(read_queue)
    extract_avg_wait = calculate_average_wait_time(extract_queue)
    store_avg_wait = calculate_average_wait_time(store_queue)

    print("queue\t\t\taverage wait time")
    print("----------------------------------------")
    print(f"read_queue\t\t{read_avg_wait:.2f} seconds")
    print(f"extract_queue\t\t{extract_avg_wait:.2f} seconds")
    print(f"store_queue\t\t{store_avg_wait:.2f} seconds")

if __name__ == "__main__":
    add_task_to_queue(read_queue, Task("READ", "file1.html"))
    time.sleep(1)
    add_task_to_queue(extract_queue, Task("EXTRACT", "file1"))
    time.sleep(2)
    add_task_to_queue(store_queue, Task("STORE", "data"))

    print_table()
