// Application State
let appState = {
    resumeScore: 0,
    detectedSkills: [],
    missingSkills: [],
    aptitudeScore: 0,
    answers: {},
    fileName: ''
};

// Questions Data
const questions = [
    {
        id: 1,
        question: "You need to design a URL shortening service like bit.ly. Which database would be most suitable for storing billions of short URLs with high read/write throughput?",
        options: [
            "MySQL with a single master instance",
            "NoSQL database like Cassandra or DynamoDB with partitioning",
            "SQLite for simplicity",
            "In-memory cache only (Redis)"
        ],
        correct: 1
    },
    {
        id: 2,
        question: "What is the time complexity of searching for an element in a balanced Binary Search Tree?",
        options: [
            "O(n)",
            "O(log n)",
            "O(n log n)",
            "O(1)"
        ],
        correct: 1
    },
    {
        id: 3,
        question: "In a microservices architecture, how would you handle distributed transactions across multiple services?",
        options: [
            "Use two-phase commit across all services",
            "Implement saga pattern with compensating transactions",
            "Use a single database for all services",
            "Avoid transactions altogether"
        ],
        correct: 1
    },
    {
        id: 4,
        question: "Which design pattern is most appropriate for creating objects when the exact types are determined at runtime?",
        options: [
            "Singleton Pattern",
            "Observer Pattern",
            "Factory Pattern",
            "Decorator Pattern"
        ],
        correct: 2
    },
    {
        id: 5,
        question: "What is the primary advantage of using Docker containers in a production environment?",
        options: [
            "Better performance than native applications",
            "Eliminates the need for testing",
            "Ensures consistency across development and production environments",
            "Automatically scales applications"
        ],
        correct: 2
    }
];

// Sample skill sets
const skillSets = {
    python: {
        detected: ['Python', 'Data Structures', 'Algorithms', 'Django'],
        missing: ['System Design', 'Docker', 'AWS', 'Microservices']
    },
    java: {
        detected: ['Java', 'Spring Boot', 'OOP', 'SQL'],
        missing: ['Cloud Technologies', 'DevOps', 'React', 'API Design']
    },
    javascript: {
        detected: ['JavaScript', 'React', 'Node.js', 'HTML/CSS'],
        missing: ['System Design', 'Testing', 'TypeScript', 'Security']
    },
    default: {
        detected: ['Python', 'Java', 'Data Structures', 'Algorithms'],
        missing: ['System Design', 'Real-world Projects', 'Communication', 'Cloud Technologies']
    }
};

// Navigation Functions
function navigateTo(pageId) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });
    
    // Show target page
    document.getElementById(pageId).classList.add('active');
    
    // Special handling for specific pages
    if (pageId === 'aptitude-page') {
        renderQuestions();
        startTimer();
    }
}

// Resume Upload Handling
document.addEventListener('DOMContentLoaded', function() {
    const uploadInput = document.getElementById('resume-upload');
    const uploadArea = document.getElementById('upload-area');
    const fileInfo = document.getElementById('file-info');
    const fileNameText = document.getElementById('file-name-text');
    const analyzeBtn = document.getElementById('analyze-btn');

    // File upload
    uploadInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file && file.type === 'application/pdf') {
            appState.fileName = file.name;
            fileNameText.textContent = file.name;
            fileInfo.classList.remove('hidden');
            uploadArea.style.borderColor = 'var(--success-color)';
            analyzeBtn.disabled = false;
        }
    });

    // Drag and drop
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--primary-color)';
    });

    uploadArea.addEventListener('dragleave', function(e) {
        uploadArea.style.borderColor = 'var(--border-color)';
    });

    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        const file = e.dataTransfer.files[0];
        if (file && file.type === 'application/pdf') {
            uploadInput.files = e.dataTransfer.files;
            appState.fileName = file.name;
            fileNameText.textContent = file.name;
            fileInfo.classList.remove('hidden');
            uploadArea.style.borderColor = 'var(--success-color)';
            analyzeBtn.disabled = false;
        }
    });
});

// Analyze Resume
function analyzeResume() {
    navigateTo('report-page');
    
    // Show loading animation
    document.getElementById('planner-loading').style.display = 'block';
    document.getElementById('pre-report').classList.add('hidden');
    
    // Simulate AI processing
    setTimeout(() => {
        // Generate resume analysis
        generateResumeAnalysis();
        
        // Hide loading and show report
        document.getElementById('planner-loading').style.display = 'none';
        document.getElementById('pre-report').classList.remove('hidden');
    }, 3000);
}

// Generate Resume Analysis (dummy data)
function generateResumeAnalysis() {
    // Determine skill set based on filename
    let selectedSkillSet = skillSets.default;
    const fileName = appState.fileName.toLowerCase();
    
    if (fileName.includes('python')) {
        selectedSkillSet = skillSets.python;
    } else if (fileName.includes('java')) {
        selectedSkillSet = skillSets.java;
    } else if (fileName.includes('javascript') || fileName.includes('react')) {
        selectedSkillSet = skillSets.javascript;
    }
    
    // Generate random resume score between 65-85
    appState.resumeScore = Math.floor(Math.random() * 21) + 65;
    appState.detectedSkills = selectedSkillSet.detected;
    appState.missingSkills = selectedSkillSet.missing;
    
    // Update UI
    document.getElementById('resume-score').textContent = appState.resumeScore;
    
    // Update detected skills
    const detectedSkillsContainer = document.getElementById('detected-skills');
    detectedSkillsContainer.innerHTML = '';
    appState.detectedSkills.forEach(skill => {
        const tag = document.createElement('span');
        tag.className = 'skill-tag';
        tag.textContent = skill;
        detectedSkillsContainer.appendChild(tag);
    });
    
    // Update missing skills
    const missingSkillsContainer = document.getElementById('missing-skills');
    missingSkillsContainer.innerHTML = '';
    appState.missingSkills.forEach(skill => {
        const tag = document.createElement('span');
        tag.className = 'skill-tag missing';
        tag.textContent = skill;
        missingSkillsContainer.appendChild(tag);
    });
}

// Render Aptitude Questions
function renderQuestions() {
    const container = document.getElementById('questions-container');
    container.innerHTML = '';
    
    questions.forEach((q, index) => {
        const questionBlock = document.createElement('div');
        questionBlock.className = 'question-block';
        
        const questionNumber = document.createElement('div');
        questionNumber.className = 'question-number';
        questionNumber.textContent = `Question ${index + 1} of ${questions.length}`;
        
        const questionText = document.createElement('div');
        questionText.className = 'question-text';
        questionText.textContent = q.question;
        
        const optionsDiv = document.createElement('div');
        optionsDiv.className = 'options';
        
        q.options.forEach((option, optIndex) => {
            const optionDiv = document.createElement('div');
            optionDiv.className = 'option';
            
            const radio = document.createElement('input');
            radio.type = 'radio';
            radio.name = `question-${q.id}`;
            radio.value = optIndex;
            radio.id = `q${q.id}-opt${optIndex}`;
            
            const label = document.createElement('label');
            label.htmlFor = `q${q.id}-opt${optIndex}`;
            label.textContent = option;
            
            optionDiv.appendChild(radio);
            optionDiv.appendChild(label);
            optionsDiv.appendChild(optionDiv);
        });
        
        questionBlock.appendChild(questionNumber);
        questionBlock.appendChild(questionText);
        questionBlock.appendChild(optionsDiv);
        container.appendChild(questionBlock);
    });
}

// Timer
let timerInterval;
let timeRemaining = 600; // 10 minutes in seconds

function startTimer() {
    clearInterval(timerInterval);
    timeRemaining = 600;
    
    timerInterval = setInterval(() => {
        timeRemaining--;
        
        const minutes = Math.floor(timeRemaining / 60);
        const seconds = timeRemaining % 60;
        
        document.getElementById('time-display').textContent = 
            `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        
        if (timeRemaining <= 0) {
            clearInterval(timerInterval);
            submitAptitude();
        }
    }, 1000);
}

// Submit Aptitude Test
function submitAptitude() {
    clearInterval(timerInterval);
    
    // Collect answers
    let correctAnswers = 0;
    questions.forEach(q => {
        const selected = document.querySelector(`input[name="question-${q.id}"]:checked`);
        if (selected) {
            appState.answers[q.id] = parseInt(selected.value);
            if (parseInt(selected.value) === q.correct) {
                correctAnswers++;
            }
        }
    });
    
    // Calculate score
    appState.aptitudeScore = Math.floor((correctAnswers / questions.length) * 100);
    
    // Show executor loading
    navigateTo('executor-loading-page');
    
    // Simulate evaluation
    setTimeout(() => {
        generateResults();
        navigateTo('results-page');
    }, 3000);
}

// Generate Results
function generateResults() {
    // Update aptitude score
    document.getElementById('aptitude-score').textContent = appState.aptitudeScore;
    
    // Generate strengths based on score
    const strengthsList = document.getElementById('strengths-list');
    strengthsList.innerHTML = '';
    
    let strengths = [];
    if (appState.aptitudeScore >= 80) {
        strengths = [
            'Excellent problem-solving abilities',
            'Strong grasp of advanced concepts',
            'Industry-ready technical skills'
        ];
    } else if (appState.aptitudeScore >= 60) {
        strengths = [
            'Good algorithmic thinking',
            'Solid programming fundamentals',
            'Decent understanding of core concepts'
        ];
    } else {
        strengths = [
            'Basic programming knowledge',
            'Willingness to learn',
            'Foundation for growth'
        ];
    }
    
    strengths.forEach(strength => {
        const li = document.createElement('li');
        li.textContent = strength;
        strengthsList.appendChild(li);
    });
    
    // Generate weak areas
    const weakAreasList = document.getElementById('weak-areas-list');
    weakAreasList.innerHTML = '';
    
    let weakAreas = [];
    if (appState.aptitudeScore < 80) {
        weakAreas = [
            'System design concepts',
            'Advanced data structures',
            'Scalability patterns'
        ];
    } else {
        weakAreas = [
            'Minor optimization techniques',
            'Edge case handling',
            'Performance tuning'
        ];
    }
    
    weakAreas.forEach(area => {
        const li = document.createElement('li');
        li.textContent = area;
        weakAreasList.appendChild(li);
    });
}

// Download Report
function downloadReport() {
    // Create a simple text report
    const report = `
AGENTIC AI CAREER BRIDGE - ASSESSMENT REPORT
=============================================

RESUME ANALYSIS
---------------
Resume Score: ${appState.resumeScore}/100

Detected Skills:
${appState.detectedSkills.map(s => `- ${s}`).join('\n')}

Missing Skills:
${appState.missingSkills.map(s => `- ${s}`).join('\n')}

APTITUDE TEST RESULTS
--------------------
Aptitude Score: ${appState.aptitudeScore}/100

PERSONALIZED ROADMAP
-------------------
1. Master System Design Fundamentals
   Duration: 4-6 weeks

2. Learn Cloud Technologies
   Duration: 6-8 weeks

3. Build Real-World Projects
   Duration: 8-10 weeks

4. Develop Communication Skills
   Duration: Ongoing

RECOMMENDED RESOURCES
--------------------
- Designing Data-Intensive Applications by Martin Kleppmann
- System Design Interview Course
- Cloud Practitioner Certification
- Contribute to Open Source Projects

Generated by: Agentic AI Career Bridge
Date: ${new Date().toLocaleDateString()}
`;

    // Create and download file
    const blob = new Blob([report], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'Career_Assessment_Report.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    // Show landing page by default
    navigateTo('landing-page');
});