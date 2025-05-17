# Flight arrival Client/Server Information System 

## Project Description:
This project develops a client-server system that facilitates the exchange of flight data for a specified airport via an external API.  The system is designed to demonstrate client/server architecture, network connection, multithreading, and the use of coding techniques. Users can interact with the application through the graphical user interface (GUI) of the tool.

## Second Semester 2024-2025
#### o Group SA8
#### o Course: ITNE-352
#### o Section: 01
#### o Reham Mohammed Alfarhan - 202105915
#### o AISHA SALEH ALNADHER - 202207765

## Table of Contents:
#### Project Title: Flight arrival Client/Server Information System 
#### Project Description
#### Second Semester 2024-2025
#### Group: SA8
#### Requirements
#### How to run The Scripts
#### Additional Concept
#### Acknowledgments
#### Conclusion

## • Requirements:
Installing the necessary libraries in your environment is necessary to guarantee error-free code execution. Enter the following commands into your terminal to accomplish this:  requests to install pip for tkinter pip  How to run the code:


## • Running the code:
Split the terminal in half after opening it in your IDE. ii. Open a terminal and run the server file, python.\server-side.py.  III. Launch the GUI_Client.py Python client file in the other.

## • Interacting with the GUI:
Once the client code has connected to the server, the user will be asked for their name.  o A menu with the following choices will be shown to the user: Quit, sources, and headlines.  If you select "Quit," the connection will be terminated.  o A list of headlines and sources with a synopsis of each result will be generated after the user selects an option. The user can select a result to see more details about it if he needs them.

## • The code:
The two primary files in the code are server-side.py and GUI_Client.py.

## • GUI_Client.py:
Using the Tkinter framework, the code generates a graphical user interface (GUI) client application to retrieve real-time flight data from a server. The client connects to the server through a socket connection to request information such as arrived flights, delayed flights, detailed flight details, and airport-based listings.

## • Main Menu:
When launching the application for the first time, users must enter their name.
-After entering a name, users are presented with a primary menu that includes the following options:

🛬 Get Arrived Flights

⏱ Get Delayed Flights

🔍 Flight Details by Airport Code

❌ Quit

## • List of Sources:
🌐 Airport List (Future/Optional Feature) Users could have access to a list of supported airports in one of two ways:
 Country.
 Region.
 ICAO Prefix.
 List All.
 Back to Main Menu.





## • Server-Side.py:
This Python script implements the server-side of a multithreaded client/server flight information system. It is responsible for retrieving real-time flight data from the aviationstack.com API, handling multiple client connections securely over SSL, and responding to various flight information requests.
The script uses core Python libraries such as socket, ssl, threading, and requests, and applies good coding practices including modular design and proper exception handling.
Main Components:
	•	Class: FlightServer
This is the core server class. It initializes the server socket, loads flight data from the API, and manages all client communication through separate threads.
	•	_init_() Method
Initializes the server with a host, port, and SSL certificates. It binds the socket, starts listening, and preloads flight data by prompting the user for an ICAO airport code.
	•	load_flight_data()
Sends an HTTP request to the aviationstack API to retrieve flight information based on the provided ICAO code. The data is stored in a file called group_A.json for reference.
	•	start_server()
Continuously listens for new client connections. For each connection, it wraps the socket with SSL encryption and starts a new thread using the handle_client() method.
	•	handle_client()
Greets the client, asks for their name, and presents a menu with 4 options:
	1.	Get all arrived flights
	2.	Get all delayed flights
	3.	Get details of a specific flight
	4.	Quit
Based on the client's selection, it sends back the appropriate data or closes the connection.
	•	send_arrived_flights()
Scans the retrieved data and sends a list of all flights that have an actual arrival time, including the flight IATA code, departure airport, arrival time, terminal, and gate.
	•	send_delayed_flights()
Filters flights that are delayed (have a non-zero delay value), and sends relevant info like departure time, estimated arrival, delay duration, terminal, and gate.
	•	send_flight_details()
Prompts the user to enter a flight IATA code, then searches for the flight and returns detailed information such as departure and arrival airports, gate and terminal info, scheduled times, and status.
	•	SSL Encryption
The server uses server.crt and server.key to encrypt all communications. This ensures secure transmission of all data exchanged between the client and server.
Final Notes:
The server is designed to handle at least 3 simultaneous client connections, all running securely and independently. It uses multithreading to keep each client session isolated and responsive. The system is scalable and easy to test locally or over a LAN, making it ideal for learning real-world client/server architecture in Python.


## • Acknowledgments:
I want to sincerely thank my doctor, Dr. Mohamed A. Almeer, for his constant encouragement, sage advice, and support throughout the entire process. His wise advice was essential in deciding the direction and result of this work. I also greatly value the cooperation and support of my classmates, especially when I encountered technical issues or needed assistance debugging. Their cooperation kept me motivated and focused. Finally, I want to give thanks to God for all of my achievements, whose graces made this effort possible.

## • Conclusion:
The project's client-server system receives real-time flight data via a graphical user interface based on Tkinter. You can find flights that have arrived or are delayed, search by airport code, and obtain detailed flight information. The server receives user input from the client, requests a flight information API, runs each request in a separate thread, and then sends the results for display. The system's capabilities include network connectivity, multithreading, and interactive GUI design for real-time data access.















