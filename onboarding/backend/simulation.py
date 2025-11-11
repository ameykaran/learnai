#!/usr/bin/env python3
"""
Simulation script to test the improved adaptive quiz algorithm.
Simulates 1000 users with different true abilities and measures classification accuracy.
"""

import random
import math
import sqlite3
import statistics
from typing import Dict, List, Tuple
from collections import defaultdict

# Simulation configuration
SIMULATION_SIZE = 1000
TRUE_ABILITY_CLUSTERS = [0.2, 0.5, 0.8]  # Low, Medium, High ability clusters
CLUSTER_WEIGHTS = [0.4, 0.35, 0.25]  # Distribution of users across clusters
NOISE_LEVEL = 0.1  # Random noise in true ability

class QuizSimulator:
    """Simulates quiz sessions with synthetic users having known true abilities."""

    def __init__(self, db_path: str = 'quiz.db'):
        self.db_path = db_path
        self.questions = self._load_questions()

        # Algorithm hyperparameters (same as implementation)
        self.ALPHA = 6.0
        self.LEARNING_RATE = 0.12
        self.INITIAL_EPSILON = 0.12
        self.INITIAL_ABILITY = 0.25
        self.MIN_MEDIUM = 4
        self.MIN_DIFFICULT = 2
        self.TOTAL_QUESTIONS = 25

        self.DIFFICULTY_SCORES = {
            'easy': 0.20,
            'medium': 0.50,
            'difficult': 0.80
        }

    def _load_questions(self) -> List[Dict]:
        """Load questions from database."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row

        cursor = conn.execute("""
            SELECT id, difficulty, correct_answer
            FROM questions
        """)

        questions = [dict(row) for row in cursor.fetchall()]
        conn.close()

        return questions

    def generate_true_ability(self) -> float:
        """Generate true ability for a synthetic user."""
        cluster = random.choices(TRUE_ABILITY_CLUSTERS, weights=CLUSTER_WEIGHTS)[0]
        noise = random.gauss(0, NOISE_LEVEL)
        return max(0.0, min(1.0, cluster + noise))

    def sigmoid(self, x: float) -> float:
        """Sigmoid function with overflow protection."""
        return 1.0 / (1.0 + math.exp(-max(-500, min(500, x))))

    def simulate_user_response(self, true_ability: float, question_difficulty: str) -> bool:
        """Simulate whether user answers question correctly based on true ability."""
        difficulty_score = self.DIFFICULTY_SCORES[question_difficulty]
        probability = self.sigmoid(self.ALPHA * (true_ability - difficulty_score))
        return random.random() < probability

    def expected_probability(self, ability: float, difficulty_score: float) -> float:
        """Expected probability of correct answer."""
        return self.sigmoid(self.ALPHA * (ability - difficulty_score))

    def update_ability(self, current_ability: float, outcome: bool, expected_prob: float) -> float:
        """Update ability estimate."""
        outcome_val = 1.0 if outcome else 0.0
        new_ability = current_ability + self.LEARNING_RATE * (outcome_val - expected_prob)
        return max(0.0, min(1.0, new_ability))

    def get_exploration_epsilon(self, question_count: int) -> float:
        """Calculate exploration rate."""
        return max(0.05, self.INITIAL_EPSILON * (1 - question_count / self.TOTAL_QUESTIONS))

    def select_next_difficulty(self, ability: float, question_count: int, medium_seen: int,
                              difficult_seen: int, remaining_questions: int) -> str:
        """Select next question difficulty using algorithm logic."""
        min_medium_remaining = max(0, self.MIN_MEDIUM - medium_seen)
        min_difficult_remaining = max(0, self.MIN_DIFFICULT - difficult_seen)

        # Force quota fulfillment
        if remaining_questions <= (min_medium_remaining + min_difficult_remaining):
            if min_difficult_remaining > 0:
                return 'difficult'
            elif min_medium_remaining > 0:
                return 'medium'

        # Exploration vs exploitation
        epsilon = self.get_exploration_epsilon(question_count - 1)

        if random.random() < epsilon:
            # Exploration: one level above
            if ability >= 0.7:
                return 'difficult'
            elif ability >= 0.35:
                return 'difficult' if random.random() < 0.7 else 'medium'
            else:
                return 'medium'
        else:
            # Exploitation: closest to ability + slight push
            target_score = min(1.0, ability + 0.05)
            distances = {
                difficulty: abs(score - target_score)
                for difficulty, score in self.DIFFICULTY_SCORES.items()
            }
            return min(distances, key=distances.get)

    def simulate_user_session(self, true_ability: float) -> Dict:
        """Simulate complete quiz session for one user."""
        ability = self.INITIAL_ABILITY
        asked_ids = []
        medium_seen = 0
        difficult_seen = 0
        total_correct = 0
        difficulty_stats = {'easy': {'correct': 0, 'total': 0},
                           'medium': {'correct': 0, 'total': 0},
                           'difficult': {'correct': 0, 'total': 0}}

        ability_trace = [ability]

        for question_num in range(1, self.TOTAL_QUESTIONS + 1):
            remaining = self.TOTAL_QUESTIONS - question_num + 1

            # Select difficulty
            target_difficulty = self.select_next_difficulty(
                ability, question_num, medium_seen, difficult_seen, remaining
            )

            # Get available questions of this difficulty
            available = [q for q in self.questions
                        if q['difficulty'] == target_difficulty and q['id'] not in asked_ids]

            if not available:
                # Fallback to any available
                available = [q for q in self.questions if q['id'] not in asked_ids]

            if not available:
                break  # No more questions

            question = random.choice(available)
            asked_ids.append(question['id'])

            # Track difficulty counts
            if target_difficulty == 'medium':
                medium_seen += 1
            elif target_difficulty == 'difficult':
                difficult_seen += 1

            # Simulate user response
            is_correct = self.simulate_user_response(true_ability, question['difficulty'])

            # Update algorithm's ability estimate
            difficulty_score = self.DIFFICULTY_SCORES[question['difficulty']]
            expected_prob = self.expected_probability(ability, difficulty_score)
            ability = self.update_ability(ability, is_correct, expected_prob)
            ability_trace.append(ability)

            # Track statistics
            if is_correct:
                total_correct += 1

            difficulty_stats[question['difficulty']]['total'] += 1
            if is_correct:
                difficulty_stats[question['difficulty']]['correct'] += 1

        # Final competence classification
        if ability < 0.35:
            final_competence = "easy"
        elif ability < 0.65:
            final_competence = "medium"
        else:
            final_competence = "difficult"

        return {
            'true_ability': true_ability,
            'estimated_ability': ability,
            'final_competence': final_competence,
            'total_correct': total_correct,
            'total_questions': len(asked_ids),
            'difficulty_stats': difficulty_stats,
            'medium_seen': medium_seen,
            'difficult_seen': difficult_seen,
            'ability_trace': ability_trace
        }

    def run_simulation(self) -> Dict:
        """Run full simulation with multiple users."""
        print(f"Running simulation with {SIMULATION_SIZE} users...")
        print(f"True ability clusters: {TRUE_ABILITY_CLUSTERS}")
        print(f"Cluster weights: {CLUSTER_WEIGHTS}")

        results = []

        for i in range(SIMULATION_SIZE):
            if (i + 1) % 100 == 0:
                print(f"Simulated {i + 1} users...")

            true_ability = self.generate_true_ability()
            session_result = self.simulate_user_session(true_ability)
            results.append(session_result)

        return self.analyze_results(results)

    def analyze_results(self, results: List[Dict]) -> Dict:
        """Analyze simulation results and compute metrics."""
        # Group by true ability clusters
        clusters = {
            'low': [r for r in results if r['true_ability'] < 0.35],
            'medium': [r for r in results if 0.35 <= r['true_ability'] < 0.65],
            'high': [r for r in results if r['true_ability'] >= 0.65]
        }

        # Classification confusion matrix
        confusion_matrix = defaultdict(lambda: defaultdict(int))
        for result in results:
            true_cluster = 'low' if result['true_ability'] < 0.35 else 'medium' if result['true_ability'] < 0.65 else 'high'
            pred_cluster = 'low' if result['final_competence'] == 'easy' else 'medium' if result['final_competence'] == 'medium' else 'high'
            confusion_matrix[true_cluster][pred_cluster] += 1

        # Calculate metrics per cluster
        cluster_metrics = {}
        for cluster_name, cluster_results in clusters.items():
            if not cluster_results:
                continue

            correct_classifications = {
                'low': sum(1 for r in cluster_results if r['final_competence'] == 'easy'),
                'medium': sum(1 for r in cluster_results if r['final_competence'] == 'medium'),
                'high': sum(1 for r in cluster_results if r['final_competence'] == 'difficult')
            }

            total = len(cluster_results)

            cluster_metrics[cluster_name] = {
                'count': total,
                'correct_easy': correct_classifications['low'] / total,
                'correct_medium': correct_classifications['medium'] / total,
                'correct_difficult': correct_classifications['high'] / total,
                'avg_true_ability': statistics.mean(r['true_ability'] for r in cluster_results),
                'avg_estimated_ability': statistics.mean(r['estimated_ability'] for r in cluster_results),
                'avg_medium_seen': statistics.mean(r['medium_seen'] for r in cluster_results),
                'avg_difficult_seen': statistics.mean(r['difficult_seen'] for r in cluster_results),
                'avg_total_correct': statistics.mean(r['total_correct'] for r in cluster_results)
            }

        # Overall accuracy
        total_correct_classifications = sum(
            confusion_matrix[true][true] for true in ['low', 'medium', 'high']
        )
        overall_accuracy = total_correct_classifications / len(results)

        # Target metrics for acceptance
        medium_high_classification_rate = 0
        if 'medium' in cluster_metrics:
            medium_high_classification_rate = (
                cluster_metrics['medium']['correct_medium'] +
                cluster_metrics['medium']['correct_difficult']
            )

        difficult_classification_rate = 0
        if 'high' in cluster_metrics:
            difficult_classification_rate = cluster_metrics['high']['correct_difficult']

        return {
            'confusion_matrix': dict(confusion_matrix),
            'cluster_metrics': cluster_metrics,
            'overall_accuracy': overall_accuracy,
            'medium_high_classification_rate': medium_high_classification_rate,
            'difficult_classification_rate': difficult_classification_rate,
            'total_simulations': len(results)
        }

def main():
    """Run simulation and print results."""
    simulator = QuizSimulator()

    # Check if questions are available
    if not simulator.questions:
        print("ERROR: No questions found in database. Make sure backend is initialized.")
        return

    print(f"Loaded {len(simulator.questions)} questions")

    # Count questions by difficulty
    difficulty_counts = defaultdict(int)
    for q in simulator.questions:
        difficulty_counts[q['difficulty']] += 1

    print("Question distribution:")
    for diff, count in difficulty_counts.items():
        print(f"  {diff}: {count}")

    # Run simulation
    results = simulator.run_simulation()

    # Print results
    print("\n" + "="*60)
    print("SIMULATION RESULTS")
    print("="*60)

    print(f"Total simulations: {results['total_simulations']}")
    print(f"Overall classification accuracy: {results['overall_accuracy']:.3f}")
    print(f"Medium users classified as medium/difficult: {results['medium_high_classification_rate']:.3f}")
    print(f"High users classified as difficult: {results['difficult_classification_rate']:.3f}")

    print("\nConfusion Matrix:")
    print("True\\Predicted    Low     Medium  High")
    for true_cluster in ['low', 'medium', 'high']:
        row = f"{true_cluster:12s}"
        for pred_cluster in ['low', 'medium', 'high']:
            count = results['confusion_matrix'][true_cluster][pred_cluster]
            row += f"{count:8d}"
        print(row)

    print("\nCluster Analysis:")
    for cluster_name, metrics in results['cluster_metrics'].items():
        print(f"\n{cluster_name.upper()} ABILITY USERS (n={metrics['count']}):")
        print(f"  Avg true ability: {metrics['avg_true_ability']:.3f}")
        print(f"  Avg estimated ability: {metrics['avg_estimated_ability']:.3f}")
        print(f"  Avg questions correct: {metrics['avg_total_correct']:.1f}/25")
        print(f"  Avg medium questions seen: {metrics['avg_medium_seen']:.1f}")
        print(f"  Avg difficult questions seen: {metrics['avg_difficult_seen']:.1f}")
        print(f"  Classified as easy: {metrics['correct_easy']:.3f}")
        print(f"  Classified as medium: {metrics['correct_medium']:.3f}")
        print(f"  Classified as difficult: {metrics['correct_difficult']:.3f}")

    print("\nACCEPTANCE CRITERIA:")
    print(f"✓ Medium users classified medium/difficult ≥60%: {results['medium_high_classification_rate']:.1%} {'✓' if results['medium_high_classification_rate'] >= 0.6 else '✗'}")
    print(f"✓ High users classified difficult ≥75%: {results['difficult_classification_rate']:.1%} {'✓' if results['difficult_classification_rate'] >= 0.75 else '✗'}")

if __name__ == "__main__":
    main()