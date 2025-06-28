import streamlit as st

# Navigation
page_0 = st.Page("page0.py", title="Home", icon="🏠")         
page_1 = st.Page("page1.py", title="NL To SQL", icon="🎬")     
page_2 = st.Page("page2.py", title="NL To DataViz", icon="📊") 
#page_3 = st.Page("page3.py", title="Movie Explorer", icon="🔎")

pg = st.navigation([page_0, page_1, page_2])
pg.run()