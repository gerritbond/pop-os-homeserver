# PopOS Home Server - AI/LLM Stack

A Docker-based home server setup for running local Large Language Models (LLMs) with a web interface and vector database for RAG (Retrieval-Augmented Generation) capabilities.

## 🏗️ Architecture

This setup provides a complete AI/LLM stack with the following components:

- **Open WebUI**: Modern web interface for chatting with LLMs
- **Weaviate**: Vector database with multimodal support for RAG applications
- **Document Processor**: Optional service for ingesting and processing documents
- **MCP**: Model Control Point for interfacing with external LLM services

## 🚀 Quick Start

### Prerequisites

- PopOS (or any Linux distribution)
- Docker and Docker Compose installed
- Git installed
- At least 8GB RAM (16GB+ recommended for larger models)
- Sufficient storage space for models and data

### Installation

1. Clone this repository:
   ```bash
   git clone <your-repo-url>
   cd popos-homeserver
   ```

2. Start the services:
   ```bash
   docker compose up -d
   ```

3. Access the services:
   - **Open WebUI**: http://localhost:3000
   - **Weaviate Console**: http://localhost:8080/v1/console
   - **MCP API**: http://localhost:5000

---

### Open WebUI (Port 3000)
- Modern, responsive web interface for LLM interactions
- Supports multiple models and conversations
- User authentication and role management
- File upload and document processing capabilities

### MCP (Port 5000)
- FastAPI-based service for interfacing with Open WebUI and external LLMs
- Example `/chat` endpoint for forwarding chat requests
- Easily extensible for more advanced control and orchestration

### Weaviate (Port 8080)
- Vector database with native multimodal support
- GraphQL API for complex queries
- Built-in modules for text and image embeddings
- Supports text, images, and other data types

**Key Features:**
- `text2vec-openai`: OpenAI text embeddings
- `text2vec-huggingface`: HuggingFace text embeddings
- `img2vec-neural`: Neural image embeddings
- `multi2vec-clip`: CLIP multimodal embeddings
- `multi2vec-bind`: BIND multimodal embeddings

## 🔧 Configuration

### Environment Variables

Update the following in `docker-compose.yml`:

```yaml
# Open WebUI
- WEBUI_SECRET_KEY=your-secure-secret-key-here

# Weaviate
- ENABLE_MODULES=text2vec-openai,text2vec-cohere,text2vec-huggingface,ref2vec-centroid,generative-openai,qna-openai,img2vec-neural,multi2vec-clip,multi2vec-bind
```

### Model Configuration

Create a `.env` file for model-specific settings (optional):

```env
WEAVIATE_TEXT2VEC_MODULE=text2vec-huggingface
WEAVIATE_IMG2VEC_MODULE=img2vec-neural
```

## 📚 Next Steps & Enhancements

### 1. Model Management
- **Connect to External LLMs**: Use MCP to interface with Ollama or other LLM servers
- **Model Optimization**: Configure model parameters for better performance
- **Model Switching**: Set up automatic model switching based on task type

### 2. RAG Implementation
- **Document Ingestion**: Set up automated document processing pipeline
- **Vector Indexing**: Create efficient vector indexes for your data
- **Query Optimization**: Implement semantic search and retrieval

### 3. Security & Access
- **Reverse Proxy**: Set up Nginx or Traefik for secure external access
- **SSL/TLS**: Configure HTTPS with Let's Encrypt
- **Authentication**: Implement proper user authentication and authorization
- **Network Security**: Configure firewall rules and VPN access

### 4. Monitoring & Logging
- **Prometheus/Grafana**: Set up monitoring for system resources
- **ELK Stack**: Implement centralized logging
- **Health Checks**: Add container health monitoring
- **Backup Strategy**: Implement automated backups for data and models

### 5. Performance Optimization
- **GPU Acceleration**: Configure CUDA support for faster inference
- **Model Quantization**: Use quantized models for reduced memory usage
- **Load Balancing**: Set up multiple LLM instances for high availability
- **Caching**: Implement response caching for common queries

### 6. Integration & Automation
- **API Gateway**: Create a unified API for all services
- **Webhook Support**: Set up webhooks for external integrations
- **Scheduled Tasks**: Implement automated model updates and maintenance
- **CI/CD Pipeline**: Set up automated deployment and testing

### 7. Advanced Features
- **Multi-modal Support**: Implement image and document understanding
- **Conversation Memory**: Add persistent conversation history
- **Custom Functions**: Implement custom tools and functions
- **Streaming Responses**: Enable real-time response streaming

## 🛠️ Development Setup

### Local Development
```bash
# Start services in development mode (if you create a dev compose file)
docker compose -f docker-compose.dev.yml up -d

# View logs
docker compose logs -f open-webui
docker compose logs -f weaviate
```

### API Documentation
- **Open WebUI API**: (see project docs)
- **Weaviate API**: https://weaviate.io/developers/weaviate/api
- **MCP API**: see `mcp/app/main.py` for example endpoints

## 📊 Resource Requirements

### Minimum Requirements
- **RAM**: 8GB (16GB+ recommended)
- **Storage**: 50GB+ for models and data
- **CPU**: 4 cores recommended
- **GPU**: Optional but recommended for faster inference

### Recommended Setup
- **RAM**: 32GB+
- **Storage**: 500GB+ SSD
- **CPU**: 8+ cores
- **GPU**: NVIDIA RTX 3060+ with CUDA support

## 🔍 Troubleshooting

### Common Issues

1. **Out of Memory Errors**
   - Reduce model size or use quantized models
   - Increase system RAM or add swap space
   - Use model offloading techniques

2. **Slow Response Times**
   - Enable GPU acceleration
   - Use quantized models
   - Optimize vector database queries
   - Implement caching

3. **Service Connection Issues**
   - Check container status: `docker compose ps`
   - View logs: `docker compose logs <service-name>`
   - Verify network connectivity: `docker network ls`

### Useful Commands
```bash
# Check service status
docker compose ps

# View logs
docker compose logs -f

# Restart services
docker compose restart

# Update images
docker compose pull
docker compose up -d

# Clean up
docker compose down -v
docker system prune -a
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Open WebUI](https://github.com/open-webui/open-webui) - Modern web interface
- [Weaviate](https://weaviate.io/) - Vector database
- [PopOS](https://pop.system76.com/) - Linux distribution

---

**Note**: This setup is designed for personal/home use. For production deployments, additional security, monitoring, and scaling considerations should be implemented.