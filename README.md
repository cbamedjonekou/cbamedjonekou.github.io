# CBA's Portfolio:

This portfolio covers the following topics: Machine Learning Models (both classical and deep learning models), Mathematical Modeling using Discrete and Continuous Dynamical Systems, Data Structures and Algorithms, IoT/Embedded Systems, Drones, Red/Blue Teaming, and anything else that catches my eye. Formally, I'm an Applied Mathematics student but through my continuous exposure with different technologies/methods (while using Math as a base/springboard) I hope to co-op the title '***Hacker***'.


**Follow me throughout my journey.**

***Definition: Hacker | Hacker Culture - subculture of individuals who enjoy the intellectual challenge of creatively overcoming limitations of systems to achieve novel and clever outcomes***  

# Machine Learning In Astronomy Coursework:

* Spring 2019 PHYS3600ID: Machine Learning In Astronomy Coursework.

## RR Lyrae Dataset 

### Decision Tree Model | Cross Validation

**| [View]() | [Download]() |**

* RR Lyrae are variable stars in the Lyra constellation. It plays a significant role in astronomy and has been studied extensively by Astronomers. The reason for this is because they are the brightest star in their class. This particular characteristic of RR Lyrae is important as it acts as a ***standard candle*** that can be used to meaure astronimical distances ([more on RR Lyrae here](https://en.wikipedia.org/wiki/RR_Lyrae_variable)). For this particular problem, we are presented with a dataset that contains 93141 instances (stars) with each instance containing 4 features which are the colors of the star. These colors which give an indication of whether a star emits more blue, green, yellow, or red light. We are also provided with the target vector implying that this is a supervised task. We use Decisions Trees in an attempt to classify the 93141 instances (stars) either as an RR Lyrae variable star or not. We also have an instance of unbalanced data here (we investigate the pitfalls of unbalanced data) and use methods in an attempt to resolve this issue.  

### Logistic Regressions Model

**| [View]() | [Download]() |** 

* Using the RR Lyrae Dataset again, we continue to explore classification Machine Learning algorithms, particularly Logistic Regression. Logistic Regression despite its name is a Classification algorithm. Logistic Regression is modeled after the Logistic Function which itself is a type of Sigmoid Function. Sigmoid Functions are valuable in that that calculate the log-odds; Log-odds is an alternative representation of probabilities. A little more specifically, they represent odds of an event happening (the ratio of the probability of success to the probability of failure). Logistics Regression assigns weight (probabilities) to a particular instance which determines the odds of it falling in one *class* or the other. We explore the effectiveness of the algorithm as well as its pitfalls. 

## Study Hours Dataset 

### Linear Regression | Gradient Descent Model

**| [View]() | [Download]() |**

* Here, we use the Study Hours Dataset. The Study Hours Dataset contains one feature vector (amount of hours studied) and one target vector (scores on the exam), both of which are continuous (There are no categories) so Regression seems appropriate here. It's a simple dataset which we'll use to illustrate the Linear Regression | Gradient Descent Models.  


## Higgs Boson Dataset

### Support Vector Machines:

**| [View]() | [Download]() |**

### Ensemble Methods: Random Forests | Extremely Random Trees:

**| [View]() | [Download]() |**

## Galaxies Dataset

### KMeans Clustering:

**| [View]() | [Download]() |**

To illustrate the KMeans (unsupervised) clustering model, we use the Galaxies Dataset which is a collection of images of different types of Galaxies.  

### Convolutional | Deep Neural Networks:

**| [View]() | [Download]() |**

# Python Modules:

# Mathematical Modeling of Continuous and Discrete Dynamical Systems Coursework:

## SIS "Common Cold" Model

**| [Report](https://github.com/deaththeberry/ML-AI-HKG_Portfolio/blob/master/Labs/MAT%204880-D692%20(Math%20Modeling%20II)/MAT%204880-D692%20(Math%20Modeling%20II)%20SIS%20Model%20Project%201.pdf) | [Jupyter](https://nbviewer.jupyter.org/github/deaththeberry/ML-AI-HKG_Portfolio/blob/master/Labs/MAT%204880-D692%20%28Math%20Modeling%20II%29/Appendix%20to%20the%20SIS%20Susceptibles%20vs.%20Infected%20Model.ipynb?flush_cache=true) |**

* In this study, we set out to create an SIS “Susceptibles vs. Infected” Model of the common cold over a 6-day period. The goal was to find the steady state of the dynamical system given the rate of infection, fixed population, and rate of recovery for the common cold. The common cold is a type of disease in which once recovered, a person is susceptible to infection again. Although the problem could be modeled using a discrete dynamical system, the objective required that we use a continuous dynamical system. We used sage/python to model and analyze this problem. Once modeled, finding the equilibrium points to the system is the next step as it shows the value in which the model reaches its steady state. Reaching the steady state (finding the equilibrium points) indicates that the recently observed behavior of the system will continue into the future. What that means for this problem is that we’ll expect the number of cases to converge to a point and remain there, or at least this is what we believe. Finally, we were interested the reproductive number as it will tell us if the disease will spread and approach the steady state or if it will eventually reach the disease-free state. As this is an SIS model we expect to the reproductive number to be greater than 1, indicating that it will reach the steady state.

## RLC Model: Eigenvalue Method

**| [Report](https://github.com/deaththeberry/ML-AI-HKG_Portfolio/blob/master/Labs/MAT%204880-D692%20(Math%20Modeling%20II)/MAT%204880-D692%20(Math%20Modeling%20II)%20RLC%20Model%20Project%202.pdf) | [Jupyter](https://nbviewer.jupyter.org/github/deaththeberry/ML-AI-HKG_Portfolio/blob/master/Labs/MAT%204880-D692%20%28Math%20Modeling%20II%29/Appendix%20to%20the%20RLC%20Electrical%20Circuit%20Model.ipynb?flush_cache=true) |**

* In this study, we set out to create an RLC Model of a Simple Series RLC Circuit. The goal was to find the steady state of the dynamical system given the $\frac{dq}{dt}$ (rate of change of q) and its rate of change $\frac{d^2q}{dt^2}$ as state variables. RLC circuits are used in many electronic systems, most notably as tuners in AM/FM radios. These circuits can be modeled by second-order, constant-coefficient differential equations; This is what we did here. We created a continuous dynamical system from the second-order differential equation, as mentioned above. We used sage/python to model and analyze this problem. Once modeled, finding the equilibrium points to the system was the next step as they show the value in which the model reaches its steady state. Reaching the steady state (finding the equilibrium points) indicates that the recently observed behavior of the system will continue into the future. What that means for this problem is that we’ll expect the current and its of change to converge to a point and remain there, or at least this is what we believe. Finally, we classify the equilibrium points using the Eigenvalue Method, and show a graphic of the model in the form of a Phase Portrait.

## SEIRV Malware Model

**| [Report]https://github.com/deaththeberry/ML-AI-HKG_Portfolio/blob/master/Labs/MAT%204880-D692%20(Math%20Modeling%20II)/MAT%204880-D692%20(Math%20Modeling%20II)%20SEIRV%20Model%20Final%20Project.pdf) | [Jupyter](https://nbviewer.jupyter.org/github/deaththeberry/ML-AI-HKG_Portfolio/blob/master/Labs/MAT%204880-D692%20%28Math%20Modeling%20II%29/MAT%204880-D692%20%28Math%20Modeling%20II%29%20Final%20Project%20Sim.ipynb?flush_cache=true) |** 

* In this study, we set out to create an SEIRV Model that models propagation of malware in wireless systems. The goal is to run simulations of the dynamical system for arbitrary lengths of time. Malware Propagation Models have previously been used to characterize the behavior of the network compartments with passage of time; This is what we'll do here through simulation. We will model this problem using a discrete time dynamical system as it will serve as an approximation to the continuous dynamical system. Python and Euler's Method are used to create and run the simulations for this problem. Ultimately, we seek to demonstrate the effect that the timestep, Δ𝑡, has on the simulation; Particularly, the effect of a 10%, 50%, and 100% increase in the timestep. We expect that a large increase in the timestep will produce a delay that will cause the simulation to fail to mimic its original characteristics (chaos).

**More Coursework [Here](https://github.com/deaththeberry/ML-AI-HKG_Portfolio/blob/master/Labs/MAT%204880-D692%20(Math%20Modeling%20II)/README.md)**