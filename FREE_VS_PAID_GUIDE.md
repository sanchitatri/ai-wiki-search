# 🆓 vs 💰 AI Wiki Search - Free vs Paid Guide

## 🎯 Overview

The AI Wiki Search system offers two versions to suit different needs and budgets:

- **🆓 FREE Version**: Uses local models, no API costs
- **💰 PAID Version**: Uses OpenAI's premium models for better quality

## 📊 Comparison Table

| Feature | 🆓 FREE Version | 💰 PAID Version |
|---------|----------------|-----------------|
| **Cost** | $0.00 | Uses OpenAI API |
| **Embeddings** | Sentence Transformers (local) | OpenAI text-embedding-ada-002 |
| **LLM** | Simple template-based responses | GPT-4 |
| **Setup** | No API keys needed | Requires OpenAI API key |
| **Quality** | Basic responses | High-quality, contextual answers |
| **Speed** | Fast (local processing) | Moderate (API calls) |
| **Offline** | ✅ Works offline | ❌ Requires internet |
| **Privacy** | ✅ Data stays local | ❌ Data sent to OpenAI |

## 🆓 FREE Version Details

### **What it includes:**
- **Local Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Simple Responses**: Template-based answer generation
- **No API Costs**: Everything runs locally
- **Fast Processing**: No network latency

### **Best for:**
- ✅ Testing and development
- ✅ Budget-conscious deployments
- ✅ Offline environments
- ✅ Privacy-sensitive data
- ✅ Learning and experimentation

### **Limitations:**
- ❌ Lower quality responses
- ❌ No advanced reasoning
- ❌ Limited context understanding
- ❌ Simple template-based answers

## 💰 PAID Version Details

### **What it includes:**
- **Premium Embeddings**: OpenAI text-embedding-ada-002
- **Advanced LLM**: GPT-4 for answer generation
- **High Quality**: Contextual, intelligent responses
- **Better Understanding**: Advanced reasoning capabilities

### **Best for:**
- ✅ Production deployments
- ✅ High-quality user experience
- ✅ Complex questions requiring reasoning
- ✅ Professional applications
- ✅ When budget allows for API costs

### **Requirements:**
- ❌ Requires OpenAI API key
- ❌ Internet connection needed
- ❌ API costs apply
- ❌ Data sent to external service

## 🚀 Quick Start

### 🆓 FREE Version Setup

```bash
# Switch to free version
python switch_version.py free
# or
./quick_switch.sh free

# Access the application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000/health
```

### 💰 PAID Version Setup

```bash
# Set your OpenAI API key
export OPENAI_API_KEY=your_key_here

# Switch to paid version
python switch_version.py paid
# or
./quick_switch.sh paid

# Access the application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000/health
```

## 🔄 Switching Between Versions

### Using Python Script

```bash
# Check current status
python switch_version.py status

# Switch to free version
python switch_version.py free

# Switch to paid version
python switch_version.py paid

# Stop all services
python switch_version.py stop
```

### Using Bash Script

```bash
# Check current status
./quick_switch.sh status

# Switch to free version
./quick_switch.sh free

# Switch to paid version
./quick_switch.sh paid

# Stop all services
./quick_switch.sh stop
```

## 💡 Decision Guide

### Choose 🆓 FREE Version if:
- You're just getting started
- Budget is a primary concern
- You need offline functionality
- Data privacy is critical
- You're testing or prototyping
- Response quality is acceptable at basic level

### Choose 💰 PAID Version if:
- You need high-quality responses
- User experience is paramount
- Budget allows for API costs
- You need advanced reasoning
- You're deploying to production
- Internet connectivity is reliable

## 🧪 Testing Both Versions

### Test Questions to Try:

1. **"What's our vacation policy?"**
2. **"How do I request time off?"**
3. **"What are the remote work guidelines?"**
4. **"How do I submit expense reports?"**
5. **"What's the process for performance reviews?"**

### Compare Results:

Try the same questions on both versions to see the difference in:
- Response quality
- Answer depth
- Context understanding
- Source citations

## 🔧 Technical Details

### 🆓 FREE Version Architecture:
```
User Question → Sentence Transformers → ChromaDB → Template Response
```

### 💰 PAID Version Architecture:
```
User Question → OpenAI Embeddings → ChromaDB → GPT-4 → Intelligent Response
```

## 💰 Cost Estimation (PAID Version)

### Typical Usage:
- **Small Team** (10 users): ~$5-20/month
- **Medium Team** (50 users): ~$25-100/month
- **Large Team** (200 users): ~$100-400/month

### Cost Factors:
- Number of questions asked
- Length of documents
- Complexity of queries
- OpenAI pricing changes

## 🛠️ Troubleshooting

### FREE Version Issues:
- **Slow startup**: First time downloads models (~100MB)
- **Memory usage**: Local models require RAM
- **Basic responses**: Expected behavior

### PAID Version Issues:
- **API key errors**: Check OPENAI_API_KEY environment variable
- **Rate limits**: OpenAI has usage limits
- **Network issues**: Requires internet connection
- **Cost concerns**: Monitor API usage

## 🎯 Recommendations

### For Development:
Start with the **FREE version** to test functionality, then upgrade to **PAID** for production.

### For Production:
Use the **PAID version** for better user experience, but keep **FREE version** as fallback.

### For Hybrid Approach:
Consider using **FREE version** for simple queries and **PAID version** for complex ones.

## 📞 Support

If you need help choosing or switching versions:
1. Check the current status: `python switch_version.py status`
2. Review this guide for decision criteria
3. Test both versions with your specific use case
4. Consider your budget and quality requirements

**Happy searching! 🔍**
