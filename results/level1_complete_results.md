# Level 1 - Regex Filter Results

## Word List
- Total words: 10
- Words used: damn, hell, shit, fuck, ass, bitch, crap, stupid, idiot, dumb

## Performance on GameTox Dataset

### Metrics:
- **Accuracy**: 83.04% - What % of all predictions were correct
- **Precision**: 84.94% - Of messages we flagged, what % were actually toxic
- **Recall**: 18.05% - Of all toxic messages, what % did we catch

### Confusion Matrix:
- True Positives: 1,337 - Correctly flagged toxic messages
- False Positives: 237 - Incorrectly flagged innocent messages
- True Negatives: 43,260 - Correctly didn't flag innocent messages
- False Negatives: 6,070 - Missed toxic messages

### What These Numbers Mean:
The high accuracy (83.04%) is somewhat misleading because most messages are clean, so simply not flagging anything would give ~86% accuracy. The real insights come from precision and recall:

- **High precision (84.94%)** means when we flag something, we're usually right - only 237 mistakes out of 1,882 flagged messages
- **Very low recall (18.05%)** reveals the filter's critical weakness - we catch less than 1 in 5 toxic messages, meaning 82% of toxic content slips through because it doesn't use these specific profanity words

## Examples of False Positives
Messages we flagged but were actually innocent:

1. "sorry arty fuck me hard" - Playful banter between teammates, not hostile
2. "damn he chose a good spot" - Complimentary statement about opponent's strategy
3. "char mle idiot press x" - Gaming instruction, "idiot" used casually
4. "you idiot meds" - Likely friendly ribbing about medkits in game context
5. "stupid heavys" - Mild frustration about heavy tank players, not directed harassment

These examples show that context matters enormously. The same words that indicate toxicity in one context ("you fucking idiot") can be completely benign in another ("why the fuck" as an expression of surprise). A simple word list cannot distinguish between hostile intent and casual language.

## Reddit Username Testing
- Total usernames tested: 25,865,740
- Usernames flagged: 3,718
- Percentage flagged: 0.0144%

Examples of flagged usernames:
1. "i-fuck-cats" - Why it was flagged: contains "fuck"
2. "show-me-your-ass" - Why it was flagged: contains "ass"
3. "1-800-EAT-SHIT" - Why it was flagged: contains "shit"
4. "Tell-Me-To-Fuck-Off" - Why it was flagged: contains "fuck"
5. "FUCK-THEDONALD" - Why it was flagged: contains "fuck"

### Are these actually offensive?
Unlike chat messages, usernames with profanity are typically chosen deliberately and intentionally provocative. The flagging rate is 240x lower than GameTox (0.0144% vs 3.50%), suggesting profanity in usernames is quite rare but usually intentional when present. There are very few false positives in username detection compared to chat messages, because usernames lack the casual conversational context where profanity might be friendly or playful.

## Adversarial Testing - Bypass Attempts

I tested these creative spellings to see if they bypass the filter:

**Test Results:**
- "d@mn" - Result: **MISSED** - The @ symbol is not a letter, breaks word boundary
- "sh1t" - Result: **MISSED** - The number 1 is not the letter 'i'
- "f**k" - Result: **MISSED** - Asterisks interrupt the word pattern
- "a s s" (with spaces) - Result: **MISSED** - Spaces break the word boundary for the full word
- "azz" (alternative spelling) - Result: **MISSED** - Different spelling not in word list

**All 5 bypass attempts succeeded.** These results demonstrate that simple character substitutions easily evade the regex filter. Any user who wants to bypass detection can use leetspeak (l33tsp34k), symbols, spacing, or alternative spellings. The filter only catches users who aren't trying to hide their language.

## Key Findings

### Strengths of Regex Approach:
- **Extremely fast and computationally efficient** - Processed 25+ million Reddit usernames with minimal computational cost. Can handle production-scale traffic easily.
- **High precision (84.94%)** - When the filter flags something, it's usually correct. Low false positive rate means fewer angry users complaining about unfair moderation.
- **Transparent and explainable** - Easy to understand why something was flagged. No "black box" AI decisions. Users can see exactly what word triggered the filter.
- **No training data required** - Works immediately without needing labeled examples or machine learning infrastructure.
- **Deterministic and consistent** - Same input always produces same output. No model drift or need for retraining.

### Weaknesses of Regex Approach:
- **Very low recall (18.05%)** - Misses 82% of toxic content that doesn't use these specific profanity words. Many toxic messages use other slurs, coded language, or context-dependent insults not in our list.
- **Trivially easy to bypass** - Any motivated user can evade detection with simple character substitutions (sh1t, f**k, a s s). The filter only catches naive users.
- **Context-blind** - Cannot distinguish between "damn it lol" (friendly frustration) and "damn noob" (insult). Treats all profanity equally regardless of intent.
- **Requires manual maintenance** - Need to continuously add new slang, misspellings, and creative variants. Adversarial users stay one step ahead.
- **Cultural and linguistic limitations** - Word list is English-only and doesn't account for cultural differences in what's offensive. "Ass" might be a surname or part of legitimate words in other contexts.
- **No understanding of implicit toxicity** - Misses subtle harassment, sarcasm, dog whistles, and coded hate speech that doesn't use explicit profanity.

### The Precision/Recall Tradeoff:
We could improve recall by adding more words to the list, but each addition risks more false positives. For example, adding "noob" would catch more toxic messages but also flag legitimate gaming terminology. This fundamental tradeoff cannot be solved with regex alone - we need more sophisticated approaches that understand context.

## Recommendation for Next Steps:
The regex approach serves as a useful baseline but is insufficient for production content moderation. The 18% recall rate means the vast majority of toxic behavior goes undetected. Level 2 (LLM-based detection) and Level 3 (traditional ML classifiers) should be explored to achieve better recall while maintaining acceptable precision.
