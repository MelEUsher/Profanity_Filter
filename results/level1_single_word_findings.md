# Level 1 - Single Word Detection Results

## Word tested: "damn"

### Statistics:
- Total messages flagged: 117
- Percentage of dataset: 0.22%
- Correct flags (actually toxic): 14
- False positives (incorrectly flagged): 65

### Observations:
The word "damn" is extremely rare in the GameTox dataset, appearing in only 0.22% of messages. However, the majority of these occurrences (55.6%) are false positives - messages that contain "damn" but are not actually toxic. The script reveals that context is critical: standalone "damn" often expresses surprise or mild frustration rather than toxicity, while phrases like "damn noob" or "goddamn" in angry contexts are more likely to be toxic. Simple substring matching cannot distinguish between friendly frustration ("damn it lol") and genuine harassment, leading to a high false positive rate that would frustrate users if implemented as-is.

### Examples of false positives:
- "damn it lol" - Friendly expression of frustration with laughter
- "well damn" - Expression of surprise, not aggressive
- "my shot missed the damn BC" - Frustration with gameplay, not directed at another player
- "damn he chose a good spot" - Complimentary statement

### Examples of correct flags:
- "damn noob" - Insult directed at another player
- "damn idiots noone?" - Calling other players idiots
- "fucking hate these goddamn maps anymore" - Aggressive language showing hostility

### Key Insight:
Simple substring matching catches many innocent uses of profanity because it cannot understand context, tone, or intent - demonstrating why more sophisticated approaches are needed for effective content moderation.
