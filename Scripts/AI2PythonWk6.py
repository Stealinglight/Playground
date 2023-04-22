# --- Goal ---
# Create a program that can create a record for an AR, 
# and track their last maintenance date

# import statement for datetime
import datetime

# --- Create empty list for future active robots ---
in_service = []

# --- Create the class with name ar_bot ---
# ---   With the attributes ---
# - 1. id                     -
# - 2. job                    -
# - 3. maintenance_date       -
# -----------------------------
class ar_bot:
    def __init__(self, id, job, maintenance_date):
        self.id = id
        self.job = job
        self.maintenance_date = maintenance_date


# --- Create the maintenance function ---
# ---------------------------------------
# -            Description              -
# - The maintenance function simply     -
# - outputs that maintenance is done @  -
# - a specific time. Hint: That time    -
# - can be datetime.datetime.now        -
# ---------------------------------------
def maintenance(self):
    print("Doing Maintenance...\nMaintenance Done")
    self.maintenance_date = datetime.datetime.now


# --- Create the AR Creation function ---
# ---------------------------------------
# -            Description              -
# - The ar creation function takes input-
# - for the following things:           -
# - 1. id                               -
# - 2. responsibility                   -
# - After taking input it assigns the   -
# - values to new_bot using the class   -
# ---------------------------------------
def ar_creation(): 
    id = int(input("Please enter an ID: "))
    responsibility = input("Please enter a job: ")
    new_bot = ar_bot(id, responsibility)
    return new_bot

# --- Create the view_bots function ---
def view_bots():
    print("Listing ARs in service")
    for ar in in_service:
        print("AR- " + str(ar.id) + "Job :" + str(ar.responsibilty) + "Maintenance: " + str(ar.maintenance_date))


# --- Create the servicing function ---
def servicing(id):
    ar_found == False
    for ar in in_service:
        if ar.id == id:
            # AR-19 is being maintained
            print("AR-" + str(ar.id) + " is being maintained :elmo-fire:")
            ar.maintenance()
            ar_found == True
        if ar_found == False:
            print("AR not found, try again after you restart AWS :elmo-fire:")
    
        
# --- Create the menu function ---
def menu():
    """
    This function will print the menu options using 
    a while loop and return the user's selection
    as well as validating the user's input.
    """
    while True:
        # Display the menu options
        print("1. Create AR")
        print("2. View ARs")
        print("3. Service AR")
        print("4. Exit")
        # Input function used to get user's selection
        selection = input("Select an option: ")

        # Input validation and error handling
        if selection in ["1", "2", "3", "4"]:
            return selection
        else:
            print("Invalid option, please try again.")
       



# ---  Finally, create the main function   ---
# --- This is what brings it all together  ---
def main():
    menu()
    new_bot = ar_creation()
    in_service.append(new_bot)
    view_bots()
    servicing(19)
    view_bots()

# Used to call main function is run from CLI
if __name__ == "__main__":
    main()
    