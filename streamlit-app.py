import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query

def add_shots(id, name, shots, date):
   st.toast(str(id) + ": Add " + str(shots) + " for " + name + " on " + str(date))

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
    st.header("Shooting Leaderboard")

    # Print results.
    for row in rows.data:
        with st.expander(f"{row['first']} {row['last']} : {row['shots']}", expanded=False):
            # col1, col2, col3 = st.columns([0.2, 0.5, 0.3])
            # col1.image("https://storage.googleapis.com/ts_assets_prod-roster_full_photos/106848656/original/b2d721cd-de4b-4a57-8536-f9aa2ed8cd18.jpg", width=64, clamp=True)
            # col2.write(f"{row['first']} {row['last']}")
            # col3.write(f"{row['shots']}")
            with st.form(f"{row['first']}_{row['last']}", clear_on_submit=True, border=False):
                col1, col2 = st.columns([0.5,0.5])
                with col1:
                    shots = st.number_input("Add Shots", value=0)
                with col2:
                    date = st.date_input("Date")
                if st.form_submit_button('Submit Shots',
                        type="primary",
                        use_container_width=True):
                    if shots > 0:
                        add_shots({row['id']},{row['last']},shots,date)
                    else:
                        st.toast("Enter a number greater than 0")
        
        # st.image({row['avatar']}) # images can't be gifs
        # st.markdown(f"[![Click me]({row['avatar']})](https://streamlit.io)")

with tab2:
    st.header("Mile Time Leaderboard")