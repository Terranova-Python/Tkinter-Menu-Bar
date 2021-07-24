from tkinter import *
from ctypes import windll
from PIL import ImageTk, Image


#this code works fine on windows 10, i didn't try it in any other OS, if you use window 8, 7, ... 
#or you use a distro of linux, you can try it anyway


#this code works fine as a exe made in pyinstaller





tk_title = "tk" # Put here your window title
winodow_icon = "" # the name or path of your icon



root=Tk() # root (your app doesn't go in root, it goes in window)
root.title(tk_title) 
root.overrideredirect(True) # turns off title bar, geometry
root.geometry('200x200+75+75') # set new geometry the + 75 + 75 is where it starts on the screen
if winodow_icon != "": 
    root.iconbitmap(winodow_icon) # to show your own icon 


root.resizable = True # put false if you don't want your window to be resizable


root.minimized = False # only to know if root is minimized
root.maximized = False # only to know if root is maximized





LGRAY = '#3e4042' # button color effects in the title bar (Hex color)
DGRAY = '#0f1012' # window background color               (Hex color)
RGRAY = '#000000' # title bar color                       (Hex color)



root.config(bg="#25292e")
title_bar = Frame(root, bg=RGRAY, relief='raised', bd=0,highlightthickness=0)


if winodow_icon != "": 
    image = Image.open(winodow_icon)
    image = image.resize((17, 17), Image.ANTIALIAS)
    im = ImageTk.PhotoImage(image)
    widget_icon = Label(title_bar,image=im,bg=RGRAY )
    widget_icon.pack(side=LEFT,padx=2)



def set_appwindow(mainWindow): # to display the window icon on the taskbar, 
                               # even when using root.overrideredirect(True)

    # Some WindowsOS styles, required for task bar integration
    GWL_EXSTYLE = -20
    WS_EX_APPWINDOW = 0x00040000
    WS_EX_TOOLWINDOW = 0x00000080
    # Magic
    hwnd = windll.user32.GetParent(mainWindow.winfo_id())
    stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    stylew = stylew & ~WS_EX_TOOLWINDOW
    stylew = stylew | WS_EX_APPWINDOW
    res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)
   
    mainWindow.wm_withdraw()
    mainWindow.after(10, lambda: mainWindow.wm_deiconify())






def minimize_me():
    root.attributes("-alpha",0) # so you can't see the window when is minimized
    root.minimized = True       



def deminimize(event):
    if root.minimized == True:
        root.attributes("-alpha",1) # so you can see the window when is not minimized
        root.focus() 
        root.minimized = False                              
    




def maximize_me():

    if root.maximized == False: # if the window was not maximized
        root.normal_size = root.geometry()
        expand_button.config(text=" 🗗 ")
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight() - 1}+0+0")
        root.maximized = not root.maximized 
        # now it's maximized
        
    else: # if the window was maximized
        expand_button.config(text=" 🗖 ")
        root.geometry(root.normal_size)
        root.maximized = not root.maximized
        # now it is not maximized






# put a close button on the title bar
close_button = Button(title_bar, text='  ×  ', command=root.destroy,bg=RGRAY,padx=2,pady=2,font=("calibri", 13),bd=0,fg='white',highlightthickness=0)
expand_button = Button(title_bar, text=' 🗖 ', command=maximize_me,bg=RGRAY,padx=2,pady=2,bd=0,fg='white',font=("calibri", 13),highlightthickness=0)
minimize_button = Button(title_bar, text=' 🗕 ',command=minimize_me,bg=RGRAY,padx=2,pady=2,bd=0,fg='white',font=("calibri", 13),highlightthickness=0)
title_bar_title = Label(title_bar, text=tk_title, bg=RGRAY,bd=0,fg='white',font=("helvetica", 10),highlightthickness=0)


if root.resizable == False:
    expand_button.config(state="disabled")


# a frame for the main area of the window, this is where the actual app will go
window = Frame(root, bg=DGRAY,highlightthickness=0)

# pack the widgets
title_bar.pack(fill=X)
close_button.pack(side=RIGHT,ipadx=7,ipady=1)
expand_button.pack(side=RIGHT,ipadx=7,ipady=1)
minimize_button.pack(side=RIGHT,ipadx=7,ipady=1)
title_bar_title.pack(side=LEFT, padx=10)
window.pack(expand=1, fill=BOTH) # replace this with your main Canvas/Frame/etc.
#xwin=None
#ywin=None
# bind title bar motion to the move window function

def changex_on_hovering(event):
    global close_button
    close_button['bg']='red'
def returnx_to_normalstate(event):
    global close_button
    close_button['bg']=RGRAY

def change_size_on_hovering(event):
    global expand_button
    expand_button['bg']=LGRAY
def return_size_on_hovering(event):
    global expand_button
    expand_button['bg']=RGRAY

def changem_size_on_hovering(event):
    global minimize_button
    minimize_button['bg']=LGRAY
def returnm_size_on_hovering(event):
    global minimize_button
    minimize_button['bg']=RGRAY




def get_pos(event): # this is executed when the title bar is clicked to move the window

    if root.maximized == False:
        
        xwin = root.winfo_x()
        ywin = root.winfo_y()
        startx = event.x_root
        starty = event.y_root

        ywin = ywin - starty
        xwin = xwin - startx

        def move_window(event): # runs when window is dragged
            root.config(cursor="fleur")
            root.geometry(f'+{event.x_root + xwin}+{event.y_root + ywin}')


        def release_window(event): # runs when window is released
            root.config(cursor="arrow")
            
        title_bar.bind('<B1-Motion>', move_window)
        title_bar.bind('<ButtonRelease-1>', release_window)
        title_bar_title.bind('<B1-Motion>', move_window)
        title_bar_title.bind('<ButtonRelease-1>', release_window)
        if winodow_icon != "": 
            widget_icon.bind('<B1-Motion>', move_window)
            widget_icon.bind('<ButtonRelease-1>', release_window)

    else:
        expand_button.config(text=" 🗖 ")
        root.maximized = not root.maximized
        
        
        


title_bar.bind('<Button-1>', get_pos) # so you can drag the window from the title bar
title_bar_title.bind('<Button-1>', get_pos) # so you can drag the window from the title 
if winodow_icon != "": 
    widget_icon.bind('<Button-1>', get_pos)


# button effects in the title bar when hovering over buttons

close_button.bind('<Enter>',changex_on_hovering)
close_button.bind('<Leave>',returnx_to_normalstate)
minimize_button.bind('<Enter>', changem_size_on_hovering)
minimize_button.bind('<Leave>', returnm_size_on_hovering)
if root.resizable == True:
    expand_button.bind('<Enter>', change_size_on_hovering)
    expand_button.bind('<Leave>', return_size_on_hovering)



# resize the window width =======================================================================
if root.resizable == True:
    resizex_widget = Frame(window,bg=DGRAY,cursor='sb_h_double_arrow')
    resizex_widget.pack(side=RIGHT,ipadx=2,fill=Y)


def resizex(event):
    if root.resizable == True and root.maximized == False:
        xwin = root.winfo_x()

        difference = (event.x_root - xwin) - root.winfo_width()

        if root.winfo_width() > 150 : # 150 is the minimum width for the window
            try:
                root.geometry(f"{ root.winfo_width() + difference }x{ root.winfo_height() }")
            except:
                pass
        else:
            if difference > 0: # so the window can't be too small (150x150)
                try:
                    root.geometry(f"{ root.winfo_width() + difference }x{ root.winfo_height() }")
                except:
                    pass


        resizex_widget.config(bg=DGRAY)

if root.resizable == True:
    resizex_widget.bind("<B1-Motion>",resizex)



# resize the window height =======================================================================


if root.resizable == True:
    resizey_widget = Frame(window,bg=DGRAY,cursor='sb_v_double_arrow')
    resizey_widget.pack(side=BOTTOM,ipady=2,fill=X)

def resizey(event):
    if root.resizable == True and root.maximized == False:
        ywin = root.winfo_y()

        difference = (event.y_root - ywin) - root.winfo_height()

        if root.winfo_height() > 150: # 150 is the minimum height for the window
            try:
                root.geometry(f"{ root.winfo_width()  }x{ root.winfo_height() + difference}")
            except:
                pass
        else:
            if difference > 0: # so the window can't be too small (150x150)
                try:
                    root.geometry(f"{ root.winfo_width()  }x{ root.winfo_height() + difference}")
                except:
                    pass

        resizex_widget.config(bg=DGRAY)
if root.resizable == True:
    resizey_widget.bind("<B1-Motion>",resizey)





# some settings
root.bind("<FocusIn>",deminimize) # to view the window by clicking on the window icon on the taskbar
root.after(10, lambda: set_appwindow(root)) # to see the icon on the task bar






#YOUR CODE GOES HERE==================================================================================





#Label(window,text="Hello :D",bg=DGRAY,fg="#fff").pack(expand=1) # example 





# ===================================================================================================


root.mainloop()



