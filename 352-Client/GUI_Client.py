# Importing Necessary Libraries
import tkinter as tk
import socket
import requests
import json

# Prepare the interface window configuration
window = tk.Tk()
window.title("Flight Information System")
window.geometry("900x700")  
window.configure(bg="#ffcccc")
global data

API_KEY = 'YOUR_API_KEY'  # Replace with your actual API key
BASE_URL = 'http://api.aviationstack.com/v1/flights'

# Function to fetch flight data from the API
def fetch_flight_data(airport_code):
    params = {
        'access_key': API_KEY,
        'arr_icao': airport_code,
        'limit': 100
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code)
        return None

# Function to prepare data and send to the server
def presendingtoserver():
    global data
    client_name = entry_label1.get()
    command = ent3.get()
    airport_code = ent4.get()
    
    # Validate inputs
    if not client_name:
        result_label.config(text="Please enter your name.", fg="red")
        return
    if command not in ["1", "2"]:
        result_label.config(text="Invalid command. Please select 1 or 2.", fg="red")
        return

    # Prepare the data for sending to server
    data = f"Client name:{client_name}, Main Option:{command}, Airport Code:{airport_code}"

    if command == "1":
        result_label.config(text="Fetching flight data...", fg="black")
        flight_data = fetch_flight_data(airport_code)
        if flight_data:
            with open('group_ID.json', 'w') as json_file:
                json.dump(flight_data, json_file, indent=4)
            display_results(flight_data)
        else:
            result_label.config(text="Failed to fetch data.", fg="red")
    elif command == "2":  # Quit the application
        window.quit()

# Function to send client request to server
def sendingToServer():
    global data
    server_ip = "127.0.0.1"
    server_port = 33222
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))

        client_socket.send(data.encode())
        response = client_socket.recv(1024).decode('utf-8')
        display_results(json.loads(response))
    except Exception as e:
        print(f"Error: {e}")
        result_label.config(text="Error sending data.", fg="red")

# Function for displaying server response to the window
def display_results(response):
    results = response.get('data', [])  # Assuming response is in JSON format
    listbox.delete(0, tk.END)
    for flight in results:
        flight_info = f"Flight: {flight['flight']['iata']}, Arrival: {flight['arrival']['estimated']}, Status: {flight['status']}"
        listbox.insert(tk.END, flight_info)

# Window widgets
greeting = tk.Label(text="🎉 WELCOME TO FLIGHT INFO 🎉", font=("Times New Roman", 20), bg="#ffcccc")
greeting.grid(row=0, column=0, columnspan=2, pady=10)

frame = tk.Frame(window, bg="#ffcccc", padx=10, pady=10)
frame.grid(row=1, column=0, columnspan=2, pady=10)

lb1 = tk.Label(frame, text="Enter Your Name:", font=("Times New Roman", 12), bg="#ffcccc")
lb1.grid(row=0, column=0, padx=10, pady=5, sticky="w")

entry_label1 = tk.Entry(frame)
entry_label1.grid(row=0, column=1, padx=10, pady=5)

lb2 = tk.Label(frame, text="The Main Menu:\n 1) Fetch Flights 🔍\n2) Quit ❌", 
               font=("Times New Roman", 12, "bold"), bg="#ffcccc", justify="left")
lb2.grid(row=1, column=0, padx=10, pady=