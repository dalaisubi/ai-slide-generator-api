# AI Slide Generator API

AI-powered slide generator backend with customizable layouts and PPTX export built using FastAPI.

## Features and Future Scopes

- 🤖 **Multiple AI Providers**: Support for OpenAI and Google Gemini
- 📊 **Slide Generation**: Generate presentation slides on any topic
- 📄 **PowerPoint Export**: Export slides to .pptx format
- 🎨 **Customizable**: Support for different slide layouts and themes
- 📝 **Citations**: Automatic citation and reference generation
- 🔄 **Adapter Pattern**: Easy to add new AI providers

## Quick Start

### Prerequisites

- Python 3.8+
- pip or pipenv

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-slide-generator-api
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

### Interactive Documentation

FastAPI provides automatic interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### API Endpoints

#### 1. Generate Slides
```bash
POST /api/v1/slides/generate
```

Generate presentation slides using AI.

**Request:**
```json
{
  "topic": "Python Programming",
  "num_slides": 5
}
```

**Response:**
```json
{
  "request_id": "uuid",
  "status": "success",
  "message": "Successfully generated 5 slides...",
  "data": {
    "title": "Python Programming",
    "slides": [...]
  },
  "num_slides": 5,
  "timestamp": "2024-01-01T12:00:00"
}
```

#### 2. Export Slides
```bash
POST /api/v1/slides/export
```

Export slides to PowerPoint format.

**Request:**
```json
{
  "title": "My Presentation",
  "slides": [
    {
      "title": "Slide Title",
      "bullets": ["Point 1", "Point 2"],
      "citation": "Source"
    }
  ]
}
```

#### 3. Download File
```bash
GET /api/v1/slides/download/{file_name}
```

Download generated PowerPoint file.

### Complete Documentation
Coming Soon


## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LLM_PROVIDER` | AI provider (`openai`, `gemini`, `mock`) | `mock` |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `OPENAI_MODEL` | OpenAI model name | `gpt-3.5-turbo` |
| `GEMINI_API_KEY` | Google Gemini API key | - |
| `GEMINI_MODEL` | Gemini model name | `gemini-1.5-flash` |

## Project Structure

```
ai-slide-generator-api/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── routes/
│   │           └── slides.py      # API routes
│   ├── models/
│   │   └── request_response_models.py  # Pydantic models
│   ├── services/
│   │   ├── llm/                    # LLM adapters
│   │   │   ├── base.py
│   │   │   ├── openai_adapter.py
│   │   │   ├── gemini_adapter.py
│   │   │   └── mock_adapter.py
│   │   ├── llm_service.py          # LLM service
│   │   └── pptx_service.py         # PowerPoint generation
│   ├── main.py                     # FastAPI app
│   └── settings.py                 # Configuration
├── API.md                          # API documentation
├── postman_collection.json         # Postman collection
├── requirements.txt                # Dependencies
└── README.md                       # This file
```

## Usage Examples

### Generate and Export Workflow

1. **Generate slides:**
```bash
curl -X POST "http://localhost:8000/api/v1/slides/generate" \
  -H "Content-Type: application/json" \
  -d '{"topic": "Machine Learning", "num_slides": 5}'
```

2. **Export to PowerPoint:**
Use the `data` field from the generate response in the export request.

3. **Download file:**
```bash
curl -X GET "http://localhost:8000/api/v1/slides/download/{file_name}" \
  --output presentation.pptx
```

## Development

### Adding New AI Providers

The project uses the Adapter pattern for easy extensibility:

1. Create a new adapter in `app/services/llm/`:
```python
from app.services.llm.base import LLMAdapter

class NewProviderAdapter(LLMAdapter):
    async def generate_slides(self, topic: str, num_slides: int):
        # Implementation
        pass
```

2. Update `app/services/llm/factory.py` to include the new provider.

3. Add configuration in `app/settings.py`.

## Testing

The API includes interactive documentation at `/docs` for testing endpoints directly in the browser.

## License

See [LICENSE](./LICENSE) file.

## Sample Outputs

Sample PowerPoint presentations are available in the `samples/` directory (if provided).

---

**TBD**: additional features like authentication, rate limiting, and error handling improvements.