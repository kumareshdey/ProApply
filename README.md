# ProApply - AI Powered JD Based Resume \& Cover Letter Generator

An AI-powered application that helps you create and customize resumes and cover letters optimized for specific job descriptions.

## Features

- Resume generation from uploaded PDF resumes
- Cover letter generation based on job descriptions
- Real-time resume and cover letter modifications
- PDF export functionality
- Vector-based information storage for better context retrieval

## Tech Stack

- **Backend**: FastAPI, Python
- **AI/ML**: GROQ API, Sentence Transformers
- **Database**: ChromaDB (Vector Database)
- **Document Processing**: LaTeX, PyPDF2

## Setup

1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Create a `creds.py` file in the backend directory with your GROQ API key:
```python
GROQ_API_KEY = "your-api-key-here"
```

3. Start the server:
```bash
python api.py
```

## API Endpoints

- `POST /store_informations/`: Upload resume text or PDF
- `POST /generate_resume/`: Generate LaTeX resume from job description
- `POST /modification_resume/`: Modify existing resume
- `POST /generate_application_message/`: Generate cover letter
- `POST /modification_cover_letter/`: Modify existing cover letter
- `POST /download_resume_in_pdf/`: Convert LaTeX to PDF

## Project Structure

```
ProApply/
├── backend/
│   ├── api.py           # FastAPI endpoints
│   ├── service.py       # Business logic
│   ├── adapter.py       # External service integrations
│   └── assets/          # Templates and resources
└── README.md
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
