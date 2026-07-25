# LangGraph Support Agent

A production-grade customer support triage and resolution system built with LangGraph. The agent classifies customer intent, gathers relevant information using tools, attempts to resolve the issue, and escalates to human agents when needed.

## What This System Does

A customer sends a support message. The agent follows a structured workflow:

1. **Classifies** the customer's intent
2. **Gathers** relevant information using tools
3. **Attempts** to resolve the issue
4. **Evaluates** whether the issue was resolved
5. **Escalates** to a human agent when the issue cannot be resolved

The workflow is implemented as a LangGraph state machine, allowing each step to update and pass state to the next node.

## Architecture

```text
Customer Message
      │
      ▼
┌──────────────┐
│   CLASSIFY   │  ← LLM determines customer intent
│    INTENT    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│    GATHER    │  ← Calls tools based on intent
│ INFORMATION  │
└──────┬───────┘
       │
       ├── Payment history
       ├── Refund policy
       ├── Knowledge base
       ├── Account verification
       └── Order status
       │
       ▼
┌──────────────┐
│   ATTEMPT    │  ← LLM generates a resolution
│  RESOLUTION  │
└──────┬───────┘
       │
       ▼
  ┌────┴─────┐
  │ RESOLVED?│
  └────┬─────┘
       │
  ┌────┴────┐
  ▼         ▼
┌──────┐ ┌──────────┐
│SOLVED│ │ ESCALATE │  ← Human handoff
│ END  │ │  HUMAN   │
└──────┘ └──────────┘
```

## Intent Categories

| Intent    | Example Messages                             | Tools Used                           |
| --------- | -------------------------------------------- | ------------------------------------ |
| Billing   | "I was charged twice", "Where is my refund?" | Payment history, Refund policy       |
| Technical | "App keeps crashing", "How do I export?"     | Knowledge base search                |
| Account   | "Can't login", "Password reset"              | Account verification, Knowledge base |
| General   | "Business hours?", "Contact info?"           | Knowledge base search                |

## Tech Stack

| Component           | Technology                                     |
| ------------------- | ---------------------------------------------- |
| Agent Orchestration | LangGraph                                      |
| LLM                 | Groq (Llama 3.1 8B) — free tier                |
| Embeddings          | HuggingFace (`all-MiniLM-L6-v2`) — free, local |
| Vector Store        | ChromaDB                                       |
| API Framework       | FastAPI                                        |
| Language            | Python 3.12                                    |

## Project Structure

```text
langgraph-support-agent/
├── app/
│   ├── main.py               # FastAPI entry point
│   ├── config.py             # Settings from .env
│   ├── agent/
│   │   ├── graph.py          # LangGraph graph definition
│   │   ├── state.py          # State schema (TypedDict)
│   │   └── nodes.py          # Graph node functions
│   ├── tools/
│   │   ├── knowledge_base.py # Chroma vector search
│   │   ├── payments.py       # Mock payment history
│   │   ├── refunds.py        # Refund policy rules
│   │   ├── accounts.py       # Mock account verification
│   │   └── orders.py         # Mock order status
│   └── models/
│       └── schemas.py        # Pydantic API models
├── data/
│   └── knowledge_base.txt    # Sample FAQ / product documentation
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variable template
├── .gitignore
└── README.md
```

## Getting Started

### 1. Prerequisites

Make sure you have:

* Python 3.12+
* A free Groq API key from [console.groq.com](https://console.groq.com)

### 2. Clone and Setup

Clone the repository and create a Python virtual environment:

```bash
git clone https://github.com/rvchandrudev/langgraph-support-agent.git
cd langgraph-support-agent

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure Environment

Create the environment configuration file:

```bash
cp .env.example .env
```

Edit `.env` and add your Groq API key:

```env
GROQ_API_KEY=gsk_your_key_here
```

> **Security Note:** Never commit your actual API key to Git. Keep your `.env` file local and make sure it is included in `.gitignore`.

### 4. Run the Server

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8002
```

### 5. Open the API Documentation

Visit:

```text
http://localhost:8002/docs
```

This opens the interactive Swagger API documentation where you can test the support agent.

## Test the Agent

### Billing Issue

```bash
curl -X POST http://localhost:8002/ticket \
  -H "Content-Type: application/json" \
  -d '{"customer_message": "I was charged twice for my subscription", "customer_id": "cust_123"}'
```

### Technical Issue

```bash
curl -X POST http://localhost:8002/ticket \
  -H "Content-Type: application/json" \
  -d '{"customer_message": "The app keeps crashing when I try to export my data"}'
```

### Account Issue

```bash
curl -X POST http://localhost:8002/ticket \
  -H "Content-Type: application/json" \
  -d '{"customer_message": "I forgot my password and cannot login", "customer_id": "cust_789"}'
```

## API Endpoints

### Health Check

```http
GET /health
```

Returns a simple response confirming that the API is running.

### Create Support Ticket

```http
POST /ticket
```

Creates a support ticket and runs the customer request through the LangGraph workflow.

**Request:**

```json
{
  "customer_message": "I was charged twice for my subscription",
  "customer_id": "cust_123"
}
```

**Example Response:**

```json
{
  "ticket_id": "TKT-E73EDCD0",
  "intent": "billing",
  "confidence": 1.0,
  "resolution": "Thank you for reaching out...",
  "status": "resolved",
  "escalated": false,
  "gathered_info": {
    "payment_history": {},
    "refund_policy": {}
  }
}
```

The response contains the classification result, generated resolution, final status, escalation state, and information gathered by the agent during execution.

## Example Execution

For example, a customer may report:

```text
The app keeps crashing when I try to export my data.
```

The agent can classify this as a **technical** issue and search the knowledge base for relevant information.

The retrieved context may contain articles related to:

* Application crashes
* Data export functionality
* Account issues
* Contacting support

The LLM then uses the retrieved information to generate a troubleshooting response.

If the available information is sufficient and the issue can be resolved, the ticket is marked as:

```text
status: resolved
escalated: false
```

If the agent determines that it cannot confidently resolve the issue, the workflow routes the ticket to human escalation with the gathered context.

## Key Concepts Demonstrated

| Concept                 | Implementation                                                           |
| ----------------------- | ------------------------------------------------------------------------ |
| **State Management**    | A `TypedDict` state flows through all graph nodes                        |
| **Graph Orchestration** | LangGraph connects classification, gathering, resolution, and escalation |
| **Conditional Routing** | Resolved requests end the workflow; unresolved requests are escalated    |
| **Tool Orchestration**  | Different tools are called based on customer intent                      |
| **LLM Decision Making** | LLM performs intent classification and generates resolutions             |
| **Vector Retrieval**    | ChromaDB retrieves relevant knowledge base content                       |
| **Human-in-the-Loop**   | Unresolved issues can be handed off to human agents                      |
| **Fallback Handling**   | JSON parsing and resolution-status fallbacks improve robustness          |
| **Context Passing**     | Gathered information is maintained throughout the workflow               |

## LangGraph Workflow

The workflow can be represented as:

```text
START
  │
  ▼
CLASSIFY INTENT
  │
  ▼
GATHER INFORMATION
  │
  ▼
ATTEMPT RESOLUTION
  │
  ▼
CHECK RESOLUTION
  │
  ├───────────────┐
  │               │
  ▼               ▼
RESOLVED       UNRESOLVED
  │               │
  ▼               ▼
 END           ESCALATE
                  │
                  ▼
                 END
```

The key advantage of this architecture is that the workflow is explicit. Each node has a specific responsibility, and conditional edges determine what happens next.

## Tool Selection by Intent

The agent selects tools based on the classified intent.

### Billing

The agent may retrieve:

* Payment history
* Refund policy
* Order information

### Technical

The agent may search:

* Product documentation
* Troubleshooting guides
* Knowledge base articles

### Account

The agent may use:

* Account verification
* Knowledge base search
* Password recovery information

### General

The agent may search:

* Frequently asked questions
* Business information
* Contact information
* General product documentation

## LangGraph vs Regular LangChain

| Feature       | LangChain                         | LangGraph (This Project)          |
| ------------- | --------------------------------- | --------------------------------- |
| Flow          | Linear chains and pipelines       | Graph-based workflow              |
| Branching     | Limited / manually implemented    | Conditional edges                 |
| Loops         | Not a core workflow primitive     | Supported through graph edges     |
| State         | Often passed between components   | Explicit shared state             |
| Tool Usage    | Tool calling and agents           | Tools integrated into graph nodes |
| Human Handoff | Requires additional orchestration | Natural graph routing             |
| Best For      | RAG and simpler LLM applications  | Agents and complex workflows      |

### Why LangGraph?

A simple RAG application generally follows a predictable sequence:

```text
Question → Retrieve → Generate → Answer
```

A support agent requires more complex decision-making:

```text
Question
   │
   ▼
Classify
   │
   ▼
Choose Tools
   │
   ▼
Gather Information
   │
   ▼
Attempt Resolution
   │
   ├── Resolved ──────→ END
   │
   └── Unresolved ────→ Human Escalation
```

LangGraph is useful here because the workflow contains explicit state, conditional routing, and the possibility of additional processing or human intervention.

## Limitations

The current implementation is a learning-focused support agent and uses mock integrations for external systems.

* Payment history is mocked
* Account verification is mocked
* Order status is mocked
* Refund policy is implemented as local rules
* No authentication or authorization
* No persistent ticket database
* No real payment gateway integration
* No real CRM or helpdesk integration
* No streaming responses
* No conversation memory
* No production-grade human agent dashboard

These limitations keep the project focused on demonstrating agent orchestration and workflow design.

## Future Improvements

Potential improvements include:

* Replace mock tools with real service integrations
* Add PostgreSQL for persistent ticket storage
* Add authentication and authorization
* Add real CRM/helpdesk integration
* Add a human-agent dashboard
* Add conversation memory
* Add multi-turn conversations
* Add streaming responses
* Add ticket priority classification
* Add SLA tracking
* Add retry and error recovery nodes
* Add observability and tracing
* Add automated evaluation
* Add unit and integration tests
* Add Docker support

## Related Projects

* **rag-document-search-streamlit:** RAG document search application with a Streamlit UI.
* **rag-api-service:** RAG API implemented manually with FastAPI, PostgreSQL, and pgvector.
* **langchain-rag-api-service:** RAG API rebuilt using LangChain.

## License

This project is licensed under the MIT License.
