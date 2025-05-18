# interface.py
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from PIL import Image, ImageTk


SEPARATOR = "_" * 81


class AgentChatGUI:
    def __init__(self, master: tk.Tk, on_message_sent_callback=None):
        self.master = master
        
        master.geometry("1100x500") 
        master.title("Warren Bot 🤖💼")
        self.on_message_sent_callback = on_message_sent_callback

        style = ttk.Style()
        self.main_font = ('Helvetica', 12)

        style.configure("TFrame", padding=12)
        style.configure("TButton", font=self.main_font, padding=8, background="#4CAF50", foreground="white")
        style.layout("TButton", [("Button.background", {"children": [("Button.padding", 
                        {"children": [("Button.label", {"sticky": "nswe"})],
                        "sticky": "nswe"})], "sticky": "nswe"})])
        style.configure("TEntry", font=self.main_font, padding=5) 
        style.configure("TLabel", font=self.main_font)

        style.configure("Transparent.TFrame", background="#FFFFFF", relief="flat")
        style.configure("Transparent.TEntry", fieldbackground="#FFFFFF", background="#FFFFFF", relief="flat")
        style.map("Transparent.TEntry", background=[('active', '#FFFFFF'), ('disabled', '#E0E0E0')])

        send_button_font_size = 16 
        send_button_padding = (6, 3) 
        style.configure("SendButton.TButton", font=(self.main_font[0], send_button_font_size), padding=send_button_padding)

        self.canvas = tk.Canvas(master, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.bg_image = Image.open("image.png")
        self.bg_image = self.bg_image.resize((300, 300), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.icon_image = ImageTk.PhotoImage(self.bg_image)
        master.iconphoto(False, self.icon_image)

        center_y = (500 - 300) // 2 

        self.canvas.create_image(0, center_y, image=self.bg_photo, anchor=tk.NW)

        self.create_widgets(style)

    def create_widgets(self, style):
        self.chat_history_frame = ttk.Frame(self.canvas, style="Transparent.TFrame")
        self.chat_history_frame.place(x=320, y=20, width=750, height=400)

        self.chat_history_text = scrolledtext.ScrolledText(self.chat_history_frame, wrap=tk.WORD, state='disabled', font=self.main_font)
        self.chat_history_text.pack(fill=tk.BOTH, expand=True)

        self.input_frame = ttk.Frame(self.canvas, style="Transparent.TFrame")
        self.input_frame.place(x=320, y=440, width=750, height=40)

        self.input_entry = ttk.Entry(self.input_frame, font=self.main_font, style="Transparent.TEntry")
        self.input_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        self.input_entry.bind("<Return>", lambda event=None: self._input_message())

        send_icon = "➤"
        style.configure("SendButton.TButton", relief="flat")
        self.send_button = ttk.Button(self.input_frame, text=send_icon, command=self._input_message, style="SendButton.TButton", width=5)
        self.send_button.pack(side=tk.RIGHT)

        def on_press(event):
            style.configure("TButton", background="#388E3C")

        def on_release(event):
            style.configure("TButton", background="#4CAF50")
            
        self.send_button.bind("<ButtonPress-1>", on_press)
        self.send_button.bind("<ButtonRelease-1>", on_release)

    def append_message(self, sender: str, message: str):
        self.chat_history_text.config(state='normal')
        self.chat_history_text.insert(tk.END, f"{sender.upper()}: {message}\n\n" if sender else f"{message}")
        self.chat_history_text.config(state='disabled')
        self.chat_history_text.yview(tk.END)

    def _input_message(self, event=None):
        user_input = self.input_entry.get().strip()
        if not user_input:
            return
        
        self.append_message("👤 Você", user_input)
        self.append_message(None, f"{SEPARATOR}\n\n")
        self.input_entry.delete(0, tk.END)
        self.input_entry.config(state='disabled')
        self.send_button.config(state='disabled')
        if self.on_message_sent_callback:
            self.master.after(0, self.on_message_sent_callback, user_input)
        else:
            print("Erro: Callback on_message_sent_callback não definido na GUI.")
            self.receive_agent_response("[Sistema] Erro: Lógica de agente não conectada.")

    def receive_agent_response(self, response: str, sender: str = "Agente"):
        self.append_message(sender, response)
        self.input_entry.config(state='normal')
        self.send_button.config(state='normal')
        self.input_entry.focus_set()
