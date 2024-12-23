import google.generativeai as genai
import os
from datetime import datetime, timedelta
import time
import json
import random
import string
import re
from typing import List, Dict, Tuple, Optional
import argparse
import logging
import sys
from dataclasses import dataclass

@dataclass
class EmailConfig:
    """Configuration for email generation"""
    min_word_count: int = 50
    max_word_count: int = 1000
    min_emails: int = 1
    max_emails: int = 100
    rate_limit_delay: int = 1  # seconds between API calls

class TestEmailMetadata:
    """Generates and manages test email metadata"""
    
    def __init__(self):
        self.domains = ['testcompany.com', 'testing.org', 'qamail.net', 'unittest.io']
        self.departments = ['qa', 'test', 'dev', 'support', 'sales', 'marketing']
        
    def generate_email(self) -> str:
        name = ''.join(random.choices(string.ascii_lowercase, k=8))
        department = random.choice(self.departments)
        domain = random.choice(self.domains)
        return f"{name}.{department}@{domain}"
    
    def generate_timestamp(self) -> str:
        now = datetime.now()
        days_ago = random.randint(0, 7)
        hours_ago = random.randint(0, 23)
        minutes_ago = random.randint(0, 59)
        
        timestamp = now - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)
        return timestamp.strftime("%Y-%m-%d %H:%M:%S")

class TestEmailGenerator:
    def __init__(self, api_key: str):
        self._setup_logging()
        self.logger = logging.getLogger(__name__)
        
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.metadata = TestEmailMetadata()
        except Exception as e:
            self.logger.error(f"Failed to initialize Gemini AI: {str(e)}")
            raise

        # Plain text test disclaimer with borders
        self.test_disclaimer = """
+==================================================+
|            THIS IS A TEST EMAIL                   |
|            DO NOT REPLY OR TAKE ACTION            |
+==================================================+
Test Email ID: {test_id}
Generated on: {timestamp}
This email was automatically generated for testing purposes.
Any resemblance to real emails or situations is purely coincidental.
+==================================================+
"""

    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler('email_generation.log')
            ]
        )

    def generate_test_id(self) -> str:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"TEST-{timestamp}-{random_suffix}"

    def generate_prompt(self, word_count: int, email_number: int, test_id: str) -> str:
        email_types = [
            ("Internal Memo", "Team update regarding unexpected facts"),
            ("Bug Report", "Strange behavior observation"),
            ("Newsletter", "Weekly Random Facts Digest"),
            ("Meeting Minutes", "Unusual discoveries discussion"),
            ("Project Update", "Interesting findings report"),
            ("Survey Results", "Unexpected data patterns")
        ]
        
        email_type, subject_context = random.choice(email_types)
        from_email = self.metadata.generate_email()
        to_email = self.metadata.generate_email()
        timestamp = self.metadata.generate_timestamp()
        
        priority_levels = ['', '[High Priority]', '[Low Priority]', '[Urgent]']
        priority = random.choice(priority_levels)
        
        # Updated prompt to generate plain text formatting
        return f"""Generate a test email using only plain text (no markdown) with this exact structure:

                    1. Start with these exact headers:
                    From: {from_email}
                    To: {to_email}
                    Date: {timestamp}
                    Subject: [TEST] {priority} {subject_context} - {test_id}

                    2. Then add this exact disclaimer:
                    {self.test_disclaimer.format(test_id=test_id, timestamp=timestamp)}

                    3. Email Content Requirements:
                    - Format as a {email_type}
                    - Word count: approximately {word_count} words
                    - Include 3-4 random, unsettling, and true psychological insights or facts about society and the dark corners of society
                    - Make content provocative, reflective, and slightly unsettling (this is test email #{email_number})
                    - Use plain text formatting (no markdown)

                    4. Include these sections with plain text formatting:
                    - A clear introduction that questions the reader's assumptions about society
                    - Main content featuring random psychological insights or dark truths, woven into a narrative
                    - A simple ASCII table if needed (e.g., human emotion and irrationality comparisons)
                    - A "Next Steps" or "Reflective Questions" section that encourages introspection or action
                    - A signature block with an enigmatic or thought-provoking statement

                    5. Optional elements to randomly include:
                    - Thread history markers (use > for quoted text)
                    - References to fictitious attachments (e.g., [Attachment: human_condition.pdf])
                    - Priority indicators that imply urgency for existential questions
                    - Department tags suggesting a connection to the unknown or unexplainable

                    6. Formatting Guidelines:
                    - Use plain text characters for emphasis (*, _, =)
                    - Use ASCII characters for tables and borders
                    - Use standard email quoting for threads (>)
                    - Separate sections with blank lines
                    - Use simple bullet points (* or -)

                    7. Tone Guidelines:
                    - Evoke curiosity and discomfort simultaneously
                    - Blend scientific accuracy with a narrative touch
                    - Conclude with a subtle invitation to explore deeper questions about human existence and choices

                    Format everything as plain text that would be readable in any email client."""

    async def validate_email_content(self, content: str, test_id: str) -> Tuple[bool, Optional[str]]:
        if not content:
            return False, "Empty content"
            
        checks = [
            (test_id in content, "Missing test ID"),
            ("THIS IS A TEST EMAIL" in content, "Missing test disclaimer"),
            (len(content.split()) >= 50, "Content too short"),
            ("From:" in content and "To:" in content, "Missing email headers"),
            ("[TEST]" in content, "Missing [TEST] in subject"),
            ("===" in content, "Missing formatting elements")
        ]
        
        for check, error in checks:
            if not check:
                return False, error
                
        return True, None

    async def generate_single_email(self, word_count: int, email_number: int) -> Dict:
        test_id = self.generate_test_id()
        
        try:
            prompt = self.generate_prompt(word_count, email_number, test_id)
            response = await self.model.generate_content_async(prompt)
            content = response.text
            
            is_valid, error = await self.validate_email_content(content, test_id)
            if not is_valid:
                raise ValueError(f"Generated content validation failed: {error}")
            
            return {
                "email_number": email_number,
                "test_id": test_id,
                "content": content,
                "timestamp": datetime.now().isoformat(),
                "status": "success"
            }
        except Exception as e:
            self.logger.error(f"Failed to generate email #{email_number}: {str(e)}")
            return {
                "email_number": email_number,
                "test_id": test_id,
                "content": None,
                "timestamp": datetime.now().isoformat(),
                "status": "failed",
                "error": str(e)
            }

    async def generate_bulk_emails(self, word_count: int, num_emails: int, 
                                 output_dir: str = "test_emails") -> List[Dict]:
        self.logger.info(f"Starting bulk generation of {num_emails} test emails")
        os.makedirs(output_dir, exist_ok=True)
        results = []
        
        batch_id = f"BATCH-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        for i in range(1, num_emails + 1):
            self.logger.info(f"Generating test email {i}/{num_emails}")
            
            result = await self.generate_single_email(word_count, i)
            results.append(result)
            
            if result["status"] == "success":
                filename = f"test_email_{result['test_id']}.txt"
                file_path = os.path.join(output_dir, filename)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(result["content"])
                self.logger.info(f"Saved email to {file_path}")
            
            if i < num_emails:
                time.sleep(EmailConfig.rate_limit_delay)
        
        report = {
            "batch_id": batch_id,
            "generation_time": datetime.now().isoformat(),
            "configuration": {
                "word_count": word_count,
                "num_emails": num_emails,
                "output_directory": output_dir
            },
            "statistics": {
                "successful_generations": sum(1 for r in results if r["status"] == "success"),
                "failed_generations": sum(1 for r in results if r["status"] == "failed"),
                "average_word_count": sum(len(r["content"].split()) if r["content"] else 0 
                                        for r in results) / len(results)
            },
            "results": results
        }
        
        report_path = os.path.join(output_dir, f"generation_report_{batch_id}.json")
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        self.logger.info(f"Generation complete. Report saved to {report_path}")
        return results

def main():
    parser = argparse.ArgumentParser(description="Generate test emails with random facts using Gemini AI")
    parser.add_argument("--api-key", required=True, help="Gemini API key")
    parser.add_argument("--word-count", type=int, default=200, help="Word count limit for each email")
    parser.add_argument("--num-emails", type=int, required=True, help="Number of emails to generate")
    parser.add_argument("--output-dir", default="test_emails", help="Output directory for emails")
    
    args = parser.parse_args()
    
    if not (EmailConfig.min_word_count <= args.word_count <= EmailConfig.max_word_count):
        print(f"Error: Word count must be between {EmailConfig.min_word_count} and {EmailConfig.max_word_count}")
        return
        
    if not (EmailConfig.min_emails <= args.num_emails <= EmailConfig.max_emails):
        print(f"Error: Number of emails must be between {EmailConfig.min_emails} and {EmailConfig.max_emails}")
        return
    
    try:
        generator = TestEmailGenerator(args.api_key)
        import asyncio
        results = asyncio.run(generator.generate_bulk_emails(
            args.word_count,
            args.num_emails,
            args.output_dir
        ))
        
        successful = sum(1 for r in results if r["status"] == "success")
        print("\n=== Generation Summary ===")
        print(f"Successfully generated: {successful}/{args.num_emails} test emails")
        print(f"Failed generations: {len(results) - successful}")
        print(f"Output directory: {args.output_dir}")
        print("========================")
        
    except Exception as e:
        print(f"Error during email generation: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
# python egen.py --api-key YOUR_API_KEY --word-count 150 --num-emails 10 --output-dir test_emails
