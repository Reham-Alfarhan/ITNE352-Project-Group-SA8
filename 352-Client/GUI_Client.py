import tkinter as tk
import socket
import json
import threading

# Set up the main window
window = tk.Tk()
window.title("Flight Information Client")
window.geometry("900x700")
window.configure(bg="#92b2c8")  # Light background color

# Global variable to store data
data = None

# Function to send data to the server
def presendingtoserver():
    global data
    client_name = entry_name.get()
    command = entry_command.get()
    flight_number = entry_flight_number.get() if command == "3" else None

    if not client_name:
        result_label.config(text="Please enter your name.", fg="red")
        return
    if command not in ["1", "2", "3", "4"]:
        result_label.config(text="Invalid command. Please select 1, 2, 3, or 4.", fg="red")
        return

    data = json.dumps({
        "client_name": client_name,
        "command": command,
        "flight_number": flight_number
    })

    # Use a new thread to communicate with the server without freezing the GUI
    threading.Thread(target=sendingToServer).start()

# Function to handle server communication
def sendingToServer():
    server_ip = "127.0.0.1"
    server_port = 12559

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))

        client_socket.send(data.encode())
        response = client_socket.recv(4096).decode('utf-8')
        display_results(response)

        client_socket.close()

    except Exception as e:
        error_message = f"Connection error: {e}"
        result_label.config(text=error_message, fg="red")

# Function to display server response in the listbox
def display_results(response):
    listbox.delete(0, tk.END)

    if isinstance(response, str):
        lines = response.split('\n')
        for line in lines:
            listbox.insert(tk.END, line)
    else:
        listbox.insert(tk.END, "Unexpected response format.")

# ----------------- GUI Elements ---------------------

# Welcome label
greeting = tk.Label(window, text="✈️ Welcome to the Flight Info Client ✈️", font=("Arial", 20, "bold"), bg="#92b2c8")
greeting.pack(pady=20)

# Frame for input fields
frame = tk.Frame(window, bg="#92b2c8", padx=20, pady=20, relief=tk.RIDGE, borderwidth=2)
frame.pack(pady=10)

# Name input
label_name = tk.Label(frame, text="Enter your name:", font=("Arial", 12), bg="#92b2c8")
label_name.grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_name = tk.Entry(frame, width=30)
entry_name.grid(row=0, column=1, padx=10, pady=5)

# Command menu
label_menu = tk.Label(frame, text="Main Menu:\n1) Get Arrived Flights\n2) Get Delayed Flights\n3) Flight Details\n4) Quit",
                       font=("Arial", 12), bg="#92b2c8", justify="left")
label_menu.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="w")

# Command input
label_command = tk.Label(frame, text="Enter your choice:", font=("Arial", 12), bg="#92b2c8")
label_command.grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_command = tk.Entry(frame, width=10)
entry_command.grid(row=2, column=1, padx=10, pady=5, sticky="w")

# Flight number input (optional)
label_flight_number = tk.Label(frame, text="Enter flight number (if option 3):", font=("Arial", 12), bg="#92b2c8")
label_flight_number.grid(row=3, column=0, padx=10, pady=5, sticky="e")
entry_flight_number = tk.Entry(frame, width=20)
entry_flight_number.grid(row=3, column=1, padx=10, pady=5, sticky="w")

# Submit button
submit_button = tk.Button(frame, text="Submit", font=("Arial", 12), bg="#4CAF50", fg="white", command=presendingtoserver)
submit_button.grid(row=4, column=0, columnspan=2, pady=10)

# Result label for displaying messages
result_label = tk.Label(frame, text="", font=("Arial", 12), bg="#ffffff", fg="red")
result_label.grid(row=5, column=0, columnspan=2, pady=5)

# Frame for the listbox to display results
listbox_frame = tk.Frame(window)
listbox_frame.pack(pady=10)

listbox = tk.Listbox(listbox_frame, font=("Arial", 10), width=80, height=15, bg="#92b2c8")
listbox.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar = tk.Scrollbar(listbox_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# Run the GUI
window.mainloop()
