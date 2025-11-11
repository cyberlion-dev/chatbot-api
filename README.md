# AI Chatbot API 🤖

A production-ready REST API chatbot backend using FastAPI and HuggingFace transformers. Provides intelligent responses with configurable business knowledge - no frontend included.

## 🚀 Features

- **Free AI Models**: Uses HuggingFace transformers (no API costs)
- **Business Knowledge**: Smart keyword-based responses for business hours, location, pricing, services, etc.
- **Configurable Context**: Define your business details in a simple environment variable
- **Topic Filtering**: Restrict inappropriate topics
- **Conversation Memory**: Track conversation history
- **Production Ready**: Docker containerized, health checks, logging
- **Easy Deployment**: One-click Railway deployment
- **Fast**: Async FastAPI with optimized inference

## 🏗 Architecture

```
Your Client → REST API → Business Knowledge / AI Model → JSON Response
                                    ↕
                            Conversation Memory
```

This is a **backend API only** - integrate it with any frontend, mobile app, or service that can make HTTP requests.

## 📦 Quick Start

### Local Development

1. **Clone and setup**:
```bash
git clone <your-repo>
cd ai-chatbot-api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure your business details**:
```bash
cp .env.example .env
# Edit .env and update BUSINESS_DETAILS with your actual info
```

3. **Run the API**:
```bash
uvicorn app.main:app --reload
```

4. **Test the API**:
- Interactive docs: http://localhost:8000/docs
- Test script: `python test_api.py`
- Health check: http://localhost:8000/health

### Railway Deployment

1. **Push to GitHub**:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo>
git push -u origin main
```

2. **Deploy to Railway**:
   - Go to [railway.app](https://railway.app)
   - Connect your GitHub repo
   - Railway auto-detects the Dockerfile
   - Set environment variables in Railway dashboard

3. **Configure Environment Variables in Railway**:
```
BUSINESS_NAME=Your Business Name
BUSINESS_TYPE=your business type
BUSINESS_DETAILS="Business Hours: Your hours here. Location: Your address. Contact: Your phone and email. Services: What you offer. Pricing: Your pricing. etc."
ALLOWED_TOPICS=topic1,topic2,topic3
RESTRICTED_TOPICS=medical advice,legal advice
ENVIRONMENT=production
PORT=8000
```

## 🎯 API Endpoints

### Chat Endpoint
```bash
POST /api/v1/chat
{
  "message": "What are your business hours?",
  "conversation_id": "optional-uuid",
  "conversation_history": []
}
```

### Health Check
```bash
GET /health
```

### Configuration
```bash
GET /api/v1/config
```

## 🔧 Configuration

Edit the `.env` file to configure your chatbot. The most important setting is `BUSINESS_DETAILS`:

### Business Details (Required)
This is where you put ALL your business information. The chatbot will use this to answer customer questions:

```bash
BUSINESS_DETAILS="Business Hours: Monday-Friday 9am-6pm, Closed weekends. Location: 123 Main St, Your City, State 12345. Contact: Phone (555) 123-4567, Email info@yourbusiness.com. Services: We offer plumbing, drain cleaning, and water heater installation. Pricing: Service calls $99, hourly rate $150/hr. Shipping: N/A. Returns: 30-day satisfaction guarantee."
```

**What to include:**
- Business hours
- Location/address
- Contact info (phone, email)
- Services offered
- Pricing information
- Shipping policies (if applicable)
- Return policies
- Any other info customers commonly ask about

### Other Settings
```bash
# Business Identity
BUSINESS_NAME="Acme Plumbing"
BUSINESS_TYPE="plumbing service company"

# Topics the bot can discuss
ALLOWED_TOPICS="plumbing,pricing,scheduling,services"

# Topics to avoid
RESTRICTED_TOPICS="medical advice,legal advice,electrical work"

# AI Model (use small for faster, medium for better quality)
MODEL_NAME="microsoft/DialoGPT-small"
```

## 💡 Integration Examples

This is a REST API backend - you can integrate it with any client. Here are some examples:

### cURL (Command Line)
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are your business hours?",
    "conversation_id": null,
    "conversation_history": []
  }'
```

### Python
```python
import requests

response = requests.post('http://localhost:8000/api/v1/chat', json={
    'message': 'What are your business hours?',
    'conversation_id': None,
    'conversation_history': []
})

data = response.json()
print(data['response'])
```

### JavaScript/Fetch
```javascript
const response = await fetch('http://localhost:8000/api/v1/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: 'What are your business hours?',
    conversation_id: null,
    conversation_history: []
  })
});

const data = await response.json();
console.log(data.response);
```

**Integrate with:** React, Vue, Angular, mobile apps, Slack bots, Discord bots, or any HTTP client!

## 🎨 Customization Examples

### E-commerce Bot
```bash
BUSINESS_NAME="Fashion Store"
BUSINESS_TYPE="online clothing retailer"
ALLOWED_TOPICS="product information,sizes,shipping,returns,orders,payment"
RESTRICTED_TOPICS="medical advice,personal styling,other retailers"
```

### Restaurant Bot  
```bash
BUSINESS_NAME="Mario's Pizza"
BUSINESS_TYPE="Italian restaurant"
ALLOWED_TOPICS="menu,ordering,delivery,reservations,hours,location"
RESTRICTED_TOPICS="health advice,nutrition,other restaurants,cooking recipes"
```

### Tech Support Bot
```bash
BUSINESS_NAME="TechFix Solutions"
BUSINESS_TYPE="computer repair service"
ALLOWED_TOPICS="computer problems,diagnostics,pricing,appointments,services"
RESTRICTED_TOPICS="medical advice,legal advice,other repair shops"
```

## 📊 Performance & Costs

### Railway Hosting
- **Free Tier**: 500 hours/month, 1GB RAM
- **Starter**: $5/month, 8GB RAM, custom domain
- **Expected Usage**: ~$5-10/month for small business

### Model Performance
- **Small Model**: ~1-2 seconds response time, 500MB memory
- **Medium Model**: ~2-4 seconds response time, 1GB memory
- **CPU Only**: Works fine for small-medium traffic

## 🔐 Security Features

- **Topic Restrictions**: Prevents inappropriate responses
- **Input Validation**: Pydantic models validate all requests
- **Rate Limiting**: Built-in protection (configurable)
- **Health Checks**: Monitoring and auto-restart
- **Non-root User**: Docker security best practices

## 🚧 Roadmap

### Current Features
- ✅ Core chat functionality
- ✅ Smart business knowledge responses
- ✅ Business context restrictions
- ✅ Railway deployment ready
- ✅ Conversation memory
- ✅ REST API with OpenAPI docs

### Potential Enhancements
- [ ] Database persistence (PostgreSQL)
- [ ] User authentication
- [ ] Analytics tracking
- [ ] Custom model fine-tuning
- [ ] Multi-language support

## 🛟 Support & Troubleshooting

### Common Issues

**Model Loading Slow**: 
- Use `microsoft/DialoGPT-small` for faster startup
- Set `MODEL_DEVICE=-1` to force CPU

**Memory Issues on Railway**:
- Upgrade to Starter plan ($5/month)
- Use smaller model variant

**CORS Errors**:
- Add your domain to `ALLOWED_ORIGINS` in Railway

### Logs
Check Railway logs for debugging:
```bash
railway logs
```

## 📝 License

MIT License - feel free to use this for commercial projects.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

**Built for business owners who want AI chatbots without recurring API costs** 🚀