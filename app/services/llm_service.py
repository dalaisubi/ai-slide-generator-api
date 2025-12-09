async def generate_slide_content(topic: str, num_slides: int):
    """
    Mock LLM generator. Replace this with OpenAI/Llama/Gemini later.
    """
    slides = []
    for i in range(num_slides):
        slides.append({
            "title": f"{topic} - Slide {i+1}",
            "bullets": [
                f"Key idea {i+1}.1 about {topic}",
                f"Key idea {i+1}.2 about {topic}",
                f"Key idea {i+1}.3 about {topic}",
            ],
            "citation": "Generated using LLM (Mock)"
        })
    return slides