import io  # 🟢 Added to handle in-memory file streams
import streamlit as st
from engine import run_scraper
from tasks import AccountIntelligencePipeline

def compile_campaign_txt(pitch_data: dict) -> str:
    """Combines structured campaign dictionary keys into a beautifully formatted text report."""
    output = []
    output.append("=========================================================================")
    output.append("       FORGEREACH AI - MULTI-CHANNEL OUTBOUND CAMPAIGN SEQUENCE         ")
    output.append("=========================================================================\n")
    
    # Extract Cold Email
    email = pitch_data.get("cold_email", {})
    output.append("--- STEP 1: COLD EMAIL ---")
    output.append(f"Subject: {email.get('subject', 'No Subject Generated')}")
    output.append(f"Body:\n{email.get('body', '')}\n")
    output.append("-" * 40 + "\n")
    
    # Extract LinkedIn
    output.append("--- STEP 2: LINKEDIN NOTE ---")
    output.append(f"{pitch_data.get('linkedin_note', '')}\n")
    output.append("-" * 40 + "\n")
    
    # Extract Follow-up
    follow_up = pitch_data.get("value_add_follow_up", {})
    output.append("--- STEP 3: VALUE-ADD FOLLOW-UP ---")
    output.append(f"Subject: {follow_up.get('subject', 'No Subject Generated')}")
    output.append(f"Body:\n{follow_up.get('body', '')}")
    output.append("\n=========================================================================")
    
    return "\n".join(output)


# 1. Page Configuration Settings
# 🟢 CORRECT
st.set_page_config(
    page_title="Multi-Agent Intelligence Studio", 
    page_icon="🤖", 
    layout="wide"
)

# 2. UI Header Configuration
st.title("🤖 Multi-Agent Intelligence Studio")
st.write("Orchestrating a specialized AI workforce to analyze corporate accounts and draft tailored outreach campaigns.")
st.markdown("---")

# 3. User Input Collection Elements
company_url = st.text_input(
    "Target Company Website Domain:", 
    placeholder="https://example.com",
    help="Enter the root domain or full landing page address of your prospective target company."
)

offered_service = st.text_area(
    "Your Core Service Offering:", 
    placeholder="Describe what you sell, your target metrics, and value proposition...",
    height=150,
    help="Detail your product or services so the market strategist agent can map it back to target friction points."
)

# 4. Pipeline Execution Lifecycle
if st.button("Run Multi-Agent Pipeline", type="primary"):
    if not company_url or not offered_service:
        st.warning("⚠️ Action Blocked: Please populate both the company website URL and your service offering.")
    else:
        # Uniform resource locator sanitization
        if not company_url.startswith("http"):
            company_url = "https://" + company_url
            
        # --- PHASE 1: WEB DATA HARVESTING CORE (MONTH 1 ENGINE) ---
        with st.status("🕵️ Crawler Agent: Mapping and deep-reading target ecosystem...", expanded=True) as status:
            scraped_content = run_scraper(company_url, status_box=status)
            status.update(label="✅ Data Gathering Phase Complete!", state="complete")
            
        # Error handling interception for scraping faults
        if "Error reading page" in scraped_content or "Error crawling page" in scraped_content:
            st.error(f"Execution Interrupted: {scraped_content}")
        else:
            # --- PHASE 2: ASYNC TASK SEQUENCING LAYER (MONTH 2 ENGINE) ---
            # Instantiate an isolated message container for real-time stage updates
            status_update_text = st.empty()
            
            def update_status_label(message):
                status_update_text.info(message)
            
            try:
                # Initialize the structural task coordinator pipeline
                pipeline = AccountIntelligencePipeline()
                
                # Execute the sequential multi-agent workforce assembly line
                results = pipeline.execute_full_outreach_sequence(
                    raw_web_data=scraped_content,
                    target_service=offered_service,
                    target_url=company_url,
                    status_callback=update_status_label
                )
                
                # Tear down the informational status block upon successful execution
                status_update_text.empty()
                st.success("🎯 Multi-Agent Campaign Strategy Generated!")
                
                # 🟢 NEW: System Latency Performance Analytics Row
                metrics = results.get("metrics", {})
                st.markdown("### 📊 System Performance Metrics")
                
                # Split display into 5 clean horizontal metric containers
                m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
                m_col1.metric("Total Execution", metrics.get("total_time", "0s"))
                m_col2.metric("Research Lead", metrics.get("research_time", "0s"))
                m_col3.metric("Vector RAG DB", metrics.get("rag_time", "0s"))
                m_col4.metric("Market Strategist", metrics.get("strategist_time", "0s"))
                m_col5.metric("Master Copywriter", metrics.get("copywriter_time", "0s"))
                
                st.markdown("---")
                
                # --- PHASE 3: MULTI-TAB INTELLIGENCE DISPLAY MATRIX ---
                tab1, tab2, tab3 = st.tabs([
                    "✉️ Drafted Outreach Email", 
                    "📊 Strategist Analysis Gaps", 
                    "📋 Research Profile Summary"
                ])
                
                
                # --- PHASE 3: MULTI-TAB INTELLIGENCE DISPLAY MATRIX (JSON COMPATIBLE) ---
            
                
                with tab1:
                    st.subheader("Bespoke Conversion Copy Blueprint")
                    st.caption("Crafted by the Master Copywriter Agent — Fed natively via clean JSON schema structures.")
                    
                    pitch_data = results["final_pitch"]
                    
                    # 🟢 Compile text data inside RAM and attach to an explicit download element
                    campaign_text_content = compile_campaign_txt(pitch_data)
                    
                    st.download_button(
                        label="📥 Download Full Campaign Sequence (.txt)",
                        data=campaign_text_content,
                        file_name="forgereach_outreach_sequence.txt",
                        mime="text/plain",
                        type="secondary"
                    )
                    
                    st.markdown("---")
                    
                    # --- RESTORED: ALL STEPS RENDERED TOGETHER ---
                    st.markdown("### 🔹 Step 1: Cold Email Sequence")
                    st.text_input("Email Subject Line:", value=pitch_data.get("cold_email", {}).get("subject", ""))
                    st.text_area("Email Body Copy:", value=pitch_data.get("cold_email", {}).get("body", ""), height=250)
                    
                    st.markdown("### 🔹 Step 2: LinkedIn Touchpoint")
                    st.text_area("Personalized Connection Note (Under 300 Chars):", value=pitch_data.get("linkedin_note", ""), height=80)
                    
                    st.markdown("### 🔹 Step 3: Value-Add Follow-Up")
                    st.text_input("Follow-Up Subject:", value=pitch_data.get("value_add_follow_up", {}).get("subject", ""))
                    st.text_area("Follow-Up Body Copy:", value=pitch_data.get("value_add_follow_up", {}).get("body", ""), height=200)

                with tab2:
                    st.subheader("Strategic Friction Map Correlation")
                    st.caption("Identified by the Market Strategist Agent — Cross-matching capabilities against target liabilities.")
                    
                    strat_data = results["market_strategy"]
                    
                    st.markdown("### 🔍 Identified Vulnerability Vectors")
                    for point in strat_data.get("friction_points", []):
                        st.info(f"📍 {point}")
                        
                    st.markdown("### 💡 Strategic Fit Breakdown")
                    st.write(strat_data.get("strategic_fit_explanation", ""))
                    
                with tab3:
                    st.subheader("Corporate Structural Knowledge Base Profile")
                    st.caption("Extracted by the Research Lead Agent running at a highly stable Temperature of 0.0.")
                    
                    profile_data = results["company_profile"]
                    
                    st.text_input("Identified Corporate Entity:", value=profile_data.get("company_name", ""))
                    st.text_area("Core Platform Operations:", value=profile_data.get("core_operations", ""), height=100)
                    st.text_input("Target Commercial B2B Demographics:", value=profile_data.get("target_audience", ""))
                    st.text_area("Primary Value Proposition Focus:", value=profile_data.get("commercial_value", ""), height=100)
                    
            except Exception as pipeline_error:
                status_update_text.empty()
                st.error(f"Pipeline Execution Mismatch Error: {str(pipeline_error)}")