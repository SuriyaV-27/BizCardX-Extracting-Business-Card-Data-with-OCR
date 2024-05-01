import streamlit as st
from PIL import Image
import easyocr
import io   
import mysql.connector
from mysql.connector import Error

# Function to create MySQL connection
def create_connection(db_config):
    conn = None
    try:
        conn = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
        if conn.is_connected():
            print("MySQL Database connection successful.")
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
    return conn

# Function to insert entry into database
def add_entry(conn, image_bytes, details):
    try:
        c = conn.cursor()
        c.execute("INSERT INTO image_details (image, details) VALUES (%s, %s)", (image_bytes, str(details)))
        conn.commit()
        print("Entry added to database.")
    except Error as e:
        print(f"Error adding entry to database: {e}")

# Function to delete entry from database
def delete_entry(conn, entry_id):
    try:
        c = conn.cursor()
        c.execute("DELETE FROM image_details WHERE id = %s", (entry_id,))
        conn.commit()
        print("Entry deleted from database.")
    except Error as e:
        print(f"Error deleting entry from database: {e}")

# Function to update entry in database
def update_entry(conn, entry_id, new_details):
    try:
        c = conn.cursor()
        c.execute("UPDATE image_details SET details = %s WHERE id = %s", (str(new_details), entry_id))
        conn.commit()
        print("Entry updated in database.")
    except Error as e:
        print(f"Error updating entry in database: {e}")

# Example database configuration for MySQL
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "suri123",
    "database": "Image_Reader"
}

# Connect to MySQL database using the configured parameters
conn = create_connection(db_config)

st.title('Image Reader')

# Upload image
uploaded_file = st.file_uploader("Upload Image Card", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    image_bytes = uploaded_file.read()  # Read image bytes directly
    image = Image.open(io.BytesIO(image_bytes))  # Use PIL to open image for display
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Perform OCR on the uploaded image
    st.subheader("Information Retrieved:")
    reader = easyocr.Reader(['en'])
    extracted_info = reader.readtext(image_bytes)  # Pass image bytes directly

    # Display extracted information
    for item in extracted_info:
        st.write(item[1])

    # Save to database
    if st.button("Save to Database"):
        add_entry(conn, image_bytes, extracted_info)
        st.success("Details saved to database!")

    # Delete entry from database
    entry_id_to_delete = st.text_input("Enter Entry ID to Delete:")
    if st.button("Delete Entry"):
        delete_entry(conn, entry_id_to_delete)
        st.success("Entry deleted from database!")

    # Update entry in database
    entry_id_to_update = st.text_input("Enter Entry ID to Update:")
    new_details = st.text_input("Enter New Details:")
    if st.button("Update Entry"):
        update_entry(conn, entry_id_to_update, new_details)
        st.success("Entry updated in database!")
