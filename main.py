# This is a sample Python script.
from fastapi import FastAPI

app = FastAPI()
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

@app.get('/')
def print_hi():
    # Use a breakpoint in the code line below to debug your script.
    return "heyy"  # Press Ctrl+F8 to toggle the breakpoint.
