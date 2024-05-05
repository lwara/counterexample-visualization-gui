import tkinter as tk
  
class LineNumbers(tk.Text):
    def __init__(self, master, text_widget, **kwargs):
        super().__init__(master, **kwargs)
  
        self.text_widget = text_widget
        self.text_widget.bind('<KeyRelease>', self.on_key_release)
  
        self.insert(1.0, '1')
        self.configure(state='disabled')
  
    def on_key_release(self, event=None):
        p, q = self.text_widget.index("@0,0").split('.')
        p = int(p)
        final_index = str(self.text_widget.index(tk.END))
        num_of_lines = final_index.split('.')[0]
        line_numbers_string = "\n".join(str(p + no) for no in range(int(num_of_lines)))
        width = len(str(num_of_lines))
  
        self.configure(state='normal', width=width)
        self.delete(1.0, tk.END)
        self.insert(1.0, line_numbers_string)
        self.configure(state='disabled')
  
if __name__ == '__main__':
    w = tk.Tk()
    t = tk.Text(w)
    l = LineNumbers(w, t, width=2)
    t.insert('1.0', 'a\n' \
                    'b\n' \
                    'c\n' \
                    'd\n' \
                    'e\n' \
                    'f\n' \
                    'g\n' \
                    'h\n' \
                    'i\n' \
                    'j\n' \
                    'k\n' \
                    'l\n' \
                    'm\n' \
                    'n\n' \
                    'o\n' \
                    'p\n' \
                    'q\n' \
                    'r\n' \
                    's\n' \
                    't\n' \
                    'u\n' \
                    'v\n' \
                    'w\n' \
                    'x\n' \
                    'y\n' \
                    'z\n' \
                    '1\n' \
                    '2\n' \
                    '3\n' \
                    '4\n' \
                    '5\n' \
                    '6\n' \
                    '7\n' \
                    '8\n' \
                    '9\n')
    l.pack(side=tk.LEFT)
    t.pack(side=tk.LEFT, expand=1)
    w.mainloop()