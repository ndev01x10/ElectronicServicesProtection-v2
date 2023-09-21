#Imports the various library and module to run the application--------------------------------------------
import datetime, time, os, socket, hashlib

#This is to clear the command line screen for a neater appearance--------------------------------------------
clear = lambda: os.system('cls')  
clear()

#ANSI Escape Codes to color the text--------------------------------------------
RED_START = "\033[91m"
COLOR_END = "\033[0m"
GREEN = "\033[92m"
RESET = "\033[0m"

#Message to present to the user--------------------------------------------
def message():
    print("=" * 90)
    print(f"{GREEN}\t\t\t\t\tWELCOME TO{RESET}")
    print(f"{GREEN}\t\t\tELECTRONIC SERVICES & PROTECTION (ESP2){RESET}")
    print("=" * 90)

#Function for a simple login mechanism, password is hashed in md5 format, details encoded and sent to the server-------------------------------------------
def login():
    while True:
        message()
        user_id = input("Please enter your User ID: ")
        password = hashlib.md5(input("Please enter your password: ").encode()).hexdigest()  # hash entered password
        mbytes = f"login:{user_id}:{password}".encode()  # send user id with hashed password
        clientsocket.send(mbytes)
        buf = clientsocket.recv(255)
        if buf.decode() == "Login successful":
            return user_id
        print("You have entered an invalid User ID or password! Please try again.")
        time.sleep(.5)
        clear()
 
clientsocket = socket.socket()
clientsocket.connect(('localhost', 8089))

user_id = login()
clear()

#The available services are being stored in services {} dictionary-------------------------------------------
services = {
    1: {'name': 'Firewall Service', 'price': 1.2},
    2: {'name': 'Security Ops Centre', 'price': 4.2},
    3: {'name': 'Hot Site', 'price': 8.5},
    4: {'name': 'Data Protection', 'price': 10.0}
}

subscriptions = {}

#This is the main function of the ELECTRONIC SERVICES & PROTECTION 2 application-------------------------------------------
def main():
    user_input = '0' 
    subscribed_services = [] 

    #Since user_input has been defined as '0' and while loop condition is != '7', the main menu will be printed everytime
    while user_input != '7':
        message()
        print("1. Display our list of services")
        print("2. Search for a service")
        print("3. Display added services")
        print("4. Remove service(s)")
        print("5. Payment")
        print("6. Display Service(s) currenly subscribed")
        print("7. Exit Electronic Services & Protection\n")

        #User_input variable will now be updated to whichever option the user selects
        user_input = input("Please input your choice of action or select 7 to exit: ") 

        if user_input == '1':
            clear()
            message()
            displayServices() 
            subscribeService(services, subscribed_services, subscriptions)
        elif user_input == '2':
            clear()
            message()
            searchService(services)
            subscribeService(services, subscribed_services, subscriptions)
        elif user_input == '3':
            clear()
            message()
            displaySubscribedServices(subscribed_services, subscriptions)
        elif user_input == '4':
            clear()
            message()
            removeService(subscribed_services) 
        elif user_input == '5':
            clear()
            message()
            calculatePayment(user_id, subscribed_services, services) 
        elif user_input == '6':
            clear()
            message()
            handle_client_interaction(clientsocket)
        elif user_input == '7':
            clear()
            message()
            print("\nThank you for using Electronic Services & Protection (ESP2). It has been a pleasure serving you!\n")
            time.sleep(.5)
        else:
            clear()
            print("[Invalid choice. Please enter a valid option!]\n")

#This function dislpays the available services of the application. The details are manually listed in order to present uniformity-------------------------------------------
def displayServices():
    print("Thank you for selecting this option. Yes, we have the following service(s): ")
    print("1. Firewall Service     :        $1.2k/year")
    print("2. Security Ops Centre  :        $4.2k/year")
    print("3. Hot Site             :        $8.5k/year")
    print("4. Data Protection      :        $10.0k/year")

# This function allows the user to search for services available within the application using keyword search. It is coded in away that keyword case sensitivity does not apply-------------------------------------------
def searchService(services):
    keyword = input("Enter the keyword to search for a service: \n") 
    found = False 
    for service_id, service_details in services.items(): 
        if keyword.lower() in service_details['name'].lower(): 
            print(f"Service ID: {service_id}\tService Name: {service_details['name']} : ${service_details['price']}k/year\t")
            found = True

    if not found:
        print("\n[No service(s) found matching the keyword!]\n") 

#This function displays the subscribed services of the user-------------------------------------------
def displaySubscribedServices(subscribed_services, subscriptions):
    clear()
    if len(subscribed_services) == 0: #The script will check the subscribed_services[] array if there are stored input, if there is none, the script will notify the user they have not subscribed to any services yet
        print("[You have not subscribed  to any service(s) yet!]\n") 
    else:
        print("\nYour subscribed services:") 
        for index, service_id in enumerate(subscribed_services): 
            service_details = services[service_id] 
            expiry_date = subscriptions[service_id] 
            print(f"{index + 1}. Service ID: {service_id}\tService Name: {service_details['name']} : ${service_details['price']}k/year\tExpiry Date: {expiry_date}") 

# This function prompts the user to select from the available services they would like to subscribe-------------------------------------------
def subscribeService(services, subscribed_services, subscriptions):
    while True: #Using while loop, the script runs without any conditions until the break is executed in the loop
        service_id = input("Enter the service 1-4 that you would like to add, 0 to stop: ") 
        if service_id == '0': #If the selected option is '0', the argument states to break the loop
            break
        try:
            clear()
            message()
            service_id = int(service_id) 
            if service_id not in services:
                raise ValueError("Please enter a valid service ID.") 
            subscribed_services.append(service_id) 
            expiry_date = calculateExpiryDate() 
            subscriptions[service_id] = expiry_date
            print(f"[Service option {service_id}] subscribed successfully! Expiry Date: {expiry_date}\n") #The subscribed service(s) is presented to the user which includes its expiry date (1year)
        except ValueError:
            print("[Invalid choice! Please enter 1-4 or 0 to stop.]\n")
        
#This function allows the user to remove any services they have added into their cart-------------------------------------------
def removeService(subscribed_services):
    clear()
    if len(subscribed_services) == 0: #The script will check the subscribed_services[] array if there are stored input, if there is none, the script will notify the user they have not subscribed to any services yet
        print("[You have not subscribed to any service(s) yet!]\n") 
        return

    print("Your subscribed services:") 
    for index, service_id in enumerate(subscribed_services):
        service_details = services[service_id]
        print(f"{index + 1}. Service ID: {service_id}\tService Name: {service_details['name']}") 

    while True: #Using while loop, the script runs without any conditions until the break is executed in the loop
        service_index = input("Enter the index number of the service you want to remove, 0 to cancel: ") 
        if service_index == '0': #If the selected option is '0', the argument states to break the loop
            break 
        try: 
            service_index = int(service_index) 
            if service_index < 1 or service_index > len(subscribed_services):
                raise ValueError("INVALID INDEX. PLEASE ENTER A VALID INDEX NUMBER!\n") 

            removed_service_id = subscribed_services.pop(service_index - 1) #Using .pop(), it allows to returns the item present in the given index from subscribed_services and subtracts from service_index as per the defined condition
            removed_service_name = services[removed_service_id]['name']
            del subscriptions[removed_service_id]
            print(f"Service '{removed_service_name}' (ID: {removed_service_id}) removed successfully!\n") 
            break
        except ValueError:
            print("[INVALID CHOICE! PLEASE ENTER A VALID INDEX NUMBER!\n") 

#This function tabulates the total amount of the services subscribed-------------------------------------------
def calculatePayment(user_id, subscribed_services, services):
    clear()
    if len(subscribed_services) == 0:
        print("[You have not subscribed to any service(s) yet!]\n")
    else:
        total_price = 0 
        for service_id in subscribed_services:
            service_details = services[service_id] 
            total_price += service_details['price'] 
        
        if len(subscribed_services) == len(services):
            discount = 0.1
            discounted_price = total_price * (1 - discount)
            discounted_price = round(discounted_price, 2)
            print(f"\nTotal payment amount: ${discounted_price:.2f}k/year") 
            print("\nCongratulations! You have selected all subscriptions and received a 10% discount.")
        else:
            total_price = round(total_price, 2)
            print(f"\nTotal payment amount: ${total_price:.2f}k/year\n")
            print(f"User {user_id} subscribed to service(s): {subscribed_services}")

    update_user_subscriptions(user_id, subscribed_services, services)
    subscribed_services.clear()
    subscriptions.clear()

#Function to update the user transaction file. Subscribed services of the authenticated user will be update accordingly into their respective transactions.jni file.-------------------------------------------
def update_user_subscriptions(user_id, subscribed_services, services):

    filename = f"{user_id}transactions.jni"
    
    with open(filename, 'a') as f: #Opens up the transaction file and appends the details
        for service_id in subscribed_services:
            service_details = services[service_id]
            service_name = service_details['name']  #Assuming each service has a 'name' key
            service_price = service_details['price']  #Assuming each service has a 'price' key

            expiry_date_for_service = subscriptions[service_id]
            current_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            f.write(f"Service ID: {service_id}, Name: {service_name}, Price: ${service_price:.2f}k/year, {RED_START}Expiry Date:{expiry_date_for_service}{COLOR_END}, Timestamp: {current_timestamp}\n")

#This function calculates the expiry date of the subscribed services-------------------------------------------
def calculateExpiryDate():
    current_datetime = datetime.datetime.now()
    current_date = current_datetime.date()
    expiry_date = current_date + datetime.timedelta(days=365)
    return expiry_date

def handle_client_interaction(clientsocket):
    msg = '[*] Data request from client'#Automatically request the transaction file

    mbytes = msg.encode() #Encode unicode str to bytes before sending out
    clientsocket.send(mbytes)

    #Receive the data from the server
    data = clientsocket.recv(1024)
    print("\nYou have currently subscribed to:\n", data.decode())

    input("\nPress any key to continue...")  #Pause the application until any key is pressed
    clear()

    #clientsocket.close()

#Calling out the main function in order for the application to run
main()

#################### Credits and References ####################

# https://realpython.com/python-sockets/
# https://www.geeksforgeeks.org/socket-programming-python/