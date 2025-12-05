import tkinter as tk #It is the main library used to build the GUI
from tkinter import messagebox #To display error messages
import requests # To send an HTTP request to the REST Countries API
from PIL import Image, ImageTk #Used to open and process the flag image , converts the image into a format that tkinter can display
import io   # Used to convert the image bytes into a real image

#Function to get country info from API
def get_country_info(country_name):
    try:
        # Requesting country info from REST Countries API
        response = requests.get(f"https://restcountries.com/v3.1/name/{country_name}")
        data = response.json()

        # If API does not return success code
        if response.status_code != 200:
            messagebox.showerror("Wait!", "There is no country with this name, check it and try again!")
            return 0

        # Extracting needed information
        country_info = {
            "Flag": data[0]['flags']['png'],  # Image URL
            "Name": data[0]['name']['common'],
            "Capital": data[0].get('capital', ['No data'])[0],
            "Population": data[0].get('population', 'No data'),
            "Currency": ', '.join([currency for currency in data[0].get('currencies', {}).keys()]),
        }
        return country_info

    except Exception as e:
        # If internet connection fails or any unknown error
        messagebox.showerror("Wait!", "Check your internet and try again!")
        return 0


# ------------------ Show the info in a new window ------------------
def show_country_info():
    country_name = country_entry.get()
    country_info = get_country_info(country_name)

    if country_info:
        show_data_window(country_info)


#Second window that displays the flag + data
def show_data_window(country_info):
    # Creating a new popup window
    new_window = tk.Toplevel(window)
    new_window.title(f"Information about {country_info['Name']}")
    new_window.geometry("600x450")
    new_window.config(bg="#003366")

    # Style used for text labels
    text_style = {"font": ("Arial", 18), "fg": "white", "bg": "#003366"}

    #Load and Display the Flag
    try:
        flag_response = requests.get(country_info["Flag"])  # Getting image data
        flag_data = flag_response.content
        flag_img = Image.open(io.BytesIO(flag_data))         # Converting bytes to image
        flag_img = flag_img.resize((170, 110))               # Resizing for better fit
        flag_photo = ImageTk.PhotoImage(flag_img)

        flag_label = tk.Label(new_window, image = flag_photo, bg="#003366")
        flag_label.image = flag_photo  # Prevent Python from deleting the image
        flag_label.place(relx=0.5, rely=0.15, anchor="center")

    except:
        tk.Label(new_window, text="Flag: Not Available", **text_style).place(relx=0.5, rely=0.15, anchor="center")

    # =============== Show Text Information ===============
    tk.Label(new_window, text=f"Name : {country_info['Name']}", **text_style).place(relx=0.5, rely=0.35, anchor="center")
    tk.Label(new_window, text=f"Capital : {country_info['Capital']}", **text_style).place(relx=0.5, rely=0.45, anchor="center")
    tk.Label(new_window, text=f"Population : {country_info['Population']}", **text_style).place(relx=0.5, rely=0.55, anchor="center")
    tk.Label(new_window, text=f"Currency : {country_info['Currency']}", **text_style).place(relx=0.5, rely=0.65, anchor="center")


#Main Window UI
window = tk.Tk()
window.title("Country Info App")
window.geometry("600x500")
window.config(bg="#f0f0f0")

#Loading Background Image
bg_img_path = "earth.jpeg"
bg_img = Image.open(bg_img_path)
bg_img = bg_img.resize((600, 500))
bg_photo = ImageTk.PhotoImage(bg_img)

bg_label = tk.Label(window, image = bg_photo)
bg_label.place(relwidth=1, relheight=1)

# Frame to hold entry + button
frame = tk.Frame(window, bg="#f0f0f0", bd=5)
frame.place(relx=0.5, rely=0.5, anchor="center")

# Label for entry
country_label = tk.Label(frame, text="Write the country name:", font=("Arial", 14), bg="#f0f0f0", fg="#003366")
country_label.pack(pady=10)

# Text entry for country name
country_entry = tk.Entry(frame, font=("Arial", 14), width=30)
country_entry.pack(pady=10)

# Search button
search_button = tk.Button(frame, text="Go !!", font=("Arial", 16), command=show_country_info,
                          bg="#003366", fg="white", padx=50, pady=5)
search_button.pack(pady=20)

# Start the Tkinter loop
window.mainloop()
