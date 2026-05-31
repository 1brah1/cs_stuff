"""WSGI entrypoint for hosted deployments."""

from app import app, start_background_jobs

start_background_jobs()
