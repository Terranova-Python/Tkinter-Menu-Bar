from tkinter import *

root=Tk()
root.overrideredirect(True) # turns off title bar, geometry
root.geometry('400x250+700+300') # set new geometry the + 500 + 300 is where it starts on the screen

LGRAY = '#545454'
DGRAY = '#242424'
RGRAY = '#2e2e2e'

title_bar = Frame(root, bg='#2e2e2e', relief='raised', bd=0,highlightthickness=0)

# put a close button on the title bar
close_button = Button(title_bar, text='  X  ', command=root.destroy,bg=RGRAY,padx=2,pady=2,font=("calibri", 10),bd=0,fg='white',highlightthickness=0)
expand_button = Button(title_bar, text=' ■ ',bg=RGRAY,padx=2,pady=2,bd=0,fg='white',font=("calibri", 10),highlightthickness=0)
minimize_button = Button(title_bar, text=' ─ ',bg=RGRAY,padx=2,pady=2,bd=0,fg='white',font=("calibri", 10),highlightthickness=0)
title_bar_title = Label(title_bar, text='App Opener 9000', bg=RGRAY,bd=0,fg='white',font=("helvetica", 10),highlightthickness=0)

# a canvas for the main area of the window, this is where the actual app will go
window = Canvas(root, bg=DGRAY,highlightthickness=0)

# pack the widgets
title_bar.pack(expand=1, fill=X)
close_button.pack(side=RIGHT)
expand_button.pack(side=RIGHT)
minimize_button.pack(side=RIGHT)
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

def get_pos(event):
    xwin = root.winfo_x()
    ywin = root.winfo_y()
    startx = event.x_root
    starty = event.y_root

    ywin = ywin - starty
    xwin = xwin - startx

    def move_window(event):
        root.geometry('+{0}+{1}'.format(event.x_root + xwin, event.y_root + ywin))
    startx = event.x_root
    starty = event.y_root

    title_bar.bind('<B1-Motion>', move_window)
title_bar.bind('<Button-1>', get_pos)

def minimize_me(event):
    #root.overrideredirect(False)
    root.update_idletasks()
    root.overrideredirect(False)
    #root.state('withdrawn')
    root.state('iconic')

def frame_mapped(e):
    print(e)
    root.update_idletasks()
    root.overrideredirect(True)
    root.state('normal')

title_bar.bind('<B1-Motion>', get_pos)
close_button.bind('<Enter>',changex_on_hovering)
close_button.bind('<Leave>',returnx_to_normalstate)
expand_button.bind('<Enter>', change_size_on_hovering)
expand_button.bind('<Leave>', return_size_on_hovering)
minimize_button.bind('<Enter>', changem_size_on_hovering)
minimize_button.bind('<Button-1>', minimize_me)
minimize_button.bind('<Leave>', returnm_size_on_hovering)

title_bar.bind("<Map>",frame_mapped) # Frame Mapped contains the event to un-minimize the screen - 
                                     # calling the override back to True (thus disabling the OG menubar/TitleBar)

root.mainloop()
