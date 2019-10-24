---
layout: post
mathjax: true
title: "A Brief Summary: Pierce's Introduction to Information Theory (Part 2)"
date: 2019-10-16
description: The second of a series of blog posts that attempts to give a concise introduction to Information Theory. This series of posts can act as a supplement to Pierce's "An Introduction to Information Theory-Symbols, Signals and Noise".
tags: natural-language-processing artificial-intelligence information-theory introduction shannon concise wheel-of-fortune
---



### Chapter 2 - The Origins of Information Theory [[Pierce](https://archive.org/details/symbolssignalsan002575mbp/page/n27)]:

Pierce starts the discussion by asserting two historically opposing view points:

* That we can learn from the past (learn by studying earlier times & passed transgressions)

* And opposingly, that we can't learn from the past

He avoids choosing which of the two is correct (due to his lack of expertise in the subject) and instead asserts two view points of his own, which serve to set the tone for the chapter:

* The first is that we learn the most from phenomena in man-made things rather than from phenomena in nature. He cites the creation & study of the steam engine, planes, and ships as catalysts for the creation of thermodynamics, aerodynamics, and hydrodynamics respectively.

* The second is that with difficulty, understanding is won. And it is through this process that we can appreciate the value of our understanding of scientific discoveries & origins. (There’s some truth to this heuristic but is this a hard fact? Don’t know.)

He discusses some topics that may lead the reader astray; One topic fitting the criteria is entropy. Entropy is a term that represents two weakly related quantities: the entropy of thermodynamics/statistical mechanics, and the entropy of information theory.

<blockquote cite="https://archive.org/details/symbolssignalsan002575mbp/page/n27">
    <p>
        "A particular quantity called entropy is used in thermodynamics and in statistical mechanics. A particular quantity called entropy is used in communication theory......In 1920, L. Szilard, a physicist, used an idea of information in resolving a particular physical paradox. From these facts we might conclude that communication theory somehow grew out of statistical mechanics"
    </p>
    <footer>-Pierce, John R.</footer>
</blockquote>

Pierce asserts that they are not related quantities, thus, their applications are different (and in different domains). Below is an excerpt featuring the definitions:

<blockquote cite="https://archive.org/details/symbolssignalsan002575mbp/page/n27">
    <p>
        "In physics, <a href="https://en.wikipedia.org/wiki/Entropy">entropy</a> is associated with the possibility of converting thermal energy into Mechanical Energy.....Statistical Mechanics interprets an increase of entropy as a decrease in order or, if we wish, as a decrease in our knowledge..... The <a href="https://en.wikipedia.org/wiki/Entropy_(information_theory)">entropy</a> of communication theory is a measure of this uncertainty and the uncertainty or entropy is taken as a measure of the amount of information conveyed by a message from a source."
    </p>
    <footer>-Pierce, John R.</footer>
</blockquote>

He, however, relents that they're analogous to each other. [Attempts to form a relationship](https://en.wikipedia.org/wiki/Entropy_in_thermodynamics_and_information_theory) between the two have occurred, but it's safer to think of these quantities as distinct; The quantities involved in solving each entropy differ in context.

He also speaks in depth about the history of electrical communication for which information theory was derived. The reason, as emphasized in Chapter 1, is to give the reader an understanding of the problems and trials previous contributors faced when developing our theory for communication:

* Pierce discusses Morse Code and the creation of the electrical telegraph. [Morse Code](https://en.wikipedia.org/wiki/Morse_code) encodes letters, and words, as a series of dots, dashes, and spaces. The most frequent letters retained short code symbols (such as the letter 'e' which happens to be the most frequent letter in English) while the least frequent letters used long combinations of code symbols (the letter 'z' for instance). The lesson provided by Morse's code, one Pierce would like the reader to retain, is that it matters profoundly how one translates a message into electrical signals.

* He also brings up the construction of a Telegraph Circuit between Washington and Baltimore (circa. 1843). The construction of the telegraph circuit ran into some difficulties with underground cables, and later, submarine cables. If one where to send multiple messages over underground/undersea circuits the messages would merge at the receiving end. To combat this phenomenon, increasing the length of the symbols is an option. However, the result is a slow rate of transmission (a limit in transmission speed, in general).

By this point a few of the problems Information Theory addresses makes themselves known to us: merging of signals at the receiving end of a transmission, and the limits in transmission speeds.

Pierce also discusses another method used to increase the amount of symbols being transmitted over a given period of time; Increasing transmission speeds is one method (previously discussed). This method suggests an increase in the number of elements (current states) used in telegraphy. Single current, double current, and quadruplex telegraph systems are implementations of this method. They're discussed below:

* The Single Current Telegraph has two elements or states which can be used to construct the morse code: current (on, '1'), and no current (off, '0').

* The Double Current Telegraph has three elements or states which can be used to construct the morse code: forward current (current in wire, '+1'), no current (off, '0'), backward current (current out wire, '-1'). The result, however, is an equivalent response as the Single Current Telegraph.

* The Quadruplex Telegraph has four elements or states which can be used to construct the morse code. Two of the current states indicate direction while the other two indicate intensity: forward current (current in wire, '+1' and '+3'), and backward current (current out wire, '-1' and '-3'). A magnitude of '3' indicates higher intensity. You can send twice as many letters per minute as the previous two, with the ablility to send two symbols at a time.

By this point we are made aware of the two factors necessary to determine the amount of information being sent via telegraph: the speed of successive symbols (successive current values) over the circuit, or transmission speeds; and the amount of different symbols (different current values) available to choose from, or [multiplexing](https://en.wikipedia.org/wiki/Multiplexing#Telegraphy). But neither of these really solve our issues regarding the spread and overlap of the symbols (not yet, and not directly), and noise. Increasing power can help with noise but cables have limits. Ultimately, it was these problems that acted as a catalyst for the creation of Information Theory (in all its mathy goodness).

<blockquote cite="https://archive.org/details/symbolssignalsan002575mbp/page/n27">
    <p>
        “Early telegraphists understood intuitively a good deal about the limitations associated with speed of signaling, interference (or noise), difficulty in distinguishing among many alternative values in current, and the limitation on the power that one could use. More than an intuitive understanding was required. An exact Mathematical Analysis of such problems was needed.” -Pierce, John R.
    </p>
    <footer>-Pierce, John R.</footer>
</blockquote>

Pierce continues by citing the contributions of many people (p.30), and specifically French Mathematician/Physicist Fourier as central to the development of information theory to solve aforementioned problems.

* Fourier’s contribution to  electrical communication came in the form of [proofs and analysis](https://en.wikipedia.org/wiki/Fourier_analysis), specifically his proof concerning electric signals.

* Electrical Signals can be viewed as a bunch of sine waves, typically. Fourier proved a theorem which showed that “any variation of a quantity with time can be accurately represented as the sum of a number of sinusoïdal variations of different amplitudes, phases, and frequencies”.

* The caveat: the circuits cannot change with time (so only [passive components](https://en.wikipedia.org/wiki/Passivity_(engineering))) and that they behave in a linear manner,

* Criterion/Identifiers for defining Linear Circuits: Signals have to act independently of each other.

Pierce also speaks about the properties of electric signals (also attributed to [Fourier Analysis](https://en.wikipedia.org/wiki/Fourier_analysis)), specifically events that occur as signals enter and exit a circuit:

* Input signals (especially ones with multiple sinusoidal components) produce output signals (also w/ multiple sinusoidal components) of the same frequency but with a different phase via a delay ([Phase Shift](https://en.wikipedia.org/wiki/Phase_(waves)#Phase_shift)), and a shrinkage in amplitude ([Attenuation](https://en.wikipedia.org/wiki/Attenuation)).

* The amounts of attenuation and delay depend on the frequency of the sine wave.

* Generally speaking, it is expected that the output sginal will have a different shape in comparison to the input signal (p. 34).

* Caveat: "If the attenuation and delay of a circuit is the same for all frequencies, the shape of the output signal will be the same as that of the input signal; such a circuit is [distortionless](https://en.wikipedia.org/wiki/Heaviside_condition)." (p. 34)

Pierce concludes the discussion concerning Fourier's Analysis with this statement: "Fourier Analysis is a powerful tool for the analysis of transmission problems" (p. 34). He also notes that many who studied electrical communication (mathematicians, telegraphists, and engineers) did not understand the variety of results provided by Fourier Analysis, and the appropriate context in which they should be used. Hence, a lot of the combinations of signals created (touted as being desirable) failed mostly due to bad mathematics and wrong arguments. Enter Harry Nyquist. To put it simply, Nyquist was a better mathematician than most men who tackled telegraphy problems. His research in the field, like Fourier, was instrumental for the development of Information Theory.

<blockquote cite="https://archive.org/details/symbolssignalsan002575mbp/page/n27">
    <p>
        “In 1917, Harry Nyquist came to the American Telephone and Telegraph Company immediately after receiving his Ph.D. at Yale  (Ph.D.'s were considerably rarer in those days). Nyquist was a much better mathematician than most men who tackled the problems of telegraphy, and he was a clear, original, and philosophical thinker concerning communication. He tackled problems of telegraphy with powerful methods and with clear insight...”
    </p>
    <footer>-Pierce, John R.</footer>
</blockquote>

The result of his research was a paper, "Certain Factors Affecting Telegraph Speed", authored in 1924. This contribution addressed one of the problems mentioned earlier: namely the limitations associated with transmission speed.

<blockquote cite="https://archive.org/details/symbolssignalsan002575mbp/page/n27">
    <p>
        "...It clarifies the relation between the speed of telegraphy and the number of current values such as $+1$, $-1$ (two current values) or $+3$, $+1$, $-1$, $-3$ (four current values)."
    </p>
    <footer>-Pierce, John R.</footer>
</blockquote>

Pierce introduces Nyquist's formula $W = K \log_n m$ which describes this relationship, and ultimately, calculates transmission speeds.

<blockquote cite="https://archive.org/details/symbolssignalsan002575mbp/page/n27">
    <p>
        "...Nyquist says that if we send symbols (successive current values) at a constant rate, the speed of transmission '$W$' is related to '$m$', the number of possible combinations of different/independent symbols (synonymous w/ current values, or messages), by $$W = K \log_n m$$ where '$K$' is a constant whose value depends on how many successive current values are sent each second."
    </p>
    <footer>-Pierce, John R.</footer>
</blockquote>

The base, '$n$', of the logarithm is dependent the amount of current values used. In the case of two current values ('$0$' and '$1$') the following is true.

<table>
    <thead>
        <tr>
            <th colspan= "2">2 Current Values (Base 2)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>$m$</td>
            <td>$\log m$</td>
        </tr>
        <tr>
            <td>1</td>
            <td>0</td>
        </tr>
        <tr>
            <td>2</td>
            <td>1</td>
        </tr>
        <tr>
            <td>3</td>
            <td>1.6</td>
        </tr>
        <tr>
            <td>4</td>
            <td>2</td>
        </tr>
        <tr>
            <td>8</td>
            <td>3</td>
        </tr>
        <tr>
            <td>16</td>
            <td>4</td>
        </tr>
    </tbody>
</table>

<blockquote>
    <p>
        <b>Reminder: Computing the logarithm of a value for a given base is equivalent to finding the required exponent necessary to produce that value. $$\log_2(x) = 3 \space \rightarrow \space 2^3 = x$$ $x$ is the value and $x = 8$ in this case.</b>
    </p>
    <footer>-CBA, Leet Warrior</footer>
</blockquote>



For three current values, aka [Balanced Ternery Numeral System](https://en.wikipedia.org/wiki/Balanced_ternary), ('$-1$', '$0$', and '$+1$') the following is true :

<table>
    <thead>
        <tr>
            <th colspan= "2">3 Current Values (Base 3)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>$m$</td>
            <td>$\log m$</td>
        </tr>
        <tr>
            <td>1</td>
            <td>0</td>
        </tr>
        <tr>
            <td>2</td>
            <td>.63</td>
        </tr>
        <tr>
            <td>3</td>
            <td>1</td>
        </tr>
        <tr>
            <td>4</td>
            <td>1.26</td>
        </tr>
        <tr>
            <td>9</td>
            <td>2</td>
        </tr>
        <tr>
            <td>27</td>
            <td>3</td>
        </tr>
    </tbody>
</table>

The idea extends to $n \geq 4$ where $n$ is the base of the logarithm, and more specifically, the number of current values we choose to use. This relation proves mathematically what was intuitively understood. The more current values we use, the more combinations (possible combinations of different/independent symbols) we have available to choose from, and more messages we can send at once. As such '$W$', the transmission speeds, increase.

<a href= "/assets/Certain Factors Affecting Telegraph Speed Nyquist.pdf">OG Nyquist Paper found here</a>

Nyquist, however, confirmed what those before him figured out: the use of more current values is difficult due to noise, attenuation, etc. Nyquist later published another, more quantitive, paper
