import datetime as dt

import gspread
import streamlit as st

st.set_page_config(
    page_title="Question :: Problem Set Generator",
    page_icon="🔢",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if ("auth" not in st.session_state) or (not st.session_state["auth"]):
    st.error(
        "&ensp; **You are unauthorized to see this page.** Please login.", icon="🔒"
    )
    st.stop()


@st.cache_resource(show_spinner="Loading...")
def connect_to_gsheets(worksheet: str):
    gc = gspread.service_account_from_dict(st.secrets["GSHEETS_CREDS"])
    sh = gc.open("Board Review")
    ws = sh.worksheet(worksheet)
    return ws


ws = connect_to_gsheets("QnA")

subject_tags = [
    "PCP",
    "CHE",
    "GEN",
    "MIX",
    "ChE Calculations",
    "Unit Operations",
    "Leaching",
    "Liquid-liquid Extraction",
    "Distillation",
    "Screening",
    "Size Reduction",
    "Sedimentation",
    "Centrifugation",
    "Filtration",
    "Fluidization",
    "Diffusion/Gas Absorption",
    "Evaporation",
    "Crystallization",
    "Humidification",
    "Drying",
    "Momentum Transfer",
    "Heat Transfer",
    "Mass Transfer",
    "Chemical Reaction Engineering",
    "Pre-Calculus",
    "Plane and Solid Geometry",
    "Analytic Geometry",
    "Differential Calculus",
    "Integral Calculus",
    "Differential Equations",
    "Engineering Data Analysis",
    "Engineering Economics",
    "Physics",
    "Engineering Mechanics",
    "General Chemistry",
    "Analytical Chemistry",
    "Organic Chemistry",
    "Physical Chemistry",
    "ChE Thermodynamics",
    "Industrial Waste Management and Control",
    "Environmental Engineering",
    "Materials Science and Engineering",
    "Solution Thermodynamics",
    "Biochemical Engineering",
    "Chemical Process Industries",
    "Instrumentation and Process Control",
    "Plant Design",
    "ChE Laws, Ethics, Contracts",
    "Engineering Management",
    "Process Safety",
]

# Main ========================================================================

# r0c1, _fill0, r0c2 = st.columns([15, 1, 15])
# with r0c1:
#     st.subheader("Data Input", anchor=False)
# with r0c2:
#     st.subheader("Preview", anchor=False)

if "question_input" not in st.session_state:
    st.session_state["question_input"] = "Hello"
if "choice1" not in st.session_state:
    st.session_state["choice1"] = "Hello"
if "choice2" not in st.session_state:
    st.session_state["choice2"] = "World"
if "choice3" not in st.session_state:
    st.session_state["choice3"] = "Goodbye"
if "choice4" not in st.session_state:
    st.session_state["choice4"] = "Okay"
if "correct_answer_input" not in st.session_state:
    st.session_state["correct_answer_input"] = "Hello"
if "tags_input" not in st.session_state:
    st.session_state["tags_input"] = []

with st.expander("**Question Input**", expanded=True):
    r1c1, _fill1, r1c2 = st.columns([15, 1, 15])

    with r1c1:
        question_input = st.text_area(
            "Enter **QUESTION** with Markdown and $\LaTeX$ formatting:",
            key="question_field",
            height=200,
            # value=st.session_state["question_input"],
        ).strip()
        st.session_state["question_input"] = question_input
    with r1c2:
        st.markdown(f"**PREVIEW**:\n\n{question_input}", unsafe_allow_html=True)

with st.expander("**Choices and Answer**", expanded=True):
    r2c1, _fill2, r2c2 = st.columns([15, 1, 15])

    with r2c1:
        opta, optb = st.columns(2)

        with opta:
            choice1 = st.text_input(
                "Option 1:",
                key="choice1_field",
                placeholder="A",
            ).strip()
            choice2 = st.text_input(
                "Option 2:",
                key="choice2_field",
                placeholder="B",
            ).strip()
            st.session_state["choice1"] = choice1
            st.session_state["choice2"] = choice2
        with optb:
            choice3 = st.text_input(
                "Option 3:",
                key="choice3_field",
                placeholder="C",
            ).strip()
            choice4 = st.text_input(
                "Option 4:",
                key="choice4_field",
                placeholder="D",
            ).strip()
            st.session_state["choice3"] = choice3
            st.session_state["choice4"] = choice4

        if choice1 and choice2 and choice3 and choice4:
            disabled_answer = False
        else:
            disabled_answer = True

        correct_answer = st.selectbox(
            "Select **CORRECT** answer:",
            [choice1, choice2, choice3, choice4],
            disabled=disabled_answer,
            key="correct_answer_field",
        )

    with r2c2:
        if choice1 and choice2 and choice3 and choice4:
            st.write("**PREVIEW**")
            preview_answer = st.radio(
                "Select Answer:",
                [choice1, choice2, choice3, choice4],
                key="answer_input",
            )
            if preview_answer == correct_answer:
                st.success(f"**Correct!** The answer is: **:orange[{correct_answer}]**")
            else:
                st.error(f"**Incorrect!** The answer is: **:orange[{correct_answer}]**")

        else:
            st.write("")
            st.warning("Please enter all choices.", icon="⚠️")

with st.expander("**Tags**", expanded=True):
    question_tags = st.multiselect(
        "Select **TAGS**:",
        subject_tags,
        key="tags_field",
        default=st.session_state["tags_input"],
    )

st.write("---")

if (
    question_input
    and choice1
    and choice2
    and choice3
    and choice4
    and correct_answer
    and question_tags
):
    unsubmittable = False
else:
    unsubmittable = True

choices = "; ".join([choice1, choice2, choice3, choice4])
tags = "; ".join(question_tags)

data = ['=INDIRECT("R[-1]C",FALSE)+1', question_input, choices, correct_answer, tags]

check1, _cfill, check2 = st.columns([25, 7, 10])

with check1:
    st.markdown(
        f"""
#### Verify Output:

{question_input}

The choices to be inputted are:
```csv
{choices}
```

And the correct answer is: 
```
{correct_answer}
```

The tags are:
```
{tags}
```
    """
    )

with check2:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    if st.button("Submit Data", type="primary", disabled=unsubmittable):
        st.balloons()
        ws.append_row(data, value_input_option="USER_ENTERED")
        st.toast("Question saved!", icon="💾")
        st.session_state["question_input"] = "Hello"
        st.session_state["choice1"] = "Hello"
        st.session_state["choice2"] = "World"
        st.session_state["choice3"] = "Goodbye"
        st.session_state["choice4"] = "Okay"
        st.session_state["correct_answer_input"] = "Hello"
        st.session_state["tags_input"] = []
