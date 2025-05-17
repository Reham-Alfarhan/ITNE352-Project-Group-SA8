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
1. The welcome screen asks for the name of the user.
The Main Menu appears when the input is valid.

2. Options on the Main Menu
Look Up Flight Details
-Search based on the status of your flight (e.g., Arrived, Delayed)
-Use the airport code to search.
-See every flight.
🔙 Return to Main Menu
✈Details of the flight
-From the results, pick a flight to view:
1- airline and flight number
2-Airports of departure and arrival.
3-Timetable, status, etc.


🌐 Airport List (Sources)
-Sort by ICAO prefix, country, or region.
-Display every airport.
❌ Quit















