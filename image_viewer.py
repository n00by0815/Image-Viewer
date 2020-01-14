import tkinter as tk

'''
The full code will access a database with information on Images.
ClassTwo should then list all available Images, containing a 
given search string (e.g. color green). A click on one of the items in the
MultiListbox should then open the image in that row.

Class Three would be called simultaneously. It will contain more granular 
information on the image (e.g. the size of green area and position). 
A click on one element in that MultiListbox will open the image and highlight 
the particular area in the image that was selected.
'''

class MultiListbox(tk.Frame):
#original Python2 code here:
#https://www.oreilly.com/library/view/python-cookbook/0596001673/ch09s05.html
    def __init__(self, master, lists):
        tk.Frame.__init__(self, master)
        self.lists = []
        #print(lists)
        for l,w in lists:
            frame = tk.Frame(self)
            frame.pack(side='left', expand='yes', fill='both')
            tk.Label(frame, text=l, borderwidth=1, relief='raised').pack(fill='x')
            lb = tk.Listbox(frame, width=w, borderwidth=0, selectborderwidth=0,
                         relief='flat', exportselection=False, height=16)
            lb.pack(expand='yes', fill='both')
            self.lists.append(lb)
            #commented out functions that were not necessary, as suggested in the comments
            #lb.bind('<B1-Motion>', self._select)
            lb.bind('<<ListboxSelect>>', self._select)
            #lb.bind('<Leave>', lambda e: 'break')
            lb.bind('<MouseWheel>', lambda e, s=self: s._scroll_mouse(e))
            #lb.bind('<Button-2>', lambda e, s=self: s._button2(e.x, e.y))
        frame = tk.Frame(self)
        frame.pack(side='left', fill='y')
        tk.Label(frame, borderwidth=1, relief='raised').pack(fill='x')
        sb = tk.Scrollbar(frame, orient='vertical', command=self._scroll)
        sb.pack(expand='yes', fill='y')
        self.lists[0]['yscrollcommand']=sb.set

    def _select(self, event):
        print('on _select({})'.format(event.type))
        w = event.widget
        curselection = w.curselection()

        if curselection:
            self.selection_clear(0, self.size())
            self.selection_set(curselection[0])

    def _button2(self, x, y):
        for l in self.lists:
            l.scan_mark(x, y)
        return 'break'

    def _b2motion(self, x, y):
        for l in self.lists: l.scan_dragto(x, y)
        return 'break'

    def _scroll(self, *args):
        for l in self.lists:
            l.yview(*args)
        return 'break'

    def _scroll_mouse(self, event):
        for l in self.lists:
            l.yview_scroll(int(-1*(event.delta/120)), 'units')
        return 'break'

    def curselection(self):
        return self.lists[0].curselection()

    def delete(self, first, last=None):
        for l in self.lists:
            l.delete(first, last)

    def get(self, first, last=None):
        result = []
        for l in self.lists:
            result.append(l.get(first,last))
        if last: return apply(map, [None] + result)
        return result

    def index(self, index):
        self.lists[0].index(index)

    def insert(self, index, *elements):
        for e in elements:
            for i, l in enumerate(self.lists):
                l.insert(index, e[i])

    def size(self):
        return self.lists[0].size()

    def see(self, index):
        for l in self.lists:
            l.see(index)

    def selection_anchor(self, index):
        for l in self.lists:
            l.selection_anchor(index)

    def selection_clear(self, first, last=None):
        for l in self.lists:
            l.selection_clear(first, last)

    def selection_includes(self, index):
        return self.lists[0].selection_includes(index)

    def selection_set(self, first, last=None):
        for l in self.lists:
            l.selection_set(first, last)

class ClassOne:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.create_elements()
        self.frame.pack()

    def create_elements(self):
        search_button = tk.Button(self.frame, text = "Launch searches", command = \
        self.call_other_classes)
        search_button.grid(row = 2, column = 0, padx = 20, pady = 10)
        exit_button = tk.Button(self.frame, text = "Exit", command = self.master.quit)
        exit_button.grid(row = 2, column = 1, padx = 20, pady = 10)

    def call_other_classes(self):
        self.classes_list = []
        self.classes_list.append(ClassTwo(self.master))
        self.classes_list.append(ClassThree(self.master))

class ClassTwo:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(tk.Toplevel(self.master))
        self.frame.pack()
        self.create_elements()
        self.fill_image_listbox()       

    def create_elements(self):
        #placement of the custom MultiListbox
        self.available_images_lb = MultiListbox(self.frame, (('stuff1', 0), ('stuff1', 0), \
        ('stuff1', 0), ('stuff1', 0), ('stuff1', 0) ))
        self.available_images_lb.grid(row = 1, column = 1)
        #self.available_images_lb.bind('<<ListboxSelect>>', self.print_stuff_two)
        #Button
        exit_button = tk.Button(self.frame, text = "Quit", command = self.frame.quit)
        exit_button.grid(row = 2, column = 1, padx = 20, pady = 10)


    def fill_image_listbox(self):
        image_info = [5*['ABCD'],5*['EFGH'],5*['JKLM'],5*['NOPQ'],5*['RSTU'], 5*['VWXY']]
        for item in image_info:
            self.available_images_lb.insert('end', item)

    def print_stuff_two(self, event):
        print('Class Two active, this will open an image in the final project')

class ClassThree:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(tk.Toplevel(self.master))
        self.create_elements()
        self.frame.pack()
        self.fill_imageparts_listbox()

    def create_elements(self):  
        self.image_parts_info_lb = MultiListbox(self.frame, (('stuff1', 0), ('stuff1', 0), \
        ('stuff1', 0), ('stuff1', 0), ('stuff1', 0) ))
        self.image_parts_info_lb.grid(row = 1, column = 1)
        #self.image_parts_info_lb.bind('<<ListboxSelect>>', self.print_stuff_three)

    def fill_imageparts_listbox(self):
        self.image_parts_info_lb.delete(0, 'end')
        image_part_info = [5*['1234'],5*['5678'],5*['91011']]
        for item in image_part_info:
            self.image_parts_info_lb.insert('end', item)

    def print_stuff_three(self, event):
        print('Class Three active, this will open an image in the final project')     

def main():
    root = tk.Tk()
    root.title('Image Viewer')
    root.geometry('500x150+300+300')
    my_class_one = ClassOne(root)
    root.mainloop()


if __name__ == "__main__":
    main()
