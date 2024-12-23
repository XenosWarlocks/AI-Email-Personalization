Here's a well-structured README file for your project:  

---

# Test Email Generator with Gemini AI  

This Python script generates customizable test emails using **Google Gemini AI**. The emails feature random psychological insights, unsettling facts, and plain text formatting. It is ideal for testing email clients, systems, or user behavior simulations.  

---

## Features  
- **Dynamic Test Emails**: Generates personalized emails with randomized content and psychological insights.  
- **Custom Word Counts**: Configure emails to include anywhere from 50 to 1,000 words.  
- **Bulk Generation**: Generate up to 100 emails per batch with rate-limiting for API safety.  
- **Plain Text Formatting**: Ensures compatibility with all email clients.  
- **Error Handling**: Validates generated content and logs issues.  
- **Email Metadata**: Includes dynamic "From," "To," timestamps, and priority levels.  
- **Detailed Reporting**: Creates JSON reports summarizing the email generation process.  

---

## Prerequisites  
1. **Python**: Install Python 3.8 or higher.  
2. **Gemini AI**: Obtain a valid API key from Google Generative AI services.  
3. **Dependencies**: Install the required libraries via pip.  

```bash
pip install google-generativeai
```  

---

## Usage  

### Command-Line Arguments  
| Argument        | Description                                       | Required/Default             |  
|------------------|---------------------------------------------------|------------------------------|  
| `--api-key`      | Your Gemini AI API key                            | **Required**                 |  
| `--word-count`   | Word count for each email                         | Default: 200 (Range: 50-1000)|  
| `--num-emails`   | Number of emails to generate                      | **Required** (1-100)         |  
| `--output-dir`   | Directory to save generated emails                | Default: `test_emails`       |  

### Example Command  
```bash
python email_generator.py --api-key YOUR_API_KEY --word-count 150 --num-emails 10 --output-dir test_email
```  

---

## Output  

### Email Files  
- Saved as `.txt` files in the specified output directory.  
- Each email includes:  
  - **Headers**: `From`, `To`, `Date`, `Subject`.  
  - **Test Disclaimer**: Explains the email's purpose and test nature.  
  - **Main Content**: Includes random unsettling facts and psychological insights.  

### Report File  
- A summary `.json` file containing:  
  - Batch statistics (success/failure counts, average word count).  
  - Detailed information for each generated email.  

---

## Customization  

### Configuration Parameters  
Modify default settings in `EmailConfig`:  
- **Rate Limit**: Set `rate_limit_delay` (in seconds) to control API call frequency.  
- **Word Count**: Adjust `min_word_count` and `max_word_count`.  

### Randomized Email Types  
The script randomly generates email types, such as:  
- Internal Memo  
- Bug Report  
- Meeting Minutes  
- Project Updates  

---

## Error Handling  
Validation checks ensure generated content meets requirements:  
- Test ID presence.  
- Proper headers (`From`, `To`, `Date`, `Subject`).  
- Minimum word count.  
- Disclaimer inclusion.  

If an email fails validation, it is logged, and the script continues with the next email.  

---

## Logging  
All operations are logged to `email_generation.log` for debugging and audit purposes.  

---

## Example Generated Email  

```
From: alex.dev@unittest.io  
To: taylor.qa@qamail.net  
Date: 2023-12-23 15:32:10  
Subject: [TEST] [Urgent] Bug Report - TEST-20231223153210-ABC123  

+==================================================+  
|            THIS IS A TEST EMAIL                   |  
|            DO NOT REPLY OR TAKE ACTION            |  
+==================================================+  
Test Email ID: TEST-20231223153210-ABC123  
Generated on: 2023-12-23 15:32:10  
This email was automatically generated for testing purposes.  
Any resemblance to real emails or situations is purely coincidental.  
+==================================================+  

Dear Team,  

Did you know that human memory is so unreliable that even the most vivid recollections are often false? Studies show that false memories can be implanted with ease, leaving us questioning reality itself.  

Additionally:  
- The average person lies several times daily, often unconsciously.  
- Obsession with control is linked to higher levels of anxiety and reduced happiness.  

Next Steps:  
- Reflect on these insights as we improve our approach to data integrity.  

Best Regards,  
Alex Dev  
```

---

## License  
This project is licensed under the MIT License.  

## Contributions  
Contributions, suggestions, or bug reports are welcome!  

---  

Let me know if you'd like further adjustments.
