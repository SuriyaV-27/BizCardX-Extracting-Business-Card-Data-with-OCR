import streamlit as st
from PIL import Image
import easyocr
import io   
import mysql.connector
from mysql.connector import Error

#It is the code that i have explained in LIVE evaluation

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

def entry_exists(conn, entry_id):
    try:
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM image_details WHERE id = %s", (entry_id,))
        count = c.fetchone()[0]
        return count > 0
    except Error as e:
        print(f"Error checking entry existence in database: {e}")
        return False

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
        if entry_exists(conn, entry_id):
            c = conn.cursor()
            c.execute("DELETE FROM image_details WHERE id = %s", (entry_id,))
            conn.commit()
            print("Entry deleted from database.")
        else:
            st.error("Entry ID does not exist.")
    except Error as e:
        st.error(f"Error deleting entry from database: {e}")

# Function to update entry in database
def update_entry(conn, entry_id, new_details):
    try:
        if entry_exists(conn, entry_id):
            c = conn.cursor()
            c.execute("UPDATE image_details SET details = %s WHERE id = %s", (str(new_details), entry_id))
            conn.commit()
            print("Entry updated in database.")
        else:
            st.error("Entry ID does not exist.")
    except Error as e:
        st.error(f"Error updating entry in database: {e}")

# Example database configuration for MySQL
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "suri123",
    "database": "Image_Reader"
}

conn = create_connection(db_config)

st.title('Image Reader')

# Upload image
uploaded_file = st.file_uploader("Upload Image Card", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    image_bytes = uploaded_file.read()  
    image = Image.open(io.BytesIO(image_bytes))
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Perform OCR on the uploaded image
    st.subheader("Information Retrieved:")
    reader = easyocr.Reader(['en'])
    extracted_info = reader.readtext(image_bytes) 

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
        if entry_id_to_delete:
            delete_entry(conn, entry_id_to_delete)
        else:
            st.error("Please enter an Entry ID to delete.")

    # Update entry in database
    entry_id_to_update = st.text_input("Enter Entry ID to Update:")
    new_details = st.text_input("Enter New Details:")
    if st.button("Update Entry"):
        if entry_id_to_update and new_details:
            update_entry(conn, entry_id_to_update, new_details)
        else:
            st.error("Please enter both Entry ID and new details to update.")
