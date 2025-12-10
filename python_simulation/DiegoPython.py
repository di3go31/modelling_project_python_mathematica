import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import hashlib
import json
import os
import random


def ai_decision(ai_troops, player_troops):
    """
    AI determines whether to attack, defend, or reinforce based on troop strength.
    """
    decision = {}
    for front in ai_troops:
        if ai_troops[front] > player_troops[front] * 1.5:
            decision[front] = "Attack"
        elif ai_troops[front] < player_troops[front] * 0.75:
            decision[front] = "Defend"
        else:
            decision[front] = "Reinforce"
    return decision

# ------------------ File for User Data Storage ------------------
USER_DATA_FILE = "military_users.json"

# ------------------ Load Users from JSON ------------------
def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            try:
                return json.load(file)  # Load user data from JSON
            except json.JSONDecodeError:
                return {}  # Reset if file is corrupted
    return {}

# ------------------ Save Users to JSON ------------------
def save_users():
    with open(USER_DATA_FILE, "w") as file:
        json.dump(users, file, indent=4)

# ------------------ Hash Passwords for Security ------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ------------------ User Data (Loaded at Startup) ------------------
users = load_users()

# ------------------ Open Main Menu ------------------
def open_main_menu(player_name, role):
    main_menu = tk.Tk()
    main_menu.title("Military Strategy Simulator")
    main_menu.geometry("800x600")

    tk.Label(main_menu, text=f"Welcome, {player_name}! Role: {role}", font=("Arial", 18)).pack(pady=10)

    if role == "Commander":
        tk.Button(main_menu, text="Allocate Resources", font=("Arial", 14), command=lambda: commander_task(player_name)).pack(pady=5)

    tk.Button(main_menu, text="Logout", font=("Arial", 14), command=main_menu.destroy).pack(pady=5)

    main_menu.mainloop()

# ------------------ Commander Task: Allocating Resources ------------------
def commander_task(player_name):
    battlefronts = ["Northern Front", "Eastern Front", "Southern Front"]
    allocated_troops = {}

    for front in battlefronts:
        troops = simpledialog.askinteger("Allocate Troops", f"Enter troops for {front} (1-{users[player_name]['progress']['troops_available']}):", minvalue=1, maxvalue=users[player_name]["progress"]["troops_available"])
        
        if troops is not None:
            allocated_troops[front] = troops
            users[player_name]["progress"]["troops_available"] -= troops

    users[player_name]["progress"]["allocated_troops"] = allocated_troops
    save_users()

    messagebox.showinfo("Resources Allocated", f"You allocated troops across multiple battlefronts.")
    
    # 📌 Open the next page (Command Center)
    command_center(player_name)


# ------------------ Commander Control Center ------------------


def command_center(player_name):
    center_window = tk.Toplevel()
    center_window.title("Commander Control Center")
    center_window.geometry("600x900")

    tk.Label(center_window, text=f"Commander: {player_name}", font=("Arial", 16)).pack(pady=10)
    tk.Label(center_window, text="Current Troop Allocations:", font=("Arial", 14)).pack(pady=5)

    allocations = users[player_name]["progress"]["allocated_troops"]
    if not allocations or sum(allocations.values()) == 0:
        tk.Label(center_window, text="No troops allocated yet.", font=("Arial", 12)).pack()
        return  # Stop here if no troops are deployed

    for front, troops in allocations.items():
        frame = tk.Frame(center_window)
        frame.pack(pady=5)

        tk.Label(frame, text=f"{front}: {troops} troops", font=("Arial", 12)).pack(side=tk.LEFT)
        tk.Button(frame, text="➕ Reinforce", command=lambda f=front: reinforce_troops(player_name, f)).pack(side=tk.RIGHT)
        tk.Button(frame, text="➖ Withdraw", command=lambda f=front: withdraw_troops(player_name, f)).pack(side=tk.RIGHT)

    # 📌 Military Strategy Formulas
    tk.Label(center_window, text="\nMilitary Strategy Formulas:", font=("Arial", 14, "bold")).pack(pady=10)
    formulas = [
        "Lanchester’s Square Law: dA/dt = -βB,  dB/dt = -αA",
        "Reinforcement Model: N(t) = N0 * e^(r*t)",
        "Combat Efficiency: E = (Morale * Training Level) / (Fatigue + Casualties)",
        "Logistics Demand: Supplies Needed = (Troops * 2.5 kg food) + (Ammo * Fire Rate)"
    ]
    for formula in formulas:
        tk.Label(center_window, text=formula, font=("Arial", 11)).pack()





    # 🌦️ Weather Effect (before logistics report)
    weather = random.choice(["Clear", "Rain", "Fog", "Storm"])
    tk.Label(center_window, text=f"🌦️ Current Weather: {weather}", font=("Arial", 12, "bold")).pack(pady=5)

    # Optional effect on supplies or movement
    if weather == "Storm":
        tk.Label(center_window, text="⚠️ Supplies delayed due to heavy storms!", fg="red", font=("Arial", 11)).pack()
    

   
    
    

    # 📌 Logistics Report
    tk.Label(center_window, text="\n📦 Logistics Report", font=("Arial", 14, "bold")).pack()
    total_troops = sum(allocations.values())
    logistics_text = f"""
    Total Troops Deployed: {total_troops}
    - Daily Food Requirement: {total_troops * 2.5} kg
    - Estimated Ammo Consumption: {total_troops * random.randint(3, 7)} rounds
    - Fuel Required: {total_troops * 1.2} liters
    """
    tk.Label(center_window, text=logistics_text, font=("Arial", 12)).pack()

    # 📌 Supply Chain Risk
    supply_risk = random.choice(["Low", "Moderate", "High", "Critical"])
    tk.Label(center_window, text=f"⚠️ Supply Chain Risk Level: {supply_risk}", font=("Arial", 12, "bold")).pack(pady=5)
    if supply_risk in ["High", "Critical"]:
        response = messagebox.askyesno("⚠️ Supply Warning", f"Supply risk is {supply_risk}! Do you want to send emergency supplies?")
        if response:
            resupply_decision(player_name)

    # 📌 BUTTONS TO MOVE FORWARD
    button_frame = tk.Frame(center_window)
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="Manage Emergency Supplies", font=("Arial", 14), command=lambda: resupply_decision(player_name)).pack(pady=5)
    tk.Button(button_frame, text="Strategic Deployment", font=("Arial", 14), command=lambda: adjust_troop_deployment(player_name)).pack(pady=5)
    tk.Button(button_frame, text="View Battlefield Attrition", font=("Arial", 14), command=lambda: battlefield_attrition(player_name)).pack(pady=5)
    tk.Button(button_frame, text="Finalize Deployment", font=("Arial", 14), command=lambda: finalize_deployment(player_name)).pack(pady=15)


    # 📌 Move to Strategic Planning
    tk.Button(center_window, text="📊 Strategic Planning", font=("Arial", 14), command=lambda: strategic_planning(player_name)).pack(pady=10)

    # 📌 Move to Battle Simulation
    tk.Button(center_window, text="⚔️ Start Battle Simulation", font=("Arial", 14), command=lambda: start_battle_simulation(player_name)).pack(pady=10)


def launch_battle_simulation():
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    from mpl_toolkits.mplot3d import Axes3D
    import time

    # Simulation Parameters
    num_units_blue = 100
    num_units_red = 300
    battlefield_size = 10
    fight_radius = 1.5
    step_size = 0.2
    terrain_variation = 2
    reinforcement_rate_blue = 0.02 * num_units_blue
    reinforcement_rate_red = 0.03 * num_units_red
    alpha = 0.002
    beta = 0.001

    blue_units = np.column_stack((np.random.rand(num_units_blue, 2) * battlefield_size, 
                                  np.random.rand(num_units_blue) * terrain_variation))
    red_units = np.column_stack((np.random.rand(num_units_red, 2) * battlefield_size, 
                                 np.random.rand(num_units_red) * terrain_variation))

    def engage_units(blue_units, red_units, frame):
        nonlocal num_units_blue, num_units_red

        blue_casualties = int(beta * len(red_units))
        red_casualties = int(alpha * len(blue_units))

        if len(blue_units) > 0:
            blue_units = np.delete(blue_units, np.random.choice(len(blue_units), min(blue_casualties, len(blue_units)), replace=False), axis=0)
        if len(red_units) > 0:
            red_units = np.delete(red_units, np.random.choice(len(red_units), min(red_casualties, len(red_units)), replace=False), axis=0)

        new_blue_units = np.column_stack((np.random.rand(int(reinforcement_rate_blue), 2) * battlefield_size, 
                                          np.random.rand(int(reinforcement_rate_blue)) * terrain_variation))
        new_red_units = np.column_stack((np.random.rand(int(reinforcement_rate_red), 2) * battlefield_size, 
                                         np.random.rand(int(reinforcement_rate_red)) * terrain_variation))

        blue_units = np.vstack((blue_units, new_blue_units))
        red_units = np.vstack((red_units, new_red_units))

        if frame % 20 == 0:
            print("\n--------------------------------------------------")
            print(f"🪖 **Battle Report at Frame {frame}** 🪖")
            print(f"🔵 U.S. Forces Remaining: {len(blue_units)}")
            print(f"🔴 PAVN Forces Remaining: {len(red_units)}")
            if blue_casualties > red_casualties:
                print("💥 The U.S. is losing troops faster. Reinforcements are crucial.")
            elif red_casualties > blue_casualties:
                print("🔥 PAVN forces are taking heavier losses, but their reinforcements are sustaining them.")
            if len(blue_units) < 50:
                print("⚠️ The U.S. is critically low on troops. Air support is needed!")
            elif len(red_units) < 150:
                print("🛑 PAVN forces are shrinking, but they still have numbers.")
            time.sleep(3)

        if len(blue_units) == 0:
            print("⚠️ U.S. Forces have been **defeated**! The PAVN controls the battlefield.")
            time.sleep(5)
        elif len(red_units) == 0:
            print("✅ The U.S. Forces have **won**! PAVN forces are retreating.")
            time.sleep(5)

        return blue_units, red_units

    def move_units(units, enemy_units):
        for i, unit in enumerate(units):
            distances = np.linalg.norm(enemy_units[:, :2] - unit[:2], axis=1)
            if len(distances) > 0:
                closest_enemy = enemy_units[np.argmin(distances)]
                direction = closest_enemy[:2] - unit[:2]
                if np.linalg.norm(direction) > 0:
                    units[i, :2] += step_size * direction / np.linalg.norm(direction)
        return units

    def update(frame):
        nonlocal blue_units, red_units
        ax.clear()
        blue_units = move_units(blue_units, red_units)
        red_units = move_units(red_units, blue_units)
        blue_units, red_units = engage_units(blue_units, red_units, frame)

        ax.set_xlim(0, battlefield_size)
        ax.set_ylim(0, battlefield_size)
        ax.set_zlim(0, terrain_variation)
        ax.set_xlabel("X Position (km)")
        ax.set_ylabel("Y Position (km)")
        ax.set_zlabel("Elevation (km)")
        ax.set_title(f"Battle of Ia Drang Valley - Frame {frame}")
        ax.scatter(blue_units[:, 0], blue_units[:, 1], blue_units[:, 2], color='blue', label='U.S. Army (Blue)')
        ax.scatter(red_units[:, 0], red_units[:, 1], red_units[:, 2], color='red', label='PAVN Forces (Red)')
        ax.legend()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ani = FuncAnimation(fig, update, frames=200, interval=100)
    plt.show()

    print("\n--------------------------------------------------")
    print("🏆 **Final Battle Report** 🏆")
    if len(blue_units) > len(red_units):
        print("✅ The U.S. Forces **secured victory** after sustained combat.")
    elif len(red_units) > len(blue_units):
        print("⚠️ The PAVN **controlled the battlefield** and forced the U.S. to withdraw.")
    else:
        print("🔄 The battle ended in a **stalemate**, with heavy losses on both sides.")


def strategic_planning(player_name):
    # Any setup code for the strategic planning window if needed

    # Launch the simulation
    launch_battle_simulation()


def reinforce_troops(player_name, front):
    amount = simpledialog.askinteger("Reinforce Troops", f"Enter number of troops to send to {front}:", minvalue=1, maxvalue=users[player_name]["progress"]["troops_available"])
    if amount:
        users[player_name]["progress"]["allocated_troops"][front] += amount
        users[player_name]["progress"]["troops_available"] -= amount
        save_users()
        messagebox.showinfo("Reinforcement Sent", f"{amount} troops sent to {front}.")
        command_center(player_name)  # Refresh UI

def withdraw_troops(player_name, front):
    amount = simpledialog.askinteger("Withdraw Troops", f"Enter number of troops to withdraw from {front}:", minvalue=1, maxvalue=users[player_name]["progress"]["allocated_troops"][front])
    if amount:
        users[player_name]["progress"]["allocated_troops"][front] -= amount
        users[player_name]["progress"]["troops_available"] += amount
        save_users()
        messagebox.showinfo("Troops Withdrawn", f"{amount} troops withdrawn from {front}.")
        command_center(player_name)  # Refresh UI


def adjust_troop_deployment(player_name):
    allocations = users[player_name]["progress"]["allocated_troops"]
    
    if not allocations or sum(allocations.values()) == 0:
        messagebox.showinfo("Strategic Deployment", "No troops are currently allocated to redeploy.")
        return

    from_front = simpledialog.askstring("Strategic Deployment", "Enter the front to move troops from (e.g., Northern Front):")
    to_front = simpledialog.askstring("Strategic Deployment", "Enter the front to move troops to (e.g., Eastern Front):")

    if from_front not in allocations or to_front not in allocations:
        messagebox.showerror("Error", "Invalid front name. Please enter a valid battlefront.")
        return

    amount = simpledialog.askinteger("Strategic Deployment", f"Enter number of troops to move from {from_front} to {to_front}:", minvalue=1, maxvalue=allocations[from_front])

    if amount:
        allocations[from_front] -= amount
        allocations[to_front] += amount
        save_users()
        messagebox.showinfo("Deployment Update", f"Moved {amount} troops from {from_front} to {to_front}.")
        command_center(player_name)  # Refresh UI


# ------------------ Battlefield Attrition Report ------------------
def battlefield_attrition(player_name):
    battlefronts = users[player_name]["progress"]["allocated_troops"]
    attrition_report = "⚔️ Battlefield Attrition Report:\n"

    total_losses = 0
    for front, troops in battlefronts.items():
        battle_intensity = random.uniform(0.05, 0.25)  # Random intensity level (5%-25% loss per day)
        losses = int(troops * battle_intensity)  # Apply attrition model
        total_losses += losses
        attrition_report += f"- {front}: Lost {losses} troops ({battle_intensity*100:.1f}% intensity)\n"

        # Update remaining troops
        users[player_name]["progress"]["allocated_troops"][front] -= losses

    save_users()

    messagebox.showinfo("Attrition Report", f"{attrition_report}\nTotal Troops Lost: {total_losses}")

    # 📌 Offer reinforcement if losses are high
    if total_losses > 100:  
        reinforce_troops(player_name)

    # 🔹 Refresh UI after attrition
    command_center(player_name)


def open_emergency_supplies_window(player_name):
    window = tk.Toplevel()
    window.title("Manage Emergency Supplies")
    window.geometry("500x400")

    tk.Label(window, text="Emergency Supplies Management", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(window, text="Allocate additional food, ammunition, and fuel.", font=("Arial", 12)).pack(pady=5)

    # Close button
    tk.Button(window, text="Close", font=("Arial", 12), command=window.destroy).pack(pady=20)


def open_strategic_deployment_window(player_name):
    window = tk.Toplevel()
    window.title("Strategic Deployment")
    window.geometry("500x400")

    tk.Label(window, text="Strategic Troop Deployment", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(window, text="Move troops between battlefronts.", font=("Arial", 12)).pack(pady=5)

    # Close button
    tk.Button(window, text="Close", font=("Arial", 12), command=window.destroy).pack(pady=20)


def open_battlefield_attrition_window(player_name):
    window = tk.Toplevel()
    window.title("Battlefield Attrition")
    window.geometry("500x400")

    tk.Label(window, text="Battlefield Attrition Analysis", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(window, text="Simulate combat losses and evaluate troop conditions.", font=("Arial", 12)).pack(pady=5)

    # Close button
    tk.Button(window, text="Close", font=("Arial", 12), command=window.destroy).pack(pady=20)


def open_strategic_planning_window(player_name):
    window = tk.Toplevel()
    window.title("Strategic Planning")
    window.geometry("500x400")

    tk.Label(window, text="Strategic Planning Dashboard", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(window, text="Analyze past battles and optimize future strategies.", font=("Arial", 12)).pack(pady=5)

    # Close button
    tk.Button(window, text="Close", font=("Arial", 12), command=window.destroy).pack(pady=20)


def open_battle_simulation_window(player_name):
    window = tk.Toplevel()
    window.title("Battle Simulation")
    window.geometry("500x400")

    tk.Label(window, text="Battle Simulation", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(window, text="Run a simulated battle based on troop deployments and strategy.", font=("Arial", 12)).pack(pady=5)

    # Close button
    tk.Button(window, text="Close", font=("Arial", 12), command=window.destroy).pack(pady=20)


# ------------------ Finalize Deployment ------------------
def finalize_deployment(player_name):
    messagebox.showinfo("Deployment Finalized", f"Troop allocations have been confirmed.\nPrepare for strategic evaluation.")
    # 🔹 Next step: Generate battle scenarios, simulate logistics.


# ------------------ Resupply Decision ------------------
def resupply_decision(player_name):
    resupply = messagebox.askyesno("Resupply Decision", "Your supply chain is under stress. Do you want to allocate emergency supplies?")
    
    if resupply:
        extra_supplies = simpledialog.askinteger("Emergency Supplies", "Enter additional food (kg):", minvalue=0, maxvalue=500)
        extra_ammo = simpledialog.askinteger("Emergency Supplies", "Enter additional ammo (rounds):", minvalue=0, maxvalue=2000)
        
        messagebox.showinfo("Resupply Completed", f"Emergency supplies allocated:\nFood: {extra_supplies} kg\nAmmo: {extra_ammo} rounds")
    else:
        messagebox.showwarning("Supply Risk", "Without resupply, troops may suffer starvation or low combat effectiveness.")


import pygame

def start_battle_simulation(player_name):
    # Initialize Pygame window
    WIDTH, HEIGHT = 1000, 800
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Battle Simulation")

    # Load background image
    BG = pygame.image.load("WorldMap.png")
    BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

    # Initialize dots (units)
    player_units = [(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)) for _ in range(100)]
    enemy_units = [(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)) for _ in range(100)]

    # AI Movement Logic
    def move_units(units):
        new_positions = []
        for x, y in units:
            dx, dy = random.randint(-5, 5), random.randint(-5, 5)  # Small movements
            new_x = max(50, min(WIDTH - 50, x + dx))
            new_y = max(50, min(HEIGHT - 50, y + dy))
            new_positions.append((new_x, new_y))
        return new_positions

    # Game loop
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)  # Run at 60 FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        WIN.blit(BG, (0, 0))  # Draw background

        # Update positions using AI movement function
        player_units = move_units(player_units)
        enemy_units = move_units(enemy_units)

        # Draw player units (blue)
        for x, y in player_units:
            pygame.draw.circle(WIN, (0, 0, 255), (x, y), 3)  

        # Draw enemy units (red)
        for x, y in enemy_units:
            pygame.draw.circle(WIN, (255, 0, 0), (x, y), 3)

        pygame.display.update()

    pygame.quit()

    # 👉 Transition to Tkinter battle simulation
    battle_simulation(player_name)

# ------------------ Start Login Window ------------------


open_main_menu("Commander", "Commander")

