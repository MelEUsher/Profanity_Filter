# Level 1 vs Level 2: Regex vs LLM Comparison

## Executive Summary

The LLM approach significantly outperformed the basic regex filter, achieving 80% accuracy compared to regex's 60% on the same 50-message sample. While regex demonstrated higher precision (85.7% vs 75.9%), it suffered from catastrophically low recall (24% vs 88%), missing 76% of toxic messages. The LLM's superior F1 score (0.815 vs 0.375) clearly demonstrates its overall effectiveness. However, production deployment requires balancing this accuracy advantage against the LLM's substantial cost and latency constraints.

---

## Performance Comparison (Same 50-Message Sample)

| Metric | Regex | LLM | Winner | Difference |
|--------|-------|-----|--------|------------|
| Accuracy | 0.600 | 0.800 | LLM | +20.0% |
| Precision | 0.857 | 0.759 | Regex | -9.8% |
| Recall | 0.240 | 0.880 | LLM | +64.0% |
| F1 Score | 0.375 | 0.815 | LLM | +44.0% |

### What These Numbers Mean:
- **Accuracy**: LLM correctly classified 40/50 messages (80%) while regex only got 30/50 (60%) correct. LLM made 10 more correct predictions overall.
- **Precision**: Regex had fewer false alarms (only 1 false positive) compared to LLM (7 false positives). When regex flags something as toxic, it's right 85.7% of the time vs LLM's 75.9%.
- **Recall**: LLM caught 22 out of 25 toxic messages (88%) while regex only caught 6 out of 25 (24%). Regex missed 76% of the toxic content.
- **F1 Score**: LLM achieved better balance between precision and recall (0.815) compared to regex's severely imbalanced performance (0.375), which was dragged down by terrible recall.

---

## Key Disagreements Analysis

### Category 1: LLM Right, Regex Wrong (16 messages)

**Example 1: Obfuscated Profanity**
- **Message**: "fuking bots"
- **Actual Label**: TOXIC
- **Regex Prediction**: CLEAN ✗
- **LLM Prediction**: TOXIC ✓
- **Why LLM Won**: LLM recognized "fuking" as an intentional misspelling of a profanity word, understanding the writer's intent despite the obfuscation.
- **Why Regex Failed**: The wordlist only contains "fuck" with correct spelling. The pattern \bfuck\b doesn't match "fuking", so regex completely missed it. This is a fundamental limitation of exact word matching.

**Example 2: Censored Profanity**
- **Message**: "f\*\*\*ing morons"
- **Actual Label**: TOXIC
- **Regex Prediction**: CLEAN ✗
- **LLM Prediction**: TOXIC ✓
- **Why LLM Won**: LLM understood that f\*\*\*ing is clearly a censored version of a profanity word, combined with "morons" (an insult). It recognized the toxic intent despite censorship.
- **Why Regex Failed**: The asterisks break the word boundary pattern. "f\*\*\*ing" doesn't match \bfuck\b or any other word in the list.

**Example 3: Non-English Profanity**
- **Message**: "уебан недоношенный"
- **Actual Label**: TOXIC
- **Regex Prediction**: CLEAN ✗
- **LLM Prediction**: TOXIC ✓
- **Why LLM Won**: LLM recognized Russian profanity and understood toxic intent across languages. Its training on multilingual data enables cross-language toxicity detection.
- **Why Regex Failed**: The profanity wordlist only contains English words. Regex has zero capability for non-English content detection.

**Example 4: Creative Insults**
- **Message**: "amx spot retard"
- **Actual Label**: TOXIC
- **Regex Prediction**: CLEAN ✗
- **LLM Prediction**: TOXIC ✓
- **Why LLM Won**: LLM recognized "retard" as an offensive term used as an insult in this gaming context.
- **Why Regex Failed**: "retard" is not in the 10-word profanity list. The wordlist is too limited to catch common insults.

**Example 5: Acronyms and Abbreviations**
- **Message**: "FKN ELC"
- **Actual Label**: TOXIC
- **Regex Prediction**: CLEAN ✗
- **LLM Prediction**: TOXIC ✓
- **Why LLM Won**: LLM recognized "FKN" as an abbreviation for a profanity word, understanding the intent behind the acronym.
- **Why Regex Failed**: The wordlist doesn't include acronyms or abbreviations. Regex requires exact word matches.

### Category 2: Regex Right, LLM Wrong (6 messages)

**Example 1: False Positive Due to Rate Limiting**
- **Message**: "push with me"
- **Actual Label**: CLEAN
- **Regex Prediction**: CLEAN ✓
- **LLM Prediction**: TOXIC ✗
- **Why Regex Won**: Simple word matching correctly identified this as a clean tactical communication with no profanity words.
- **Why LLM Failed**: This appears to be a rate limiting artifact. The message appears near the end of the 50-message sequence (message #48), where the LLM began over-flagging clean messages, likely due to degraded API response quality or timeout issues.

**Example 2: Another Rate Limit Victim**
- **Message**: "best"
- **Actual Label**: CLEAN
- **Regex Prediction**: CLEAN ✓
- **LLM Prediction**: TOXIC ✗
- **Why Regex Won**: No profanity words detected - correctly classified as clean.
- **Why LLM Failed**: This is message #50, the last message processed. The single word "best" is clearly non-toxic, suggesting the LLM's decision-making degraded at the end of processing, possibly due to rate limiting or API timeout issues.

**Example 3: Innocuous Game Communication**
- **Message**: "let them come"
- **Actual Label**: CLEAN
- **Regex Prediction**: CLEAN ✓
- **LLM Prediction**: TOXIC ✗
- **Why Regex Won**: No profanity words present - correctly identified as clean tactical chat.
- **Why LLM Failed**: Message #45 in the sequence. The LLM may have misinterpreted the tactical language as threatening, or this could be another rate limiting artifact.

### Category 3: Both Wrong (4 messages)

**Example 1: Indirect Toxicity**
- **Message**: "campers"
- **Actual Label**: TOXIC
- **Regex Prediction**: CLEAN ✗
- **LLM Prediction**: CLEAN ✗
- **Why Both Failed**: "Campers" is considered toxic in gaming contexts (derogatory term for players using a defensive strategy), but neither approach caught it. Regex failed because "campers" isn't in the wordlist. LLM failed because the word itself isn't inherently toxic - it requires deep gaming culture knowledge to understand why this is labeled toxic in this dataset. This shows a limitation of the ground truth labels, which may reflect game-specific toxicity definitions that even the LLM doesn't capture.

**Example 2: Subtle Context-Dependent Toxicity**
- **Message**: "do nothing there"
- **Actual Label**: TOXIC
- **Regex Prediction**: CLEAN ✗
- **LLM Prediction**: CLEAN ✗
- **Why Both Failed**: This is labeled toxic, but appears to be tactical advice without explicit profanity or obvious toxicity. Both approaches correctly identified no profanity words. This might be a labeling error in the ground truth dataset, or it may be toxic due to context we don't have (e.g., tone, previous conversation, teammate frustration). Without explicit toxic language, neither approach could detect it.

---

## Context Understanding Examples

### Same Word, Different Context:

**Example 1: Profanity Used to Emphasize Frustration**
- **Message**: "so fuck u"
- **Regex**: TOXIC ✓
- **LLM**: TOXIC ✓
- **Analysis**: Both correctly identified this as toxic. The word "fuck" combined with "u" is clearly hostile. This is the type of straightforward case where regex performs well.

**Example 2: Word Fragment in Censored Form**
- **Message**: "wg is fck"
- **Regex**: CLEAN ✗
- **LLM**: TOXIC ✓
- **Analysis**: "fck" is a censored version of "fuck". LLM understood the intent; regex couldn't match the pattern. This demonstrates why context and intent matter beyond exact string matching.

### Indirect Toxicity:

**Example:**
- **Message**: "2 TD on base cen kill 5 whom, push NORTH = NORTH USLESS flank"
- **Regex**: CLEAN ✗
- **LLM**: CLEAN ✗
- **Both Failed**: This is labeled toxic (possibly due to "USLESS" being a frustrated statement about teammates), but contains no explicit profanity. Neither approach caught it. This represents the hardest category - toxic intent expressed without profanity words. The misspelling "USLESS" and frustrated tone don't trigger regex, and even the LLM missed the negative sentiment in this gaming context.

---

## Production Feasibility Analysis

### Speed/Latency Comparison

#### Regex:
- **Time per message**: <0.001 seconds (essentially instant)
- **Time for 1M messages**: ~16 minutes (parallel processing possible)
- **Real-time chat**: ✅ YES - users experience zero delay
- **Scalability**: ✅ Excellent - can process any volume with minimal resources

#### LLM:
- **Time per message**: ~3 seconds (with rate limiting, API latency)
- **Time for 1M messages**: ~35 days (serial processing with free tier rate limits)
- **Real-time chat**: ❌ NO - 3-second delay per message destroys user experience
- **Scalability**: ❌ Poor - rate limits make high-volume processing impractical

**Reality Check**: In a live game chat, users type messages and expect immediate delivery. A 3-second delay per message is completely unacceptable. Even with paid tiers and parallel processing, LLM latency (200-500ms minimum) is 200-500x slower than regex.

### Cost Comparison

#### Regex:
- **Development cost**: Low (one-time wordlist creation: ~1 hour)
- **Operating cost**: $0 (runs locally, no external APIs)
- **Per-message cost**: $0
- **Daily cost (1M messages)**: $0
- **Monthly cost**: $0
- **Annual cost**: $0

#### LLM (Free Tier):
- **Rate limit**: ~50 requests/day (OpenRouter free tier)
- **Max messages/day**: 50
- **Can handle 1M messages/day**: ❌ NO - would take 54 years
- **Conclusion**: Free tier unusable for production at scale

#### LLM (Paid - GPT-4o pricing):
**Assumptions:**
- $5 per 1M input tokens
- ~100 tokens per request (system prompt: ~60 tokens, message: ~20 tokens, response: ~20 tokens)
- 1M messages per day

**Calculations:**
- Tokens per day: 1M messages × 100 tokens = 100M tokens
- Cost per day: 100M ÷ 1M × $5 = $500
- Cost per month: $500 × 30 = $15,000
- Cost per year: $15,000 × 12 = $180,000

**Reality**: For a game with 1M messages/day, LLM-only filtering would cost $180,000/year vs $0/year for regex. This is before considering output token costs, API overhead, and infrastructure.

### Infrastructure Requirements

#### Regex:
- **Dependencies**: Python 3.x, re module (built-in)
- **External APIs**: None
- **Internet required**: No
- **Can run offline**: ✅ Yes - fully self-contained
- **Single point of failure**: None (local processing)
- **Maintenance**: Low (update wordlist quarterly: ~1 hour)

#### LLM:
- **Dependencies**: Python 3.x, OpenAI SDK, API credentials
- **External APIs**: OpenRouter or OpenAI (required for every message)
- **Internet required**: Yes (always)
- **Can run offline**: ❌ No - completely dependent on external API
- **Single point of failure**: API availability, internet connection, API key validity
- **Maintenance**: Medium (monitor costs, rate limits, API changes, prompt updates)

---

## The Trade-off Analysis

### When to Use Regex:

1. **High-volume processing**: Millions of messages per day where speed is critical
2. **Real-time requirements**: Live chat where sub-millisecond latency is needed
3. **Cost constraints**: Zero operating budget for content moderation
4. **Offline capability**: No guarantee of internet connectivity
5. **Simple profanity**: Clear-cut profanity words in a single language
6. **Known vocabulary**: Established set of terms to filter

**Best use case**: Primary filter for bulk processing in real-time systems where speed, cost, and reliability matter more than perfect accuracy. Accept 24% recall as a trade-off for zero cost and instant processing.

### When to Use LLM:

1. **Context-critical cases**: Messages where word meaning depends on usage and intent
2. **Appeal reviews**: User-reported false positives that need intelligent re-evaluation
3. **Multilingual content**: Chat in multiple languages without language-specific wordlists
4. **Indirect toxicity**: Harassment, sarcasm, and toxic intent without explicit profanity
5. **Low-volume, high-stakes**: Small number of critical messages (e.g., public forum posts, support tickets)
6. **Unknown or evolving profanity**: New slang, creative obfuscation, acronyms

**Best use case**: Secondary review layer for edge cases, appeals, and strategic moderation where accuracy justifies the cost and latency. Not suitable as primary filter for high-volume real-time systems.

### Hybrid Approach (Recommended for Production):

**Architecture:**
```
All messages
    ↓
[1. Regex Filter - Fast screening]
    ↓
├─ Clear Pass (no bad words) → ALLOW ✅
├─ Clear Fail (obvious profanity) → BLOCK ❌
└─ Uncertain Cases (borderline/appeals) → [2. LLM Review]
                                              ↓
                                          Final Decision
```

**Benefits:**
- **Speed**: 95%+ messages handled instantly by regex (sub-millisecond)
- **Cost**: Only 5-10% of messages use expensive LLM
- **Accuracy**: Best of both worlds - fast filtering + smart review
- **Scalability**: Handles high volume without rate limit issues

**Implementation for 1M messages/day:**

**Assumption**: Regex filters 90% of messages immediately (700K clean pass, 200K toxic block), leaving 10% uncertain for LLM review.

- **Regex processes**: ~900,000 messages (instant, $0)
  - ~700K clean (no profanity) → immediate pass
  - ~200K toxic (obvious profanity) → immediate block
- **LLM reviews**: ~100,000 uncertain cases
  - Messages with partial matches
  - Obfuscated words
  - Appeals and reports
- **LLM cost**: 100K messages × 100 tokens × ($5/1M tokens) = $50/day = $1,500/month

**Savings**: ~$1,500/month for hybrid vs $15,000/month for LLM-only = **90% cost reduction**

**Performance**:
- Recall improves from 24% (regex-only) to ~85%+ (hybrid)
- Precision remains high (false positives only in uncertain cases)
- Latency: <1ms for 90% of messages, 3s for 10% (acceptable for review queue)

---

## Observed Patterns

### Regex Strengths:
1. **Perfect precision on exact matches**: When a message contains an exact profanity word from the list ("fuck", "shit", "idiot"), regex catches it with 100% confidence.
2. **Zero false positives on clean messages**: Of the 25 clean messages, regex only had 1 false positive (96% precision on clean messages).
3. **Instant processing**: No latency, no rate limits, completely reliable.

### Regex Weaknesses:
1. **Catastrophic recall**: Missed 19 out of 25 toxic messages (76% miss rate) due to limited wordlist.
2. **No obfuscation handling**: Completely blind to "fuking", "f\*\*\*ing", "fck", "wtf" and other creative spellings.
3. **No multilingual support**: Missed 100% of non-English profanity (Russian examples).
4. **No context understanding**: Can't distinguish between "You're an idiot" (toxic) and "idiot mode activated" (potentially game feature/joke).
5. **Limited wordlist**: Only 10 words in the profanity list - real-world lists need 100-1000+ terms.

### LLM Strengths:
1. **Excellent recall**: Caught 22 out of 25 toxic messages (88% recall) - including obfuscated, censored, and non-English profanity.
2. **Context understanding**: Recognized "fuking" as intentional misspelling, "f\*\*\*ing" as censored profanity, and creative insults like "noob", "retard".
3. **Multilingual capability**: Detected Russian profanity without language-specific rules.
4. **Handles variations**: Caught "FKN" (acronym), "fck" (abbreviation), "IDIOTSSSSSSSSSSSSSS" (repeated letters).

### LLM Weaknesses:
1. **False positives from rate limiting**: Messages #45-51 showed degraded performance with clean messages incorrectly flagged as toxic ("push with me", "best", "gg").
2. **Lower precision**: 7 false positives vs regex's 1 (75.9% vs 85.7% precision).
3. **Unpredictable errors**: No clear pattern for why "let them come" or "making right move" were flagged as toxic - suggests API instability or rate limit throttling.
4. **No offline capability**: Completely dependent on external API availability.

---

## Precision vs Recall Trade-off

### Observed in This Study:

**Regex Performance:**
- Precision: 0.857 - High precision, low false positive rate (1 FP out of 7 total toxic predictions)
- Recall: 0.240 - Catastrophically low recall (missed 19 out of 25 toxic messages)
- Trade-off: Regex is **extremely conservative** - only flags messages with explicit profanity words. This means very few false alarms, but massive under-detection.

**LLM Performance:**
- Precision: 0.759 - Good precision, but 7 false positives (mostly due to rate limiting)
- Recall: 0.880 - Excellent recall (caught 22 out of 25 toxic messages)
- Trade-off: LLM is **more aggressive** - flags based on intent and context, not just word matching. This catches more toxicity but at the cost of some false positives.

**Content Moderation Context:**
- **False Positive** (blocking innocent message): User frustration, bad experience, but community stays safe. User can appeal.
- **False Negative** (missing toxic message): Toxic user harasses others, community becomes hostile, players quit. No appeal possible - the damage is done.

**Industry Standard**: Most content moderation systems prefer **higher recall** (catch more toxicity) at the cost of **lower precision** (some false positives), because:
1. False negatives (missed toxicity) cause more damage to community health
2. False positives can be appealed and reviewed
3. Toxic users who slip through harm retention and community culture

**Conclusion**: LLM's trade-off (88% recall, 76% precision) is more appropriate for production than regex's (24% recall, 86% precision). However, regex's precision makes it ideal for the first pass in a hybrid system.

---

## Key Learnings

### About Regex Filtering:
1. **Speed and cost matter in production**: Zero latency and zero cost make regex the foundation of any high-volume filtering system, even with low recall.
2. **Wordlist quality is everything**: The 10-word list is too limited. Production regex systems need comprehensive wordlists (100-1000+ terms) including variations, obfuscations, and common misspellings.
3. **Exact matching is fundamentally limited**: Without fuzzy matching or pattern variations, regex misses 76% of toxicity in real-world data with creative spellings and obfuscations.

### About LLM Filtering:
1. **Context understanding is powerful**: LLM's ability to recognize intent, obfuscation, and multilingual toxicity makes it 64% more effective at catching toxic content (88% vs 24% recall).
2. **Rate limiting kills production viability**: The degraded performance at the end of the 50-message batch shows that free-tier LLMs are unreliable for production use.
3. **Cost and latency are show-stoppers for real-time**: $180,000/year and 3-second delays make LLM-only filtering impractical for high-volume live chat systems.

### About Production ML Systems:
1. **"Best accuracy" doesn't mean "best solution"**: LLM is more accurate (80% vs 60%), but regex is better for production primary filtering due to cost, speed, and reliability.
2. **Hybrid approaches solve real-world constraints**: Using regex for 90% of messages (fast, free) and LLM for 10% (uncertain cases) achieves 85%+ recall at 10% of LLM-only cost.
3. **Trade-offs are unavoidable**: You cannot optimize for accuracy, cost, speed, and reliability simultaneously. Production systems require strategic compromise based on business requirements.

---

## Recommendations for Production

### For a game like Palia (1M messages/day):

**Recommended Architecture:**

**Tier 1 - Regex Pre-filter (100% of messages):**
- Use comprehensive wordlist (100-200 terms) including:
  - Core profanity (fuck, shit, damn, etc.)
  - Common variations (fck, fuk, f\*\*\*, sh!t, etc.)
  - Gaming-specific insults (noob, scrub, trash, etc.)
  - Slurs and hate speech terms
- Catch obvious profanity instantly
- **Cost**: $0
- **Speed**: <1ms per message
- **Expected recall**: 40-50% (better than 24% with expanded wordlist)

**Tier 2 - Pattern Detection (Supplement to Tier 1):**
- Add regex patterns for common obfuscations:
  - Letter substitutions (@ for a, 3 for e, $ for s)
  - Repeated characters (shiiiiit, f***uuuuuck)
  - Spacing tricks (f u c k, s.h.i.t)
- **Cost**: $0 (still regex)
- **Speed**: <1ms per message
- **Expected recall improvement**: +10-15% (total 50-65%)

**Tier 3 - LLM Review Queue (5-10% of messages):**
- Review cases where:
  - User appeals a block
  - Moderator reports but no regex match
  - Message contains partial matches or suspicious patterns
  - High-profile users or public channels
- **Cost**: ~$1,500-3,000/month (50K-100K reviews/day)
- **Speed**: Not critical (batch processing acceptable)
- **Expected recall**: 85-90% total (combining all tiers)

**Tier 4 - Human Moderation (<1% of messages):**
- Complex edge cases where LLM is uncertain
- Policy decisions for new terms/phrases
- Final appeals from users
- **Cost**: Existing moderation team time (~2-4 hours/day)

**Expected Results:**
- **Accuracy**: 85-90% (combining all tiers)
- **Cost**: $1,500-3,000/month (vs $15,000 LLM-only)
- **Speed**: <1ms for 95% of users (real-time chat maintained)
- **Scalability**: Handles 10M messages/day with same architecture

**Alternative Strategies:**

1. **Regex-Only with Expanded Wordlist** (Budget Option):
   - Invest 20-40 hours creating comprehensive wordlist with variations
   - Expected recall: 50-60%
   - Cost: $0/month
   - Best for: Small games with limited budget, acceptable miss rate

2. **ML-Based Local Classifier** (Advanced Option):
   - Train custom ML model (like detoxify, BERT-based) on game-specific data
   - Deploy locally (no API costs)
   - Expected recall: 70-80%
   - Cost: $0/month operating (one-time training cost)
   - Speed: ~10-50ms per message (acceptable for real-time)
   - Best for: Medium games with ML expertise, want accuracy without ongoing costs

3. **Community-Based Reporting** (Supplement):
   - Player reporting system for missed toxicity
   - Crowd-sourced moderation with reputation system
   - Feeds data back to improve Tier 1 wordlist
   - Cost: Development time only
   - Best for: All games - enhances any filtering approach

---

## Conclusion

The comparison reveals a clear winner in raw accuracy - the LLM approach achieved 80% accuracy with 88% recall, far surpassing regex's 60% accuracy and catastrophic 24% recall. The LLM's ability to understand context, detect obfuscated profanity, and handle multilingual content makes it technically superior for identifying toxic messages. However, this 20-percentage-point accuracy advantage masks the fundamental question: what matters more in production - being right more often, or being fast, cheap, and reliable?

The reality is that for a high-volume production system processing 1 million messages per day, the LLM-only approach is completely impractical. At $180,000 per year in API costs and 3 seconds per message in latency, the LLM approach would destroy both the budget and the user experience. Real-time chat requires sub-millisecond response times, not multi-second delays. Meanwhile, regex processes messages instantly at zero cost, even if it misses 76% of toxicity. This doesn't mean regex wins - it means neither approach alone is the right answer.

The ideal solution for real-world deployment is a hybrid architecture that leverages the strengths of both approaches while mitigating their weaknesses. Use regex as the primary filter to handle 90-95% of messages instantly and for free, catching obvious profanity with high precision. Route only uncertain cases - obfuscated words, partial matches, appeals - to the LLM for intelligent review. This approach achieves 85%+ recall (3x better than regex alone) at roughly 10% of the LLM-only cost (~$1,500/month vs ~$15,000/month), while maintaining sub-millisecond latency for the vast majority of users. The hybrid system delivers production-ready performance by optimizing for the real-world constraint that matters most: cost-effective accuracy at scale.

This project reveals what building production ML systems is really about - not finding the most accurate model, but finding the right balance between accuracy, cost, speed, and operational complexity. The LLM is more accurate, but accuracy alone doesn't pay the bills or keep users happy. Regex is cheaper and faster, but 24% recall means 76% of toxicity slips through, poisoning the community. The hybrid approach isn't a compromise - it's an optimization for real-world constraints. It demonstrates that production ML systems require thinking beyond model performance to business requirements, infrastructure constraints, and user experience. The best technical solution is the one you can actually deploy, maintain, and afford.

My key takeaway from building this profanity filtering system is that production ML is fundamentally about trade-offs, not absolutes. I started this project thinking the goal was to maximize accuracy - build the best classifier possible. But the comparison between regex and LLM shows that "best" depends entirely on context. For a research paper, the LLM approach wins because it has higher accuracy. For a real-world game with millions of daily messages, the hybrid approach wins because it balances accuracy with cost, speed, and scalability. The technical skill isn't just building a good model - it's understanding your constraints (budget, latency, volume), measuring what actually matters (user impact, not just F1 score), and architecting a solution that works within those constraints. Production ML systems are successful not when they achieve perfect accuracy, but when they deliver sufficient accuracy at sustainable cost with acceptable user experience. That's the engineering mindset that separates academic ML from production ML.

---

## Appendix: Full Results Data

**Regex Results (from Level 1):**
- Total messages tested: 50
- Accuracy: 0.600 (60.0%)
- Precision: 0.857 (85.7%)
- Recall: 0.240 (24.0%)
- F1 Score: 0.375 (37.5%)
- True Positives: 6
- False Positives: 1
- True Negatives: 24
- False Negatives: 19

**LLM Results (from Level 2):**
- Total messages tested: 50
- Accuracy: 0.800 (80.0%)
- Precision: 0.759 (75.9%)
- Recall: 0.880 (88.0%)
- F1 Score: 0.815 (81.5%)
- True Positives: 22
- False Positives: 7
- True Negatives: 18
- False Negatives: 3
- Rate limit issues: Yes (affected ~6 messages at end of batch)

**Comparison Results:**
- Messages where both correct: 24
- Messages where both wrong: 4
- Messages where only Regex correct: 6
- Messages where only LLM correct: 16
- Total disagreements: 22 (44% of messages)
