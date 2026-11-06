"""WSGI entry point for the public GitHub Pages rewrite relay."""

from app import create_pages_app

application = create_pages_app()
