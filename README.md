# 🌟 Spots Recommendation System

An intelligent place discovery application that combines **AI-powered natural language processing** with **OpenStreetMap data** to help users find amazing places based on conversational queries.

![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🚀 Features

- **🤖 AI-Powered Search**: Uses Ollama with llama3.1:8b model for intelligent query interpretation
- **🗺️ Interactive Maps**: Beautiful Leaflet.js-powered maps with marker clustering
- **🌍 Global Coverage**: Powered by OpenStreetMap's comprehensive geographic database
- **📱 Responsive Design**: Modern UI that works perfectly on desktop and mobile
- **⚡ Real-time Results**: Fast API responses with proper error handling and timeouts
- **🎯 Smart Suggestions**: Quick-access buttons for popular searches
- **💫 Modern UI/UX**: Gradient designs, animations, and intuitive interactions

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, high-performance web framework for APIs
- **Ollama**: Local LLM integration for natural language processing
- **OpenStreetMap APIs**: 
  - Nominatim for geocoding
  - Overpass API for place searches
- **httpx**: Async HTTP client for external API calls
- **SlowAPI**: Rate limiting middleware
- **Pydantic**: Data validation and serialization

### Frontend
- **HTML5/CSS3**: Modern responsive design
- **Vanilla JavaScript**: Clean, dependency-free frontend code
- **Leaflet.js**: Interactive mapping library
- **Font Awesome**: Beautiful icons and visual elements

### Development
- **uvicorn**: ASGI server with hot reload
- **Python 3.13+**: Latest Python features and performance

## 📋 Prerequisites

Before running this application, ensure you have:

1. **Python 3.13+** installed
2. **Ollama** installed and running
3. **llama3.1:8b model** downloaded in Ollama
4. **Git** (for cloning the repository)

### Installing Ollama

1. Download and install Ollama from [ollama.ai](https://ollama.ai)
2. Pull the required model:
   ```bash
   ollama pull llama3.1:8b
   ```
3. Start the Ollama service:
   ```bash
   ollama serve
   ```

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/spots_recommendation.git
cd spots_recommendation
```

### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Start the Backend Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Open the Frontend
Navigate to `web/index.html` in your browser or serve it locally:
```bash
# Option 1: Direct file access
# Open web/index.html in your browser

# Option 2: Simple HTTP server (optional)
python -m http.server 3000 --directory web
# Then open http://localhost:3000
```

## 🎯 Usage Examples

Try these example queries:

- **"best seafood restaurants in Jakarta"**
- **"coffee shops in Bandung"** 
- **"museums in Yogyakarta"**
- **"parks near Surabaya"**
- **"romantic dining in Bali"**
- **"shopping malls in Manila"**

## 📁 Project Structure

```
spots_recommendation/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── schema.py            # Pydantic models and data structures
│   ├── services/
│   │   ├── __init__.py
│   │   ├── llm.py           # Ollama LLM integration
│   │   └── osm.py           # OpenStreetMap API services
│   └── utils/
│       ├── __init__.py
│       ├── logging.py       # Logging configuration
│       └── rate_limit.py    # Rate limiting utilities
├── web/
│   └── index.html           # Frontend application
├── requirements.txt         # Python dependencies
├── start_servers.bat        # Windows batch script for easy startup
└── README.md               # This file
```

## 🔧 Configuration

### Environment Variables (Optional)
Create a `.env` file in the root directory to customize settings:

```env
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# Rate Limiting
RATE_LIMIT_REQUESTS=10
RATE_LIMIT_WINDOW=60
```

### Ollama Model Configuration
The application uses the `llama3.1:8b` model by default. You can modify this in `app/services/llm.py` if you want to use a different model.

## 🔍 API Documentation

Once the server is running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

### Main Endpoint

**POST** `/chat`
```json
{
  "prompt": "best coffee shops in Bandung"
}
```

**Response:**
```json
{
  "message": "Found 5 coffee shops in Bandung",
  "items": [
    {
      "name": "Kedai Kopi Bandung",
      "lat": -6.9175,
      "lon": 107.6191,
      "address": "Jl. Braga No. 123, Bandung",
      "category": "cafe"
    }
  ]
}
```

## 🛡️ Security & Best Practices

- **Rate Limiting**: Built-in request throttling to prevent abuse
- **Input Validation**: Pydantic models ensure data integrity
- **Error Handling**: Comprehensive error management with user-friendly messages
- **CORS Configuration**: Properly configured for web browser security
- **Timeout Handling**: 30-second request timeouts to prevent hanging

## 🧪 Testing

Run basic functionality tests:

```bash
# Test backend server
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "coffee shops in Jakarta"}'

# Check API documentation
curl http://localhost:8000/docs
```

## 🚀 Deployment

### Local Development
The application is designed for local development and demonstration. For production deployment, consider:

1. **Environment Variables**: Use proper environment configuration
2. **Database**: Add persistent storage for caching results
3. **Authentication**: Implement user authentication if needed
4. **HTTPS**: Configure SSL/TLS for secure connections
5. **Docker**: Containerize the application for easier deployment

### Docker Deployment (Future Enhancement)
```bash
# Build Docker image
docker build -t spots-recommendation .

# Run container
docker run -p 8000:8000 spots-recommendation
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Acknowledgments

- **OpenStreetMap**: For providing comprehensive geographic data
- **Ollama**: For making local LLM deployment accessible
- **FastAPI**: For the excellent web framework
- **Leaflet.js**: For beautiful interactive maps

## 📞 Support

If you encounter any issues or have questions:

1. Check the [API Documentation](http://localhost:8000/docs)
2. Review the console logs for error messages
3. Ensure Ollama is running with the correct model
4. Verify your internet connection for OpenStreetMap API access

## 🔮 Future Enhancements

- [ ] **User Authentication**: Personal saved places and preferences
- [ ] **Advanced Filtering**: Price range, ratings, opening hours
- [ ] **Multi-language Support**: Queries and results in multiple languages
- [ ] **Offline Mode**: Cached results for frequently searched areas
- [ ] **Social Features**: Share discoveries and reviews
- [ ] **Mobile App**: Native iOS/Android applications
- [ ] **Advanced Analytics**: Usage patterns and popular locations

---

**Built with ❤️ using AI, Maps, and Modern Web Technologies**