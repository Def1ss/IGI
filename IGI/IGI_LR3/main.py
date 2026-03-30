"""
Purpose: Main user interface and execution loop
Lab: Laboratory Work 3
Version: 1.0
Developer: Daniil Vadimovich Borsuk
Date: 2026-03-30
"""
import  tasks   
import initialization
from tabulate import tabulate

def log_execution(func):
    """Decorator to log the start and end of function execution."""
    def wrapper(*args, **kwargs):
        print(f"\n[{func.__name__.upper()}] --- Execution started ---")
        result = func(*args, **kwargs)
        print(f"[{func.__name__.upper()}] --- Execution finished ---\n")
        return result
    return wrapper

@log_execution
def run_task1():
    try:
        x = float(input("Enter argument x (|x| < 1) for ln(1+x): "))
        if abs(x) >= 1:
            print("Error: The series converges only for |x| < 1.")
            return
            
        eps = float(input("Enter precision eps (e.g., 0.001): "))
        n, f_x, math_f_x = tasks.task1_series(x, eps)
        
        table_data = [[x, n, f_x, math_f_x]]
        headers = ["x", "n", "F(x)", "Math F(x)"]
        print(tabulate(table_data, headers=headers, 
                      floatfmt=(".4f", "d", ".6f", ".6f"),
                      tablefmt="grid"))
    except ValueError:
        print("Error: Invalid number format.")

@log_execution
def run_task2():
    print("Enter integers to count Positive numbers. Enter 10 to stop.")
    positive_count = 0
    numbers_entered = []
    
    while True:
        try:
            val = int(input("> "))
            numbers_entered.append(val)
            if val == 10:
                print("Stop condition met (entered 10).")
                break
            if val > 0:
                positive_count += 1
        except ValueError:
            print("Error: Please enter a valid integer.")
    
    if numbers_entered:
        table_data = [[i+1, num] for i, num in enumerate(numbers_entered)]
        headers = ["Entry #", "Value"]
        print("\n" + tabulate(table_data, headers=headers, tablefmt="grid"))
    
    print(f"\nTotal positive numbers entered: {positive_count}")

@log_execution
def run_task3():
    text = input("Enter a string for hexadecimal analysis: ")
    is_hex = tasks.task3_is_hex(text)
    
    table_data = [[text, "Valid hexadecimal" if is_hex else "Invalid hexadecimal"]]
    headers = ["Input String", "Analysis Result"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

@log_execution
def run_task4():
    target_string = ("So she was considering in her own mind, as well as she could, "
                     "for the hot day made her feel very sleepy and stupid, whether "
                     "the pleasure of making a daisy-chain would be worth the trouble "
                     "of getting up and picking the daisies, when suddenly a White "
                     "Rabbit with pink eyes ran close by her.")
                     
    print("Analyzing predefined string:\n", target_string)
    
    total, even_words, short_a, repeaters = tasks.task4_analyze_alice(target_string)
    
    summary_data = [
        ["Total words", total],
        ["Shortest word starting with 'a'", f"'{short_a}'"],
        ["Number of even-length words", len(even_words)],
        ["Number of repeating words", len(repeaters)]
    ]
    print("\n" + tabulate(summary_data, tablefmt="grid"))
    
    if even_words:
        even_data = [[i+1, word] for i, word in enumerate(even_words)]
        print("\n" + tabulate(even_data, headers=["#", "Even-length words"], 
                              tablefmt="grid"))
    
    if repeaters:
        repeaters_data = [[i+1, word] for i, word in enumerate(repeaters)]
        print("\n" + tabulate(repeaters_data, headers=["#", "Repeating words"], 
                              tablefmt="grid"))

@log_execution
def run_task5():
    try:
        size = int(input("Enter the size of the list: "))
        if size <= 0:
            print("Size must be a positive integer.")
            return
            
        choice = input("Initialize manually (m) or via random generator (r)? ").strip().lower()
        my_list = []
        

        if choice == 'm':
            initialization.init_via_input(my_list, size)
        elif choice == 'r':
            initialization.init_via_generator(my_list, size)
        else:
            print("Invalid initialization choice.")
            return
            
        print("\nGenerated list:", my_list)
        
        max_mod, sum_before = tasks.task5_process_list(my_list)
        
        table_data = [
            ["Element with maximum absolute value", f"{max_mod:.4f}"],
            ["Sum before last positive element", f"{sum_before:.4f}"]
        ]
        headers = ["Metric", "Value"]
        print("\n" + tabulate(table_data, headers=headers, tablefmt="grid"))
        
    except ValueError:
        print("Error: Invalid integer input.")

def main():
    while True:
        print("\n" + "="*25)
        print("        MAIN MENU")
        print("="*25)
        print("1. Task 1 (ln(1+x) Taylor series)")
        print("2. Task 2 (Counting positive numbers until 10)")
        print("3. Task 3 (String analysis: is hexadecimal)")
        print("4. Task 4 (Alice text complex analysis)")
        print("5. Task 5 (Processing list of floats)")
        print("0. Exit program")
        
        choice = input("\nSelect a task: ").strip()
        

        if choice == '1': run_task1()
        elif choice == '2': run_task2()
        elif choice == '3': run_task3()
        elif choice == '4': run_task4()
        elif choice == '5': run_task5()
        elif choice == '0':
            print("Exiting... Have a good day!")
            break
        else:
            print("Invalid choice. Please select a number from 0 to 5.")

        

if __name__ == "__main__":
    main()