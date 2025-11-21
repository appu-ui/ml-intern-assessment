import random


class TrigramModel:
    def __init__(self):
        """
        Initializes the TrigramModel.
        """
        # TODO: Initialize any data structures you need to store the n-gram counts.

        # This dictionary will store trigram counts:
        # { (w1, w2): { next_word: count } }
        self.trigram_counts = {}

    def fit(self, text):
        """
        Trains the trigram model on the given text.

        Args:
            text (str): The text to train the model on.
        """

        # 1. Cleaning the text (convert to lowercase, remove punctuation)
        cleaned = ""
        for ch in text.lower():
            if ch.isalnum() or ch.isspace():
                cleaned += ch
            else:
                cleaned += " "

        # 2. Tokenizing the text into words
        words = cleaned.split()

        # 3. Padding the text with start and end tokens
        tokens = ["<s>", "<s>"] + words + ["</s>"]

        # 4. Counting the trigrams
        for i in range(len(tokens) - 2):
            w1, w2, w3 = tokens[i], tokens[i + 1], tokens[i + 2]

            # Create dict for (w1, w2) if not exists
            if (w1, w2) not in self.trigram_counts:
                self.trigram_counts[(w1, w2)] = {}

            # Increment count of w3
            if w3 not in self.trigram_counts[(w1, w2)]:
                self.trigram_counts[(w1, w2)][w3] = 0

            self.trigram_counts[(w1, w2)][w3] += 1

    def generate(self, max_length=50):
        """
        Generates new text using the trained trigram model.

        Args:
            max_length (int): The maximum length of the generated text.

        Returns:
            str: The generated text.
        """

        # 1. Start with start tokens
        w1, w2 = "<s>", "<s>"
        result = []

        # 2. Repeatedly choose next word based on trigram probabilities
        for _ in range(max_length):

            # If (w1, w2) not in model → stop
            if (w1, w2) not in self.trigram_counts:
                w1, w2 = random.choice(list(self.trigram_counts.keys()))

            next_words = self.trigram_counts[(w1, w2)]

            # Probabilistically choose next word
            words = list(next_words.keys())
            counts = list(next_words.values())
            w3 = random.choices(words, counts)[0]

            # 3. Stop if end token is reached
            if w3 == "</s>":
                break

            result.append(w3)

            # Shift window: (w1,w2) → (w2,w3)
            w1, w2 = w2, w3

        return " ".join(result)
