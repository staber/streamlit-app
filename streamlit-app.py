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
rows = execute_query(conn.table("players").select("*"), ttl=0)

# Print results.
for row in rows.data:
    st.write(f"{row['first']} {row['last']} : {row['shots']}")