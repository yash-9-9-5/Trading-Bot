import tkinter as tk
from tkinter import ttk, scrolledtext
import sys
import threading

class RedirectText(object): 
    def __init__(self, text_widget):
        self.output = text_widget

    def write(self, string):
        self.output.insert(tk.END, string)
        self.output.see(tk.END)

    def flush(self):
        pass

from bot.client import MockClient
from bot.orders import OrderManager

class TradingBotUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mock Trading Bot (No API Keys)")
        self.root.geometry("500x600")
        self.root.configure(padx=20, pady=20)

        style = ttk.Style()
        style.configure("TLabel", padding=5, font=("Arial", 10))
        style.configure("TButton", padding=5, font=("Arial", 10, "bold"))
        style.configure("TEntry", padding=5)

        self.create_widgets()

    def create_widgets(self):
        # --- Order Frame ---
        order_frame = ttk.LabelFrame(self.root, text="Mock Order Details", padding=10)
        order_frame.pack(fill="x", pady=10)

        ttk.Label(order_frame, text="Symbol:").grid(row=0, column=0, sticky="w")
        self.symbol_entry = ttk.Entry(order_frame)
        self.symbol_entry.insert(0, "BTCUSDT")
        self.symbol_entry.grid(row=0, column=1, pady=5, sticky="w")

        ttk.Label(order_frame, text="Side:").grid(row=1, column=0, sticky="w")
        self.side_var = tk.StringVar(value="BUY")
        side_combo = ttk.Combobox(order_frame, textvariable=self.side_var, values=["BUY", "SELL"], state="readonly")
        side_combo.grid(row=1, column=1, pady=5, sticky="w")

        ttk.Label(order_frame, text="Type:").grid(row=2, column=0, sticky="w")
        self.type_var = tk.StringVar(value="MARKET")
        type_combo = ttk.Combobox(order_frame, textvariable=self.type_var, values=["MARKET", "LIMIT"], state="readonly")
        type_combo.grid(row=2, column=1, pady=5, sticky="w")

        ttk.Label(order_frame, text="Quantity:").grid(row=3, column=0, sticky="w")
        self.qty_entry = ttk.Entry(order_frame)
        self.qty_entry.insert(0, "0.01")
        self.qty_entry.grid(row=3, column=1, pady=5, sticky="w")

        ttk.Label(order_frame, text="Price (Limit):").grid(row=4, column=0, sticky="w")
        self.price_entry = ttk.Entry(order_frame)
        self.price_entry.grid(row=4, column=1, pady=5, sticky="w")

        # --- Action ---
        self.place_btn = ttk.Button(self.root, text="Place Mock Order", command=self.place_order_thread)
        self.place_btn.pack(pady=10)

        # --- Output Log ---
        log_frame = ttk.LabelFrame(self.root, text="Output Logs", padding=10)
        log_frame.pack(fill="both", expand=True)

        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=15)
        self.log_text.pack(fill="both", expand=True)

        sys.stdout = RedirectText(self.log_text)
        sys.stderr = RedirectText(self.log_text)

    def place_order_thread(self):
        threading.Thread(target=self.place_order, daemon=True).start()

    def place_order(self):
        print("\n--- Starting Mock Order ---")
        self.place_btn.config(state="disabled")

        try:
            client = MockClient()
            manager = OrderManager(client)
            
            manager.place_order(
                symbol=self.symbol_entry.get(),
                side=self.side_var.get(),
                order_type=self.type_var.get(),
                quantity=self.qty_entry.get(),
                price=self.price_entry.get()
            )
        except Exception as e:
            print(f"Exception caught in UI: {e}")
        finally:
            self.place_btn.config(state="normal")
            print("--- Ready ---\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = TradingBotUI(root)
    root.mainloop()
