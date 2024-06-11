'''This is just an idea for development. 
I'm not a frontend programmer and don't really have these skills (this is chatGPT code)
But I think the idea of a database viewer would be important.
If anyone has any idea on how to make this better, please feel free to run with this'''

import h5py
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class HDF5Viewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PYDB Viewer")
        self.geometry("800x600")
        
        # Menu
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.open_file)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=menubar)
        
        # Treeview for file structure
        self.tree = ttk.Treeview(self)
        self.tree.heading("#0", text="PYDB File Structure", anchor='w')
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Textbox for displaying dataset content
        self.textbox = tk.Text(self)
        self.textbox.pack(fill=tk.BOTH, expand=True)
    
    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PYDB files", "*.pydb")])
        if file_path:
            try:
                self.hdf5_file = h5py.File(file_path, 'r')
                self.populate_tree()
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def populate_tree(self):
        self.tree.delete(*self.tree.get_children())
        self.add_node("", self.hdf5_file)
    
    def add_node(self, parent, obj):
        if isinstance(obj, h5py.Group):
            for key, item in obj.items():
                node = self.tree.insert(parent, 'end', text=key, open=False)
                self.tree.insert(node, 'end', text="Loading...", tags=('dummy',))
        elif isinstance(obj, h5py.Dataset):
            self.tree.insert(parent, 'end', text=f"{obj.name} [Dataset]", tags=('dataset',))
    
    def on_tree_open(self, event):
        node = self.tree.focus()
        self.tree.delete(*self.tree.get_children(node))
        
        item = self.tree.item(node)
        path = self.get_node_path(node)
        
        try:
            obj = self.hdf5_file[path]
            self.add_node(node, obj)
            if isinstance(obj, h5py.Dataset):
                self.display_dataset(obj)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def get_node_path(self, node):
        path = ""
        while node:
            path = "/" + self.tree.item(node, "text") + path
            node = self.tree.parent(node)
        return path[1:]
    
    def display_dataset(self, dataset):
        self.textbox.delete("1.0", tk.END)
        self.textbox.insert(tk.END, dataset[()])

if __name__ == "__main__":
    app = HDF5Viewer()
    app.tree.bind("<<TreeviewOpen>>", app.on_tree_open)
    app.mainloop()
