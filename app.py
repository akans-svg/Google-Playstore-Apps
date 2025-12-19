import streamlit as st
import pandas as pd
from src.data_loader import load_and_process_data
from src.visualizer import create_category_chart, create_rating_density_chart, create_price_vs_rating_chart
from src.report_gen import generate_pdf

# Page Config
st.set_page_config(page_title="Play Store Analytics", layout="wide")

st.title("Google Play Store Analytics Pro")
st.markdown("Upload your dataset to generate a professional analysis report.")

# --- 1. BROWSE / UPLOAD SECTION ---
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # --- 2. PROCESSING ---
    with st.spinner('Processing Data...'):
        try:
            df = load_and_process_data(uploaded_file)
            st.success("Data successfully loaded and cleaned!")
        except Exception as e:
            st.error(f"Error loading data: {e}")
            st.stop()

    # --- 3. PREVIEW DATASET ---
    st.subheader("1. Dataset Preview")
    st.dataframe(df.head())
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Apps", len(df))
    col2.metric("Avg Rating", f"{df['Rating'].mean():.2f}")
    col3.metric("Free Apps", len(df[df['Type']=='Free']))

    # --- 4. VISUALIZATIONS ---
    st.subheader("2. Visualizations")
    
    # Generate Figures
    fig_cat = create_category_chart(df)
    fig_rate = create_rating_density_chart(df)
    fig_price = create_price_vs_rating_chart(df)

    # Display in Grid
    c1, c2 = st.columns(2)
    with c1:
        st.pyplot(fig_cat)
    with c2:
        st.pyplot(fig_rate)
    
    st.pyplot(fig_price)

    # --- 5. DOWNLOAD SECTION ---
    st.subheader("3. Export Report")
    
    # Compile dictionary of figures for the PDF
    figures = {
        "Category Distribution": fig_cat,
        "Rating Density": fig_rate,
        "Price vs Rating": fig_price
    }

    if st.button('Generate PDF Report'):
        with st.spinner("Generating PDF..."):
            pdf_bytes = generate_pdf(df, figures)
            
            st.download_button(
                label="Download Full Report (PDF)",
                data=pdf_bytes,
                file_name="PlayStore_Analysis_Report.pdf",
                mime="application/pdf"
            )
            
    # Option to download Cleaned CSV
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Cleaned Dataset (CSV)",
        data=csv_data,
        file_name="cleaned_googleplaystore.csv",
        mime="text/csv"
    )

else:
    st.info("Please upload a CSV file to begin.")