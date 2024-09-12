import time

import PostureComputation
# import tkinter as tk
from mttkinter import mtTkinter as tk
from multiprocessing import freeze_support
import threading
import config
from queue import Queue

window_instances = []


def destroy_all_windows(window_instances):
    for window in window_instances:
        window.destroy()


def create_new_window(window_instances):
    new_window = tk.Tk()
    window_instances.append(new_window)
    return new_window


def posture_start():
    print("Posture Start has been entered")
    PostureComputation.postureMain()


def gui_start():
    #  destroy_all_windows(window_instances)
    #  config.exit_flag = False
    print("The Start Menu Is Starting Up")

    # ratio for desired window size (40% width and height of full screen)

    start_menu_ratio = 0.3
    button_offset_y_ratio = 0.5

    # def tester():
    #     print("Tester")
    # start_menu = create_new_window(window_instances)
    start_menu = tk.Tk()

    # Capture the users screen height and width
    screen_width = start_menu.winfo_screenwidth()
    screen_height = start_menu.winfo_screenheight()

    # Calculated desired window size for user
    width = int(screen_width * start_menu_ratio)
    height = int(screen_height * start_menu_ratio)

    start_menu.geometry(f"{width}x{height}")

    start_button = tk.Button(start_menu, text="Start", command=lambda: [start_thread(start_menu)])
    start_button.place(relx=0.8, rely=0.5, anchor=tk.E)
    quit_button = tk.Button(start_menu, text="Quit", command=start_menu.destroy)
    quit_button.place(relx=0.2, rely=0.5, anchor=tk.W)
    start_menu.mainloop()


def on_overlay():
    print("Overlay Activated")
    config.exit_flag = False

    # global overlay_screen
    overlay_screen = tk.Tk()
    overlay_screen.overrideredirect(True)
    overlay_screen.geometry("100x100+400+300")  # Change this to be variables corresponding to the users screen size
    overlay_screen.lift()

    # overlay_screen.after(0, update_overlay_colour)

    config.update_colour_flag = True

    def change_overlay_colour():

        while config.update_colour_flag:

            print("Colour Changing Thread Entered")

            if config.good_posture_flag:
                overlay_screen.config(bg='green')
                print("Status colour has been changed to green")
            else:
                overlay_screen.config(bg='red')
                print("Status colour has been changed to red")

        print("Change Colour Thread Exited")

    def exit_button_clicked():
        config.exit_flag = True
        config.update_colour_flag = False
        overlay_screen.destroy()
        gui_start()

    overlay_screen_exit_button = tk.Button(overlay_screen, text="EXIT",
                                           command=lambda: [exit_button_clicked()])
    # command=lambda: [overlay_screen.destroy(), gui_start()])
    overlay_screen_exit_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    if __name__ == 'gui':
        print("Colour Changing Thread Setup Entered")
        process3 = threading.Thread(target=change_overlay_colour)
        process4 = threading.Thread(target=posture_start)

        process3.start()
        process4.start()

        process3.join()
        process4.join()

        print("Thread 3 and Thread 4 Have Completed")

    # overlay_screen.after(0, update_overlay_colour)

    overlay_screen.mainloop()

    print("Overlay Window Has Been Closed")


def start_thread(start_menu_gui):
    start_menu_gui.destroy()
    config.update_colour_flag = True
    on_overlay()
    print("Start Menu Closed")

    #if __name__ == "guis":
     #   print('Start Button Pressed')
        # freeze_support()

      #  process1 = threading.Thread(target=on_overlay)
        # process2 = threading.Thread(target=posture_start)

       # process1.start()
        # process2.start()

        #destroy_all_windows(window_instances)

        #process1.join()
        # process2.join()

        #print("Both Threads Have Finished")
