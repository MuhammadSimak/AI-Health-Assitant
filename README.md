AI-Agents-for-Medical-Diagnostics
image
A Python project that creates specialized LLM-based AI agents to analyze complex medical cases.
The system integrates insights from different medical specialists to provide comprehensive assessments
and suggested treatment directions, demonstrating the potential of AI in multidisciplinary medicine.

⚠️ Disclaimer: This project is for research and educational purposes only.
It is not intended for clinical use.

Upgraded core LLM to GPT-5
🚀 How It Works
In the current version, we use three AI agents (GPT-5), each specializing in a different aspect of medical analysis.
A medical report is passed to all agents, which run in parallel (threading) and return their findings.
The outputs are then combined and summarized into three possible health issues with reasoning.

### AI Agents

**1. Cardiologist Agent**  
- *Focus*: Detect cardiac issues such as arrhythmias or structural abnormalities.  
- *Recommendations*: Cardiovascular testing, monitoring, and management strategies.  

**2. Psychologist Agent**  
- *Focus*: Identify psychological conditions (e.g., panic disorder, anxiety).  
- *Recommendations*: Therapy, stress management, or medication adjustments.  

**3. Pulmonologist Agent**  
- *Focus*: Assess respiratory causes for symptoms (e.g., asthma, breathing disorders).  
- *Recommendations*: Lung function tests, breathing exercises, respiratory treatments.  
