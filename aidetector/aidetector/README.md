# TrueLens - Fake News Detector Frontend

A beautiful, modern frontend for detecting fake news articles using AI-powered analysis.

## Features

- 🎨 **Modern, Branded UI**: Hero, about, feature, and contact sections with the TrueLens eye logo
- 📱 **Fully Responsive**: Adaptive navigation, mobile drawer menu, and fluid grids
- ⚡ **Real-time Analysis**: Detector lab with loaders, confidence bars, and contextual messaging
- 🔐 **Login Portal**: Dedicated login page for moderators with CTA highlights
- 🤝 **Contact & Social**: Outreach cards, form, and partner-friendly callouts
- ✨ **Beautiful Animations**: Ambient gradients, shadows, and motion cues

## Files Structure

```
aidetector/
├── index.html           # Main landing page with sections + detector
├── login.html           # Moderator login experience
├── styles.css           # Shared styles, components, and responsive rules
├── script.js            # Detector logic and API integration
├── assets/
│   └── truelens-logo.svg # Eye logo used site-wide
└── README.md
```

## Setup Instructions

1. **Open the frontend**: Simply open `index.html` in your web browser, or serve it using a local server:
   ```bash
   # Using Python
   python -m http.server 8080
   
   # Using Node.js (if you have http-server installed)
   npx http-server -p 8080
   ```

2. **Connect to Backend API**: 
   - Open `script.js`
   - Update the `API_BASE_URL` and `API_ENDPOINT` variables (around line 15-16) to match your backend API
   - Uncomment the actual API call code in the `analyzeArticle` function (lines 48-62)
   - Remove or comment out the mock implementation (lines 65-85)

## API Integration

The frontend expects your backend API to:

1. **Endpoint**: Accept POST requests at `/api/detect` (or your configured endpoint)
2. **Request Format**:
   ```json
   {
     "article": "Your news article text here..."
   }
   ```

3. **Response Format**:
   ```json
   {
     "is_fake": true/false,
     "confidence": 0.85,
     "explanation": "Detailed explanation of the analysis..."
   }
   ```

## Customization

- **Colors & Theme**: Update CSS variables near the top of `styles.css`
- **Navigation Links**: Edit the anchor targets inside `index.html`
- **Logo**: Replace `assets/truelens-logo.svg` with your preferred artwork (keep the same filename to avoid markup changes)
- **API Endpoint**: Update the configuration in `script.js`

## Browser Support

Works on all modern browsers:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Opera (latest)

## Notes

- The current implementation includes a mock/demo mode for testing without a backend
- Minimum 50 characters required for analysis
- Results are displayed with confidence scores and explanations


