import streamlit as st
import requests

title = st.header("Join WAIR-Sandbox")
org = "WAIR-sandbox"
success = False

# Show a form with a text field
form_container = st.empty()
with form_container.form("my_form", clear_on_submit=True):
    text_input = st.text_input("Enter GitHub username")

    st.caption("the limit is 500 invitations per 24 hour period")

    submitted = st.form_submit_button("Submit")
    if submitted:
        url = f"https://api.github.com/users/{text_input}"
        r = requests.get(url.format(text_input)).json()
        if 'status' in r:
            st.write(f"User `{text_input}` is not found, please enter a valid username")
            success = False
        else:
            url = f"https://api.github.com/orgs/{org}/memberships/{text_input}"
            h = {
                'Authorization': f'Bearer {st.secrets["github_token"]}',
                'Accept' : 'application/vnd.github+json'
            }
            r = requests.put(url.format(org, text_input), headers=h, json={"role":"member"}).json()
            if 'state' in r:
                success = True
            else:
                st.write(f"__{r['message']}__")
                success = False
    

# if user exists show greetings
if success:
    form_container.empty()
    if r['state'] == "pending":
        st.title(f"_Welcome_ :blue[{text_input}]!!!")
    elif r['state'] == "active":
        st.title(f"Hi :blue[{text_input}], you have already joined")
    st.html('<a href="https://github.com/WAIR-sandbox">Go to WAIR-Sandbox</a>')
    st.balloons()