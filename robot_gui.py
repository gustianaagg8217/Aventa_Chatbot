"""
Project Robot - GUI Interface
Interface grafis untuk interaksi dengan chatbot
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
from pathlib import Path
import json
from robot_core import RobotBrain


class RobotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 Project Robot - Chatbot Offline")
        self.root.geometry("900x700")
        self.root.configure(bg="#1e1e2e")
        
        self.robot = RobotBrain()
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background="#1e1e2e")
        style.configure('TLabel', background="#1e1e2e", foreground="#ffffff")
        style.configure('TButton', font=('Segoe UI', 10))
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup user interface"""
        
        # Header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title_label = ttk.Label(
            header_frame, 
            text="🤖 PROJECT ROBOT - CHATBOT OFFLINE YANG BISA DIAJARKAN",
            font=('Segoe UI', 14, 'bold'),
            foreground="#00d4ff"
        )
        title_label.pack()
        
        # Main content frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left panel - Chat
        left_panel = ttk.Frame(main_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        chat_label = ttk.Label(left_panel, text="💬 Percakapan:", font=('Segoe UI', 11, 'bold'))
        chat_label.pack()
        
        self.chat_display = scrolledtext.ScrolledText(
            left_panel,
            height=20,
            width=50,
            bg="#2d2d44",
            fg="#ffffff",
            font=('Segoe UI', 10),
            state=tk.DISABLED
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Input frame
        input_frame = ttk.Frame(left_panel)
        input_frame.pack(fill=tk.X, pady=5)
        
        self.input_field = tk.Text(
            input_frame,
            height=3,
            width=50,
            bg="#2d2d44",
            fg="#ffffff",
            font=('Segoe UI', 10),
            insertbackground='white'
        )
        self.input_field.pack(fill=tk.BOTH, expand=True)
        
        # Button frame
        button_frame = ttk.Frame(left_panel)
        button_frame.pack(fill=tk.X, pady=5)
        
        send_btn = ttk.Button(
            button_frame,
            text="📤 Kirim",
            command=self.send_message,
            width=10
        )
        send_btn.pack(side=tk.LEFT, padx=2)
        
        clear_btn = ttk.Button(
            button_frame,
            text="🗑️ Clear Chat",
            command=self.clear_chat,
            width=12
        )
        clear_btn.pack(side=tk.LEFT, padx=2)
        
        # Right panel - Controls
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(5, 0))
        
        # Stats
        stats_label = ttk.Label(right_panel, text="📊 Statistik:", font=('Segoe UI', 11, 'bold'))
        stats_label.pack()
        
        self.stats_display = scrolledtext.ScrolledText(
            right_panel,
            height=8,
            width=25,
            bg="#2d2d44",
            fg="#00d4ff",
            font=('Segoe UI', 9),
            state=tk.DISABLED
        )
        self.stats_display.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Control buttons
        control_label = ttk.Label(right_panel, text="⚙️ Kontrol:", font=('Segoe UI', 11, 'bold'))
        control_label.pack(pady=(10, 5))
        
        buttons_config = [
            ("📚 Lihat Pattern", self.show_patterns),
            ("🎓 Ajarkan Baru", self.teach_robot),
            ("📜 History", self.show_history),
            ("🔄 Refresh Stats", self.refresh_stats),
            ("🗑️ Clear Memory", self.clear_memory),
        ]
        
        for btn_text, cmd in buttons_config:
            btn = ttk.Button(
                right_panel,
                text=btn_text,
                command=cmd,
                width=22
            )
            btn.pack(fill=tk.X, pady=2)
        
        # Bind Enter key
        self.input_field.bind('<Control-Return>', lambda e: self.send_message())
        
        # Initial stats
        self.refresh_stats()
        
        # Display welcome message
        self.display_bot_message("Halo! Aku Project Robot 🤖\nAka senang mengobrol denganmu!\nKamu bisa mengajari saya percakapan baru lho!")
    
    def display_user_message(self, message: str):
        """Tampilkan pesan user"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"\n👤 Anda:\n{message}\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def display_bot_message(self, message: str):
        """Tampilkan pesan bot"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"\n🤖 Project Robot:\n{message}\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def send_message(self):
        """Kirim pesan ke robot"""
        message = self.input_field.get("1.0", tk.END).strip()
        
        if not message:
            return
        
        self.display_user_message(message)
        self.input_field.delete("1.0", tk.END)
        
        response = self.robot.process_input(message)
        self.display_bot_message(response)
        
        self.refresh_stats()
    
    def clear_chat(self):
        """Clear chat display"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def show_patterns(self):
        """Tampilkan semua pattern"""
        patterns_text = self.robot.list_patterns()
        
        pattern_window = tk.Toplevel(self.root)
        pattern_window.title("📚 Pattern Yang Dipelajari")
        pattern_window.geometry("600x500")
        pattern_window.configure(bg="#1e1e2e")
        
        text_widget = scrolledtext.ScrolledText(
            pattern_window,
            bg="#2d2d44",
            fg="#ffffff",
            font=('Segoe UI', 10)
        )
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert(tk.END, patterns_text)
        text_widget.config(state=tk.DISABLED)
    
    def teach_robot(self):
        """Buka dialog untuk ajarkan robot"""
        teach_window = tk.Toplevel(self.root)
        teach_window.title("🎓 Ajarkan Robot Percakapan Baru")
        teach_window.geometry("500x400")
        teach_window.configure(bg="#1e1e2e")
        
        # Intent
        ttk.Label(teach_window, text="Intent (nama kategori):", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W, padx=10, pady=(10, 0))
        intent_entry = ttk.Entry(teach_window, width=40)
        intent_entry.pack(fill=tk.X, padx=10, pady=5)
        
        # Keywords
        ttk.Label(teach_window, text="Keywords (pisahkan dengan koma):", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W, padx=10, pady=(10, 0))
        keywords_text = tk.Text(teach_window, height=3, width=40, bg="#2d2d44", fg="#ffffff")
        keywords_text.pack(fill=tk.X, padx=10, pady=5)
        
        # Responses
        ttk.Label(teach_window, text="Responses (pisahkan dengan |):", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W, padx=10, pady=(10, 0))
        responses_text = tk.Text(teach_window, height=3, width=40, bg="#2d2d44", fg="#ffffff")
        responses_text.pack(fill=tk.X, padx=10, pady=5)
        
        def save_teaching():
            intent = intent_entry.get().strip()
            keywords = [k.strip() for k in keywords_text.get("1.0", tk.END).split(',') if k.strip()]
            responses = [r.strip() for r in responses_text.get("1.0", tk.END).split('|') if r.strip()]
            
            if not intent or not keywords or not responses:
                messagebox.showerror("Error", "Semua field harus diisi!")
                return
            
            result = self.robot.teach(intent, keywords, responses)
            messagebox.showinfo("Info", result)
            teach_window.destroy()
            self.refresh_stats()
        
        ttk.Button(teach_window, text="💾 Simpan & Ajarkan", command=save_teaching, width=30).pack(pady=10)
    
    def show_history(self):
        """Tampilkan history percakapan"""
        recent = self.robot.memory.get_context(20)
        
        history_window = tk.Toplevel(self.root)
        history_window.title("📜 Riwayat Percakapan")
        history_window.geometry("600x500")
        history_window.configure(bg="#1e1e2e")
        
        text_widget = scrolledtext.ScrolledText(
            history_window,
            bg="#2d2d44",
            fg="#ffffff",
            font=('Segoe UI', 10)
        )
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        if recent:
            history_text = "📜 RIWAYAT 20 PERCAKAPAN TERAKHIR\n" + "="*50 + "\n"
            for i, conv in enumerate(recent, 1):
                history_text += f"\n{i}. [{conv['timestamp']}]\n"
                history_text += f"   👤 Anda: {conv['user']}\n"
                history_text += f"   🤖 Bot: {conv['bot']}\n"
            text_widget.insert(tk.END, history_text)
        else:
            text_widget.insert(tk.END, "Belum ada riwayat percakapan")
        
        text_widget.config(state=tk.DISABLED)
    
    def refresh_stats(self):
        """Refresh statistik"""
        stats_text = self.robot.get_stats()
        
        self.stats_display.config(state=tk.NORMAL)
        self.stats_display.delete("1.0", tk.END)
        self.stats_display.insert(tk.END, stats_text)
        self.stats_display.config(state=tk.DISABLED)
    
    def clear_memory(self):
        """Hapus semua memory"""
        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus semua memory?"):
            result = self.robot.clear_all_memory()
            messagebox.showinfo("Info", result)
            self.clear_chat()
            self.refresh_stats()


def main():
    root = tk.Tk()
    gui = RobotGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
