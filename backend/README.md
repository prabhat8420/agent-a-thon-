# Agentic AI Career Bridge - Backend

Multi-agent system for bridging the academic-industry gap using **CrewAI** and **FastAPI**.

## 🤖 Agent Architecture

### Three Autonomous Agents:

1. **Planner Agent (Career Planning Specialist)**
   - Analyzes resumes
   - Extracts technical skills
   - Compares with industry standards
   - Identifies skill gaps
   - Generates assessment blueprint

2. **Executor Agent (Technical Assessment Executor)**
   - Generates targeted aptitude questions
   - Evaluates candidate responses
   - Calculates performance metrics
   - Identifies strengths and weaknesses

3. **Evaluator Agent (Career Development Evaluator)**
   - Synthesizes all assessment data
   - Creates personalized learning roadmap
   - Recommends resources and career paths
   - Provides feedback loop to Planner

### Workflow:
```
Resume → Planner → Executor → Evaluator → Planner (Feedback Loop)
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip

### Installation

1. **Clone and navigate to backend:**
```bash
cd backend
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key (optional for demo)
```

5. **Run the server:**
```bash
python main.py
```

Server will start at: `http://localhost:8000`

## 📡 API Endpoints

### 1. Upload Resume
**POST** `/upload_resume`

Planner Agent analyzes resume and identifies skill gaps.

**Request:**
```json
{
  "resume_text": "Full Stack Developer with 2 years experience in Python, Django, React..."
}
```

**Response:**
```json
{
  "resume_score": 75,
  "detected_skills": ["Python", "Django", "React", "SQL"],
  "missing_skills": ["System Design", "Docker", "AWS"],
  "skill_gaps": {
    "critical": ["System Design", "Microservices"],
    "important": ["Docker", "Kubernetes"],
    "nice_to_have": ["GraphQL"]
  },
  "recommended_focus_areas": ["System Design", "Docker", "AWS"],
  "agent_status": "Planner Agent: Analysis Complete ✓"
}
```

### 2. Start Aptitude Test
**POST** `/start_aptitude`

Executor Agent generates personalized aptitude test.

**Request:**
```json
{
  "focus_areas": ["System Design", "Data Structures"]
}
```

**Response:**
```json
{
  "test_id": "550e8400-e29b-41d4-a716-446655440000",
  "total_questions": 5,
  "questions": [
    {
      "id": "sd1",
      "question": "You need to design a URL shortening service...",
      "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
      "category": "system_design",
      "difficulty": "medium"
    }
  ],
  "agent_status": "Executor Agent: Test Generated ✓"
}
```

### 3. Submit Answers
**POST** `/submit_answers`

Executor evaluates answers, Evaluator creates roadmap.

**Request:**
```json
{
  "test_id": "550e8400-e29b-41d4-a716-446655440000",
  "answers": [
    {
      "question_id": "sd1",
      "selected_option": 1
    }
  ],
  "resume_analysis": {
    "detected_skills": ["Python", "Django"],
    "missing_skills": {
      "critical": ["System Design"],
      "important": ["Docker"]
    }
  }
}
```

**Response:**
```json
{
  "aptitude_score": 80,
  "strengths": ["Strong problem-solving", "System Design"],
  "weak_areas": ["Data Structures", "Algorithms"],
  "personalized_roadmap": [
    {
      "step": "1",
      "title": "Master System Design Fundamentals",
      "description": "Study scalability, microservices...",
      "duration": "4-6 weeks",
      "priority": "Critical"
    }
  ],
  "recommended_resources": [
    "📚 Designing Data-Intensive Applications",
    "🎓 System Design Interview Course"
  ],
  "career_recommendations": [
    "You're ready for mid-level engineering roles"
  ],
  "evaluator_summary": "Based on your assessment...",
  "agent_workflow_status": {
    "planner": "Complete ✓",
    "executor": "Complete ✓",
    "evaluator": "Complete ✓",
    "feedback_loop": "Active ✓"
  }
}
```

### Other Endpoints

- **GET** `/health` - Health check
- **GET** `/agent_status` - Get agent status
- **DELETE** `/clear_sessions` - Clear test sessions

## 🧪 Testing with cURL

### 1. Upload Resume
```bash
curl -X POST http://localhost:8000/upload_resume \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Software Engineer with expertise in Python, Java, React, and Node.js. Experience with REST APIs, SQL databases, and Git version control. Built multiple full-stack applications."
  }'
```

### 2. Start Aptitude Test
```bash
curl -X POST http://localhost:8000/start_aptitude \
  -H "Content-Type: application/json" \
  -d '["System Design", "Data Structures", "Cloud"]'
```

### 3. Submit Answers
```bash
curl -X POST http://localhost:8000/submit_answers \
  -H "Content-Type: application/json" \
  -d '{
    "test_id": "YOUR_TEST_ID_HERE",
    "answers": [
      {"question_id": "sd1", "selected_option": 1},
      {"question_id": "ds1", "selected_option": 1},
      {"question_id": "dp1", "selected_option": 2},
      {"question_id": "cl1", "selected_option": 2},
      {"question_id": "api1", "selected_option": 2}
    ]
  }'
```

## 📂 Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── agents/
│   ├── agents.py          # Agent definitions (Planner, Executor, Evaluator)
│   ├── tasks.py           # Task definitions for each agent
│   └── crew.py            # CrewAI workflow orchestration
├── models/
│   └── schemas.py         # Pydantic models for requests/responses
├── services/
│   └── assessment_service.py  # Business logic layer
├── utils/
│   └── data_loader.py     # Data loading utilities
└── data/
    ├── skills.csv         # Industry skills dataset
    ├── aptitude.json      # Aptitude questions
    └── roles.json         # Job roles and requirements
```

## 🔒 Security Features

- **Input Validation**: Pydantic models validate all inputs
- **Resume Size Limit**: Max 10,000 characters
- **Prompt Injection Prevention**: Filters suspicious patterns
- **Answer Count Validation**: Ensures answer count matches questions
- **Try-Except Guards**: All endpoints have error handling
- **No Arbitrary Code Execution**: Safe evaluation only

## 🎯 Key Features

### Multi-Agent Workflow
- Agents communicate in sequence
- Feedback loop from Evaluator to Planner
- Workflow status tracking

### Skill Gap Analysis
- Extracts skills from resume text
- Compares against 50+ industry skills
- Categorizes gaps by priority

### Adaptive Testing
- Questions tailored to skill gaps
- Multiple difficulty levels
- Covers 5 categories (System Design, Data Structures, etc.)

### Personalized Roadmap
- Step-by-step learning path
- Estimated timelines
- Resource recommendations
- Career guidance

## 🛠️ Development

### Running in Development Mode
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### API Documentation
Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Adding New Skills
Edit `data/skills.csv` and add rows:
```csv
skill,category,importance,demand_level
TensorFlow,AI/ML,Medium,High
```

### Adding New Questions
Edit `data/aptitude.json` and add to appropriate category:
```json
{
  "system_design": [
    {
      "id": "sd4",
      "question": "Your question here...",
      "options": ["A", "B", "C", "D"],
      "correct": 1,
      "difficulty": "medium",
      "category": "system_design"
    }
  ]
}
```

## 🤝 Integration with Frontend

The backend is designed to work seamlessly with the frontend application.

### CORS Configuration
CORS is enabled for all origins. In production, update:
```python
allow_origins=["http://your-frontend-domain.com"]
```

### API Flow
1. Frontend sends resume text to `/upload_resume`
2. Frontend receives analysis and calls `/start_aptitude`
3. User answers questions in frontend
4. Frontend submits answers to `/submit_answers`
5. Frontend displays final report and roadmap

## 📊 Demo Data

The application includes:
- **50+ industry skills** across categories
- **12 aptitude questions** in 5 categories
- **5 job role templates** with requirements

## 🚧 Future Enhancements

- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] User authentication (JWT)
- [ ] Resume file upload (PDF parsing)
- [ ] Real-time agent communication logs
- [ ] Advanced analytics dashboard
- [ ] Email notifications
- [ ] Integration with LinkedIn/GitHub APIs

## ⚠️ Important Notes

- **OpenAI API Key**: Optional for demo. App works with mock data.
- **Session Storage**: Currently in-memory. Use Redis/DB for production.
- **Rate Limiting**: Not implemented. Add for production deployment.
- **Authentication**: Not implemented. Add for production use.

## 📝 License

Hackathon Demo Project - Free to use and modify.

## 👥 Contributors

Developed for Agentic AI Hackathon demonstrating multi-agent workflow using CrewAI.

---

**Happy Hacking! 🚀**
