import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query

st.set_page_config(page_title="LCFH 2011", page_icon="https://raw.githubusercontent.com/staber/Supabase-Leaderboard/master/public/android-chrome-512x512.png",
                    layout="centered", initial_sidebar_state="auto", menu_items=None)

# Add row to player table
def add_shots(id, name, shots, date):
   #st.toast(str(id) + ": Add " + str(shots) + " shots for " + str(name) + " on " + date.strftime("%Y-%m-%d"))
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
    #st.toast(player + " has " + str(shots) + " shots total.")
    execute_query(conn.table("players").update({"shots": shots}, count="None").eq("id", id), ttl=0)
    st.rerun()

# Add row to player table
def add_time(id, name, time, date):
   #st.toast(str(id) + ": Add " + str(time) + " time for " + str(name) + " on " + date.strftime("%Y-%m-%d"))
   execute_query(conn.table(name).insert(
       [{"activity_date": date.strftime("%Y-%m-%d"), "mile_time": time}], count="None"
   ), ttl=0,)
   update_best_time(id, name)

# Update the team table to show the newly updated player mile time
def update_best_time(id, player):
    time = 1000
    player_table = execute_query(conn.table(player).select("*").gt("mile_time", 0), ttl=0)
    for row in player_table.data:
        if row['mile_time'] < time:
            time = row['mile_time']
    #st.toast(player + " has a best mile time of: " + str(time))
    execute_query(conn.table("players").update({"mile_time": time}, count="None").eq("id", id), ttl=0)
    st.rerun()

# Returns a list of players from the main database table
def getPlayerList():
    output = []
    for row in shooting_leaderboard.data:
        output.append(f"{row['first']}_{row['last']}")
    return output

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
tab1, tab2, tab3, tab4 = st.tabs(["📅 Schedule", "🏒 Shots", "🏃 Running", "📈 Data"])

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

    total_team_shots = 0

    # display shooting_leaderboard table as expandable items
    for row in shooting_leaderboard.data:
        total_team_shots = total_team_shots + row['shots']
        with st.expander(f"{row['first']} {row['last']} : {row['shots']}", expanded=False):
            with st.form(f"{row['first']}_{row['last']}_shots", clear_on_submit=True, border=False):
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
    
    st.divider()
    st.write("Team Total: " + str(total_team_shots))

# Running Leaderboard Tab
with tab3:
    st.header("Mile Time Leaderboard")

    running_leaderboard = execute_query(conn.table("players").select("*").order("mile_time", desc=False), ttl=0)

    # display running_leaderboard table as expandable items with positive time's entered
    for row in running_leaderboard.data:
        if row['mile_time'] > 0:
            with st.expander(f"{row['first']} {row['last']} : {row['mile_time']} Minutes", expanded=False):
                with st.form(f"{row['first']}_{row['last']}_time", clear_on_submit=True, border=False):
                    col1, col2 = st.columns([0.5,0.5])
                    with col1:
                        time = st.number_input("Mile Time (minutes)", value=0.00)
                    with col2:
                        date = st.date_input("Date")
                    if st.form_submit_button('Submit Time',
                            type="primary",
                            use_container_width=True):
                        if time > 0:
                            add_time(row['id'], f"{row['first']}_{row['last']}", time, date)
                        else:
                            st.toast("Enter a number greater than 0")
    
    # display running_leaderboard table as expandable items for players with no time entered
    for row in running_leaderboard.data:
        if row['mile_time'] == 0:
            with st.expander(f"{row['first']} {row['last']} : No Time Recorded", expanded=False):
                with st.form(f"{row['first']}_{row['last']}_time", clear_on_submit=True, border=False):
                    col1, col2 = st.columns([0.5,0.5])
                    with col1:
                        time = st.number_input("Mile Time (minutes)", value=0.00)
                    with col2:
                        date = st.date_input("Date")
                    if st.form_submit_button('Submit Time',
                            type="primary",
                            use_container_width=True):
                        if time > 0:
                            add_time(row['id'], f"{row['first']}_{row['last']}", time, date)
                        else:
                            st.toast("Enter a number greater than 0")

# Player Analysis
with tab4:

    player = st.selectbox(
        "Select a player to view their stats",
        (getPlayerList()),
        index=None,
        placeholder="Select a player...",
        )
    
    st.divider()

    if player != None:
        player_shot_table = execute_query(conn.table(player).select("*").gt("shots", 0), ttl=0)
        player_time_table = execute_query(conn.table(player).select("*").gt("mile_time", 0), ttl=0)

        # st.dataframe(player_shot_table.data, use_container_width=True)
        
        st.bar_chart(data=player_shot_table.data, x="activity_date", y="shots", use_container_width=True)
        
        st.divider()
        
        st.line_chart(data=player_time_table.data, x="activity_date", y="mile_time", use_container_width=True)