import reflex as rx
from app.components.about_section import about_me_section


def index() -> rx.Component:
    """The main page displaying about section and posts."""
    return rx.el.div(
        about_me_section(),
        class_name="min-h-screen bg-neutral-800 p-4 sm:p-8 md:p-12 flex flex-col items-center font-sans text-gray-200",
    )


app = rx.App(theme=rx.theme(appearance="light"))
app.add_page(index, route="/")