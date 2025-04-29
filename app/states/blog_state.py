import reflex as rx
from typing import TypedDict, Optional, List
import os
import re
from datetime import datetime


class Post(TypedDict):
    slug: str
    title: str
    content: str
    date: str
    snippet: str


POSTS_DIR = "app/posts"


def get_post_date_obj(post: Post) -> datetime:
    """Helper function to get a datetime object for sorting posts."""
    try:
        return datetime.strptime(post["date"], "%Y-%m-%d")
    except (ValueError, KeyError, TypeError):
        print(
            f"Warning: Could not parse date '{post.get('date')}' for sorting post '{post.get('slug', 'Unknown')}'."
        )
        return datetime.min


def load_posts_from_markdown() -> List[Post]:
    """
    Loads blog posts from markdown files in the POSTS_DIR.
    Expects metadata lines at the top like:
    title: My Post Title
    date: YYYY-MM-DD  <- IMPORTANT: Use this exact format!
    snippet: A short description...
    (followed by a blank line, then the content)
    """
    posts: List[Post] = []
    if not os.path.exists(POSTS_DIR):
        print(
            f"Warning: Posts directory '{POSTS_DIR}' not found."
        )
        try:
            os.makedirs(POSTS_DIR)
            print(
                f"Created directory '{POSTS_DIR}'. Add your markdown files (like 'my-post.md') here."
            )
            placeholder_path = os.path.join(
                POSTS_DIR, "example-post.md"
            )
            if not os.path.exists(placeholder_path):
                with open(
                    placeholder_path, "w", encoding="utf-8"
                ) as f:
                    f.write("title: Example Post\n")
                    f.write(
                        f"date: {datetime.now().strftime('%Y-%m-%d')}\n"
                    )
                    f.write(
                        "snippet: This is an example post.\n\n"
                    )
                    f.write(
                        "Start writing your blog content here using Markdown!\nMake sure to include the `title`, `date` (in YYYY-MM-DD format), and `snippet` metadata at the top."
                    )
                print(
                    f"Created '{placeholder_path}' as an example."
                )
        except OSError as e:
            print(
                f"Error creating directory '{POSTS_DIR}': {e}"
            )
        return posts
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith(".md"):
            slug = filename[:-3]
            filepath = os.path.join(POSTS_DIR, filename)
            try:
                with open(
                    filepath, "r", encoding="utf-8"
                ) as f:
                    lines = f.readlines()
                metadata = {}
                content_start_index = 0
                metadata_keys = {"title", "date", "snippet"}
                for i, line in enumerate(lines):
                    if i >= 10:
                        break
                    stripped_line = line.strip()
                    if not stripped_line:
                        content_start_index = i + 1
                        break
                    if ":" in stripped_line:
                        try:
                            key, value = (
                                stripped_line.split(":", 1)
                            )
                            key = key.strip().lower()
                            if key in metadata_keys:
                                metadata[key] = (
                                    value.strip()
                                )
                                content_start_index = i + 1
                        except ValueError:
                            content_start_index = i
                            break
                    else:
                        content_start_index = i
                        break
                else:
                    content_start_index = len(lines)
                actual_content_start = content_start_index
                for i in range(
                    content_start_index, len(lines)
                ):
                    if lines[i].strip():
                        actual_content_start = i
                        break
                content = "".join(
                    lines[actual_content_start:]
                ).strip()
                title = metadata.get(
                    "title", slug.replace("-", " ").title()
                )
                raw_date = metadata.get("date", "")
                date_str = "1970-01-01"
                if raw_date:
                    try:
                        datetime.strptime(
                            raw_date, "%Y-%m-%d"
                        )
                        date_str = raw_date
                    except ValueError:
                        print(
                            f"Warning: Invalid date format '{raw_date}' in '{filename}'. Using default '{date_str}'. Expected 'YYYY-MM-DD'."
                        )
                else:
                    print(
                        f"Warning: Missing 'date: YYYY-MM-DD' metadata in '{filename}'. Using default '{date_str}'."
                    )
                snippet = metadata.get(
                    "snippet", ""
                ).strip()
                if not snippet:
                    if content:
                        plain_text_content = re.sub(
                            "<[^>]+>", "", content
                        )
                        plain_text_content = re.sub(
                            "\\[([^\\]]+)\\]\\([^\\)]+\\)",
                            "\\1",
                            plain_text_content,
                        )
                        plain_text_content = re.sub(
                            "[`*_~#]",
                            "",
                            plain_text_content,
                        )
                        plain_text_content = (
                            plain_text_content.replace(
                                "\r\n", " "
                            )
                            .replace("\n", " ")
                            .strip()
                        )
                        snippet = plain_text_content[
                            :150
                        ] + (
                            "..."
                            if len(plain_text_content) > 150
                            else ""
                        )
                    else:
                        snippet = "No snippet available."
                posts.append(
                    Post(
                        slug=slug,
                        title=title,
                        content=(
                            content
                            if content
                            else "No content available."
                        ),
                        date=date_str,
                        snippet=snippet,
                    )
                )
            except Exception as e:
                print(
                    f"Error processing file '{filename}': {e}"
                )
    try:
        posts.sort(key=get_post_date_obj, reverse=True)
    except Exception as e:
        print(
            f"Warning: Could not sort posts by date. Error: {e}"
        )
    if not posts and os.path.exists(POSTS_DIR):
        print(
            f"No valid markdown files (.md with 'title', 'date: YYYY-MM-DD', 'snippet' metadata) found or processed successfully in '{POSTS_DIR}'."
        )
    elif posts:
        print(f"Successfully loaded {len(posts)} posts.")
    return posts


class BlogState(rx.State):
    """State for managing blog posts loaded from markdown files."""

    posts: list[Post] = load_posts_from_markdown()
    selected_post_slug: str = ""

    @rx.var
    def selected_post(self) -> Optional[Post]:
        """Returns the currently selected post based on the slug."""
        if not self.selected_post_slug:
            return None
        return next(
            (
                post
                for post in self.posts
                if post["slug"] == self.selected_post_slug
            ),
            None,
        )

    @rx.event
    def select_post(self, slug: str):
        """Selects a post by its slug."""
        print(f"Selecting post with slug: {slug}")
        found: bool = False
        for post in self.posts:
            if post["slug"] == slug:
                found = True
                break
        if found:
            self.selected_post_slug = slug
        else:
            print(
                f"Warning: Attempted to select non-existent slug: {slug}"
            )

    @rx.event
    def clear_selection(self):
        """Clears the current post selection and returns to the posts list."""
        self.selected_post_slug = ""

    @rx.event
    def reload_posts(self):
        """Reloads posts from the markdown directory."""
        print("Reloading posts...")
        self.posts = load_posts_from_markdown()
        current_slug_exists: bool = False
        if self.selected_post_slug:
            for post in self.posts:
                if post["slug"] == self.selected_post_slug:
                    current_slug_exists = True
                    break
        if (
            not current_slug_exists
            and self.selected_post_slug
        ):
            print(
                f"Previously selected post '{self.selected_post_slug}' not found after reload. Clearing selection."
            )
            self.selected_post_slug = ""
        elif self.selected_post_slug:
            print(
                f"Keeping selection '{self.selected_post_slug}' after reload."
            )