import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query

st.set_page_config(page_title="LCFH 2011", page_icon="https://raw.githubusercontent.com/staber/Supabase-Leaderboard/master/public/android-chrome-512x512.png",
                    layout="centered", initial_sidebar_state="auto", menu_items=None)

# Add row to player table
def add_shots(id, name, shots, date):
   st.toast(str(id) + ": Add " + str(shots) + " shots for " + str(name) + " on " + date.strftime("%Y-%m-%d"))
   execute_query(conn.table(name).insert(
       [{"activity_date": date.strftime("%Y-%m-%d"), "shots": shots}], count="None"
   ), ttl=0,)
   update_total_shots(id, name)

# Update the team table to show the newly updated player total
def update_total_shots(id, player):
    shots = 0
    player_table = execute_query(conn.table(player).select("*"), ttl=0)
    for row in player_table.data:
        shots = shots + row['shots']
    st.toast(player + " has " + str(shots) + " shots total.")
    execute_query(conn.table("players").update({"shots": shots}, count="None").eq("id", id), ttl=0)
    st.rerun()

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

strength_training = '''
            **Warm-up:**
            - 5-10 minutes of dynamic stretching or light jogging.

            **Strength Training:**
            - Push-ups: 3 sets of 12-15 repetitions.
            - Bodyweight Squats: 3 sets of 15-20 repetitions.
            - Lunges: 3 sets of 12-15 repetitions per leg.
            - Planks: 3 sets of 30-60 seconds.

            **Hockey Shots:**
            - 100-150 shots on goal, focusing on different types of shots (wrist shots, slap shots, backhands).
            - Break down the shots into sets (e.g., 5 sets of 20-30 shots) with rest in between.

            **Cool-down:**
            - 5-10 minutes of static stretching focusing on the muscles used.'''

running = '''
            **Warm-up:**
            - 5-10 minutes of dynamic stretching or light jogging.

            **Running:**
            - Interval Training: Alternate between running and walking.
                - Week 1-4: 1 minute running, 1 minute walking for 20 minutes.
                - Week 5-8: 2 minutes running, 1 minute walking for 25 minutes.
                - Week 9-12: 3 minutes running, 1 minute walking for 30 minutes.

            **Hockey Shots:**
            - 100-150 shots on goal, focusing on different types of shots (wrist shots, slap shots, backhands).
            - Break down the shots into sets (e.g., 5 sets of 20-30 shots) with rest in between.

            **Cool-down:**
            - 5-10 minutes of static stretching focusing on the muscles used.'''

long_run = '''
            **Warm-up:**
            - 5-10 minutes of dynamic stretching or light jogging.

            **Long Run:**
            - Gradually increase the distance each week to build endurance.
                - Week 1-4: 1.5 miles at a comfortable pace.
                - Week 5-8: 2 miles at a comfortable pace.
                - Week 9-12: 3 miles aiming for under 30 minutes.

            **Hockey Shots:**
            - 100-150 shots on goal, focusing on different types of shots (wrist shots, slap shots, backhands).
            - Break down the shots into sets (e.g., 5 sets of 20-30 shots) with rest in between.

            **Cool-down:**
            - 5-10 minutes of static stretching focusing on the muscles used.'''

recover = '''
            - Focus on rest and recovery to allow the body to heal and grow.
            - Encourage light activities like walking or yoga.
            - Spend time on flexibility and mobility exercises, such as foam rolling and static stretching.'''

# Perform query.
shooting_leaderboard = execute_query(conn.table("players").select("*").order("shots", desc=True), ttl=0)

# Setup Main Page
tab1, tab2, tab3 = st.tabs(["📅 Schedule", "🏒 Shots", "🏃 Running"])

# Schedule Tab
with tab1:
    st.header("Daily Schedule")

    with st.expander("Monday: (Strength Training + Hockey Shots)", expanded=False):
        st.markdown(strength_training, unsafe_allow_html=False)
    with st.expander("Tuesday: (Running + Hockey Shots)", expanded=False):
        st.markdown(running, unsafe_allow_html=False)
    with st.expander("Wednesday: (Strength Training + Hockey Shots)", expanded=False):
        st.markdown(strength_training, unsafe_allow_html=False)
    with st.expander("Thursday: (Running + Hockey Shots)", expanded=False):
        st.markdown(running, unsafe_allow_html=False)
    with st.expander("Friday: (Strength Training + Hockey Shots)", expanded=False):
        st.markdown(strength_training, unsafe_allow_html=False)
    with st.expander("Saturday: (Long Run + Hockey Shots)", expanded=False):
        st.markdown(long_run, unsafe_allow_html=False)
    with st.expander("Sunday: (Rest and Recovery)", expanded=False):
        st.markdown(recover, unsafe_allow_html=False)

# Shooting Leaderboard Tab
with tab2:
    st.header("Shooting Leaderboard")

    # Print results.
    for row in shooting_leaderboard.data:
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
                        add_shots(row['id'], f"{row['first']}_{row['last']}", shots, date)
                    else:
                        st.toast("Enter a number greater than 0")
        
        # st.image({row['avatar']}) # images can't be gifs
        # st.markdown(f"[![Click me]({row['avatar']})](https://streamlit.io)")

# Running Leaderboard Tab
with tab3:
    st.header("Mile Time Leaderboard")