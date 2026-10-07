import tkinter as tk
from tkinter import messagebox, filedialog
from validator import validate_ip, validate_network, validate_vlan
from subnet import calculate_subnet
from network_generator import generate_complete_config


# ============================================================
# DATA
# ============================================================

vlans = []


# ============================================================
# FUNCTIONS
# ============================================================

def add_vlan():

    vlan_id = vlan_id_entry.get()
    vlan_name = vlan_name_entry.get()
    interface = vlan_interface_entry.get()

    if not validate_vlan(vlan_id):
        messagebox.showerror(
            "Error",
            "VLAN ID must be between 1 and 4094."
        )
        return

    if not vlan_name:
        messagebox.showerror(
            "Error",
            "Enter VLAN name."
        )
        return

    if not interface:
        messagebox.showerror(
            "Error",
            "Enter interface."
        )
        return

    vlans.append({
        "id": vlan_id,
        "name": vlan_name,
        "interface": interface
    })

    vlan_list.insert(
        tk.END,
        f"VLAN {vlan_id} - {vlan_name} - {interface}"
    )

    vlan_id_entry.delete(0, tk.END)
    vlan_name_entry.delete(0, tk.END)
    vlan_interface_entry.delete(0, tk.END)


def calculate_network():

    network = network_entry.get()

    if not validate_network(network):
        messagebox.showerror(
            "Error",
            "Invalid network. Example: 192.168.10.0/24"
        )
        return

    data = calculate_subnet(network)

    subnet_result.delete("1.0", tk.END)

    subnet_result.insert(
        tk.END,
        f"Network Address : {data['network']}\n"
        f"Broadcast       : {data['broadcast']}\n"
        f"Subnet Mask     : {data['subnet_mask']}\n"
        f"First IP        : {data['first_ip']}\n"
        f"Last IP         : {data['last_ip']}\n"
        f"Usable Hosts    : {data['total_hosts']}"
    )


def generate_config():

    if not vlans:
        messagebox.showerror(
            "Error",
            "Add at least one VLAN."
        )
        return

    interface = router_interface_entry.get()
    ip = router_ip_entry.get()
    mask = router_mask_entry.get()

    if not interface:
        messagebox.showerror(
            "Error",
            "Enter router interface."
        )
        return

    if not validate_ip(ip):
        messagebox.showerror(
            "Error",
            "Invalid IP address."
        )
        return

    if not validate_ip(mask):
        messagebox.showerror(
            "Error",
            "Invalid subnet mask."
        )
        return

    config = generate_complete_config(
        vlans,
        interface,
        ip,
        mask
    )

    output.delete("1.0", tk.END)
    output.insert(tk.END, config)


def save_config():

    config = output.get("1.0", tk.END).strip()

    if not config:
        messagebox.showerror(
            "Error",
            "Generate configuration first."
        )
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[
            ("Text Files", "*.txt"),
            ("All Files", "*.*")
        ]
    )

    if file_path:

        with open(file_path, "w") as file:
            file.write(config)

        messagebox.showinfo(
            "Success",
            "Configuration saved successfully."
        )


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title(
    "Python Network Configuration Generator"
)

root.geometry("950x700")

root.minsize(700, 500)


# ============================================================
# SCROLLBAR SETUP
# ============================================================

# Canvas
canvas = tk.Canvas(
    root,
    highlightthickness=0
)

# Vertical scrollbar
scrollbar = tk.Scrollbar(
    root,
    orient="vertical",
    command=canvas.yview
)

# Frame inside canvas
main_frame = tk.Frame(canvas)


# Create frame inside canvas
canvas_window = canvas.create_window(
    (0, 0),
    window=main_frame,
    anchor="nw"
)


# Connect scrollbar with canvas
canvas.configure(
    yscrollcommand=scrollbar.set
)


# Pack canvas and scrollbar
canvas.pack(
    side="left",
    fill="both",
    expand=True
)

scrollbar.pack(
    side="right",
    fill="y"
)


# ============================================================
# UPDATE SCROLL REGION
# ============================================================

def update_scroll_region(event=None):

    canvas.configure(
        scrollregion=canvas.bbox("all")
    )


main_frame.bind(
    "<Configure>",
    update_scroll_region
)


# ============================================================
# MAKE FRAME WIDTH SAME AS CANVAS
# ============================================================

def resize_frame(event):

    canvas.itemconfig(
        canvas_window,
        width=event.width
    )


canvas.bind(
    "<Configure>",
    resize_frame
)


# ============================================================
# MOUSE WHEEL SCROLL
# ============================================================

def mouse_scroll(event):

    canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )


canvas.bind_all(
    "<MouseWheel>",
    mouse_scroll
)


# ============================================================
# TITLE
# ============================================================

title = tk.Label(
    main_frame,
    text="Network Configuration Generator",
    font=("Arial", 20, "bold")
)

title.pack(
    pady=10
)


# ============================================================
# VLAN SECTION
# ============================================================

vlan_frame = tk.LabelFrame(
    main_frame,
    text="VLAN Configuration",
    padx=10,
    pady=10
)

vlan_frame.pack(
    fill="x",
    padx=15,
    pady=5
)


tk.Label(
    vlan_frame,
    text="VLAN ID"
).grid(
    row=0,
    column=0,
    padx=5,
    pady=5
)


vlan_id_entry = tk.Entry(
    vlan_frame
)

vlan_id_entry.grid(
    row=0,
    column=1,
    padx=5,
    pady=5
)


tk.Label(
    vlan_frame,
    text="VLAN Name"
).grid(
    row=0,
    column=2,
    padx=5,
    pady=5
)


vlan_name_entry = tk.Entry(
    vlan_frame
)

vlan_name_entry.grid(
    row=0,
    column=3,
    padx=5,
    pady=5
)


tk.Label(
    vlan_frame,
    text="Interface"
).grid(
    row=0,
    column=4,
    padx=5,
    pady=5
)


vlan_interface_entry = tk.Entry(
    vlan_frame
)

vlan_interface_entry.grid(
    row=0,
    column=5,
    padx=5,
    pady=5
)


tk.Button(
    vlan_frame,
    text="Add VLAN",
    command=add_vlan
).grid(
    row=0,
    column=6,
    padx=10
)


# VLAN List

vlan_list = tk.Listbox(
    vlan_frame,
    width=90,
    height=6
)

vlan_list.grid(
    row=1,
    column=0,
    columnspan=7,
    pady=10
)


# ============================================================
# SUBNET SECTION
# ============================================================

subnet_frame = tk.LabelFrame(
    main_frame,
    text="Automatic Subnet Calculator",
    padx=10,
    pady=10
)

subnet_frame.pack(
    fill="x",
    padx=15,
    pady=5
)


tk.Label(
    subnet_frame,
    text="Network (Example: 192.168.10.0/24)"
).grid(
    row=0,
    column=0,
    padx=5,
    pady=5
)


network_entry = tk.Entry(
    subnet_frame,
    width=25
)

network_entry.grid(
    row=0,
    column=1,
    padx=5,
    pady=5
)


tk.Button(
    subnet_frame,
    text="Calculate",
    command=calculate_network
).grid(
    row=0,
    column=2,
    padx=10
)


subnet_result = tk.Text(
    subnet_frame,
    height=6,
    width=70
)

subnet_result.grid(
    row=1,
    column=0,
    columnspan=3,
    pady=5
)


# ============================================================
# ROUTER / IP CONFIGURATION
# ============================================================

router_frame = tk.LabelFrame(
    main_frame,
    text="IP Configuration",
    padx=10,
    pady=10
)

router_frame.pack(
    fill="x",
    padx=15,
    pady=5
)


tk.Label(
    router_frame,
    text="Interface"
).grid(
    row=0,
    column=0,
    padx=5,
    pady=5
)


router_interface_entry = tk.Entry(
    router_frame
)

router_interface_entry.grid(
    row=0,
    column=1,
    padx=5,
    pady=5
)


tk.Label(
    router_frame,
    text="IP Address"
).grid(
    row=0,
    column=2,
    padx=5,
    pady=5
)


router_ip_entry = tk.Entry(
    router_frame
)

router_ip_entry.grid(
    row=0,
    column=3,
    padx=5,
    pady=5
)


tk.Label(
    router_frame,
    text="Subnet Mask"
).grid(
    row=0,
    column=4,
    padx=5,
    pady=5
)


router_mask_entry = tk.Entry(
    router_frame
)

router_mask_entry.grid(
    row=0,
    column=5,
    padx=5,
    pady=5
)


# ============================================================
# BUTTON SECTION
# ============================================================

button_frame = tk.Frame(
    main_frame
)

button_frame.pack(
    pady=10
)


tk.Button(
    button_frame,
    text="Generate Configuration",
    command=generate_config,
    width=25
).pack(
    side="left",
    padx=10
)


tk.Button(
    button_frame,
    text="Save Configuration",
    command=save_config,
    width=25
).pack(
    side="left",
    padx=10
)


# ============================================================
# OUTPUT SECTION
# ============================================================

tk.Label(
    main_frame,
    text="Generated Cisco Configuration",
    font=("Arial", 13, "bold")
).pack(
    pady=5
)


output = tk.Text(
    main_frame,
    height=15,
    width=110
)

output.pack(
    padx=15,
    pady=5
)


# ============================================================
# FOOTER
# ============================================================

tk.Label(
    main_frame,
    text="Python-Based Network Configuration Generator",
    font=("Arial", 9)
).pack(
    pady=15
)


# ============================================================
# START GUI
# ============================================================

root.mainloop()