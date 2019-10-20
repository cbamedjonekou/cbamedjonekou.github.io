---
layout: post
mathjax: true
title: "A Concise Introduction to Information Theory Part 2"
date: 2019-10-16
description: The seond of a series of blog posts that attempts to give a concise introduction to Information Theory. This series of posts can act as a supplement to Pierce's "An Introduction to Information Theory-Symbols, Signals and Noise".
tags: natural-language-processing artificial-intelligence information-theory introduction shannon concise wheel-of-fortune
---



### Chapter 2 - The Origins of Information Theory:

1. Pierce starts the discussion by asserting two historically opposing view points:

    * That we can learn from the past (learn by studying earlier times/passed transgressions)

    * That we cannot learn from the past

2. He then claims not to have the scope to choose which is correct and instead asserts two view points of his own:

    * That we learn the most from phenomena in man-made things rather than from phenomena in nature citing the study/creation of the steam engine, planes, and ships as catalyst for the creation of thermodynamics, aerodynamics, and hydrodynamics, respectively.

    * That with difficulty understanding is won. And it is through this process that we can appreciate the value of our understanding of scientific origin. (There’s some truth to this anecdote but is this a hard fact? Don’t know.)

    which serve to set the tone for the chapter.

3. He discusses some topics that may lead the reader astray; one being entropy. Entropy is a term that represent two weakly related quantities: the entropy of thermodynamics/statistical mechanics, and (it’s analogous counterpart) the entropy of information theory:

    <blockquote>
        <p>
            "A particular quantity called entropy is used in thermodynamics and in statistical mechanics. A particular quantity called entropy is used in communication theory......In 1920, L. Szilard, a physicist, used an idea of information in resolving a particular physical paradox from these facts we might include that communication theory somehow grew out of statistical mechanics" - Pierce, John R. 
        </p>
    </blockquote>

    Pierce asserts that they are not related quantities, thus, their applications are different in the different domains. Below is an excerpt featuring the definitions.

    <blockquote>
        <p>
            "In physics, <a href="https://en.wikipedia.org/wiki/Entropy">entropy</a> is associated with the possibility of converting thermal energy into Mechanical Energy.....Statistical Mechanics interprets an increase of entropy as a decrease in order or, if we wish, as a decrease in our knowledge..... The <a href="https://en.wikipedia.org/wiki/Entropy_(information_theory)">entropy</a> of communication theory is a measure of this uncertainty and the uncertainty or entropy is taken as a measure of the amount of information conveyed by a message from a source." - Pierce, John R.
        </p>
    </blockquote>

    He, however, relents that they are seen as analogous to each other. [Attempts to form a relationship](https://en.wikipedia.org/wiki/Entropy_in_thermodynamics_and_information_theory) between the two have occurred, but it's safer to think of these quantities as distinct; The quantities involved in solving each entropy differ in context.

4. He also goes into depth about the history of electrical communication here in Chapter 2, after he briefly touched upon it in Chapter 1. The reason, as emphasized in Chapter 1, is to give the reader an understanding of the problems and trials faced when developing the theory. Specifically, he discusses the following:

    * Morse Code and the creation of the electrical telegraph. [Morse Code](https://en.wikipedia.org/wiki/Morse_code) encodes letters, and words, as a series of dots, dashes, and spaces. The most frequent letters retained short code symbols (such as the most frequent letter in English, the letter 'e') while the least frequent letters used long combinations of code symbols. The lesson (the one Pierce would like the reader to retain) provided by Morse's code is that it matters profoundly how one translates a message into electrical signals.

    * The construction of a Telegraph Circuit between Washington and Baltimore (circa. 1843).  The construction of the telegraph circuit ran into some difficulties with underground cables. These difficulties later plagued submarine cables as well. If one where to send multiple messages over underground/undersea circuits the messages would merge at the receiving end. To combat this phenomenon, increasing the length of the symbols was an option. However, the result was slow rate of transmission (a limit in transmission speed, in general).

5. Pierce continues to discuss the methods used to increase the amount of symbols to be transmitted over a given period of time. One solution was to increase the number of elements (current states) used in telegraphy. Single current, double current, and quadruplex telegraph systems are discussed below:

    * The Single Current Telegraph has two elements or states which can be used to construct the morse code: current (on, '1'), and no current (off, '0'). You can only send one symbol at a time.

    * The Double Current Telegraph has three elements or states which can be used to construct the morse code: forward current (current in wire, '+1'), no current (off, '0'), backward current (current out wire, '-1'). Equivalent response as the Single Current Telegraph, you can only send one symbol at a time.

    * The Quadruplex Telegraph has four elements or states which can be used to construct the morse code. Two of the current states indicate direction while the other two indicate intensity. forward current (current in wire, '+1' and '+3'),and backward current (current out wire, '-1' and '-3'). A magnitude of '3' indicates higher intensity. You can send twice as many as the previous two, with the ablility to send two symbols at a time.

6. Pierce discusses two ways of increasing the amount of symbols being sent via telegraph: increase in the speed of successive current values (symbols) over the circuit, and increase in the amount of different current values (symbols) available. But neither of these really solve our issues regarding the spread and overlap of the symbols, and noise. Increasing power can help with noise but cables have limits. Ultimately, it was these problems that acted as a catalyst for the creation of Information Theory (in all its mathy goodness).

    * “Early telegraphists understoond intuitively a good deal about the limitations associated with speed of signaling, interference (or noise), difficultiy in distinguishing among many alternative values in current, and the limitation on the power that one could use. More than an intuitive understanding was required. An exact Mathematical Analysis of such problems was needed.” -Pierce, John R.

7. He then goes on to cite the contributions of many people (p.30), and specifically French Mathematician/Physicist Fourier.

    * Fourier’s contribution to  electrical communication came in the form of proofs and analysis, specifically his proof concerning electric signals.

    * Electrical Signals can be viewed as a bunch of sine waves, typically. Fourier proved a theorem which showed that “any variation of a quantity with time can be accurately represented as the sum of a number of sinusoïdal variations of different amplitudes, phases, and frequencies”.

    * The caveat: the circuits cannot change with time (so only [passive components](https://en.wikipedia.org/wiki/Passivity_(engineering))) and that they behave in a linear manner,

    * Criterion/Identifiers for defining Linear Circuits: Signals have to act independently of each other.

8. He continues to discuss electric signals, specifically events that occur as signals enter and exit a circuit:

    * Output signals that exit electric circuits tend to be different from the input signals in which they were derived. This can be a change in phase via delay ([Phase Shift](https://en.wikipedia.org/wiki/Phase_(waves)#Phase_shift)), or a shrinkage in amplitude ([Attenuation](https://en.wikipedia.org/wiki/Attenuation)).

    * The amounts of attenuation and delay depend on the frequency of the sine wave.
