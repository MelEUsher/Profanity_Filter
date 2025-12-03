# Profanity Filter Project - Progress Tracker

**Project Goal:** Build and compare profanity filtering approaches to understand trade-offs between rule-based systems, traditional ML, and LLMs.

**Key Learning Objectives:**
- Solution spectrum: Understand tradeoffs between rule-based systems, traditional ML, and LLMs
- Text classification: Gain hands-on experience with applied machine learning for NLP tasks
- LLM integration: Learn to work with LLM APIs effectively
- Text processing: Handle real-world challenges with Unicode, multilingual data, and noisy text

---

## Project Setup ✅

**Completed:** [Date: Dec 3, 2024]

### Environment
- **OS:** Mac
- **Python Version:** 3.13.9
- **Virtual Environment:** venv/
- **Repository:** https://github.com/MelEUsher/Profanity_Filter

### Datasets
- **GameTox Dataset:** 53,704 gaming chat messages
  - Text column: `message`
  - Label column: `label` (0.0 = clean, 1.0 = toxic)
  - Source: https://github.com/shucoll/GameTox
  
- **Reddit Usernames:** 25,865,740 usernames
  - For false positive testing
  - Source: Kaggle

### Project Structure
```
Profanity_Filter/
├── data/
│   ├── gametox.csv
│   └── reddit_usernames.csv
├── scripts/
│   ├── explore_data.py
│   └── explore_usernames.py
├── results/
├── venv/
└── .gitignore
```

---

## LEVEL 1: Regex-Based Filter 🔄

**Status:** Not Started  
**Started:** [Date]  
**Completed:** [Date]

### Learning Goals (From Project README)
- Regular expressions
- Working with real-world datasets (incomplete documentation, inherent biases)
- Evaluation metrics (accuracy, precision) vs. traditional testing approaches
- Understanding the precision/recall tradeoff

### Issue #3: Simple Single-Word Detection

**Objective:** Count messages containing "damn" and measure accuracy

**Implementation Details:**
```
Script: scripts/level1_single_word.py
Word tested: "damn"
```

**Results:**
- Total messages flagged: [NUMBER]
- Percentage of dataset: [X.X%]
- Correct flags (true positives): [NUMBER]
- False positives: [NUMBER]
- False negatives: [NUMBER]

**Key Observations:**
[Write 3-5 sentences about what you noticed]

**Examples of False Positives:**
1. [Example message that was incorrectly flagged]
2. [Example message that was incorrectly flagged]
3. [Example message that was incorrectly flagged]

**Examples of Missed Toxic Messages (False Negatives):**
1. [Example toxic message that wasn't caught]
2. [Example toxic message that wasn't caught]

**Insights:**
[What did this teach you about simple word matching?]

---

### Issue #4: Full Regex-Based Filter

**Objective:** Build comprehensive regex filter with profanity word list

**Implementation Details:**
```
Script: scripts/level1_regex_filter.py
Word list: data/profanity_words.txt
Number of words: [NUMBER]
Regex pattern: \b(word1|word2|word3|...)\b
```

**Performance Metrics on GameTox Dataset:**

| Metric | Value | Explanation |
|--------|-------|-------------|
| **Accuracy** | [0.XXX] | What % of all predictions were correct |
| **Precision** | [0.XXX] | Of messages we flagged, what % were actually toxic |
| **Recall** | [0.XXX] | Of all toxic messages, what % did we catch |
| **F1 Score** | [0.XXX] | Harmonic mean of precision and recall |

**Confusion Matrix:**
```
                    Actually Toxic    Actually Clean
Flagged as Toxic         [TP]              [FP]
Not Flagged              [FN]              [TN]

TP (True Positives):  [NUMBER] - Correctly caught toxic messages
FP (False Positives): [NUMBER] - Incorrectly flagged clean messages
TN (True Negatives):  [NUMBER] - Correctly didn't flag clean messages
FN (False Negatives): [NUMBER] - Missed toxic messages
```

**Reddit Username Testing:**
- Total usernames tested: [NUMBER]
- Usernames flagged: [NUMBER] ([X.X%])

**Examples of Flagged Usernames:**
1. [USERNAME] - Reason: [contains word "X"]
2. [USERNAME] - Reason: [contains word "Y"]
3. [USERNAME] - Reason: [contains word "Z"]

**Analysis:** Are these actually offensive? [YOUR THOUGHTS]

**Adversarial Testing - Bypass Attempts:**

| Creative Spelling | Caught? | Notes |
|-------------------|---------|-------|
| d@mn | ✓ / ✗ | [Why it worked/failed] |
| sh1t | ✓ / ✗ | [Why it worked/failed] |
| f**k | ✓ / ✗ | [Why it worked/failed] |
| a s s (spaces) | ✓ / ✗ | [Why it worked/failed] |
| azz (homophone) | ✓ / ✗ | [Why it worked/failed] |
| [Your test] | ✓ / ✗ | [Why it worked/failed] |

**Key Findings:**

**Strengths of Regex Approach:**
1. [Strength 1]
2. [Strength 2]
3. [Strength 3]

**Weaknesses of Regex Approach:**
1. [Weakness 1]
2. [Weakness 2]
3. [Weakness 3]

**The Precision/Recall Tradeoff Observed:**
[Explain: When we try to catch more bad messages (increase recall), what happens to false positives (precision)? Can you have both high precision AND high recall with regex?]

**Context Understanding:**
- Can regex understand context? [YES/NO]
- Example: "damn good game" vs "damn you"
  - Regex treats them: [THE SAME / DIFFERENTLY]
  - Why: [EXPLANATION]

**Production Considerations:**
- Speed: [INSTANT / FAST / SLOW]
- Cost: [FREE / $X per message]
- Can handle 1M messages/day: [YES / NO]
- Requires internet: [YES / NO]

---

## LEVEL 2: LLM-Powered Filter 🔄

**Status:** Not Started  
**Started:** [Date]  
**Completed:** [Date]

### Learning Goals (From Project README)
- LLM API integration and prompt engineering
- Cost/latency tradeoffs in production ML systems
- When LLMs are (and aren't) practical solutions

### Setup

**OpenRouter Account:**
- Created: [Date]
- API Key stored in: `.env`
- Model used: `meta-llama/llama-3.3-70b-instruct:free`

**Rate Limits:**
- Free tier: 50 requests/day
- Velocity limit: 20 requests/minute

**Sample Size Decision:**
[Explain why you're using a small sample instead of the full dataset]
- Messages selected: [50 / 100 / OTHER]
- Sampling strategy: [BALANCED / RANDOM / OTHER]
- Reason: [EXPLANATION]

---

### Issue #5: OpenRouter API Setup

**Objective:** Setup API access and test connection

**Implementation Details:**
```
Script: scripts/test_openrouter.py
Test message: "Say 'Hello! API is working!' and nothing else."
```

**Results:**
- Connection successful: [YES / NO]
- Response received: [YES / NO]
- Latency: [X.X seconds]

**Issues Encountered:**
[Any problems and how you solved them]

---

### Issue #6: LLM Classification Implementation

**Objective:** Use LLM to classify messages as toxic/clean

**Implementation Details:**
```
Script: scripts/level2_llm_classifier.py
Sample script: scripts/create_sample.py
Sample file: data/gametox_sample_50.csv
Prompt template: data/prompt_template.txt
```

**Prompt Used:**
```
[Copy your exact prompt here]
```

**Sample Composition:**
- Total messages: [NUMBER]
- Toxic messages: [NUMBER]
- Clean messages: [NUMBER]
- Sampling method: [BALANCED / RANDOM]

**Performance Metrics on Sample:**

| Metric | Value | Explanation |
|--------|-------|-------------|
| **Accuracy** | [0.XXX] | What % of all predictions were correct |
| **Precision** | [0.XXX] | Of messages we flagged, what % were actually toxic |
| **Recall** | [0.XXX] | Of all toxic messages, what % did we catch |
| **F1 Score** | [0.XXX] | Harmonic mean of precision and recall |

**Confusion Matrix:**
```
                    Actually Toxic    Actually Clean
Flagged as Toxic         [TP]              [FP]
Not Flagged              [FN]              [TN]

TP (True Positives):  [NUMBER]
FP (False Positives): [NUMBER]
TN (True Negatives):  [NUMBER]
FN (False Negatives): [NUMBER]
```

**Processing Details:**
- Total time: [X minutes]
- Average time per message: [X seconds]
- API calls made: [NUMBER]
- Errors encountered: [NUMBER]

**Examples Where LLM Succeeded:**

**Case 1 - Context Understanding:**
- Message: "[EXAMPLE]"
- Actual label: [TOXIC/CLEAN]
- LLM prediction: [TOXIC/CLEAN] ✓
- Why LLM got it right: [EXPLANATION - did it understand context? Implicit meaning?]

**Case 2 - Context Understanding:**
- Message: "[EXAMPLE]"
- Actual label: [TOXIC/CLEAN]
- LLM prediction: [TOXIC/CLEAN] ✓
- Why LLM got it right: [EXPLANATION]

**Case 3 - Subtle Toxicity:**
- Message: "[EXAMPLE - no profanity words but still toxic]"
- Actual label: [TOXIC/CLEAN]
- LLM prediction: [TOXIC/CLEAN] ✓
- Why regex would miss this: [EXPLANATION]
- Why LLM caught it: [EXPLANATION]

**Examples Where LLM Failed:**

**Case 1 - LLM Error:**
- Message: "[EXAMPLE]"
- Actual label: [TOXIC/CLEAN]
- LLM prediction: [TOXIC/CLEAN] ✗
- Why it failed: [YOUR ANALYSIS - was it too subtle? Too context-dependent? Unclear prompt?]

**Case 2 - LLM Error:**
- Message: "[EXAMPLE]"
- Actual label: [TOXIC/CLEAN]
- LLM prediction: [TOXIC/CLEAN] ✗
- Why it failed: [YOUR ANALYSIS]

**Key Findings:**

**Strengths of LLM Approach:**
1. [Strength 1]
2. [Strength 2]
3. [Strength 3]

**Weaknesses of LLM Approach:**
1. [Weakness 1]
2. [Weakness 2]
3. [Weakness 3]

**Context Understanding Examples:**

**Same Word, Different Context:**
- Message 1 (Innocent): "[EXAMPLE with profanity word used innocently]"
  - LLM prediction: [CLEAN/TOXIC]
  - Correct? [YES/NO]
  
- Message 2 (Toxic): "[EXAMPLE with same word used toxically]"
  - LLM prediction: [CLEAN/TOXIC]
  - Correct? [YES/NO]

- Analysis: [Did LLM understand the difference? How?]

**Indirect Toxicity:**
- Message: "[EXAMPLE - toxic meaning without profanity words]"
- Contains profanity words? [YES/NO]
- Regex would catch it? [YES/NO]
- LLM caught it? [YES/NO]
- Why: [EXPLANATION]

**Production Feasibility:**

**Cost Analysis:**

For 1 Million Messages per Day:

**Free Tier:**
- Rate limit: 50 requests/day
- Can handle 1M/day? ❌ NO
- Max messages per day: 50
- Why not feasible: [EXPLANATION]

**Paid Tier (Example: GPT-4o):**
- Model cost: $[X.XX] per 1M input tokens
- Estimated tokens per message: ~[NUMBER]
  - Message: ~[NUMBER] tokens
  - Prompt overhead: ~[NUMBER] tokens
- Total tokens for 1M messages: [NUMBER]M tokens
- Cost per day: $[CALCULATE]
- Cost per month (30 days): $[CALCULATE]
- Cost per year: $[CALCULATE]

**Compared to Regex:**
- Regex cost: $0
- LLM cost: $[X,XXX] per [day/month/year]
- Difference: [X]x more expensive

**Latency Analysis:**

| Approach | Time per Message | Can Handle Real-Time Chat? |
|----------|------------------|----------------------------|
| Regex | <0.001 seconds | ✅ YES |
| LLM (with rate limits) | ~3-5 seconds | ❌ NO |
| LLM (paid, no limits) | ~1-2 seconds | ⚠️ MAYBE (depends on requirements) |

**Infrastructure Requirements:**

| Requirement | Regex | LLM |
|-------------|-------|-----|
| External API | ❌ No | ✅ Yes |
| Internet required | ❌ No | ✅ Yes |
| Can run offline | ✅ Yes | ❌ No |
| Dependencies | Minimal | API libraries |
| Maintenance | Low | Medium (API changes, prompt updates) |

---

## LEVEL 1 vs LEVEL 2: COMPARISON 🔄

**Status:** Not Started  
**Started:** [Date]  
**Completed:** [Date]

### Direct Head-to-Head Comparison

**Note:** Both approaches evaluated on the **exact same 50-message sample** for fair comparison.

**Performance Comparison:**

| Metric | Regex | LLM | Winner | Difference |
|--------|-------|-----|--------|------------|
| Accuracy | [0.XXX] | [0.XXX] | [REGEX/LLM/TIE] | ±[X.X%] |
| Precision | [0.XXX] | [0.XXX] | [REGEX/LLM/TIE] | ±[X.X%] |
| Recall | [0.XXX] | [0.XXX] | [REGEX/LLM/TIE] | ±[X.X%] |
| F1 Score | [0.XXX] | [0.XXX] | [REGEX/LLM/TIE] | ±[X.X%] |

**Interpretation:**
- **Accuracy winner:** [REGEX/LLM] got [X]% more predictions correct overall
- **Precision winner:** [REGEX/LLM] had [X]% fewer false alarms
- **Recall winner:** [REGEX/LLM] caught [X]% more of the toxic messages

---

### Disagreement Analysis

**Total Disagreements:** [NUMBER] messages where regex and LLM gave different answers

**Category 1: LLM Right, Regex Wrong** ([NUMBER] cases)

**Example 1:**
- Message: "[COPY EXACT MESSAGE]"
- Actual label: [TOXIC/CLEAN]
- Regex predicted: [TOXIC/CLEAN] ✗
- LLM predicted: [TOXIC/CLEAN] ✓
- Why regex failed: [EXPLANATION - word not in list? Context needed? Misspelling?]
- Why LLM succeeded: [EXPLANATION - understood context? Implicit meaning? Paraphrasing?]

**Example 2:**
- Message: "[COPY EXACT MESSAGE]"
- Actual label: [TOXIC/CLEAN]
- Regex predicted: [TOXIC/CLEAN] ✗
- LLM predicted: [TOXIC/CLEAN] ✓
- Why regex failed: [EXPLANATION]
- Why LLM succeeded: [EXPLANATION]

**Example 3:**
- Message: "[COPY EXACT MESSAGE]"
- Actual label: [TOXIC/CLEAN]
- Regex predicted: [TOXIC/CLEAN] ✗
- LLM predicted: [TOXIC/CLEAN] ✓
- Why regex failed: [EXPLANATION]
- Why LLM succeeded: [EXPLANATION]

**Category 2: Regex Right, LLM Wrong** ([NUMBER] cases)

**Example 1:**
- Message: "[COPY EXACT MESSAGE]"
- Actual label: [TOXIC/CLEAN]
- Regex predicted: [TOXIC/CLEAN] ✓
- LLM predicted: [TOXIC/CLEAN] ✗
- Why regex succeeded: [EXPLANATION - clear profanity word?]
- Why LLM failed: [EXPLANATION - too subtle? Prompt issue? Model limitation?]

[Add more examples if they exist]

**Category 3: Both Wrong** ([NUMBER] cases)

**Example:**
- Message: "[COPY EXACT MESSAGE]"
- Actual label: [TOXIC/CLEAN]
- Regex predicted: [TOXIC/CLEAN] ✗
- LLM predicted: [TOXIC/CLEAN] ✗
- Why both failed: [YOUR ANALYSIS - is this message genuinely hard? Ambiguous? Mislabeled in dataset?]

---

### Context Understanding Deep Dive

**The Key Advantage of LLMs: Understanding Context**

**Example 1 - Same Word, Different Intent:**

Message A (Clean): "[EXAMPLE - profanity word used innocuously]"
- Regex: [TOXIC/CLEAN] - treats based on word presence only
- LLM: [TOXIC/CLEAN] - considers context and intent
- Actual: [TOXIC/CLEAN]

Message B (Toxic): "[EXAMPLE - same profanity word used harmfully]"
- Regex: [TOXIC/CLEAN] - treats based on word presence only
- LLM: [TOXIC/CLEAN] - considers context and intent
- Actual: [TOXIC/CLEAN]

Analysis: [Can regex distinguish between these? Can LLM? What does this tell you about context?]

**Example 2 - Implicit Toxicity:**

Message: "[EXAMPLE - toxic without profanity words, like insults or harassment]"
- Contains profanity words? [YES/NO]
- Regex: [TOXIC/CLEAN] - [why it got this result]
- LLM: [TOXIC/CLEAN] - [why it got this result]
- Actual: [TOXIC/CLEAN]

Analysis: [What does this show about the limits of word-matching vs semantic understanding?]

**Example 3 - Sarcasm/Irony:**

Message: "[EXAMPLE - if you found any sarcastic messages]"
- Regex: [TOXIC/CLEAN]
- LLM: [TOXIC/CLEAN]
- Actual: [TOXIC/CLEAN]

Analysis: [Can either approach handle sarcasm? Why/why not?]

---

### Production Trade-offs Summary

**When to Use Regex:**

**Scenarios:**
1. [SCENARIO - e.g., "Need to process millions of messages per day"]
2. [SCENARIO - e.g., "Cost must be near zero"]
3. [SCENARIO - e.g., "Latency must be <1ms"]
4. [SCENARIO - e.g., "No internet connection available"]

**Best Use Case:** [1-2 sentences about ideal regex scenario]

**When to Use LLM:**

**Scenarios:**
1. [SCENARIO - e.g., "Context is critical to accuracy"]
2. [SCENARIO - e.g., "Processing human appeals/reports"]
3. [SCENARIO - e.g., "Budget allows for quality over cost"]
4. [SCENARIO - e.g., "Volume is low (<1000/day)"]

**Best Use Case:** [1-2 sentences about ideal LLM scenario]

---

### Hybrid Architecture Recommendation

**For a Real Production System Processing 1M Messages/Day:**

[Describe how you'd combine both approaches]

**Proposed Architecture:**
1. **First Pass - Regex:**
   - [What would you do? Catch obvious cases? Pre-filter?]
   - [Why? Cost? Speed?]

2. **Second Pass - LLM:**
   - [What messages go to LLM? Borderline cases? Appeals?]
   - [Why? Context needed? Higher accuracy required?]

3. **Human Review:**
   - [What needs human review? When?]
   - [How does this fit into the system?]

**Expected Performance:**
- Cost: [Estimate based on % going to each tier]
- Latency: [Estimate based on architecture]
- Accuracy: [Would this be better than either alone?]

**Rationale:**
[2-3 paragraphs explaining why this hybrid approach makes sense based on your findings]

---

### The Precision/Recall Tradeoff Across Both Approaches

**What is the Precision/Recall Tradeoff?**
[Explain in your own words after seeing it in action]

**How It Manifested:**

**In Regex:**
- When we made regex stricter (more words): [What happened to precision? Recall?]
- When we made regex looser (fewer words): [What happened to precision? Recall?]
- Can you have both high precision AND high recall with regex? [YES/NO - explain why]

**In LLM:**
- Precision: [HIGH/MEDIUM/LOW] - [Why?]
- Recall: [HIGH/MEDIUM/LOW] - [Why?]
- Did prompt wording affect this? [YOUR OBSERVATIONS]
- Can you tune the tradeoff with prompts? [YES/NO - how?]

**Which Approach Handles the Tradeoff Better?**
[Your analysis based on data]

---

## KEY LEARNINGS & INSIGHTS

### About Regex-Based Filtering

**Technical Learnings:**
1. [What you learned about regular expressions]
2. [What you learned about pattern matching]
3. [What you learned about word boundaries, escaping, etc.]

**Practical Learnings:**
1. [What you learned about false positives in production]
2. [What you learned about the impossibility of perfect word lists]
3. [What you learned about adversarial users]

**Surprises:**
- [What surprised you about regex performance?]
- [What surprised you about its limitations?]

### About LLM-Based Filtering

**Technical Learnings:**
1. [What you learned about API integration]
2. [What you learned about prompt engineering]
3. [What you learned about structured outputs]

**Practical Learnings:**
1. [What you learned about cost/latency tradeoffs]
2. [What you learned about rate limits]
3. [What you learned about when LLMs fail]

**Surprises:**
- [What surprised you about LLM performance?]
- [What surprised you about its limitations?]

### About Production ML Systems

**Cost vs Performance:**
[What you learned about balancing accuracy with cost]

**Latency Constraints:**
[What you learned about real-time requirements]

**The "Good Enough" Problem:**
[When is 80% accuracy acceptable? When do you need 99%? What determines this?]

**Evaluation Metrics:**
[What you learned about accuracy vs precision vs recall - which matters when?]

### Personal Growth

**Skills Gained:**
1. [Technical skill 1]
2. [Technical skill 2]
3. [Technical skill 3]

**Mindset Shifts:**
1. [How your thinking changed about ML in production]
2. [How your thinking changed about "best" solutions]
3. [How your thinking changed about trade-offs]

**Most Valuable Lesson:**
[2-3 sentences: What will you remember from this project in 6 months?]

---

## TEAM LEAD FEEDBACK & DISCUSSION NOTES

**Feedback Received:**
[After you discuss this with your team lead, capture their feedback here]

**Questions Asked:**
1. [Question you asked]
   - Answer: [What they said]

**Additional Context Provided:**
[Anything your team lead explained about real production systems, similar work they've done, etc.]

**Next Steps Suggested:**
[What they recommended you do next or explore further]

---

## NEXT STEPS & FUTURE WORK

### Immediate Next Steps
- [ ] [What's next in the project?]

### Optional Extensions (If Time/Interest)
- [ ] Level 3: Traditional ML (scikit-learn)
- [ ] Multi-language support
- [ ] Fine-tune an LLM for this task
- [ ] Build a web API
- [ ] Create a user interface
- [ ] Test on non-English languages
- [ ] Implement the hybrid architecture

### Questions to Explore Further
1. [Question you still have]
2. [Question you still have]
3. [Question you still have]

---

## APPENDIX

### Files Created

**Data Files:**
- `data/gametox.csv` - 53,704 gaming chat messages
- `data/reddit_usernames.csv` - 25M+ usernames
- `data/gametox_sample_50.csv` - Balanced sample for LLM testing
- `data/profanity_words.txt` - Word list for regex
- `data/prompt_template.txt` - LLM prompt template

**Scripts:**
- `scripts/explore_data.py` - Initial data exploration
- `scripts/explore_usernames.py` - Username dataset exploration
- `scripts/level1_single_word.py` - Single word detection
- `scripts/level1_regex_filter.py` - Full regex implementation
- `scripts/level1_test_usernames.py` - Test regex on usernames
- `scripts/create_sample.py` - Create balanced sample
- `scripts/test_openrouter.py` - Test API connection
- `scripts/level2_llm_classifier.py` - LLM implementation
- `scripts/compare_approaches.py` - Side-by-side comparison
- `scripts/create_comparison_chart.py` - Visualization

**Results:**
- `results/level1_single_word_findings.md`
- `results/level1_complete_results.md`
- `results/level1_flagged_messages.csv`
- `results/level1_flagged_usernames.csv`
- `results/level2_complete_results.md`
- `results/level2_llm_predictions.csv`
- `results/level1_vs_level2_comparison.csv`
- `results/comparison_chart.png`
- `results/FINAL_COMPARISON.md`

### Git Commits
[List major commits as you go]
- `[commit hash]` - [commit message]
- `[commit hash]` - [commit message]

### Time Tracking
- Setup: [X hours]
- Level 1: [X hours]
- Level 2: [X hours]
- Comparison: [X hours]
- Documentation: [X hours]
- **Total:** [X hours] over [Y days]

---

**Last Updated:** [Date]  
**Project Status:** [In Progress / Complete]  
**Current Phase:** [Phase name]
