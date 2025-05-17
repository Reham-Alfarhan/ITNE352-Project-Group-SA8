import socket
import ssl
import json
import threading
import requests

# Server class to handle flight data and client interactions
class FlightServer:
    def __init__(self, host='localhost', port=12346, certfile='server.crt', keyfile='server.key'):
        self.host = host
        self.port = port
        self.certfile = certfile
        self.keyfile = keyfile
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(3)
        self.flights_data = self.load_flight_data()

    # Load flight data from the API and store in JSON file
    def load_flight_data(self):
        api_key = '28dcd233c4e20284933d0280f6f9b673'
        airport_code = input("Enter the ICAO code of the airport (e.g., BAH): ").strip().upper()
        url = f"http://api.aviationstack.com/v1/flights?access_key={api_key}&arr_icao={airport_code}&limit=100"

        response = requests.get(url)
        if response.status_code == 200:
            flight_data = response.json()
            with open("group_A.json", "w") as json_file:  # Replace "group_A" with your actual group ID
                json.dump(flight_data, json_file, indent=4)
            print(f"[INFO] Flight data for {airport_code} retrieved successfully.")
            return flight_data
        else:
            print("[ERROR] Failed to retrieve flight data.")
            return {"data": []}

    # Handle individual client connection
    def handle_client(self, client_socket, client_address):
        try:
            print(f"[INFO] New connection from {client_address}")
            client_socket.send("Welcome! Please enter your username: ".encode())
            client_name = client_socket.recv(1024).decode().strip()
            print(f"[INFO] Client name: {client_name}")

            while True:
                menu = """
1. Get all arrived flights
2. Get all delayed flights
3. Get details of a particular flight
4. Quit
Enter your choice: """
                client_socket.send(menu.encode())
                choice = client_socket.recv(1024).decode().strip()
                print(f"[REQUEST] {client_name} selected option {choice}")

                if choice == '1':
                    self.send_arrived_flights(client_socket)
                elif choice == '2':
                    self.send_delayed_flights(client_socket)
                elif choice == '3':
                    self.send_flight_details(client_socket)
                elif choice == '4':
                    break
                else:
                    client_socket.send("Invalid choice. Try again.\n".encode())

            client_socket.send("Goodbye!\n".encode())
            print(f"[DISCONNECT] {client_name} has disconnected.")
            client_socket.close()

        except Exception as e:
            print(f"[ERROR] Client error: {e}")
            client_socket.close()

    # Send all arrived flights to client
    def send_arrived_flights(self, client_socket):
        output = "Arrived Flights:\n"
        for flight in self.flights_data['data']:
            try:
                if flight['arrival']['actual']:
                    output += f"Flight {flight['flight']['iata']}, From {flight['departure']['airport']}, Arrival: {flight['arrival']['scheduled']}, Terminal: {flight['arrival']['terminal']}, Gate: {flight['arrival']['gate']}\n"
            except:
                continue
        client_socket.send(output.encode())

    # Send delayed flights info
    def send_delayed_flights(self, client_socket):
        output = "Delayed Flights:\n"
        for flight in self.flights_data['data']:
            try:
                delay = flight['arrival']['delay']
                if delay and delay > 0:
                    output += f"Flight {flight['flight']['iata']}, From {flight['departure']['airport']}, Departure: {flight['departure']['scheduled']}, Estimated Arrival: {flight['arrival']['estimated']}, Delay: {delay} minutes, Terminal: {flight['arrival']['terminal']}, Gate: {flight['arrival']['gate']}\n"
            except:
                continue
        client_socket.send(output.encode())

    # Send details for a specific flight
    def send_flight_details(self, client_socket):
        client_socket.send("Enter flight IATA code: ".encode())
        code = client_socket.recv(1024).decode().strip().upper()
        flight_found = False

        for flight in self.flights_data['data']:
            if flight['flight']['iata'] == code:
                try:
                    details = f"""
Flight {code} Details:
Departure: {flight['departure']['airport']}, Terminal: {flight['departure']['terminal']}, Gate: {flight['departure']['gate']}
Arrival: {flight['arrival']['airport']}, Terminal: {flight['arrival']['terminal']}, Gate: {flight['arrival']['gate']}
Status: {flight['flight_status']}
Scheduled Departure: {flight['departure']['scheduled']}
Scheduled Arrival: {flight['arrival']['scheduled']}
"""
                    client_socket.send(details.encode())
                    flight_found = True
                    break
                except:
                    continue

        if not flight_found:
            client_socket.send(f"No details found for flight {code}\n".encode())

    # Start the server and accept client connections
    def start_server(self):
        print(f"[SERVER] Listening on {self.host}:{self.port} with SSL")
        while True:
            client_socket, client_address = self.server_socket.accept()
            ssl_client_socket = ssl.wrap_socket(
                client_socket,
                keyfile=self.keyfile,
                certfile=self.certfile,
                server_side=True
            )
            thread = threading.Thread(target=self.handle_client, args=(ssl_client_socket, client_address))
            thread.start()


# Run the server
if __name__ == "__main__":
    server = FlightServer(host='0.0.0.0', port=12346)
    server.start_server()
