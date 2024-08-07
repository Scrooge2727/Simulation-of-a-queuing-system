import tkinter as tk
from tkinter import ttk
import random


class QueueSimulation:
    def __init__(self, master):
        self.master = master
        self.master.title("Queue Simulation")
        self.label_lambda_exp = ttk.Label(master, text="Средний интервал поступления (λ):")
        self.label_lambda_exp.grid(row=0, column=0, padx=5, pady=5)
        self.lambda_exp_entry = ttk.Entry(master)
        self.lambda_exp_entry.grid(row=0, column=1, padx=5, pady=5)

        self.label_std_dev_exp = ttk.Label(master, text="Стандартное отклонение поступления (σ):")
        self.label_std_dev_exp.grid(row=1, column=0, padx=5, pady=5)
        self.std_dev_exp_entry = ttk.Entry(master)
        self.std_dev_exp_entry.grid(row=1, column=1, padx=5, pady=5)

        self.label_lambda_norm = ttk.Label(master, text="Средний интервал обработки (λ):")
        self.label_lambda_norm.grid(row=2, column=0, padx=5, pady=5)
        self.lambda_norm_entry = ttk.Entry(master)
        self.lambda_norm_entry.grid(row=2, column=1, padx=5, pady=5)

        self.label_std_dev_norm = ttk.Label(master, text="Стандартное отклонение обработки (σ):")
        self.label_std_dev_norm.grid(row=3, column=0, padx=5, pady=5)
        self.std_dev_norm_entry = ttk.Entry(master)
        self.std_dev_norm_entry.grid(row=3, column=1, padx=5, pady=5)

        self.queue_value = tk.Listbox(master, width=30, height=20)
        self.queue_value.grid(row=4, column=0, padx=5, pady=5)

        self.start_simulation_button = ttk.Button(master, text="Начать моделирование", command=self.start)
        self.start_simulation_button.grid(row=5, column=0, pady=10)

        self.standard_data_button = ttk.Button(master, text="Внести стандартные данные", command=self.standard_data)
        self.standard_data_button.grid(row=5, column=1, pady=10)

        self.stop_simulation_button = ttk.Button(master, text="Остановить моделирование", command=self.stop_simulation)
        self.stop_simulation_button.grid(row=5, column=2, pady=10)

        self.label_current_number = ttk.Label(master, text="Обработка:")
        self.label_current_number.grid(row=6, column=0, padx=5, pady=5)

        self.current_number_entry = ttk.Entry(master)
        self.current_number_entry.grid(row=6, column=1, padx=5, pady=5)
        self.label_processing_time = ttk.Label(master, text="Следующее число через:")
        self.label_processing_time.grid(row=7, column=0, padx=5, pady=5)
        self.processing_time_entry = ttk.Entry(master)
        self.processing_time_entry.grid(row=7, column=1, padx=5, pady=5)

        self.label_max_queue_size = ttk.Label(master, text="Максимальный размер очереди")
        self.label_max_queue_size.grid(row=0, column=2, padx=5, pady=5)
        self.max_queue_size_entry = ttk.Entry(master)
        self.max_queue_size_entry.grid(row=0, column=3, padx=5, pady=5)

        self.label_average_queue_size = ttk.Label(master, text="Средний размер очереди")
        self.label_average_queue_size.grid(row=1, column=2, padx=5, pady=5)
        self.average_queue_size_entry = ttk.Entry(master)
        self.average_queue_size_entry.grid(row=1, column=3, padx=5, pady=5)

        self.label_max_time_in_queue = ttk.Label(master, text="Максимальное время нахождения запроса в очереди")
        self.label_max_time_in_queue.grid(row=2, column=2, padx=5, pady=5)
        self.max_time_in_queue_entry = ttk.Entry(master)
        self.max_time_in_queue_entry.grid(row=2, column=3, padx=5, pady=5)

        self.label_average_time_in_queue = ttk.Label(master, text="Среднее время нахождения запроса в очереди")
        self.label_average_time_in_queue.grid(row=3, column=2, padx=5, pady=5)
        self.average_time_in_queue_entry = ttk.Entry(master)
        self.average_time_in_queue_entry.grid(row=3, column=3, padx=5, pady=5)


    def stop_simulation(self):
        self.simulation_running = False

    def update_average_queue_size(self):
        if self.measurements_count > 0:
            self.average_queue_size_entry.delete(0, tk.END)
            self.average_queue_size_entry.insert(0, self.total_queue_size / self.measurements_count)

    def update_max_queue_size(self, current_size):
        if current_size > self.max_queue_size:
            self.max_queue_size = current_size
        self.max_queue_size_entry.delete(0, tk.END)
        self.max_queue_size_entry.insert(0, self.max_queue_size)

    def update_average_time_in_queue(self):
        #self.sum_q += total_size_queue
        if len(self.numbers2) > 0:
            self.average_time_in_queue_entry .delete(0, tk.END)
            self.average_time_in_queue_entry .insert(0, sum(self.numbers2) / len(self.numbers2))

    def update_max_time_in_queue(self, total_size_queue):
        if total_size_queue > self.max_time_in_queue:
            self.max_time_in_queue = total_size_queue
        self.max_time_in_queue_entry.delete(0, tk.END)
        self.max_time_in_queue_entry.insert(0, self.max_time_in_queue)

    def update_current_number(self):
        if self.numbers:
            current_number = self.numbers[0]
            self.current_number_entry.delete(0, tk.END)
            self.current_number_entry.insert(0, current_number)

    def update_processing_time(self, processing_time):
        self.processing_time_entry.delete(0, tk.END)
        self.processing_time_entry.insert(0, processing_time)

    def update_queue_listbox(self):
        self.queue_value.delete(0, tk.END)
        for item in self.numbers:
            self.queue_value.insert(tk.END, item)

    def generate_exponential_intervals(self, mean):
        return int(random.expovariate(1 / mean))

    def generate_normal_intervals(self, mean, std_dev):
        return int(random.normalvariate(mean, std_dev))

    def simulate_queue(self, lambda_exp_val, std_dev_exp_val, lambda_norm_val, std_dev_norm_val):
        if not self.simulation_running:
            return
        self.numbers.append(self.generate_normal_intervals(lambda_norm_val, std_dev_norm_val))
        self.numbers2.append(self.generate_normal_intervals(lambda_norm_val, std_dev_norm_val))
        #processing_time = 2
        processing_time = self.generate_exponential_intervals(lambda_exp_val)
        if self.numbers[0] > 0:
            self.update_current_number()
            self.master.after(1, self.process_queue, processing_time, self.numbers[0])

    def process_queue(self, processing_time, remaining_count):
        if not self.simulation_running:
            return
        self.measurements_count += 1
        current_size = len(self.numbers)
        total_sum_size_queue = sum(self.numbers)
        self.update_average_time_in_queue()
        self.update_max_time_in_queue(total_sum_size_queue)
        self.total_queue_size += current_size
        self.update_max_queue_size(current_size)
        self.update_average_queue_size()
        self.update_queue_listbox()
        self.update_processing_time(processing_time)
        processing_time -= 1
        if processing_time <= 0:
            # self.update_processing_time(processing_time)
            # self.update_queue_listbox()
            self.master.after(100, self.simulate_queue,
                              self.lambda_exp_val, self.std_dev_exp_val, self.lambda_norm_val, self.std_dev_norm_val)
        elif remaining_count > 0:
            self.numbers[0] -= 1
            remaining_count -= 1
            self.update_current_number()
            self.master.after(100, self.process_queue, processing_time, remaining_count)
        elif remaining_count == 0:
            self.numbers.pop(0)
            self.update_queue_listbox()
            if self.numbers:
                remaining_count = self.numbers[0]
            else:
                remaining_count = -1
            self.master.after(100, self.process_queue, processing_time, remaining_count)
        elif remaining_count <= -1:
            self.master.after(100, self.process_queue, processing_time, remaining_count)

    def start(self):
        self.simulation_running = True
        self.numbers = []
        self.numbers2 = []  # Используйте список для хранения текущего числа
        self.max_queue_size = 0  # Отслеживание максимального размера очереди
        self.total_queue_size = 0  # Общий размер очереди
        self.measurements_count = 0  # Количество замеров размера очереди
        self.total_time_in_queue = 0
        self.max_time_in_queue = 0
        self.sum_q = 0
        self.simulation_running = True
        self.lambda_exp_val = float(self.lambda_exp_entry.get())
        self.std_dev_exp_val = float(self.std_dev_exp_entry.get())
        self.lambda_norm_val = float(self.lambda_norm_entry.get())
        self.std_dev_norm_val = float(self.std_dev_norm_entry.get())
        self.simulate_queue(self.lambda_exp_val, self.std_dev_exp_val, self.lambda_norm_val, self.std_dev_norm_val)

    def standard_data(self):
        self.lambda_exp_entry.insert(0, "25")
        self.std_dev_exp_entry.insert(0, "10")
        self.lambda_norm_entry.insert(0, "20")
        self.std_dev_norm_entry.insert(0, "7")


def main():
    root = tk.Tk()
    QueueSimulation(root)
    root.mainloop()


if __name__ == "__main__":
    main()
