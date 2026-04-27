import json
import os
from collections import deque
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- DATA ----------------
facilities = []
bookings = []
complaints = []
assets = []

# ---------------- MODELS ----------------
class Facility:
    def __init__(self, fid, building, room_type, capacity, floor, coordinates):
        self.fid = fid
        self.building = building
        self.room_type = room_type
        self.capacity = capacity
        self.floor = floor
        self.coordinates = coordinates

    def to_dict(self):
        return self.__dict__

    def __str__(self):
        return f"{self.fid} | {self.building} | {self.room_type} | {self.capacity}"


class Booking:
    def __init__(self, facility_id, purpose, start, end):
        self.facility_id = facility_id
        self.purpose = purpose
        self.start = start
        self.end = end

    def to_dict(self):
        return self.__dict__


class Complaint:
    def __init__(self, cid, facility_id, issue, severity, status="Open"):
        self.cid = cid
        self.facility_id = facility_id
        self.issue = issue
        self.severity = severity
        self.status = status

    def to_dict(self):
        return self.__dict__


class Asset:
    def __init__(self, aid, category, building, room, status):
        self.aid = aid
        self.category = category
        self.building = building
        self.room = room
        self.status = status

    def to_dict(self):
        return self.__dict__


# ---------------- STORAGE ----------------
def save_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def load_data(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as f:
        return json.load(f)


def save_all():
    save_data("facilities.json", [f.to_dict() for f in facilities])
    save_data("bookings.json", [b.to_dict() for b in bookings])
    print("💾 Data Saved")


def load_all():
    global facilities, bookings
    facilities_data = load_data("facilities.json")
    bookings_data = load_data("bookings.json")

    facilities = [Facility(**f) for f in facilities_data]
    bookings = [Booking(**b) for b in bookings_data]


# ---------------- NAVIGATION ----------------
campus_map = {
    "E-Block": ["Library", "Admin"],
    "Library": ["E-Block", "Canteen"],
    "Admin": ["E-Block"],
    "Canteen": ["Library"]
}


def bfs(start, goal):
    queue = deque([[start]])
    visited = set()

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == goal:
            return path

        if node not in visited:
            visited.add(node)
            for neighbor in campus_map.get(node, []):
                queue.append(path + [neighbor])

    return "No path found"


# ---------------- FEATURES ----------------
def add_facility():
    fid = input("ID: ")
    building = input("Building: ")
    room_type = input("Type: ")
    capacity = int(input("Capacity: "))
    floor = int(input("Floor: "))
    coordinates = tuple(map(int, input("Coordinates (x y): ").split()))

    facilities.append(Facility(fid, building, room_type, capacity, floor, coordinates))
    print("✅ Facility Added")


def view_facilities():
    print("\n--- Facilities ---")
    for f in facilities:
        print(f)


def book_facility():
    fid = input("Facility ID: ")
    purpose = input("Purpose: ")
    start = input("Start Time: ")
    end = input("End Time: ")

    for b in bookings:
        if b.facility_id == fid and b.start == start:
            print("❌ Booking Conflict!")
            return

    bookings.append(Booking(fid, purpose, start, end))
    print("✅ Booked Successfully")


def add_complaint():
    cid = input("Complaint ID: ")
    fid = input("Facility ID: ")
    issue = input("Issue: ")
    severity = int(input("Severity (1-5): "))

    complaints.append(Complaint(cid, fid, issue, severity))
    print("✅ Complaint Added")


def add_asset():
    aid = input("Asset ID: ")
    category = input("Category: ")
    building = input("Building: ")
    room = input("Room: ")
    status = input("Status: ")

    assets.append(Asset(aid, category, building, room, status))
    print("✅ Asset Added")


def navigate():
    start = input("Start Location: ")
    end = input("Destination: ")
    print("Path:", bfs(start, end))


# ---------------- ANALYTICS ----------------
def analytics():
    if not bookings:
        print("No booking data")
        return

    df = pd.DataFrame([b.to_dict() for b in bookings])
    result = df.groupby("facility_id").size()

    print("\n--- Usage ---")
    print(result)

    result.plot(kind="bar")
    plt.title("Facility Usage")
    plt.xlabel("Facility")
    plt.ylabel("Bookings")
    plt.show()


# ---------------- MENU ----------------
def menu():
    load_all()

    while True:
        print("\n===== SCN-FMRA SYSTEM =====")
        print("1. Add Facility")
        print("2. View Facilities")
        print("3. Book Facility")
        print("4. Add Complaint")
        print("5. Add Asset")
        print("6. Navigation")
        print("7. Analytics")
        print("8. Save Data")
        print("9. Exit")

        ch = input("Enter choice: ")

        if ch == "1":
            add_facility()
        elif ch == "2":
            view_facilities()
        elif ch == "3":
            book_facility()
        elif ch == "4":
            add_complaint()
        elif ch == "5":
            add_asset()
        elif ch == "6":
            navigate()
        elif ch == "7":
            analytics()
        elif ch == "8":
            save_all()
        elif ch == "9":
            save_all()
            print("Exiting...")
            break
        else:
            print("Invalid choice!")


# ---------------- RUN ----------------
if __name__ == "__main__":
     menu() 
