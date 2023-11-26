import tkinter as tk
from tkinter import messagebox
import sqlite3

def add_to_database():
    entry_text = entry.get()

    if entry_text:
        try:
            # Connect to the SQLite database
            connection = sqlite3.connect('your_database.db')
            cursor = connection.cursor()

            # Create the table if it doesn't exist
            cursor.execute('CREATE TABLE IF NOT EXISTS your_table (word TEXT)')

            # Insert the entered word into the database
            cursor.execute('INSERT INTO your_table (word) VALUES (?)', (entry_text,))

            # Commit the changes
            connection.commit()

            # Close the connection
            connection.close()

            # Clear the entry box
            entry.delete(0, tk.END)

            # Directly refresh the entries in the main window
            view_entries()
        except Exception as e:
            messagebox.showerror('Error', f'An error occurred: {str(e)}')
    else:
        messagebox.showwarning('Warning', 'Please enter a word.')

def delete_entry(entry_id):
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect('your_database.db')
        cursor = connection.cursor()

        # Delete the selected entry
        cursor.execute('DELETE FROM your_table WHERE rowid=?', (entry_id,))

        # Commit the changes
        connection.commit()

        # Close the connection
        connection.close()

        # Refresh the entries directly in the main window
        view_entries()
    except Exception as e:
        messagebox.showerror('Error', f'An error occurred: {str(e)}')

def view_entries():
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect('your_database.db')
        cursor = connection.cursor()

        # Check if the table exists
        cursor.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='your_table' ''')
        table_exists = cursor.fetchone()

        if table_exists:
            # Fetch all entries from the database, ordered alphabetically by word
            cursor.execute('SELECT rowid, word FROM your_table ORDER BY word')
            entries = cursor.fetchall()

            # Clear the existing entries in the text widget
            entries_text.delete('1.0', tk.END)

            # Display entries directly in the main window with delete buttons
            for entry in entries:
                entry_text = f'Word: {entry[1]}\n'
                entries_text.insert(tk.END, entry_text)

                # Add a line break and create a delete button for each entry
                delete_button = tk.Button(entries_text, text='Delete', command=lambda e=entry[0]: delete_entry(e), bg='#FF5A5A', fg='white', relief=tk.GROOVE)
                entries_text.window_create(tk.END, window=delete_button)
                entries_text.insert(tk.END, '\n\n')

            # Add some color and font to the text widget
            entries_text.tag_configure('bold', font=('Courier New', 12, 'bold'), foreground='white')
            entries_text.tag_add('bold', '1.0', tk.END)
        else:
            # If the table doesn't exist, show a message
            entries_text.delete('1.0', tk.END)
            entries_text.insert(tk.END, "No entries found.")

        # Close the connection
        connection.close()

    except Exception as e:
        messagebox.showerror('Error', f'An error occurred: {str(e)}')

# Create the main window
root = tk.Tk()
root.title('Word Database')
root.geometry('800x600')  # Set the initial size of the window
root.configure(bd=5, relief=tk.SOLID, bg='black')  # Add a black border with a border width of 5 and a dark background

# Create a label for the input box
label = tk.Label(root, text='Add word:', font=('Courier New', 14), bg='black', fg='white')
label.pack(side=tk.LEFT, padx=10)

# Create and pack the entry box
entry = tk.Entry(root, width=20, font=('Courier New', 14), bg='black', fg='white', insertbackground='white')
entry.pack(side=tk.LEFT, pady=10)

# Create and pack the "Add to Database" button
add_button = tk.Button(root, text='Add to Dictionary', command=add_to_database, bg='#008080', fg='white', font=('Courier New', 12), relief=tk.GROOVE)
add_button.pack(side=tk.LEFT, pady=10)

# Create a text widget to display entries
entries_text = tk.Text(root, wrap=tk.WORD, width=60, height=20, font=('Courier New', 12), bg='black', fg='white', bd=0)
entries_text.pack(padx=10, pady=10)

# Directly call the view_entries function to show entries on startup
view_entries()

# Run the Tkinter event loop
root.mainloop()