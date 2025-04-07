import tkinter as tk
from tkinter import ttk, messagebox
import secrets
import json
import os
import string
#打包
#pyinstaller --onefile --add-data "config.json;." --noconsole your_script.py
class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("安全密码生成器 v3.5")
        self.root.geometry("420x300")
        self.setup_config()
        self.setup_ui()
        self.set_window_topmost()

    def setup_config(self):
        """读取/创建配置文件"""
        self.config_file = "config.json"
        default_config = {"length": 16, "special_chars": "!@#$%^&*"}
        
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = default_config
            self.save_config()

    def save_config(self):
        """保存配置到文件"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f)

    def setup_ui(self):
        """构建界面组件"""
        style = ttk.Style()
        style.configure('TButton', font=('微软雅黑', 10), padding=5)
        style.map('TButton', background=[('active', '#45a049')])

        # 配置区域
        config_frame = ttk.LabelFrame(self.root, text="配置参数")
        config_frame.pack(pady=10, padx=10, fill=tk.X)

        ttk.Label(config_frame, text="密码长度:").grid(row=0, column=0, padx=5)
        self.length_entry = ttk.Entry(config_frame, width=8)
        self.length_entry.insert(0, str(self.config["length"]))
        self.length_entry.grid(row=0, column=1)

        ttk.Label(config_frame, text="特殊字符:").grid(row=1, column=0, padx=5)
        self.special_entry = ttk.Entry(config_frame)
        self.special_entry.insert(0, self.config["special_chars"])
        self.special_entry.grid(row=1, column=1, columnspan=2, sticky=tk.EW)

        # 功能按钮
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="生成密码", command=self.generate_password).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="复制密码", command=self.copy_password).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="保存配置", command=self.update_config).grid(row=0, column=2, padx=5)

        # 密码显示
        self.password_var = tk.StringVar()
        ttk.Entry(self.root, textvariable=self.password_var, 
                width=35, font=('Consolas', 12), state='readonly').pack(pady=10)

        # 窗口置顶开关
        self.top_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.root, text="窗口置顶", variable=self.top_var,
                      command=self.set_window_topmost).pack()

    def generate_password(self):
        """生成密码核心逻辑"""
        try:
            length = int(self.length_entry.get())
            specials = self.special_entry.get()
            
            if length < 8:
                raise ValueError("密码长度至少8位")
                
            # 构建字符池
            char_sets = {
                'upper': string.ascii_uppercase,
                'lower': string.ascii_lowercase,
                'digit': string.digits,
                'special': specials
            }
            
            # 确保每个类别至少一个字符
            password = [
                secrets.choice(char_sets['upper']),
                secrets.choice(char_sets['lower']),
                secrets.choice(char_sets['digit']),
                secrets.choice(char_sets['special'])
            ]
            
            # 填充剩余长度
            remaining = length - 4
            all_chars = ''.join(char_sets.values())
            password += [secrets.choice(all_chars) for _ in range(remaining)]
            secrets.SystemRandom().shuffle(password)
            
            self.password_var.set(''.join(password))
            
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def copy_password(self):
        """复制密码到剪贴板"""
        if self.password_var.get():
            self.root.clipboard_clear()
            self.root.clipboard_append(self.password_var.get())
            messagebox.showinfo("成功", "密码已复制到剪贴板")

    def update_config(self):
        """更新并保存配置"""
        self.config["length"] = int(self.length_entry.get())
        self.config["special_chars"] = self.special_entry.get()
        self.save_config()
        messagebox.showinfo("提示", "配置已永久保存")

    def set_window_topmost(self):
        """切换窗口置顶状态"""
        self.root.attributes('-topmost', self.top_var.get())

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()