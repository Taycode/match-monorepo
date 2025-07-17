# HayaNG MVP Technical Architecture - Phase 1

## 🎯 Core MVP Workflow
```
Job Creation → Google Form → Google Sheet → Twitter Post → Candidate Matching
     ↓              ↓             ↓             ↓              ↓
  Save to DB    Form API      Sheet API     Twitter API    AI Matching
```

## 🏗️ Simple Architecture

### Technology Stack
- **Frontend**: React + TypeScript + Vite (already setup)
- **Backend**: Django + PostgreSQL
- **Vector Database**: Pinecone (for candidate matching)
- **AI**: OpenAI text-embedding-3-small + GPT-4
- **External APIs**: Google Forms API, Google Sheets API, Twitter API v2

### Core Flow
1. User creates job (title + description)
2. Backend stores job in database
3. Backend calls Google Forms API to create form
4. Backend calls Google Sheets API to create sheet
5. Backend calls Twitter API to post job
6. Backend matches candidates using AI embeddings
7. Frontend displays matched candidates

---

## 🗂️ Simple Database Schema

### Core Tables (Minimum Required)
```sql
-- Job postings
CREATE TABLE jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    google_form_id VARCHAR(255),
    google_form_url VARCHAR(500),
    google_sheet_id VARCHAR(255),
    google_sheet_url VARCHAR(500),
    twitter_post_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Existing talent pool (you already have this)
CREATE TABLE talents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    resume_url VARCHAR(500),
    skills JSONB,
    experience_years INTEGER,
    parsed_role VARCHAR(255),
    vector_id VARCHAR(255), -- Pinecone vector ID
    created_at TIMESTAMP DEFAULT NOW()
);

-- Form responses (fetched from Google Sheets)
CREATE TABLE form_responses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id UUID REFERENCES jobs(id),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    resume_url VARCHAR(500),
    response_data JSONB, -- Store all form data
    vector_id VARCHAR(255), -- Pinecone vector ID
    created_at TIMESTAMP DEFAULT NOW()
);

-- Candidate matches
CREATE TABLE matches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id UUID REFERENCES jobs(id),
    candidate_id UUID NOT NULL,
    candidate_type VARCHAR(50) CHECK (candidate_type IN ('talent', 'form_response')),
    similarity_score FLOAT,
    is_shortlisted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🔗 Core API Endpoints

### Job Management
```python
# Create and manage jobs
POST   /api/jobs/                           # Create job (triggers all automations)
GET    /api/jobs/                           # List all jobs
GET    /api/jobs/{id}/                      # Get specific job
```

### Candidate Matching
```python
# Get matched candidates
GET    /api/jobs/{id}/matches/              # Get all matches for a job
POST   /api/matches/{id}/shortlist/         # Shortlist a candidate
DELETE /api/matches/{id}/shortlist/         # Remove from shortlist
```

### Key Automation Flow
When `POST /api/jobs/` is called, the backend automatically:
1. Saves job to database
2. Creates Google Form
3. Creates Google Sheet
4. Posts to Twitter
5. Runs candidate matching
6. Returns job with all generated links
---

## 🧠 Simple Matching Logic

### Core Matching Process
```python
def match_candidates_for_job(job_id):
    job = Job.objects.get(id=job_id)
    
    # 1. Get job embedding
    job_embedding = get_embedding(job.title + " " + job.description)
    
    # 2. Match against talent pool
    talent_matches = match_talent_pool(job_embedding)
    
    # 3. Match against form responses
    form_matches = match_form_responses(job_id, job_embedding)
    
    # 4. Combine and rank all matches
    all_matches = talent_matches + form_matches
    ranked_matches = rank_matches(all_matches)
    
    # 5. Save to database
    save_matches_to_db(job_id, ranked_matches)
    
    return ranked_matches

def get_embedding(text):
    # Use OpenAI embedding API
    response = openai.Embedding.create(
        model="text-embedding-3-small",
        input=text
    )
    return response['data'][0]['embedding']
```

### Integration Flow
```python
# When job is created, this happens automatically:
def create_job_with_automations(title, description):
    # 1. Save job
    job = Job.objects.create(title=title, description=description)
    
    # 2. Create Google Form
    form_id, form_url = create_google_form(job)
    
    # 3. Create Google Sheet
    sheet_id, sheet_url = create_google_sheet(job, form_id)
    
    # 4. Post to Twitter
    tweet_id = post_to_twitter(job, form_url)
    
    # 5. Update job with generated links
    job.google_form_id = form_id
    job.google_form_url = form_url
    job.google_sheet_id = sheet_id
    job.google_sheet_url = sheet_url
    job.twitter_post_id = tweet_id
    job.save()
    
    # 6. Run matching
    matches = match_candidates_for_job(job.id)
    
    return job, matches
```

---

## 🔧 Environment Setup

### Required API Keys
```bash
# Add to environment variables
OPENAI_API_KEY=your-openai-key
PINECONE_API_KEY=your-pinecone-key
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
TWITTER_CONSUMER_KEY=your-twitter-consumer-key
TWITTER_CONSUMER_SECRET=your-twitter-consumer-secret
TWITTER_ACCESS_TOKEN=your-twitter-access-token
TWITTER_ACCESS_TOKEN_SECRET=your-twitter-access-token-secret
```

### Minimum Setup
1. Django backend with PostgreSQL
2. React frontend (already setup)
3. Pinecone vector database
4. OpenAI API access
5. Google Cloud API credentials
6. Twitter API credentials

This simplified architecture focuses on your core MVP requirements: automated job posting workflow with candidate matching from two sources.
