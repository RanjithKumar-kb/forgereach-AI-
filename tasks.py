import os
import time
import logging
from urllib.parse import urlparse
import chromadb
from agents import OutreachAgency

# 🟢 Configure standard production-grade logging parameters
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("ForgeReachLogger")

class AccountIntelligencePipeline:
    """Manages the sequential execution contract, RAG retrieval, and performance analytics logging."""
    
    def __init__(self):
        self.agency = OutreachAgency()
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        logger.info("AccountIntelligencePipeline initialized with persistent ChromaDB storage.")

    def query_local_intelligence(self, domain_source: str, query_text: str, n_results: int = 3) -> str:
        """Queries ChromaDB for relevant website fragments and logs vector performance metrics."""
        start_time = time.time()
        try:
            collection = self.chroma_client.get_collection(name="account_intelligence")
            results = collection.query(
                query_texts=[query_text],
                n_results=n_results,
                where={"source": domain_source}
            )
            elapsed_time = time.time() - start_time
            logger.info(f"Vector Space Query completed in {elapsed_time:.3f} seconds for source: {domain_source}")
            
            if results and 'documents' in results and results['documents']:
                return "\n\n=== RETRIEVED HIGH-VALUE CONTEXT ===\n".join(results['documents'][0])
            
            logger.warning(f"No vector records matched for query: '{query_text}' under source: {domain_source}")
            return ""
        except Exception as db_error:
            elapsed_time = time.time() - start_time
            logger.error(f"Vector lookup failed after {elapsed_time:.3f}s: {str(db_error)}")
            return ""

    def execute_full_outreach_sequence(self, raw_web_data: str, target_service: str, target_url: str, status_callback=None) -> dict:
        """Runs the JSON-contract assembly pipeline while capturing telemetry metrics."""
        pipeline_start = time.time()
        domain_source = urlparse(target_url).netloc
        logger.info(f"--- Launching Full Campaign Execution Pipeline for Domain: {domain_source} ---")
        
        # --- TASK 1: Deep Account Research ---
        if status_callback:
            status_callback("🕵️ Research Lead: Extracting data into JSON contract...")
        task_start = time.time()
        research_persona = self.agency.get_research_lead_persona()
        company_profile_dict = self.agency.run_structured_agent(research_persona, raw_web_data, temperature=0.0)
        research_time = time.time() - task_start
        logger.info(f"[Perf Audit] Research Lead execution time: {research_time:.3f} seconds.")
        
        # --- TASK 2: Vertical Data Retrieval Step (RAG) ---
        if status_callback:
            status_callback("💾 Vector Database: Contextual text block identification...")
        rag_start = time.time()
        targeted_db_context = self.query_local_intelligence(
            domain_source=domain_source,
            query_text=f"What are their operational infrastructure challenges related to {target_service}?"
        )
        rag_time = time.time() - rag_start
        
        profile_string = f"Company: {company_profile_dict.get('company_name')}\nOperations: {company_profile_dict.get('core_operations')}"
        vulnerability_context = f"{profile_string}\n\nDB Fragments:\n{targeted_db_context}"

        # --- TASK 3: Strategic Solution Friction Mapping ---
        if status_callback:
            status_callback("📊 Market Strategist: Parsing pain matrices...")
        task_start = time.time()
        strategist_persona = self.agency.get_market_strategist_persona()
        strategy_context = f"Vulnerability Metrics:\n{vulnerability_context}\n\nOur Offering:\n{target_service}"
        market_strategy_dict = self.agency.run_structured_agent(strategist_persona, strategy_context, temperature=0.1)
        strategist_time = time.time() - task_start
        logger.info(f"[Perf Audit] Market Strategist execution time: {strategist_time:.3f} seconds.")
        
        # --- TASK 4: High-Conversion Copy Drafting ---
        if status_callback:
            status_callback("✍️ Master Copywriter: Refining copy blueprints...")
        task_start = time.time()
        copywriter_persona = self.agency.get_copywriter_persona()
        copywriter_context = f"Strategic Blueprint:\n{str(market_strategy_dict)}"
        final_pitch_dict = self.agency.run_structured_agent(copywriter_persona, copywriter_context, temperature=0.7)
        copywriter_time = time.time() - task_start
        logger.info(f"[Perf Audit] Master Copywriter execution time: {copywriter_time:.3f} seconds.")
        
        total_pipeline_time = time.time() - pipeline_start
        logger.info(f"🏁 --- Pipeline Lifecycle Complete. Total Execution Time: {total_pipeline_time:.2f} seconds. ---")
        
        # 🟢 Added metrics payload directly into our return data contract package
        return {
            "company_profile": company_profile_dict,
            "market_strategy": market_strategy_dict,
            "final_pitch": final_pitch_dict,
            "metrics": {
                "research_time": f"{research_time:.2f}s",
                "rag_time": f"{rag_time:.3f}s",
                "strategist_time": f"{strategist_time:.2f}s",
                "copywriter_time": f"{copywriter_time:.2f}s",
                "total_time": f"{total_pipeline_time:.2f}s"
            }
        }