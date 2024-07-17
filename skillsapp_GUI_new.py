import tkinter as tk
from tkinter import ttk, messagebox
import pymysql

# Define global variables
skills_treeview = None
window = None
window_top = None
window_low = None


# Database connection details
rds_host = '127.0.0.1'
username = 'test'
password = 'test123'
db_name = 'progress'

# Create the database connection
db = pymysql.connect(host=rds_host, user=username,
                     password=password, database=db_name)
cr = db.cursor()

# Function to authenticate login


def authenticate_login():

    entered_username = username_entry.get()
    entered_password = password_entry.get()
    cr.execute(
        f"SELECT * FROM user WHERE User_Name = '{entered_username}' AND Pass ='{entered_password}'")
    test = cr.fetchone()

    if test != None:
        # Successful login, open the main application window
        login_window.destroy()
        cr.execute(
            f"SELECT User_ID FROM user WHERE User_Name = '{entered_username}'")
        user_id = cr.fetchone()[0]
        global u_id
        u_id = user_id
        open_main_window()
    else:
        # Invalid login, show error message
        messagebox.showerror(
            title="Error", message="Invalid username or password.")

# Function to open the main application window


def open_main_window():
    global window, skills_treeview
    window = tk.Tk()
    window.title("Skills App")

    # Create a frame for the window
    frame = tk.Frame(window)
    frame.pack()

    # Create a style to configure the treeview
    style = ttk.Style(window)
    style.theme_use("clam")
    style.configure("Treeview",
                    background="#D3D3D3",
                    foreground="black",
                    fieldbackground="#D3D3D3")
    style.map("Treeview", background=[("selected", "#347083")])

    # Create the treeview table
    skills_treeview = ttk.Treeview(frame, columns=(
        "Skill Name", "Progress", "Start Date", "End Date", "Skill Field", "User ID"), show="headings")
    for col in ("Skill Name", "Progress", "Start Date", "End Date", "Skill Field", "User ID"):
        skills_treeview.column(col, width=150, anchor="center", stretch=True)

    skills_treeview.heading("Skill Name", text="Skill Name")
    skills_treeview.heading("Progress", text="Progress")
    skills_treeview.heading("Start Date", text="Start Date")
    skills_treeview.heading("End Date", text="End Date")
    skills_treeview.heading("Skill Field", text="Skill Field")
    skills_treeview.heading("User ID", text="User ID")

    data = cr.execute(f"select * from skills where User_ID={u_id}")
    data = cr.fetchall()

    # Insert sample data into the treeview
    for row in data:
        skills_treeview.insert("", tk.END, values=row)

    skills_treeview.pack(pady=10)

    # Create buttons for editing and deleting skills
    edit_button = tk.Button(frame, text="Edite Skill", bg="#347083",
                            fg="#FFFFFF", font=("Arial", 16), command=edit_skill)
    edit_button.pack(side=tk.LEFT, padx=5, pady=10)

    insert_button = tk.Button(frame, text="Insert Skill", bg="#347083",
                              fg="#FFFFFF", font=("Arial", 16), command=insert_skill)
    insert_button.pack(side=tk.LEFT, padx=5, pady=10)

    delete_button = tk.Button(frame, text="Delete Skill", bg="#347083",
                              fg="#FFFFFF", font=("Arial", 16), command=delete_skill)
    delete_button.pack(side=tk.LEFT, padx=5, pady=10)

    # Create buttons for top, and low skills
    top_button = tk.Button(frame, text="Top Skills", bg="#347083",
                           fg="#FFFFFF", font=("Arial", 16), command=topSkills)
    top_button.pack(side=tk.LEFT, padx=5, pady=10)

    low_button = tk.Button(frame, text="Low Skills", bg="#347083",
                           fg="#FFFFFF", font=("Arial", 16), command=lowSkills)
    low_button.pack(side=tk.LEFT, padx=5, pady=10)

    # Run the main loop
    window.mainloop()

# Function to handle editing a skill


def edit_skill():
    selected_item = skills_treeview.focus()
    if selected_item:
        skill_data = skills_treeview.item(selected_item)['values']
        edit_window = tk.Toplevel(window)
        edit_window.title("Edit Skill")

        # Create a frame for the edit window
        frame = tk.Frame(edit_window)
        frame.pack()

        # Create labels and entry fields for each skill attribute
        skill_name_label = tk.Label(frame, text="Skill Name:")
        skill_name_label.grid(row=0, column=0, padx=5, pady=5)
        skill_name_entry = tk.Entry(frame)
        skill_name_entry.grid(row=0, column=1, padx=5, pady=5)
        skill_name_entry.insert(tk.END, skill_data[0])

        progress_label = tk.Label(frame, text="Progress:")
        progress_label.grid(row=1, column=0, padx=5, pady=5)
        progress_entry = tk.Entry(frame)
        progress_entry.grid(row=1, column=1, padx=5, pady=5)
        progress_entry.insert(tk.END, skill_data[1])

        start_date_label = tk.Label(frame, text="Start Date:")
        start_date_label.grid(row=2, column=0, padx=5, pady=5)
        start_date_entry = tk.Entry(frame)
        start_date_entry.grid(row=2, column=1, padx=5, pady=5)
        start_date_entry.insert(tk.END, skill_data[2])

        end_date_label = tk.Label(frame, text="End Date:")
        end_date_label.grid(row=3, column=0, padx=5, pady=5)
        end_date_entry = tk.Entry(frame)
        end_date_entry.grid(row=3, column=1, padx=5, pady=5)
        end_date_entry.insert(tk.END, skill_data[3])

        field_label = tk.Label(frame, text="Skill Field:")
        field_label.grid(row=4, column=0, padx=5, pady=5)
        field_entry = tk.Entry(frame)
        field_entry.grid(row=4, column=1, padx=5, pady=5)
        field_entry.insert(tk.END, skill_data[4])

        User_ID_label = tk.Label(frame, text="User ID:")
        User_ID_label.grid(row=5, column=0, padx=5, pady=5)
        User_ID_entry = tk.Entry(frame)
        User_ID_entry.grid(row=5, column=1, padx=5, pady=5)
        User_ID_entry.insert(tk.END, skill_data[5])

        def save_changes():
            new = (skill_name_entry.get(), progress_entry.get(), start_date_entry.get(
            ), end_date_entry.get(), field_entry.get().strip().title(), User_ID_entry.get())

        # Execute the update
            cr.callproc('UpdateSkill', (new[0], new[0], new[1], new[2],
                        new[3], new[4], new[5]))

            db.commit()
        

            skills_treeview.item(selected_item, values=new)
            messagebox.showinfo("Success", "Skill updated successfully.")
            edit_window.destroy()

        save_button = tk.Button(
            frame, text="Save Changes", command=save_changes)
        save_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

    else:
        messagebox.showerror("Error", "No skill selected.")

# Function to handle inserting a skill


def insert_skill():

    def submit_skill():
        skill_name = skill_name_entry.get().strip().title()
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()
        skill_progress = skill_progress_entry.get()
        User_ID = User_ID_entry.get()
        skill_field = skill_Field_entry.get().strip().title()

        row_inserted = (skill_name, skill_progress, start_date, end_date,
                        skill_field, User_ID)
        skills_treeview.insert("", tk.END, values=row_inserted)
        skills_treeview.pack(pady=10)

        cr.callproc('InsertSkill', (skill_name, skill_progress,start_date, end_date, skill_field, User_ID))
        db.commit()
        
        def clear_form():
            skill_name_entry.delete(0, tk.END)
            start_date_entry.delete(0, tk.END)
            end_date_entry.delete(0, tk.END)
            skill_progress_entry.delete(0, tk.END)
            User_ID_entry.delete(0, tk.END)
            skill_Field_entry.delete(0, tk.END)
        clear_form()

    root = tk.Toplevel()
    root.title("skill Details Form")
    root.geometry('600x450')
    root.configure()
    frame = tk.Frame(root)
    frame.pack()

    # Create and place form elements
    skill_name_label = tk.Label(frame, text="Skill Name:",
                                bg='#347083', fg="#FFFFFF", font=("Arial", 16))
    skill_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
    skill_name_entry = tk.Entry(frame, font=("Arial", 16))
    skill_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    start_date_label = tk.Label(frame, text="Start Date:",
                                bg='#347083', fg="#FFFFFF", font=("Arial", 16))
    start_date_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    start_date_entry = tk.Entry(frame, font=("Arial", 16))
    start_date_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    end_date_label = tk.Label(frame, text="End Date:",
                              bg='#347083', fg="#FFFFFF", font=("Arial", 16))
    end_date_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    end_date_entry = tk.Entry(frame, font=("Arial", 16))
    end_date_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    skill_progress_label = tk.Label(frame, text="Skill Progress:",
                                    bg='#347083', fg="#FFFFFF", font=("Arial", 16))
    skill_progress_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
    skill_progress_entry = tk.Entry(frame, font=("Arial", 16))
    skill_progress_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    User_ID_label = tk.Label(frame, text="User ID:",
                             bg='#347083', fg="#FFFFFF", font=("Arial", 16))
    User_ID_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
    User_ID_entry = tk.Entry(frame, font=("Arial", 16))
    User_ID_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

    skill_Field_label = tk.Label(frame, text="Skill Field",
                                 bg='#347083', fg="#FFFFFF", font=("Arial", 16))
    skill_Field_label.grid(row=5, column=0, padx=10, pady=5, sticky="e")
    skill_Field_entry = tk.Entry(frame, font=("Arial", 16))
    skill_Field_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")

    submit_button = tk.Button(frame, text="Submit", bg="#347083",
                              fg="#FFFFFF", font=("Arial", 16), command=submit_skill)
    submit_button.grid(row=6, column=0, columnspan=2, pady=10)
    # Run the Tkinter event loop
    root.mainloop()
    

# Function to handle deleteing a skill


def delete_skill():
    selected_item = skills_treeview.focus()
    if selected_item:
        skill_name = selected_item[0]
        cr.callproc('DeleteSkill', (skill_name))
        db.commit()
        
        skills_treeview.delete(selected_item)
        messagebox.showinfo("Success", "Skill deleted successfully.")
    else:
        messagebox.showerror("Error", "No skill selected.")

# Function to show top skills


def topSkills():
    top_skills_window = tk.Toplevel(window_top)
    top_skills_window.title("Top Skills")
    top_skills_window.geometry("400x400")

    cr.execute("SELECT Skill_Name,Progress FROM skills WHERE Progress >= '70'")

    results_top = cr.fetchall()

    db.commit()

    result_dict_top = {}

    for row in results_top:
        key = row[0]
        value = row[1]
        result_dict_top[key] = value

    sorted_skills = sorted(result_dict_top.items(),
                           key=lambda x: int(x[1]), reverse=True)

    for (key, value) in (sorted_skills):
        skill_label = tk.Label(
            top_skills_window, text=f"{key}:  {value}%",  bg='#347083', fg="#FFFFFF", font=("Arial", 16))
        skill_label.pack(side=tk.TOP, padx=5, pady=10)

# Function to show low skills


def lowSkills():
    low_skills_window = tk.Toplevel(window_low)
    low_skills_window.title("Low Skills")
    low_skills_window.geometry("400x400")

    cr.execute("SELECT Skill_Name,Progress FROM skills WHERE Progress <= '70'")

    results_low = cr.fetchall()

    db.commit()

    result_dict_low = {}

    for row in results_low:
        key = row[0]
        value = row[1]
        result_dict_low[key] = value

    sorted_skills = sorted(result_dict_low.items(),
                           key=lambda x: int(x[1]), reverse=False)

    for key, value in sorted_skills:
        skill_label = tk.Label(
            low_skills_window, text=f"{key}:  {value}%",  bg='#347083', fg="#FFFFFF", font=("Arial", 16))
        skill_label.pack(side=tk.TOP, padx=5, pady=10)


# Function to handle signup
def signup():
    signup_window = tk.Toplevel()
    signup_window.title("Signup")

    # Create a frame for the signup window
    frame = tk.Frame(signup_window)
    frame.pack()

    # Creating widgets for the signup window
    signup_label = tk.Label(frame, text="Signup",
                            bg='#347083', fg="#FFFFFF", font=("Arial", 30))
    username_label = tk.Label(frame, text="Username",
                              bg='#347083', fg="#FFFFFF", font=("Arial", 16))
    email_label = tk.Label(frame, text="Email",
                           bg='#347083', fg="#FFFFFF", font=("Arial", 16))
    password_label = tk.Label(frame, text="Password",
                              bg='#347083', fg="#FFFFFF", font=("Arial", 16))
    confirm_password_label = tk.Label(frame, text="Confirm Password",
                                      bg='#347083', fg="#FFFFFF", font=("Arial", 16))
    user_id_label = tk.Label(frame, text="User ID",
                             bg='#347083', fg="#FFFFFF", font=("Arial", 16))
    job_profile_label = tk.Label(frame, text="Job Profile",
                                 bg='#347083', fg="#FFFFFF", font=("Arial", 16))

    username_entry = tk.Entry(frame, font=("Arial", 16))
    email_entry = tk.Entry(frame, font=("Arial", 16))
    password_entry = tk.Entry(frame, show="*", font=("Arial", 16))
    confirm_password_entry = tk.Entry(frame, show="*", font=("Arial", 16))
    user_id_entry = tk.Entry(frame, font=("Arial", 16))
    job_profile_entry = tk.Entry(frame, font=("Arial", 16))

    def save_signup():
        username = username_entry.get()
        user_id = user_id_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        job_profile = job_profile_entry.get()

        # Insert the new user into the database
        cr.callproc('InsertUser', (username, user_id,
                    email, password, job_profile))
        db.commit()

        # Show success message
        messagebox.showinfo("Success", "Signup successful. You can now login.")
        signup_window.destroy()

    signup_button = tk.Button(frame, text="Signup", bg="#347083",
                              fg="#FFFFFF", font=("Arial", 16), command=save_signup)

    # Placing widgets for the signup window
    signup_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
    username_label.grid(row=1, column=0)
    username_entry.grid(row=1, column=1, pady=20)
    email_label.grid(row=2, column=0)
    email_entry.grid(row=2, column=1, pady=20)
    password_label.grid(row=3, column=0)
    password_entry.grid(row=3, column=1, pady=20)
    confirm_password_label.grid(row=4, column=0)
    confirm_password_entry.grid(row=4, column=1, pady=20)
    user_id_label.grid(row=5, column=0)
    user_id_entry.grid(row=5, column=1, pady=20)
    job_profile_label.grid(row=6, column=0)
    job_profile_entry.grid(row=6, column=1, pady=20)
    signup_button.grid(row=7, column=0, columnspan=2, pady=30)


# Create the login window
login_window = tk.Tk()
login_window.title("Login")
login_window.geometry('600x450')
login_window.configure()

# Create a frame for the login window
frame = tk.Frame(login_window)
frame.pack()

# Creating widgets for the login window
login_label = tk.Label(frame, text="Login",
                       bg='#347083', fg="#FFFFFF", font=("Arial", 30))
username_label = tk.Label(frame, text="Username",
                          bg='#347083', fg="#FFFFFF", font=("Arial", 16))
password_label = tk.Label(frame, text="Password",
                          bg='#347083', fg="#FFFFFF", font=("Arial", 16))
username_entry = tk.Entry(frame, font=("Arial", 16))
password_entry = tk.Entry(frame, show="*", font=("Arial", 16))
login_button = tk.Button(frame, text="Login", bg="#347083",
                         fg="#FFFFFF", font=("Arial", 16), command=authenticate_login)
signup_button = tk.Button(frame, text="Signup", bg="#347083",
                          fg="#FFFFFF", font=("Arial", 16), command=signup)

# Placing widgets for the login window
login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
username_label.grid(row=1, column=0)
username_entry.grid(row=1, column=1, pady=20)
password_label.grid(row=2, column=0)
password_entry.grid(row=2, column=1, pady=20)
login_button.grid(row=3, column=0, pady=10)
signup_button.grid(row=3, column=1, pady=10)

# Run the login window
login_window.mainloop()
