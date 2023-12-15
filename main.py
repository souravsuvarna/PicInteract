from tempfile import NamedTemporaryFile
import streamlit as st
from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from tools import ImageCaptionTool, ObjectDetectionTool

##############################
### initialize agent #########
##############################
tools = [ImageCaptionTool(), ObjectDetectionTool()]

conversational_memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=5,
    return_messages=True
)

llm = ChatOpenAI(
    openai_api_key='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',
    temperature=0,
    model_name="gpt-3.5-turbo"
)

agent = initialize_agent(
    agent="chat-conversational-react-description",
    tools=tools,
    llm=llm,
    max_iterations=5,
    verbose=True,
    memory=conversational_memory,
    early_stopping_method='generate'
)
st.set_page_config(page_title="PicInteract", page_icon=":zap:")

st.markdown("""
    <h1 style='text-align: center; font-family: "silver-forte", sans-serif; color: white;'>
        <span style='color: white;'>Pic</span><span style='color: gold;'>Interact</span>
    </h1>
    <style>
        h1 {
            font-size: 3.2em;
            vertical-align: super;
            color: rgba(144, 141, 143, 0.9);
            letter-spacing: 1px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #E9E8E8; font-family:'alata', sans-serif;'> Beyond the Frame, Where Every Pixel Holds a Query.</p>", unsafe_allow_html=True)
st.title("")

st.markdown("""
    <p class="a" style='font-family: "sans-serif", Arial; color: white;'>
        Prompt the thoughts, one at a time.
    </p>
    <style>
        p.a{
            font-size:1.2em;
            font-style: italic;
            vertical-align: super;
            color: rgba(144, 141, 143, 0.9);
        }
    </style>
""", unsafe_allow_html=True)

# set header
# st.caption("Please upload an image")

# upload file
file = st.file_uploader("", type=["jpeg", "jpg", "png"])

if file:
    # display image
    st.image(file, use_column_width=True)

    # text input
    user_question = st.text_input('Ask a question about your image:')

    ##############################
    ### compute agent response ###
    ##############################
    with NamedTemporaryFile(dir='.', delete=False) as f:
        f.write(file.getbuffer())
        image_path = f.name

        # Explicitly close the file to ensure it's not deleted immediately
        f.close()

        # Now you can use image_path without any issues

    if user_question and user_question != "":
        with st.spinner(text="In progress..."):
            response = agent.run('{}, this is the image path: {}'.format(user_question, image_path))
            st.write(response)
