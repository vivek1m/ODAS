import streamlit
from getters.prompts import get_drug, get_diagnosis, q_n_a
from utils.predict_utils import predict_sentence
from utils.pdf_extraction import extract_from_pdf, extract_from_pdfs


def show_results(container, query, text_docs):
    cnt = 1

    for i in get_matches(query, text_docs):
        cnt += 1        

def get_cancer_matches(results):
    matches = sorted(results, key=results.get,reverse=True) # top match at index 0
    match = ""
    for j in range(len(matches)):
        match += "<br>" + acc_cancer.format(matches[j], f"{results[matches[j]] * 100:.2f} %")

    return match 

# static text
about = open("about.txt","r")
info = about.read()
title = "Oncology Document Analyzer System"

acc_cancer = "<i>{}</i>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code style='font-size:15px'>{}</code><br>"
footer = f"""<footer style="left: 0;
                            bottom: 0;
                            width: 100%;
                            padding-top: 120px;
                            font-size: medium;
                            text-align: center;">
                Copyright © ODAS | <a style="text-decoration: none;" href={}> GitHub</a>
            </footer>"""


#persistent data
if 'home' not in st.session_state:
    st.session_state.home = True
if 'text_prompt' not in st.session_state:
    st.session_state.text_prompt = ""
if 'cancer' not in st.session_state:
    st.session_state.cancer = ""
if 'file_input' not in st.session_state:
    st.session_state.file_input = None
if 'file_content' not in st.session_state:
    st.session_state.file_content = ""

st.markdown('<h1 style="text-align:center; font-family:Verdana;">O D A S</h1>',
            unsafe_allow_html=True)
st.markdown(f'<p style="text-align:center; font-family:Verdana;">{title}</p>',
            unsafe_allow_html=True)

text, search, chat = st.tabs(["Oncology Classification", "Search", "ONCObot"])   # tabs

about.close()

with text:
    if st.session_state.home:
        st.session_state.text_prompt = st.text_area(label="Enter any text")
        st.markdown('<h5 style="text-align:center;">or</h5>',unsafe_allow_html=True)
        st.session_state.file_input = st.file_uploader("Upload PDF(s)",accept_multiple_files=True)
        st.markdown(footer,unsafe_allow_html=True)

        if (st.session_state.text_prompt or st.session_state.file_input):
            if st.session_state.text_prompt != "":
                st.session_state.cancer = get_cancer_matches(predict_sentence(
                    st.session_state.text_prompt))    # model prediction w/ prompt
            elif st.session_state.file_input is not None:
                if(str(type(st.session_state.file_input).__name__)=='list'):
                    st.session_state.file_content = extract_from_pdfs(st.session_state.file_input)
                else:
                    st.session_state.file_content = extract_from_pdf(st.session_state.file_input)
                st.session_state.cancer = get_cancer_matches(predict_sentence(
                    st.session_state.file_content))   # model prediction w/ file
            
    if not st.session_state.home:
        st.markdown(f'<h3><b>Cancer \tMatches<b> :</h3><h5>{st.session_state.cancer}</h5>',
                    unsafe_allow_html=True)
    
        st.markdown('<h2 style="font-style:italic;">Drug Use Advisory</h2>',
                unsafe_allow_html=True)
        # Drug call
        st.markdown(get_drug(st.session_state.text_prompt,st.session_state.cancer)
                    .choices[0].message.content)
        st.markdown('<h2 style="font-style:italic;">Diagnosis</h2>',
                    unsafe_allow_html=True)
        time.sleep(0.5)
        # Diagnosis call 
        st.markdown(get_diagnosis(st.session_state.text_prompt,st.session_state.cancer)
                    .choices[0].message.content)


with search:
    results = """<i style="font-family:Verdana;">{}</i>"""

    with qtr1:
        query = st.text_input("Enter Keywords")
    with qtr2:
        st.write("\n")
        st.write("\n")        
        find = st.button("Search")

    if find or query:
        with st.spinner("Searching the document(s) for matches"):
            st.markdown("Relevant matches")
            container = st.container(border=True)

            if(st.session_state.text_prompt or st.session_state.file_content) == "":
                container.write("Please provide text in the classification section. ")
            elif query=="":
                container.write("Please enter a keyword to search")
            else:
                time.sleep(5)
                
                if st.session_state.text_prompt != "":
                    show_results(container, query,st.session_state.text_prompt)
                elif st.session_state.file_input is not None:
                    if(str(type(st.session_state.file_input).__name__)=='list'):
                        st.session_state.file_content = extract_from_pdfs(st.session_state.file_input)
                    else:
                        st.session_state.file_content = extract_from_pdf(st.session_state.file_input)
                    show_results(container, query, st.session_state.file_content)

    st.markdown(footer, unsafe_allow_html=True)
with chat:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if st.session_state.messages != []:
        st.markdown("Chat History")
        for message in st.session_state.messages:
            with st.chat_message(message['role']):
                st.markdown(message["content"])

    if prompt := st.chat_input("Summarize this is 50 words..."):
        st.session_state.messages.append({'role':'user','content':prompt})
        with st.chat_message('user'):
            st.markdown(prompt)
            
        if st.session_state.file_input is not None:
            if(str(type(st.session_state.file_input).__name__)=='list'):
                st.session_state.file_content = extract_from_pdfs(st.session_state.file_input)
            else:
                st.session_state.file_content = extract_from_pdf(st.session_state.file_input)
            response = q_n_a(st.session_state.file_content,prompt)
        elif st.session_state.text_prompt != "":
            response = q_n_a(st.session_state.text_prompt,prompt)

        st.session_state.messages.append({'role':'assistant',
                                          'content':response.choices[0].message.content})
        with st.chat_message("assistant"):
            st.markdown(response.choices[0].message.content)