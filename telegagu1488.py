import threading
from customtkinter import *
from socket import *

set_default_color_theme("blue")

class w(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x300")
        self.title('Уничтожітель телерама')
        
        self.configure(fg_color=("#F2F4F7", "#1A1A1A"))
        
        self.frame = CTkFrame(
            self, 
            width=200, 
            height=self.winfo_height(),
            fg_color=("#D1D5DB", "#252A34"),
            border_color=("#9CA3AF", "#4F5D75"),
            border_width=2
        )
        self.frame.pack_propagate(False)
        self.frame.configure(width=0)
        self.frame.place(x=0, y=0)
        
        self.oshow_menu = False
        self.frame_width = 0
        self.s_speed = 20

        self.label = CTkLabel(self.frame, text="Як можна вас назвати?", text_color=("#111827", "#EEEEEE"))
        self.label.pack(pady=20)

        self.entry = CTkEntry(self.frame, width=120, height=25, fg_color=("#FFFFFF", "#303846"))
        self.entry.pack(pady=10)

        self.option = CTkOptionMenu(
            self.frame, 
            width=120, 
            height=35, 
            values=["Europa", "Africa"], 
            command=self.change_theme,
            fg_color=("#4B5563", "#4F5D75"),
            button_color=("#374151", "#3F4E65")
        )
        self.option.pack(pady=10)

        self.btn = CTkButton(
            self, 
            width=40, 
            height=30, 
            text='👉🏻', 
            command=self.i_show_speed,
            fg_color=("#6B7280", "#3A4750"),
            hover_color=("#4B5563", "#303841")
        )
        self.btn.place(x=0, y=0)

        self.textbox = CTkTextbox(
            self, 
            state="disable",
            fg_color=("#FFFFFF", "#111111"),
            text_color=("#1F2937", "#E5E7EB"),
            border_color=("#E5E7EB", "#2D2D2D"),
            border_width=1
        )
        self.textbox.place(x=200, y=30)

        self.send = CTkEntry(
            self, 
            placeholder_text='Тап тап клава: ',
            fg_color=("#FFFFFF", "#222222"),
            text_color=("#000000", "#FFFFFF")
        )
        self.send.place(x=0, y=250)

        self.btn_send = CTkButton(
            self, 
            text='☝🏻', 
            command=self.send_m,
            fg_color=("#2563EB", "#1D4ED8"),
            hover_color=("#1D4ED8", "#1E40AF")
        )
        self.btn_send.place(x=200, y=250)

        self.username = "Golub Opezdal"
        
        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.connect(('6.tcp.eu.ngrok.io', 21176))
            hello_text = f"TEXT@{self.username}@Welcome!\n"
            self.sock.send(hello_text.encode())
            
            threading.Thread(target=self.recv_message, daemon=True).start()
        except Exception as e:
            print(f"Error connecting to server: {e}")

        self.adaptiv_ui()

    def i_show_speed(self):
        if self.oshow_menu:
            self.oshow_menu = False
            self.close_menu()
        else:
            self.oshow_menu = True
            self.show_menu()
    
    def show_menu(self):
        if self.frame_width <= 200:
            self.frame_width += self.s_speed
            self.frame.configure(width=self.frame_width, height=self.winfo_height())
            if self.frame_width >= 30:
                self.btn.configure(width=self.frame_width, text='👈🏻')
        if self.oshow_menu:
            self.after(20, self.show_menu)

    def close_menu(self):
        if self.frame_width >= 0:
            self.frame_width -= self.s_speed
            self.frame.configure(width=self.frame_width, height=self.winfo_height())
            if self.frame_width <= 30:
                self.btn.configure(width=max(self.frame_width, 40), text='👉🏻')
        if not self.oshow_menu:
            self.after(20, self.close_menu)

    def change_theme(self, value):
        if value == "Africa":
            set_appearance_mode('dark')
        else:
            set_appearance_mode('light')
    
    def adaptiv_ui(self):
        w_width = max(self.winfo_width(), 100)
        w_height = max(self.winfo_height(), 100)
        f_width = self.frame.winfo_width()
        
        tb_width = max(w_width - f_width, 10)
        tb_height = max(w_height - 80, 10)
        
        self.textbox.configure(width=tb_width, height=tb_height)
        self.textbox.place(x=f_width, y=30)

        send_width = max(w_width - f_width - self.btn_send.winfo_width(), 10)
        self.send.configure(width=send_width)
        self.send.place(x=f_width, y=w_height - 40)

        self.btn_send.place(x=f_width + send_width, y=w_height - 40)

        self.after(50, self.adaptiv_ui)

    def add_message(self, text):
        self.textbox.configure(state='normal')
        self.textbox.insert(END, f"{text}\n")
        self.textbox.see(END)
        self.textbox.configure(state="disable")
    
    def send_m(self):
        message = self.send.get()
        if message:
            self.add_message(f"Me: {message}")
            data = f"TEXT@{self.username}@{message}\n"
            try:
                self.sock.sendall(data.encode())
            except Exception as e:
                self.add_message(f"System: Failed to send ({e})")
        self.send.delete(0, END)

    def recv_message(self):
        buffer = ''
        while True:
            try:
                chunk = self.sock.recv(4096)
                if not chunk:
                    break
                buffer += chunk.decode()
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    self.handle_line(line.strip())
            except:
                break
        try:
            self.sock.close()
        except:
            pass

    def handle_line(self, line):
        if not line:
            return
        parts = line.split("@", 2)
        msg_type = parts[0]
        if msg_type == 'TEXT':
            if len(parts) >= 3:
                author = parts[1]
                message = parts[2]
                if author != self.username:
                    self.add_message(f"{author}: {message}")
            else:
                self.add_message(line)

if __name__ == "__main__":
    win = w()
    win.mainloop()