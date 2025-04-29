import reflex as rx
from app.states.blog_state import BlogState, Post
from datetime import datetime


def blog_post_list_item(post: Post) -> rx.Component:
    """Displays a single blog post item in the list."""
    return rx.el.div(
        rx.el.h2(
            post["title"],
            class_name="text-xl font-semibold mb-1 text-gray-100",
        ),
        rx.moment(
            date=post["date"],
            format="MMMM Do, YYYY",
            class_name="text-xs text-gray-400 mb-2 italic",
        ),
        rx.el.p(
            post["snippet"],
            class_name="text-gray-300 mb-3 leading-snug",
        ),
        rx.el.button(
            "Read More ->",
            on_click=lambda: BlogState.select_post(
                post["slug"]
            ),
            class_name="text-indigo-400 hover:text-indigo-300 transition-colors duration-200 font-medium text-sm",
        ),
        class_name="py-4 border-b border-gray-700 last:border-b-0 font-mono w-full",
    )


def blog_post_list() -> rx.Component:
    """Displays the list of all blog posts."""
    return rx.el.div(
        rx.el.h2(
            "Research Projects/Notes",
            class_name="text-3xl font-bold mb-6 text-gray-100 font-mono",
        ),
        rx.el.div(
            rx.cond(
                BlogState.posts.length() > 0,
                rx.foreach(
                    BlogState.posts, blog_post_list_item
                ),
                rx.el.p(
                    "No posts found. Add markdown files with 'date: YYYY-MM-DD' metadata to the 'app/posts' directory.",
                    class_name="text-gray-400",
                ),
            ),
            class_name="flex flex-col",
        ),
        class_name="w-full mt-10",
    )