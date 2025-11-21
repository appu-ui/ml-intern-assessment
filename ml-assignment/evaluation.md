**1\. Storing N-gram Counts**
-----------------------------

The trigram counts are stored using a **nested dictionary**, where:

-   The **outer dictionary** key is a tuple `(w1, w2)` representing a 2-word context.

-   The **inner dictionary** maps the possible next word `w3` to the number of times it appears after that context.

Example structure:

`{
    ("i", "love"): { "python": 2, "coding": 1 },
    ("love", "python"): { "</s>": 1 }
}`

### **Why this design?**

-   Fast O(1) lookup for contexts and next-word counts.

-   Easy to extend to higher-order n-grams.

-   Matches standard NLP practices for n-gram language models.

-   Works smoothly with probabilistic sampling during text generation.

* * * * *

**2\. Text Cleaning and Tokenization**
--------------------------------------

Before training, the input text is processed in several stages:

### **Lowercasing**

All characters are converted to lowercase to eliminate case-based duplicates (e.g., "Hello" vs "hello").

### **Punctuation Handling**

Non-alphanumeric characters (except spaces) are replaced with spaces.\
This keeps only meaningful textual content and avoids introducing noisy tokens.

### **Tokenization**

The cleaned text is split using whitespace, producing a sequence of word tokens.

### **Padding with Special Tokens**

Two `<s>` tokens are added at the start of the text, and a `</s>` token is added at the end:

`["<s>", "<s>", token1, token2, ..., tokenN, "</s>"]`

Padding is needed so that:

-   The model can generate valid first and second words.

-   Sequence boundaries are properly represented.

* * * * *

**3\. Handling Unknown Words / Unseen Contexts**
------------------------------------------------

This implementation uses a **simple and practical strategy** for unknown contexts:

When generating text, if the model encounters a bigram `(w1, w2)` that never appeared during training, it performs a **fallback to a random known context**:

`if (w1, w2) not in trigram_counts:
    (w1, w2) = random.choice(list(trigram_counts.keys()))`

### **Why this approach?**

-   Prevents generation failures due to unseen word combinations.

-   Removes the need for explicit `<UNK>` tokens during training.

-   Keeps the code simple while ensuring robustness.

-   Allows continuous generation without early termination.

This acts as an effective unknown-word handling mechanism for assignment-level n-gram models.

* * * * *

**4\. Text Generation Strategy**
--------------------------------

The generation algorithm works as follows:

1.  **Initialization**\
    Start with the context `<s>, <s>`.

2.  **Context Lookup**\
    Retrieve all possible next words for the current context:

    `next_words = trigram_counts[(w1, w2)]`

3.  **Probabilistic Sampling**\
    Select the next word using frequency-weighted random choice:

    `random.choices(words, counts)[0]`

    This ensures that words occurring more frequently during training are more likely to be generated.

4.  **Stopping Condition**\
    If `</s>` is produced, the sentence is finished.

5.  **Context Shift**\
    Move the 2-word window forward:\
    `(w1, w2) → (w2, w3)`

6.  **Fallback Handling**\
    If a context does not exist, randomly choose another known context.

### **Why probabilistic sampling?**

-   Produces more natural and varied text.

-   Prevents repetitive or deterministic outputs.

-   Better reflects the statistical patterns learned from training data.

* * * * *

**5\. Additional Design Choices**
---------------------------------

-   No external NLP libraries were used to maintain transparency and simplicity.

-   The model avoids smoothing techniques (e.g., Laplace, Kneser-Ney) to focus on clear n-gram behavior.

-   The implementation is modular and easy to extend to higher-order n-grams or UNK vocab filtering.

-   The code is optimized for readability and educational value rather than raw performance.
