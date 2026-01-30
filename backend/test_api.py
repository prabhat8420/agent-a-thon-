"""
Example test script to demonstrate API usage
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_complete_workflow():
    """Test the complete assessment workflow"""
    
    print("=" * 60)
    print("AGENTIC AI CAREER BRIDGE - API TEST")
    print("=" * 60)
    
    # Test 1: Upload Resume
    print("\n1. Testing Resume Upload (Planner Agent)...")
    resume_data = {
        "resume_text": """
        Full Stack Software Engineer
        
        Skills: Python, Django, JavaScript, React, Node.js, PostgreSQL, 
        Git, REST APIs, HTML, CSS, jQuery, Express.js
        
        Experience:
        - Built e-commerce platform using Django and React
        - Implemented RESTful APIs for mobile applications
        - Worked with PostgreSQL databases and optimization
        - Collaborated using Git and Agile methodologies
        
        Education: B.Tech in Computer Science
        """
    }
    
    try:
        response = requests.post(f"{BASE_URL}/upload_resume", json=resume_data)
        response.raise_for_status()
        resume_result = response.json()
        
        print(f"✓ Resume Score: {resume_result['resume_score']}/100")
        print(f"✓ Detected Skills: {', '.join(resume_result['detected_skills'][:5])}")
        print(f"✓ Missing Skills: {', '.join(resume_result['missing_skills'][:5])}")
        print(f"✓ {resume_result['agent_status']}")
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Resume upload failed: {e}")
        return
    
    # Test 2: Start Aptitude Test
    print("\n2. Testing Aptitude Test Generation (Executor Agent)...")
    
    focus_areas = resume_result.get('recommended_focus_areas', 
                                    ['System Design', 'Data Structures'])
    
    try:
        response = requests.post(f"{BASE_URL}/start_aptitude", json=focus_areas)
        response.raise_for_status()
        test_result = response.json()
        
        test_id = test_result['test_id']
        questions = test_result['questions']
        
        print(f"✓ Test ID: {test_id}")
        print(f"✓ Questions Generated: {test_result['total_questions']}")
        print(f"✓ {test_result['agent_status']}")
        
        # Display first question
        if questions:
            q1 = questions[0]
            print(f"\nSample Question:")
            print(f"Q: {q1['question'][:100]}...")
            print(f"Category: {q1['category']}, Difficulty: {q1['difficulty']}")
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Test generation failed: {e}")
        return
    
    # Test 3: Submit Answers
    print("\n3. Testing Answer Submission (Executor + Evaluator Agents)...")
    
    # Simulate answers (selecting option 1 for all questions for demo)
    answers_data = {
        "test_id": test_id,
        "answers": [
            {
                "question_id": q['id'],
                "selected_option": 1  # Demo: selecting second option
            }
            for q in questions
        ],
        "resume_analysis": {
            "detected_skills": resume_result['detected_skills'],
            "missing_skills": resume_result['skill_gaps']
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/submit_answers", json=answers_data)
        response.raise_for_status()
        final_result = response.json()
        
        print(f"✓ Aptitude Score: {final_result['aptitude_score']}/100")
        print(f"✓ Strengths: {', '.join(final_result['strengths'][:3])}")
        print(f"✓ Weak Areas: {', '.join(final_result['weak_areas'][:3])}")
        
        print("\nPersonalized Roadmap:")
        for step in final_result['personalized_roadmap'][:3]:
            print(f"  {step['step']}. {step['title']} ({step['duration']})")
        
        print("\nAgent Workflow Status:")
        for agent, status in final_result['agent_workflow_status'].items():
            print(f"  {agent.capitalize()}: {status}")
        
        print(f"\n{final_result['evaluator_summary'][:200]}...")
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Answer submission failed: {e}")
        return
    
    print("\n" + "=" * 60)
    print("✓ COMPLETE WORKFLOW TEST PASSED")
    print("=" * 60)


def test_health_check():
    """Test health endpoint"""
    print("\nTesting Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        response.raise_for_status()
        health = response.json()
        print(f"✓ Status: {health['status']}")
        print(f"✓ Agents Loaded: {health['agents_loaded']}")
        print(f"✓ Data Loaded: {health['data_loaded']}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Health check failed: {e}")


def test_agent_status():
    """Test agent status endpoint"""
    print("\nTesting Agent Status...")
    try:
        response = requests.get(f"{BASE_URL}/agent_status")
        response.raise_for_status()
        status = response.json()
        print(f"✓ Workflow: {status['workflow']}")
        print(f"✓ Active Sessions: {status['active_sessions']}")
        for name, agent in status['agents'].items():
            print(f"  - {agent['name']}: {agent['status']}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Agent status check failed: {e}")


if __name__ == "__main__":
    print("\n🚀 Starting API Tests...")
    print("Make sure the server is running at http://localhost:8000\n")
    
    # Run tests
    test_health_check()
    test_agent_status()
    test_complete_workflow()
    
    print("\n✅ All tests completed!\n")
