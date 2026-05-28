from db import connect_db

def save_responder(form_data):
    conn = connect_db()
    cursor = conn.cursor()

    # =================================================
    # 1. INSERT INTO RESPONDERS (PARENT TABLE)
    # =================================================
    cursor.execute("""
        INSERT INTO responders (Date_Of_Interview)
        VALUES (%s)
    """, (form_data["date_of_interview"],))

    respondent_id = cursor.lastrowid  # 🔥 IMPORTANT

    # =================================================
    # 2. INSERT INTO PERSONAL INFORMATION
    # =================================================
    cursor.execute("""
        INSERT INTO Personal_Information (
            Respondent_ID,
            First_Name,
            Middle_Name,
            Last_Name,
            Extension_Name,
            Age,
            Date_Of_Birth,
            Gender,
            House_Number,
            Street_Name,
            Barangay,
            Religion,
            Contact_Number
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        respondent_id,
        form_data["first_name"],
        form_data["middle_name"],
        form_data["last_name"],
        form_data["ext_name"],
        form_data["age"],
        form_data["birthdate"],
        form_data["gender"],
        form_data["house_number"],
        form_data["street_name"],
        form_data["barangay"],
        form_data["religion"],
        form_data["contact_number"]
    ))

    conn.commit()
    conn.close()

    return respondent_id