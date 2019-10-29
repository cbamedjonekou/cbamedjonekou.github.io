---
layout: post
mathjax: true
title: "A Brief Summary to Pierce's Introduction to Information Theory (Part 3)"
date: 2019-10-16
description: The second of a series of blog posts that attempts to give a concise introduction to Information Theory. This series of posts can act as a summary of events of Pierce's "An Introduction to Information Theory-Symbols, Signals and Noise".
tags: natural-language-processing artificial-intelligence information-theory introduction shannon concise wheel-of-fortune
---

<h2 id="Top">Introduction</h2>

In this post we look to provide a brief summary for Chapter 3 (<i>"The Origins of Information Theory"</i>) of [Pierce's](https://archive.org/details/symbolssignalsan002575mbp/page/n27) <i>"An Introduction to Information Theory: Symbols, Signals, and Noise</i>. Skip to <a href="#tldr">TL;DR</a> for a summary of the summary (that's so [meta](https://www.grammarly.com/blog/meta-meaning/)).

<h2 id="TOC">Table of Contents</h2>
<ul>
    <li><a href="#tldr">TL;DR</a></li>
    <li><a href="#MM">What is a Mathematical Model?</a></li>
    <li><a href="#ith-order-approx">$i$-th Order Letter Approximation of English Text</a>
        <ul>
            <li><a href="#0th-order-approx">Zero Order Letter Approximation of English Text</a></li>
            <li><a href="#1st-order-approx">First Order Letter Approximation of English Text</a></li>
            <li><a href="#2nd-order-approx">Second Order Letter Approximation of English Text</a></li>
            <li><a href="#n-order-approx">Letter Approximations greater than 2</a></li>
        </ul>
    </li>
    <li><a href="#Morse">Morse Code and the Telegraph</a></li>
    <li><a href="#Fourier">Contributions of Joseph Fourier</a></li>
    <li><a href="#Nyquist">Contributions of Harry Nyquist</a></li>
    <li><a href="#Hartley">Contributions of R.V.L. Hartley</a></li>
    <li><a href="#Shannon">Contributions of Claude Shannon,</a></li>
    <li><a href="#Conclusion">Conclusion</a></li>
</ul>

<h2 id="tldr">TL;DR</h2>

To be written later.

<h2 id="MM">What is a Mathematical Model?</h2>
<a href="#TOC">Back to Table of Contents</a>

We start Chapter 3 discussing what a mathematical model is. A mathematical model is a simplification of our environment, or phenomena; It is a simplified version of our world focusing only on what is relevant to the behavior that is under consideration.

<blockquote cite="https://archive.org/details/symbolssignalsan002575mbp/page/n27">
    <p>
        "A Mathematical Theory which seeks to explain and to predict the events in the world about us always deals with a simplified model of the world, a mathematical model in which only things pertinent to the behavior under consideration enter...The great beauty and power of a mathematical theory or model lies in the separation of the relevant from the irrelevant, so that certain observable behavior can be related and understood without the need of comprehending the whole nature and behavior of the universe."
    </p>
    <footer>-Pierce, John R.</footer>
</blockquote>

A benefit of creating mathematical models is that we can start simple and then iterate over them, adding (what we perceive to be) relevant features over time. Additionally, mathematical models can have various degrees of application and accuracy. This means that our model does not have to be perfectly descriptive (exact in description) of the phenomenon in order to be effective (e.g.: accurately predicting orbits of planets by considering them rigid bodies, despite the fact that no truly rigid bodies exist). Mathematical Models are also good at modeling ***deterministic*** systems; Deterministic Systems are systems that are predictable as they follow the same sort of pattern every time.

<blockquote cite="https://archive.org/details/symbolssignalsan002575mbp/page/n27">
    <p>
        "...idealize <i>deterministic</i> systems which have the sort of predictable behavior we ordinarily expect from machines."
    </p>
    <footer>-Pierce, John R.</footer>
</blockquote>

There are caveats to consider, however. Pierce infers that while certain phenomena may be predictable (or ***deterministic***), there is a degree of unpredictability still present with regard to said phenomena.

<blockquote cite="https://archive.org/details/symbolssignalsan002575mbp/page/n27">
    <p>
        "Even the individual economic man is deterministic, for he will always act for his economic gin. But, if he at some time gambles on the honest throw of a die because the odds favor him, his economic fate becomes to a degree unpredictable, for he may lose even though the odds do favor him."
    </p>
    <footer>-Pierce, John R.</footer>
</blockquote>

This is especially true for humans. Phenomena regarding human behavior, particularly human communication for which we are interested in, tend to be more successfully modeled by statistical models as opposed to [deterministic](https://en.wikipedia.org/wiki/Deterministic_system) ones. [Statistical Models](https://en.wikipedia.org/wiki/Statistical_model) allows for randomness which is the reason why we use them to model human behavior. [Claude Shannon](https://en.wikipedia.org/wiki/Claude_Shannon), the man whose work is considered in this post (and in Pierce's book in general), formed a mathematical process (and model) demonstrating how English words and text can be approximated and carried out by machines. We examine this below.

<h2 id="ith-order-approx">$i$-th Order Letter Approximation of English Text</h2>
<a href="#TOC">Back to Table of Contents</a>

We begin to examine how Claude Shannon formed a mathematical process (and model) demonstrating how English words and text can be approximated and carried out by machines. We only consider letter approximations up to third order to demonstrate a point: with each increase in order, we start to form letter combinations that start to resemble words in English (or any other language). Finding probabilities of letters are important to this discussion.

<h3 id="0th-order-approx">Zero Order Letter Approximation of English Text</h3>

When we talk about Zero Order Letter Approximation of English Text, we consider that each letter (26 letters) have two qualities: that they have equal probability (the chance of selecting one letter is equal to another letter), and that they are independent from each other (selecting one letter has nothing to do with selecting another letter).

<blockquote cite="https://archive.org/details/symbolssignalsan002575mbp/page/n27">
    <p>
        "Suppose, for instance that we merely produce a sequence of letters and spaces with equal probabilities. We might do this by putting equal numbers of cards marked with each letter and with the space into a hat, mixing them up, drawing a card, recording its symbol, returning it, remixing, drawing a card, and so on. This gives what Shannon calls the zero-order approximation to English text. His example, obtained by an equivalent process goes:
        <p> 1. Zero-order approximation (symbols independent and equi-probable):</p>
        <p>XFOML RXKHRJFFJUJ ZLPWCFWKCYJ FFJEYVKCQSGHYD QPAAMKBZAACIBZLHJQD</p>
        "
    </p>
    <footer>-Pierce, John R.</footer>
</blockquote>

The problem with zero-order, as shown above, is that our sequence does not mimic English text at all with each letter appearing at equal frequency. We have a bunch of consonants appearing one after the other. We try and resolve this in our discussion of first-order approximations.

<h3 id="1st-order-approx">First Order Letter Approximation of English Text</h3>

First Order Letter Approximation differs from zero order approximation via one feature: letters no longer have equal probability, and follow more closely the frequency of letters in English text. The means certain letters, such as the letter 'E', have higher relative frequency (probability) than others. However, the fact that the letters are independent from each other still remains.

<blockquote cite="https://archive.org/details/symbolssignalsan002575mbp/page/n27">
    <p>
        "...We can approach more nearly to English text by choosing letters independently of one another, but choosing E more often than W or Z. We could do this by putting many E's and few W's and Z's into the hat, mixing, and drawing out the letters. As the <i>probability</i> that a given letter is an E should be .13, out of every hundred letters we put in the hat 13 should be E's. As the probability that a letter will be W should be .02, out of each hundred letters we put in the hat, 2 should be W's, and so on. Here is the result of an equivalent procedure, which gives what Shannon calls a first-order approximation of English text:
        <p> 2. First-order approximation (symbols are independent but with frequencies of English text):</p>
        <p>OCRO HLI RGWR NMIELWIS EULL NBNESEBYA TH EEI ALHENHTTPA OOBTTVA NAH BRL</p>
        "
    </p>
    <footer>-Pierce, John R.</footer>
</blockquote>

First order approximations move us closer to English text but we're still not quite there yet. The main problem with first-order, as shown above, is that letters in English (and other languages for that matter) are not independent of each other. For example, in English text we almost never encounter any pairing of letters beginning 'Q' except 'QU'. This extends to other pairings as well. These pairings are called ***digram probabilities*** (or [bigram](https://en.wikipedia.org/wiki/Bigram)) and are the center our discussion for second-order approximations, next.

<h3 id="2nd-order-approx">Second Order Letter Approximation of English Text</h3>

For Second Order approximations we consider pairings of letters called ***digrams*** (or [bigrams](https://en.wikipedia.org/wiki/Bigram)) which have probabilities (relative frequencies) that are [conditional](https://en.wikipedia.org/wiki/Conditional_probability) as opposed to zero & first order approximations which are independent. They have frequencies of English text just like first order approximations. To calculate their relative frequencies you'll need [Bayes' Theorem](https://en.wikipedia.org/wiki/Bayes%27_theorem).

<blockquote cite="https://archive.org/details/symbolssignalsan002575mbp/page/n27">
    <p>
        "3. Second-order approximation (digram structure as in English):
        <p>ON IE ANTSOUTINYS ARE T INCTORE ST BE S DEAMYACHIN D ILONASIVE TUCOOWE AT TEASONARE FUSO TIZIN ANDY TOBE SEACE CTISBE</p>
        "
    </p>
    <footer>-Pierce, John R.</footer>
</blockquote>

Second order approximations move us even closer to English text that first and zero order approximations. From our example we can see that we got a couple of words using [bigram probabilities](https://en.wikipedia.org/wiki/Bigram)). To be specific we were able to obtain 5 English words: ON, ARE, BE, AT, ANDY. We can extend our our letter combinations to a length of $n$ where $n \geq 2$ thus increasing the order of the approximations. We cover this next.

<h3 id="n-order-approx">Letter Approximations greater than 2</h3>

We can have more letter combinations with sequences of 3 letters called [trigrams](https://en.wikipedia.org/wiki/Trigram) or of any length, generally called [n-grams](https://en.wikipedia.org/wiki/N-gram). Again, the probabilities of these n-grams are conditional and to calculate them you'll need Bayes' Theorem. The following is an example of a trigram (a special case of $n$-gram where $n = 3$).

<blockquote cite="https://archive.org/details/symbolssignalsan002575mbp/page/n27">
    <p>
        "3. Second-order approximation (digram structure as in English):
        <p>ON IE ANTSOUTINYS ARE T INCTORE ST BE S DEAMYACHIN D ILONASIVE TUCOOWE AT TEASONARE FUSO TIZIN ANDY TOBE SEACE CTISBE</p>
        "
    </p>
    <footer>-Pierce, John R.</footer>
</blockquote>

Second order approximations move us even closer to English text that first and zero order approximations. From our example we can see that we got a couple of words using [bigram probabilities](https://en.wikipedia.org/wiki/Bigram)). To be specific we were able to obtain 5 English words: ON, ARE, BE, AT, ANDY. We can extend our our letter combinations to a length of $n$ where $n \geq 2$ thus increasing the order of the approximations. We cover this next.


<h2 id="Morse">Morse Code and the Telegraph</h2>
<a href="#TOC">Back to Table of Contents</a>

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

<h2 id="Fourier">Contributions of Joseph Fourier</h2>
<a href="#TOC">Back to Table of Contents</a>

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

<h2 id="Nyquist">Contributions of Harry Nyquist</h2>
<a href="#TOC">Back to Table of Contents</a>

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
([found here](http://physics.oregonstate.edu/~hetheriw/whiki/ph415_s15/tasks/dsp/files/nyquist/Nyquist.pdf)) which showed that

<blockquote cite="https://archive.org/details/symbolssignalsan002575mbp/page/n27">
    <p>
        "...if one sends some number $2N$ of different current values per second, all the sinusoidal components of the signal with frequencies greater that $N$ are redundant, in the sense that they are not needed in deducing from the received signal the succession of current values which were sent."
    </p>
    <footer>-Pierce, John R.</footer>
</blockquote>

Basically in removing all higher frequencies above the threshold, one could still figure out which current values were sent.

<h2 id= "Hartley">Contributions of R.V.L. Hartley</h2>
<a href="#TOC">Back to Table of Contents</a>

Hartley, another contributer who Pierce speaks about, wrote a paper called [Transmission of Information](http://keszei.chem.elte.hu/entropia/Hartley1928text.pdf) (1928). In this paper, he regarded a sender of a message as:

<blockquote cite="https://archive.org/details/symbolssignalsan002575mbp/page/n27">
    <p>
        "...equipped with a set of symbols (the letters of the alphabet for instance) from which he mentally selects symbol after symbol, thus generating a sequence of symbols. He observed that a chance event, such as rolling balls into pockets, might equally well generate such a sequence."
    </p>
    <footer>-Pierce, John R.</footer>
</blockquote>

The result of this premise was the following equation:

<p>$$H = n \log s$$</p>

where $H$ is defined as the information of the message, $n$ is the number of symbols selected, and $s$ is the number of unique symbols in the set (from which symbols are selected). There are caveats, criteria that needs to be considered:

<blockquote cite="https://archive.org/details/symbolssignalsan002575mbp/page/n27">
    <p>
        "This is acceptable...only if successive symbols are chosen independently and if any of the $s$ symbols is equally likely to be to be selected."
    </p>
    <footer>-Pierce, John R.</footer>
</blockquote>

Hartley's premise is analogous to what Nyquist proposed. [Read More.](http://keszei.chem.elte.hu/entropia/Hartley1928text.pdf)

<h2 id="Shannon">Contributions of Claude Shannon</h2>
<a href="#TOC">Back to Table of Contents</a>

Shannon, whose work is the basis of Pierce's Book, primarily considered the problem of dealing with any signal selected from a group of signals. Specifically, his research focused on encoding messages chosen from known groups (of signals) so they can be transmitted accurately and swiftly in the presence of noise. For example, given a source text (an English text ***not of our choosing***, for example) as well an electric circuit of some kind (such as a noisy telegraph cable ***also not of our choosing***), Shannon showed that we can transmit the messages accurately and swiftly since we are allowed to choose the way we represent the message as a signal (amount of current values we allow) as well as the transmission rate. Making these assumptions change the dynamic of the problem: we go from "how do we treat a signal with noise in order to get the best estimate" to "what sort of signal can we send to best convey our messages given a particular noisy circuit".

<blockquote cite="https://archive.org/details/symbolssignalsan002575mbp/page/n27">
    <p>
        "Thus efficient coding and it's consequences form the chief substance of information theory."
    </p>
    <footer>-Pierce, John R.</footer>
</blockquote>

<h2 id="Conclusion">Conclusion</h2>

Pierce does not go to much into depth about Shannon's contributions in Chapter 2, because he claims to have the whole book for that (which is fact). Therefore, our summary of Chapter 2 ends on that note. Again, refer to <a href="#tldr">TL;DR</a> for an even more brief summary of what was covered in Chapter 2.

<img src="https://media.giphy.com/media/Y0btn5YtZRGNkTnvNx/giphy.gif">

<a href="#Top">Back to the Top</a>