from django.core.management.base import BaseCommand
from openai_client.client import OpenAPIClient
from postings.job_services import cosine_similarity
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Test OpenAI embeddings functionality'

    def add_arguments(self, parser):
        parser.add_argument(
            '--test-similarity',
            action='store_true',
            help='Test similarity between job descriptions and candidate profiles',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🧪 Testing OpenAI Embeddings')
        )
        
        if options['test_similarity']:
            self.test_similarity()
        else:
            self.test_basic_embeddings()
            self.test_similarity()

    def test_basic_embeddings(self):
        """Test basic embedding functionality"""
        self.stdout.write("\n🔧 Testing Basic Embeddings...")
        
        test_texts = [
            "Software Engineer with Python and Django experience",
            "Frontend Developer skilled in React and JavaScript",
            "Data Scientist proficient in machine learning and Python",
            "Senior Backend Developer with 5+ years experience",
            ""  # Empty text test
        ]
        
        for i, text in enumerate(test_texts):
            try:
                self.stdout.write(f"  📝 Text {i+1}: {text[:50]}...")
                embedding = OpenAPIClient.get_embedding(text)
                
                if embedding:
                    self.stdout.write(f"    ✅ Embedding generated: {len(embedding)} dimensions")
                    self.stdout.write(f"    📊 Sample values: {embedding[:3]}")
                else:
                    self.stdout.write(f"    ❌ No embedding generated")
                    
            except Exception as e:
                self.stdout.write(f"    ❌ Error: {str(e)}")

    def test_similarity(self):
        """Test similarity calculations between job and candidate profiles"""
        self.stdout.write("\n🎯 Testing Similarity Calculations...")
        
        # Test job description
        job_description = """
        We are looking for a Senior Python Developer to join our team.
        
        Requirements:
        - 5+ years of Python development experience
        - Strong experience with Django and Flask frameworks
        - Knowledge of REST APIs and microservices
        - Experience with PostgreSQL and Redis
        - Familiar with Docker and AWS
        - Strong problem-solving skills
        
        Responsibilities:
        - Develop and maintain web applications
        - Design and implement REST APIs
        - Optimize database performance
        - Collaborate with frontend teams
        - Code review and mentoring
        """
        
        # Test candidate profiles
        candidates = [
            {
                "name": "Perfect Match",
                "profile": "Senior Python Developer with 6 years of experience. Expert in Django, Flask, REST APIs, PostgreSQL, Redis, Docker, and AWS. Strong problem-solving skills and experience with microservices architecture."
            },
            {
                "name": "Good Match",
                "profile": "Python Developer with 4 years of experience. Proficient in Django, REST APIs, and PostgreSQL. Some experience with Docker and cloud platforms."
            },
            {
                "name": "Partial Match",
                "profile": "Full-stack Developer with 3 years of experience. Strong in JavaScript and React, some Python experience with Django. Familiar with databases and APIs."
            },
            {
                "name": "Poor Match",
                "profile": "Java Developer with 8 years of experience. Expert in Spring Boot, Hibernate, and Oracle databases. No Python experience."
            }
        ]
        
        try:
            # Get job embedding
            self.stdout.write("  📋 Generating job embedding...")
            job_embedding = OpenAPIClient.get_embedding(job_description)
            
            if not job_embedding:
                self.stdout.write("    ❌ Failed to generate job embedding")
                return
            
            self.stdout.write(f"    ✅ Job embedding generated: {len(job_embedding)} dimensions")
            
            # Test each candidate
            self.stdout.write("\n  👥 Testing candidate matches:")
            
            similarities = []
            for candidate in candidates:
                try:
                    # Get candidate embedding
                    candidate_embedding = OpenAPIClient.get_embedding(candidate["profile"])
                    
                    if not candidate_embedding:
                        self.stdout.write(f"    ❌ Failed to generate embedding for {candidate['name']}")
                        continue
                    
                    # Calculate similarity
                    similarity = cosine_similarity(job_embedding, candidate_embedding)
                    similarities.append((candidate["name"], similarity))
                    
                    # Color code based on similarity
                    if similarity > 0.8:
                        color = self.style.SUCCESS
                    elif similarity > 0.6:
                        color = self.style.WARNING
                    else:
                        color = self.style.ERROR
                    
                    message = f"{candidate['name']}: {similarity:.3f}"
                    self.stdout.write(f"    {color(message)}")
                    
                except Exception as e:
                    self.stdout.write(f"    ❌ Error testing {candidate['name']}: {str(e)}")
            
            # Sort by similarity
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            self.stdout.write("\n  🏆 Ranking:")
            for rank, (name, similarity) in enumerate(similarities, 1):
                self.stdout.write(f"    {rank}. {name}: {similarity:.3f}")
            
            # Validate ranking makes sense
            if len(similarities) >= 2:
                if similarities[0][0] == "Perfect Match":
                    self.stdout.write(
                        self.style.SUCCESS("\n  ✅ Ranking looks correct - Perfect Match is #1!")
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f"\n  ⚠️  Unexpected ranking - {similarities[0][0]} is #1")
                    )
            
        except Exception as e:
            self.stdout.write(f"    ❌ Error in similarity testing: {str(e)}")
            logger.error(f"Error in similarity testing: {str(e)}", exc_info=True)

    def test_edge_cases(self):
        """Test edge cases and error handling"""
        self.stdout.write("\n🔍 Testing Edge Cases...")
        
        edge_cases = [
            "",  # Empty string
            "   ",  # Whitespace only
            "a",  # Single character
            "Hello world",  # Simple text
            "🚀 Emojis and special characters! @#$%^&*()",  # Special characters
            "Very long text " * 100,  # Very long text
        ]
        
        for i, text in enumerate(edge_cases):
            try:
                self.stdout.write(f"  📝 Edge case {i+1}: {repr(text[:50])}")
                embedding = OpenAPIClient.get_embedding(text)
                
                if embedding and len(embedding) > 0:
                    self.stdout.write(f"    ✅ Handled successfully: {len(embedding)} dimensions")
                else:
                    self.stdout.write(f"    ⚠️  Empty embedding returned")
                    
            except Exception as e:
                self.stdout.write(f"    ❌ Error: {str(e)}") 