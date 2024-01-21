

import streamlit as st
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import calendar

# Assuming you have already set the secrets in Streamlit using st.secrets["your_secret_name"]
service_account_type = st.secrets["type"]
project_id = st.secrets["project_id"]
private_key_id = st.secrets["private_key_id"]
private_key = st.secrets["private_key"]
client_email = st.secrets["client_email"]
client_id = st.secrets["client_id"]
auth_uri = st.secrets["auth_uri"]
token_uri = st.secrets["token_uri"]
auth_provider_x509_cert_url = st.secrets["auth_provider_x509_cert_url"]
client_x509_cert_url = st.secrets["client_x509_cert_url"]
universe_domain = st.secrets["universe_domain"]

# Create a JSON object
json_data = {
    "type": service_account_type,
    "project_id": project_id,
    "private_key_id": private_key_id,
    "private_key": private_key,
    "client_email": client_email,
    "client_id": client_id,
    "auth_uri": auth_uri,
    "token_uri": token_uri,
    "auth_provider_x509_cert_url": auth_provider_x509_cert_url,
    "client_x509_cert_url": client_x509_cert_url,
    "universe_domain": universe_domain
}

# Create a credentials.Certificate object
cred = credentials.Certificate(json_data)
if not firebase_admin._apps:
    app = firebase_admin.initialize_app(cred)
firestore_client = firestore.client()

def main():
    # Initialize session state
    if 'date_input' not in st.session_state:
        st.session_state.date_input = datetime.today()
        
    # page configuration 
    st.set_page_config(page_title="OpenAI", page_icon="🖖",layout="wide")
    
    # Streamlit UI
    st.title("Habit Tracker")
    
    # data
    coll_ref_1 = firestore_client.collection("habit") 
    # Fetch all data
    all_months_data = coll_ref_1.document("all_month").get().to_dict()

    if st.button("Load Score"):
        # Initialize variables
        total_points = 0
        max_possible_points = 0
        # Iterate through all_months_data
        for year_key, year_data in all_months_data.items():
            for day_key, value in year_data.items():
                if "rating" in day_key:
                    # Extract day information from the key
                    year, month, day = map(int, day_key.split('_')[:3])
                    # Get the rating and corresponding task for the day
                rating = value
                task_key = f"{year}_{month}_{day}_task"
                task = year_data.get(task_key, "")

                # Check if the task is not an empty string
                if task != "":
                    # Calculate points based on the scoring system
                    if rating == 'red':
                        points = 1
                    elif rating == 'orange':
                        points = 2
                    elif rating == 'green':
                        points = 3
                    else:
                        points = 0  # Handle other cases
                    # Update total points and max possible points
                    total_points += points
                    max_possible_points += 3  
        # Calculate strike rate
        if max_possible_points > 0:
            strike_rate = (total_points / max_possible_points) * 100
        else:
            strike_rate = 0
        # Display the calculated strike rate
        st.write(f"Total Points: {total_points}")
        st.write(f"Maximum Possible Points: {max_possible_points}")
        st.write(f"Strike Rate: {strike_rate:.2f}%")
        
        st.success(" Loaded successfully!")
    
    if st.button("strike score"):

        # Assuming today is the current date
        today = datetime.today()

        # Calculate the start date for the last 2 weeks
        start_date = today - timedelta(days=14)
        st.write(start_date.strftime("%Y-%m-%d"))
        # Initialize variables
        total_points = 0
        max_possible_points = 0

        # Iterate through all_months_data
        for year_key, year_data in all_months_data.items():
            for day_key, value in year_data.items():
                if "rating" in day_key:
                    # Extract day information from the key
                    year, month, day = map(int, day_key.split('_')[:3])
                    
                    # Convert day information to a datetime object
                    day_date = datetime(year, month, day)
                    
                    # Check if the day is within the last 2 weeks
                    if start_date <= day_date <= today:
                        # Get the rating and corresponding task for the day
                        rating = value
                        task_key = f"{year}_{month}_{day}_task"
                        task = year_data.get(task_key, "")

                        # Check if the task is not an empty string
                        if task != "":
                            # Calculate points based on the scoring system
                            if rating == 'red':
                                points = 1
                            elif rating == 'orange':
                                points = 2
                            elif rating == 'green':
                                points = 3
                            else:
                                points = 0  # Handle other cases
                            # Update total points and max possible points
                            total_points += points
                            max_possible_points += 3  

        # Calculate strike rate
        if max_possible_points > 0:
            strike_rate = (total_points / max_possible_points) * 100
        else:
            strike_rate = 0

        # Display the calculated strike rate
        st.write(f"Total Points: {total_points}")
        st.write(f"Maximum Possible Points: {max_possible_points}")
        st.write(f"Strike Rate for the Last 2 Weeks: {strike_rate:.2f}%")

    
    st.write("---")
    
    jan, feb, col3, col4, col5, col6 = st.columns(6)
    color_list = {'red':0, 'orange':1, "green":2}
    year = 2024
    
    d_jan,d_feb = {},{}
    with jan:
        month = 1
        MON = "JAN"
        # Get the number of days in the specified month
        num_days = calendar.monthrange(year, month)[1]
        month_key = f"{year}_{month}"
        if all_months_data[month_key]:
            d = all_months_data[month_key]
 
        for i in range(num_days):
            day_key = f"{year}_{month}_{i+1}"
            # Check if the day is a Saturday or Sunday
            day_of_week = calendar.weekday(year, month, i + 1)
            is_weekend = day_of_week in [5, 6]  # 5 is Saturday, 6 is Sunday

            # Determine label color based on the day of the week
            label_color = "red" if is_weekend else "white"

            # Change the label style using HTML and CSS
            label_style = f"color: {label_color}; font-weight: {'bold' if is_weekend else 'normal'}"
            st.write(
                f'<p style="{label_style}">{MON} {i + 1}</p>',
                unsafe_allow_html=True
            )
            rating = st.radio(
                label=f"{MON} {i+1}", 
                options=('red', 'orange', "green"),
                index=color_list[d.get(f"{day_key}_rating", "red")],
                key=f"{MON}rating_{i}",
                label_visibility = "collapsed"
            )
            task = st.text_area(
                label=f"{MON} {i}", key=f"{MON} {i}", 
                value=d.get(f"{day_key}_task", ""), 
                height=1,
                label_visibility="collapsed"
            )
            d_jan[f"{year}_{month}_{i+1}_task"] = task
            d_jan[f"{year}_{month}_{i+1}_rating"] = rating

    with feb:
        month = 2
        MON = "FEB"
        # Get the number of days in the specified month
        num_days = calendar.monthrange(year, month)[1]
        month_key = f"{year}_{month}"
        if all_months_data[month_key]:
            d = all_months_data[month_key]
        if coll_ref_1.document(month_key).get().to_dict():
            d = coll_ref_1.document(month_key).get().to_dict()
        for i in range(num_days):
            day_key = f"{year}_{month}_{i+1}"
            rating = st.radio(
                label=f"{MON} {i+1}", 
                options=('red', 'orange', "green"),
                index=color_list[d.get(f"{day_key}_rating", "red")],
                key=f"{MON}_rating_{i}"
            )
            task = st.text_area(
                label=f"{MON} {i}", key=f"{MON} {i}", 
                value=d.get(f"{day_key}_task", ""), 
                height=1,
                label_visibility="collapsed"
            )
            d_feb[f"{year}_{month}_{i+1}_task"] = task
            d_feb[f"{year}_{month}_{i+1}_rating"] = rating
    
    st.write("---")
    if st.button("Save Task"):
        coll_ref_1.document("all_month").update({
            "2024_1": d_jan,
            "2024_2":d_feb
        })
        st.success("Expenses saved successfully!")

if __name__ == "__main__":
    main()



# 

    # # Initialize session state
    # if 'current_color' not in st.session_state:
    #     st.session_state.current_color = 'red'
    
    # def get_next_color(current_color):
    #     colors = ['red', 'green', 'blue']
    #     current_index = colors.index(current_color)
    #     next_index = (current_index + 1) % len(colors)
    #     return colors[next_index]

    # # Use a container to layout the button and the colored box horizontally
    # col1, col2 = st.columns([1, 12])

    # # Display "Next Color" button in the first column
    # if col1.button('Next Color'):
    #     st.session_state.current_color = get_next_color(st.session_state.current_color)
