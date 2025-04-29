import reflex as rx
from app.components.blog_post_list import blog_post_list
from app.components.post_detail import post_detail
from app.states.blog_state import BlogState


def post_not_found() -> rx.Component:
    """Displays a message when a selected post is not found."""
    return rx.el.div(
        rx.el.button(
            "< Back to Posts",
            on_click=BlogState.clear_selection,
            class_name="mb-6 text-indigo-400 hover:text-indigo-300 transition-colors duration-200 font-medium text-sm font-mono",
        ),
        rx.el.p(
            "Post not found or failed to load.",
            class_name="text-red-500 font-mono",
        ),
        class_name="p-6",
    )


def about_me_section() -> rx.Component:
    """The About Me section component, now including posts."""
    link_style = "text-lg text-indigo-400 hover:text-indigo-300 mb-2 font-mono block"
    return rx.el.div(
        rx.el.h1(
            "Rohan Bopardikar",
            class_name="text-5xl font-bold mb-6 text-gray-100",
        ),
        rx.el.p(
            "I'm interested in database systems, probability, and philosophy. ",
            class_name="text-lg text-gray-300 mb-4 font-mono",
        ),
        rx.el.p(
            "Currently I am studying CS + Math @ASU and completing my honors thesis under Dr. Jia Zou.",
            class_name="text-lg text-gray-300 mb-8 font-mono",
        ),
        rx.el.div(
            rx.el.p(
                "Get in touch:",
                class_name="text-lg text-gray-300 mb-2 font-mono font-semibold",
            ),
            rx.el.p(
                "Email: rohanbopi [at] gmail [dot] com",
                class_name="text-lg text-gray-300 mb-2 font-mono",
            ),
            rx.el.a(
                "GitHub",
                href="https://github.com/rohanrrb",
                target="_blank",
                rel="noopener noreferrer",
                class_name=link_style,
            ),
            rx.el.a(
                "LinkedIn",
                href="https://linkedin.com/in/rohan-bopardikar",
                target="_blank",
                rel="noopener noreferrer",
                class_name=link_style,
            ),
            class_name="w-full mb-8",
        ),
        rx.el.hr(class_name="my-12 border-gray-700"),
        rx.cond(
            (BlogState.selected_post_slug != "")
            & (BlogState.selected_post != None),
            post_detail(BlogState.selected_post),
            rx.cond(
                BlogState.selected_post_slug != "",
                post_not_found(),
                blog_post_list(),
            ),
        ),
        class_name="w-full max-w-6xl mx-auto py-12 px-4",
    )