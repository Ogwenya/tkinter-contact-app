from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from db import Database

db = Database('contacts.db')


root = Tk()
root.title("My Contacts")
root.geometry("620x560")

# tkinter style
style = ttk.Style()
style.theme_use('default')
style.configure('Treeview', background="white", foreground="black", rowheight=25, fieldbackground="white")
style.map('Treeview', background=[('selected', '#333')])

# create a Treeview Frame
tree_frame = Frame(root)
tree_frame.pack(pady=10)

# create Scrollbar
scrollbar = Scrollbar(tree_frame)
scrollbar.pack(side=RIGHT, fill=Y)

# create Treeview
contact_tree = ttk.Treeview(tree_frame, yscrollcommand=scrollbar.set)
contact_tree.pack()

# configure scrollbar
scrollbar.config(command=contact_tree.yview)

# configure contact Treeview
contact_tree['columns'] = ("ID", "Name", "Phone Number", "Email")

contact_tree.column("#0", stretch=NO, width=0)
contact_tree.column("ID", anchor=CENTER, width=50)
contact_tree.column("Name", anchor=W, width=200)
contact_tree.column("Phone Number", anchor=W, width=150)
contact_tree.column("Email", anchor=W, width=200)

contact_tree.heading("#0", text="", anchor=W)
contact_tree.heading("ID", text="ID", anchor=CENTER)
contact_tree.heading("Name", text="Name", anchor=W)
contact_tree.heading("Phone Number", text="Phone Number", anchor=W)
contact_tree.heading("Email", text="Email", anchor=W)

# create stripped rows
contact_tree.tag_configure('oddrow', background="white")
contact_tree.tag_configure('evenrow', background="lightblue")


# edit frame
edit_frame = LabelFrame(root, text=" Double tap on record to edit", pady=20)
edit_frame.pack(fill="x", pady=10, padx=10)

first_name_label = Label(edit_frame, text="First Name*")
first_name_label.grid(row=0, column=0)
first_name_entry = Entry(edit_frame)
first_name_entry.grid(row=1, column=0, padx=20, pady=10, ipadx=40, ipady=5)

last_name_label = Label(edit_frame, text="Last Name")
last_name_label.grid(row=0, column=1)
last_name_entry = Entry(edit_frame)
last_name_entry.grid(row=1, column=1, padx=20, pady=10, ipadx=40, ipady=5)

phone_label = Label(edit_frame, text="Phone Number*")
phone_label.grid(row=2, column=0)
phone_entry = Entry(edit_frame)
phone_entry.grid(row=3, column=0, padx=20, pady=10, ipadx=40, ipady=5)

email_label = Label(edit_frame, text="Email")
email_label.grid(row=2, column=1)
email_entry = Entry(edit_frame)
email_entry.grid(row=3, column=1, padx=20, pady=10, ipadx=40, ipady=5)

# COMMANDS
# clear entry fields after updating, deleting or adding new contact
def clear_entry():
    first_name_entry.delete(0, END)
    last_name_entry.delete(0, END)
    phone_entry.delete(0, END)
    email_entry.delete(0, END)

# select a record for deleting or editing
def select_record():
    clear_entry()
    global selected_item_id
    selected_item = contact_tree.focus()
    selected_item_values = contact_tree.item(selected_item, 'values')

    selected_item_id = selected_item_values[0]

    name = selected_item_values[1].split()

    first_name = name[0]
    last_name = name[1:]

    first_name_entry.insert(0, first_name)
    last_name_entry.insert(0, last_name)
    phone_entry.insert(0, selected_item_values[2])
    email_entry.insert(0, selected_item_values[3])


# create new contact
def new_contact():
    if first_name_entry.get() == '' or phone_entry.get() == '':
        messagebox.showerror('Required Fields', 'first name and phone number is required')
        return
    db.insert(first_name_entry.get(), last_name_entry.get(), phone_entry.get(), email_entry.get())

    clear_entry()

    populate()

# update a contact
def update_contact():
    db.update(selected_item_id, first_name_entry.get(), last_name_entry.get(), phone_entry.get(), email_entry.get())

    clear_entry()
    populate()

# delete a contact
def delete_contact():
    select_item = contact_tree.focus()
    select_item_values = contact_tree.item(select_item, 'values')
    item = select_item_values[0]
    # if selected by single click
    if item:
        db.remove(item)
    else:
        # if selected by double click or using the select button
        db.remove(selected_item_id)

    clear_entry()
    populate()

# binding function(for double click)
def double_clicked(e):
    select_record()

# FETCH CONTACTS FROM DATABASE AND POPULATE TREEVIEW
def populate():
    for record in contact_tree.get_children():
        contact_tree.delete(record)
    global count
    count = 0
    for record in db.fetch():
        if count % 2 == 0:
            contact_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1] + ' ' + record[2], record[3], record[4]), tags=('evenrow',))
        else:
            contact_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1] + ' ' + record[2], record[3], record[4]), tags=('oddrow',))
        count += 1
    return count
# buttons
button_frame = Frame(root)
button_frame.pack()

new_contact = Button(button_frame, text="ADD CONTACT", command=new_contact)
new_contact.grid(row=0, column=0, padx=20)

select_button = Button(button_frame, text="SELECT RECORD", command=select_record)
select_button.grid(row=0, column=1, padx=20)

update_contact = Button(button_frame, text="UPDATE", command=update_contact)
update_contact.grid(row=0, column=2, padx=20)

delete_contact = Button(button_frame, text="DELETE", command=delete_contact)
delete_contact.grid(row=0, column=3, padx=20)

# bindings (populates the entry fields for editing when item is double clicked)
contact_tree.bind("<Double-1>", double_clicked)

# populate contacts to Treeview
populate()

root.mainloop()
