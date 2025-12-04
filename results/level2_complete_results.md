# Level 2 - LLM Classifier Results

## Setup
- Model used: meta-llama/llama-3.3-70b-instruct:free
- Sample size: 50 messages (25 toxic, 25 clean)
- API: OpenRouter
- Date completed: 2025-12-03

## Performance Metrics

### Overall Performance:
- **Accuracy**: 0.800 (80.0%) - Percentage of all predictions that were correct
- **Precision**: 0.759 (75.9%) - Of messages flagged as toxic, what % were actually toxic
- **Recall**: 0.880 (88.0%) - Of all toxic messages, what % did we catch

### Confusion Matrix:
- True Positives: 22 - Correctly identified toxic messages
- False Positives: 7 - Incorrectly flagged clean messages as toxic
- True Negatives: 18 - Correctly identified clean messages
- False Negatives: 3 - Missed toxic messages (incorrectly marked as clean)

## Analysis of Results

### Examples of Correct Classifications:

1. **Message:** "f***ing morons"
   - **Label:** TOXIC
   - **Prediction:** TOXIC ✓
   - **Why it worked:** Clear profanity and insult, easy for LLM to identify

2. **Message:** "vroom vroom :D"
   - **Label:** CLEAN
   - **Prediction:** CLEAN ✓
   - **Why it worked:** Playful, no toxic indicators, emoticon shows positive sentiment

3. **Message:** "уебан недоношенный" (Russian profanity)
   - **Label:** TOXIC
   - **Prediction:** TOXIC ✓
   - **Why it worked:** LLM understands multilingual profanity, showing advantage over simple regex

### Examples of Incorrect Classifications:

#### False Positives (Incorrectly flagged as toxic):

1. **Message:** "do your job BZ Idiot and dont push me"
   - **Label:** CLEAN
   - **Prediction:** TOXIC ✗
   - **Analysis:** Contains "Idiot" which LLM flagged, but dataset labeled as clean. This shows inconsistency in dataset labeling or context-dependent toxicity.

2. **Message:** "gg" (last instance, line 51)
   - **Label:** CLEAN
   - **Prediction:** TOXIC ✗
   - **Analysis:** API rate limit hit (429 error), defaulted to TOXIC for safety. This is a limitation of the free tier.

3. **Message:** "push with me"
   - **Label:** CLEAN
   - **Prediction:** TOXIC ✗
   - **Analysis:** Rate limit error caused default to TOXIC. This is a technical issue, not a model accuracy issue.

#### False Negatives (Missed toxic content):

1. **Message:** "campers"
   - **Label:** TOXIC
   - **Prediction:** CLEAN ✗
   - **Analysis:** "Campers" is gaming slang that can be negative but isn't explicitly profane. LLM may not understand game-specific toxic terminology.

2. **Message:** "do nothing there"
   - **Label:** TOXIC
   - **Prediction:** CLEAN ✗
   - **Analysis:** Passive-aggressive but not explicitly toxic. LLM struggles with subtle toxicity without explicit profanity.

3. **Message:** "2 TD on base cen kill 5 whom, push NORTH = NORTH USLESS flank"
   - **Label:** TOXIC
   - **Prediction:** CLEAN ✗
   - **Analysis:** Contains "USLESS" (misspelled "useless") which is mildly critical. LLM may have missed the negativity due to poor grammar and misspelling.

## Key Findings

### Strengths of LLM Approach:
1. **Multilingual Understanding:** Successfully identified toxic content in Russian (уебан недоношенный, рикошет блядь), which regex would struggle with unless explicitly programmed.

2. **Context Awareness:** Correctly classified messages with profanity like "f***ing morons" while understanding playful messages like "vroom vroom :D" are clean.

3. **High Recall (88%):** Caught most toxic messages, reducing the risk of letting inappropriate content through. Better to over-flag than under-flag for moderation.

### Weaknesses of LLM Approach:
1. **Rate Limiting Issues:** Hit 429 errors starting at message 38, forcing defaults to TOXIC and causing 4-5 false positives. Free tier is severely limited for any meaningful testing.

2. **Subtle Toxicity:** Missed game-specific toxic terms like "campers" and passive-aggressive messages like "do nothing there" that don't contain explicit profanity.

3. **Dataset Inconsistency:** Some messages like "do your job BZ Idiot" are labeled clean despite containing "Idiot," suggesting the LLM may actually be more consistent than the dataset labels.

## Production Considerations

### Cost Calculation:
**For 1 million messages per day:**

**Free Tier:**
- Rate limit: ~50-100 requests/day (based on errors at message 38)
- **Conclusion:** Not viable for production scale - can barely handle 50 messages without rate limiting

**Paid Tier (estimated using current LLM pricing):**
- Tokens per message: ~50 (prompt) + 10 (response) = 60 tokens
- Total tokens per day: 1M messages × 60 tokens = 60M tokens/day
- Cost estimate (at $0.50 per 1M tokens): $30/day
- Monthly cost: ~$900/month
- Annual cost: ~$10,800/year

**Note:** Actual costs vary by model and provider. Free tier clearly insufficient.

### Latency:
- Average processing time: ~3 seconds per message (including rate limiting sleep)
- **For real-time chat:** Too slow - users expect instant responses (<500ms)
- **Batch processing:** Feasible but expensive and slow (1M messages = 34+ days at 3 sec/msg)

**Reality:** With rate limits, processing 50 messages took ~3 minutes. Processing 1M would be impractical even with paid tier.

### Reliability:
- API availability: Dependent on external service (OpenRouter experienced 429 errors)
- Error handling: Script defaults to TOXIC on errors (safe but increases false positives)
- Rate limits: Must be carefully managed - even 3-second delays weren't sufficient for free tier

## Conclusion

The LLM approach achieved 80% accuracy with strong recall (88%), demonstrating capability to catch most toxic content including multilingual profanity that regex would miss. However, **significant limitations make this unsuitable for production at scale:**

1. **Rate limiting** on free tier makes it unusable for any real application
2. **Cost** of $900+/month for paid tier is prohibitive for high-volume chat moderation
3. **Latency** of 3+ seconds per message is unacceptable for real-time chat
4. **Reliability** depends on external API availability

The LLM excels at understanding context and multilingual content, but the practical constraints (cost, speed, reliability) suggest a **hybrid approach** would be optimal: use fast regex for obvious cases, reserve LLM for edge cases or appeals. For production, a fine-tuned local model or hybrid system would be more practical than API-based LLM classification.
