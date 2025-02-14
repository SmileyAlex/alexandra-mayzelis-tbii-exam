# Importing all the libraries
import streamlit as st
import folium
import pandas as pd
from streamlit_folium import st_folium
from streamlit.components.v1 import html
import os
from pymongo import MongoClient
import datetime

# Page Configuration
st.set_page_config(page_title="FLINTA Space App", page_icon="🏳️‍🌈")

# Initialize session state for page selection
if 'selected_page' not in st.session_state:
    st.session_state.selected_page = "Home"

# Function to update session state when a button is clicked
def set_page(page):
    st.session_state.selected_page = page

# Function to connect to MongoDB (for the feedback page)
@st.cache_resource
def connect_to_mongo():
    # Load the MongoDB username and password from secrets.toml file
    db_username = st.secrets['mongodb']['db_username']
    db_password = st.secrets['mongodb']['db_password']

    # MongoDB connection string
    mongo_uri = f"mongodb+srv://{db_username}:{db_password}@techbasic2.fh3wv.mongodb.net/?retryWrites=true&w=majority&appName=TechBasic2"

    # Connect to MongoDB client
    client = MongoClient(mongo_uri)

    return client

# Function to load events from CSV file
def load_events():
    if not os.path.exists('events.csv'):
        df = pd.DataFrame(columns=["title", "date", "adress", "description", "source"])
        df.to_csv('events.csv', index=False)
    else:
        df = pd.read_csv('events.csv')

    # Ensure 'source' column exists
    if 'source' not in df.columns:
        df['source'] = "official"

    return df

# Function to save new event to CSV file
def save_event(new_event):
    # Load existing events
    df = load_events()

    # Append the new event to the dataframe
    df = pd.concat([df, pd.DataFrame([new_event])], ignore_index=True)

    # Save the updated dataframe back to the CSV file
    df.to_csv('events.csv', index=False)

# Sidebar title (Header for the Sidebar Menu)
st.sidebar.markdown("""
    <h2 style="font-size: 24px; font-weight: bold;">FLINTA Space 🌈</h2>
""", unsafe_allow_html=True)

# Sidebar Buttons for Navigation (with callbacks)
st.sidebar.button("Home", on_click=set_page, args=("Home",))
st.sidebar.button("Map", on_click=set_page, args=("Map",))
st.sidebar.button("Events", on_click=set_page, args=("Events",))
st.sidebar.button("Add Your Event", on_click=set_page, args=("Add Your Event",))
st.sidebar.button("About FLINTA", on_click=set_page, args=("About FLINTA",))
st.sidebar.button("Feedback", on_click=set_page, args=("Feedback",))

# Code for Home page
if st.session_state.selected_page == "Home":
    st.image("flinta-app/Flinta3.jpg")
    st.header("Welcome to FLINTA Space Hamburg🌈", divider='rainbow')
    st.markdown("""
    **Looking for safe, welcoming spaces in Hamburg?** 

    You've come to the right place!  
    FLINTA Space Hamburg is a platform dedicated to highlighting and supporting spaces that prioritize the safety and inclusion of **Female, Lesbian, Intersex, Non-Binary, Trans, and Agender** people.  
    In a city where public spaces often cater to cisgender, male-dominated experiences, we're here to change that narrative.  

    Whether you're searching for a cozy café, an inclusive event, or a supportive community center, **we've got you covered**. Together, we can create a city where everyone feels seen, safe, and celebrated.
    """)

# styled box underneath the displayed text (the code for all the design choices, is provided by Chat gpt)
    st.markdown("""
        <div style="
            background: linear-gradient(90deg, #00bac1, #051efe);
            padding: 15px;
            border-radius: 15px;
            font-size: 20px;
            text-align: center;
            color: #ffffff;
            border: 2px solid #028a92;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);">
            <strong>🌟 Start Exploring Now! 🌟</strong><br><br>
            Discover <strong>Safe Spaces</strong> on our interactive map, join exciting <strong>Events</strong>, connect with the <strong>Community</strong>, and access helpful <strong>Resources</strong>.<br><br>
            Have something to share? <em>Submit your event</em> and help us grow this inclusive network! 
        </div>
    """, unsafe_allow_html=True)

# Code for Map page
elif st.session_state.selected_page == "Map":
    st.header("Explore Safe Spaces in Hamburg 🗺️", divider='rainbow')
    st.markdown("""
    Click on the colored markers on the map to discover details about different safe spaces around Hamburg!  
    Each color represents a different type of space:
    """)

    # Creating columns (map in the left column, legend in the right column)
    col1, col2 = st.columns([3, 1])  #Adjusting column sizes

    # Left Column - Map
    with col1:
        # Load data from CSV (downloaded from Google Sheets)
        data = pd.read_csv('places.csv')  # Ensure this CSV is in your project folder

        # Folium Map Setup (provided by Chat gpt)
        m = folium.Map(location=[53.5511, 9.9937], zoom_start=12)

        # Add markers with dynamic colors based on category
        for _, row in data.iterrows():
            color = 'red' if row['Category'] == 'Clubs & Bars' else \
                'green' if row['Category'] == 'Community Centers' else \
                    'purple' if row['Category'] == 'Cultural Spaces' else \
                        'blue' if row['Category'] == 'Restaurants & Cafes' else 'gray'

            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                popup=f"<strong>{row['Name']}</strong><br><strong>Category:</strong> {row['Category']}<br><strong>Description:</strong> {row['Description']}",
                icon=folium.Icon(color=color)
            ).add_to(m)


        st_folium(m, width=700, height=500)

    # Right Column - Legend in Expander (styled & adjusted with Chat gpt)
    with col2:
        with st.expander("**Legend**", expanded=True):  # Set expanded=True to have it open by default
            # The coloured box containing the legend ends exactly at the text
            st.markdown("""
            <div style="
            background: linear-gradient(90deg, #d0f7f7, #e6f1ff);
            padding: 15px;
            padding-bottom: 10px;  /* No extra padding at the bottom for the legend */
            border-radius: 15px;
            font-size: 18px;
            text-align: left;
            color: #4B0082;
            ">
                <span style="color: red;">● Clubs & Bars</span><br>
                <span style="color: green;">● Community Centers</span><br>
                <span style="color: purple;">● Cultural Spaces</span><br>
                <span style="color: blue;">● Restaurants & Cafes</span>
            </div>
            """, unsafe_allow_html=True)

            # Add extra height to the expander container (white space), not affecting the legend box
            st.markdown("""
            <div style="height: 20px;"></div>  <!-- Extra white space after the legend content -->
            """, unsafe_allow_html=True)

# Code for the Events page
elif st.session_state.selected_page == "Events":
    st.header("Upcoming Events for FLINTA People🎉", divider='rainbow')
    st.markdown("""
    **Looking for upcoming events in Hamburg & the surrounding areas?**  
    We've got you covered! Just scroll through the slides to find exciting gatherings, workshops, and more! 🌈✨
    """)

    # Load events
    events = load_events().to_dict(orient="records")

    # Carousel HTML (Carousel design & technical code, improved and created with Chat gpt)
    carousel_html = """
    <div class="carousel" style="width: 100%; overflow: hidden; position: relative;">
        <style>
            .carousel-container {{
                display: flex;
                transition: transform 0.5s ease-in-out;
                width: 100%;
            }}
            .carousel-slide {{
                min-width: 100%;
                flex-shrink: 0;
                box-sizing: border-box;
                padding: 20px;
                text-align: center;
                background: linear-gradient(135deg, #00bac1, #011efe);
                border-radius: 15px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                color: white;
                height: 300px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                overflow: hidden;
                word-wrap: break-word;
            }}
            .carousel-buttons {{
                text-align: center;
                margin-top: 10px;
            }}
            .carousel-buttons button {{
                color: white;
                border: none;
                padding: 10px 20px;
                margin: 5px;
                border-radius: 5px;
                cursor: pointer;
                font-weight: bold;
            }}
            .carousel-buttons button:first-child {{
                background-color: #196415; /* Green for Previous */
            }}
            .carousel-buttons button:last-child {{
                background-color: #f9af00; /* Yellow-Orange for Next */
            }}
        </style>

        <!-- Carousel Container with Slides (including clones for seamless looping) -->
        <div class="carousel-container" id="carousel-container">
            {last_slide_clone}
            {slides}
            {first_slide_clone}
        </div>

        <!-- Navigation Buttons -->
        <div class="carousel-buttons">
            <button onclick="moveSlide(-1)">Previous</button>
            <button onclick="moveSlide(1)">Next</button>
        </div>

        <!-- JavaScript for Seamless Loop Navigation -->
        <script>
            let currentIndex = 1;
            const container = document.getElementById('carousel-container');
            const slides = container.children;
            const totalSlides = slides.length;

            container.style.transform = 'translateX(' + (-currentIndex * 100) + '%)';

            function moveSlide(direction) {{
                currentIndex += direction;
                container.style.transition = 'transform 0.5s ease-in-out';
                container.style.transform = 'translateX(' + (-currentIndex * 100) + '%)';

                container.addEventListener('transitionend', () => {{
                    if (currentIndex === totalSlides - 1) {{
                        container.style.transition = 'none';
                        currentIndex = 1;
                        container.style.transform = 'translateX(' + (-currentIndex * 100) + '%)';
                    }}
                    if (currentIndex === 0) {{
                        container.style.transition = 'none';
                        currentIndex = totalSlides - 2;
                        container.style.transform = 'translateX(' + (-currentIndex * 100) + '%)';
                    }}
                }});
            }}
        </script>
    </div>
    """

    # Generate event slides dynamically from CSV
    event_slides = ""
    for event in events:
        event_type = "Official Event" if event['source'] == "official" else "📝 User-Submitted Event"

        slide = f"""
            <div class="carousel-slide">
                <h2>{event['title']}</h2>
                <h4 style="color: yellow;">{event_type}</h4>
                <p><strong>Date:</strong> {event['date']}</p>
                <p><strong>Address:</strong> {event['address']}</p>
                <p>{event['description']}</p>
            </div>
        """
        event_slides += slide

    # Clone the first and last slides for seamless looping
    first_slide_clone = event_slides.split('</div>')[0] + '</div>'
    last_slide_clone = event_slides.split('</div>')[-2] + '</div>'

    # Inject the slides and clones into the carousel HTML
    final_carousel = carousel_html.format(
        slides=event_slides,
        first_slide_clone=first_slide_clone,
        last_slide_clone=last_slide_clone
    )

    # Display the carousel in Streamlit
    st.components.v1.html(final_carousel, height=500)

# Code for the Adding Events page
elif st.session_state.selected_page == "Add Your Event":
    st.header("Add Your Event ✏️", divider='rainbow')
    st.write(
        "Do you know about an event happening in or around Hamburg that others might be interested in? Feel free to share it with us by submitting your event here! ✨"
        "Your event will be displayed on the **Events page**, as **user-proposed event** 😊"
    )

    # Creating a submission form with different inputs
    with st.form(key="event_submission_form"):
        event_title = st.text_input("**Event Title**")
        event_date = st.date_input("**Event Date**")
        event_address = st.text_input("**Event Address**")
        event_description = st.text_area("**Event Description**")

        submit_button = st.form_submit_button("Submit Event")

        # Code for the function of the Submit button
        if submit_button:
            if event_title and event_date and event_address and event_description:
                new_event = {
                    "title": event_title,
                    "date": event_date.strftime("%Y-%m-%d"),
                    "adress": event_address,
                    "description": event_description,
                    "source": "user"
                }
                save_event(new_event)
                st.success(f"Your event '{event_title}' has been successfully added!")
            else:
                st.error("Please fill out all fields.")

    # Custom CSS for gradient button (personal design choice, made with the help of Chat gpt)
    st.markdown("""
        <style>
            /* Target the submit button inside the form */
            div.stForm button {
                background: linear-gradient(135deg, #00bac1, #011ef9);  /* Gradient from teal to deep blue */
                color: white;
                padding: 10px 24px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
                transition: background 0.3s ease;  /* Smooth transition on hover */
            }

            /* Hover effect for a brighter gradient */
            div.stForm button:hover {
                background: linear-gradient(135deg, #011ef9, #00bac1);  /* Reverse gradient on hover */
            }
        </style>
    """, unsafe_allow_html=True)

# Code for the About FLINTA page
elif st.session_state.selected_page == "About FLINTA":
    st.header("About FLINTA📖", divider='rainbow')
    st.image("flinta-app/FLINTA2.jpg")
    st.markdown("""
        **Welcome to the FLINTA Space**

        Are you wondering what **FLINTA** stands for? 🤔  
        Scroll down to discover the meaning behind this empowering acronym and learn about the vibrant community it represents!

        ---
    """)
    # Additional text to be displayed above the expanders
    st.markdown("""
    The acronym **FLINTA*** stands for women, lesbians, intersex, non-binary, trans, and agender people – in other words, for all those who are patriarchally discriminated against because of their gender identity. The term FLINTA* is often used to make it clear who is welcome in certain spaces and at specific events.
    """)

    # Custom Expandable Sections with Inline Styling (All titles in black text)
    def colored_expander(title, content, color, text_color='black'):  # Set default title color to black
        st.markdown(f"""
            <details style="
                background-color: {color};
                color: {text_color};
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 10px;
                box-shadow: 2px 2px 8px rgba(0,0,0,0.2);
            ">
                <summary style="
                    font-size: 16px;
                    font-weight: normal;
                    cursor: pointer;
                    padding: 5px 0;
                    font-family: 'Arial', sans-serif;
                    color: black;  /* Ensure title text is black */
                ">{title}</summary>
                <div style="padding: 10px; color: black; background-color: #ffffff; border-radius: 10px; margin-top: 10px;">
                    {content}
                </div>
            </details>
        """, unsafe_allow_html=True)


    # Rainbow Colors for each expandable section
    colored_expander("F - Frauen (Women) 👩‍🦰",
                     "Women usually refers to cisgender heterosexual women, meaning women whose biological sex aligns with their gender identity.",
                     "#FF6B6B")

    colored_expander("L - Lesben (Lesbians) 👭",
                     "Although being a lesbian is generally considered a sexual orientation rather than a gender identity, the term has been included in the acronym to highlight feminist achievements that are largely credited to the lesbian movement. It also serves to critique the fact that, in a heteronormative society, it is often assumed that sex and romantic relationships with cisgender men are an inherent part of femininity.",
                     "#FFB26B")

    colored_expander("I - Inter (Intersex) ⚧",
                     "Intersex people have innate gender characteristics that are not clearly accepted by societal and medical norms, meaning they do not fit into the categories of male or female, whether genetically, hormonally, or anatomically.",
                     "#FFD93D")

    colored_expander("N - Nicht-binär (Non-binary) 💛🤍💜🖤",
                     "Non-binary refers to people who do not (only) identify with one of the two supposedly biological sexes. They may position themselves somewhere between these two genders, outside of them, or fluid in their gender identity.",
                     "#6BCB77")

    colored_expander("T - Trans (Transgender) 🏳️‍⚧️",
                     "Trans people do not identify with the gender they have lived in up until now and wish to live physically and socially in the other of the two genders.",
                     "#4D96FF")

    colored_expander("A - Agender/Andere (Agender/Others) 🌍",
                     "Agender people, some of whom also use the term genderless, do not feel they belong to any gender and may completely reject the concept of gender. Being agender is a specific expression of non-binarism, which is why the abbreviation FLINT* is sometimes used, where agender people can identify with either the N or the asterisk (*).",
                     "#C77DFF")

    st.markdown("ℹ️ **The gender asterisk (*)** aims to include those individuals who do not find themselves in any of the letters but are also marginalized in a patriarchal, heteronormative majority society because of their gender identity. This means anyone who is not a cisgender man — including gay or bisexual cisgender men, who are therefore not part of this group.")

# Code for the Feedback page
elif st.session_state.selected_page == "Feedback":
    st.header("Feedback 💬", divider="rainbow")
    st.markdown("""
    Since this website is still a work in progress, we would greatly appreciate your feedback!  
    Your thoughts and suggestions help us improve and make this space even better.  
    Feel free to let us know what you like, what we could improve, or any ideas you have!
    """)
    # Subheader
    st.subheader("Rate Different Aspects of the Website:")

    # 1.slider - rating navigation
    usability_rating = st.select_slider(
        "**How easy was it to navigate the website?**",
        options=['😞', '🙁', '😐', '🙂', '😍'],
        value='😐',  # Default value to Neutral
    )

    # 2.slider - rating quality
    content_rating = st.select_slider(
        "**How would you rate the quality of the content?**",
        options=['😞', '🙁', '😐', '🙂', '😍'],
        value='😐',  # Default value to Neutral
    )

    # 3.slider - rating design
    design_rating = st.select_slider(
        "**How visually appealing is the website design?**",
        options=['😞', '🙁', '😐', '🙂', '😍'],
        value='😐',  # Default value to Neutral
    )

    # 4.slider - rating experience
    satisfaction_rating = st.select_slider(
        "**How satisfied are you with your overall experience?**",
        options=['😞', '🙁', '😐', '🙂', '😍'],
        value='😐',  # Default value to Neutral
    )

    # Feedback Form
    with st.form(key="feedback_form"):
        # Submit Button for feedback
        submit_button = st.form_submit_button("Submit Feedback")

        # Handle the submission through submit button - data stored in MonoDB
        if submit_button:
            # Connect to MongoDB
            client = connect_to_mongo()
            # Select the database and collection
            db = client['feedback_db']
            collection = db['feedback_data']

            # Create the document to insert into MongoDB
            feedback_document = {
                "usability_rating": usability_rating,
                "content_rating": content_rating,
                "design_rating": design_rating,
                "satisfaction_rating": satisfaction_rating,
                "created_at": datetime.datetime.now()
            }

            # Insert the feedback document into the collection
            collection.insert_one(feedback_document)

            # Display success message for the user
            st.success("Your feedback has been submitted! Thank you for your input!")

    # Custom CSS for gradient button (design choice, made with the help of Chat gpt)
    st.markdown("""
        <style>
            /* Target the submit button inside the feedback form */
            div.stForm button {
                background: linear-gradient(135deg, #00bac1, #011ef9);  /* Gradient from teal to deep blue */
                color: white;
                padding: 10px 24px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
                transition: background 0.3s ease;  /* Smooth transition on hover */
            }

            /* Hover effect for a brighter gradient */
            div.stForm button:hover {
                background: linear-gradient(135deg, #011ef9, #00bac1);  /* Reverse gradient on hover */
            }
        </style>
    """, unsafe_allow_html=True)
