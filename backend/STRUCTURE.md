# Project Structure

```
backend/
│
├── main.py                          # FastAPI application entry point
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variables template
├── .gitignore                       # Git ignore rules
├── Dockerfile                       # Docker container configuration
├── docker-compose.yml               # Docker compose for easy deployment
├── run.sh                           # Quick start script
├── test_api.py                      # API test examples
│
├── README.md                        # Project documentation
├── ARCHITECTURE.md                  # System architecture details
├── DEMO_GUIDE.md                    # Hackathon demo guide
│
├── agents/                          # Multi-agent system
│   ├── __init__.py
│   ├── agents.py                    # Agent definitions (Planner, Executor, Evaluator)
│   ├── tasks.py                     # Task definitions for each agent
│   └── crew.py                      # CrewAI workflow orchestration
│
├── models/                          # Pydantic data models
│   ├── __init__.py
│   └── schemas.py                   # Request/response schemas
│
├── services/                        # Business logic layer
│   ├── __init__.py
│   └── assessment_service.py        # Core assessment logic
│
├── utils/                           # Utility modules
│   ├── __init__.py
│   └── data_loader.py              # Data loading utilities
│
└── data/                            # Datasets
    ├── skills.csv                   # 50+ industry skills
    ├── aptitude.json                # 12 aptitude questions
    └── roles.json                   # Job roles and requirements
```

## Key Files

### Core Application
- **main.py**: FastAPI app with all API endpoints
- **requirements.txt**: All Python dependencies including CrewAI

### Multi-Agent System
- **agents/agents.py**: Defines the 3 autonomous agents
- **agents/tasks.py**: Tasks for each agent to execute
- **agents/crew.py**: Orchestrates the agent workflow

### Business Logic
- **services/assessment_service.py**: 
  - ResumeAnalyzer: Skill extraction and scoring
  - QuestionGenerator: Adaptive test generation
  - AnswerEvaluator: Performance evaluation
  - RoadmapGenerator: Personalized roadmap creation

### Data Models
- **models/schemas.py**: Pydantic models for API validation

### Data
- **data/skills.csv**: Industry skills database
- **data/aptitude.json**: Question bank
- **data/roles.json**: Job role requirements

### Documentation
- **README.md**: Complete setup and API guide
- **ARCHITECTURE.md**: System design and architecture
- **DEMO_GUIDE.md**: Hackathon demo script

### Deployment
- **Dockerfile**: Container image definition
- **docker-compose.yml**: One-command deployment
- **run.sh**: Local development startup script
