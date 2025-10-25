**Solution** Let b stand for boy and g for girl. The sample space of the experiment is

$$S = \{(b, b), (g, b), (b, g), (g, g)\}$$

Let E and F denote the following events:

E: 'both the children are boys'

F: 'at least one of the child is a boy'

Then 
$$E = \{(b,b)\} \text{ and } F = \{(b,b), (g,b), (b,g)\}$$
 Now 
$$E \cap F = \{(b,b)\}$$
 Thus 
$$P(F) = \frac{3}{4} \text{ and } P(E \cap F) = \frac{1}{4}$$

Therefore  $P(E|F) = \frac{P(E \cap F)}{P(F)} = \frac{\frac{1}{4}}{\frac{3}{4}} = \frac{1}{3}$ 

**Example 3** Ten cards numbered 1 to 10 are placed in a box, mixed up thoroughly and then one card is drawn randomly. If it is known that the number on the drawn card is more than 3, what is the probability that it is an even number?

**Solution** Let A be the event 'the number on the card drawn is even' and B be the event 'the number on the card drawn is greater than 3'. We have to find P(A|B).

Now, the sample space of the experiment is  $S = \{1, 2, 3, 4, 5, 6, 7, 8, 9, 10\}$ 

Then 
$$A = \{2, 4, 6, 8, 10\}, B = \{4, 5, 6, 7, 8, 9, 10\}$$
 and 
$$A \cap B = \{4, 6, 8, 10\}$$
 Also 
$$P(A) = \frac{5}{10}, P(B) = \frac{7}{10} \text{ and } P(A \cap B) = \frac{4}{10}$$

Then  $P(A|B) = \frac{P(A \cap B)}{P(B)} = \frac{\frac{4}{10}}{\frac{7}{10}} = \frac{4}{7}$ 

**Example 4** In a school, there are 1000 students, out of which 430 are girls. It is known that out of 430, 10% of the girls study in class XII. What is the probability that a student chosen randomly studies in Class XII given that the chosen student is a girl?

**Solution** Let E denote the event that a student chosen randomly studies in Class XII and F be the event that the randomly chosen student is a girl. We have to find P (EIF).

$$P(E \cap F) = \frac{2}{36}$$

Hence, the required probability

$$P(E|F) = \frac{P(E \cap F)}{P(F)} = \frac{\frac{2}{36}}{\frac{5}{36}} = \frac{2}{5}$$

For the conditional probability discussed above, we have considered the elementary events of the experiment to be equally likely and the corresponding definition of the probability of an event was used. However, the same definition can also be used in the general case where the elementary events of the sample space are not equally likely, the probabilities  $P(E \cap F)$  and P(F) being calculated accordingly. Let us take up the following example.

Example 7 Consider the experiment of tossing a coin. If the coin shows head, toss it again but if it shows tail, then throw a die. Find the conditional probability of the event that 'the die shows a number greater than 4' given that 'there is at least one tail' (H,T)

**Solution** The outcomes of the experiment can be represented in following diagrammatic manner called the 'tree diagram'.

The sample space of the experiment may be described as

$$S = \{(H,H), (H,T), (T,1), (T,2), (T,3), (T,4), (T,5), (T,6)\}$$

where (H, H) denotes that both the tosses result into head and (T, i) denote the first toss result into a tail and the number i appeared on the die for i = 1,2,3,4,5,6.

Thus, the probabilities assigned to the 8 elementary events

$$(H, H), (H, T), (T, 1), (T, 2), (T, 3), (T, 4), (T, 5), (T, 6)$$

are 
$$\frac{1}{4}$$
,  $\frac{1}{4}$ ,  $\frac{1}{12}$ ,  $\frac{1}{12}$ ,  $\frac{1}{12}$ ,  $\frac{1}{12}$ ,  $\frac{1}{12}$  respectively which is clear from the Fig 13.2.

![](_page_1_Figure_16.jpeg)

$$P(X = 9) = P({(3,6), (4,5), (5,4), (6,3)}) = \frac{4}{36}$$

$$P(X = 10) = P({(4,6), (5,5), (6,4)}) = \frac{3}{36}$$

$$P(X = 11) = P({(5,6), (6,5)}) = \frac{2}{36}$$

$$P(X = 12) = P({(6,6)}) = \frac{1}{36}$$

The probability distribution of X is

| $\mathbf{X}$ or $\mathbf{x}_i$ | 2              | 3              | 4              | 5              | 6              | 7              | 8              | 9              | 10             | 11             | 12             |
|--------------------------------|----------------|----------------|----------------|----------------|----------------|----------------|----------------|----------------|----------------|----------------|----------------|
| $P(X)$ or $p_i$                | $\frac{1}{36}$ | $\frac{2}{36}$ | $\frac{3}{36}$ | $\frac{4}{36}$ | $\frac{5}{36}$ | $\frac{6}{36}$ | $\frac{5}{36}$ | $\frac{4}{36}$ | $\frac{3}{36}$ | $\frac{2}{36}$ | $\frac{1}{36}$ |

Therefore,

$$\mu = E(X) = \sum_{i=1}^{n} x_i p_i = 2 \times \frac{1}{36} + 3 \times \frac{2}{36} + 4 \times \frac{3}{36} + 5 \times \frac{4}{36}$$

$$+ 6 \times \frac{5}{36} + 7 \times \frac{6}{36} + 8 \times \frac{5}{36} + 9 \times \frac{4}{36} + 10 \times \frac{3}{36} + 11 \times \frac{2}{36} + 12 \times \frac{1}{36}$$

$$= \frac{2 + 6 + 12 + 20 + 30 + 42 + 40 + 36 + 30 + 22 + 12}{36} = 7$$

Thus, the mean of the sum of the numbers that appear on throwing two fair dice is 7.

## 13.6.3 Variance of a random variable

The mean of a random variable does not give us information about the variability in the values of the random variable. In fact, if the variance is small, then the values of the random variable are close to the mean. Also random variables with different probability distributions can have equal means, as shown in the following distributions of X and Y.

| X    | 1             | 2             | 3             | 4             |
|------|---------------|---------------|---------------|---------------|
| P(X) | $\frac{1}{8}$ | $\frac{2}{8}$ | $\frac{3}{8}$ | $\frac{2}{8}$ |

| Y    | -1            | 0             | 4             | 5             | 6             |
|------|---------------|---------------|---------------|---------------|---------------|
| P(Y) | $\frac{1}{8}$ | $\frac{2}{8}$ | $\frac{3}{8}$ | $\frac{1}{8}$ | $\frac{1}{8}$ |

Clearly 
$$E(X) = 1 \times \frac{1}{8} + 2 \times \frac{2}{8} + 3 \times \frac{3}{8} + 4 \times \frac{2}{8} = \frac{22}{8} = 2.75$$

and 
$$E(Y) = -1 \times \frac{1}{8} + 0 \times \frac{2}{8} + 4 \times \frac{3}{8} + 5 \times \frac{1}{8} = 6 \times \frac{1}{8} = \frac{22}{8} = 2.75$$

The variables X and Y are different, however their means are same. It is also easily observable from the diagramatic representation of these distributions (Fig 13.5).

![](_page_3_Figure_5.jpeg)

To distinguish X from Y, we require a measure of the extent to which the values of the random variables spread out. In Statistics, we have studied that the variance is a measure of the spread or scatter in data. Likewise, the variability or spread in the values of a random variable may be measured by variance.

**Definition 7** Let X be a random variable whose possible values  $x_1, x_2,...,x_n$  occur with probabilities  $p(x_1), p(x_2),..., p(x_n)$  respectively.

Let  $\mu = E(X)$  be the mean of X. The variance of X, denoted by Var(X) or  $\sigma_x^2$  is defined as

$$\sigma_x^2 = \text{Var}(X) = \sum_{i=1}^n (x_i - \mu)^2 p(x_i)$$

or equivalently  $\sigma_x^2 = E(X - \mu)^2$