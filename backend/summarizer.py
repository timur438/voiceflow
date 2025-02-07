from llama_cpp import Llama

class TranscriptSummarizer:
    def __init__(self, model_path="models/mistral-7b-instruct-v0.2.Q4_K_M.gguf"):
        """Initialize the summarizer with a local GGUF model"""
        self.llm = Llama(
            model_path=model_path,
            n_ctx=8192,  # Контекстное окно
            n_gpu_layers=-1  # Использовать GPU где возможно
        )

    def _create_prompt(self, transcript, prompt_type="summary"):
        """Create a prompt for the summarization or HR interview"""
        if prompt_type == "summary":
            prompt_template = """Below is a transcript of a meeting. Please provide:
1. A brief summary (2-3 paragraphs)
2. Key topics discussed (bullet points)
3. Main decisions and action items
4. Important follow-ups

Transcript:
{transcript}

Response:"""
        elif prompt_type == "hr_interview":
            prompt_template = """Below is a transcript of an HR interview. Please provide:
1. Key insights about the candidate's skills and experience
2. Behavioral traits observed during the interview
3. Recommendations for the next steps in the hiring process

Transcript:
{transcript}

Response:"""
        
        return prompt_template.format(transcript=transcript)

    def generate_summary(self, transcript, prompt_type="summary", temperature=0.7, max_tokens=1024):
        """Generate a summary or HR interview analysis from the transcript"""
        prompt = self._create_prompt(transcript, prompt_type)
        
        response = self.llm(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            stop=["</s>", "Transcript:"],
        )
        
        return response['choices'][0]['text'].strip()