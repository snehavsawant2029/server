# Sahayu - Backend API

A FastAPI-based backend service that powers Sahayu, providing location-based service discovery, AI-powered chat assistance, and intelligent categorization of support services.

## 🔗 Related Repositories

**Frontend Application**: https://github.com/snehavsawant2029/care-connect-ai

This backend API serves the Sahayu frontend with all data processing, external API integrations, and AI-powered recommendations.

## 📋 What This API Does

Sahayu Backend provides:

- **AI-Powered Chat**: Context-aware conversational AI using Google Gemini for personalized assistance
- **Service Discovery**: Integration with Google Places API to find nearby support services
- **Intelligent Categorization**: Automatic intent classification to understand user needs
- **Location Services**: Reverse geocoding to convert coordinates to readable addresses
- **Email Notifications**: Contact form handling with email delivery
- **Age-Appropriate Responses**: Tailored recommendations based on user age groups

## 🛠️ Technologies Used

- **FastAPI** - Modern, fast web framework for building APIs
- **Python 3.8+** - Programming language
- **Google Gemini API** - AI-powered natural language processing
- **Google Places API** - Location and business data
- **Google Maps Geocoding API** - Address lookup services
- **HTTPX** - Async HTTP client for external API calls
- **Pydantic** - Data validation using Python type annotations

## 📦 Prerequisites

### For macOS:

1. **Install Homebrew** (if not already installed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install Python 3.8 or higher**:
   ```bash
   brew install python@3.11
   ```

3. **Verify installation**:
   ```bash
   python3 --version  # Should show 3.8 or higher
   pip3 --version     # Should be installed with Python
   ```

### For Windows:

1. **Download and install Python**:
   - Visit [python.org](https://www.python.org/downloads/)
   - Download Python 3.8 or higher (3.11 recommended)
   - Run the installer
   - **IMPORTANT**: Check "Add Python to PATH" during installation
   - Check "pip" in optional features

2. **Verify installation** (in Command Prompt or PowerShell):
   ```bash
   python --version   # Should show 3.8 or higher
   pip --version      # Should be installed with Python
   ```

   Note: On Windows, use `python` instead of `python3` and `pip` instead of `pip3`

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd Sahayu-backend
```

### 2. Create Virtual Environment

Creating a virtual environment isolates your project dependencies from system-wide Python packages.

#### macOS/Linux:
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Your prompt should now show (venv) at the beginning
```

#### Windows (Command Prompt):
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Your prompt should now show (venv) at the beginning
```

#### Windows (PowerShell):
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\Activate.ps1

# If you get an execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Then try activating again
```

**Note**: You need to activate the virtual environment every time you open a new terminal window.

### 3. Install Dependencies

With your virtual environment activated:

```bash
pip install -r requirements.txt
```

This will install:
- `fastapi` - Web framework
- `uvicorn[standard]` - ASGI server
- `pydantic` - Data validation
- `python-dotenv` - Environment variable management
- `httpx` - Async HTTP client
- `google-generativeai` - Gemini AI SDK
- And other required packages

### 4. Environment Configuration

Create a `.env` file in the root directory:

```bash
# For macOS/Linux:
touch .env

# For Windows (Command Prompt):
type nul > .env

# For Windows (PowerShell):
New-Item .env
```

Add the following environment variables to `.env`:

```env
# Google API Keys (Required)
GOOGLE_API_KEY=your_google_maps_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# Email Configuration (Optional - for contact form)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_specific_password
CONTACT_EMAIL=contact@Sahayuai.com

# Server Configuration (Optional)
HOST=0.0.0.0
PORT=8000
```

**Important Notes:**
- Never commit `.env` to version control (it's in `.gitignore`)
- Keep your API keys secure and private

### 5. Obtain Required API Keys

#### Google Maps API Key:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the following APIs:
   - Maps JavaScript API
   - Places API
   - Geocoding API
4. Create credentials → API Key
5. Copy the key to `GOOGLE_API_KEY` in `.env`

#### Google Gemini API Key:
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create an API key
3. Copy the key to `GEMINI_API_KEY` in `.env`

#### Email Configuration (Optional):
For Gmail:
1. Enable 2-Factor Authentication on your Google account
2. Generate an [App Password](https://myaccount.google.com/apppasswords)
3. Use this password in `SMTP_PASSWORD`

### 6. Run the Development Server

With your virtual environment activated:

```bash
# Method 1: Using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Method 2: Using Python
python -m uvicorn main:app --reload
```

The API will start on [http://localhost:8000](http://localhost:8000)

**API Documentation**: Visit [http://localhost:8000/docs](http://localhost:8000/docs) for interactive API documentation (Swagger UI)

## 📜 Available Commands

```bash
# Start development server with auto-reload
uvicorn main:app --reload

# Start with custom host and port
uvicorn main:app --host 0.0.0.0 --port 8000

# Production server (no auto-reload)
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Run with access logs
uvicorn main:app --reload --access-log
```

## 📁 Project Structure

```
Sahayu-backend/
├── main.py                 # FastAPI application entry point
├── schemas.py             # Pydantic models for request/response
├── services/              # Business logic modules
│   ├── intent.py         # Service type classification
│   ├── geocode.py        # Location services
│   ├── places.py         # Google Places integration
│   ├── gemini.py         # AI chat generation
│   └── email.py          # Email notification service
├── .env                   # Environment variables (create this)
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🔌 API Endpoints

### Chat Endpoint
```http
POST /api/chat
Content-Type: application/json

{
  "messages": [
    {"role": "user", "content": "I need food assistance"}
  ],
  "latitude": 37.7749,
  "longitude": -122.4194,
  "age_group": "18+"
}
```

### Discover Services
```http
POST /api/discover
Content-Type: application/json

{
  "category": "FOOD",
  "latitude": 37.7749,
  "longitude": -122.4194
}
```

### Reverse Geocode
```http
POST /api/reverse_geocode
Content-Type: application/json

{
  "latitude": 37.7749,
  "longitude": -122.4194
}
```

### Contact Form
```http
POST /api/contact
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "subject": "Question about services",
  "message": "How can I volunteer?"
}
```

## 🎯 Service Categories

The API supports the following service categories:

- `FOOD` - Food banks, pantries, meal programs
- `MEDICAL` - Healthcare clinics, hospitals
- `SHELTER` - Emergency shelters, housing assistance
- `MENTAL_HEALTH` - Counseling, therapy, crisis services
- `FINANCIAL` - Financial assistance, credit counseling
- `LEGAL` - Legal aid, pro bono services
- `EDUCATION` - Libraries, adult education, job training
- `COMMUNITY_NGOS` - Community centers, nonprofits
- `TRANSPORTATION` - Public transit, mobility services
- `EMERGENCY` - Emergency services, urgent care

## 🐛 Troubleshooting

### Virtual Environment Issues
```bash
# Deactivate current environment
deactivate

# Remove old environment
rm -rf venv  # macOS/Linux
rmdir /s venv  # Windows

# Recreate environment
python3 -m venv venv  # macOS/Linux
python -m venv venv   # Windows

# Reactivate and reinstall
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Port Already in Use
```bash
# Find and kill process on port 8000 (macOS/Linux)
lsof -ti:8000 | xargs kill -9

# Or run on different port
uvicorn main:app --reload --port 8001
```

### API Key Errors
- Verify API keys are correctly set in `.env`
- Check that required APIs are enabled in Google Cloud Console
- Ensure no extra spaces or quotes around API keys in `.env`
- Restart the server after changing `.env` file

### Module Not Found Errors
```bash
# Ensure virtual environment is activated
# Then reinstall dependencies
pip install -r requirements.txt --upgrade
```

### CORS Issues
The backend allows all origins by default (`allow_origins=["*"]`). In production, update this in `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Deployment Platforms

#### Railway
1. Connect your GitHub repository
2. Add environment variables in dashboard
3. Deploy automatically

#### Render
1. Create new Web Service
2. Connect repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

#### Heroku
```bash
# Create Procfile
echo "web: uvicorn main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

## 📊 Performance Optimization

- Uses async/await for non-blocking I/O operations
- Connection pooling with httpx for external API calls
- Batch processing for multiple API requests
- Tiered radius search (5km → 15km) to minimize API calls
- Intelligent result filtering to reduce unnecessary API requests

## 🔐 Security Best Practices

- Never commit `.env` file to version control
- Use environment variables for all sensitive data
- Implement rate limiting in production (using middleware)
- Validate and sanitize all user inputs (Pydantic handles this)
- Use HTTPS in production
- Restrict CORS origins in production

## 📝 Environment Variables Reference

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `GOOGLE_API_KEY` | Google Maps/Places API key | Yes | `AIza...` |
| `GEMINI_API_KEY` | Google Gemini AI API key | Yes | `AIza...` |
| `SMTP_SERVER` | Email SMTP server | No | `smtp.gmail.com` |
| `SMTP_PORT` | Email SMTP port | No | `587` |
| `SMTP_USERNAME` | Email account username | No | `user@gmail.com` |
| `SMTP_PASSWORD` | Email account password | No | `app_password` |
| `CONTACT_EMAIL` | Recipient email for contacts | No | `contact@example.com` |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

[Your License Here]

## 💬 Support

For issues and questions:
- Open an issue on GitHub
- Contact: contact@Sahayuai.com

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Powered by [Google Gemini AI](https://ai.google.dev/)
- Location data from [Google Maps Platform](https://mapsplatform.google.com/)