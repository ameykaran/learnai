# 🎲 Lesson: Introduction to Probability

## 1. What is Probability?
Probability measures how likely an event is to occur. It is a number between **0** and **1**:
- **0** means the event will *never* happen.
- **1** means the event will *certainly* happen.

For any event **A**:

\[ P(A) = \frac{\text{Number of favorable outcomes}}{\text{Total number of possible outcomes}} \]

---

## 2. Basic Terminology

| Term | Definition | Example |
|------|-------------|----------|
| **Experiment** | A process that leads to an outcome | Rolling a die |
| **Sample Space (S)** | The set of all possible outcomes | {1, 2, 3, 4, 5, 6} |
| **Event (A)** | A subset of the sample space | {2, 4, 6} → even numbers |
| **Outcome** | A single result from the experiment | Rolling a 4 |

---

## 3. Types of Probability

### (a) **Theoretical Probability**
Calculated by reasoning or symmetry:
\[ P(A) = \frac{\text{favorable outcomes}}{\text{total outcomes}} \]

Example: Probability of getting a 3 when rolling a fair die:
\[ P(3) = \frac{1}{6} \]

### (b) **Experimental Probability**
Based on observation or experiment:
\[ P(A) = \frac{\text{Number of times A occurred}}{\text{Total number of trials}} \]

### (c) **Subjective Probability**
Based on intuition, belief, or experience.

Example: Probability that it rains tomorrow (based on weather forecast).

---

## 4. Complementary Events
For any event **A**, the probability that **A does not occur** is:
\[ P(A') = 1 - P(A) \]

Example: If \( P(A) = 0.3 \), then \( P(A') = 1 - 0.3 = 0.7 \).

---

## 5. Independent and Dependent Events

| Type | Definition | Example |
|------|-------------|----------|
| **Independent** | One event does not affect the other | Rolling two dice |
| **Dependent** | One event affects the other | Drawing two cards without replacement |

For independent events **A** and **B**:
\[ P(A \text{ and } B) = P(A) \times P(B) \]

---

## 6. Conditional Probability
The probability of **A** given that **B** has already occurred:
\[ P(A|B) = \frac{P(A \cap B)}{P(B)} \]

Example: If 40% of students play sports, and 25% both play sports and play chess, then:
\[ P(\text{Chess | Sports}) = \frac{0.25}{0.40} = 0.625 \]

---

## 7. Addition Rule of Probability
For any two events **A** and **B**:
\[ P(A \cup B) = P(A) + P(B) - P(A \cap B) \]

If **A** and **B** are mutually exclusive (cannot happen together):
\[ P(A \cup B) = P(A) + P(B) \]

---

## 8. Law of Total Probability
If events \( A_1, A_2, \ldots, A_n \) are mutually exclusive and exhaustive:
\[ P(B) = P(A_1)P(B|A_1) + P(A_2)P(B|A_2) + \ldots + P(A_n)P(B|A_n) \]

---

## 9. Bayes’ Theorem
Used to update probabilities based on new information:
\[ P(A|B) = \frac{P(B|A)P(A)}{P(B)} \]

Example: In medical testing, it helps find the probability a patient actually has a disease given a positive test.

---

## 10. Random Variables
A **random variable** assigns a numerical value to outcomes of a random process.
- **Discrete:** Finite number of outcomes (e.g., dice rolls)
- **Continuous:** Infinite outcomes within an interval (e.g., height, time)

### Expected Value (Mean):
\[ E(X) = \sum x_i P(x_i) \]

---

## 11. Common Probability Distributions

| Distribution | Type | Example |
|---------------|------|----------|
| **Bernoulli** | Discrete | Success/Failure |
| **Binomial** | Discrete | Number of successes in n trials |
| **Poisson** | Discrete | Number of events in fixed time |
| **Uniform** | Continuous | Equal likelihood in a range |
| **Normal (Gaussian)** | Continuous | Heights, test scores |

---

## 12. Practice Problems

1. A fair coin is tossed twice. Find the probability of getting:
   - (a) Two heads
   - (b) At least one head

2. A bag contains 3 red, 4 blue, and 5 green balls. One ball is picked at random. Find the probability that it is:
   - (a) Red
   - (b) Not blue

3. The probability that it rains on Monday is 0.6 and on Tuesday is 0.5. Assuming independence, find the probability it rains on both days.

---

## 13. Summary Table

| Concept | Formula |
|----------|----------|
| Complement | \( P(A') = 1 - P(A) \) |
| Intersection (AND) | \( P(A \cap B) = P(A)P(B) \) (if independent) |
| Union (OR) | \( P(A \cup B) = P(A) + P(B) - P(A \cap B) \) |
| Conditional | \( P(A|B) = \frac{P(A \cap B)}{P(B)} \) |
| Bayes’ Theorem | \( P(A|B) = \frac{P(B|A)P(A)}{P(B)} \) |

---

## 14. References
- Sheldon Ross, *A First Course in Probability*
- Blitzstein & Hwang, *Introduction to Probability*
- Khan Academy: [https://www.khanacademy.org/math/statistics-probability](https://www.khanacademy.org/math/statistics-probability)

---

> **Tip:** Always start by identifying the sample space and defining the event clearly before applying any formula.

