# Demo Guide - Agentic AI Career Bridge

## Quick Demo (5 minutes)

### Prerequisites
1. Server running at `http://localhost:8000`
2. Terminal or API client (Postman/curl)

### Demo Script

#### Step 1: Health Check (15 seconds)
```bash
curl http://localhost:8000/health
```

**Expected**: Status "healthy", agents loaded ✓

#### Step 2: Upload Resume (30 seconds)
```bash
curl -X POST http://localhost:8000/upload_resume \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Software Engineer with 3 years experience. Skills: Python, Django, React, PostgreSQL, Git, REST APIs. Built multiple web applications. Strong problem-solving skills."
  }'
```

**Show**:
- Resume score (typically 65-85)
- Detected skills (Python, Django, React, etc.)
- Missing critical skills (System Design, Docker, AWS)
- Agent status: "Planner Agent: Analysis Complete ✓"

**Highlight**: "The Planner Agent analyzed the resume and identified skill gaps"

#### Step 3: Start Aptitude Test (30 seconds)
```bash
curl -X POST http://localhost:8000/start_aptitude \
  -H "Content-Type: application/json" \
  -d '["System Design", "Data Structures", "Cloud"]'
```

**Show**:
- Test ID generated
- 5 industry-level questions
- Categories: System Design, Data Structures, Cloud
- Agent status: "Executor Agent: Test Generated ✓"

**Highlight**: "The Executor Agent created a personalized test based on skill gaps"

**Save the test_id from response for next step!**

#### Step 4: Submit Answers (1 minute)
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

**Show**:
- Aptitude score (calculated based on correct answers)
- Strengths identified
- Weak areas highlighted
- **Personalized Roadmap** (4-6 steps)
- Recommended resources
- Career recommendations
- Agent workflow status showing all three agents complete

**Highlight**: 
1. "Executor Agent evaluated the answers"
2. "Evaluator Agent created a personalized roadmap"
3. "All three agents worked together in sequence"

#### Step 5: Check Agent Status (15 seconds)
```bash
curl http://localhost:8000/agent_status
```

**Show**:
- All three agents ready
- Complete workflow: Planner → Executor → Evaluator
- Active sessions count

## Key Demo Points

### 1. Multi-Agent Workflow
**Say**: "This system uses three autonomous AI agents:"
- **Planner**: Analyzes resume, identifies gaps
- **Executor**: Generates test, evaluates answers
- **Evaluator**: Creates personalized roadmap

### 2. Agent Communication
**Say**: "The agents communicate in a workflow:"
```
Resume → Planner → Executor → Evaluator → Planner (feedback)
```

### 3. Personalization
**Say**: "Each assessment is personalized based on:"
- Individual skill gaps
- Test performance
- Career goals

### 4. Industry Alignment
**Say**: "System uses real industry data:"
- 50+ industry skills
- Multiple question categories
- Job role requirements

## Visual Demo Flow

```
┌─────────────────┐
│  Upload Resume  │ ◄── Planner Agent analyzes
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Get Analysis   │ ◄── Shows skill gaps
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Start Test     │ ◄── Executor Agent generates
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Submit Answers  │ ◄── Executor evaluates
└────────┬────────┘         Evaluator synthesizes
         │
         ▼
┌─────────────────┐
│ Get Roadmap     │ ◄── Personalized learning path
└─────────────────┘
```

## Common Questions & Answers

**Q**: How does this bridge the academic-industry gap?
**A**: It identifies exactly what skills students learn vs what industry needs, then provides a personalized roadmap to fill those gaps.

**Q**: What makes this "agentic"?
**A**: Three autonomous AI agents work together - Planner analyzes, Executor tests, Evaluator synthesizes - each with specific roles and goals.

**Q**: How is this different from regular assessment tools?
**A**: Multi-agent collaboration, feedback loop for continuous improvement, and personalized roadmaps instead of just scores.

**Q**: Can it handle different career paths?
**A**: Yes, it analyzes skills against multiple job roles and recommends paths based on current skills and interests.

## Hackathon Judging Points

✅ **Innovation**: Multi-agent AI system for career development
✅ **Technical Complexity**: CrewAI, FastAPI, 3 autonomous agents
✅ **Practical Impact**: Solves real problem for fresh graduates
✅ **Agent Autonomy**: Each agent makes independent decisions
✅ **Workflow Design**: Clear sequential + feedback loop pattern
✅ **Scalability**: Modular design, API-first architecture
✅ **Safety**: Input validation, error handling, rate limiting ready

## Sample Output Highlights

### Resume Analysis
```json
{
  "resume_score": 75,
  "detected_skills": ["Python", "Django", "React"],
  "missing_skills": ["System Design", "Docker", "Kubernetes"],
  "agent_status": "Planner Agent: Analysis Complete ✓"
}
```

### Personalized Roadmap
```json
{
  "roadmap": [
    {
      "step": "1",
      "title": "Master System Design Fundamentals",
      "duration": "4-6 weeks",
      "priority": "Critical"
    },
    {
      "step": "2", 
      "title": "Learn Cloud Technologies",
      "duration": "6-8 weeks",
      "priority": "High"
    }
  ]
}
```

## Extended Demo (10 minutes)

### Show Different Scenarios

1. **Low-Score Candidate**
   - Resume with few skills
   - Gets comprehensive roadmap
   - More foundational focus

2. **High-Score Candidate**
   - Resume with many skills
   - Gets advanced roadmap
   - Focus on specialization

3. **Different Career Paths**
   - Frontend focus
   - Backend focus
   - Full-stack path

## Presentation Tips

1. **Start with the problem**: "Fresh graduates don't know what industry needs"
2. **Show the solution**: "Three AI agents work together to assess and guide"
3. **Live demo**: Execute the API calls in real-time
4. **Highlight innovation**: "Multi-agent system with feedback loop"
5. **Show impact**: "Personalized, actionable roadmap for career readiness"

## Troubleshooting

**Server not starting?**
```bash
python main.py
# Check port 8000 is free
```

**API errors?**
- Check request format
- Verify JSON syntax
- Ensure test_id is correct

**No questions generated?**
- Check data/aptitude.json exists
- Verify focus_areas are valid

---

**Ready to Demo! 🚀**
