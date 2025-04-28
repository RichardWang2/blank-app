import streamlit as st
import psycopg2

st.title("Missiongmind Backend Logs")

# Input fields
user_id = st.text_input("User ID")
chatlog_id = st.text_input("Chatlog ID")
worker = st.selectbox("Worker", ["document_worker"])
environment = st.selectbox("Environment", ["dev"])

# Function to show logs
def show_logs(user_id, chatlog_id, worker, environment):
    # You should replace these connection details with your actual database credentials
    conn = psycopg2.connect(
        dbname=st.secrets['DB_NAME'],
        user=st.secrets['DB_USER'],
        password=st.secrets['DB_PASSWORD'],
        host=st.secrets['DB_HOST'],
        port=st.secrets['DB_PORT']
    )
    cur = conn.cursor()
    try:
        query = """
            SELECT debug_log FROM document_worker_jobs
            WHERE user_id = %s AND chatlog_id = %s
            LIMIT 1
        """
        cur.execute(query, (user_id, chatlog_id,))
        result = cur.fetchone()
        if result:
            st.text_area("Debug Log", result[0], height=300)
        else:
            st.warning("No log found for the given user_id and chatlog_id.")
    except Exception as e:
        st.error(f"Error fetching logs: {e}")
    finally:
        cur.close()
        conn.close()

if st.button("Show Logs"):
    if user_id and chatlog_id:
        show_logs(user_id, chatlog_id, worker, environment)
    else:
        st.warning("Please enter both user_id and chatlog_id.")
