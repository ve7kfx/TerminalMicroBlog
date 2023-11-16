import json

def load_posts():
    try:
        with open('posts.json', 'r') as file:
            return [json.loads(line) for line in file]
    except FileNotFoundError:
        return []

def display_post(post, display_type):
    print("\nTimestamp:", post['timestamp'])
    print("Text Content:\n")
    print(post['text'])

    if display_type == 'A' and post['type'] == 'ascii':
        print("\nDisplaying ASCII art:\n")
        print(post['art'])
    elif display_type == 'N' and post['type'] == 'ansi':
        try:
            with open(post['art'], 'r') as file:
                art = file.read()
                print(f"\nDisplaying ANSI art from {post['art']}:\n")
                print(art)
        except FileNotFoundError:
            print(f"ANSI art file {post['art']} not found.")
    elif display_type != 'T':
        print("\nInvalid display type.")

def list_posts(posts):
    for index, post in enumerate(posts, start=1):
        print(f"\n{index}. Timestamp: {post['timestamp']}")
    choice = input("Enter the number of the post you want to view, or 'Q' to quit: ").strip()
    if choice.lower() == 'q':
        return
    try:
        choice = int(choice)
        if 1 <= choice <= len(posts):
            display_type = input("Display type - A (ASCII), N (ANSI), or T (Text only): ").strip().upper()
            display_post(posts[choice - 1], display_type)
        else:
            print("Invalid post number.")
    except ValueError:
        print("Invalid input. Please enter a valid post number.")

def find_posts_by_date(date, posts):
    matching_posts = [post for post in posts if post['timestamp'].startswith(date)]
    return matching_posts

def main():
    posts = load_posts()

    while True:
        choice = input("\nEnter 'D' to display posts by date, 'L' to list all posts, 'R' to view the most recent post, or 'Q' to quit: ").strip().upper()
        if choice == 'D':
            date = input("Enter date (YYYY-MM-DD): ")
            matching_posts = find_posts_by_date(date, posts)
            if matching_posts:
                list_posts(matching_posts)
            else:
                print("No posts found for this date.")
        elif choice == 'L':
            if posts:
                list_posts(posts)
            else:
                print("No posts available.")
        elif choice == 'R':
            if posts:
                most_recent_post = max(posts, key=lambda x: x['timestamp'])
                display_type = input("Display type - A (ASCII), N (ANSI), or T (Text only): ").strip().upper()
                display_post(most_recent_post, display_type)
            else:
                print("No posts available.")
        elif choice == 'Q':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
