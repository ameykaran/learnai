![](_page_0_Picture_0.jpeg)

Chapter 13

# **PROBABILITY**

❖ The theory of probabilities is simply the Science of logic quantitatively treated. – C.S. PEIRCE ❖

## 13.1 Introduction

In earlier Classes, we have studied the probability as a measure of uncertainty of events in a random experiment. We discussed the axiomatic approach formulated by Russian Mathematician, A.N. Kolmogorov (1903-1987) and treated probability as a function of outcomes of the experiment. We have also established equivalence between the axiomatic theory and the classical theory of probability in case of equally likely outcomes. On the basis of this relationship, we obtained probabilities of events associated with discrete sample spaces. We have also studied the addition rule of probability. In this chapter, we shall discuss the important concept of conditional probability of an event given that another event has occurred, which will be helpful in understanding the Bayes' theorem, multiplication rule of probability and independence of events. We shall also learn an important concept of random variable and its probability

![](_page_0_Picture_6.jpeg)

Pierre de Fermat (1601-1665)

distribution and also the mean and variance of a probability distribution. In the last section of the chapter, we shall study an important discrete probability distribution called Binomial distribution. Throughout this chapter, we shall take up the experiments having equally likely outcomes, unless stated otherwise.

## 13.2 Conditional Probability

Uptill now in probability, we have discussed the methods of finding the probability of events. If we have two events from the same sample space, does the information about the occurrence of one of the events affect the probability of the other event? Let us try to answer this question by taking up a random experiment in which the outcomes are equally likely to occur.

Consider the experiment of tossing three fair coins. The sample space of the experiment is

 $S = \{HHH, HHT, HTH, THH, HTT, THT, TTH, TTT\}$ 

Since the coins are fair, we can assign the probability  $\frac{1}{8}$  to each sample point. Let

E be the event 'at least two heads appear' and F be the event 'first coin shows tail'. Then

$$E = \{HHH, HHT, HTH, THH\}$$
and 
$$F = \{THH, THT, TTH, TTT\}$$
Therefore 
$$P(E) = P(\{HHH\}) + P(\{HHT\}) + P(\{HTH\}) + P(\{THH\})$$

$$= \frac{1}{8} + \frac{1}{8} + \frac{1}{8} + \frac{1}{8} = \frac{1}{2} \text{ (Why ?)}$$
and 
$$P(F) = P(\{THH\}) + P(\{THT\}) + P(\{TTT\}) + P(\{TTT\})$$

$$= \frac{1}{8} + \frac{1}{8} + \frac{1}{8} + \frac{1}{8} = \frac{1}{2}$$
Also 
$$E \cap F = \{THH\}$$
with 
$$P(E \cap F) = P(\{THH\}) = \frac{1}{8}$$

Now, suppose we are given that the first coin shows tail, i.e. F occurs, then what is the probability of occurrence of E? With the information of occurrence of F, we are sure that the cases in which first coin does not result into a tail should not be considered while finding the probability of E. This information reduces our sample space from the set S to its subset F for the event E. In other words, the additional information really amounts to telling us that the situation may be considered as being that of a new random experiment for which the sample space consists of all those outcomes only which are favourable to the occurrence of the event F.

Now, the sample point of F which is favourable to event E is THH.

Thus, Probability of E considering F as the sample space =  $\frac{1}{4}$ ,

or Probability of E given that the event F has occurred = 
$$\frac{1}{4}$$

This probability of the event E is called the *conditional probability of E given* that F has already occurred, and is denoted by P (EIF).

Thus 
$$P(E|F) = \frac{1}{4}$$

Note that the elements of F which favour the event E are the common elements of E and F, i.e. the sample points of  $E \cap F$ .

Thus, we can also write the conditional probability of E given that F has occurred as

$$P(E|F) = \frac{\text{Number of elementary events favourable to } E \cap F}{\text{Number of elementary events which are favourable to } F}$$
$$= \frac{n(E \cap F)}{n(F)}$$

Dividing the numerator and the denominator by total number of elementary events of the sample space, we see that P(EIF) can also be written as

$$P(E|F) = \frac{\frac{n(E \cap F)}{n(S)}}{\frac{n(F)}{n(S)}} = \frac{P(E \cap F)}{P(F)} \qquad \dots (1)$$

Note that (1) is valid only when  $P(F) \neq 0$  i.e.,  $F \neq \emptyset$  (Why?)

Thus, we can define the conditional probability as follows:

**Definition 1** If E and F are two events associated with the same sample space of a random experiment, the conditional probability of the event E given that F has occurred, i.e. P (EIF) is given by

$$P(E|F) = \frac{P(E \cap F)}{P(F)}$$
 provided  $P(F) \neq 0$ 

## 13.2.1 Properties of conditional probability

Let E and F be events of a sample space S of an experiment, then we have

**Property 1** P(S|F) = P(F|F) = 1

We know that

$$P(S|F) = \frac{P(S \cap F)}{P(F)} = \frac{P(F)}{P(F)} = 1$$

Also

$$P(F|F) = \frac{P(F \cap F)}{P(F)} = \frac{P(F)}{P(F)} = 1$$

Thus

$$P(S|F) = P(F|F) = 1$$

**Property 2** If A and B are any two events of a sample space S and F is an event of S such that  $P(F) \neq 0$ , then

$$P((A \cup B)|F) = P(A|F) + P(B|F) - P((A \cap B)|F)$$

In particular, if A and B are disjoint events, then

$$P((A \cup B)|F) = P(A|F) + P(B|F)$$

We have

$$\begin{split} P((A \cup B)|F) &= \frac{P[(A \cup B) \cap F]}{P(F)} \\ &= \frac{P[(A \cap F) \cup (B \cap F)]}{P(F)} \end{split}$$

(by distributive law of union of sets over intersection)

$$= \frac{P(A \cap F) + P(B \cap F) - P(A \cap B \cap F)}{P(F)}$$

$$= \frac{P(A \cap F)}{P(F)} + \frac{P(B \cap F)}{P(F)} - \frac{P[(A \cap B) \cap F]}{P(F)}$$

$$= P(A|F) + P(B|F) - P((A \cap B)|F)$$

When A and B are disjoint events, then

$$P((A \cap B)|F) = 0$$

$$\Rightarrow P((A \cup B)|F) = P(A|F) + P(B|F)$$

**Property 3** P(E'|F) = 1 - P(E|F)

From Property 1, we know that P(S|F) = 1

$$\Rightarrow \qquad \qquad P(E \cup E'|F) = 1 \qquad \text{since } S = E \cup E'$$
 
$$\Rightarrow \qquad P(E|F) + P(E'|F) = 1 \qquad \text{since E and E' are disjoint events}$$
 Thus, 
$$P(E'|F) = 1 - P(E|F)$$

Let us now take up some examples.

**Example 1** If 
$$P(A) = \frac{7}{13}$$
,  $P(B) = \frac{9}{13}$  and  $P(A \cap B) = \frac{4}{13}$ , evaluate  $P(A|B)$ .

Solution We have 
$$P(A|B) = \frac{P(A \cap B)}{P(B)} = \frac{\frac{4}{13}}{\frac{9}{13}} = \frac{4}{9}$$

**Example 2** A family has two children. What is the probability that both the children are boys given that at least one of them is a boy ?

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

Then 
$$P(A|B) = \frac{P(A \cap B)}{P(B)} = \frac{\frac{4}{10}}{\frac{7}{10}} = \frac{4}{7}$$

**Example 4** In a school, there are 1000 students, out of which 430 are girls. It is known that out of 430, 10% of the girls study in class XII. What is the probability that a student chosen randomly studies in Class XII given that the chosen student is a girl?

**Solution** Let E denote the event that a student chosen randomly studies in Class XII and F be the event that the randomly chosen student is a girl. We have to find P (EIF).

Now 
$$P(F) = \frac{430}{1000} = 0.43 \text{ and } P(E \cap F) = \frac{43}{1000} = 0.043 \text{ (Why?)}$$
Then 
$$P(E|F) = \frac{P(E \cap F)}{P(F)} = \frac{0.043}{0.43} = 0.1$$

**Example 5** A die is thrown three times. Events A and B are defined as below:

A: 4 on the third throw

B: 6 on the first and 5 on the second throw

Find the probability of A given that B has already occurred.

**Solution** The sample space has 216 outcomes.

Now 
$$A = \begin{cases} (1,1,4) & (1,2,4) \dots (1,6,4) & (2,1,4) & (2,2,4) \dots (2,6,4) \\ (3,1,4) & (3,2,4) & \dots (3,6,4) & (4,1,4) & (4,2,4) & \dots (4,6,4) \\ (5,1,4) & (5,2,4) & \dots & (5,6,4) & (6,1,4) & (6,2,4) & \dots (6,6,4) \end{cases}$$

$$B = \{(6,5,1), (6,5,2), (6,5,3), (6,5,4), (6,5,5), (6,5,6)\}$$
and 
$$A \cap B = \{(6,5,4)\}.$$

$$P(B) = \frac{6}{216} \text{ and } P(A \cap B) = \frac{1}{216}$$
Then 
$$P(A|B) = \frac{P(A \cap B)}{P(B)} = \frac{\frac{1}{216}}{\frac{6}{216}} = \frac{1}{6}$$

**Example 6** A die is thrown twice and the sum of the numbers appearing is observed to be 6. What is the conditional probability that the number 4 has appeared at least once?

**Solution** Let E be the event that 'number 4 appears at least once' and F be the event that 'the sum of the numbers appearing is 6'.

Then, 
$$E = \{(4,1), (4,2), (4,3), (4,4), (4,5), (4,6), (1,4), (2,4), (3,4), (5,4), (6,4)\}$$
 and 
$$F = \{(1,5), (2,4), (3,3), (4,2), (5,1)\}$$
 We have 
$$P(E) = \frac{11}{36} \text{ and } P(F) = \frac{5}{36}$$
 Also 
$$E \cap F = \{(2,4), (4,2)\}$$

$$P(E \cap F) = \frac{2}{36}$$

Hence, the required probability

$$P(E|F) = \frac{P(E \cap F)}{P(F)} = \frac{\frac{2}{36}}{\frac{5}{36}} = \frac{2}{5}$$

For the conditional probability discussed above, we have considered the elementary events of the experiment to be equally likely and the corresponding definition of the probability of an event was used. However, the same definition can also be used in the general case where the elementary events of the sample space are not equally likely, the probabilities  $P(E \cap F)$  and P(F) being calculated accordingly. Let us take up the following example.

Example 7 Consider the experiment of tossing a coin. If the coin shows head, toss it again but if it shows tail, then throw a die. Find the conditional probability of the event that 'the die shows a number greater than 4' given that 'there is at least one tail' (H,T)

**Solution** The outcomes of the experiment can be represented in following diagrammatic manner called the 'tree diagram'.

The sample space of the experiment may be described as

be ed 
$$Tail (T)$$
  $(T,1)$   $(T,2)$   $(T,3)$   $(T,4)$   $(T,5)$   $(T,6)$ 

$$S = \{(H,H), (H,T), (T,1), (T,2), (T,3), (T,4), (T,5), (T,6)\}$$

where (H, H) denotes that both the tosses result into head and (T, i) denote the first toss result into a tail and the number i appeared on the die for i = 1,2,3,4,5,6.

Thus, the probabilities assigned to the 8 elementary events

$$(H, H), (H, T), (T, 1), (T, 2), (T, 3), (T, 4), (T, 5), (T, 6)$$

are 
$$\frac{1}{4}$$
,  $\frac{1}{4}$ ,  $\frac{1}{12}$ ,  $\frac{1}{12}$ ,  $\frac{1}{12}$ ,  $\frac{1}{12}$ ,  $\frac{1}{12}$  respectively which is clear from the Fig 13.2.

![](_page_6_Figure_16.jpeg)

#### 538 MATHEMATICS

Let F be the event that 'there is at least one tail' and E be the event 'the die shows a number greater than 4'. Then

$$F = \{(H,T), (T,1), (T,2), (T,3), (T,4), (T,5), (T,6)\}$$

$$E = \{(T,5), (T,6)\} \text{ and } E \cap F = \{(T,5), (T,6)\}$$

$$P(F) = P(\{(H,T)\}) + P(\{(T,1)\}) + P(\{(T,2)\}) + P(\{(T,3)\})$$

$$+ P(\{(T,4)\}) + P(\{(T,5)\}) + P(\{(T,6)\})$$

$$= \frac{1}{4} + \frac{1}{12} + \frac{1}{12} + \frac{1}{12} + \frac{1}{12} + \frac{1}{12} + \frac{1}{12} = \frac{3}{4}$$
and 
$$P(E \cap F) = P(\{(T,5)\}) + P(\{(T,6)\}) = \frac{1}{12} + \frac{1}{12} = \frac{1}{6}$$

$$P(E|F) = \frac{P(E \cap F)}{P(F)} = \frac{\frac{1}{6}}{\frac{3}{4}} = \frac{2}{9}$$

Hence

# **EXERCISE 13.1**

- 1. Given that E and F are events such that P(E) = 0.6, P(F) = 0.3 and  $P(E \cap F) = 0.2$ , find P(E|F) and P(F|E)
- **2.** Compute P(A|B), if P(B) = 0.5 and P (A  $\cap$  B) = 0.32
- 3. If P(A) = 0.8, P(B) = 0.5 and P(B|A) = 0.4, find
  - (i)  $P(A \cap B)$
- (ii) P(A|B)
- (iii)  $P(A \cup B)$
- 4. Evaluate  $P(A \cup B)$ , if  $2P(A) = P(B) = \frac{5}{13}$  and  $P(A|B) = \frac{2}{5}$
- 5. If  $P(A) = \frac{6}{11}$ ,  $P(B) = \frac{5}{11}$  and  $P(A \cup B) = \frac{7}{11}$ , find
  - (i)  $P(A \cap B)$
- (ii) P(A|B)
- (iii) P(B|A)

Determine P(E|F) in Exercises 6 to 9.

- **6.** A coin is tossed three times, where
  - (i) E: head on third toss, F: heads on first two tosses
  - (ii) E: at least two heads , F: at most two heads
  - (iii) E: at most two tails , F: at least one tail

7. Two coins are tossed once, where

(i) E: tail appears on one coin, F: one coin shows head

(ii) E: no tail appears, F: no head appears

**8.** A die is thrown three times,

E: 4 appears on the third toss, F: 6 and 5 appears respectively on first two tosses

9. Mother, father and son line up at random for a family picture

E : son on one end, F : father in middle

- 10. A black and a red dice are rolled.
  - (a) Find the conditional probability of obtaining a sum greater than 9, given that the black die resulted in a 5.
  - (b) Find the conditional probability of obtaining the sum 8, given that the red die resulted in a number less than 4.
- 11. A fair die is rolled. Consider events  $E = \{1,3,5\}$ ,  $F = \{2,3\}$  and  $G = \{2,3,4,5\}$  Find
  - (i) P(E|F) and P(F|E)
- (ii) P(E|G) and P(G|E)
- (iii)  $P((E \cup F)|G)$  and  $P((E \cap F)|G)$
- 12. Assume that each born child is equally likely to be a boy or a girl. If a family has two children, what is the conditional probability that both are girls given that (i) the youngest is a girl, (ii) at least one is a girl?
- 13. An instructor has a question bank consisting of 300 easy True / False questions, 200 difficult True / False questions, 500 easy multiple choice questions and 400 difficult multiple choice questions. If a question is selected at random from the question bank, what is the probability that it will be an easy question given that it is a multiple choice question?
- **14.** Given that the two numbers appearing on throwing two dice are different. Find the probability of the event 'the sum of numbers on the dice is 4'.
- 15. Consider the experiment of throwing a die, if a multiple of 3 comes up, throw the die again and if any other number comes, toss a coin. Find the conditional probability of the event 'the coin shows a tail', given that 'at least one die shows a 3'.

In each of the Exercises 16 and 17 choose the correct answer:

**16.** If 
$$P(A) = \frac{1}{2}$$
,  $P(B) = 0$ , then  $P(A|B)$  is

(A) 0

(B)  $\frac{1}{2}$ 

(C) not defined

(D) 1

17. If A and B are events such that P(A|B) = P(B|A), then

- (A)  $A \subset B$  but  $A \neq B$
- (B) A = B

(C)  $A \cap B = \emptyset$ 

(D) P(A) = P(B)

# 13.3 Multiplication Theorem on Probability

Let E and F be two events associated with a sample space S. Clearly, the set  $E \cap F$  denotes the event that both E and F have occurred. In other words,  $E \cap F$  denotes the simultaneous occurrence of the events E and F. The event  $E \cap F$  is also written as EF.

Very often we need to find the probability of the event EF. For example, in the experiment of drawing two cards one after the other, we may be interested in finding the probability of the event 'a king and a queen'. The probability of event EF is obtained by using the conditional probability as obtained below:

We know that the conditional probability of event E given that F has occurred is denoted by P(EIF) and is given by

$$P(E|F) = \frac{P(E \cap F)}{P(F)}, P(F) \neq 0$$

From this result, we can write

$$P(E \cap F) = P(F) \cdot P(E|F)$$
 ... (1)

Also, we know that

$$P(F|E) = \frac{P(F \cap E)}{P(E)}, P(E) \neq 0$$

or

$$P(F|E) = \frac{P(E \cap F)}{P(E)} \text{ (since } E \cap F = F \cap E)$$

Thus,  $P(E \cap F) = P(E)$ . P(F|E) .... (2)

Combining (1) and (2), we find that

$$P(E \cap F) = P(E) \ P(F|E)$$
  
=  $P(F) \ P(E|F) \ provided \ P(E) \neq 0 \ and \ P(F) \neq 0.$ 

The above result is known as the *multiplication rule of probability*.

Let us now take up an example.

**Example 8** An urn contains 10 black and 5 white balls. Two balls are drawn from the urn one after the other without replacement. What is the probability that both drawn balls are black?

**Solution** Let E and F denote respectively the events that first and second ball drawn are black. We have to find  $P(E \cap F)$  or P(EF).

Now 
$$P(E) = P \text{ (black ball in first draw)} = \frac{10}{15}$$

Also given that the first ball drawn is black, i.e., event E has occurred, now there are 9 black balls and five white balls left in the urn. Therefore, the probability that the second ball drawn is black, given that the ball in the first draw is black, is nothing but the conditional probability of F given that E has occurred.

i.e. 
$$P(F|E) = \frac{9}{14}$$

By multiplication rule of probability, we have

$$P(E \cap F) = P(E) P(F|E)$$
$$= \frac{10}{15} \times \frac{9}{14} = \frac{3}{7}$$

*Multiplication rule of probability for more than two events* If E, F and G are three events of sample space, we have

$$P(E \cap F \cap G) = P(E) P(F|E) P(G|(E \cap F)) = P(E) P(F|E) P(G|EF)$$

Similarly, the multiplication rule of probability can be extended for four or more events.

The following example illustrates the extension of multiplication rule of probability for three events.

**Example 9** Three cards are drawn successively, without replacement from a pack of 52 well shuffled cards. What is the probability that first two cards are kings and the third card drawn is an ace?

**Solution** Let K denote the event that the card drawn is king and A be the event that the card drawn is an ace. Clearly, we have to find P (KKA)

Now 
$$P(K) = \frac{4}{52}$$

Also, P(K|K) is the probability of second king with the condition that one king has already been drawn. Now there are three kings in (52 - 1) = 51 cards.

Therefore 
$$P(K|K) = \frac{3}{51}$$

Lastly, P(AlKK) is the probability of third drawn card to be an ace, with the condition that two kings have already been drawn. Now there are four aces in left 50 cards.

Therefore

$$P(A|KK) = \frac{4}{50}$$

By multiplication law of probability, we have

$$P(KKA) = P(K)$$
  $P(K|K)$   $P(A|KK)$   
=  $\frac{4}{52} \times \frac{3}{51} \times \frac{4}{50} = \frac{2}{5525}$ 

## 13.4 Independent Events

Consider the experiment of drawing a card from a deck of 52 playing cards, in which the elementary events are assumed to be equally likely. If E and F denote the events 'the card drawn is a spade' and 'the card drawn is an ace' respectively, then

$$P(E) = \frac{13}{52} = \frac{1}{4}$$
 and  $P(F) = \frac{4}{52} = \frac{1}{13}$ 

Also E and F is the event 'the card drawn is the ace of spades' so that

$$P(E \cap F) = \frac{1}{52}$$

Hence

$$P(E|F) = \frac{P(E \cap F)}{P(F)} = \frac{\frac{1}{52}}{\frac{1}{13}} = \frac{1}{4}$$

Since  $P(E) = \frac{1}{4} = P$  (E|F), we can say that the occurrence of event F has not affected the probability of occurrence of the event E.

We also have

$$P(F|E) = \frac{P(E \cap F)}{P(E)} = \frac{\frac{1}{52}}{\frac{1}{4}} = \frac{1}{13} = P(F)$$

Again,  $P(F) = \frac{1}{13} = P(F|E)$  shows that occurrence of event E has not affected the probability of occurrence of the event F.

Thus, E and F are two events such that the probability of occurrence of one of them is not affected by occurrence of the other.

Such events are called independent events.

**Definition 2** Two events E and F are said to be independent, if

$$P(F|E) = P(F)$$
 provided  $P(E) \neq 0$ 

and

$$P(E|F) = P(E)$$
 provided  $P(F) \neq 0$ 

Thus, in this definition we need to have  $P(E) \neq 0$  and  $P(F) \neq 0$ 

Now, by the multiplication rule of probability, we have

$$P(E \cap F) = P(E) \cdot P(F|E) \qquad \dots (1)$$

If E and F are independent, then (1) becomes

$$P(E \cap F) = P(E) \cdot P(F) \qquad \dots (2)$$

Thus, using (2), the independence of two events is also defined as follows:

**Definition 3** Let E and F be two events associated with the same random experiment, then E and F are said to be independent if

$$P(E \cap F) = P(E) \cdot P(F)$$

## Remarks

- (i) Two events E and F are said to be dependent if they are not independent, i.e. if  $P(E \cap F) \neq P(E)$ . P (F)
- (ii) Sometimes there is a confusion between independent events and mutually exclusive events. Term 'independent' is defined in terms of 'probability of events' whereas mutually exclusive is defined in term of events (subset of sample space). Moreover, mutually exclusive events never have an outcome common, but independent events, may have common outcome. Clearly, 'independent' and 'mutually exclusive' do not have the same meaning.
  - In other words, two independent events having nonzero probabilities of occurrence can not be mutually exclusive, and conversely, i.e. two mutually exclusive events having nonzero probabilities of occurrence can not be independent.
- (iii) Two experiments are said to be independent if for every pair of events E and F, where E is associated with the first experiment and F with the second experiment, the probability of the simultaneous occurrence of the events E and F when the two experiments are performed is the product of P(E) and P(F) calculated separately on the basis of two experiments, i.e.,  $P(E \cap F) = P(E) \cdot P(F)$
- (iv) Three events A, B and C are said to be mutually independent, if

$$P(A \cap B) = P(A) P(B)$$

$$P(A \cap C) = P(A) P(C)$$

$$P(B \cap C) = P(B) P(C)$$

$$P(A \cap B \cap C) = P(A) P(B) P(C)$$

and

#### 544 MATHEMATICS

If at least one of the above is not true for three given events, we say that the events are not independent.

**Example 10** A die is thrown. If E is the event 'the number appearing is a multiple of 3' and F be the event 'the number appearing is even' then find whether E and F are independent?

**Solution** We know that the sample space is  $S = \{1, 2, 3, 4, 5, 6\}$ 

Now  $E = \{3, 6\}, F = \{2, 4, 6\} \text{ and } E \cap F = \{6\}$ 

Then  $P(E) = \frac{2}{6} = \frac{1}{3}$ ,  $P(F) = \frac{3}{6} = \frac{1}{2}$  and  $P(E \cap F) = \frac{1}{6}$ 

Clearly  $P(E \cap F) = P(E)$ . P(F)

Hence E and F are independent events.

**Example 11** An unbiased die is thrown twice. Let the event A be 'odd number on the first throw' and B the event 'odd number on the second throw'. Check the independence of the events A and B.

**Solution** If all the 36 elementary events of the experiment are considered to be equally likely, we have

$$P(A) = \frac{18}{36} = \frac{1}{2} \text{ and } P(B) = \frac{18}{36} = \frac{1}{2}$$

Also

 $P(A \cap B) = P \text{ (odd number on both throws)}$ 

$$=\frac{9}{36}=\frac{1}{4}$$

Now

$$P(A) P(B) = \frac{1}{2} \times \frac{1}{2} = \frac{1}{4}$$

Clearly

$$P(A \cap B) = P(A) \times P(B)$$

Thus.

A and B are independent events

**Example 12** Three coins are tossed simultaneously. Consider the event E 'three heads or three tails', F 'at least two heads' and G 'at most two heads'. Of the pairs (E,F), (E,G) and (F,G), which are independent? which are dependent?

**Solution** The sample space of the experiment is given by

 $S = \{HHH, HHT, HTH, THH, HTT, THT, TTH, TTT\}$ 

Clearly  $E = \{HHH, TTT\}, F = \{HHH, HHT, HTH, THH\}$ 

and 
$$G = \{HHT, HTH, THH, HTT, THT, TTH, TTT\}$$
Also  $E \cap F = \{HHH\}, E \cap G = \{TTT\}, F \cap G = \{HHT, HTH, THH\}$ 
Therefore  $P(E) = \frac{2}{8} = \frac{1}{4}, P(F) = \frac{4}{8} = \frac{1}{2}, P(G) = \frac{7}{8}$ 
and  $P(E \cap F) = \frac{1}{8}, P(E \cap G) = \frac{1}{8}, P(F \cap G) = \frac{3}{8}$ 
Also  $P(E) \cdot P(F) = \frac{1}{4} \times \frac{1}{2} = \frac{1}{8}, P(E) \cdot P(G) = \frac{1}{4} \times \frac{7}{8} = \frac{7}{32}$ 
and  $P(F) \cdot P(G) = \frac{1}{2} \times \frac{7}{8} = \frac{7}{16}$ 
Thus  $P(E \cap F) = P(E) \cdot P(F)$ 
 $P(E \cap G) \neq P(E) \cdot P(G)$ 
and  $P(F \cap G) \neq P(F) \cdot P(G)$ 

Hence, the events (E and F) are independent, and the events (E and G) and (F and G) are dependent.

**Example 13** Prove that if E and F are independent events, then so are the events E and F'.

**Solution** Since E and F are independent, we have

$$P(E \cap F) = P(E) \cdot P(F) \qquad \dots (1)$$

From the venn diagram in Fig 13.3, it is clear that  $E \cap F$  and  $E \cap F'$  are mutually exclusive events and also  $E = (E \cap F) \cup (E \cap F')$ .

Therefore  $P(E) = P(E \cap F) + P(E \cap F')$ or  $P(E \cap F') = P(E) - P(E \cap F)$   $= P(E) - P(E) \cdot P(F)$  (by (1)) = P(E) (1-P(F))

= P(E). P(F')

Hence, E and F' are independent

![](_page_14_Picture_11.jpeg)

Fig 13.3

Note In a similar manner, it can be shown that if the events E and F are independent, then

- (a) E' and F are independent,
- (b) E' and F' are independent

**Example 14** If A and B are two independent events, then the probability of occurrence of at least one of A and B is given by 1 - P(A') P(B')

## **Solution** We have

P(at least one of A and B) = 
$$P(A \cup B)$$
  
=  $P(A) + P(B) - P(A \cap B)$   
=  $P(A) + P(B) - P(A) P(B)$   
=  $P(A) + P(B) [1-P(A)]$   
=  $P(A) + P(B) P(A')$   
=  $P(A') + P(B) P(A')$   
=  $P(A') P(B')$ 

# **EXERCISE 13.2**

- 1. If  $P(A) = \frac{3}{5}$  and  $P(B) = \frac{1}{5}$ , find  $P(A \cap B)$  if A and B are independent events.
- 2. Two cards are drawn at random and without replacement from a pack of 52 playing cards. Find the probability that both the cards are black.
- 3. A box of oranges is inspected by examining three randomly selected oranges drawn without replacement. If all the three oranges are good, the box is approved for sale, otherwise, it is rejected. Find the probability that a box containing 15 oranges out of which 12 are good and 3 are bad ones will be approved for sale.
- 4. A fair coin and an unbiased die are tossed. Let A be the event 'head appears on the coin' and B be the event '3 on the die'. Check whether A and B are independent events or not.
- 5. A die marked 1, 2, 3 in red and 4, 5, 6 in green is tossed. Let A be the event, 'the number is even,' and B be the event, 'the number is red'. Are A and B independent?
- **6.** Let E and F be events with P(E) =  $\frac{3}{5}$ , P(F) =  $\frac{3}{10}$  and P(E  $\cap$  F) =  $\frac{1}{5}$ . Are E and F independent?

- 7. Given that the events A and B are such that  $P(A) = \frac{1}{2}$ ,  $P(A \cup B) = \frac{3}{5}$  and P(B) = p. Find p if they are (i) mutually exclusive (ii) independent.
- **8.** Let A and B be independent events with P(A) = 0.3 and P(B) = 0.4. Find
  - (i)  $P(A \cap B)$

(ii)  $P(A \cup B)$ 

(iii) P(A|B)

- (iv) P(B|A)
- 9. If A and B are two events such that  $P(A) = \frac{1}{4}$ ,  $P(B) = \frac{1}{2}$  and  $P(A \cap B) = \frac{1}{8}$ , find P (not A and not B).
- 10. Events A and B are such that  $P(A) = \frac{1}{2}$ ,  $P(B) = \frac{7}{12}$  and  $P(\text{not A or not B}) = \frac{1}{4}$ . State whether A and B are independent?
- 11. Given two independent events A and B such that P(A) = 0.3, P(B) = 0.6. Find
  - (i) P(A and B)

(ii) P(A and not B)

(iii) P(A or B)

- (iv) P(neither A nor B)
- 12. A die is tossed thrice. Find the probability of getting an odd number at least once.
- 13. Two balls are drawn at random with replacement from a box containing 10 black and 8 red balls. Find the probability that
  - (i) both balls are red.
  - (ii) first ball is black and second is red.
  - (iii) one of them is black and other is red.
- 14. Probability of solving specific problem independently by A and B are  $\frac{1}{2}$  and  $\frac{1}{3}$  respectively. If both try to solve the problem independently, find the probability that
  - (i) the problem is solved
- (ii) exactly one of them solves the problem.
- 15. One card is drawn at random from a well shuffled deck of 52 cards. In which of the following cases are the events E and F independent?
  - (i) E: 'the card drawn is a spade'

F: 'the card drawn is an ace'

(ii) E: 'the card drawn is black'

F: 'the card drawn is a king'

(iii) E: 'the card drawn is a king or queen'

F: 'the card drawn is a queen or jack'.

548

- **16.** In a hostel, 60% of the students read Hindi newspaper, 40% read English newspaper and 20% read both Hindi and English newspapers. A student is selected at random.
  - (a) Find the probability that she reads neither Hindi nor English newspapers.
  - (b) If she reads Hindi newspaper, find the probability that she reads English newspaper.
  - (c) If she reads English newspaper, find the probability that she reads Hindi newspaper.

Choose the correct answer in Exercises 17 and 18.

17. The probability of obtaining an even prime number on each die, when a pair of dice is rolled is

(A) 0 (B) 
$$\frac{1}{3}$$
 (C)  $\frac{1}{12}$  (D)  $\frac{1}{36}$ 

- 18. Two events A and B will be independent, if
  - (A) A and B are mutually exclusive
  - (B) P(A'B') = [1 P(A)][1 P(B)]
  - (C) P(A) = P(B)
  - (D) P(A) + P(B) = 1

# 13.5 Bayes' Theorem

Consider that there are two bags I and II. Bag I contains 2 white and 3 red balls and Bag II contains 4 white and 5 red balls. One ball is drawn at random from one of the

bags. We can find the probability of selecting any of the bags (i.e.  $\frac{1}{2}$ ) or probability of drawing a ball of a particular colour (say white) from a particular bag (say Bag I). In other words, we can find the probability that the ball drawn is of a particular colour, if

other words, we can find the probability that the ball drawn is of a particular colour, if we are given the bag from which the ball is drawn. But, can we find the probability that the ball drawn is from a particular bag (say Bag II), if the colour of the ball drawn is given? Here, we have to find the reverse probability of Bag II to be selected when an event occurred after it is known. Famous mathematician, John Bayes' solved the problem of finding reverse probability by using conditional probability. The formula developed by him is known as 'Bayes theorem' which was published posthumously in 1763. Before stating and proving the Bayes' theorem, let us first take up a definition and some preliminary results.

# 13.5.1 Partition of a sample space

A set of events E<sub>1</sub>, E<sub>2</sub>, ..., E<sub>n</sub> is said to represent a partition of the sample space S if

(a) 
$$E_i \cap E_j = \emptyset$$
,  $i \neq j$ ,  $i, j = 1, 2, 3, ..., n$ 

- (b)  $E_1 \cup E_2 \cup ... \cup E_n = S$  and
- (c)  $P(E_i) > 0$  for all i = 1, 2, ..., n.

In other words, the events  $E_1$ ,  $E_2$ , ...,  $E_n$  represent a partition of the sample space S if they are pairwise disjoint, exhaustive and have nonzero probabilities.

As an example, we see that any nonempty event E and its complement E' form a partition of the sample space S since they satisfy  $E \cap E' = \emptyset$  and  $E \cup E' = S$ .

From the Venn diagram in Fig 13.3, one can easily observe that if E and F are any two events associated with a sample space S, then the set  $\{E \cap F', E \cap F, E' \cap F, E' \cap F'\}$  is a partition of the sample space S. It may be mentioned that the partition of a sample space is not unique. There can be several partitions of the same sample space.

We shall now prove a theorem known as Theorem of total probability.

## 13.5.2 Theorem of total probability

Let  $\{E_1, E_2, ..., E_n\}$  be a partition of the sample space S, and suppose that each of the events  $E_1, E_2, ..., E_n$  has nonzero probability of occurrence. Let A be any event associated with S, then

$$P(A) = P(E_1) P(A|E_1) + P(E_2) P(A|E_2) + ... + P(E_n) P(A|E_n)$$

$$= \sum_{j=1}^{n} P(E_j) P(A|E_j)$$

**Proof** Given that  $E_1, E_2, ..., E_n$  is a partition of the sample space S (Fig 13.4). Therefore,

$$\begin{split} \mathbf{S} &= \mathbf{E}_1 \cup \mathbf{E}_2 \cup ... \cup \mathbf{E}_n \\ \mathbf{E}_i &\cap \mathbf{E}_j = \emptyset, \, i \neq j, \, i, j = 1, \, 2, \, ..., \, n \end{split}$$

Now, we know that for any event A.

and

$$A = A \cap S$$

$$= A \cap (E_1 \cup E_2 \cup ... \cup E_n)$$

$$= (A \cap E_1) \cup (A \cap E_2) \cup ... \cup (A \cap E_n)$$

![](_page_18_Picture_15.jpeg)

Fig 13.4

Also  $A \cap E_i$  and  $A \cap E_j$  are respectively the subsets of  $E_i$  and  $E_j$ . We know that  $E_i$  and  $E_j$  are disjoint, for  $i \neq j$ , therefore,  $A \cap E_i$  and  $A \cap E_j$  are also disjoint for all  $i \neq j$ , i, j = 1, 2, ..., n.

Thus, 
$$P(A) = P[(A \cap E_1) \cup (A \cap E_2) \cup ..... \cup (A \cap E_n)]$$
  
=  $P(A \cap E_1) + P(A \cap E_2) + ... + P(A \cap E_n)$ 

Now, by multiplication rule of probability, we have

$$P(A \cap E_i) = P(E_i) P(A|E_i) \text{ as } P(E_i) \neq 0 \forall i = 1,2,..., n$$

Therefore, 
$$P(A) = P(E_1) P(A|E_1) + P(E_2) P(A|E_2) + ... + P(E_n)P(A|E_n)$$

or 
$$P(A) = \sum_{j=1}^{n} P(E_j) P(A|E_j)$$

**Example 15** A person has undertaken a construction job. The probabilities are 0.65 that there will be strike, 0.80 that the construction job will be completed on time if there is no strike, and 0.32 that the construction job will be completed on time if there is a strike. Determine the probability that the construction job will be completed on time.

**Solution** Let A be the event that the construction job will be completed on time, and B be the event that there will be a strike. We have to find P(A). We have

$$P(B) = 0.65$$
,  $P(\text{no strike}) = P(B') = 1 - P(B) = 1 - 0.65 = 0.35$   
 $P(A|B) = 0.32$ ,  $P(A|B') = 0.80$ 

Since events B and B' form a partition of the sample space S, therefore, by theorem on total probability, we have

$$P(A) = P(B) P(A|B) + P(B') P(A|B')$$
$$= 0.65 \times 0.32 + 0.35 \times 0.8$$
$$= 0.208 + 0.28 = 0.488$$

Thus, the probability that the construction job will be completed in time is 0.488.

We shall now state and prove the Bayes' theorem.

**Bayes' Theorem** If  $E_1, E_2, ..., E_n$  are n non empty events which constitute a partition of sample space S, i.e.  $E_1, E_2, ..., E_n$  are pairwise disjoint and  $E_1 \cup E_2 \cup ... \cup E_n = S$  and A is any event of nonzero probability, then

$$P(E_i|A) = \frac{P(E_i)P(A|E_i)}{\sum_{j=1}^{n} P(E_j)P(A|E_j)} \text{ for any } i = 1, 2, 3, ..., n$$

**Proof** By formula of conditional probability, we know that

$$P(E_i|A) = \frac{P(A \cap E_i)}{P(A)}$$

$$= \frac{P(E_i)P(A|E_i)}{P(A)} \text{ (by multiplication rule of probability)}$$

$$= \frac{P(E_i)P(A|E_i)}{\sum_{i=1}^{n} P(E_j)P(A|E_j)} \text{ (by the result of theorem of total probability)}$$

**Remark** The following terminology is generally used when Bayes' theorem is applied.

The events  $E_1$ ,  $E_2$ , ...,  $E_n$  are called hypotheses.

The probability P(E<sub>i</sub>) is called the *priori probability* of the hypothesis E<sub>i</sub>

The conditional probability  $P(E_i|A)$  is called *a posteriori probability* of the hypothesis  $E_i$ .

Bayes' theorem is also called the formula for the probability of "causes". Since the  $E_i$ 's are a partition of the sample space S, one and only one of the events  $E_i$  occurs (i.e. one of the events  $E_i$  must occur and only one can occur). Hence, the above formula gives us the probability of a particular  $E_i$  (i.e. a "Cause"), given that the event A has occurred.

The Bayes' theorem has its applications in variety of situations, few of which are illustrated in following examples.

**Example 16** Bag I contains 3 red and 4 black balls while another Bag II contains 5 red and 6 black balls. One ball is drawn at random from one of the bags and it is found to be red. Find the probability that it was drawn from Bag II.

**Solution** Let  $E_1$  be the event of choosing the bag I,  $E_2$  the event of choosing the bag II and A be the event of drawing a red ball.

Then 
$$P(E_1) = P(E_2) = \frac{1}{2}$$

Also 
$$P(A|E_1) = P(drawing a red ball from Bag I) = \frac{3}{7}$$

and 
$$P(A|E_2) = P(drawing a red ball from Bag II) = \frac{5}{11}$$

Now, the probability of drawing a ball from Bag II, being given that it is red, is  $P(E_2|A)$ 

By using Bayes' theorem, we have

$$P(E_2|A) = \frac{P(E_2)P(A|E_2)}{P(E_1)P(A|E_1) + P(E_2)P(A|E_2)} = \frac{\frac{1}{2} \times \frac{5}{11}}{\frac{1}{2} \times \frac{3}{7} + \frac{1}{2} \times \frac{5}{11}} = \frac{35}{68}$$

**Example 17** Given three identical boxes I, II and III, each containing two coins. In box I, both coins are gold coins, in box II, both are silver coins and in the box III, there is one gold and one silver coin. A person chooses a box at random and takes out a coin. If the coin is of gold, what is the probability that the other coin in the box is also of gold?

Solution Let  $E_1$ ,  $E_2$  and  $E_3$  be the events that boxes I, II and III are chosen, respectively.

Then 
$$P(E_1) = P(E_2) = P(E_3) = \frac{1}{3}$$

Also, let A be the event that 'the coin drawn is of gold'

Then 
$$P(A|E_1) = P(a \text{ gold coin from bag I}) = \frac{2}{2} = 1$$
  
 $P(A|E_2) = P(a \text{ gold coin from bag II}) = 0$   
 $P(A|E_3) = P(a \text{ gold coin from bag III}) = \frac{1}{2}$ 

Now, the probability that the other coin in the box is of gold

= the probability that gold coin is drawn from the box I.

 $= P(E_1|A)$ 

By Bayes' theorem, we know that

$$P(E_1|A) = \frac{P(E_1)P(A|E_1)}{P(E_1)P(A|E_1) + P(E_2)P(A|E_2) + P(E_3)P(A|E_3)}$$
$$= \frac{\frac{1}{3} \times 1}{\frac{1}{3} \times 1 + \frac{1}{3} \times 0 + \frac{1}{3} \times \frac{1}{2}} = \frac{2}{3}$$

**Example 18** Suppose that the reliability of a HIV test is specified as follows:

Of people having HIV, 90% of the test detect the disease but 10% go undetected. Of people free of HIV, 99% of the test are judged HIV–ive but 1% are diagnosed as showing HIV+ive. From a large population of which only 0.1% have HIV, one person is selected at random, given the HIV test, and the pathologist reports him/her as HIV+ive. What is the probability that the person actually has HIV?

**Solution** Let E denote the event that the person selected is actually having HIV and A the event that the person's HIV test is diagnosed as +ive. We need to find P(E|A).

Also E' denotes the event that the person selected is actually not having HIV.

Clearly,  $\{E,E'\}$  is a partition of the sample space of all people in the population. We are given that

$$P(E) = 0.1\% = \frac{0.1}{100} = 0.001$$

$$P(E') = 1 - P(E) = 0.999$$

P(A|E) = P(Person tested as HIV+ive given that he/she is actually having HIV)

$$=90\% = \frac{90}{100} = 0.9$$

and

P(AlE') = P(Person tested as HIV +ive given that he/she is actually not having HIV)

$$=1\% = \frac{1}{100} = 0.01$$

Now, by Bayes' theorem

$$P(E|A) = \frac{P(E)P(A|E)}{P(E)P(A|E) + P(E')P(A|E')}$$
$$= \frac{0.001 \times 0.9}{0.001 \times 0.9 + 0.999 \times 0.01} = \frac{90}{1089}$$
$$= 0.083 \text{ approx.}$$

Thus, the probability that a person selected at random is actually having HIV given that he/she is tested HIV+ive is 0.083.

**Example 19** In a factory which manufactures bolts, machines A, B and C manufacture respectively 25%, 35% and 40% of the bolts. Of their outputs, 5, 4 and 2 percent are respectively defective bolts. A bolt is drawn at random from the product and is found to be defective. What is the probability that it is manufactured by the machine B?

**Solution** Let events  $B_1$ ,  $B_2$ ,  $B_3$  be the following:

B<sub>1</sub>: the bolt is manufactured by machine A

B<sub>2</sub>: the bolt is manufactured by machine B

B<sub>3</sub>: the bolt is manufactured by machine C

Clearly, B<sub>1</sub>, B<sub>2</sub>, B<sub>3</sub> are mutually exclusive and exhaustive events and hence, they represent a partition of the sample space.

Let the event E be 'the bolt is defective'.

The event E occurs with B<sub>1</sub> or with B<sub>2</sub> or with B<sub>3</sub>. Given that,

$$P(B_1) = 25\% = 0.25$$
,  $P(B_2) = 0.35$  and  $P(B_3) = 0.40$ 

Again  $P(E|B_1)$  = Probability that the bolt drawn is defective given that it is manufactured by machine A = 5% = 0.05

Similarly,  $P(E|B_2) = 0.04$ ,  $P(E|B_3) = 0.02$ .

Hence, by Bayes' Theorem, we have

$$\begin{split} P(B_2|E) &= \frac{P(B_2)P(E|B_2)}{P(B_1)P(E|B_1) + P(B_2)P(E|B_2) + P(B_3)P(E|B_3)} \\ &= \frac{0.35 \times 0.04}{0.25 \times 0.05 + 0.35 \times 0.04 + 0.40 \times 0.02} \\ &= \frac{0.0140}{0.0345} = \frac{28}{69} \end{split}$$

**Example 20** A doctor is to visit a patient. From the past experience, it is known that the probabilities that he will come by train, bus, scooter or by other means of transport

are respectively  $\frac{3}{10}$ ,  $\frac{1}{5}$ ,  $\frac{1}{10}$  and  $\frac{2}{5}$ . The probabilities that he will be late are  $\frac{1}{4}$ ,  $\frac{1}{3}$ , and  $\frac{1}{12}$ ,

if he comes by train, bus and scooter respectively, but if he comes by other means of transport, then he will not be late. When he arrives, he is late. What is the probability that he comes by train?

Solution Let E be the event that the doctor visits the patient late and let  $T_1$ ,  $T_2$ ,  $T_3$ ,  $T_4$ be the events that the doctor comes by train, bus, scooter, and other means of transport respectively.

Then

$$P(T_1) = \frac{3}{10}, P(T_2) = \frac{1}{5}, P(T_3) = \frac{1}{10} \text{ and } P(T_4) = \frac{2}{5}$$
 (given)

 $P(E|T_1)$  = Probability that the doctor arriving late comes by train =  $\frac{1}{4}$ 

Similarly,  $P(E|T_2) = \frac{1}{3}$ ,  $P(E|T_3) = \frac{1}{12}$  and  $P(E|T_4) = 0$ , since he is not late if he comes by other means of transport.

Therefore, by Bayes' Theorem, we have

 $P(T_i|E)$  = Probability that the doctor arriving late comes by train

$$= \frac{P(T_1)P(E|T_1)}{P(T_1)P(E|T_1) + P(T_2)P(E|T_2) + P(T_3)P(E|T_3) + P(T_4)P(E|T_4)}$$

$$= \frac{\frac{3}{10} \times \frac{1}{4}}{\frac{3}{10} \times \frac{1}{4} + \frac{1}{5} \times \frac{1}{3} + \frac{1}{10} \times \frac{1}{12} + \frac{2}{5} \times 0} = \frac{3}{40} \times \frac{120}{18} = \frac{1}{2}$$

$$= \frac{\frac{\frac{3}{10} \times \frac{1}{4}}{\frac{3}{10} \times \frac{1}{4} + \frac{1}{5} \times \frac{1}{3} + \frac{1}{10} \times \frac{1}{12} + \frac{2}{5} \times 0} = \frac{3}{40} \times \frac{120}{18} = \frac{1}{2}$$

Hence, the required probability is  $\frac{1}{2}$ .

**Example 21** A man is known to speak truth 3 out of 4 times. He throws a die and reports that it is a six. Find the probability that it is actually a six.

**Solution** Let E be the event that the man reports that six occurs in the throwing of the die and let  $S_1$  be the event that six occurs and  $S_2$  be the event that six does not occur.

Then

$$P(S_1)$$
 = Probability that  $six$  occurs =  $\frac{1}{6}$ 

$$P(S_2)$$
 = Probability that *six* does not occur =  $\frac{5}{6}$ 

 $P(E|S_1)$  = Probability that the man reports that six occurs when six has actually occurred on the die

= Probability that the man speaks the truth = 
$$\frac{3}{4}$$

 $P(E|S_2)$  = Probability that the man reports that six occurs when six has not actually occurred on the die

= Probability that the man does not speak the truth = 
$$1 - \frac{3}{4} = \frac{1}{4}$$

Thus, by Bayes' theorem, we get

 $P(S_1|E)$  = Probability that the report of the man that six has occurred is actually a six

$$= \frac{P(S_1)P(E|S_1)}{P(S_1)P(E|S_1) + P(S_2)P(E|S_2)}$$

$$= \frac{\frac{1}{6} \times \frac{3}{4}}{\frac{1}{6} \times \frac{3}{4} + \frac{5}{6} \times \frac{1}{4}} = \frac{1}{8} \times \frac{24}{8} = \frac{3}{8}$$

Hence, the required probability is  $\frac{3}{8}$ .

# **EXERCISE 13.3**

1. An urn contains 5 red and 5 black balls. A ball is drawn at random, its colour is noted and is returned to the urn. Moreover, 2 additional balls of the colour drawn are put in the urn and then a ball is drawn at random. What is the probability that the second ball is red?

556

- 2. A bag contains 4 red and 4 black balls, another bag contains 2 red and 6 black balls. One of the two bags is selected at random and a ball is drawn from the bag which is found to be red. Find the probability that the ball is drawn from the first bag.
- 3. Of the students in a college, it is known that 60% reside in hostel and 40% are day scholars (not residing in hostel). Previous year results report that 30% of all students who reside in hostel attain A grade and 20% of day scholars attain A grade in their annual examination. At the end of the year, one student is chosen at random from the college and he has an A grade, what is the probability that the student is a hostlier?
- 4. In answering a question on a multiple choice test, a student either knows the answer or guesses. Let  $\frac{3}{4}$  be the probability that he knows the answer and  $\frac{1}{4}$  be the probability that he guesses. Assuming that a student who guesses at the answer will be correct with probability  $\frac{1}{4}$ . What is the probability that the student knows the answer given that he answered it correctly?
- 5. A laboratory blood test is 99% effective in detecting a certain disease when it is in fact, present. However, the test also yields a false positive result for 0.5% of the healthy person tested (i.e. if a healthy person is tested, then, with probability 0.005, the test will imply he has the disease). If 0.1 percent of the population actually has the disease, what is the probability that a person has the disease given that his test result is positive?
- 6. There are three coins. One is a two headed coin (having head on both faces), another is a biased coin that comes up heads 75% of the time and third is an unbiased coin. One of the three coins is chosen at random and tossed, it shows heads, what is the probability that it was the two headed coin?
- 7. An insurance company insured 2000 scooter drivers, 4000 car drivers and 6000 truck drivers. The probability of an accidents are 0.01, 0.03 and 0.15 respectively. One of the insured persons meets with an accident. What is the probability that he is a scooter driver?
- 8. A factory has two machines A and B. Past record shows that machine A produced 60% of the items of output and machine B produced 40% of the items. Further, 2% of the items produced by machine A and 1% produced by machine B were defective. All the items are put into one stockpile and then one item is chosen at random from this and is found to be defective. What is the probability that it was produced by machine B?
- **9.** Two groups are competing for the position on the Board of directors of a corporation. The probabilities that the first and the second groups will win are

0.6 and 0.4 respectively. Further, if the first group wins, the probability of introducing a new product is 0.7 and the corresponding probability is 0.3 if the second group wins. Find the probability that the new product introduced was by the second group.

- 10. Suppose a girl throws a die. If she gets a 5 or 6, she tosses a coin three times and notes the number of heads. If she gets 1, 2, 3 or 4, she tosses a coin once and notes whether a head or tail is obtained. If she obtained exactly one head, what is the probability that she threw 1, 2, 3 or 4 with the die?
- 11. A manufacturer has three machine operators A, B and C. The first operator A produces 1% defective items, where as the other two operators B and C produce 5% and 7% defective items respectively. A is on the job for 50% of the time, B is on the job for 30% of the time and C is on the job for 20% of the time. A defective item is produced, what is the probability that it was produced by A?
- 12. A card from a pack of 52 cards is lost. From the remaining cards of the pack, two cards are drawn and are found to be both diamonds. Find the probability of the lost card being a diamond.
- 13. Probability that A speaks truth is  $\frac{4}{5}$ . A coin is tossed. A reports that a head appears. The probability that actually there was head is

(A) 
$$\frac{4}{5}$$
 (B)  $\frac{1}{2}$  (C)  $\frac{1}{5}$  (D)  $\frac{2}{5}$ 

- **14.** If A and B are two events such that  $A \subset B$  and  $P(B) \neq 0$ , then which of the following is correct?
  - (A)  $P(A|B) = \frac{P(B)}{P(A)}$  (B) P(A|B) < P(A)
  - (C)  $P(A|B) \ge P(A)$  (D) None of these

# 13.6 Random Variables and its Probability Distributions

We have already learnt about random experiments and formation of sample spaces. In most of these experiments, we were not only interested in the particular outcome that occurs but rather in some number associated with that outcomes as shown in following examples/experiments.

- (i) In tossing two dice, we may be interested in the sum of the numbers on the two dice.
- (ii) In tossing a coin 50 times, we may want the number of heads obtained.

(iii) In the experiment of taking out four articles (one after the other) at random from a lot of 20 articles in which 6 are defective, we want to know the number of defectives in the sample of four and not in the particular sequence of defective and nondefective articles.

In all of the above experiments, we have a rule which assigns to each outcome of the experiment a single real number. This single real number may vary with different outcomes of the experiment. Hence, it is a variable. Also its value depends upon the outcome of a random experiment and, hence, is called random variable. A random variable is usually denoted by X.

If you recall the definition of a function, you will realise that the random variable X is really speaking a function whose domain is the set of outcomes (or sample space) of a random experiment. A random variable can take any real value, therefore, its co-domain is the set of real numbers. Hence, a random variable can be defined as follows:

**Definition 4** A random variable is a real valued function whose domain is the sample space of a random experiment.

For example, let us consider the experiment of tossing a coin two times in succession. The sample space of the experiment is  $S = \{HH, HT, TH, TT\}$ .

If X denotes the number of heads obtained, then X is a random variable and for each outcome, its value is as given below:

$$X(HH) = 2$$
,  $X(HT) = 1$ ,  $X(TH) = 1$ ,  $X(TT) = 0$ .

More than one random variables can be defined on the same sample space. For example, let Y denote the number of heads minus the number of tails for each outcome of the above sample space S.

Then 
$$Y(HH) = 2$$
,  $Y(HT) = 0$ ,  $Y(TH) = 0$ ,  $Y(TT) = -2$ .

Thus, X and Y are two different random variables defined on the same sample space S.

**Example 22** A person plays a game of tossing a coin thrice. For each head, he is given Rs 2 by the organiser of the game and for each tail, he has to give Rs 1.50 to the organiser. Let X denote the amount gained or lost by the person. Show that X is a random variable and exhibit it as a function on the sample space of the experiment.

**Solution** X is a number whose values are defined on the outcomes of a random experiment. Therefore, X is a random variable.

Now, sample space of the experiment is

$$S = \{HHH, HHT, HTH, THH, HTT, THT, TTH, TTT\}$$

Then 
$$X (HHH) = Rs (2 \times 3) = Rs 6$$
  
 $X (HHT) = X (HTH) = X (THH) = Rs (2 \times 2 - 1 \times 1.50) = Rs 2.50$   
 $X (HTT) = X (THT) = (TTH) = Rs (1 \times 2) - (2 \times 1.50) = - Re 1$   
and  $X (TTT) = - Rs (3 \times 1.50) = - Rs 4.50$ 

where, minus sign shows the loss to the player. Thus, for each element of the sample space, X takes a unique value, hence, X is a function on the sample space whose range is

$$\{-1, 2.50, -4.50, 6\}$$

**Example 23** A bag contains 2 white and 1 red balls. One ball is drawn at random and then put back in the box after noting its colour. The process is repeated again. If X denotes the number of red balls recorded in the two draws, describe X.

**Solution** Let the balls in the bag be denoted by  $w_1, w_2, r$ . Then the sample space is

$$S = \{w_1 \ w_1, \ w_1 \ w_2, \ w_2 \ w_2, \ w_2 \ w_1, \ w_1 \ r, \ w_2 \ r, \ r \ w_1, \ r \ w_2, \ r \ r\}$$

$$\mathbf{w} \in S$$

Now, for

 $X(\omega)$  = number of red balls

Therefore

$$X(\{w_1 \ w_1\}) = X(\{w_1 \ w_2\}) = X(\{w_2 \ w_2\}) = X(\{w_2 \ w_1\}) = 0$$
  
 $X(\{w_1 \ r\}) = X(\{w_2 \ r\}) = X(\{r \ w_1\}) = X(\{r \ w_2\}) = 1 \text{ and } X(\{r \ r\}) = 2$ 

Thus, X is a random variable which can take values 0, 1 or 2.

## 13.6.1 Probability distribution of a random variable

Let us look at the experiment of selecting one family out of ten families  $f_1$ ,  $f_2$ ,..., $f_{10}$  in such a manner that each family is equally likely to be selected. Let the families  $f_1$ ,  $f_2$ , ...,  $f_{10}$  have 3, 4, 3, 2, 5, 4, 3, 6, 4, 5 members, respectively.

Let us select a family and note down the number of members in the family denoting X. Clearly, X is a random variable defined as below:

$$X(f_1) = 3$$
,  $X(f_2) = 4$ ,  $X(f_3) = 3$ ,  $X(f_4) = 2$ ,  $X(f_5) = 5$ ,  $X(f_6) = 4$ ,  $X(f_7) = 3$ ,  $X(f_8) = 6$ ,  $X(f_9) = 4$ ,  $X(f_{10}) = 5$ 

Thus, X can take any value 2,3,4,5 or 6 depending upon which family is selected.

Now, X will take the value 2 when the family  $f_4$  is selected. X can take the value 3 when any one of the families  $f_1$ ,  $f_3$ ,  $f_7$  is selected.

Similarly, X = 4, when family  $f_2$ ,  $f_6$  or  $f_9$  is selected,

X = 5, when family  $f_5$  or  $f_{10}$  is selected

and X = 6, when family  $f_8$  is selected.

Since we had assumed that each family is equally likely to be selected, the probability that family  $f_4$  is selected is  $\frac{1}{10}$ .

Thus, the probability that X can take the value 2 is  $\frac{1}{10}$ . We write  $P(X = 2) = \frac{1}{10}$ . Also, the probability that any one of the families  $f_1$ ,  $f_3$  or  $f_7$  is selected is

$$P(\{f_1, f_3, f_7\}) = \frac{3}{10}$$

Thus, the probability that X can take the value  $3 = \frac{3}{10}$ 

We write

$$P(X = 3) = \frac{3}{10}$$

Similarly, we obtain

$$P(X = 4) = P({f_2, f_6, f_9}) = \frac{3}{10}$$

$$P(X = 5) = P(\{f_5, f_{10}\}) = \frac{2}{10}$$

and

$$P(X = 6) = P({f_8}) = \frac{1}{10}$$

Such a description giving the values of the random variable along with the corresponding probabilities is called the *probability distribution of the random variable X*.

In general, the probability distribution of a random variable X is defined as follows: **Definition 5** The probability distribution of a random variable X is the system of numbers

$$\begin{array}{cccccccccccccccccccccccccccccccccccc$$

where,

$$p_i > 0$$
,  $\sum_{i=1}^{n} p_i = 1$ ,  $i = 1, 2, ..., n$ 

The real numbers  $x_1, x_2, ..., x_n$  are the possible values of the random variable X and  $p_i$  (i = 1, 2, ..., n) is the probability of the random variable X taking the value  $x_i$  i.e.,  $P(X = x_i) = p_i$ 

**Note** If  $x_i$  is one of the possible values of a random variable X, the statement  $X = x_i$  is true only at some point (s) of the sample space. Hence, the probability that X takes value  $x_i$  is always nonzero, i.e.  $P(X = x_i) \neq 0$ .

Also for all possible values of the random variable X, all elements of the sample space are covered. Hence, the sum of all the probabilities in a probability distribution must be one.

**Example 24** Two cards are drawn successively with replacement from a well-shuffled deck of 52 cards. Find the probability distribution of the number of aces.

**Solution** The number of aces is a random variable. Let it be denoted by X. Clearly, X can take the values 0, 1, or 2.

Now, since the draws are done with replacement, therefore, the two draws form independent experiments.

$$P(X = 0) = P(\text{non-ace and non-ace})$$

$$= P(\text{non-ace}) \times P(\text{non-ace})$$

$$= \frac{48}{52} \times \frac{48}{52} = \frac{144}{169}$$

$$P(X = 1) = P(\text{ace and non-ace or non-ace and ace})$$

$$= P(\text{ace and non-ace}) + P(\text{non-ace and ace})$$

$$= P(\text{ace}). P(\text{non-ace}) + P(\text{non-ace}). P(\text{ace})$$

$$= \frac{4}{52} \times \frac{48}{52} + \frac{48}{52} \times \frac{4}{52} = \frac{24}{169}$$

and

$$P(X = 2) = P \text{ (ace and ace)}$$
  
=  $\frac{4}{52} \times \frac{4}{52} = \frac{1}{169}$ 

Thus, the required probability distribution is

| X    | 0          | 1         | 2     |
|------|------------|-----------|-------|
| P(X) | 144<br>169 | 24<br>169 | 1/169 |

**Example 25** Find the probability distribution of number of doublets in three throws of a pair of dice.

**Solution** Let X denote the number of doublets. Possible doublets are

$$(1,1)$$
,  $(2,2)$ ,  $(3,3)$ ,  $(4,4)$ ,  $(5,5)$ ,  $(6,6)$ 

Clearly, X can take the value 0, 1, 2, or 3.

Probability of getting a doublet  $=\frac{6}{36} = \frac{1}{6}$ 

Probability of not getting a doublet =  $1 - \frac{1}{6} = \frac{5}{6}$ 

Now  $P(X = 0) = P \text{ (no doublet)} = \frac{5}{6} \times \frac{5}{6} \times \frac{5}{6} = \frac{125}{216}$ 

P(X = 1) = P (one doublet and two non-doublets)

$$= \frac{1}{6} \times \frac{5}{6} \times \frac{5}{6} + \frac{5}{6} \times \frac{1}{6} \times \frac{5}{6} + \frac{5}{6} \times \frac{5}{6} \times \frac{1}{6}$$

$$= 3 \frac{1}{6} \times \frac{5^2}{6^2} = \frac{75}{216}$$

P(X = 2) = P (two doublets and one non-doublet)

$$= \frac{1}{6} \times \frac{1}{6} \times \frac{5}{6} + \frac{1}{6} \times \frac{5}{6} \times \frac{1}{6} + \frac{5}{6} \times \frac{1}{6} \times \frac{1}{6} = 3 \quad \frac{1}{6^2} \times \frac{5}{6} = \frac{15}{216}$$

and

$$P(X = 3) = P$$
 (three doublets)

$$=\frac{1}{6}\times\frac{1}{6}\times\frac{1}{6}=\frac{1}{216}$$

Thus, the required probability distribution is

| X    | 0                 | 1                | 2                | 3               |
|------|-------------------|------------------|------------------|-----------------|
| P(X) | $\frac{125}{216}$ | $\frac{75}{216}$ | $\frac{15}{216}$ | $\frac{1}{216}$ |

**Verification** Sum of the probabilities

$$\sum_{i=1}^{n} p_i = \frac{125}{216} + \frac{75}{216} + \frac{15}{216} + \frac{1}{216}$$
$$= \frac{125 + 75 + 15 + 1}{216} = \frac{216}{216} = 1$$

**Example 26** Let X denote the number of hours you study during a randomly selected school day. The probability that X can take the values x, has the following form, where k is some unknown constant.

$$P(X = x) = \begin{cases} 0.1, & \text{if } x = 0 \\ kx, & \text{if } x = 1 \text{ or } 2 \\ k(5 - x), & \text{if } x = 3 \text{ or } 4 \\ 0, & \text{otherwise} \end{cases}$$

- (a) Find the value of k.
- (b) What is the probability that you study at least two hours? Exactly two hours? At most two hours?

**Solution** The probability distribution of X is

| X    | 0   | 1 | 2  | 3          | 4 |
|------|-----|---|----|------------|---|
| P(X) | 0.1 | k | 2k | 2 <i>k</i> | k |

(a) We know that 0.1 + k + 2k + 2k + k = 1Therefore k = 0.15i.e.  $= P(X \ge 2)$ (b) P(you study at least two hours) = P(X = 2) + P(X = 3) + P(X = 4) $= 2k + 2k + k = 5k = 5 \times 0.15 = 0.75$ = P(X = 2)P(you study exactly two hours)  $= 2k = 2 \times 0.15 = 0.3$ P(you study at most two hours)  $= P(X \le 2)$ = P(X = 0) + P(X = 1) + P(X = 2) $= 0.1 + k + 2k = 0.1 + 3k = 0.1 + 3 \times 0.15$ 

# 13.6.2 Mean of a random variable

In many problems, it is desirable to describe some feature of the random variable by means of a single number that can be computed from its probability distribution. Few such numbers are mean, median and mode. In this section, we shall discuss mean only. Mean is a measure of location or central tendency in the sense that it roughly locates a *middle* or *average value* of the random variable.

= 0.55

**Definition 6** Let X be a random variable whose possible values  $x_1, x_2, x_3, ..., x_n$  occur with probabilities  $p_1, p_2, p_3, ..., p_n$ , respectively. The mean of X, denoted by  $\mu$ , is the

number  $\sum_{i=1}^{n} x_i p_i$  i.e. the mean of X is the weighted average of the possible values of X,

each value being weighted by its probability with which it occurs.

The mean of a random variable X is also called the expectation of X, denoted by E(X).

Thus, 
$$E(X) = \mu = \sum_{i=1}^{n} x_i p_i = x_1 p_1 + x_2 p_2 + \dots + x_n p_n.$$

In other words, the mean or expectation of a random variable X is the sum of the products of all possible values of X by their respective probabilities.

**Example 27** Let a pair of dice be thrown and the random variable X be the sum of the numbers that appear on the two dice. Find the mean or expectation of X.

**Solution** The sample space of the experiment consists of 36 elementary events in the form of ordered pairs  $(x_i, y_i)$ , where  $x_i = 1, 2, 3, 4, 5, 6$  and  $y_i = 1, 2, 3, 4, 5, 6$ .

The random variable X i.e. the sum of the numbers on the two dice takes the values 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 or 12.

Now 
$$P(X = 2) = P(\{(1,1)\}) = \frac{1}{36}$$

$$P(X = 3) = P(\{(1,2), (2,1)\}) = \frac{2}{36}$$

$$P(X = 4) = P(\{(1,3), (2,2), (3,1)\}) = \frac{3}{36}$$

$$P(X = 5) = P(\{(1,4), (2,3), (3,2), (4,1)\}) = \frac{4}{36}$$

$$P(X = 6) = P(\{(1,5), (2,4), (3,3), (4,2), (5,1)\}) = \frac{5}{36}$$

$$P(X = 7) = P(\{(1,6), (2,5), (3,4), (4,3), (5,2), (6,1)\}) = \frac{6}{36}$$

$$P(X = 8) = P(\{(2,6), (3,5), (4,4), (5,3), (6,2)\}) = \frac{5}{36}$$

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

![](_page_35_Figure_5.jpeg)

To distinguish X from Y, we require a measure of the extent to which the values of the random variables spread out. In Statistics, we have studied that the variance is a measure of the spread or scatter in data. Likewise, the variability or spread in the values of a random variable may be measured by variance.

**Definition 7** Let X be a random variable whose possible values  $x_1, x_2,...,x_n$  occur with probabilities  $p(x_1), p(x_2),..., p(x_n)$  respectively.

Let  $\mu = E(X)$  be the mean of X. The variance of X, denoted by Var(X) or  $\sigma_x^2$  is defined as

$$\sigma_x^2 = \text{Var}(X) = \sum_{i=1}^n (x_i - \mu)^2 p(x_i)$$

or equivalently  $\sigma_x^2 = E(X - \mu)^2$ 

The non-negative number

$$\sigma_x = \sqrt{Var(X)} = \sqrt{\sum_{i=1}^{n} (x_i - \mu)^2 p(x_i)}$$

is called the standard deviation of the random variable X.

Another formula to find the variance of a random variable. We know that,

$$\operatorname{Var}(X) = \sum_{i=1}^{n} (x_{i} - \mu)^{2} p(x_{i})$$

$$= \sum_{i=1}^{n} (x_{i}^{2} + \mu^{2} - 2\mu x_{i}) p(x_{i})$$

$$= \sum_{i=1}^{n} x_{i}^{2} p(x_{i}) + \sum_{i=1}^{n} \mu^{2} p(x_{i}) - \sum_{i=1}^{n} 2\mu x_{i} p(x_{i})$$

$$= \sum_{i=1}^{n} x_{i}^{2} p(x_{i}) + \mu^{2} \sum_{i=1}^{n} p(x_{i}) - 2\mu \sum_{i=1}^{n} x_{i} p(x_{i})$$

$$= \sum_{i=1}^{n} x_{i}^{2} p(x_{i}) + \mu^{2} - 2\mu^{2} \left[ \operatorname{since} \sum_{i=1}^{n} p(x_{i}) = 1 \operatorname{and} \mu = \sum_{i=1}^{n} x_{i} p(x_{i}) \right]$$

$$= \sum_{i=1}^{n} x_{i}^{2} p(x_{i}) - \mu^{2}$$
or
$$\operatorname{Var}(X) = \sum_{i=1}^{n} x_{i}^{2} p(x_{i}) - \left( \sum_{i=1}^{n} x_{i} p(x_{i}) \right)^{2}$$

or  $Var(X) = E(X^2) - [E(X)]^2$ , where  $E(X^2) = \sum_{i=1}^{n} x_i^2 p(x_i)$ 

**Example 28** Find the variance of the number obtained on a throw of an unbiased die.

**Solution** The sample space of the experiment is  $S = \{1, 2, 3, 4, 5, 6\}$ .

Let X denote the number obtained on the throw. Then X is a random variable which can take values 1, 2, 3, 4, 5, or 6.

Also 
$$P(1) = P(2) = P(3) = P(4) = P(5) = P(6) = \frac{1}{6}$$

Therefore, the Probability distribution of X is

| X    | 1             | 2             | 3             | 4             | 5             | 6             |
|------|---------------|---------------|---------------|---------------|---------------|---------------|
| P(X) | $\frac{1}{6}$ | $\frac{1}{6}$ | $\frac{1}{6}$ | $\frac{1}{6}$ | $\frac{1}{6}$ | $\frac{1}{6}$ |

Now 
$$E(X) = \sum_{i=1}^{n} x_i p(x_i)$$

$$= 1 \times \frac{1}{6} + 2 \times \frac{1}{6} + 3 \times \frac{1}{6} + 4 \times \frac{1}{6} + 5 \times \frac{1}{6} + 6 \times \frac{1}{6} = \frac{21}{6}$$
Also 
$$E(X^2) = 1^2 \times \frac{1}{6} + 2^2 \times \frac{1}{6} + 3^2 \times \frac{1}{6} + 4^2 \times \frac{1}{6} + 5^2 \times \frac{1}{6} + 6^2 \times \frac{1}{6} = \frac{91}{6}$$
Thus, 
$$Var(X) = E(X^2) - (E(X))^2$$

$$= \frac{91}{6} - \left(\frac{21}{6}\right)^2 = \frac{91}{6} - \frac{441}{36} = \frac{35}{12}$$

**Example 29** Two cards are drawn simultaneously (or successively without replacement) from a well shuffled pack of 52 cards. Find the mean, variance and standard deviation of the number of kings.

**Solution** Let X denote the number of kings in a draw of two cards. X is a random variable which can assume the values 0, 1 or 2.

Now 
$$P(X = 0) = P \text{ (no king)} = \frac{{}^{48}C_2}{{}^{52}C_2} = \frac{\frac{1}{2!(48-2)!}}{\frac{52!}{2!(52-2)!}} = \frac{48\times47}{52\times51} = \frac{188}{221}$$

$$P(X = 1) = P \text{ (one king and one non-king)} = \frac{{}^{4}C_1}{{}^{52}C_2}$$

$$= \frac{4\times48\times2}{52\times51} = \frac{32}{221}$$

and 
$$P(X = 2) = P \text{ (two kings)} = \frac{{}^{4}C_{2}}{{}^{52}C_{2}} = \frac{4 \times 3}{52 \times 51} = \frac{1}{221}$$

Thus, the probability distribution of X is

| X    | 0                 | 1                | 2               |
|------|-------------------|------------------|-----------------|
| P(X) | $\frac{188}{221}$ | $\frac{32}{221}$ | $\frac{1}{221}$ |

Now

Mean of 
$$X = E(X) = \sum_{i=1}^{n} x_i p(x_i)$$
  
=  $0 \times \frac{188}{221} + 1 \times \frac{32}{221} + 2 \times \frac{1}{221} = \frac{34}{221}$ 

Also

$$E(X^{2}) = \sum_{i=1}^{n} x_{i}^{2} p(x_{i})$$

$$= 0^{2} \times \frac{188}{221} + 1^{2} \times \frac{32}{221} + 2^{2} \times \frac{1}{221} = \frac{36}{221}$$

Now

$$=\frac{36}{221}-\left(\frac{34}{221}\right)^2=\frac{6800}{(221)^2}$$

Therefore

$$\sigma_x = \sqrt{\text{Var}(X)} = \frac{\sqrt{6800}}{221} = 0.37$$

# **EXERCISE 13.4**

 $Var(X) = E(X^2) - [E(X)]^2$ 

1. State which of the following are not the probability distributions of a random variable. Give reasons for your answer.

| (i) | X    | 0   | 1   | 2   |
|-----|------|-----|-----|-----|
|     | P(X) | 0.4 | 0.4 | 0.2 |

#### 570 MATHEMATICS

| (iii) | Y    | - 1 | 0   | 1   |
|-------|------|-----|-----|-----|
|       | P(Y) | 0.6 | 0.1 | 0.2 |

| (iv) | Z    | 3   | 2   | 1   | 0   | -1   |
|------|------|-----|-----|-----|-----|------|
|      | P(Z) | 0.3 | 0.2 | 0.4 | 0.1 | 0.05 |

- 2. An urn contains 5 red and 2 black balls. Two balls are randomly drawn. Let X represent the number of black balls. What are the possible values of X? Is X a random variable?
- 3. Let X represent the difference between the number of heads and the number of tails obtained when a coin is tossed 6 times. What are possible values of X?
- 4. Find the probability distribution of
  - (i) number of heads in two tosses of a coin.
  - (ii) number of tails in the simultaneous tosses of three coins.
  - (iii) number of heads in four tosses of a coin.
- 5. Find the probability distribution of the number of successes in two tosses of a die, where a success is defined as
  - (i) number greater than 4
  - (ii) six appears on at least one die
- 6. From a lot of 30 bulbs which include 6 defectives, a sample of 4 bulbs is drawn at random with replacement. Find the probability distribution of the number of defective bulbs.
- 7. A coin is biased so that the head is 3 times as likely to occur as tail. If the coin is tossed twice, find the probability distribution of number of tails.
- **8.** A random variable X has the following probability distribution:

| X    | 0 | 1 | 2          | 3          | 4          | 5     | 6      | 7          |
|------|---|---|------------|------------|------------|-------|--------|------------|
| P(X) | 0 | k | 2 <i>k</i> | 2 <i>k</i> | 3 <i>k</i> | $k^2$ | $2k^2$ | $7k^2 + k$ |

### Determine

(i) k

(ii) P(X < 3)

(iii) P(X > 6)

(iv) P(0 < X < 3)

**9.** The random variable X has a probability distribution P(X) of the following form, where *k* is some number :

$$P(X) = \begin{cases} k, & \text{if } x = 0\\ 2k, & \text{if } x = 1\\ 3k, & \text{if } x = 2\\ 0, & \text{otherwise} \end{cases}$$

- (a) Determine the value of k.
- (b) Find P (X < 2), P (X  $\leq$  2), P(X  $\geq$  2).
- 10. Find the mean number of heads in three tosses of a fair coin.
- 11. Two dice are thrown simultaneously. If X denotes the number of sixes, find the expectation of X.
- 12. Two numbers are selected at random (without replacement) from the first six positive integers. Let X denote the larger of the two numbers obtained. Find E(X).
- **13.** Let X denote the sum of the numbers obtained when two fair dice are rolled. Find the variance and standard deviation of X.
- 14. A class has 15 students whose ages are 14, 17, 15, 14, 21, 17, 19, 20, 16, 18, 20, 17, 16, 19 and 20 years. One student is selected in such a manner that each has the same chance of being chosen and the age X of the selected student is recorded. What is the probability distribution of the random variable X? Find mean, variance and standard deviation of X.
- 15. In a meeting, 70% of the members favour and 30% oppose a certain proposal. A member is selected at random and we take X = 0 if he opposed, and X = 1 if he is in favour. Find E(X) and Var (X).

Choose the correct answer in each of the following:

**16.** The mean of the numbers obtained on throwing a die having written 1 on three faces, 2 on two faces and 5 on one face is

(A) 1 (B) 2 (C) 5 (D) 
$$\frac{8}{3}$$

- 17. Suppose that two cards are drawn at random from a deck of cards. Let X be the number of aces obtained. Then the value of E(X) is
  - (A)  $\frac{37}{221}$  (B)  $\frac{5}{13}$  (C)  $\frac{1}{13}$  (D)  $\frac{2}{13}$

## 13.7 Bernoulli Trials and Binomial Distribution

### 13.7.1 Bernoulli trials

Many experiments are dichotomous in nature. For example, a tossed coin shows a 'head' or 'tail', a manufactured item can be 'defective' or 'non-defective', the response to a question might be 'yes' or 'no', an egg has 'hatched' or 'not hatched', the decision is 'yes' or 'no' etc. In such cases, it is customary to call one of the outcomes a 'success' and the other 'not success' or 'failure'. For example, in tossing a coin, if the occurrence of the head is considered a success, then occurrence of tail is a failure.

Each time we toss a coin or roll a die or perform any other experiment, we call it a trial. If a coin is tossed, say, 4 times, the number of trials is 4, each having exactly two outcomes, namely, success or failure. The outcome of any trial is independent of the outcome of any other trial. In each of such trials, the probability of success or failure remains constant. Such independent trials which have only two outcomes usually referred as 'success' or 'failure' are called *Bernoulli trials*.

**Definition 8** Trials of a random experiment are called Bernoulli trials, if they satisfy the following conditions:

- (i) There should be a finite number of trials.
- (ii) The trials should be independent.
- (iii) Each trial has exactly two outcomes: success or failure.
- (iv) The probability of success remains the same in each trial.

For example, throwing a die 50 times is a case of 50 Bernoulli trials, in which each trial results in success (say an even number) or failure (an odd number) and the probability of success (p) is same for all 50 throws. Obviously, the successive throws of the die are independent experiments. If the die is fair and have six numbers 1 to 6 written on six faces, then  $p = \frac{1}{2}$  and  $q = 1 - p = \frac{1}{2}$  = probability of failure.

**Example 30** Six balls are drawn successively from an urn containing 7 red and 9 black balls. Tell whether or not the trials of drawing balls are Bernoulli trials when after each draw the ball drawn is

(i) replaced (ii) not replaced in the urn.

#### **Solution**

(i) The number of trials is finite. When the drawing is done with replacement, the probability of success (say, red ball) is  $p = \frac{7}{16}$  which is same for all six trials (draws). Hence, the drawing of balls with replacements are Bernoulli trials.

(ii) When the drawing is done without replacement, the probability of success (i.e., red ball) in first trial is  $\frac{7}{16}$ , in 2nd trial is  $\frac{6}{15}$  if the first ball drawn is red or  $\frac{7}{15}$  if the first ball drawn is black and so on. Clearly, the probability of success is not same for all trials, hence the trials are not Bernoulli trials.

## 13.7.2 Binomial distribution

Consider the experiment of tossing a coin in which each trial results in success (say, heads) or failure (tails). Let S and F denote respectively success and failure in each trial. Suppose we are interested in finding the ways in which we have one success in six trials.

Clearly, six different cases are there as listed below:

Similarly, two successes and four failures can have  $\frac{6!}{4!\times 2!}$  combinations. It will be

lengthy job to list all of these ways. Therefore, calculation of probabilities of 0, 1, 2, ..., n number of successes may be lengthy and time consuming. To avoid the lengthy calculations and listing of all the possible cases, for the probabilities of number of successes in n-Bernoulli trials, a formula is derived. For this purpose, let us take the experiment made up of three Bernoulli trials with probabilities p and q = 1 - p for success and failure respectively in each trial. The sample space of the experiment is the set

$$S = \{SSS, SSF, SFS, FSS, SFF, FSF, FFS, FFF\}$$

The number of successes is a random variable X and can take values 0, 1, 2, or 3. The probability distribution of the number of successes is as below:

$$P(X = 0) = P(\text{no success})$$

$$= P(\{FFF\}) = P(F) P(F) P(F)$$

$$= q \cdot q \cdot q = q^3 \text{ since the trials are independent}$$

$$P(X = 1) = P(\text{one successes})$$

$$= P(\{SFF, FSF, FFS\})$$

$$= P(\{SFF\}) + P(\{FSF\}) + P(\{FFS\})$$

$$= P(S) P(F) P(F) + P(F) P(S) P(F) + P(F) P(F) P(S)$$

$$= p \cdot q \cdot q + q \cdot p \cdot q + q \cdot q \cdot p = 3pq^2$$

$$P(X = 2) = P \text{ (two successes)}$$

$$= P(\{SSF, SFS, FSS\})$$

$$= P(\{SSF\}) + P(\{SFS\}) + P(\{FSS\})$$

$$= P(S) \ P(S) \ P(F) + P(S) \ P(F) \ P(S) + P(F) \ P(S) \ P(S)$$

$$= p.p.q. + p.q.p + q.p.p = 3p^2q$$
and
$$P(X = 3) = P(\text{three success}) = P \ (\{SSS\})$$

$$= P(S) \cdot P(S) \cdot P(S) = p^3$$

Thus, the probability distribution of X is

| X    | 0     | 1       | 2       | 3     |  |
|------|-------|---------|---------|-------|--|
| P(X) | $q^3$ | $3q^2p$ | $3qp^2$ | $p^3$ |  |

Also, the binominal expansion of  $(q + p)^3$  is

$$q^3 + 3q^2p + 3qp^2 + p^3$$

Note that the probabilities of 0, 1, 2 or 3 successes are respectively the 1st, 2nd, 3rd and 4th term in the expansion of  $(q + p)^3$ .

Also, since q + p = 1, it follows that the sum of these probabilities, as expected, is 1.

Thus, we may conclude that in an experiment of n-Bernoulli trials, the probabilities of 0, 1, 2, ..., n successes can be obtained as 1st,  $2nd, ..., (n + 1)^{th}$  terms in the expansion of  $(q + p)^n$ . To prove this assertion (result), let us find the probability of x-successes in an experiment of n-Bernoulli trials.

Clearly, in case of x successes (S), there will be (n - x) failures (F).

Now, x successes (S) and (n-x) failures (F) can be obtained in  $\frac{n!}{x!(n-x)!}$  ways.

In each of these ways, the probability of x successes and (n - x) failures is

= 
$$P(x \text{ successes}) \cdot P(n-x)$$
 failures is

$$= \frac{P(S).P(S)...P(S) \cdot P(F).P(F)...P(F)}{x \text{times}} = p^{x} q^{n-x}$$

Thus, the probability of x successes in n-Bernoulli trials is  $\frac{n!}{x!(n-x)!}p^x q^{n-x}$ 

or 
$${}^{n}C_{x}p^{x}$$
  $q^{n-x}$ 

Thus 
$$P(x \text{ successes}) = {}^{n}C_{x}p^{x}q^{n-x}, \quad x = 0, 1, 2,...,n. \ (q = 1 - p)$$

Clearly, P(x successes), i.e.  ${}^{n}C_{x}p^{x}q^{n-x}$  is the  $(x+1)^{th}$  term in the binomial expansion of  $(q+p)^{n}$ .

Thus, the probability distribution of number of successes in an experiment consisting of *n* Bernoulli trials may be obtained by the binomial expansion of  $(q + p)^n$ . Hence, this

distribution of number of successes X can be written as

| X    | 0                  | 1                         | 2                       | <br>х                      | <br>n              |
|------|--------------------|---------------------------|-------------------------|----------------------------|--------------------|
| P(X) | ${}^{n}C_{0}q^{n}$ | ${}^{n}C_{1}q^{n-1}p^{1}$ | $^{n}C_{2}q^{n-2}p^{2}$ | ${}^{n}C_{x} q^{n-x}p^{x}$ | ${}^{n}C_{n}p^{n}$ |

The above probability distribution is known as *binomial distribution* with parameters n and p, because for given values of n and p, we can find the complete probability distribution.

The probability of x successes P(X = x) is also denoted by P(x) and is given by

$$P(x) = {}^{n}C_{x}q^{n-x}p^{x}, \quad x = 0, 1,..., n. (q = 1 - p)$$

This P(x) is called the *probability function* of the binomial distribution.

A binomial distribution with n-Bernoulli trials and probability of success in each trial as p, is denoted by B(n, p).

Let us now take up some examples.

**Example 31** If a fair coin is tossed 10 times, find the probability of

- (i) exactly six heads
- (ii) at least six heads
- (iii) at most six heads

**Solution** The repeated tosses of a coin are Bernoulli trials. Let X denote the number of heads in an experiment of 10 trials.

Clearly, X has the binomial distribution with n = 10 and  $p = \frac{1}{2}$ 

Therefore  $P(X = x) = {}^{n}C_{x}q^{n-x}p^{x}, x = 0, 1, 2,...,n$ 

Here  $n = 10, p = \frac{1}{2}, q = 1 - p = \frac{1}{2}$ 

Therefore  $P(X = x) = {}^{10}C_x \left(\frac{1}{2}\right)^{10-x} \left(\frac{1}{2}\right)^x = {}^{10}C_x \left(\frac{1}{2}\right)^{10}$ 

Now (i)  $P(X = 6) = {}^{10}C_6 \left(\frac{1}{2}\right)^{10} = \frac{10!}{6! \times 4!} \frac{1}{2^{10}} = \frac{105}{512}$ 

(ii)  $P(\text{at least six heads}) = P(X \ge 6)$ 

= P(X = 6) + P(X = 7) + P(X = 8) + P(X = 9) + P(X = 10)

$$\begin{split} &= {}^{10}C_6 \bigg(\frac{1}{2}\bigg)^{10} + {}^{10}C_7 \bigg(\frac{1}{2}\bigg)^{10} + {}^{10}C_8 \bigg(\frac{1}{2}\bigg)^{10} + {}^{10}C_9 \bigg(\frac{1}{2}\bigg)^{10} + {}^{10}C_{10} \bigg(\frac{1}{2}\bigg)^{10} \\ &= \bigg[\bigg(\frac{10!}{6! \times 4!}\bigg) + \bigg(\frac{10!}{7! \times 3!}\bigg) + \bigg(\frac{10!}{8! \times 2!}\bigg) + \bigg(\frac{10!}{9! \times 1!}\bigg) + \bigg(\frac{10!}{10!}\bigg)\bigg]\frac{1}{2^{10}} = \frac{193}{512} \end{split}$$

(iii) P(at most six heads) = P(X \le 6)  
= P(X = 0) + P(X = 1) + P(X = 2) + P(X = 3)  
+ P(X = 4) + P(X = 5) + P(X = 6)  
= 
$$\left(\frac{1}{2}\right)^{10} + {}^{10}C_1\left(\frac{1}{2}\right)^{10} + {}^{10}C_2\left(\frac{1}{2}\right)^{10} + {}^{10}C_3\left(\frac{1}{2}\right)^{10}$$
  
+  ${}^{10}C_4\left(\frac{1}{2}\right)^{10} + {}^{10}C_5\left(\frac{1}{2}\right)^{10} + {}^{10}C_6\left(\frac{1}{2}\right)^{10}$   
=  $\frac{848}{1024} = \frac{53}{64}$ 

**Example 32** Ten eggs are drawn successively with replacement from a lot containing 10% defective eggs. Find the probability that there is at least one defective egg.

**Solution** Let X denote the number of defective eggs in the 10 eggs drawn. Since the drawing is done with replacement, the trials are Bernoulli trials. Clearly, X has the

binomial distribution with n = 10 and  $p = \frac{10}{100} = \frac{1}{10}$ .

Therefore

$$q = 1 - p = \frac{9}{10}$$

Now

P(at least one defective egg) =  $P(X \ge 1) = 1 - P(X = 0)$ 

$$= 1^{-10} C_0 \left( \frac{9}{10} \right)^{10} = 1 - \frac{9^{10}}{10^{10}}$$

# **EXERCISE 13.5**

- 1. A die is thrown 6 times. If 'getting an odd number' is a success, what is the probability of
  - (i) 5 successes?

- (ii) at least 5 successes?
- (iii) at most 5 successes?

- 2. A pair of dice is thrown 4 times. If getting a doublet is considered a success, find the probability of two successes.
- 3. There are 5% defective items in a large bulk of items. What is the probability that a sample of 10 items will include not more than one defective item?
- **4.** Five cards are drawn successively with replacement from a well-shuffled deck of 52 cards. What is the probability that
  - (i) all the five cards are spades?
  - (ii) only 3 cards are spades?
  - (iii) none is a spade?
- 5. The probability that a bulb produced by a factory will fuse after 150 days of use is 0.05. Find the probability that out of 5 such bulbs
  - (i) none
  - (ii) not more than one
  - (iii) more than one
  - (iv) at least one

will fuse after 150 days of use.

- 6. A bag consists of 10 balls each marked with one of the digits 0 to 9. If four balls are drawn successively with replacement from the bag, what is the probability that none is marked with the digit 0?
- 7. In an examination, 20 questions of true-false type are asked. Suppose a student tosses a fair coin to determine his answer to each question. If the coin falls heads, he answers 'true'; if it falls tails, he answers 'false'. Find the probability that he answers at least 12 questions correctly.
- **8.** Suppose X has a binomial distribution  $B\left(6, \frac{1}{2}\right)$ . Show that X = 3 is the most likely outcome.

(Hint: P(X = 3) is the maximum among all  $P(x_i)$ ,  $x_i = 0,1,2,3,4,5,6$ )

- **9.** On a multiple choice examination with three possible answers for each of the five questions, what is the probability that a candidate would get four or more correct answers just by guessing?
- 10. A person buys a lottery ticket in 50 lotteries, in each of which his chance of winning a prize is  $\frac{1}{100}$ . What is the probability that he will win a prize (a) at least once (b) exactly once (c) at least twice?

- 11. Find the probability of getting 5 exactly twice in 7 throws of a die.
- 12. Find the probability of throwing at most 2 sixes in 6 throws of a single die.
- 13. It is known that 10% of certain articles manufactured are defective. What is the probability that in a random sample of 12 such articles, 9 are defective? In each of the following, choose the correct answer:
- **14.** In a box containing 100 bulbs, 10 are defective. The probability that out of a sample of 5 bulbs, none is defective is
  - (A)  $10^{-1}$  (B)  $\left(\frac{1}{2}\right)^5$  (C)  $\left(\frac{9}{10}\right)^5$  (D)  $\frac{9}{10}$
- 15. The probability that a student is not a swimmer is  $\frac{1}{5}$ . Then the probability that out of five students, four are swimmers is

(A) 
$${}^{5}C_{4} \left(\frac{4}{5}\right)^{4} \frac{1}{5}$$
 (B)  $\left(\frac{4}{5}\right)^{4} \frac{1}{5}$ 

(C) 
$${}^5C_1 \frac{1}{5} \left(\frac{4}{5}\right)^4$$
 (D) None of these

# Miscellaneous Examples

**Example 33** Coloured balls are distributed in four boxes as shown in the following table:

| Box | x Colour |       |     |      |  |
|-----|----------|-------|-----|------|--|
|     | Black    | White | Red | Blue |  |
| I   | 3        | 4     | 5   | 6    |  |
| II  | 2        | 2     | 2   | 2    |  |
| III | 1        | 2     | 3   | 1    |  |
| IV  | 4        | 3     | 1   | 5    |  |

A box is selected at random and then a ball is randomly drawn from the selected box. The colour of the ball is black, what is the probability that ball drawn is from the box III?

Solution Let A,  $E_1$ ,  $E_2$ ,  $E_3$  and  $E_4$  be the events as defined below:

A: a black ball is selected  $E_1$ : box I is selected  $E_2$ : box II is selected  $E_3$ : box III is selected

E<sub>4</sub>: box IV is selected

Since the boxes are chosen at random,

Therefore

$$P(E_1) = P(E_2) = P(E_3) = P(E_4) = \frac{1}{4}$$

Also

$$P(A|E_1) = \frac{3}{18}$$
,  $P(A|E_2) = \frac{2}{8}$ ,  $P(A|E_3) = \frac{1}{7}$  and  $P(A|E_4) = \frac{4}{13}$ 

P(box III is selected, given that the drawn ball is black) =  $P(E_3|A)$ . By Bayes' theorem,

$$P(E_3|A) = \frac{P(E_3) \cdot P(A|E_3)}{P(E_1)P(A|E_1) + P(E_2)P(A|E_2) + P(E_3)P(A|E_3) + P(E_4)P(A|E_4)}$$

$$= \frac{\frac{1}{4} \times \frac{1}{7}}{\frac{1}{4} \times \frac{3}{18} + \frac{1}{4} \times \frac{1}{4} + \frac{1}{4} \times \frac{1}{7} + \frac{1}{4} \times \frac{4}{13}} = 0.165$$

**Example 34** Find the mean of the Binomial distribution  $B\left(4,\frac{1}{3}\right)$ .

**Solution** Let X be the random variable whose probability distribution is  $B\left(4,\frac{1}{3}\right)$ .

Here

$$n = 4, p = \frac{1}{3}$$
 and  $q = 1 - \frac{1}{3} = \frac{2}{3}$ 

We know that

$$P(X = x) = {}^{4}C_{x} \left(\frac{2}{3}\right)^{4-x} \left(\frac{1}{3}\right)^{x}, x = 0, 1, 2, 3, 4.$$

i.e. the distribution of X is

| $\boldsymbol{x}_{i}$ | $\mathbf{P}(\mathbf{x}_i)$                                      | $x_i P(x_i)$                                                |  |
|----------------------|-----------------------------------------------------------------|-------------------------------------------------------------|--|
| 0                    | ${}^{4}C_{0}\left(\frac{2}{3}\right)^{4}$                       | 0                                                           |  |
| 1                    | $^{4}C_{1}\left(\frac{2}{3}\right)^{3}\left(\frac{1}{3}\right)$ | ${}^4C_1\left(\frac{2}{3}\right)^3\left(\frac{1}{3}\right)$ |  |

$$\begin{array}{c|ccccccccccccccccccccccccccccccccccc$$

Now Mean (
$$\mu$$
) =  $\sum_{i=1}^{4} x_i p(x_i)$   
=  $0 + {}^{4}C_1 \left(\frac{2}{3}\right)^3 \left(\frac{1}{3}\right) + 2 \cdot {}^{4}C_2 \left(\frac{2}{3}\right)^2 \left(\frac{1}{3}\right)^2 + 3 \cdot {}^{4}C_3 \left(\frac{2}{3}\right) \left(\frac{1}{3}\right)^3 + 4 \cdot {}^{4}C_4 \left(\frac{1}{3}\right)^4$   
=  $4 \times \frac{2^3}{3^4} + 2 \times 6 \times \frac{2^2}{3^4} + 3 \times 4 \times \frac{2}{3^4} + 4 \times 1 \times \frac{1}{3^4}$   
=  $\frac{32 + 48 + 24 + 4}{3^4} = \frac{108}{81} = \frac{4}{3}$ 

**Example 35** The probability of a shooter hitting a target is  $\frac{3}{4}$ . How many minimum number of times must he/she fire so that the probability of hitting the target at least once is more than 0.99?

**Solution** Let the shooter fire *n* times. Obviously, *n* fires are *n* Bernoulli trials. In each trial,  $p = \text{probability of hitting the target} = \frac{3}{4}$  and q = probability of not hitting the

target = 
$$\frac{1}{4}$$
. Then  $P(X = x) = {}^{n}C_{x} q^{n-x} p^{x} = {}^{n}C_{x} \left(\frac{1}{4}\right)^{n-x} \left(\frac{3}{4}\right)^{x} = {}^{n}C_{x} \frac{3^{x}}{4^{n}}$ .

Now, given that,

P(hitting the target at least once) > 0.99

i.e. 
$$P(x \ge 1) > 0.99$$

Therefore, 
$$1 - P(x = 0) > 0.99$$
or 
$$1 - {}^{n}C_{0}\frac{1}{4^{n}} > 0.99$$
or 
$${}^{n}C_{0}\frac{1}{4^{n}} < 0.01 \text{ i.e. } \frac{1}{4^{n}} < 0.01$$
or 
$$4^{n} > \frac{1}{0.01} = 100$$
 ... (1)

The minimum value of n to satisfy the inequality (1) is 4.

Thus, the shooter must fire 4 times.

**Example 36** A and B throw a die alternatively till one of them gets a '6' and wins the game. Find their respective probabilities of winning, if A starts first.

**Solution** Let S denote the success (getting a '6') and F denote the failure (not getting a '6').

Thus,

$$P(S) = \frac{1}{6}, P(F) = \frac{5}{6}$$

P(A wins in the first throw) = P(S) = 
$$\frac{1}{6}$$

A gets the third throw, when the first throw by A and second throw by B result into failures.

Therefore,  $P(A \text{ wins in the 3rd throw}) = P(FFS) = P(F)P(F)P(S) = \frac{5}{6} \times \frac{5}{6} \times \frac{1}{6}$ 

$$=\left(\frac{5}{6}\right)^2 \times \frac{1}{6}$$

P(A wins in the 5th throw) = P (FFFFS) =  $\left(\frac{5}{6}\right)^4 \left(\frac{1}{6}\right)$  and so on.

Hence,

$$P(A \text{ wins}) = \frac{1}{6} + \left(\frac{5}{6}\right)^2 \left(\frac{1}{6}\right) + \left(\frac{5}{6}\right)^4 \left(\frac{1}{6}\right) + \dots$$
$$= \frac{\frac{1}{6}}{1 - \frac{25}{36}} = \frac{6}{11}$$

$$P(B \text{ wins}) = 1 - P(A \text{ wins}) = 1 - \frac{6}{11} = \frac{5}{11}$$

**Remark** If  $a + ar + ar^2 + ... + ar^{n-1} + ...$ , where |r| < 1, then sum of this infinite G.P.

is given by  $\frac{a}{1-r}$  (Refer A.1.3 of Class XI Text book).

**Example 37** If a machine is correctly set up, it produces 90% acceptable items. If it is incorrectly set up, it produces only 40% acceptable items. Past experience shows that 80% of the set ups are correctly done. If after a certain set up, the machine produces 2 acceptable items, find the probability that the machine is correctly setup.

**Solution** Let A be the event that the machine produces 2 acceptable items.

Also let B<sub>1</sub> represent the event of correct set up and B<sub>2</sub> represent the event of incorrect setup.

Now  $P(B_1) = 0.8, P(B_2) = 0.2$   $P(A|B_1) = 0.9 \times 0.9 \text{ and } P(A|B_2) = 0.4 \times 0.4$ Therefore  $P(B_1|A) = \frac{P(B_1) P(A|B_1)}{P(B_1) P(A|B_1) + P(B_2) P(A|B_2)}$   $= \frac{0.8 \times 0.9 \times 0.9}{0.8 \times 0.9 \times 0.9 + 0.2 \times 0.4 \times 0.4} = \frac{648}{680} = 0.95$ 

# Miscellaneous Exercise on Chapter 13

- 1. A and B are two events such that  $P(A) \neq 0$ . Find P(B|A), if
  - (i) A is a subset of B
- (ii)  $A \cap B = \phi$
- 2. A couple has two children,
  - (i) Find the probability that both children are males, if it is known that at least one of the children is male.
  - (ii) Find the probability that both children are females, if it is known that the elder child is a female.
- 3. Suppose that 5% of men and 0.25% of women have grey hair. A grey haired person is selected at random. What is the probability of this person being male? Assume that there are equal number of males and females.
- **4.** Suppose that 90% of people are right-handed. What is the probability that at most 6 of a random sample of 10 people are right-handed?

- 5. An urn contains 25 balls of which 10 balls bear a mark 'X' and the remaining 15 bear a mark 'Y'. A ball is drawn at random from the urn, its mark is noted down and it is replaced. If 6 balls are drawn in this way, find the probability that
  - (i) all will bear 'X' mark.
  - (ii) not more than 2 will bear 'Y' mark.
  - (iii) at least one ball will bear 'Y' mark.
  - (iv) the number of balls with 'X' mark and 'Y' mark will be equal.
- 6. In a hurdle race, a player has to cross 10 hurdles. The probability that he will clear each hurdle is  $\frac{5}{6}$ . What is the probability that he will knock down fewer than 2 hurdles?
- 7. A die is thrown again and again until three sixes are obtained. Find the probability of obtaining the third six in the sixth throw of the die.
- **8.** If a leap year is selected at random, what is the chance that it will contain 53 tuesdays?
- **9.** An experiment succeeds twice as often as it fails. Find the probability that in the next six trials, there will be atleast 4 successes.
- 10. How many times must a man toss a fair coin so that the probability of having at least one head is more than 90%?
- 11. In a game, a man wins a rupee for a six and loses a rupee for any other number when a fair die is thrown. The man decided to throw a die thrice but to quit as and when he gets a six. Find the expected value of the amount he wins / loses.
- **12.** Suppose we have four boxes A,B,C and D containing coloured marbles as given below:

| Box | Marble colour |       |       |  |
|-----|---------------|-------|-------|--|
| X   | Red           | White | Black |  |
| A   | 1             | 6     | 3     |  |
| В   | 6             | 2     | 2     |  |
| С   | 8             | 1     | 1     |  |
| D   | 0             | 6     | 4     |  |

One of the boxes has been selected at random and a single marble is drawn from it. If the marble is red, what is the probability that it was drawn from box A?, box B?, box C?

- 13. Assume that the chances of a patient having a heart attack is 40%. It is also assumed that a meditation and yoga course reduce the risk of heart attack by 30% and prescription of certain drug reduces its chances by 25%. At a time a patient can choose any one of the two options with equal probabilities. It is given that after going through one of the two options the patient selected at random suffers a heart attack. Find the probability that the patient followed a course of meditation and yoga?
- 14. If each element of a second order determinant is either zero or one, what is the probability that the value of the determinant is positive? (Assume that the individual entries of the determinant are chosen independently, each value being assumed with probability  $\frac{1}{2}$ ).
- 15. An electronic assembly consists of two subsystems, say, A and B. From previous testing procedures, the following probabilities are assumed to be known:

$$P(A fails) = 0.2$$

$$P(B fails alone) = 0.15$$

$$P(A and B fail) = 0.15$$

Evaluate the following probabilities

- (i) P(A fails|B has failed)
- (ii) P(A fails alone)
- **16.** Bag I contains 3 red and 4 black balls and Bag II contains 4 red and 5 black balls. One ball is transferred from Bag I to Bag II and then a ball is drawn from Bag II. The ball so drawn is found to be red in colour. Find the probability that the transferred ball is black.

Choose the correct answer in each of the following:

- 17. If A and B are two events such that  $P(A) \neq 0$  and  $P(B \mid A) = 1$ , then
  - $(A) A \subset B \qquad (B) B \subset A$
- (C)  $B = \phi$
- (D)  $A = \phi$
- 18. If P(A|B) > P(A), then which of the following is correct:
  - (A) P(B|A) < P(B)

(B)  $P(A \cap B) < P(A) \cdot P(B)$ 

(C) P(B|A) > P(B)

- (D) P(B|A) = P(B)
- 19. If A and B are any two events such that P(A) + P(B) P(A and B) = P(A), then
  - (A) P(B|A) = 1

(B) P(A|B) = 1

(C) P(B|A) = 0

(D) P(A|B) = 0

# **Summary**

The salient features of the chapter are –

◆ The conditional probability of an event E, given the occurrence of the event F

is given by 
$$P(E \mid F) = \frac{P(E \cap F)}{P(F)}$$
,  $P(F) \neq 0$ 

- ◆  $0 \le P(E|F) \le 1$ , P(E'|F) = 1 P(E|F) $P(E \cup F)|G) = P(E|G) + P(F|G) - P(E \cap F)|G)$
- ◆  $P(E \cap F) = P(E) P(F|E), P(E) \neq 0$  $P(E \cap F) = P(F) P(E|F), P(F) \neq 0$
- ♦ If E and F are independent, then

$$P(E \cap F) = P(E) P(F)$$

$$P(E|F) = P(E), P(F) \neq 0$$

$$P(F|E) = P(F), P(E) \neq 0$$

♦ Theorem of total probability

Let  $\{E_1, E_2, ..., E_n\}$  be a partition of a sample space and suppose that each of  $E_1, E_2, ..., E_n$  has nonzero probability. Let A be any event associated with S, then

$$P(A) = P(E_1) P (A|E_1) + P (E_2) P (A|E_2) + ... + P (E_n) P(A|E_n)$$

♦ **Bayes' theorem** If  $E_1$ ,  $E_2$ , ...,  $E_n$  are events which constitute a partition of sample space S, i.e.  $E_1$ ,  $E_2$ , ...,  $E_n$  are pairwise disjoint and  $E_1 \cup E_2 \cup ... \cup E_n = S$  and A be any event with nonzero probability, then

$$P(E_i | A) = \frac{P(E_i) P(A|E_i)}{\sum_{i=1}^{n} P(E_j) P(A|E_j)}$$

- A random variable is a real valued function whose domain is the sample space of a random experiment.
- ♦ The probability distribution of a random variable X is the system of numbers

$$\begin{array}{cccccccccccccccccccccccccccccccccccc$$

where, 
$$p_i > 0$$
,  $\sum_{i=1}^{n} p_i = 1$ ,  $i = 1, 2, ..., n$ 

• Let X be a random variable whose possible values  $x_1, x_2, x_3, ..., x_n$  occur with probabilities  $p_1, p_2, p_3, ..., p_n$  respectively. The mean of X, denoted by  $\mu$ , is

the number 
$$\sum_{i=1}^{n} x_i p_i$$
.

The mean of a random variable X is also called the expectation of X, denoted by E(X).

Let X be a random variable whose possible values  $x_1, x_2, ..., x_n$  occur with probabilities  $p(x_1), p(x_2), ..., p(x_n)$  respectively.

Let  $\mu = E(X)$  be the mean of X. The variance of X, denoted by Var (X) or

$$\sigma_x^2$$
, is defined as  $\sigma_x^2 = \text{Var}(X) = \sum_{i=1}^n (x_i - \mu)^2 p(x_i)$ 

or equivalently  $\sigma_{x}^{2} = E(X - \mu)^{2}$ 

The non-negative number

$$\sigma_x = \sqrt{\operatorname{Var}(X)} = \sqrt{\sum_{i=1}^{n} (x_i - \mu)^2 p(x_i)}$$

is called the standard deviation of the random variable X.

- $Var(X) = E(X^2) [E(X)]^2$
- Trials of a random experiment are called Bernoulli trials, if they satisfy the following conditions:
  - (i) There should be a finite number of trials.
  - (ii) The trials should be independent.
  - (iii) Each trial has exactly two outcomes: success or failure.
  - (iv) The probability of success remains the same in each trial.

For Binomial distribution B (n, p), P  $(X = x) = {}^{n}C_{x} q^{n-x} p^{x}$ , x = 0, 1,..., n (q = 1 - p)

## **Historical Note**

The earliest indication on measurement of chances in game of dice appeared in 1477 in a commentary on Dante's Divine Comedy. A treatise on gambling named *liber de Ludo Alcae*, by Geronimo Carden (1501-1576) was published posthumously in 1663. In this treatise, he gives the number of favourable cases for each event when two dice are thrown.

Galileo (1564-1642) gave casual remarks concerning the correct evaluation of chance in a game of three dice. Galileo analysed that when three dice are thrown, the sum of the number that appear is more likely to be 10 than the sum 9, because the number of cases favourable to 10 are more than the number of cases for the appearance of number 9.

Apart from these early contributions, it is generally acknowledged that the true origin of the science of probability lies in the correspondence between two great men of the seventeenth century, Pascal (1623-1662) and Pierre de Fermat (1601-1665). A French gambler, Chevalier de Metre asked Pascal to explain some seeming contradiction between his theoretical reasoning and the observation gathered from gambling. In a series of letters written around 1654, Pascal and Fermat laid the first foundation of science of probability. Pascal solved the problem in algebraic manner while Fermat used the method of combinations.

Great Dutch Scientist, Huygens (1629-1695), became acquainted with the content of the correspondence between Pascal and Fermat and published a first book on probability, "*De Ratiociniis in Ludo Aleae*" containing solution of many interesting rather than difficult problems on probability in games of chances.

The next great work on probability theory is by Jacob Bernoulli (1654-1705), in the form of a great book, "Ars Conjectendi" published posthumously in 1713 by his nephew, Nicholes Bernoulli. To him is due the discovery of one of the most important probability distribution known as Binomial distribution. The next remarkable work on probability lies in 1993. A. N. Kolmogorov (1903-1987) is credited with the axiomatic theory of probability. His book, 'Foundations of probability' published in 1933, introduces probability as a set function and is considered a 'classic!'.

![](_page_56_Picture_6.jpeg)