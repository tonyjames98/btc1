import tkinter as tk
from coinmarketcapapi import CoinMarketCapAPI
from PIL import Image, ImageTk
import os


def get_bitcoin_price():
    cmc = CoinMarketCapAPI('269658e2-7c6a-404f-87f9-a0bbb1f611be')
    data_quote = cmc.cryptocurrency_quotes_latest(symbol='BTC', convert='USD')
    return data_quote.data['BTC'][0]['quote']['USD']['price']


class BitcoinPriceDisplay:
    def __init__(self, master):
        self.master = master
        master.title("Bitcoin Price")

        # Set a specific color for transparency
        self.transparent_color = '#000001'  # Nearly black

        # Make the window transparent
        master.attributes('-alpha', 1.0)
        master.attributes('-topmost', True)
        master.overrideredirect(True)
        master.wm_attributes('-transparentcolor', self.transparent_color)

        master.configure(bg=self.transparent_color)

        self.frame = tk.Frame(master, bg=self.transparent_color, padx=10, pady=10)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.create_widgets()
        self.update_price()

        # Bind dragging events to the entire window
        master.bind("<ButtonPress-1>", self.start_move)
        master.bind("<ButtonRelease-1>", self.stop_move)
        master.bind("<B1-Motion>", self.do_move)

    def create_widgets(self):
        content_frame = tk.Frame(self.frame, bg=self.transparent_color)
        content_frame.pack(side=tk.LEFT)

        # Logo
        script_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(script_dir, "opengraph.png")

        try:
            img = Image.open(logo_path)
            img = img.resize((40, 40), Image.LANCZOS)
            self.logo = ImageTk.PhotoImage(img)
            logo_label = tk.Label(content_frame, image=self.logo, bg=self.transparent_color)
            logo_label.pack(side=tk.LEFT, padx=(0, 10))
        except Exception as e:
            print(f"Failed to load Bitcoin logo: {e}. Continuing without it.")

        # Price display
        self.price_label = tk.Label(content_frame, text="", font=("Courier", 28, "bold"), fg='#00FF00',
                                    bg=self.transparent_color)
        self.price_label.pack(side=tk.LEFT)

        # Add a small, subtle close button
        close_button = tk.Label(self.frame, text="×", font=("Arial", 12), fg='#888888', bg=self.transparent_color,
                                cursor="hand2")
        close_button.pack(side=tk.RIGHT, anchor=tk.NE)
        close_button.bind("<Button-1>", lambda e: self.master.quit())

    def update_price(self):
        try:
            price = get_bitcoin_price()
            self.price_label.config(text=f"${price:,.2f}")
        except Exception as e:
            self.price_label.config(text="Error fetching price")
            print(f"Error updating price: {e}")

        self.master.after(300000, self.update_price)  # Update every 10 minutes (600000 milliseconds)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.master.winfo_x() + deltax
        y = self.master.winfo_y() + deltay
        self.master.geometry(f"+{x}+{y}")


def main():
    root = tk.Tk()
    app = BitcoinPriceDisplay(root)
    root.mainloop()


if __name__ == "__main__":
    main()