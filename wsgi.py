"""WSGI entry point for BrandLex."""

from app import create_app

application = create_app()
