// DOM Elements
const articleInput = document.getElementById('news-article');
const analyzeBtn = document.getElementById('analyze-btn');
const charCount = document.getElementById('char-count');
const loadingSection = document.getElementById('loading-section');
const resultSection = document.getElementById('result-section');
const resultContent = document.getElementById('result-content');
const closeResultBtn = document.getElementById('close-result');

// Character counter
articleInput.addEventListener('input', () => {
    const count = articleInput.value.length;
    charCount.textContent = count.toLocaleString();
    
    // Enable/disable button based on content
    analyzeBtn.disabled = count < 50;
});

// API Configuration
const API_BASE_URL = 'http://localhost:8000'; // Change this to your backend URL
const API_ENDPOINT = '/api/detect'; // Change this to your actual endpoint

// Analyze button click handler
analyzeBtn.addEventListener('click', async () => {
    const articleText = articleInput.value.trim();
    
    if (articleText.length < 50) {
        showError('Please enter at least 50 characters of text to analyze.');
        return;
    }
    
    // Show loading, hide result
    showLoading();
    hideResult();
    
    try {
        const result = await analyzeArticle(articleText);
        displayResult(result);
    } catch (error) {
        console.error('Error analyzing article:', error);
        showError('Failed to analyze article. Please try again or check your connection.');
    }
});

// Close result button
closeResultBtn.addEventListener('click', () => {
    hideResult();
});

// Analyze article function
async function analyzeArticle(text) {
    // Simulate API call - Replace this with actual API call
    // For now, this is a mock implementation
    
    // Uncomment below and modify to match your actual API
    /*
    const response = await fetch(`${API_BASE_URL}${API_ENDPOINT}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            article: text
        })
    });
    
    if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
    }
    
    return await response.json();
    */
    
    // Mock implementation for demonstration
    return new Promise((resolve) => {
        setTimeout(() => {
            // Simulate analysis
            const wordCount = text.split(/\s+/).length;
            const hasQuestionMarks = (text.match(/\?/g) || []).length;
            const hasExclamationMarks = (text.match(/!/g) || []).length;
            
            // Simple heuristic (replace with actual AI model)
            const isFake = hasExclamationMarks > 3 || (hasQuestionMarks > 2 && wordCount < 200);
            const confidence = Math.random() * 0.3 + 0.7; // 70-100%
            
            resolve({
                is_fake: isFake,
                confidence: confidence,
                explanation: isFake 
                    ? 'This article shows characteristics commonly associated with fake news, including excessive use of punctuation and potentially misleading information.'
                    : 'This article appears to be from a credible source with balanced reporting and factual presentation.'
            });
        }, 2000); // Simulate 2 second delay
    });
}

// Display result
function displayResult(result) {
    hideLoading();
    
    const isFake = result.is_fake;
    const confidence = Math.round(result.confidence * 100);
    const explanation = result.explanation || 'Analysis complete.';
    
    resultContent.innerHTML = `
        <div class="result-badge ${isFake ? 'fake' : 'real'}">
            ${isFake ? `
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="12" y1="8" x2="12" y2="12"></line>
                    <line x1="12" y1="16" x2="12.01" y2="16"></line>
                </svg>
                <span>Fake News Detected</span>
            ` : `
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                    <polyline points="22 4 12 14.01 9 11.01"></polyline>
                </svg>
                <span>Real News Verified</span>
            `}
        </div>
        
        <div class="result-details">
            <h3>Analysis Details</h3>
            <p>${explanation}</p>
            
            <div class="confidence-bar">
                <div class="confidence-label">
                    <span>Confidence Level</span>
                    <span><strong>${confidence}%</strong></span>
                </div>
                <div class="confidence-progress">
                    <div class="confidence-fill" style="width: ${confidence}%"></div>
                </div>
            </div>
        </div>
    `;
    
    showResult();
}

// Show loading state
function showLoading() {
    loadingSection.classList.remove('hidden');
    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = '<span class="btn-text">Analyzing...</span>';
}

// Hide loading state
function hideLoading() {
    loadingSection.classList.add('hidden');
    analyzeBtn.disabled = false;
    analyzeBtn.innerHTML = `
        <span class="btn-text">Analyze Article</span>
        <svg class="btn-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path d="M4 10 L16 10 M10 4 L16 10 L10 16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
    `;
}

// Show result
function showResult() {
    resultSection.classList.remove('hidden');
    resultSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Hide result
function hideResult() {
    resultSection.classList.add('hidden');
}

// Show error
function showError(message) {
    hideLoading();
    
    resultContent.innerHTML = `
        <div class="result-badge fake">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="15" y1="9" x2="9" y2="15"></line>
                <line x1="9" y1="9" x2="15" y2="15"></line>
            </svg>
            <span>Error</span>
        </div>
        <div class="result-details">
            <p style="color: #e53e3e;">${message}</p>
        </div>
    `;
    
    showResult();
}

// Allow Enter key to submit (Ctrl+Enter or Cmd+Enter)
articleInput.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        if (!analyzeBtn.disabled) {
            analyzeBtn.click();
        }
    }
});

// Initialize
analyzeBtn.disabled = true;


