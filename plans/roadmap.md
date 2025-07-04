# HayaNG MVP Product Roadmap - Phase 1

## 🎯 Core MVP Flow
1. **Create Job Posting** (Title + Job Description)
2. **Auto-Generate Google Form** for applications
3. **Auto-Create Google Sheet** linked to the form
4. **Auto-Post to Twitter** with job details
5. **Match Candidates** from:
   - Existing talent pool
   - Form application responses

---

## 🚀 MVP Goals
- **Automate job posting workflow** from creation to Twitter
- **Streamline application collection** via Google Forms/Sheets
- **Intelligent candidate matching** using AI from both talent sources
- **Reduce manual work** for recruiters

---

## 📅 4-Week Sprint Plan

### Week 1: Job Posting Creation
**Goal:** Create and store job postings

#### Core Features
- [ ] **Job Creation Form**
  - Simple form: Title + Job Description
  - Save job to database
  - Basic admin interface to view/edit jobs

#### Success Metrics
- Create 5+ job posts
- Form works without errors
- Jobs stored in database correctly

### Week 2: Google Forms & Sheets Integration
**Goal:** Auto-generate Google Form and Sheet for each job

#### Core Features
- [ ] **Google Form Generation**
  - Auto-create Google Form when job is created
  - Basic questions: Name, Email, Resume upload
  - Store form ID/URL in database

- [ ] **Google Sheet Creation**
  - Auto-create Google Sheet linked to form
  - Store sheet ID/URL in database
  - Form responses automatically populate sheet

#### Success Metrics
- Form created successfully for each job
- Sheet created and linked to form
- Responses flow from form to sheet

### Week 3: Twitter Integration
**Goal:** Auto-post job to Twitter after creation

#### Core Features
- [ ] **Twitter Posting**
  - Auto-tweet when job is published
  - Tweet format: Job title + brief description + form link
  - Store tweet ID in database

#### Success Metrics
- Job automatically posted to Twitter
- Tweet contains job details and form link
- No errors in posting process

### Week 4: Candidate Matching
**Goal:** Match candidates from talent pool and form responses

#### Core Features
- [ ] **Talent Pool Matching**
  - Match existing talent pool candidates to job posting
  - Use AI to rank candidates by fit
  - Display top matches with scores

- [ ] **Form Response Matching**
  - Fetch responses from Google Sheet
  - Match form applicants to job posting
  - Rank all candidates (talent pool + form responses)

- [ ] **Shortlisting Interface**
  - View ranked candidates from both sources
  - Mark candidates as shortlisted/rejected
  - Basic candidate profiles

#### Success Metrics
- Successfully match candidates from both sources
- Display ranked list of candidates
- Allow shortlisting functionality

---

## ✅ MVP Success Criteria

### Core Functionality Working
- [ ] Create job posting with title and description
- [ ] Auto-generate Google Form for each job
- [ ] Auto-create Google Sheet linked to form
- [ ] Auto-post job to Twitter
- [ ] Match candidates from talent pool
- [ ] Match candidates from form responses
- [ ] Display ranked candidate list
- [ ] Allow shortlisting candidates

### Basic Metrics
- Create 3+ job posts end-to-end
- Generate 10+ form applications
- Successfully match candidates from both sources
- Complete workflow works without manual intervention

---

## 🚀 Technical Requirements

### Minimum Features Needed
- Simple job creation form
- Google Forms API integration
- Google Sheets API integration
- Twitter API integration
- Basic AI matching using embeddings
- Simple admin interface to view matches

### Success Definition
The MVP is successful if you can:
1. Create a job posting
2. See it automatically create a Google Form
3. See it automatically create a Google Sheet
4. See it automatically post to Twitter
5. See matched candidates from existing talent pool
6. See matched candidates from form responses
7. Shortlist candidates you want to interview

This is a focused MVP that solves the core problem of automating job posting and candidate matching.
