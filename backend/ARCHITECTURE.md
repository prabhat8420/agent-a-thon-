# System Architecture - Agentic AI Career Bridge

## Overview

The Agentic AI Career Bridge is a multi-agent system designed to bridge the gap between academic learning and industry expectations for fresh graduates.

## Multi-Agent Architecture

### Agent Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERACTION                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      FASTAPI BACKEND                         │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │              AGENT ORCHESTRATOR                     │    │
│  │                                                     │    │
│  │   ┌───────────────┐    ┌───────────────┐          │    │
│  │   │ Planner Agent │───▶│Executor Agent │──┐       │    │
│  │   └───────────────┘    └───────────────┘  │       │    │
│  │          ▲                                  │       │    │
│  │          │              ┌───────────────┐  │       │    │
│  │          └──────────────│Evaluator Agent◀──┘       │    │
│  │         Feedback Loop   └───────────────┘          │    │
│  │                                                     │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │              BUSINESS LOGIC LAYER                   │    │
│  │                                                     │    │
│  │  • Resume Analyzer                                 │    │
│  │  • Question Generator                              │    │
│  │  • Answer Evaluator                                │    │
│  │  • Roadmap Generator                               │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │                 DATA LAYER                          │    │
│  │                                                     │    │
│  │  • Skills Dataset (CSV)                            │    │
│  │  • Aptitude Questions (JSON)                       │    │
│  │  • Job Roles (JSON)                                │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Agent Details

### 1. Planner Agent (Career Planning Specialist)

**Role**: Resume analysis and skill gap identification

**Inputs**:
- Resume text (raw string)
- Industry skills database

**Processing**:
1. Text parsing and skill extraction
2. Skill matching against industry standards
3. Gap analysis (critical/important/nice-to-have)
4. Resume scoring algorithm
5. Focus area recommendation

**Outputs**:
- Resume score (0-100)
- Detected skills list
- Missing skills categorized
- Recommended focus areas for testing
- Agent status

**Implementation**: `agents/agents.py::create_planner_agent()`

### 2. Executor Agent (Technical Assessment Executor)

**Role**: Test generation and answer evaluation

**Inputs**:
- Skill gaps from Planner
- User answers to questions

**Processing**:
1. Question selection based on gaps
2. Difficulty adjustment
3. Answer validation
4. Performance calculation
5. Category-wise analysis

**Outputs**:
- Aptitude test (5 questions)
- Test ID for session tracking
- Aptitude score (0-100)
- Strengths identified
- Weak areas identified
- Category breakdown

**Implementation**: `agents/agents.py::create_executor_agent()`

### 3. Evaluator Agent (Career Development Evaluator)

**Role**: Roadmap creation and feedback synthesis

**Inputs**:
- Resume analysis from Planner
- Test results from Executor

**Processing**:
1. Holistic assessment synthesis
2. Priority ranking of skills
3. Timeline estimation
4. Resource mapping
5. Career path alignment
6. Feedback generation for Planner

**Outputs**:
- Personalized roadmap (4-6 steps)
- Recommended resources
- Career path suggestions
- Motivational summary
- Feedback to Planner for improvement

**Implementation**: `agents/agents.py::create_evaluator_agent()`

## Workflow Details

### Phase 1: Resume Analysis (Planner)

```
POST /upload_resume
    │
    ├─▶ Validate input (security checks)
    ├─▶ Extract skills using pattern matching
    ├─▶ Compare with 50+ industry skills
    ├─▶ Calculate resume score
    ├─▶ Categorize missing skills
    └─▶ Return analysis + focus areas
```

### Phase 2: Test Generation & Evaluation (Executor)

```
POST /start_aptitude
    │
    ├─▶ Generate test ID (UUID)
    ├─▶ Map focus areas to question categories
    ├─▶ Select questions (5 from pool of 12)
    ├─▶ Store session
    └─▶ Return questions

POST /submit_answers
    │
    ├─▶ Validate test ID and answer count
    ├─▶ Evaluate each answer (correct/incorrect)
    ├─▶ Calculate aptitude score
    ├─▶ Identify strengths/weaknesses by category
    └─▶ Pass to Evaluator
```

### Phase 3: Roadmap Creation (Evaluator)

```
Evaluator receives:
    │
    ├─▶ Resume analysis data
    ├─▶ Aptitude test results
    │
    ├─▶ Synthesize both assessments
    ├─▶ Generate 4-6 step roadmap
    ├─▶ Add timelines and priorities
    ├─▶ Recommend resources
    ├─▶ Suggest career paths
    ├─▶ Create motivational summary
    └─▶ Send feedback to Planner
```

### Phase 4: Feedback Loop

```
Evaluator → Planner:
    │
    ├─▶ Insights on assessment quality
    ├─▶ Suggested improvements for future
    ├─▶ Pattern recognition across candidates
    └─▶ Continuous learning data
```

## Data Models

### Resume Analysis Model
```json
{
  "resume_score": 75,
  "detected_skills": ["Python", "React"],
  "missing_skills": ["Docker", "AWS"],
  "skill_gaps": {
    "critical": ["System Design"],
    "important": ["Kubernetes"],
    "nice_to_have": ["GraphQL"]
  },
  "recommended_focus_areas": ["System Design", "Docker"]
}
```

### Aptitude Question Model
```json
{
  "id": "sd1",
  "question": "Design a URL shortener...",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "correct": 1,
  "category": "system_design",
  "difficulty": "medium"
}
```

### Final Report Model
```json
{
  "aptitude_score": 72,
  "strengths": ["Problem solving", "Algorithms"],
  "weak_areas": ["System Design", "Cloud"],
  "personalized_roadmap": [
    {
      "step": "1",
      "title": "Master System Design",
      "description": "...",
      "duration": "4-6 weeks",
      "priority": "Critical"
    }
  ],
  "recommended_resources": ["Books", "Courses"],
  "career_recommendations": ["Entry-level roles"],
  "evaluator_summary": "...",
  "agent_workflow_status": {...}
}
```

## Security Measures

### Input Validation
- Resume text: 50-10,000 characters
- Prompt injection filters
- Suspicious pattern detection
- Answer count validation

### Rate Limiting (Production)
- Per-IP request limits
- Session-based throttling
- API key rate limits

### Data Sanitization
- HTML/script stripping
- Special character handling
- SQL injection prevention (when using DB)

## Scalability Considerations

### Current (Demo)
- In-memory session storage
- Single server instance
- Mock AI responses for speed

### Production Ready
- Redis for session management
- PostgreSQL for persistent data
- Load balancing across instances
- Caching layer (Redis)
- Message queue for async processing
- Horizontal scaling with Kubernetes

## Technology Stack

### Core
- **FastAPI**: Web framework
- **CrewAI**: Multi-agent orchestration
- **LangChain**: LLM integration
- **Pydantic**: Data validation

### AI/ML
- **OpenAI GPT-4**: Agent reasoning
- **Custom NLP**: Skill extraction

### Data
- **Pandas**: Data processing
- **JSON**: Configuration storage
- **CSV**: Skills database

### Development
- **Uvicorn**: ASGI server
- **Python 3.10+**: Runtime

## Performance Metrics

### Expected Latency
- Resume analysis: 1-2 seconds
- Test generation: 1 second
- Answer evaluation: 2-3 seconds
- Complete workflow: 5-7 seconds

### Throughput
- Current: ~10 requests/second
- Production target: 100+ requests/second with scaling

## Monitoring & Logging

### Logging Levels
```python
INFO  - Workflow progress
ERROR - Failures and exceptions
DEBUG - Detailed agent communication
```

### Key Metrics to Monitor
- Agent execution time
- API response times
- Error rates
- Session counts
- Cache hit rates

## Future Enhancements

### Short-term
- WebSocket for real-time updates
- PDF resume parsing
- Email notifications
- Analytics dashboard

### Long-term
- Video interview analysis
- Peer comparison
- Mentor matching
- Job recommendation engine
- Integration with job boards

## Deployment

### Development
```bash
python main.py
# Runs on localhost:8000
```

### Production
```bash
# Using Docker
docker build -t career-bridge .
docker run -p 8000:8000 career-bridge

# Using systemd
systemctl start career-bridge

# Using Kubernetes
kubectl apply -f k8s/deployment.yaml
```

## Testing Strategy

### Unit Tests
- Agent logic
- Business logic functions
- Data loaders

### Integration Tests
- API endpoints
- Agent workflow
- Database operations

### Load Tests
- Concurrent users
- Response times under load
- Memory usage

## Hackathon Compliance

✅ Minimum 3 autonomous agents (Planner, Executor, Evaluator)
✅ Defined workflow with communication loop
✅ Clear agent responsibilities
✅ Safety-aware actions (input validation, error handling)
✅ Demo-ready API endpoints
✅ Agents communicate in feedback loop
✅ No production auth required (demo mode)
✅ Uses CrewAI for orchestration

---

**Architecture Version**: 1.0.0
**Last Updated**: 2024-01-30
