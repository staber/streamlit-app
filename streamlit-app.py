import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query

# Initialize connection.
conn = st.connection(
    name="supabase",
    type=SupabaseConnection,
    ttl="10m"
)

# Remove Fullscreen Image Button
hide_img_fs = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
'''

st.markdown(hide_img_fs, unsafe_allow_html=True)

# Perform query.
rows = execute_query(conn.table("players").select("*").order("shots", desc=True), ttl=0)

tab1, tab2 = st.tabs(["🏒 Shots", "🏃 Running"])

with tab1:

    # Print results.
    for row in rows.data:
        col1, col2, col3 = st.columns([0.2, 0.5, 0.3])
        # st.image({row['avatar']}) # images can't be gifs
        col1.image("https://storage.googleapis.com/ts_assets_prod-roster_full_photos/106848656/original/b2d721cd-de4b-4a57-8536-f9aa2ed8cd18.jpg", width=64)
        # st.markdown(f"[![Click me]({row['avatar']})](https://streamlit.io)")
        col2.write(f"{row['first']} {row['last']}")
        col3.write(f"{row['shots']}")