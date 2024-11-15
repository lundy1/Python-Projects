import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
import socket
import threading

def show_page(page):
    page.tkraise() 

def start_sniffing():
    packet_text.insert(tk.END, "Packet Sniffer not implemented yet.\n")

def scan_ports():
    target_ip = ip_entry.get().strip()
    if not target_ip:
        messagebox.showwarning("Input Error", "Please enter an IP address")
        return

    scan_button.config(state='disabled')
    ip_entry.config(state='disabled')
    port_text.delete(1.0, tk.END) 
    open_ports = []

    def scan():
        try:
            for port in range(1, 1025):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket.setdefaulttimeout(0.5)
                result = sock.connect_ex((target_ip, port))
                if result == 0:
                    open_ports.append(port)
                sock.close()

            port_text.insert(tk.END, f"Open Ports on {target_ip}:\n")
            for port in open_ports:
                port_text.insert(tk.END, f"{port}\n")
        except Exception as e:
            port_text.insert(tk.END, f"Error: {str(e)}\n")
        finally:
            reset_ui()

    threading.Thread(target=scan, daemon=True).start()

def reset_ui():
    ip_entry.config(state='normal')
    scan_button.config(state='normal')

root = tk.Tk()
root.title("Lundy's Multi-Tool")
root.geometry("600x400")

container = tk.Frame(root)
container.pack(fill="both", expand=True)

pages = {}

main_menu = tk.Frame(container)
main_menu.grid(row=0, column=0, sticky="nsew")
main_label = tk.Label(main_menu, text="Lundy's Multi-Tool", font=("Helvetica", 18))
main_label.pack(pady=30)

tools = ["Packet Sniffer", "Port Scanner", "Tool 3", "Tool 4", "Tool 5", "Tool 6"]
button_frame = tk.Frame(main_menu)
button_frame.pack(pady=10)

for i, tool in enumerate(tools):
    btn = tk.Button(button_frame, text=tool, width=12, height=2,
                    command=lambda t=tool: show_page(pages[t]))
    btn.grid(row=i // 3, column=i % 3, padx=10, pady=5) 

pages["Main Menu"] = main_menu  

for i, tool in enumerate(tools):
    page = tk.Frame(container)
    page.grid(row=0, column=0, sticky="nsew")
    label = tk.Label(page, text=f"This is the page for {tool}", font=("Helvetica", 16))
    label.pack(pady=100)

    back_btn = tk.Button(page, text="Back to Main Menu", command=lambda: show_page(main_menu))
    back_btn.pack(pady=10)

    pages[tool] = page 

packet_sniffer = tk.Frame(container)
packet_sniffer.grid(row=0, column=0, sticky="nsew")
label = tk.Label(packet_sniffer, text="Packet Sniffer", font=("Helvetica", 16))
label.pack(pady=10)

start_button = tk.Button(packet_sniffer, text="Start Sniffing", command=start_sniffing)
start_button.pack(pady=10)

packet_text = scrolledtext.ScrolledText(packet_sniffer, width=50, height=10)
packet_text.pack(pady=10)

back_btn = tk.Button(packet_sniffer, text="Back to Main Menu", command=lambda: show_page(main_menu))
back_btn.pack(pady=10)

pages["Packet Sniffer"] = packet_sniffer 

port_scanner = tk.Frame(container)
port_scanner.grid(row=0, column=0, sticky="nsew")
label = tk.Label(port_scanner, text="Port Scanner", font=("Helvetica", 16))
label.pack(pady=10)

ip_label = tk.Label(port_scanner, text="Enter IP Address:")
ip_label.pack(pady=5)
ip_entry = tk.Entry(port_scanner)
ip_entry.pack(pady=5)

scan_button = tk.Button(port_scanner, text="Scan Ports", command=scan_ports)
scan_button.pack(pady=10)

port_text = scrolledtext.ScrolledText(port_scanner, width=50, height=10)
port_text.pack(pady=10)

back_btn = tk.Button(port_scanner, text="Back to Main Menu", command=lambda: show_page(main_menu))
back_btn.pack(pady=10)

pages["Port Scanner"] = port_scanner 

show_page(main_menu)

root.mainloop()
