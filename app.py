import streamlit as st
import google.generativeai as genai
from datetime import datetime
from fpdf import FPDF

# --- Gemini API Setup ---
genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("Model_Version")


# --- Functions ---
def diagnosis_agent(symptoms):
    prompt = f"""
    You are simulating a virtual doctor in a multi-agent AI healthcare chatbot system (for academic use only).
    The patient reports: {symptoms}
    Based on common clinical knowledge, provide a likely diagnosis and short explanation.
    """
    return model.generate_content(prompt).text.strip()

def pharmacy_agent(diagnosis):
    prompt = f"""
    You are simulating a pharmacist agent.
    Based on this diagnosis: "{diagnosis}", list common OTC medicines for demo purposes.
    """
    return model.generate_content(prompt).text.strip()

def consultation_agent(diagnosis):
    prompt = f"""
    You are simulating a medical advisor chatbot.
    Based on this diagnosis: "{diagnosis}", provide final advice and end with 'CONSULTATION_COMPLETE'.
    """
    return model.generate_content(prompt).text.strip()

def save_to_pdf(symptoms, diagnosis, meds, advice):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="AI Healthcare Consultation Report", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt=f"Symptoms: {symptoms}\n\nDiagnosis: {diagnosis}\n\nMedications: {meds}\n\nFinal Advice: {advice}")
    filename = f"consultation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

# --- Streamlit UI ---
st.set_page_config(page_title="AI Healthcare Chatbot", page_icon="🩺")
st.image("https://cdn-icons-png.flaticon.com/512/3774/3774299.png", width=100)
st.title("🤖 Gemini Multi-Agent Healthcare Chatbot")

symptoms = st.text_area("🩺 Please describe your symptoms")
if st.button("Start Consultation") and symptoms.strip():
    with st.spinner("Diagnosing symptoms..."):
        diagnosis = diagnosis_agent(symptoms)
        meds = pharmacy_agent(diagnosis)
        advice = consultation_agent(diagnosis)

    st.subheader("📋 Diagnosis")
    st.markdown(diagnosis)

    st.subheader("💊 Medications")
    st.markdown(meds)

    st.subheader("🧾 Final Advice")
    st.markdown(advice)

if st.button("🔄 Reset"):
    st.write("Please manually refresh the page to reset.")
