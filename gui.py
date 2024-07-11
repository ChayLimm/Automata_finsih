import tkinter
from customtkinter import CTk, CTkFrame, CTkLabel, CTkEntry, CTkButton
from function import FiniteAutomaton
import numpy as np
from fake_automaton import FakeAutomaton
import subprocess
file_name = 'gui.py'


# Global variables
entries_state1 = []
entries_state2 = []
entries_symbol = []
transitions= []
entries = []
fa = None
count = 3
labeldfa = None
labelmin = None
arr = []

def onClick():
    global fa
    arr.clear()
    transitions.clear()
    # alov yg prepare state sen (unique state)
    for i in range(count -2):
        arr.append(entries_state1[i].get())
        arr.append(entries_state2[i].get())
    
    unique_states = list(set(arr))
    print(unique_states)

    print(arr)
    # prepare transition mdong
    for i in range (count-2):
        state1 = entries_state1[i].get()
        state2 = entries_state2[i].get()
        symbol = entries_symbol[i].get()
        if state1 and state2:
            if not symbol : 
                transitions.append((state1, state2, "ε"))
                print(f"added {state1}  {state2} ε")
            transitions.append((state1, state2, symbol))
            print(f"added {state1}  {state2}  {symbol}")
        else :
            error_label.configure(text="All fields must be filled.")
            return


    #prepare start state hz final state
    start_state = starter[0].get()
    accepting_states_str = starter[1].get()
    accepting_states = set(accepting_states_str.split())
    print(f"start {start_state} final {accepting_states}")
    
    
    fa = FiniteAutomaton(unique_states, transitions, start_state, accepting_states)
    fake = FakeAutomaton(unique_states, transitions, start_state, accepting_states)
    # Generate FA image
    fake.generate_fa_image("nfa.png")
    # Convert NFA to DFA
    dfa = fa.convert_to_dfa()
    dfa.generate_fa_image("dfa.png")
    # Minimize DFA
    minimized_dfa = dfa.minimize_dfa()
    minimized_dfa.generate_fa_image("mindfa.png")       
    update_image()

def update_image():
    global label
    new_image_path = "nfa.png"  # Update this with the path to the new image
    new_image = tkinter.PhotoImage(file=new_image_path)
    if label:
        label.destroy()  # Destroy the previous label if it exists
    label = CTkLabel(master=frameimg, image=new_image, text="")
    label.image = new_image  # Keep a reference to prevent garbage collection
    label.pack()

def minimizedfa():
    all_filled = True
    for row in entries:
        for entry in row:
            if not entry.get():
                error_label.configure(text="All fields must be filled.")
                all_filled = False
                break
        if not all_filled:
            break

    if all_filled:
        global labelmin

        new_image_path = "mindfa.png"  # Update this with the path to the new image
        new_image = tkinter.PhotoImage(file=new_image_path)
        if labelmin:
            labelmin.destroy()  # Destroy the previous labelmin if it exists
        labelmin = CTkLabel(master=framemini, image=new_image, text="")
        labelmin.image = new_image  # Keep a reference to prevent garbage collection
        labelmin.pack()

def update_imagedfa():
    global labeldfa
    labeldfa = CTkLabel(master=container, text="DFA", width=100, height=40,fg_color="#FAF9F6", corner_radius=5)
    labeldfa.grid(row=1, column=1, padx=10, pady=10)
    # Check if all fields are filled
    all_filled = True
    for row in entries:
        for entry in row:
            if not entry.get():
                error_label.configure(text="All fields must be filled.")
                all_filled = False
                break
        if not all_filled:
            break

    if all_filled:
        new_image_pathdfa = "dfa.png"  # Update this with the path to the new image
        new_imagedfa = tkinter.PhotoImage(file=new_image_pathdfa)
        if labeldfa:
            labeldfa.destroy()  # Destroy the previous label if it exists
        labeldfa = CTkLabel(master=framedfa, image=new_imagedfa, text="")
        labeldfa.image = new_imagedfa  # Keep a reference to prevent garbage collection
        labeldfa.pack()

def addRow():
    global count
    if count >= 2 + 18:  # 2 is default
        error_label.configure(text="Row maximum 10")
        return
    else:
        state = CTkEntry(master=frame, placeholder_text="state..")
        state.grid(row=count, column=0, padx=10, pady=10)
        entries_state1.append(state)

        tostate = CTkEntry(master=frame, placeholder_text="to...")
        tostate.grid(row=count, column=1, padx=10, pady=10)
        entries_state2.append(tostate)

        symbol = CTkEntry(master=frame, placeholder_text="symbol..")
        symbol.grid(row=count, column=2, padx=10, pady=10)
        entries_symbol.append(symbol)

        # Add the new row of entries to the entries list
        entries.append([state, tostate, symbol])
        
        count += 1

def deleteRow():
    global count
    if count > 3:
        # Remove the last row of entries
        last_row = entries.pop()
        for entry in last_row:
            entry.destroy()
        
        # Also remove the entries from the individual lists
        entries_state1.pop()
        entries_state2.pop()
        entries_symbol.pop()

        count -= 1
        error_label.configure(text="")
    else:
        error_label.configure(text="No more rows to delete.")

def resetAll():
    app.destroy()
    subprocess.run(['python3', file_name], check=True)


def test_deterministic():
    global fa

    if fa.is_deterministic():
        string_accepted_label.configure(text="Deterministic", text_color="#2FC92C")
    else:
        string_accepted_label.configure(text="NOT Deterministic", text_color="#424949")

def functionteststring():
    global fa
    if fa:
        string = test_string[0].get()
        if fa.accepts_string(string):
            string_accepted_label.configure(text="String accepted", text_color="#FAF9F6")
        else:
            string_accepted_label.configure(text="Not accepted", text_color="#FAF9F6")
    else:
        error_label.configure(text="Please create automaton first.")

def main():
    global app, label, labeldfa, labelmin, frameimg, framedfa, framemini, frame, frameBtn, error_label, test_string, starter, string_accepted_label, container, label1

    app = CTk()
    app.geometry("2160x1080")
    app.title("Automata")

    # Answer frame
    frameAns = CTkFrame(master=app, fg_color="#424949")
    frameAns.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")

    # Container for image
    container = CTkFrame(master=frameAns, fg_color="#424949")
    container.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

    # Test acception string
    acceptionframe = CTkFrame(master=frameAns, border_color="black")
    acceptionframe.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Button frame
    frameBtn = CTkFrame(master=app, fg_color="#424949")
    frameBtn.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Frame input
    frame = CTkFrame(master=app, fg_color="#424949")
    frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    labelfa = CTkLabel(master=container, text="Fa", width=100, height=40, fg_color="#2b2b2b", corner_radius=5)
    labelfa.grid(row=1, column=0, padx=10, pady=10)
    labeldfa = CTkLabel(master=container, text="DFA", width=100, height=40,fg_color="#2b2b2b", corner_radius=5)
    labeldfa.grid(row=1, column=1, padx=10, pady=10)
    labelmindfa = CTkLabel(master=container, text="Minimized DFA", width=120, height=40,fg_color="#2b2b2b", corner_radius=5)
    labelmindfa.grid(row=1, column=2, padx=10, pady=10)

    # Frame image
    frameimg = CTkFrame(master=container, fg_color="#FAF9F6")
    frameimg.grid(row=3, column=0, padx=20, pady=20, sticky="nsew")

    # DFA frame
    framedfa = CTkFrame(master=container, fg_color="#FAF9F6")
    framedfa.grid(row=3, column=1, padx=20, pady=20, sticky="nsew")

    # Minimize DFA frame
    framemini = CTkFrame(master=container, fg_color="#FAF9F6")
    framemini.grid(row=3, column=2, padx=20, pady=20, sticky="nsew")

    # Starting of the app
    start_final_frame = CTkFrame(master=frame, border_color="black")
    start_final_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

    starter = []
    label3 = CTkLabel(master=start_final_frame, text="Start/Final:")
    label3.grid(row=0, column=0, padx=30, pady=10)
    start = CTkEntry(master=start_final_frame, placeholder_text="start..")
    start.grid(row=0, column=1, padx=30, pady=10)
    starter.append(start)

    final = CTkEntry(master=start_final_frame, placeholder_text="final..")
    final.grid(row=0, column=2, padx=10, pady=10)
    starter.append(final)

    # Create labels
    label = CTkLabel(master=frame, text="State")
    label.grid(row=1, column=0, padx=10, pady=10)
    label1 = CTkLabel(master=frame, text="TO State")
    label1.grid(row=1, column=1, padx=10, pady=10)
    label2 = CTkLabel(master=frame, text="Symbol")
    label2.grid(row=1, column=2, padx=10, pady=10)

    # Create initial set of entry widgets
    initial_row = []

    state = CTkEntry(master=frame, placeholder_text="state..")
    state.grid(row=2, column=0, padx=10, pady=10)
    entries_state1.append(state)

    tostate = CTkEntry(master=frame, placeholder_text="to...")
    tostate.grid(row=2, column=1, padx=10, pady=10)
    entries_state2.append(tostate)

    symbol = CTkEntry(master=frame, placeholder_text="symbol..")
    symbol.grid(row=2, column=2, padx=10, pady=10)
    entries_symbol.append(symbol)

    # Create the buttons
    add_row_button = CTkButton(master=frameBtn, text="Add row", command=addRow)
    add_row_button.grid(row=0, column=0, columnspan=1, pady=10)

    delete_row_button = CTkButton(master=frameBtn, text="Delete row", command=deleteRow)
    delete_row_button.grid(row=1, column=0, columnspan=1, pady=10)

    enter_button = CTkButton(master=frameBtn, text="Enter", command=onClick)
    enter_button.grid(row=2, column=0, columnspan=2, pady=10)

    # Deterministic button
    deterministic = CTkButton(master=frameBtn, text="Test deterministic", command=test_deterministic)
    deterministic.grid(row=3, column=0, padx=10, pady=10, sticky='ne')

    # DFA button
    dfa_button = CTkButton(master=frameBtn, text="Convert to DFA", command=update_imagedfa)
    dfa_button.grid(row=4, column=0, padx=10, pady=10, sticky='ne')

    # Reset button
    reset_button = CTkButton(master=frameBtn, text="Reset", command=resetAll, fg_color="#FF5B41")
    reset_button.grid(row=6, column=0, padx=10, pady=10, sticky='ne')

    # Minimize DFA button
    minimize_button = CTkButton(master=frameBtn, text="Minimize DFA", command=minimizedfa)
    minimize_button.grid(row=5, column=0, padx=10, pady=10, sticky='ne')

    # Create the error label
    error_label = CTkLabel(master=frameBtn, text="", text_color="red")
    error_label.grid(row=7, column=0, padx=10, pady=10)

    # Testing string
    test_string = []

    string = CTkEntry(master=acceptionframe, placeholder_text="test string", width=200, height=40)
    string.grid(row=0, column=1, padx=5, pady=5)
    test_string.append(string)

    enter_button_teststring = CTkButton(master=acceptionframe, text="Test", command=functionteststring, width=60, height=40)
    enter_button_teststring.grid(row=0, column=0, pady=10, padx=10)

    answer_state = CTkLabel(master=acceptionframe, text="Answer : ")
    answer_state.grid(row=1, column=0, padx=15, pady=15)

    string_accepted_label = CTkLabel(master=acceptionframe, text="Test if the string accept or not", fg_color="#424949", padx=10, pady=10, corner_radius= 5)
    string_accepted_label.grid(row=1, column=1, padx=10, pady=10)

    app.mainloop()

if __name__ == "__main__":
    main()
