// Bob - AI Teacher Assistant - Frontend JavaScript

// Global State
let currentMode = '';
let questions = [];
let currentQuestionIndex = 0;
let userAnswers = [];
let sessionActive = false;

// API Base URL
const API_BASE = '';

// Mode Selection
function selectMode(mode) {
    currentMode = mode;
    document.getElementById('modeSelection').style.display = 'none';
    document.getElementById('configPanel').style.display = 'block';
    
    // Hide question count for quiz mode (one at a time)
    if (mode === 'QUIZ') {
        document.getElementById('countGroup').style.display = 'none';
    } else {
        document.getElementById('countGroup').style.display = 'block';
    }
}

function backToModes() {
    document.getElementById('configPanel').style.display = 'none';
    document.getElementById('modeSelection').style.display = 'block';
    currentMode = '';
}

// Start Session
async function startSession() {
    const topic = document.getElementById('topic').value.trim();
    const difficulty = document.getElementById('difficulty').value;
    const count = parseInt(document.getElementById('questionCount').value);
    
    if (!topic) {
        alert('Please enter a topic!');
        return;
    }
    
    showLoading(true);
    
    try {
        if (currentMode === 'QUIZ') {
            // Quiz mode - get one question at a time
            await startQuizMode(topic);
        } else {
            // Regular modes - get all questions
            const response = await fetch(`${API_BASE}/api/generate-questions`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    mode: currentMode,
                    topic: topic,
                    difficulty: difficulty,
                    count: count
                })
            });
            
            const data = await response.json();
            questions = data.questions;
            currentQuestionIndex = 0;
            userAnswers = new Array(questions.length).fill(null);
            
            document.getElementById('configPanel').style.display = 'none';
            document.getElementById('questionSection').style.display = 'block';
            
            displayQuestion();
            updateProgress();
        }
        
        sessionActive = true;
    } catch (error) {
        console.error('Error starting session:', error);
        alert('Failed to start session. Please try again.');
    } finally {
        showLoading(false);
    }
}

// Quiz Mode
async function startQuizMode(topic) {
    try {
        const response = await fetch(`${API_BASE}/api/quiz-mode`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ topic: topic })
        });
        
        const data = await response.json();
        questions = [data.question];
        currentQuestionIndex = 0;
        userAnswers = [null];
        
        document.getElementById('configPanel').style.display = 'none';
        document.getElementById('questionSection').style.display = 'block';
        
        displayQuestion();
        updatePerformanceBadge(data.performance, data.current_difficulty);
    } catch (error) {
        console.error('Error in quiz mode:', error);
        throw error;
    }
}

// Display Question
function displayQuestion() {
    const question = questions[currentQuestionIndex];
    const container = document.getElementById('questionContainer');
    
    let html = `
        <div class="question-header">
            <span class="question-number">Question ${currentQuestionIndex + 1}${currentMode !== 'QUIZ' ? ' of ' + questions.length : ''}</span>
            <span class="difficulty-badge difficulty-${question.difficulty}">${question.difficulty}</span>
        </div>
        <div class="question-text">${question.question}</div>
    `;
    
    if (question.type === 'MCQ') {
        html += '<div class="options-container">';
        for (const [key, value] of Object.entries(question.options)) {
            const selected = userAnswers[currentQuestionIndex] === key ? 'selected' : '';
            html += `
                <div class="option ${selected}" onclick="selectOption('${key}')">
                    <span class="option-label">${key}.</span>
                    <span>${value}</span>
                </div>
            `;
        }
        html += '</div>';
    } else if (question.type === 'SHORT') {
        const answer = userAnswers[currentQuestionIndex] || '';
        html += `
            <textarea class="answer-input" id="answerInput" placeholder="Type your answer here..." maxlength="500">${answer}</textarea>
            <p style="color: #7f8c8d; margin-top: 10px;">Maximum ${question.max_words} words</p>
        `;
    } else if (question.type === 'LONG') {
        const answer = userAnswers[currentQuestionIndex] || '';
        html += `
            <textarea class="answer-input" id="answerInput" placeholder="Type your detailed answer here..." style="min-height: 200px;">${answer}</textarea>
            <p style="color: #7f8c8d; margin-top: 10px;">Minimum ${question.min_words} words</p>
        `;
    }
    
    container.innerHTML = html;
    container.classList.add('fade-in');
    
    // Update navigation buttons
    updateNavigationButtons();
}

// Select MCQ Option
function selectOption(option) {
    userAnswers[currentQuestionIndex] = option;
    
    // Update UI
    const options = document.querySelectorAll('.option');
    options.forEach(opt => opt.classList.remove('selected'));
    event.target.closest('.option').classList.add('selected');
}

// Submit Answer
async function submitAnswer() {
    const question = questions[currentQuestionIndex];
    let userAnswer = userAnswers[currentQuestionIndex];
    
    // Get answer from textarea if applicable
    if (question.type !== 'MCQ') {
        const input = document.getElementById('answerInput');
        if (input) {
            userAnswer = input.value.trim();
            userAnswers[currentQuestionIndex] = userAnswer;
        }
    }
    
    if (!userAnswer) {
        alert('Please provide an answer before submitting!');
        return;
    }
    
    showLoading(true);
    
    try {
        const response = await fetch(`${API_BASE}/api/evaluate-answer`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question: question,
                answer: userAnswer
            })
        });
        
        const feedback = await response.json();
        
        // Store feedback with question
        questions[currentQuestionIndex].feedback = feedback;
        
        // Display feedback
        displayFeedback(feedback, question);
        
        // Update performance badge
        if (feedback.performance) {
            updatePerformanceBadge(feedback.performance, feedback.next_difficulty);
        }
        
        // Hide submit button, show next/finish button
        document.getElementById('submitBtn').style.display = 'none';
        
        if (currentMode === 'QUIZ') {
            document.getElementById('nextBtn').style.display = 'inline-block';
            document.getElementById('finishBtn').style.display = 'inline-block';
        } else if (currentQuestionIndex < questions.length - 1) {
            document.getElementById('nextBtn').style.display = 'inline-block';
        } else {
            document.getElementById('finishBtn').style.display = 'inline-block';
        }
        
    } catch (error) {
        console.error('Error submitting answer:', error);
        alert('Failed to submit answer. Please try again.');
    } finally {
        showLoading(false);
    }
}

// Display Feedback
function displayFeedback(feedback, question) {
    const feedbackSection = document.getElementById('feedbackSection');
    const container = document.getElementById('feedbackContainer');
    
    let html = '<div class="feedback-header">';
    
    if (feedback.is_correct) {
        html += `
            <div class="feedback-icon">✅</div>
            <h2 class="feedback-title correct">Correct! Well Done!</h2>
        `;
    } else {
        html += `
            <div class="feedback-icon">❌</div>
            <h2 class="feedback-title incorrect">Not Quite Right</h2>
        `;
    }
    
    html += '</div><div class="feedback-content">';
    
    if (question.type === 'MCQ') {
        html += `
            <div class="feedback-item">
                <strong>Your Answer:</strong> ${userAnswers[currentQuestionIndex]}
            </div>
            <div class="feedback-item">
                <strong>Correct Answer:</strong> ${feedback.correct_answer}
            </div>
        `;
    } else if (question.type === 'SHORT') {
        html += `
            <div class="feedback-item">
                <strong>Score:</strong> ${feedback.score.toFixed(1)}%
            </div>
            <div class="feedback-item">
                <strong>Keywords Found:</strong> ${feedback.keywords_found} / ${feedback.total_keywords}
            </div>
            <div class="feedback-item">
                <strong>Word Count:</strong> ${feedback.word_count}
            </div>
        `;
    } else if (question.type === 'LONG') {
        html += `
            <div class="feedback-item">
                <strong>Score:</strong> ${feedback.score}%
            </div>
            <div class="feedback-item">
                <strong>Word Count:</strong> ${feedback.word_count}
            </div>
            <div class="feedback-item">
                <strong>Structure:</strong> ${feedback.has_structure ? '✓ Good' : '✗ Needs Improvement'}
            </div>
        `;
    }
    
    html += '</div>';
    
    // Add explanation
    if (feedback.explanation) {
        html += `
            <div class="explanation-box">
                <h4>📚 Explanation:</h4>
                <p>${feedback.explanation}</p>
            </div>
        `;
    } else if (feedback.feedback) {
        html += `
            <div class="explanation-box">
                <h4>💡 Feedback:</h4>
                <p>${feedback.feedback}</p>
            </div>
        `;
    }
    
    // Show next difficulty
    if (feedback.next_difficulty) {
        html += `
            <div style="text-align: center; margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 8px;">
                <strong>Next Question Difficulty:</strong> 
                <span class="difficulty-badge difficulty-${feedback.next_difficulty}">${feedback.next_difficulty}</span>
            </div>
        `;
    }
    
    container.innerHTML = html;
    feedbackSection.style.display = 'block';
    feedbackSection.scrollIntoView({ behavior: 'smooth' });
}

// Next Question
async function nextQuestion() {
    document.getElementById('feedbackSection').style.display = 'none';
    
    if (currentMode === 'QUIZ') {
        // Get next question from server
        showLoading(true);
        try {
            const topic = document.getElementById('topic').value.trim();
            const response = await fetch(`${API_BASE}/api/quiz-mode`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ topic: topic })
            });
            
            const data = await response.json();
            questions.push(data.question);
            userAnswers.push(null);
            currentQuestionIndex++;
            
            displayQuestion();
            updatePerformanceBadge(data.performance, data.current_difficulty);
            
            // Reset buttons
            document.getElementById('submitBtn').style.display = 'inline-block';
            document.getElementById('nextBtn').style.display = 'none';
            document.getElementById('finishBtn').style.display = 'none';
            
        } catch (error) {
            console.error('Error getting next question:', error);
            alert('Failed to get next question. Please try again.');
        } finally {
            showLoading(false);
        }
    } else {
        currentQuestionIndex++;
        displayQuestion();
        updateProgress();
        
        // Reset buttons
        document.getElementById('submitBtn').style.display = 'inline-block';
        document.getElementById('nextBtn').style.display = 'none';
    }
}

// Previous Question
function previousQuestion() {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        displayQuestion();
        updateProgress();
        document.getElementById('feedbackSection').style.display = 'none';
    }
}

// Finish Session
async function finishSession() {
    showLoading(true);
    
    try {
        const response = await fetch(`${API_BASE}/api/performance-report`);
        const report = await response.json();
        
        displayPerformanceReport(report);
        
        document.getElementById('questionSection').style.display = 'none';
        document.getElementById('feedbackSection').style.display = 'none';
        document.getElementById('reportSection').style.display = 'block';
        
    } catch (error) {
        console.error('Error getting performance report:', error);
        alert('Failed to generate report. Please try again.');
    } finally {
        showLoading(false);
    }
}

// Display Performance Report
function displayPerformanceReport(report) {
    const container = document.getElementById('reportContainer');
    
    const perf = report.overall_performance;
    
    let html = `
        <div class="report-summary">
            <div class="summary-card">
                <h3>${perf.total_questions}</h3>
                <p>Total Questions</p>
            </div>
            <div class="summary-card">
                <h3>${perf.correct}</h3>
                <p>Correct Answers</p>
            </div>
            <div class="summary-card">
                <h3>${perf.wrong}</h3>
                <p>Wrong Answers</p>
            </div>
            <div class="summary-card">
                <h3>${perf.accuracy}%</h3>
                <p>Accuracy</p>
            </div>
        </div>
        
        <div class="report-section-detail">
            <h3>📊 Difficulty Breakdown</h3>
            <div class="difficulty-stats">
    `;
    
    for (const [level, stats] of Object.entries(report.difficulty_breakdown)) {
        html += `
            <div class="stat-card">
                <h4>${level}</h4>
                <p>Attempted: ${stats.attempted}</p>
                <p>Correct: ${stats.correct}</p>
                <p>Accuracy: ${stats.accuracy}%</p>
            </div>
        `;
    }
    
    html += `
            </div>
        </div>
        
        <div class="report-section-detail">
            <h3>💪 Your Strengths</h3>
            <ul class="report-list">
    `;
    
    report.strengths.forEach(strength => {
        html += `<li>✓ ${strength}</li>`;
    });
    
    html += `
            </ul>
        </div>
        
        <div class="report-section-detail">
            <h3>📈 Areas for Improvement</h3>
            <ul class="report-list">
    `;
    
    report.weaknesses.forEach(weakness => {
        html += `<li>→ ${weakness}</li>`;
    });
    
    html += `
            </ul>
        </div>
        
        <div class="report-section-detail">
            <h3>💡 Bob's Advice</h3>
            <ul class="report-list">
    `;
    
    report.improvement_advice.forEach(advice => {
        html += `<li>${advice}</li>`;
    });
    
    html += `
            </ul>
        </div>
    `;
    
    container.innerHTML = html;
}

// Update Progress Bar
function updateProgress() {
    const progress = ((currentQuestionIndex + 1) / questions.length) * 100;
    document.getElementById('progressFill').style.width = `${progress}%`;
}

// Update Performance Badge
function updatePerformanceBadge(performance, difficulty) {
    document.getElementById('scoreDisplay').textContent = 
        `Score: ${performance.correct}/${performance.total_questions}`;
    document.getElementById('difficultyDisplay').textContent = 
        `Difficulty: ${difficulty}`;
}

// Update Navigation Buttons
function updateNavigationButtons() {
    const prevBtn = document.getElementById('prevBtn');
    const submitBtn = document.getElementById('submitBtn');
    
    if (currentMode === 'QUIZ') {
        prevBtn.style.display = 'none';
    } else {
        prevBtn.style.display = currentQuestionIndex > 0 ? 'inline-block' : 'none';
    }
    
    submitBtn.style.display = 'inline-block';
    document.getElementById('nextBtn').style.display = 'none';
    document.getElementById('finishBtn').style.display = 'none';
}

// Export to PDF
function exportToPDF() {
    // Create printable version
    const reportContent = document.getElementById('reportContainer').innerHTML;
    const printWindow = window.open('', '', 'height=600,width=800');
    
    printWindow.document.write(`
        <html>
        <head>
            <title>Bob - Performance Report</title>
            <style>
                body { font-family: Arial, sans-serif; padding: 20px; }
                h2, h3 { color: #4a90e2; }
                .report-summary { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px; }
                .summary-card { background: #f0f0f0; padding: 20px; text-align: center; border-radius: 8px; }
                .summary-card h3 { font-size: 2em; margin: 0; }
                .report-section-detail { margin-bottom: 30px; padding: 20px; background: #f9f9f9; border-radius: 8px; }
                .report-list { list-style: none; padding: 0; }
                .report-list li { padding: 10px 0; border-bottom: 1px solid #ddd; }
                .difficulty-stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; }
                .stat-card { background: white; padding: 15px; border-radius: 8px; border-left: 4px solid #4a90e2; }
            </style>
        </head>
        <body>
            <h1>📊 Bob - AI Teacher Assistant</h1>
            <h2>Performance Report</h2>
            ${reportContent}
            <p style="text-align: center; margin-top: 40px; color: #7f8c8d;">
                Generated on ${new Date().toLocaleString()}
            </p>
        </body>
        </html>
    `);
    
    printWindow.document.close();
    printWindow.focus();
    
    setTimeout(() => {
        printWindow.print();
    }, 250);
}

// Start New Session
async function startNewSession() {
    showLoading(true);
    
    try {
        await fetch(`${API_BASE}/api/reset-session`, { method: 'POST' });
        
        // Reset state
        currentMode = '';
        questions = [];
        currentQuestionIndex = 0;
        userAnswers = [];
        sessionActive = false;
        
        // Reset UI
        document.getElementById('reportSection').style.display = 'none';
        document.getElementById('modeSelection').style.display = 'block';
        document.getElementById('topic').value = '';
        document.getElementById('difficulty').value = 'MEDIUM';
        document.getElementById('questionCount').value = '5';
        
    } catch (error) {
        console.error('Error resetting session:', error);
    } finally {
        showLoading(false);
    }
}

// Show/Hide Loading Spinner
function showLoading(show) {
    document.getElementById('loadingSpinner').style.display = show ? 'flex' : 'none';
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('Bob - AI Teacher Assistant initialized');
});

// Made with Bob
