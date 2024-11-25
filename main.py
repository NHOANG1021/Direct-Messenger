'''
Code to implement functionality to run GUI
'''
import tkinter as tk
from tkinter import ttk, simpledialog
import ds_messenger as dsm


class Body(tk.Frame):
    '''
    Represents the body of the GUI where contacts and messages are displayed
    '''
    def __init__(self, root, recipient_selected_callback=None):
        '''
        initializes body of the GUI
        '''
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback

        self._draw()

    def node_select(self, event):
        '''
        Callback function to handle the selection of a contact
        '''
        index = int(self.posts_tree.selection()[0])
        entry = self._contacts[index]
        if self._select_callback is not None:
            self._select_callback(entry)

    def insert_contact(self, contact: str):
        '''
        Inserts a new contact into the GUI
        '''
        self._contacts.append(contact)
        id = len(self._contacts) - 1
        self._insert_contact_tree(id, contact)

    def _insert_contact_tree(self, id, contact: str):
        '''
        Inserts a new contact into the treeview widget
        '''
        if len(contact) > 25:
            entry = contact[:24] + "..."
        id = self.posts_tree.insert('', id, id, text=contact)

    def insert_user_message(self, message: str):
        '''
        Inserts a message sent by the user into the GUI
        '''
        self.entry_editor.insert(1.0, message + '\n', 'entry-right')

    def insert_contact_message(self, message: str):
        '''
        Inserts a message recieved from a contact into the GUI
        '''
        self.entry_editor.insert(1.0, message + '\n', 'entry-left')

    def insert_contact_message_bottom(self, message: str):
        '''
        Inserts a message received from a contact at the bottom of the GUI
        '''
        self.entry_editor.insert(tk.END, message + '\n', 'entry-left')
        self.entry_editor.see(tk.END)

    def get_text_entry(self) -> str:
        '''
        Retrieves text from the message entry widget
        '''
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text: str):
        '''
        Sets text in the message entry widget
        '''
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def _draw(self):
        '''
        Draws the body of the GUI with its widgets
        '''
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="yellow")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5)
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True, padx=0, pady=0)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5)
        self.entry_editor.tag_configure('entry-right',
                                        justify='right',
                                        foreground='red')
        self.entry_editor.tag_configure('entry-left',
                                        justify='left',
                                        foreground='blue')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                               expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    '''
    Represents the footer of the GUI; usually contains the send button
    '''
    def __init__(self, root, send_callback=None):
        '''
        initializes the footer of the GUI
        '''
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._draw()

    def send_click(self):
        '''
        Callback function to handle clicking on the send button
        '''
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        '''
        Draws the footer of the GUi with its widgets
        '''
        save_button = tk.Button(command=self.send_click,
                                master=self,
                                text="Send",
                                width=20)

        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class NewContactDialog(tk.simpledialog.Dialog):
    '''
    Represents a dialog box for adding a new contact
    '''
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        '''
        Initializes the dialog box
        '''
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def body(self, frame):
        '''
        Draws the body of the dialogbox with entry fields
        for the server address, username, and password
        '''
        self.server_label = tk.Label(frame, width=30, text="DS Server Address")
        self.server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.insert(tk.END, self.server)
        self.server_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()

        self.password_label = tk.Label(frame, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, width=30, show='*')
        self.password_entry.insert(tk.END, self.pwd)
        self.password_entry.pack()

    def apply(self):
        '''
        Applies the changes made in the dialog box
        '''
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()


class MainApp(tk.Frame):
    '''
    Represents the main application window
    '''
    def __init__(self, root):
        '''
        Initializes the main application
        '''
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = 'peter'
        self.password = 'joe'
        self.server = '168.235.86.101'
        self.recipient = 'Nicholas'
        self.direct_messenger = dsm.DirectMessenger(username=self.username,
                                                    password=self.password)

        self._draw()
        self.restore_contacts()

    def send_message(self):
        '''
        Sends a message to the selected recipient
        '''
        message = self.body.get_text_entry()

        if self.recipient:
            self.direct_messenger.send(message, self.recipient)
            self.body.insert_user_message(message)

        self.body.set_text_entry('')

    def add_contact(self):
        '''
        Opens a dialog box to add a new contact
        '''
        # prompt the user to enter a new contact name
        new_contact = simpledialog.askstring("Add Contact",
                                             "Enter name of the new contact:")

        if new_contact:
            self.body.insert_contact(new_contact)

    def recipient_selected(self, recipient):
        '''
        Callback function to handle the selection of a recipient
        '''
        self.recipient = recipient
        self.body.entry_editor.delete(1.0, tk.END)
        self.publish(None)

    def configure_server(self):
        '''
        Opens a dialog box to configure server settings
        '''
        ud = NewContactDialog(self.root, "Configure Account",
                              self.username, self.password, self.server)
        self.username = ud.user
        self.password = ud.pwd
        self.server = ud.server
        self.direct_messenger = dsm.DirectMessenger(username=self.username,
                                                    password=self.password,
                                                    server=self.server)
        self.reset_gui()

    def publish(self, message: str):
        '''
        Publishes old messages to display them in the GUI
        '''
        for i in range(len(self.direct_messenger.load_data()) - 1, -1, -1):
            message = self.direct_messenger.load_data()[i].message
            if self.direct_messenger.load_data()[i].recipient == self.recipient:
                self.body.insert_contact_message(message)

        with open('sent.txt', 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()[1:-1]
                data = line.split(', ')
                name = data[1].replace("'", '')
                if name == self.recipient:
                    self.body.insert_user_message(data[0].replace("'", ''))

    def check_new(self):
        '''
        Checks for any new messages
        '''
        self.root.after(500, self.check_new)
        new_msg = self.direct_messenger.retrieve_new()

        for msg in new_msg:
            msg = msg.message
            self.body.insert_contact_message_bottom(msg)

    def restore_contacts(self):
        '''
        Restores contacts of past dms
        '''
        for i in range(len(self.direct_messenger.load_data()) - 1, -1, -1):
            contact = self.direct_messenger.load_data()[i].recipient
            if contact not in self.body._contacts:
                self.body.insert_contact(contact)

    def reset_gui(self):
        '''
        Clears the GUI
        '''
        self.username = ''
        self.password = ''
        self.server = ''
        self.recipient = ''
        self.body.set_text_entry('')
        self.body.entry_editor.delete(1.0, tk.END)
        self.body._contacts = []
        self.body.posts_tree.delete(*self.body.posts_tree.get_children())

    def _draw(self):
        '''
        Draws the main application with its widgets and menus
        '''
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar

        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(label='Add Contact',
                                  command=self.add_contact)
        settings_file.add_command(label='Configure DS Server',
                                  command=self.configure_server)

        # The Body and Footer classes must be initialized and
        # packed into the root window.
        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


if __name__ == "__main__":
    main = tk.Tk()
    main.title("ICS 32 Distributed Social Messenger")
    main.geometry("700x500")
    main.option_add('*tearOff', False)
    app = MainApp(main)
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    id = main.after(2000, app.check_new)
    print(id)
    main.mainloop()
