# AI Chatbot API 🤖

A production-ready FastAPI chatbot service using HuggingFace transformers. Designed for business-specific contexts with configurable topics and restrictions.

## 🚀 Features

- **Free AI Models**: Uses HuggingFace transformers (no API costs)
- **Business Context**: Configurable topics and restrictions
- **Memory**: Conversation history tracking
- **Production Ready**: Docker containerized, health checks, logging
- **Easy Deployment**: One-click Railway deployment
- **Fast**: Async FastAPI with optimized inference

## 🏗 Architecture

```
Frontend (Next.js) → FastAPI → HuggingFace Model → Response
                              ↕
                         Conversation Memory
```

## 📦 Quick Start

### Local Development

1. **Clone and setup**:
```bash
git clone <your-repo>
cd ai-chatbot-api
pip install -r requirements.txt
```

2. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your business details
```

3. **Run locally**:
```bash
uvicorn app.main:app --reload
```

4. **Test the API**:
- Visit: http://localhost:8000/docs
- Try the `/api/v1/test` endpoint

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
ALLOWED_TOPICS=topic1,topic2,topic3
RESTRICTED_TOPICS=medical advice,legal advice
ENVIRONMENT=production
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

### Business Settings
Customize your bot by setting environment variables:

```bash
# Business Identity
BUSINESS_NAME="Acme Plumbing"
BUSINESS_TYPE="plumbing service company"

# What the bot can discuss
ALLOWED_TOPICS="drain cleaning,pipe repair,water heaters,pricing,scheduling"

# What the bot should avoid  
RESTRICTED_TOPICS="medical advice,legal advice,electrical work"
```

### Model Settings
```bash
# Use smaller model for faster responses (good for Railway)
MODEL_NAME="microsoft/DialoGPT-small"

# Use larger model for better quality (needs more memory)
MODEL_NAME="microsoft/DialoGPT-medium"
```

## 💡 Frontend Integration

### Next.js Example
```javascript
// pages/api/chat.js
export default async function handler(req, res) {
  const response = await fetch('https://your-railway-app.railway.app/api/v1/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(req.body)
  });
  
  const data = await response.json();
  res.json(data);
}

// components/ChatBot.jsx
const sendMessage = async (message) => {
  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message })
  });
  return response.json();
};
```

### React Component
```javascript
import { useState } from 'react';

function ChatBot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  
  const sendMessage = async () => {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        message: input,
        conversation_history: messages 
      })
    });
    
    const data = await response.json();
    setMessages([...messages, 
      { role: 'user', content: input },
      { role: 'assistant', content: data.response }
    ]);
    setInput('');
  };

  return (
    <div>
      {/* Your chat UI */}
    </div>
  );
}
```

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

### Phase 1 (Current)
- ✅ Core chat functionality
- ✅ Business context restrictions
- ✅ Railway deployment
- ✅ Conversation memory

### Phase 2 (Next)
- [ ] Database persistence (PostgreSQL)
- [ ] User authentication
- [ ] Multiple business tenants
- [ ] Analytics dashboard

### Phase 3 (Future)
- [ ] Custom model fine-tuning
- [ ] Integration with external tools
- [ ] Multi-language support
- [ ] Voice interface

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