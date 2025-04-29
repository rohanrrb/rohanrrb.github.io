import reflex as rx
from app.states.blog_state import BlogState, Post
from datetime import datetime


def post_detail(post: Post) -> rx.Component:
    """Displays the full content of a selected blog post."""
    return rx.el.div(
        rx.el.button(
            "< Back to Posts",
            on_click=BlogState.clear_selection,
            class_name="mb-6 text-indigo-400 hover:text-indigo-300 transition-colors duration-200 font-medium text-sm font-mono",
        ),
        rx.el.h1(
            post["title"],
            class_name="text-4xl font-bold mb-2 text-gray-100 font-mono",
        ),
        rx.moment(
            date=post["date"],
            format="MMMM Do, YYYY",
            class_name="text-sm text-gray-400 mb-6 italic font-mono",
        ),
        rx.el.div(
            rx.markdown(post["content"]),
            class_name="prose prose-lg prose-invert max-w-none text-gray-300 leading-relaxed font-mono",
        ),
        class_name="p-6 bg-neutral-800 w-full border border-gray-700",
    )