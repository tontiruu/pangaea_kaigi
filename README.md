# Pangaea Kaigi

## **Alignment with Y Combinator RFS**

Our "LLM Meeting Agent" is a B2B SaaS that directly addresses multiple RFS themes Y Combinator is seeking.

### **1. Infrastructure for Multi-Agent Systems**

Our service is a multi-agent infrastructure specifically designed for "strategic decision-making." The Facilitator Agent handles "monitoring" and "dynamic prompt generation," while our proprietary consensus-building algorithm guides the AI agent fleet's output toward "reliable" conclusions.

### **2. Automating Complex, Legacy Workflows**

We target the most complex, person-dependent, and legacy workflow in any company: "executive decision-making." Through AI-driven MECE (Mutually Exclusive, Collectively Exhaustive) issue generation and high-speed debate, we replace traditional "intuition and experience"-based processes with an AI-native workflow.

### **3. AI for Governance, Compliance & Audit**

The "black box" nature of AI is a key governance challenge. Our service "logs the entire discussion process" leading to a decision. This makes the thought process of both AI (and humans) fully "auditable," fulfilling a high level of "accountability" to stakeholders, shareholders, and auditors.

---

## Setup

### Prerequisites

- Node.js (v18 or higher)
- Python 3.8+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the backend directory with the following:
```
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

4. Start the backend server:
```bash
python main.py
```

The backend will run on `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will run on `http://localhost:3000`

---

## Demo Instructions

1. **Access the Application**: Open your browser and navigate to `http://localhost:3000`

2. **Configure Context Sources** (Optional):
   - Click the "Context Sources" button to open the MCP configuration panel
   - Currently supports mock data integration
   - Future versions will support Slack, Notion, and other enterprise knowledge sources via Dedaluslabs.ai

3. **Start a Discussion**:
   - Enter your discussion topic or question in the chat input
   - The system will automatically generate relevant issues using MECE (Mutually Exclusive, Collectively Exhaustive) framework
   - AI agents will engage in structured debate to explore different perspectives

4. **Monitor the Discussion**:
   - Watch as multiple AI agents (Strategist, Analyst, Devil's Advocate, etc.) contribute their viewpoints
   - The Facilitator Agent guides the discussion and ensures balanced coverage
   - View retrieved context from your configured sources in the Context Panel

5. **Review Results**:
   - The discussion will converge toward a consensus-based conclusion
   - All discussion logs are preserved for auditability and governance purposes

---

## Future Roadmap

### Phase 1: Enhanced Context Integration (In Progress)
- **Complete MCP Implementation**: Currently, the integration with Slack, Notion, and other enterprise tools via Dedaluslabs.ai is using mock data
- **Unified Knowledge Management**: Implement centralized management of multiple MCP sources through Dedaluslabs.ai
- **Real-time Context Retrieval**: Enable dynamic fetching of relevant company knowledge during discussions

### Phase 2: Advanced Discussion Quality
- **Context-Aware Debates**: Leverage internal company knowledge to generate more informed and relevant arguments
- **Historical Decision Mining**: Use past decisions and their outcomes to improve current recommendations
- **Custom Domain Adaptation**: Train on company-specific terminology and decision patterns

### Phase 3: Enterprise Features
- **Role-Based Access Control**: Secure access to sensitive discussions and context
- **Integration APIs**: Connect with existing enterprise workflows and tools
- **Advanced Analytics**: Provide insights into decision-making patterns and quality metrics

### Phase 4: Scale & Optimization
- **Multi-language Support**: Enable discussions in multiple languages for global teams
- **Performance Optimization**: Handle larger-scale discussions with more agents and context
- **Customizable Agent Personas**: Allow organizations to define their own agent roles and behaviors

Our primary goal is to complete the MCP integration, enabling the system to access comprehensive internal company knowledge and facilitate higher-quality strategic discussions informed by real organizational context.
