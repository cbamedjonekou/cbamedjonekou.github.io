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
    <li><a href="#ith-order-word">$i$-th Order Word Approximation of English Text</a>
        <ul>
            <li><a href="#1st-order-word">First Order Word Approximation of English Text</a></li>
            <li><a href="#2nd-order-word">Second Order Word Approximation of English Text</a></li>
            <li><a href="#n-order-word">Word Approximations greater than 2</a></li>
        </ul>
    </li>
    <li><a href="#FS-Markov-Automaton">Incorporating Grammar Rules (Shannon's Mathematical Model of Communication) via Markov Chains/Finite State Automaton</a></li>
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

First Order Letter Approximation differs from zero order approximation via one feature: letters no longer have equal probability, and follow more closely the frequency of letters in English text. This means certain letters, such as the letter 'E', have higher relative frequency (probability) than others. However, the fact that the letters are independent from each other still remains.

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
        "4. Third-order approximation (digram structure as in English):
        <p>IN NO IST LAT WHEY CRATICT FROURE BIRS GROCID PONDENOME OF DEMONSTURES OF THE REPTAGIN IS REGOACTIONA OF CRE</p>
        "
    </p>
    <footer>-Pierce, John R.</footer>
</blockquote>

As you can gather by now, increasing the order increases the chance of forming more English words/text. This time we have 8 English words formed: IN, NO, IST, LAT, WHEY, OF, THE, IS. This includes a bro-supplement, 'WHEY' (as in whey protein). We can extend these to other symbols, syllables, and words as well. We cover the use case for words in the next section.


<h2 id="ith-order-word">$n$-th Order Word Approximation of English Text</h2>
<a href="#TOC">Back to Table of Contents</a>

We can extend order approximations to words as well. Doing so makes sense in comparison to increasing the order of letter approximations to generate sequences of text. It is just a lot simpler to provide a machine with actual English words and have it produce sequence of text based on that rather than increasing the order of letter approximations to match the [longest English word](https://en.wikipedia.org/wiki/Longest_word_in_English) available. 

<blockquote cite="https://archive.org/details/symbolssignalsan002575mbp/page/n27">
    <p>
        "But it would be much simpler merely to supply machine with words rather than letters and to let it produce these words according to certain probabilities"
    </p>
    <footer>-Pierce, John R.</footer>
</blockquote>

This is done by using a corpus (or sequence of text) and creating a "dictionary" to select words from. Just like with letters you can have $n$-order approximations. We'll cover $n = 1, 2$ approximations.

<h3 id="1st-order-word">First Order Word Approximation of English Text</h3>

First Order Word Approximations have the exact same qualities as the <a href="#1st-order-approx">First Order Letter Approximations</a> discussed earlier; They follow more closely the frequency of words in English text. This means certain words, such as the word 'the', have higher relative frequency (probability) than others. Just like the case with letters, the words in a sequence are independent from each other.

To create a sequence of text, we would start by selecting words at random from an imaginary bucket (words w/ higher frequency would be selected more often) and appending them to our sequence.

<blockquote cite="https://archive.org/details/symbolssignalsan002575mbp/page/n27">
    <p>...This could be achieved by cutting text into words, scrambling the words in a hat, and then drawing out a succession of words. He (Shannon) calls this a first-order word approximation...
        <p> "5. First-order word approximation. Here words are chosen independently but with appropriate frequencies:</p>
        <p>REPRESENTING AND SPEEDILY IS AN GOOD APT OR COME CAN DIFFERENT NATURAL HERE HE THE A IN CAME THE TO OF TO EXPERT GRAY COME TO FURNISHES THE LINE MESSAGE HAD BE THESE</p>
        "
    </p>
    <footer>-Pierce, John R.</footer>
</blockquote>

The result is a string of text that makes no sense at all to any English speaker, however. The reason is simple: language is not some random assortment of words that are independent from each other. The choice of words that follow are dependent on the previous words used. We have a structure to our language. We could possibly handle this by using  ***digram probabilities*** (or [bigram](https://en.wikipedia.org/wiki/Bigram)) again, which is a second-order approximation. We discuss this next.

**Note: [Bigram](https://en.wikipedia.org/wiki/Bigram) can refer to pairings of words, syllables, or letters.**

<h3 id="2nd-order-word">Second Order Word Approximation of English Text</h3>

Second order word approximations are similar to <a href="#2nd-order-approx">second order letter approximations</a> in that we consider pairings of words instead of letters. They're still called ***digrams*** (or [bigrams](https://en.wikipedia.org/wiki/Bigram)) and the probabilities (relative frequencies) are [conditional](https://en.wikipedia.org/wiki/Conditional_probability) as opposed to first order word approximations which are independent. They have frequencies of English text just like first order approximations. [Bayes' Theorem](https://en.wikipedia.org/wiki/Bayes%27_theorem) is still very much relevant in calculating their relative frequencies.

<blockquote cite="https://archive.org/details/symbolssignalsan002575mbp/page/n27">
    <p>...Shannon constructed a random passage in which the probabilities a of pairs of words were the same as in English text by the following expedient. He chose a first pair of words at random in a novel. He then looked through the novel for the next occurrence of the second word of the first pair and added the word which followed it in this new occurrence, and so on. This process gave him the following second-order word approximation to English.
        <p>"6. Second-order word approximation. The word transition probabilities are correct, but no further structure is included:</p>
        <p> THE HEAD AND IN FRONTAL ATTACK ON AN ENGLISH WRITER THAT THE CHARACTER OF THIS POINT IS THEREFORE ANOTHER METHOD FOR THE LETTERS THAT THE TIME OF WHO EVER TOLD THE PROBLEM FOR AN UNEXPECTED.</p>
        "
    </p>
    <footer>-Pierce, John R.</footer>
</blockquote>

With second order word approximations we get more familiar chunks of English text compared to first order word approximations. We can continue this process with any value of $n > 2$ as well. We discuss Word Approximations greater than 2 ([n-grams](https://en.wikipedia.org/wiki/N-gram)) next.

<h3 id="n-order-word">Word Approximations greater than 2</h3>

We can have more word combinations with sequences of 3 words called [trigrams](https://en.wikipedia.org/wiki/Trigram) or of any length, generally called [n-grams](https://en.wikipedia.org/wiki/N-gram). Again, the probabilities of these n-grams are conditional and to calculate them you'll need Bayes' Theorem.

As aforementioned, increasing the order of approximations increases the chance of forming more English sequences of words/text. The discussion so far yields progress in our goal in getting machines to replicate english text as a native speaker would but there are still issues. For one, this method of production is heavily dependent on historical English text. To be more specific, the method is reliant on works that have been previously produced but does not produce any sentence that can/might be spoken by an English speaker (in the future).

<blockquote cite="https://archive.org/details/symbolssignalsan002575mbp/page/n27">
    <p>"...Such a scheme, even if refined greatly, would not, however, produce all sequences the words that a person might utter. Carried to an extreme, it would be confined to combinations of words which had occurred; otherwise, there would be no statistical data available on them. Yet I may say, "The magenta typhoon whirled the <a href="https://www.dictionary.com/browse/farded">farded</a> bishop away," and this may well never have been said before."</p>
    <footer>-Pierce, John R.</footer>
</blockquote>

Also, as we learned in grade school (or other levels of education), English (and language in general), deals not only in letters/words but also in [grammar](https://en.wikipedia.org/wiki/Grammar).

<blockquote cite="https://archive.org/details/symbolssignalsan002575mbp/page/n27">
    <p>"...The real rules of English text deal not with the letters or words alone but with classes of words and their rules of association, that is, with grammar. Linguist and engineers who try to make machines for translating one language into another must find these rules, so that Their machines can combine words to form grammatical utterances even when these exact combinations have not occurred before (And also so that the meaning of words in the text to be translated can be deduced from the context)..."</p>
    <footer>-Pierce, John R.</footer>
</blockquote>

We explore how Shannon incorporates grammar in the development of machines that can "speak English" in the next section.

<h2 id="FS-Markov-Automaton">Incorporating Grammar Rules (Shannon's Mathematical Model of Communication) via Markov Chains/Finite State Automaton</h2>
<a href="#TOC">Back to Table of Contents</a>



<h2 id="Nyquist">Contributions of Harry Nyquist</h2>
<a href="#TOC">Back to Table of Contents</a>



<h2 id= "Hartley">Contributions of R.V.L. Hartley</h2>
<a href="#TOC">Back to Table of Contents</a>



<h2 id="Shannon">Contributions of Claude Shannon</h2>
<a href="#TOC">Back to Table of Contents</a>



<h2 id="Conclusion">Conclusion</h2>



<img src="https://media.giphy.com/media/Y0btn5YtZRGNkTnvNx/giphy.gif">

<a href="#Top">Back to the Top</a>
