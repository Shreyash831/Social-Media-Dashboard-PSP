import requests
import tkinter as tk
from tkinter import messagebox

def fetch_user_data(user_id, access_token):
    """Fetch user data from Instagram using Graph API."""
    url = f"https://graph.instagram.com/{user_id}?fields=id,username,media_count,followers_count&access_token={access_token}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return {
                "username": data.get("username", "N/A"),
                "followers": data.get("followers_count", 0),
                "posts": data.get("media_count", 0)
            }
        else:
            try:
                error_msg = response.json().get('error', {}).get('message', 'Unknown error')
            except Exception:
                error_msg = response.text
            messagebox.showerror("Error", f"Failed to fetch data: {error_msg}")
            return None
    except Exception as e:
        messagebox.showerror("Error", f"Request failed: {e}")
        return None

def calculate_engagement(likes, comments, shares, followers):
    """Calculate total engagement and engagement rate."""
    total_engagement = likes + comments + shares
    engagement_rate = (total_engagement / followers) * 100 if followers != 0 else 0
    return total_engagement, engagement_rate

def display_metrics(metrics):
    """Display selected metrics in the GUI."""
    try:
        likes = int(likes_entry.get())
        comments = int(comments_entry.get())
        shares = int(shares_entry.get())
        followers = metrics.get('followers', 0)
        total_engagement, engagement_rate = calculate_engagement(likes, comments, shares, followers)

        result_text = f"""
Username: {metrics['username']}
Followers: {metrics['followers']}
Posts: {metrics['posts']}
Total Engagement: {total_engagement}
Engagement Rate: {round(engagement_rate, 2)}%
        """
        messagebox.showinfo("User Engagement Metrics", result_text)
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers for likes, comments, and shares.")

def fetch_data():
    """Fetch user data and display metrics."""
    user_id = username_entry.get().strip()
    access_token = access_token_entry.get().strip()
    if not user_id:
        messagebox.showerror("Error", "Please enter the Instagram User ID.")
        return
    if not access_token:
        messagebox.showerror("Error", "Please enter the Instagram Access Token.")
        return
    user_data = fetch_user_data(user_id, access_token)
    if user_data:
        display_metrics(user_data)

# Setting up the GUI
root = tk.Tk()
root.title("Instagram Analytics Dashboard")

# Access Token input
tk.Label(root, text="Instagram Access Token:").pack()
access_token_entry = tk.Entry(root, show='*')
access_token_entry.pack()

# Username/User ID input
tk.Label(root, text="Instagram User ID:").pack()
username_entry = tk.Entry(root)
username_entry.pack()

# Engagement metrics input
tk.Label(root, text="Total Likes:").pack()
likes_entry = tk.Entry(root)
likes_entry.pack()

tk.Label(root, text="Total Comments:").pack()
comments_entry = tk.Entry(root)
comments_entry.pack()

tk.Label(root, text="Total Shares:").pack()
shares_entry = tk.Entry(root)
shares_entry.pack()

# Fetch data button
fetch_button = tk.Button(root, text="Fetch Data", command=fetch_data)
fetch_button.pack()

# Run the GUI
root.mainloop()

