# Guvi-3-Task

Import the needed package:-
import streamlit as st
from PIL import Image
import easyocr
import io   
import mysql.connector
from mysql.connector import Error

while uploading image in streamlit UI inside the image, data is readed by OCR and shown in the streamlit UI and if we click save to database it will directly save the appropriate table with image as blob and information stored as varchar.In streamlit UI we have update and delete button, based on ID no from Database we can delete the row in database and if we click update it will ask update new details and it will be reflected in database.We can upload a image multiple times and it will create new id and new entry in database.
