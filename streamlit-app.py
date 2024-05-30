import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query

# Initialize connection.
conn = st.connection(
    name="supabase",
    type=SupabaseConnection,
    ttl="10m"
)

# Perform query.
rows = execute_query(conn.table("players").select("*").order("shots", desc=True), ttl=0)

# Print results.
for row in rows.data:
    # st.image({row['avatar']}) # images can't be gifs
    st.image("https://storage.googleapis.com/ts_assets_prod-roster_full_photos/106848656/original/b2d721cd-de4b-4a57-8536-f9aa2ed8cd18.jpg")
    # st.markdown(f"[![Click me]({row['avatar']})](https://streamlit.io)")
    st.write(f"{row['first']} {row['last']} : {row['shots']}")