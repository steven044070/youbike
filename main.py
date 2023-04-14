import datasource
import tkinter as tk
from tkinter import ttk
import datetime
from tkinter.simpledialog import askinteger, askstring
from PIL import Image, ImageTk
from messageWindow import MapDisplay

sbi_numbers = 3
bemp_numbers = 3

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        # add menubar that contains a menu
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)
        # add command menu in menubar
        self.command_menu = tk.Menu(self.menubar, tearoff=0)
        self.command_menu.add_command(
            label="設定", command=self.menu_setting_click)
        self.command_menu.add_command(label="離開", command=self.destroy)
        self.menubar.add_cascade(label="File", menu=self.command_menu)

        self.command02_menu = tk.Menu(self.menubar, tearoff=0)
        self.command02_menu.add_command(
            label='查詢', command=self.menu_search_click)
        self.menubar.add_cascade(label='查詢', menu=self.command02_menu)

        #main Frame
        mainFrame = ttk.Frame(self)
        mainFrame.pack(padx=30,pady=50)

        # logoLabel top of top_wrapperFrame
        logoImage = Image.open('pic1.png')
        resizeImage = logoImage.resize((389, 129), Image.LANCZOS)
        self.logoTkimage = ImageTk.PhotoImage(resizeImage)
        logoLabel = ttk.Label(mainFrame, image=self.logoTkimage)
        logoLabel.pack(pady=(0, 50))

# top_wrapperFrame=================
        top_wrapperFrame = ttk.Frame(mainFrame)
        top_wrapperFrame.pack(fill=tk.X)
# topFrame_start===================
        topFrame = ttk.LabelFrame(top_wrapperFrame, text="台北市行政區")
        length = len(datasource.sarea_list)
        self.radioStringVar = tk.StringVar()
        for i in range(length):
            cols = i % 3
            rows = i // 3
            ttk.Radiobutton(topFrame, text=datasource.sarea_list[i], value=datasource.sarea_list[i], variable=self.radioStringVar, command=self.radio_Event).grid(
                column=cols, row=rows, sticky=tk.W, padx=10, pady=10)
        topFrame.pack(side=tk.LEFT)
        self.radioStringVar.set('中山區')
        self.area_data = datasource.getInfoFromArea('中山區')
# topFrame_end===================

# sbi_warningFrame_start====================
        self.sbi_warningFrame = ttk.LabelFrame(top_wrapperFrame)
        columns = ('#1', '#2', '#3')
        self.sbi_tree = ttk.Treeview(
            self.sbi_warningFrame, columns=columns, show='headings')
        self.sbi_tree.heading('#1', text='站點')
        self.sbi_tree.column("#1", minwidth=0, width=200)
        self.sbi_tree.heading('#2', text='可借')
        self.sbi_tree.column("#2", minwidth=0, width=30)
        self.sbi_tree.heading('#3', text='可還')
        self.sbi_tree.column("#3", minwidth=0, width=30)
        self.sbi_tree.pack(side=tk.LEFT)
        self.sbi_warning_data = datasource.filter_sbi_warning_data(
            self.area_data, sbi_numbers)
        
        sbi_sites_numbers = len(self.sbi_warning_data)
        self.sbi_warningFrame.configure(text=f"可借不足站點數:{sbi_sites_numbers}")

        for item in self.sbi_warning_data:
            self.sbi_tree.insert('', tk.END, values=[
                                item['sna'][11:], item['sbi'], item['bemp']])
        self.sbi_warningFrame.pack(side=tk.LEFT)

        sbi_scrollbar = ttk.Scrollbar(self.sbi_warningFrame, command=self.sbi_tree.yview)
        sbi_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.sbi_tree.config(yscrollcommand=sbi_scrollbar.set)
# sbi_warningFrame_end======================

# bemp_warningFrame_start====================
        self.bemp_warningFrame = ttk.LabelFrame(top_wrapperFrame)
        columns = ('#1', '#2', '#3')
        self.bemp_tree = ttk.Treeview(
            self.bemp_warningFrame, columns=columns, show='headings')
        self.bemp_tree.heading('#1', text='站點')
        self.bemp_tree.column("#1", minwidth=0, width=200)
        self.bemp_tree.heading('#2', text='可借')
        self.bemp_tree.column("#2", minwidth=0, width=30)
        self.bemp_tree.heading('#3', text='可還')
        self.bemp_tree.column("#3", minwidth=0, width=30)
        self.bemp_tree.pack(side=tk.LEFT)
        self.bemp_warning_data = datasource.filter_bemp_warning_data(
            self.area_data, bemp_numbers)
        
        bemp_sites_numbers = len(self.bemp_warning_data)
        self.bemp_warningFrame.configure(text=f"可還不足站點數:{bemp_sites_numbers}")

        for item in self.bemp_warning_data:
            self.bemp_tree.insert('', tk.END, values=[
                                item['sna'][11:], item['sbi'], item['bemp']])
        self.bemp_warningFrame.pack(side=tk.LEFT)

        bemp_scrollbar = ttk.Scrollbar(self.bemp_warningFrame, command=self.bemp_tree.yview)
        bemp_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.bemp_tree.config(yscrollcommand=bemp_scrollbar.set)
# bemp_warningFrame_end======================

# self.bottomFrame(製作bottomFrame)
        # get current datetime
        now = datetime.datetime.now()
        # display current datetime
        nowString = now.strftime("%Y-%m-%d %H:%M:%S")
        self.bottomFrame = ttk.LabelFrame(mainFrame, text=f"中山區-{nowString}")
        self.bottomFrame.pack()

# 製作bottomFrame介面
        columns = ('#1', '#2', '#3', '#4', '#5', '#6', '#7')
        self.tree = ttk.Treeview(self.bottomFrame, columns=columns, show='headings')
        self.tree.heading('#1', text='站點')
        self.tree.column("#1", minwidth=0, width=200)
        self.tree.heading('#2', text='時間')
        self.tree.column("#2", minwidth=0, width=200)
        self.tree.heading('#3', text='總車數')
        self.tree.column("#3", minwidth=0, width=50)
        self.tree.heading('#4', text='可借')
        self.tree.column("#4", minwidth=0, width=30)
        self.tree.heading('#5', text='可還')
        self.tree.column("#5", minwidth=0, width=30)
        self.tree.heading('#6', text='地址')
        self.tree.column("#6", minwidth=0, width=250)
        self.tree.heading('#7', text='狀態')
        self.tree.column("#7", minwidth=0, width=30)
        self.tree.pack(side=tk.LEFT)

        #self.tree, addItem
        for item in self.area_data:
            self.tree.insert('', tk.END, values=[
                item['sna'][11:], item['mday'], item['tot'], item['sbi'], item['bemp'], item['ar'], item['act']], tags=item['sna'])

        # self.tree bind event
        self.tree.bind('<<TreeviewSelect>>', self.treeSelected)

        # 製作treeview的scrollbar
        scrollbar = ttk.Scrollbar(self.bottomFrame,command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.config(yscrollcommand=scrollbar.set)

    #製作事件
    def radio_Event(self):
        # get current datetime
        now = datetime.datetime.now()
        # display current datetime
        nowString = now.strftime("%Y-%m-%d %H:%M:%S")

        # Clear tree view
        for item in self.tree.get_children():
            self.tree.delete(item)

        for item in self.sbi_tree.get_children():
            self.sbi_tree.delete(item)

        for item in self.bemp_tree.get_children():
            self.bemp_tree.delete(item)
        
        # Get selected radio button value
        area_name = self.radioStringVar.get()
        self.bottomFrame.config(text=f"{area_name}-{nowString}")

        # Get all station data from selected area
        self.area_data = datasource.getInfoFromArea(area_name)

        # Filter data with sbi warning number
        self.sbi_warning_data = datasource.filter_sbi_warning_data(self.area_data, sbi_numbers)
        sbi_site_numbers = len(self.sbi_warning_data)
        self.sbi_warningFrame.config(text=f"可借不足站點數:{sbi_site_numbers}")

        # Filter data with bemp warning number
        self.bemp_warning_data = datasource.filter_bemp_warning_data(self.area_data, bemp_numbers)
        bemp_site_numbers = len(self.bemp_warning_data)
        self.bemp_warningFrame.configure(text=f"可還不足站點數:{bemp_site_numbers}")

        # Display data in tree view
        for item in self.area_data:
            self.tree.insert('', tk.END, values=[
                item['sna'][11:], item['mday'], item['tot'], item['sbi'], item['bemp'], item['ar'], item['act']],tags=item['sna'])

        for item in self.sbi_warning_data:
            self.sbi_tree.insert('', tk.END, values=[
                                item['sna'][11:], item['sbi'], item['bemp']])

        for item in self.bemp_warning_data:
            self.bemp_tree.insert('', tk.END, values=[
                                item['sna'][11:], item['sbi'], item['bemp']])

    def treeSelected(self, event):
        selectedTree = event.widget
        if len(selectedTree.selection()) == 0:return
        itemTag = selectedTree.selection()[0]
        itemDic = selectedTree.item(itemTag)
        siteName = itemDic['tags'][0]
        for item in self.area_data:
            if siteName == item['sna']:
                select_data = item
                break
        
        #顯示地圖的window
        mapdisplay = MapDisplay(self,select_data)

    #menu事件
    def menu_setting_click(self):
        global sbi_numbers, bemp_numbers
        retVal = askinteger(f"目前設定不足數量:{sbi_numbers}",
                            "請輸入不足可借可還數量",
                            minvalue=0, maxvalue=5)
        sbi_numbers = retVal
        bemp_numbers = retVal

    def menu_search_click(self):
        retVal = askstring('站點搜尋', '請輸入名稱')
        for item in self.tree.get_children():
            self.tree.delete(item)
        for item in self.area_data:
            if retVal in item['sna'] or retVal in item['ar']:
                self.tree.insert('', tk.END, values=[
                                item['sna'][11:], item['mday'], item['tot'], item['sbi'], item['bemp'], item['ar'], item['act']], tags=item['sna'])

def main():
    window = Window()
    window.title('台北市youbike2.0資訊')
    window.mainloop()

if __name__ == '__main__':
    main()