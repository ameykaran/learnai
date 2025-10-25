#!/usr/bin/env python3
"""
Mathematical Keyword Extractor using Custom NER + Fuzzy Matching
================================================================

This script trains a custom spaCy NER model to recognize mathematical keywords
from probability_keywords.csv and provides fuzzy matching fallback using RapidFuzz.
"""

import csv
import json
import random
import sqlite3
from pathlib import Path
from typing import List, Tuple, Dict, Set, Optional

import spacy
import pandas as pd
from spacy.training.example import Example
from spacy.util import minibatch, compounding
from rapidfuzz import fuzz, process
import numpy as np


class MathKeywordExtractor:
    """Extract mathematical keywords using NER + fuzzy matching."""

    def __init__(self, keywords_file: str = "probability_keywords.csv",
                 model_path: str = "math_ner_model"):
        self.keywords_file = keywords_file
        self.model_path = model_path
        self.keywords = self._load_keywords()
        self.nlp = None
        self.fuzzy_threshold = 80  # Minimum fuzzy match score

    def _load_keywords(self) -> List[str]:
        """Load keywords from CSV file."""
        keywords = []
        try:
            with open(self.keywords_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                for row in reader:
                    if row and row[0].strip():
                        keywords.append(row[0].strip())
        except FileNotFoundError:
            print(f"Error: {self.keywords_file} not found!")
            return []

        print(f"Loaded {len(keywords)} keywords from {self.keywords_file}")
        return keywords

    def generate_training_data(self, num_examples: int = 2000) -> List[Tuple[str, Dict]]:
        """Generate synthetic training data for NER."""
        training_data = []

        # Templates for generating diverse sentences
        templates = [
            "I want to learn about {keyword}",
            "Can you explain {keyword}?",
            "What is {keyword}?",
            "Tell me about {keyword}",
            "I need help with {keyword}",
            "How does {keyword} work?",
            "Could you help me understand {keyword}?",
            "I'm studying {keyword}",
            "Can you teach me {keyword}?",
            "I'm confused about {keyword}",
            "What's the definition of {keyword}?",
            "I want to know more about {keyword}",
            "Please explain {keyword} to me",
            "I need information on {keyword}",
            "Help me with {keyword}",
            "I'm learning about {keyword}",
            "Show me examples of {keyword}",
            "What are the applications of {keyword}?",
            "I want to understand {keyword} better",
            "Can you give me an overview of {keyword}?",
            "I'm researching {keyword}",
            "What is the concept of {keyword}?",
            "I need to study {keyword}",
            "Explain the theory behind {keyword}",
            "What are the principles of {keyword}?",
            "I want to master {keyword}",
            "How do I calculate {keyword}?",
            "What's involved in {keyword}?",
            "I'm working on {keyword}",
            "Can you clarify {keyword}?",
            # Multi-keyword templates
            "I need help with {keyword} and {keyword2}",
            "What's the difference between {keyword} and {keyword2}?",
            "How are {keyword} and {keyword2} related?",
            "I'm studying both {keyword} and {keyword2}",
            "Can you compare {keyword} with {keyword2}?",
        ]

        for _ in range(num_examples):
            template = random.choice(templates)

            if "{keyword2}" in template:
                # Multi-keyword sentence
                keyword1, keyword2 = random.sample(self.keywords, 2)
                text = template.format(keyword=keyword1, keyword2=keyword2)

                entities = []
                start1 = text.find(keyword1)
                start2 = text.find(keyword2)

                # Check for overlapping entities and skip if they overlap
                if start1 != -1 and start2 != -1:
                    end1 = start1 + len(keyword1)
                    end2 = start2 + len(keyword2)

                    # Check if entities overlap
                    if not (end1 <= start2 or end2 <= start1):
                        # Skip this example if entities overlap
                        continue

                    entities.append((start1, end1, "MATH_KEYWORD"))
                    entities.append((start2, end2, "MATH_KEYWORD"))
                elif start1 != -1:
                    entities.append((start1, start1 + len(keyword1), "MATH_KEYWORD"))
                elif start2 != -1:
                    entities.append((start2, start2 + len(keyword2), "MATH_KEYWORD"))

            else:
                # Single keyword sentence
                keyword = random.choice(self.keywords)
                text = template.format(keyword=keyword)

                start = text.find(keyword)
                entities = [(start, start + len(keyword), "MATH_KEYWORD")] if start != -1 else []

            training_data.append((text, {"entities": entities}))

        return training_data

    def train_ner_model(self, training_data: List[Tuple[str, Dict]],
                       n_iter: int = 30) -> None:
        """Train custom NER model."""
        print(f"Training NER model with {len(training_data)} examples...")

        # Create blank English model
        nlp = spacy.blank("en")

        # Add NER pipeline
        if "ner" not in nlp.pipe_names:
            ner = nlp.add_pipe("ner")
        else:
            ner = nlp.get_pipe("ner")

        # Add label
        ner.add_label("MATH_KEYWORD")

        # Convert training data to spaCy format
        examples = []
        for text, annotations in training_data:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            examples.append(example)

        # Initialize model
        nlp.initialize()

        # Training loop
        optimizer = nlp.create_optimizer()

        for i in range(n_iter):
            random.shuffle(examples)
            losses = {}

            # Batch the examples
            batches = minibatch(examples, size=compounding(4.0, 32.0, 1.001))

            for batch in batches:
                nlp.update(batch, drop=0.2, losses=losses, sgd=optimizer)

            if i % 10 == 0:
                print(f"Iteration {i}, Losses: {losses}")

        # Save model
        nlp.to_disk(self.model_path)
        print(f"Model saved to {self.model_path}")

        self.nlp = nlp

    def load_model(self) -> bool:
        """Load trained NER model."""
        try:
            self.nlp = spacy.load(self.model_path)
            print(f"Loaded model from {self.model_path}")
            return True
        except OSError:
            print(f"Model not found at {self.model_path}")
            return False

    def extract_keywords_ner(self, text: str) -> List[Tuple[str, float]]:
        """Extract keywords using NER model."""
        if not self.nlp:
            return []

        doc = self.nlp(text)
        keywords = []

        for ent in doc.ents:
            if ent.label_ == "MATH_KEYWORD":
                # Confidence score approximation based on entity length and position
                confidence = min(0.9, 0.5 + len(ent.text.split()) * 0.1)
                keywords.append((ent.text.lower().strip(), confidence))

        return keywords

    def extract_keywords_fuzzy(self, text: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """Extract keywords using fuzzy matching."""
        text_lower = text.lower()
        matches = []

        # Use RapidFuzz to find best matches
        results = process.extract(
            text_lower,
            self.keywords,
            scorer=fuzz.partial_ratio,
            limit=top_k
        )

        for result in results:
            keyword, score, _ = result
            if score >= self.fuzzy_threshold:
                # Normalize score to 0-1 range
                confidence = score / 100.0
                matches.append((keyword.lower(), confidence))

        return matches

    def extract_keywords(self, text: str, use_ner: bool = True,
                        use_fuzzy: bool = True, top_k: int = 5) -> List[Tuple[str, float]]:
        """Extract keywords using both NER and fuzzy matching."""
        all_keywords = {}

        # NER extraction
        if use_ner and self.nlp:
            ner_keywords = self.extract_keywords_ner(text)
            for keyword, confidence in ner_keywords:
                if keyword in all_keywords:
                    # Take maximum confidence
                    all_keywords[keyword] = max(all_keywords[keyword], confidence)
                else:
                    all_keywords[keyword] = confidence

        # Fuzzy matching as fallback
        if use_fuzzy:
            fuzzy_keywords = self.extract_keywords_fuzzy(text, top_k)
            for keyword, confidence in fuzzy_keywords:
                if keyword in all_keywords:
                    # Combine scores (weighted average, favoring NER)
                    existing_conf = all_keywords[keyword]
                    combined_conf = 0.7 * existing_conf + 0.3 * confidence
                    all_keywords[keyword] = combined_conf
                else:
                    # Add fuzzy result with slightly lower confidence
                    all_keywords[keyword] = confidence * 0.8

        # Sort by confidence and return top results
        sorted_keywords = sorted(all_keywords.items(), key=lambda x: x[1], reverse=True)
        return sorted_keywords[:top_k]



def main():
    """Main function to demonstrate the system."""
    extractor = MathKeywordExtractor()

    if not extractor.keywords:
        print("No keywords loaded. Exiting.")
        return

    # Try to load existing model
    if not extractor.load_model():
        print("Training new NER model...")
        training_data = extractor.generate_training_data(num_examples=500)
        extractor.train_ner_model(training_data, n_iter=10)


    print("\n" + "="*60)
    print("TESTING MATH KEYWORD EXTRACTION SYSTEM")
    print("="*60)

    for query in test_queries:
        print(f"\nQuery: '{query}'")
        print("-" * 40)

        # Extract keywords
        keywords = extractor.extract_keywords(query, top_k=3)
        print(f"Extracted keywords: {keywords}")

        if keywords:
            # Get just the keyword strings for retrieval
            keyword_strings = [kw[0] for kw in keywords]

            # Retrieve relevant chunks
            chunks = retriever.retrieve_chunks(keyword_strings, top_k=2)
            print(f"Retrieved {len(chunks)} relevant chunks:")

            for i, chunk in enumerate(chunks, 1):
                print(f"  {i}. Topic: {chunk['topic']}")
                print(f"     Content: {chunk['content'][:100]}...")
                print(f"     Matched: {chunk['matched_keyword']}")
        else:
            print("No keywords extracted.")

        print()


if __name__ == "__main__":
    main()