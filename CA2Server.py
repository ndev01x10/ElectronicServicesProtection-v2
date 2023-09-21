#Imports the various library and module to run the application--------------------------------------------
import socket, datetime, time, os

#This is to clear the command line screen for a neater appearance--------------------------------------------
clear = lambda: os.system('cls')  
clear()

#ANSI Escape Codes to color the text--------------------------------------------
GREEN = "\033[92m"
RESET = "\033[0m"

#Message to notify the creation of socket and process of binding--------------------------------------------
print("=" * 90)
print(f"{GREEN}\t\t\tELECTRONIC SERVICES & PROTECTION SERVER{RESET}")
print("=" * 90)
print('[*] Socket created')
time.sleep(.5)
print('[*] Socket bind complete')
time.sleep(.5)

host = socket.gethostname() 
port = 8089                 

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('0.0.0.0', port))

#Function to check the user login credentials, details are stored in the shadow.jni file where the script reads it from--------------------------------------------
def check_login(user_id, password):
    with open("shadow.jni", "r") as f:
        for line in f:
            uid, pwd = line.strip().split(':')
            if uid == user_id and pwd == password:
                return True
    return False

#Function to verify the authenticated user-------------------------------------------- 
def handle_request(con, command):
    if command.startswith("login:"):
        user_id, password = command.split(':', 2)[1:]  #Split command to get User ID and password
        if check_login(user_id, password):
            con.send("Login successful".encode())
            return user_id, True
        else:
            con.send("Login failed".encode())
    return None, False

print(f"[*] Server now listening on {host} at port: {port} on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 90)
serversocket.listen(5)

user_id = None #This will store the authenticated user ID

while True:
    con, address = serversocket.accept()
    print(f">> New connection established from {address}...")

    authenticated = False
    while True: #Nested loop to handle multiple interactions
        buf = con.recv(1024)
        if len(buf) > 0:
            received_data = buf.decode()
            print(received_data)

            if received_data.startswith("login:"):
                user_id, authenticated = handle_request(con, received_data)

            elif received_data == '[*] Data request from client':
                if authenticated: #Check if the user is authenticated
                    transaction_filename = f"{user_id}transactions.jni" #Build the filename based on User ID if its not presently created
                    with open(transaction_filename, 'r') as f:
                        data = f.read()
                        con.send(data.encode())
                else:
                    con.send("You need to authenticate first.".encode())

            elif received_data == 'x':
                con.close()
                break #This breaks the inner loop, ending the connection

    #This is to break the outer loop when a client shuts down the server
    if received_data == 'x':
        break 

#Closing the socket--------------------------------------------  
serversocket.close()
print(f"[*] Server has stopped at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("[*] Closing server now")
print("=" * 90)
time.sleep(.5)

#################### Credits and References ####################

# https://realpython.com/python-sockets/
# https://www.geeksforgeeks.org/socket-programming-python/
