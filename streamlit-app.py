import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query

# Initialize connection.
conn = st.connection(
    name="supabase",
    type=SupabaseConnection,
    ttl="10m"
)

# Perform query.
# rows = conn.query("*", table="players").execute()
rows = execute_query(conn.table("players").select("*").order("shots", desc=True), ttl=0)

# Print results.
for row in rows.data:
    # st.image({row['avatar']}) # images can't be gifs
    st.markdown(f"[![Click me]({row['avatar']})](https://streamlit.io)")
    st.write(f"{row['first']} {row['last']} : {row['shots']}")