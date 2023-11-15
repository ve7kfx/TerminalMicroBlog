import json
import os
from datetime import datetime

def load_posts():
    try:
        with open('posts.json', 'r') as file:
            return [json.loads(line) for line in file]
    except FileNotFoundError:
        return []

def find_posts_by_date(date):
    posts = load_posts()
    return [post for post in posts if post['timestamp'].startswith(date)]

def display_post(post, display_type, show_images):
    if show_images:
        if display_type == 'ansi' and post['type'] == 'ansi':
            with open(post['art'], 'r') as file:
                print(file.read())
        else:
            print(post['art'])
    print(post['text'])

def paginate_text(text, words_per_page=500):
    words = text.split()
    for i in range(0, len(words), words_per_page):
        print(' '.join(words[i:i+words_per_page]))
        input("Press Enter to continue...")

def display_posts(posts, show_images):
    for i, post in enumerate(posts, start=1):
        print(f"\nPost Date: {post['timestamp']}")
        display_type = 'ascii'
        if show_images:
            display_type = input("Choose display type ('ascii' or 'ansi'): ").strip().lower()
        display_post(post, display_type, show_images)
        if len(post['text'].split()) > 500:
            paginate_text(post['text'])
        if i % 5 == 0:
            if input("Press 'q' to stop or any key to continue: ").strip().lower() == 'q':
                break

def main():
    while True:
        choice = input("\nEnter a date (YYYY-MM-DD) to search, 'list' to list posts, or 'quit' to exit: ").strip().lower()
        if choice == 'quit':
            break
        elif choice == 'list':
            show_images = input("Show images? (yes/no): ").strip().lower() == 'yes'
            posts = load_posts()
            display_posts(posts, show_images)
        else:
            try:
                datetime.strptime(choice, '%Y-%m-%d')
                posts = find_posts_by_date(choice)
                if not posts:
                    print("No posts found for this date.")
                else:
                    show_images = input("Show images? (yes/no): ").strip().lower() == 'yes'
                    display_posts(posts, show_images)
            except ValueError:
                print("Invalid date format. Please enter in YYYY-MM-DD format.")

if __name__ == '__main__':
    main()
