import instaloader
import tkinter
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO

# Instaloader instance
x = instaloader.Instaloader()

# Function to get user info for the user profile
def get_user_info():
    usrName = user_name_entry.get()
    
    if not usrName:
        messagebox.showerror("Error", "Please enter a username.")
        return
    
    try:
        profile = instaloader.Profile.from_username(x.context, usrName)
        
        privacy_status = "Private" if profile.is_private else "Public"
        user_id_label.config(text=f"User Id: {profile.userid}")
        user_followers_label.config(text=f"Followers: {profile.followers}")
        user_following_label.config(text=f"Following: {profile.followees}")
        user_post_label.config(text=f"Posts: {profile.mediacount}")
        privacy_status_label.config(text=f"Privacy Status: {privacy_status}")
        user_bio_label.config(text=f"Bio: {profile.biography[:100]}...")  # Show first 100 characters of bio
        
        # Load and display profile image
        response = requests.get(profile.profile_pic_url)
        image_data = BytesIO(response.content)
        profile_pic = Image.open(image_data)
        profile_pic.thumbnail((150, 150))
        profile_pic = ImageTk.PhotoImage(profile_pic)
        profile_pic_label.config(image=profile_pic)
        profile_pic_label.image = profile_pic
        profile_pic_label.place(x=255, y=130)

        # Display recent posts as thumbnails
        posts_frame.delete("all")  # Clear previous thumbnails
        posts = profile.get_posts()
        for index, post in enumerate(posts):
            if index >= 3:  # Show only the latest 3 posts
                break
            response = requests.get(post.url)
            image_data = BytesIO(response.content)
            post_image = Image.open(image_data)
            post_image.thumbnail((75, 75))
            post_image = ImageTk.PhotoImage(post_image)
            posts_frame.create_image(index * 80, 0, anchor='nw', image=post_image)
            posts_frame.image = post_image

    except instaloader.exceptions.ProfileNotExistsException:
        messagebox.showerror("Error", "No profile associated with this username found.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create a tkinter window
window = tkinter.Tk()
window.title("Instagram User Info")
window.minsize(width=600, height=500)

# Username input field
user_name_entry = tkinter.Entry(width=27)
user_name_entry.place(x=210, y=48)

# Labels
enter_user_name_label = tkinter.Label(text="Enter UserName:", font=("Arial", 16))
enter_user_name_label.place(x=9, y=50)

user_id_label = tkinter.Label(text="User Id: ", font=("Arial", 16))
user_id_label.place(x=9, y=100)

user_followers_label = tkinter.Label(text="Followers: ", font=("Arial", 16))
user_followers_label.place(x=9, y=150)

user_following_label = tkinter.Label(text="Following: ", font=("Arial", 16))
user_following_label.place(x=9, y=200)

user_post_label = tkinter.Label(text="Posts: ", font=("Arial", 16))
user_post_label.place(x=9, y=250)

privacy_status_label = tkinter.Label(text="Privacy Status: ", font=("Arial", 16))
privacy_status_label.place(x=9, y=300)

user_bio_label = tkinter.Label(text="Bio: ", font=("Arial", 14), wraplength=500, justify="left")
user_bio_label.place(x=9, y=350)

# Get Info button
get_info_button = tkinter.Button(text="Get Info", padx=10, pady=10, font=("Arial", 16), bg="black", command=get_user_info)
get_info_button.place(x=200, y=400)

# Profile picture label
profile_pic_label = tkinter.Label(window)
profile_pic_label.place(x=255, y=130)

# Frame for displaying recent posts
posts_frame = tkinter.Canvas(window, width=300, height=80)
posts_frame.place(x=9, y=450)

# Start the tkinter window
window.mainloop()
