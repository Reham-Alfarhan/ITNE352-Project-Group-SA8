import socket
import threading
import requests
import json

# Server configuration
HOST = '127.0.0.1'
PORT = 12559
API_KEY = '28dcd233c4e20284933d0280f6f9b673'
API_URL = 'http://api.aviationstack.com/v1/flights'


# Load data once when the server starts
def fetch_flight_data(airport_code):
    params = {
        'access_key': API_KEY,
        'arr_icao': airport_code,
        'limit': 100
    }
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        filename = f"flights_{airport_code}.json"
        with open(filename, "w") as f:
            json.dump(data, f)

        print(f" JSON file created successfully: {filename}")

        if not data.get("data"):
            print("[WARNING] API returned no data.")
            return None



        print("[INFO] Flight data fetched and stored.")
        return data

    except Exception as e:
        print(f"Failed to fetch flight data: {e}")
        return None


# Process client request based on command
def process_request(command, airport_code, flight_number=None):
    try:
        print("[DEBUG] Attempting to open flights_data.json...")

        filename = f"flights_{airport_code}.json"
        print(f"[DEBUG] Attempting to open {filename}...")
        try:
            with open(filename, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            return f"Error: {filename} not found. Please fetch data first."
        except json.JSONDecodeError:
            return f"Error: {filename} is corrupted or empty."

        flights = data.get("data", [])
        if not flights:
            return "No flight data found for the selected airport."

        result = []

        if command == "1":  # Get Arrived Flights
            for flight in flights:
                if flight['arrival']['airport'] and flight['arrival']['iata']:
                    result.append(
                        f"Flight: {flight['flight']['iata']}, From: {flight['departure']['airport']}, "
                        f"Arrival Time: {flight['arrival']['actual']}, "
                        f"Terminal: {flight['arrival'].get('terminal', '-')}, "
                        f"Gate: {flight['arrival'].get('gate', '-')}"
                    )

        elif command == "2":  # Get Delayed Flights
            for flight in flights:
                delay = flight['arrival'].get('delay')
                if delay and delay > 0:
                    result.append(
                        f"Flight: {flight['flight']['iata']}, From: {flight['departure']['airport']}, "
                        f"Departure: {flight['departure'].get('scheduled', '-')}, "
                        f"ETA: {flight['arrival'].get('estimated', '-')}, "
                        f"Terminal: {flight['arrival'].get('terminal', '-')}, "
                        f"Gate: {flight['arrival'].get('gate', '-')}, Delay: {delay} min"
                    )

        elif command == "3" and flight_number:
            for flight in flights:
                if flight['flight']['iata'].lower() == flight_number.lower():
                    result.append(
                        f"Flight: {flight['flight']['iata']},\n"
                        f"Departure: {flight['departure']['airport']} "
                        f"(Gate: {flight['departure'].get('gate', '-')}, Terminal: {flight['departure'].get('terminal', '-')})\n"
                        f"Arrival: {flight['arrival']['airport']} "
                        f"(Gate: {flight['arrival'].get('gate', '-')}, Terminal: {flight['arrival'].get('terminal', '-')})\n"
                        f"Status: {flight['flight_status']}, "
                        f"Departure Time: {flight['departure'].get('scheduled', '-')}, "
                        f"Arrival Time: {flight['arrival'].get('scheduled', '-')}"
                    )
                    break

        return "\n".join(result) if result else "No matching flights found."

    except FileNotFoundError:
        return "Error: flights_data.json not found. Server might not have fetched data yet."
    except Exception as e:
        return f"Error processing request: {str(e)}"


# Handle client connection
def handle_client(client_socket, address):
    print(f"[CONNECTED] Client {address} connected.")
    try:
        while True:
            data = client_socket.recv(2048).decode('utf-8')
            if not data:
                break  #

            print(f"[RECEIVED] {data}")
            request = json.loads(data)

            name = request.get("client_name")
            command = request.get("command")
            airport_code = request.get("airport_code")
            flight_number = request.get("flight_number")

            print(f"[REQUEST] From: {name}, Command: {command}, Airport: {airport_code}, Flight: {flight_number}")
            fetch_flight_data(airport_code)


            if command == "4":
                response = "Goodbye!"
                client_socket.sendall(response.encode('utf-8', errors='replace'))
                break
            else:
                response = process_request(command, airport_code, flight_number)
                client_socket.sendall(response.encode('utf-8', errors='replace'))

        client_socket.close()
        print(f"[DISCONNECTED] Client {address} disconnected.")


    except Exception as e:
        error = f"[SERVER ERROR] {str(e)}"
        print(error)
        try:
            client_socket.sendall(error.encode('utf-8', errors='replace'))
        except:
            pass
    finally:
        client_socket.close()
        print(f"[DISCONNECTED] Client {address} disconnected.")



# Start server and accept multiple clients
def start_server():
    airport_code = input("Enter ICAO airport code (e.g., OBBI): ").strip().upper()
    data = fetch_flight_data(airport_code)
    with open("group_SA8.json", "w") as f:
        json.dump(data, f)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[LISTENING] Server is running on {HOST}:{PORT}")

    while True:
        try:
            client_socket, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
        except KeyboardInterrupt:
            print("\n[SHUTDOWN] Server shutting down.")
            server.close()
            break


# Entry point
if __name__ == "__main__":
    start_server()
