#!/usr/bin/env python
# coding: utf-8

import os
import sys
try:
    import streamlit as st
    import requests
except ImportError as e:
    import traceback
    print(f"Error importing required packages: {e}")
    print(traceback.format_exc())
    try:
        # If streamlit is successfully imported, show error in UI
        if 'st' in globals():
            st.error(
                f"Failed to import required packages. Please install them using: pip install -r requirements.txt\n\nError: {e}")
            st.stop()
    except:
        # If we can't even use streamlit, exit the program
        sys.exit(1)

# App configuration
st.set_page_config(page_title="YouTube Script Assistant", page_icon="🎬")

# Title and description
st.title('🦜🔗 YouTube Script Assistant')
st.image('./Youtube.png')
st.markdown(
    "Generate engaging YouTube video titles and scripts with AI assistance")

# Sidebar for API key and settings
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input(
        "OpenAI API Key", type="password",
        value="210167a306e2affee74535654c4b8ed5",
        help="Enter your OpenAI API key or set OPENAI_API_KEY in .env file")

    # Use API key from input or environment variable
    if api_key:
        os.environ['OPENAI_API_KEY'] = api_key

    if not os.environ.get('OPENAI_API_KEY'):
        st.error("Please add your OpenAI API key to continue.")
        st.stop()

print("====================================")
print(f"API Key: {os.environ.get('OPENAI_API_KEY')}")
print("====================================")

# Main content
topic = st.text_area('Enter your video topic:', height=100)
print(f"Topic: {topic}")

# Generate content when button is pressed
if st.button('Generate Script') and topic:
    pass
#     try:
#         with st.spinner('Generating title...'):
#             llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=temperature)
#             title_chain = LLMChain(llm=llm, prompt=title_template,
#                                    verbose=True, output_key='title', memory=title_memory)
#             title = title_chain.run(topic)

#         with st.spinner('Researching content...'):
#             wiki_research = wiki.run(topic)

#         with st.spinner('Writing script...'):
#             script_chain = LLMChain(llm=llm, prompt=script_template,
#                                     verbose=True, output_key='script', memory=script_memory)
#             script = script_chain.run(
#                 title=title, wikipedia_research=wiki_research)

#         # Display results
#         st.subheader("Generated Title:")
#         st.success(title)

#         st.subheader("Generated Script:")
#         st.write(script)

#         # Expandable sections for additional info
#         with st.expander('Title History'):
#             st.info(title_memory.buffer)

#         with st.expander('Script History'):
#             st.info(script_memory.buffer)

#         with st.expander('Wikipedia Research'):
#             st.info(wiki_research)

#         # Download options
#         st.download_button(
#             label="Download Script",
#             data=f"TITLE: {title}\n\n{script}",
#             file_name="youtube_script.txt",
#             mime="text/plain"
#         )

#     except Exception as e:
#         st.error(f"An error occurred: {e}")

# elif topic == "":
#     st.info("Please enter a topic to generate a YouTube script.")
