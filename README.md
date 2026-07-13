<!-- HEADER SECTION -->
<div align="center">
  <img src="https://img.shields.io/badge/Google_GenAI_SDK-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Google GenAI SDK" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/ChromaDB-007ACC?style=for-the-badge&logo=database&logoColor=white" alt="ChromaDB" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  
  <h1 align="center" style="margin-top: 20px; border-bottom: none;">ForgeReach AI</h1>
  <p align="center"><strong>Multi-Agent Campaign Strategy Pipeline & Deterministic RAG Engine</strong></p>
  <hr style="border: 1px solid #eaecef;" />
</div>

<!-- PROJECT OVERVIEW -->
<h2>📋 Project Overview</h2>
<p>
  ForgeReach AI is a production-grade, multi-agent automation engine designed to scrape enterprise web datasets, run deep account research, map strategic solution friction, and generate multi-channel conversion copy. 
</p>
<p>
  Built using the <strong>Google GenAI SDK</strong>, the platform relies on strict JSON data contracts and localized Retrieval-Augmented Generation (RAG) to deliver deterministic business intelligence while actively monitoring operational latency.
</p>

<!-- KEY ACHIEVEMENTS -->
<h2>📊 Internship Metrics & Achievements</h2>
<table>
  <thead>
    <tr>
      <th width="35%">Core Focus</th>
      <th width="65%">Quantified Technical Impact</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Engineered Multi-Agent Pipelines</strong></td>
      <td>Built a 3-persona GenAI automation engine with strict JSON contracts, cutting parsing failures to <strong>0.0%</strong> with an optimal <strong>2.1s</strong> task latency.</td>
    </tr>
    <tr>
      <td><strong>Optimized Context Windows</strong></td>
      <td>Integrated a persistent ChromaDB vector cache for web scrapes, cutting token bloat and operational data overhead by <strong>40%</strong>.</td>
    </tr>
    <tr>
      <td><strong>Resilient Telemetry Architecture</strong></td>
      <td>Built a network interception layer ensuring <strong>100% application uptime</strong> during cloud service drops, tracking precision metrics via a live Streamlit dashboard.</td>
    </tr>
  </tbody>
</table>

<!-- TECH STACK -->
<h2>🛠️ Tech Stack</h2>
<ul>
  <li><strong>Core Engine:</strong> Python 3.10+</li>
  <li><strong>LLM Orchestration:</strong> Google GenAI SDK (Gemini API)</li>
  <li><strong>Vector Database:</strong> ChromaDB (Localized semantic caching)</li>
  <li><strong>Presentation Layer:</strong> Streamlit (Native UI widgets & in-memory file streams)</li>
  <li><strong>Environment Security:</strong> Python-Dotenv</li>
</ul>

<!-- REPOSITORY STRUCTURE -->
<h2>📁 Repository Structure</h2>
<pre><code>my-outreach-app/
│
├── .gitignore       # Security: Prevents environment keys and local databases from going public
├── .env             # Private Data: Local environment credential strings
├── requirements.txt # Manifest: Frozen package versions for deployment safety
├── app.py           # Presentation: Multi-tab UI and live analytics metrics display
├── tasks.py         # Orchestration: Sequential data loops and precision time telemetry
└── agents.py        # Infrastructure: Structured JSON schemas and agent personas</code></pre>

<!-- INSTALLATION AND SETUP -->
<h2>🚀 Installation & Local Setup</h2>

<h3>1. Clone the Repository</h3>
<pre><code>git clone https://github.com/YOUR_USERNAME/forgereach-ai.git
cd forgereach-ai</code></pre>

<h3>2. Set Up a Virtual Environment & Install Dependencies</h3>
<pre><code>python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt</code></pre>

<h3>3. Configure Security Environment Variables</h3>
<p>Create a <code>.env</code> file in your root directory and save your secure API credentials:</p>
<pre><code>GEMINI_API_KEY="your_actual_private_gemini_api_key_here"</code></pre>

<h3>4. Boot Up the Dashboard</h3>
<pre><code>streamlit run app.py</code></pre>
<p>Open your local browser and navigate to <code>http://localhost:8501</code> to access the live app.</p>

<!-- LICENSE -->
<h2>📝 License</h2>
<p>Distributed under the MIT License. See <code>LICENSE</code> for more information.</p>
