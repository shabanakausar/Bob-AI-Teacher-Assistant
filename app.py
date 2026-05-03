"""
Bob - AI Teacher Assistant Agent
A comprehensive educational platform with adaptive learning capabilities
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import json
import random
from datetime import datetime
import os
from dotenv import load_dotenv
import warnings

# Import Groq client
from groq_client import GroqClient

# Suppress deprecation warnings
warnings.filterwarnings('ignore', category=FutureWarning)

# Load environment variables
load_dotenv()

# Configure AI Model - Try Groq first, then Gemini as fallback
model = None
AI_PROVIDER = None

# Try Groq API first (preferred - fast and free)
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
if GROQ_API_KEY:
    try:
        model = GroqClient(GROQ_API_KEY)
        # Test the connection
        test_response = model.generate_text("test", max_tokens=5)
        if test_response:
            AI_PROVIDER = "GROQ"
            print("SUCCESS: Groq AI configured successfully with Llama 3.3!")
        else:
            model = None
    except Exception as e:
        print(f"WARNING: Could not configure Groq AI: {e}")
        model = None

# Fallback to Gemini if Groq not available
if model is None:
    try:
        import google.generativeai as genai
        GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
        if GEMINI_API_KEY:
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-2.0-flash')
            AI_PROVIDER = "GEMINI"
            print("SUCCESS: Gemini AI configured successfully with gemini-2.0-flash!")
    except Exception as e:
        print(f"WARNING: Could not configure Gemini AI: {e}")
        model = None

if model is None:
    AI_PROVIDER = "FALLBACK"
    print("WARNING: No AI provider configured. Using fallback mode with sample questions.")

app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)

class BobTeacherAssistant:
    """
    Main AI Teacher Assistant class implementing all educational modes
    """
    
    def __init__(self):
        self.difficulty_levels = ['EASY', 'MEDIUM', 'HARD']
        self.current_difficulty = 'MEDIUM'
        self.performance_tracker = {
            'correct': 0,
            'wrong': 0,
            'total': 0,
            'difficulty_performance': {'EASY': [], 'MEDIUM': [], 'HARD': []},
            'weak_topics': [],
            'session_history': []
        }
        
    def generate_mcq(self, topic, difficulty='MEDIUM', count=1):
        """
        Generate Multiple Choice Questions based on topic and difficulty using Gemini AI
        """
        questions = []
        
        if model is None:
            # Fallback to sample questions if API key not configured
            return self._generate_fallback_mcq(topic, difficulty, count)
        
        difficulty_prompts = {
            'EASY': 'basic level, suitable for beginners',
            'MEDIUM': 'intermediate level, requiring conceptual understanding',
            'HARD': 'advanced level, requiring analytical thinking and deep understanding'
        }
        
        for i in range(count):
            try:
                prompt = f"""Generate a multiple-choice question about "{topic}" at {difficulty_prompts[difficulty]}.

Format your response EXACTLY as follows (use this exact structure):
QUESTION: [Your question here]
A) [First option]
B) [Second option]
C) [Third option]
D) [Fourth option]
CORRECT: [A, B, C, or D]
EXPLANATION: [Detailed explanation of why the answer is correct]

Make sure the question is educational, accurate, and the options are plausible but only one is correct."""

                # Call AI based on provider
                if AI_PROVIDER == "GROQ":
                    response_text = model.generate_text(prompt, max_tokens=500)
                elif AI_PROVIDER == "GEMINI":
                    response = model.generate_content(prompt)
                    response_text = response.text
                else:
                    response_text = None
                
                if response_text:
                    parsed = self._parse_mcq_response(response_text, topic, difficulty, i+1)
                    if parsed:
                        questions.append(parsed)
                    else:
                        # Fallback if parsing fails
                        questions.append(self._generate_fallback_mcq(topic, difficulty, 1)[0])
                else:
                    questions.append(self._generate_fallback_mcq(topic, difficulty, 1)[0])
            except Exception as e:
                print(f"Error generating question: {e}")
                questions.append(self._generate_fallback_mcq(topic, difficulty, 1)[0])
        
        return questions
    
    def _parse_mcq_response(self, response_text, topic, difficulty, question_num):
        """Parse Gemini AI response into structured question format"""
        try:
            lines = response_text.strip().split('\n')
            question_text = ""
            options = {}
            correct_answer = ""
            explanation = ""
            
            current_section = None
            
            for line in lines:
                line = line.strip()
                if line.startswith('QUESTION:'):
                    question_text = line.replace('QUESTION:', '').strip()
                    current_section = 'question'
                elif line.startswith('A)'):
                    options['A'] = line.replace('A)', '').strip()
                elif line.startswith('B)'):
                    options['B'] = line.replace('B)', '').strip()
                elif line.startswith('C)'):
                    options['C'] = line.replace('C)', '').strip()
                elif line.startswith('D)'):
                    options['D'] = line.replace('D)', '').strip()
                elif line.startswith('CORRECT:'):
                    correct_answer = line.replace('CORRECT:', '').strip().upper()
                    if correct_answer not in ['A', 'B', 'C', 'D']:
                        correct_answer = correct_answer[0] if correct_answer else 'A'
                elif line.startswith('EXPLANATION:'):
                    explanation = line.replace('EXPLANATION:', '').strip()
                    current_section = 'explanation'
                elif current_section == 'explanation' and line:
                    explanation += ' ' + line
            
            if question_text and len(options) == 4 and correct_answer:
                return {
                    'id': f'mcq_{question_num}',
                    'type': 'MCQ',
                    'difficulty': difficulty,
                    'topic': topic,
                    'question': question_text,
                    'options': options,
                    'correct_answer': correct_answer,
                    'explanation': explanation or f'The correct answer is {correct_answer}.'
                }
        except Exception as e:
            print(f"Error parsing MCQ response: {e}")
        
        return None
    
    def _generate_fallback_mcq(self, topic, difficulty, count):
        """Fallback method for generating sample MCQs when AI is not available"""
        questions = []
        question_templates = {
            'EASY': f'What is the basic concept of {topic}?',
            'MEDIUM': f'How does {topic} work in practice?',
            'HARD': f'Analyze the advanced applications of {topic}.'
        }
        
        for i in range(count):
            question = {
                'id': f'mcq_{i+1}',
                'type': 'MCQ',
                'difficulty': difficulty,
                'topic': topic,
                'question': question_templates[difficulty],
                'options': {
                    'A': f'A fundamental aspect of {topic}',
                    'B': f'An alternative interpretation of {topic}',
                    'C': f'A related but different concept',
                    'D': f'An incorrect understanding of {topic}'
                },
                'correct_answer': 'A',
                'explanation': f'This is a sample question. Please configure GEMINI_API_KEY for AI-generated questions.'
            }
            questions.append(question)
        
        return questions
    
    def generate_short_question(self, topic, difficulty='MEDIUM', count=1):
        """
        Generate Short Answer Questions using Gemini AI
        """
        questions = []
        
        if model is None:
            return self._generate_fallback_short(topic, difficulty, count)
        
        difficulty_prompts = {
            'EASY': 'basic level, requiring simple explanation',
            'MEDIUM': 'intermediate level, requiring clear understanding',
            'HARD': 'advanced level, requiring detailed knowledge'
        }
        
        for i in range(count):
            try:
                prompt = f"""Generate a short answer question about "{topic}" at {difficulty_prompts[difficulty]}.

Format your response EXACTLY as follows:
QUESTION: [Your question here - should require a brief 50-100 word answer]
KEYWORDS: [List 3-5 key terms that should appear in a good answer, separated by commas]
SAMPLE_ANSWER: [A brief sample answer showing what a good response looks like]

Make the question clear and focused."""

                response = model.generate_content(prompt)
                parsed = self._parse_short_response(response.text, topic, difficulty, i+1)
                if parsed:
                    questions.append(parsed)
                else:
                    questions.append(self._generate_fallback_short(topic, difficulty, 1)[0])
            except Exception as e:
                print(f"Error generating short question: {e}")
                questions.append(self._generate_fallback_short(topic, difficulty, 1)[0])
        
        return questions
    
    def _parse_short_response(self, response_text, topic, difficulty, question_num):
        """Parse Gemini AI response for short answer questions"""
        try:
            lines = response_text.strip().split('\n')
            question_text = ""
            keywords = []
            
            for line in lines:
                line = line.strip()
                if line.startswith('QUESTION:'):
                    question_text = line.replace('QUESTION:', '').strip()
                elif line.startswith('KEYWORDS:'):
                    keywords_str = line.replace('KEYWORDS:', '').strip()
                    keywords = [k.strip().lower() for k in keywords_str.split(',')]
            
            if question_text and keywords:
                return {
                    'id': f'short_{question_num}',
                    'type': 'SHORT',
                    'difficulty': difficulty,
                    'topic': topic,
                    'question': question_text,
                    'expected_keywords': keywords,
                    'max_words': 50 if difficulty == 'EASY' else 100
                }
        except Exception as e:
            print(f"Error parsing short answer response: {e}")
        
        return None
    
    def _generate_fallback_short(self, topic, difficulty, count):
        """Fallback for short answer questions"""
        questions = []
        for i in range(count):
            question = {
                'id': f'short_{i+1}',
                'type': 'SHORT',
                'difficulty': difficulty,
                'topic': topic,
                'question': f'Briefly explain {topic}.',
                'expected_keywords': [topic.lower(), 'concept', 'definition'],
                'max_words': 50 if difficulty == 'EASY' else 100
            }
            questions.append(question)
        return questions
    
    def generate_long_question(self, topic, difficulty='MEDIUM', count=1):
        """
        Generate Long Descriptive Questions using Gemini AI
        """
        questions = []
        
        if model is None:
            return self._generate_fallback_long(topic, difficulty, count)
        
        difficulty_prompts = {
            'EASY': 'basic level, requiring a structured explanation with examples',
            'MEDIUM': 'intermediate level, requiring detailed analysis and multiple perspectives',
            'HARD': 'advanced level, requiring comprehensive analysis, critical thinking, and real-world applications'
        }
        
        for i in range(count):
            try:
                prompt = f"""Generate a long answer question about "{topic}" at {difficulty_prompts[difficulty]}.

Format your response EXACTLY as follows:
QUESTION: [Your question here - should require a detailed 200-400 word answer]
STRUCTURE: [List the expected sections: e.g., Introduction, Main Concepts, Examples, Applications, Conclusion]
MIN_WORDS: [Minimum word count expected: 200 for EASY, 300 for MEDIUM/HARD]

Make the question comprehensive and thought-provoking."""

                response = model.generate_content(prompt)
                parsed = self._parse_long_response(response.text, topic, difficulty, i+1)
                if parsed:
                    questions.append(parsed)
                else:
                    questions.append(self._generate_fallback_long(topic, difficulty, 1)[0])
            except Exception as e:
                print(f"Error generating long question: {e}")
                questions.append(self._generate_fallback_long(topic, difficulty, 1)[0])
        
        return questions
    
    def _parse_long_response(self, response_text, topic, difficulty, question_num):
        """Parse Gemini AI response for long answer questions"""
        try:
            lines = response_text.strip().split('\n')
            question_text = ""
            min_words = 200 if difficulty == 'EASY' else 300
            
            for line in lines:
                line = line.strip()
                if line.startswith('QUESTION:'):
                    question_text = line.replace('QUESTION:', '').strip()
                elif line.startswith('MIN_WORDS:'):
                    try:
                        min_words = int(line.replace('MIN_WORDS:', '').strip())
                    except:
                        pass
            
            if question_text:
                return {
                    'id': f'long_{question_num}',
                    'type': 'LONG',
                    'difficulty': difficulty,
                    'topic': topic,
                    'question': question_text,
                    'expected_structure': ['introduction', 'main_points', 'examples', 'conclusion'],
                    'min_words': min_words
                }
        except Exception as e:
            print(f"Error parsing long answer response: {e}")
        
        return None
    
    def _generate_fallback_long(self, topic, difficulty, count):
        """Fallback for long answer questions"""
        questions = []
        for i in range(count):
            question = {
                'id': f'long_{i+1}',
                'type': 'LONG',
                'difficulty': difficulty,
                'topic': topic,
                'question': f'Provide a detailed explanation of {topic}, including examples and applications.',
                'expected_structure': ['introduction', 'main_points', 'examples', 'conclusion'],
                'min_words': 200 if difficulty == 'EASY' else 300
            }
            questions.append(question)
        return questions
    
    def evaluate_mcq_answer(self, question, user_answer):
        """
        Evaluate MCQ answer and provide feedback
        """
        is_correct = user_answer.upper() == question['correct_answer'].upper()
        
        self.performance_tracker['total'] += 1
        if is_correct:
            self.performance_tracker['correct'] += 1
            self.performance_tracker['difficulty_performance'][question['difficulty']].append(1)
        else:
            self.performance_tracker['wrong'] += 1
            self.performance_tracker['difficulty_performance'][question['difficulty']].append(0)
        
        # Adaptive difficulty adjustment
        self._adjust_difficulty(is_correct)
        
        feedback = {
            'is_correct': is_correct,
            'correct_answer': question['correct_answer'],
            'explanation': question['explanation'],
            'next_difficulty': self.current_difficulty,
            'performance': self._get_performance_summary()
        }
        
        return feedback
    
    def evaluate_short_answer(self, question, user_answer):
        """
        Evaluate short answer based on keywords and length
        """
        user_answer_lower = user_answer.lower()
        word_count = len(user_answer.split())
        
        # Check for expected keywords
        keywords_found = sum(1 for keyword in question['expected_keywords'] 
                           if keyword in user_answer_lower)
        keyword_score = keywords_found / len(question['expected_keywords'])
        
        # Check word count
        length_appropriate = word_count <= question['max_words']
        
        # Overall score
        is_correct = keyword_score >= 0.5 and length_appropriate
        
        self.performance_tracker['total'] += 1
        if is_correct:
            self.performance_tracker['correct'] += 1
            self.performance_tracker['difficulty_performance'][question['difficulty']].append(1)
        else:
            self.performance_tracker['wrong'] += 1
            self.performance_tracker['difficulty_performance'][question['difficulty']].append(0)
        
        self._adjust_difficulty(is_correct)
        
        feedback = {
            'is_correct': is_correct,
            'score': keyword_score * 100,
            'keywords_found': keywords_found,
            'total_keywords': len(question['expected_keywords']),
            'word_count': word_count,
            'feedback': self._generate_short_answer_feedback(keyword_score, length_appropriate),
            'next_difficulty': self.current_difficulty
        }
        
        return feedback
    
    def evaluate_long_answer(self, question, user_answer):
        """
        Evaluate long answer based on structure, content, and length
        """
        word_count = len(user_answer.split())
        
        # Check minimum word count
        meets_length = word_count >= question['min_words']
        
        # Simple structure check (in real implementation, use NLP)
        has_structure = len(user_answer.split('\n\n')) >= 2
        
        # Content relevance (simple keyword check)
        topic_mentioned = question['topic'].lower() in user_answer.lower()
        
        # Overall evaluation
        score = 0
        if meets_length:
            score += 40
        if has_structure:
            score += 30
        if topic_mentioned:
            score += 30
        
        is_correct = score >= 70
        
        self.performance_tracker['total'] += 1
        if is_correct:
            self.performance_tracker['correct'] += 1
            self.performance_tracker['difficulty_performance'][question['difficulty']].append(1)
        else:
            self.performance_tracker['wrong'] += 1
            self.performance_tracker['difficulty_performance'][question['difficulty']].append(0)
        
        self._adjust_difficulty(is_correct)
        
        feedback = {
            'is_correct': is_correct,
            'score': score,
            'word_count': word_count,
            'meets_length': meets_length,
            'has_structure': has_structure,
            'topic_mentioned': topic_mentioned,
            'feedback': self._generate_long_answer_feedback(score, meets_length, has_structure),
            'next_difficulty': self.current_difficulty
        }
        
        return feedback
    
    def _adjust_difficulty(self, is_correct):
        """
        Adaptive difficulty adjustment based on performance
        """
        current_index = self.difficulty_levels.index(self.current_difficulty)
        
        if is_correct and current_index < len(self.difficulty_levels) - 1:
            # Increase difficulty if answer is correct
            self.current_difficulty = self.difficulty_levels[current_index + 1]
        elif not is_correct and current_index > 0:
            # Decrease difficulty if answer is wrong
            self.current_difficulty = self.difficulty_levels[current_index - 1]
    
    def _generate_short_answer_feedback(self, keyword_score, length_appropriate):
        """
        Generate feedback for short answers
        """
        if keyword_score >= 0.8 and length_appropriate:
            return "Excellent! Your answer covers the key points concisely."
        elif keyword_score >= 0.5:
            return "Good attempt! Try to include more key concepts in your answer."
        else:
            return "Your answer needs improvement. Focus on the main concepts and be more specific."
    
    def _generate_long_answer_feedback(self, score, meets_length, has_structure):
        """
        Generate feedback for long answers
        """
        feedback_parts = []
        
        if score >= 90:
            return "Outstanding! Your answer is comprehensive, well-structured, and detailed."
        
        if not meets_length:
            feedback_parts.append("Your answer is too brief. Provide more detailed explanation.")
        if not has_structure:
            feedback_parts.append("Improve your answer structure with clear paragraphs.")
        
        if feedback_parts:
            return " ".join(feedback_parts)
        else:
            return "Good answer! Keep up the good work."
    
    def _get_performance_summary(self):
        """
        Get current performance summary
        """
        if self.performance_tracker['total'] == 0:
            accuracy = 0
        else:
            accuracy = (self.performance_tracker['correct'] / self.performance_tracker['total']) * 100
        
        return {
            'total_questions': self.performance_tracker['total'],
            'correct': self.performance_tracker['correct'],
            'wrong': self.performance_tracker['wrong'],
            'accuracy': round(accuracy, 2)
        }
    
    def get_detailed_performance_report(self):
        """
        Generate detailed performance report for end of session
        """
        performance = self._get_performance_summary()
        
        # Calculate difficulty-wise performance
        difficulty_stats = {}
        for level in self.difficulty_levels:
            results = self.performance_tracker['difficulty_performance'][level]
            if results:
                difficulty_stats[level] = {
                    'attempted': len(results),
                    'correct': sum(results),
                    'accuracy': round((sum(results) / len(results)) * 100, 2)
                }
            else:
                difficulty_stats[level] = {
                    'attempted': 0,
                    'correct': 0,
                    'accuracy': 0
                }
        
        # Determine strengths and weaknesses
        strengths = []
        weaknesses = []
        
        for level, stats in difficulty_stats.items():
            if stats['accuracy'] >= 70:
                strengths.append(f"{level} level questions")
            elif stats['accuracy'] < 50 and stats['attempted'] > 0:
                weaknesses.append(f"{level} level questions")
        
        # Generate improvement advice
        advice = self._generate_improvement_advice(performance['accuracy'], weaknesses)
        
        report = {
            'overall_performance': performance,
            'difficulty_breakdown': difficulty_stats,
            'strengths': strengths if strengths else ['Keep practicing to identify your strengths'],
            'weaknesses': weaknesses if weaknesses else ['Great job! No major weaknesses identified'],
            'improvement_advice': advice,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return report
    
    def _generate_improvement_advice(self, accuracy, weaknesses):
        """
        Generate personalized improvement advice
        """
        advice = []
        
        if accuracy < 50:
            advice.append("Focus on understanding basic concepts before moving to advanced topics.")
            advice.append("Review your notes and practice more fundamental questions.")
        elif accuracy < 70:
            advice.append("You're making good progress! Focus on areas where you made mistakes.")
            advice.append("Try to understand why you got questions wrong, not just the correct answer.")
        else:
            advice.append("Excellent performance! Challenge yourself with harder questions.")
            advice.append("Help others learn - teaching reinforces your own understanding.")
        
        if weaknesses:
            advice.append(f"Pay special attention to: {', '.join(weaknesses)}")
        
        return advice
    
    def reset_session(self):
        """
        Reset performance tracker for new session
        """
        self.performance_tracker = {
            'correct': 0,
            'wrong': 0,
            'total': 0,
            'difficulty_performance': {'EASY': [], 'MEDIUM': [], 'HARD': []},
            'weak_topics': [],
            'session_history': []
        }
        self.current_difficulty = 'MEDIUM'


# Initialize Bob
bob = BobTeacherAssistant()

# Routes
@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')

@app.route('/api/generate-questions', methods=['POST'])
def generate_questions():
    """Generate questions based on mode and parameters"""
    data = request.json
    mode = data.get('mode', 'MCQ')
    topic = data.get('topic', 'General Knowledge')
    difficulty = data.get('difficulty', 'MEDIUM')
    count = data.get('count', 5)
    
    if mode == 'MCQ':
        questions = bob.generate_mcq(topic, difficulty, count)
    elif mode == 'SHORT':
        questions = bob.generate_short_question(topic, difficulty, count)
    elif mode == 'LONG':
        questions = bob.generate_long_question(topic, difficulty, count)
    else:
        return jsonify({'error': 'Invalid mode'}), 400
    
    return jsonify({
        'questions': questions,
        'current_difficulty': bob.current_difficulty
    })

@app.route('/api/evaluate-answer', methods=['POST'])
def evaluate_answer():
    """Evaluate student answer"""
    data = request.json
    question = data.get('question')
    user_answer = data.get('answer')
    
    if not question or not user_answer:
        return jsonify({'error': 'Missing question or answer'}), 400
    
    question_type = question.get('type')
    
    if question_type == 'MCQ':
        feedback = bob.evaluate_mcq_answer(question, user_answer)
    elif question_type == 'SHORT':
        feedback = bob.evaluate_short_answer(question, user_answer)
    elif question_type == 'LONG':
        feedback = bob.evaluate_long_answer(question, user_answer)
    else:
        return jsonify({'error': 'Invalid question type'}), 400
    
    return jsonify(feedback)

@app.route('/api/performance-report', methods=['GET'])
def performance_report():
    """Get detailed performance report"""
    report = bob.get_detailed_performance_report()
    return jsonify(report)

@app.route('/api/reset-session', methods=['POST'])
def reset_session():
    """Reset current session"""
    bob.reset_session()
    return jsonify({'message': 'Session reset successfully'})

@app.route('/api/quiz-mode', methods=['POST'])
def quiz_mode():
    """Interactive quiz mode - get next question"""
    data = request.json
    topic = data.get('topic', 'General Knowledge')
    
    # Generate one question at current difficulty
    question = bob.generate_mcq(topic, bob.current_difficulty, 1)[0]
    
    return jsonify({
        'question': question,
        'current_difficulty': bob.current_difficulty,
        'performance': bob._get_performance_summary()
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)

# Made with Bob
