# Importing Necessary Libraries
import tkinter as tk
import socket
import json

# Prepare the interface window configuration
window = tk.Tk()
window.title("Flight Information Client")
window.geometry("900x700")  
window.configure(bg="#ffcccc")
global data

#---------Placing Main widgets-----------------
def presendingtoserver():
    global data
    client_name = entry_label1.get()
    command = ent3.get()
    airport_code = ent4.get()

    # Validate inputs
    if not client_name:
        result_label.config(text="Please enter your name.", fg="red")
        return
    if command not in ["1", "2", "3", "4"]:
        result_label.config(text="Invalid command. Please select 1, 2, 3, or 4.", fg="red")
        return

    # Prepare the data for sending to server
    data = json.dumps({
        "client_name": client_name,
        "command": command,
        "airport_code": airport_code
    })

    sendingToServer()

#---------------Function To send Client Request To Server------------------
def sendingToServer():
    server_ip = "127.0.0.1"
    server_port = 12346  # Ensure this matches the server port
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))

        client_socket.send(data.encode())
        response = client_socket.recv(4096).decode('utf-8')
        
        # Display the results
        display_results(json.loads(response))
        
    except Exception as e:
        print(f"Error: {e}")
        result_label.config(text="Error communicating with server.", fg="red")

#-----------Function For Displaying Server Response To Window---------------
def display_results(response):
    listbox.delete(0, tk.END)  # Clear previous results
    if "error" in response:
        result_label.config(text=response["error"], fg="red")
    else:
        for flight in response.get('data', []):
            flight_info = f"Flight: {flight['flight']['iata']}, From: {flight['departure']['airport']}, Arrival: {flight['arrival']['airport']}, Status: {flight['flight_status']}"
            listbox.insert(tk.END, flight_info)

#-----------------Window Widgets---------------------
greeting = tk.Label(text="🎉 WELCOME TO FLIGHT INFO CLIENT 🎉", font=("Times New Roman", 20), bg="#ffcccc")
greeting.grid(row=0, column=0, columnspan=2, pady=10)

frame = tk.Frame(window, bg="#ffcccc", padx=10, pady=10)
frame.grid(row=1, column=0, columnspan=2, pady=10)

lb1 = tk.Label(frame, text="Enter Your Name:", font=("Times New Roman", 12), bg="#ffcccc")
lb1.grid(row=0, column=0, padx=10, pady=5, sticky="w")

entry_label1 = tk.Entry(frame)
entry_label1.grid(row=0, column=1, padx=10, pady=5)

lb2 = tk.Label(frame, text="The Main Menu:\n 1) Get Arrived Flights\n 2) Get Delayed Flights\n 3) Flight Details\n 4) Quit", 
               font=("Times New Roman", 12, "bold"), bg="#ffcccc", justify="left")
lb2.grid(row=1, column=0, padx=10, pady=10, sticky="w")

lb3 = tk.Label(frame, text="Enter Your choice:", font=("Times New Roman", 12), bg="#ffcccc")
lb3.grid(row=2, column=0, padx=10, pady=10, sticky="w")

ent3 = tk.Entry(frame)
ent3.grid(row=2, column=1, padx=10, pady=10, sticky="w")

lb4 = tk.Label(frame, text="Enter Airport Code (ICAO):", font=("Times New Roman", 12), bg="#ffcccc")
lb4.grid(row=3, column=0, padx=10, pady=10, sticky="w")

ent4 = tk.Entry(frame)
ent4.grid(row=3, column=1, padx=10, pady=10, sticky="w")

button = tk.Button(frame, text="Submit", font=("Times New Roman", 12), bg="#ffcccc", command=presendingtoserver)
button.grid(row=4, column=0, padx=10, pady=10, sticky="w")

result_label = tk.Label(frame, text="", font=("Times New Roman", 12), bg="#ffcccc")
result_label.grid(row=5, column=0, columnspan=2, pady=10)

listbox_frame = tk.Frame(frame)
listbox_frame.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

listbox = tk.Listbox(listbox_frame, font=("Times New Roman", 10), width=70, height=15, bg="#f0f0f0")
listbox.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar = tk.Scrollbar(listbox_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# Run the interface
window.mainloop()