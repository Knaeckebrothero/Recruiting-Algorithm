import streamlit as st
import pickle
import spacy
from wordcloud import WordCloud
import pdfplumber
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
import pandas as pd
import seaborn as sns
import numpy as np

# Attempt to load the spaCy model, downloading it if necessary
try:
    nlp = spacy.load("en_core_web_sm")
except IOError:
    print("Downloading the spaCy language model...")
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Define the text preprocessing function using spaCy
def preprocess_text(text):
    doc = nlp(text)
    clean = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and token.is_alpha]
    return " ".join(clean)

# Load the model pipeline from file
with open('./Models/model_res.pkl', 'rb') as file:
    model_pipeline = pickle.load(file)

# Define the category mapping for prediction output
category_mapping = {
    15: "Java Developer",
    23: "Testing",
    8: "DevOps Engineer",
    20: "Python Developer",
    24: "Web Designing",
    12: "HR",
    13: "Hadoop",
    3: "Blockchain",
    10: "ETL Developer",
    18: "Operations Manager",
    6: "Data Science",
    22: "Sales",
    16: "Mechanical Engineer",
    1: "Arts",
    7: "Database",
    11: "Electrical Engineering",
    14: "Health and fitness",
    19: "PMO",
    4: "Business Analyst",
    9: "DotNet Developer",
    2: "Automation Testing",
    17: "Network Security Engineer",
    21: "SAP Developer",
    5: "Civil Engineer",
    0: "Advocate",
}

# Function to predict the category of a resume
def predict_category(text):
    cleaned_text = preprocess_text(text)
    prediction_id = model_pipeline.predict([cleaned_text])[0]
    return category_mapping.get(prediction_id, "Unknown")

# Function to extract text from a PDF file using pdfplumber
def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        pages = pdf.pages[0]
        pdf_text = pages.extract_text()
    return pdf_text

def getResult(JD_txt, resume_txt):
    content = [JD_txt, resume_txt]
    cv = CountVectorizer()
    matrix = cv.fit_transform(content)
    similarity_matrix = cosine_similarity(matrix)
    match = similarity_matrix[0][1] * 100
    return match

def plot_term_frequency(text):
    words = text.split()
    word_freq = Counter(words)
    most_common_words = word_freq.most_common(10)
    words_df = pd.DataFrame(most_common_words, columns=['Word', 'Frequency'])

    plt.figure(figsize=(10, 6))
    sns.barplot(x='Frequency', y='Word', data=words_df, palette='viridis')
    plt.title('Top 10 Most Common Words in Resume')
    plt.xlabel('Frequency')
    plt.ylabel('Word')
    st.pyplot(plt)

def plot_skills_match(resume_text, job_text):
    resume_words = resume_text.split()
    job_words = job_text.split()

    resume_freq = Counter(resume_words)
    job_freq = Counter(job_words)

    common_words = set(resume_freq.keys()).intersection(set(job_freq.keys()))
    common_freq = [(word, resume_freq[word], job_freq[word]) for word in common_words]

    words_df = pd.DataFrame(common_freq, columns=['Word', 'Resume_Frequency', 'Job_Frequency'])

    plt.figure(figsize=(10, 6))
    sns.barplot(x='Resume_Frequency', y='Word', data=words_df, label='Resume', color='b', alpha=0.6)
    sns.barplot(x='Job_Frequency', y='Word', data=words_df, label='Job', color='g', alpha=0.6)
    plt.legend()
    plt.title('Skills Match Analysis')
    plt.xlabel('Frequency')
    plt.ylabel('Skill')
    st.pyplot(plt)

def plot_experience_timeline():
    # Example data for experience timeline
    experience_data = {
        'Role': ['Data Scientist', 'Data Analyst', 'Software Engineer'],
        'Start Year': [2020, 2018, 2015],
        'End Year': [2022, 2020, 2018]
    }
    experience_df = pd.DataFrame(experience_data)

    fig, ax = plt.subplots(figsize=(10, 6))
    for index, row in experience_df.iterrows():
        ax.plot([row['Start Year'], row['End Year']], [row['Role'], row['Role']], marker='o')

    ax.set_title("Timeline of Candidate's Work Experience")
    ax.set_xlabel('Year')
    ax.set_ylabel('Role')
    st.pyplot(fig)

def plot_education_timeline():
    # Example data for education timeline
    education_data = {
        'Degree': ['B.Sc. Computer Science', 'M.Sc. Data Science'],
        'Year': [2015, 2018]
    }
    education_df = pd.DataFrame(education_data)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(education_df['Degree'], education_df['Year'])
    ax.set_title("Timeline of Candidate's Education")
    ax.set_xlabel('Year')
    ax.set_ylabel('Degree')
    st.pyplot(fig)

def plot_profile_summary():
    # Example data for profile summary
    profile_data = {
        'Dimension': ['Technical Skills', 'Experience', 'Education', 'Soft Skills'],
        'Score': [80, 70, 90, 85]
    }
    profile_df = pd.DataFrame(profile_data)

    fig, ax = plt.subplots()
    sns.barplot(x='Dimension', y='Score', data=profile_df, ax=ax)
    ax.set_title("Profile Summary")
    st.pyplot(fig)

def plot_profile_radar_chart():
    # Example data for radar chart
    labels = ['Technical Skills', 'Experience', 'Education', 'Soft Skills']
    scores = [80, 70, 90, 85]
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    scores += scores[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, scores, color='red', alpha=0.25)
    ax.plot(angles, scores, color='red', linewidth=2)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_title('Candidate Profile Radar Chart')
    st.pyplot(fig)

def main():
    st.title("IBIS/EBIS Project Advanced Resume Screening App", anchor=None)
    st.markdown('<p class="big-font">Welcome to your Candidate Screening App!</p>', unsafe_allow_html=True)
    st.markdown("## Upload candidates resume and job posting to receive an overview of the candidate:")

    # Using columns to layout the file uploader and text box
    col1, col3 = st.columns(2)

    with col1:
        uploaded_files = st.file_uploader("Upload Resumes", type=["txt", "pdf"], accept_multiple_files=True)

    with col3:
        uploaded_file2 = st.file_uploader("Upload Job Posting/Requirement", type=["txt", "pdf"])

    job_text = ""
    if uploaded_file2 is not None:
        if uploaded_file2.type == "application/pdf":
            job_text = extract_text_from_pdf(uploaded_file2)
        elif uploaded_file2.type == "text/plain":
            job_text = uploaded_file2.getvalue().decode("utf-8")

    if st.button("Process") and uploaded_files and job_text:
        results = []
        for uploaded_file in uploaded_files:
            resume_text = ""
            if uploaded_file.type == "application/pdf":
                resume_text = extract_text_from_pdf(uploaded_file)
            elif uploaded_file.type == "text/plain":
                resume_text = uploaded_file.getvalue().decode("utf-8")

            if resume_text:
                with st.spinner(f"Analyzing {uploaded_file.name}..."):
                    # Predict Job Category
                    category = predict_category(resume_text)

                    # Match Job Description with resume
                    match = getResult(job_text, resume_text)
                    match = round(match, 2)

                    results.append((uploaded_file.name, match, category, resume_text))

        # Sort results by match percentage
        results.sort(key=lambda x: x[1], reverse=True)

        # Display results table
        st.markdown("## Top Candidates")
        results_df = pd.DataFrame(results, columns=['Candidate', 'Match Percentage', 'Category', 'Resume Text'])
        st.dataframe(results_df[['Candidate', 'Match Percentage', 'Category']])

        # Display detailed results
        st.markdown("## Detailed Analysis for each candidate")
        for name, match, category, resume_text in results:
            st.markdown(f"### {name}")
            st.markdown(f"**Predicted Category:** {category}")
            st.markdown(f"**Match Percentage:** {match}%")
            cleaned_text = preprocess_text(resume_text)
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(cleaned_text)
            fig, ax = plt.subplots()
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig)

            plot_term_frequency(cleaned_text)
            plot_skills_match(cleaned_text, preprocess_text(job_text))
            plot_experience_timeline()
            plot_education_timeline()
            plot_profile_summary()
            plot_profile_radar_chart()

            #Preprocessing todo en pequqeno
            #Timeline con educacion y trabajo al mismo tiempo

if __name__ == "__main__":
    main()
