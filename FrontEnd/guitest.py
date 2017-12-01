from tkinter import *

def startGUI():

  	
    root = Tk()

    S = Scrollbar(root)
    chatBox = Frame(width = 500, height = 900, bg="gray")
    S.grid(row=0, column=1)
    chatBox.grid(row=0, column=0)
    S.config(command=chatBox.yview)
    chatBox.config(yscrollcommand=S.set)

    st = StringVar()
    st.set("Enter message here")
    searchBox = Entry(root, textvariable=st, width=45)
    searchBox.grid(row=1, column=0)
    Button(root, text='send', command= lambda: sendMsg(searchBox)).grid(row=1, column=1)
    myThread("client").start()

    Button(root, text='close', command= lambda: close(root)).grid(row=2)
    root.mainloop()
    sys.exit()
    print("broke out here?")