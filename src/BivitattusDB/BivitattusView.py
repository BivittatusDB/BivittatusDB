import h5py, gzip, json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from binascii import unhexlify

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

        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=2)
        self.grid_rowconfigure(1, weight=1)

        # Treeview for file structure
        self.tree = ttk.Treeview(self)
        self.tree.heading("#0", text="Open a file with file > open", anchor='w')
        self.tree.grid(column=1, row=1, sticky='NESW')
        
        # Frame for displaying dataset content
        self.dataset_frame = tk.Frame(self)
        self.dataset_frame.grid(column=2, row=1, sticky='NWSE')

    
    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PYDB files", "*.pydb")])
        if file_path:
            try:
                self.hdf5_file = h5py.File(file_path, 'r')
                self.populate_tree()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        self.tree.heading("#0", text="")
    
    def populate_tree(self):
        self.tree.delete(*self.tree.get_children())
        self.add_node("", self.hdf5_file)
    
    def add_node(self, parent, obj):
        if isinstance(obj, h5py.Group):
            for key, item in obj.items():
                if key == "database":
                    continue
                node = self.tree.insert(parent, 'end', text=key, open=False)
                self.tree.insert(node, 'end', text="Loading...", tags=('dummy',))
        elif isinstance(obj, h5py.Dataset):
            if obj.name.split('/')[-1] == "database":
                return
            self.tree.insert(parent, 'end', text=f"{obj.name} [Dataset]", tags=('dataset',))
    
    def on_tree_open(self, event):
        node = self.tree.focus()
        self.tree.delete(*self.tree.get_children(node))
        
        item = self.tree.item(node)
        path = self.get_node_path(node)
        
        try:
            obj = self.hdf5_file[path]
            self.close_other_nodes(node)
            self.add_node(node, obj)
            if isinstance(obj, h5py.Dataset):
                self.display_dataset(obj)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def close_other_nodes(self, except_node):
        # Get all root-level nodes
        root_nodes = self.tree.get_children()
        
        # Traverse all nodes and close them except the one being opened
        nodes_to_close = set(root_nodes) - {except_node}
        for node in nodes_to_close:
            self.close_node_recursively(node)
    
    def close_node_recursively(self, node):
        # Close the node
        self.tree.item(node, open=False)
        
        # Close all its children recursively
        for child in self.tree.get_children(node):
            self.close_node_recursively(child)
    
    def get_node_path(self, node):
        path = ""
        while node:
            path = "/" + self.tree.item(node, "text") + path
            node = self.tree.parent(node)
        return path[1:]
    
    def create_table(self, frame, data):
        # Clear previous content in the frame
        for widget in frame.winfo_children():
            widget.destroy()
        
        # Create table headers
        for col_num, col_name in enumerate(data[0]):
            header = tk.Label(frame, text=col_name, borderwidth=1, relief="solid", width=15)
            header.grid(row=0, column=col_num)
        
        # Create table cells
        for row_num, row_data in enumerate(data[1:], start=1):
            for col_num, cell_data in enumerate(row_data):
                cell = tk.Entry(frame, borderwidth=1, relief="solid", width=15)
                cell.grid(row=row_num, column=col_num)
                cell.insert(tk.END, cell_data)
    
    def display_dataset(self, dataset):
        # Clear the frame
        self.dataset_frame.pack_forget()
        self.dataset_frame = tk.Frame(self)
        self.dataset_frame.grid(column=2, row=1, sticky='NS')
        
        # Decompress and decode the dataset
        data = json.loads(gzip.decompress(unhexlify(dataset[()])))
        
        # Create and display the table
        self.create_table(self.dataset_frame, data)

if __name__ == "__main__":
    app = HDF5Viewer()
    app.tree.bind("<<TreeviewOpen>>", app.on_tree_open)
    app.mainloop()
