#!/bin/bash
gunicorn --bind 0.0.0.0:$PORT bot.main:flask_app
