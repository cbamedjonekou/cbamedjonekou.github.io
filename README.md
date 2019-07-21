# CBA's Portfolio:

This portfolio covers the following topics: Machine Learning Models (both classical and deep learning models), Mathematical Modeling using Discrete and Continuous Dynamical Systems, Data Structures and Algorithms, IoT/Embedded Systems, Drones, Red/Blue Teaming, and anything else that catches my eye. Formally, I'm an Applied Mathematics student but through my continuous exposure with different technologies/methods (while using Math as a base/springboard) I hope to co-op the title '***Hacker***'.


**Follow me throughout my journey.**

***Definition: Hacker | Hacker Culture - subculture of individuals who enjoy the intellectual challenge of creatively overcoming limitations of systems to achieve novel and clever outcomes***  

#### Editor Note:

* I'm currently doing an overhaul of this repo/portfolio. Anything labeled ***under construction*** is currently being modified and is not yet complete. 

# Machine Learning In Astronomy Coursework:

* Spring 2019 PHYS3600ID: Machine Learning In Astronomy Coursework.

## RR Lyrae Dataset

### Decision Tree Model | Cross Validation

***[under construction]***

[View](https://nbviewer.jupyter.org/github/deaththeberry/ML-AI-HKG_Portfolio/blob/master/Labs/PHYS%203600ID-D862%20%28Machine%20Learning%29/PHYS%203600ID-D862%20%28Machine%20Learning%29%20RR-Lyrae%20Decision%20Tree%20Classifier.ipynb?flush_cache=true)|[Download](https://github.com/deaththeberry/ML-AI-HKG_Portfolio/blob/master/Labs/PHYS%203600ID-D862%20(Machine%20Learning)/PHYS%203600ID-D862%20(Machine%20Learning)%20RR-Lyrae%20Decision%20Tree%20Classifier.ipynb)

* RR Lyrae are variable stars in the Lyra constellation. It plays a significant role in astronomy and has been studied extensively by Astronomers. The reason for this is because they are the brightest star in their class. This particular characteristic of RR Lyrae is important as it acts as a ***standard candle*** that can be used to meaure astronimical distances ([more on RR Lyrae here](https://en.wikipedia.org/wiki/RR_Lyrae_variable)). For this particular problem, we are presented with a dataset that contains 93141 instances (stars) with each instance containing 4 features which are the colors of the star. These colors which give an indication of whether a star emits more blue, green, yellow, or red light. We are also provided with the target vector implying that this is a supervised task. We use Decisions Trees in an attempt to classify the 93141 instances (stars) either as an RR Lyrae variable star or not. We also have an instance of unbalanced data here (we investigate the pitfalls of unbalanced data) and use methods in an attempt to resolve this issue.  

### Logistic Regressions Model

***[under construction]***

[View](https://nbviewer.jupyter.org/github/deaththeberry/ML-AI-HKG_Portfolio/blob/master/Labs/PHYS%203600ID-D862%20%28Machine%20Learning%29/PHYS%203600ID-D862%20%28Machine%20Learning%29%20RR-Lyrae%20Logistic%20Regression.ipynb?flush_cache=true)|[Download](https://github.com/deaththeberry/ML-AI-HKG_Portfolio/blob/master/Labs/PHYS%203600ID-D862%20(Machine%20Learning)/PHYS%203600ID-D862%20(Machine%20Learning)%20RR-Lyrae%20Logistic%20Regression.ipynb)

* Using the RR Lyrae Dataset again, we continue to explore classification Machine Learning algorithms, particularly Logistic Regression. Logistic Regression despite its name is a Classification algorithm. Logistic Regression is modeled after the Logistic Function which itself is a type of Sigmoid Function. Sigmoid Functions are valuable in that that calculate the log-odds; Log-odds is an alternative representation of probabilities. A little more specifically, they represent odds of an event happening (the ratio of the probability of success to the probability of failure). Logistics Regression assigns weight (probabilities) to a particular instance which determines the odds of it falling in one *class* or the other. We explore the effectiveness of the algorithm as well as its pitfalls. 

## Study Hours Dataset 

### Linear Regression | Gradient Descent Model

***[Close to Completion]***

[View](https://nbviewer.jupyter.org/github/deaththeberry/ML-AI-HKG_Portfolio/blob/master/Labs/PHYS%203600ID-D862%20%28Machine%20Learning%29/PHYS%203600ID-D862%20%28Machine%20Learning%29%20Study%20Hours%20Linear%20Regression.ipynb?flush_cache=true)|[Download](https://github.com/deaththeberry/ML-AI-HKG_Portfolio/blob/master/Labs/PHYS%203600ID-D862%20(Machine%20Learning)/PHYS%203600ID-D862%20(Machine%20Learning)%20Study%20Hours%20Linear%20Regression.ipynb)  

* Here, we use the Study Hours Dataset. The Study Hours Dataset contains one feature vector (amount of hours studied) and one target vector (scores on the exam), both of which are continuous (There are no categories) so Regression seems appropriate here. It's a simple dataset which we'll use to illustrate the Linear Regression | Gradient Descent Models for regression tasks. A concise theory is provided and implementations are done from scratch as well as will Scikit-Learn & TensorFlow.  


## Higgs Boson Dataset

### Support Vector Machines:

***[under construction]***

[View](https://nbviewer.jupyter.org/github/deaththeberry/ML-AI-HKG_Portfolio/blob/master/Labs/PHYS%203600ID-D862%20%28Machine%20Learning%29/PHYS%203600ID-D862%20%28Machine%20Learning%29%20Higgs%20Boson%20SVM.ipynb?flush_cache=true)|[Download](https://github.com/deaththeberry/ML-AI-HKG_Portfolio/blob/master/Labs/PHYS%203600ID-D862%20(Machine%20Learning)/PHYS%203600ID-D862%20(Machine%20Learning)%20Higgs%20Boson%20SVM.ipynb)

* We use the Higgs Boson Dataset, to implement/evaluate the Support Vector Machine (SVM) ML Model. Higgs Bosons, and the Higgs Field, are fundamentals in the Standard Model of Particle Physics. They are necessary in linking Electromagnetic force to Weak force (Electroweak force). More on the Higgs Boson [here](https://home.cern/science/physics/higgs-boson). We use the SVM to classify events into "tau tau decay of a Higgs boson" versus "background"; The dataset contained Simulated data with features characterizing events detected by ATLAS. More on the Higgs Dataset [here](https://www.kaggle.com/c/higgs-boson). We compare the result to a Decision Tree Classifier.

### Ensemble Methods: Random Forests | Extremely Random Trees:

***[under construction]***

[View](https://nbviewer.jupyter.org/github/deaththeberry/ML-AI-HKG_Portfolio/blob/master/Labs/PHYS%203600ID-D862%20%28Machine%20Learning%29/PHYS%203600ID-D862%20%28Machine%20Learning%29%20Higgs%20Boson%20Ensemble%20Methods.ipynb?flush_cache=true)|[Download](https://github.com/deaththeberry/ML-AI-HKG_Portfolio/blob/master/Labs/PHYS%203600ID-D862%20(Machine%20Learning)/PHYS%203600ID-D862%20(Machine%20Learning)%20Higgs%20Boson%20Ensemble%20Methods.ipynb)

* We use the Higgs Boson Dataset, to implement/evaluate Ensemble Methods: Random Forests, Extremely Random Trees. We use the Ensemble Methods to classify events into "tau tau decay of a Higgs boson" versus "background"; The dataset contained Simulated data with features characterizing events detected by ATLAS. More on the Higgs Dataset [here](https://www.kaggle.com/c/higgs-boson). We compare the result to a Decision Tree Classifier, evaluate Feature Importance, and find ideal hyperparameters. 


## Galaxies Dataset

### KMeans Clustering:

***[under construction]***

[View](https://nbviewer.jupyter.org/github/deaththeberry/ML-AI-HKG_Portfolio/blob/master/Labs/PHYS%203600ID-D862%20%28Machine%20Learning%29/PHYS%203600ID-D862%20%28Machine%20Learning%29%20Galaxy%20Classifier%20KMeans%20Clustering.ipynb?flush_cache=true)|[Download](https://github.com/deaththeberry/ML-AI-HKG_Portfolio/blob/master/Labs/PHYS%203600ID-D862%20(Machine%20Learning)/PHYS%203600ID-D862%20(Machine%20Learning)%20Galaxy%20Classifier%20KMeans%20Clustering.ipynb)

* To illustrate the KMeans (unsupervised) clustering model, we used a sample of the Galaxy Zoo Dataset (found on [Kaggle](https://www.kaggle.com/c/galaxy-zoo-the-galaxy-challenge)) which is a collection of images of different types of Galaxies. Galaxies, independent of this dataset, are classified into several different categories (shapes): Ellipticals, Spirals/Barred spirals, Irregulars. Since this is an unsupervised task (we withheld the target data), we use the KMeans clustering model primarily as an exploratory tool. The goal, ultimately, is to see the ability of KMeans in clustering galaxies together based off of similar characteristics.  

### Convolutional | Deep Neural Networks:

***[under construction]***

* For this project, we set out to create a Deep Learning Model, specifically a Convoluational Neural Network (CNN), to analyze the Galaxies Dataset. The goal of this assignment is to act as a introduction to Deep Learning, and Neural Networks. We present the results of our implementation of the CNN, parameter validation, generalization errors, and visualizations. Python, and Google's open source **Tensorflow**, were used to implement the CNN for this problem. We will give you an overview of our experience playing around with tutorials/examples then show the results for the morphology classification of galaxies.

[READ ME](https://github.com/deaththeberry/NeuralNetworkProject/blob/master/README.md)

# Python Modules:

# Mathematical Modeling of Continuous and Discrete Dynamical Systems Coursework:

## SIS "Common Cold" Model

[Report](https://github.com/deaththeberry/ML-AI-HKG_Portfolio/blob/master/Labs/MAT%204880-D692%20(Math%20Modeling%20II)/MAT%204880-D692%20(Math%20Modeling%20II)%20SIS%20Model%20Project%201.pdf)|[Jupyter](https://nbviewer.jupyter.org/github/deaththeberry/ML-AI-HKG_Portfolio/blob/master/Labs/MAT%204880-D692%20%28Math%20Modeling%20II%29/Appendix%20to%20the%20SIS%20Susceptibles%20vs.%20Infected%20Model.ipynb?flush_cache=true)

* In this study, we set out to create an SIS “Susceptibles vs. Infected” Model of the common cold over a 6-day period. The goal was to find the steady state of the dynamical system given the rate of infection, fixed population, and rate of recovery for the common cold. The common cold is a type of disease in which once recovered, a person is susceptible to infection again. Although the problem could be modeled using a discrete dynamical system, the objective required that we use a continuous dynamical system. We find the equilibrium points, reproductive number, and discuss the significance of both. We used sage/python to model and analyze this problem. 

## RLC Model: Eigenvalue Method

[Report](https://github.com/deaththeberry/ML-AI-HKG_Portfolio/blob/master/Labs/MAT%204880-D692%20(Math%20Modeling%20II)/MAT%204880-D692%20(Math%20Modeling%20II)%20RLC%20Model%20Project%202.pdf)|[Jupyter](https://nbviewer.jupyter.org/github/deaththeberry/ML-AI-HKG_Portfolio/blob/master/Labs/MAT%204880-D692%20%28Math%20Modeling%20II%29/Appendix%20to%20the%20RLC%20Electrical%20Circuit%20Model.ipynb?flush_cache=true)

* In this study, we set out to create an RLC Model of a Simple Series RLC Circuit. The goal was to find the steady state of the dynamical system given the $\frac{dq}{dt}$ (rate of change of q) and its rate of change $\frac{d^2q}{dt^2}$ as state variables. RLC circuits are used in many electronic systems, most notably as tuners in AM/FM radios. These circuits can be modeled by second-order, constant-coefficient differential equations; This is what we did here. We find the equilibrium points, and discuss their significance. We used sage/python to model and analyze this problem. 

## SEIRV Malware Model

[Report](https://github.com/deaththeberry/ML-AI-HKG_Portfolio/blob/master/Labs/MAT%204880-D692%20(Math%20Modeling%20II)/MAT%204880-D692%20(Math%20Modeling%20II)%20SEIRV%20Model%20Final%20Project.pdf)|[Jupyter](https://nbviewer.jupyter.org/github/deaththeberry/ML-AI-HKG_Portfolio/blob/master/Labs/MAT%204880-D692%20%28Math%20Modeling%20II%29/MAT%204880-D692%20%28Math%20Modeling%20II%29%20Final%20Project%20Sim.ipynb?flush_cache=true)

* In this study, we set out to create an SEIRV Model that models propagation of malware in wireless systems. The goal is to run simulations of the dynamical system for arbitrary lengths of time. Malware Propagation Models have previously been used to characterize the behavior of the network compartments with passage of time; This is what we'll do here through simulation. We will model this problem using a discrete time dynamical system as it will serve as an approximation to the continuous dynamical system. Python and Euler's Method are used to create and run the simulations for this problem. Ultimately, we seek to demonstrate the effect that the timestep, Δ𝑡, has on the simulation; Particularly, the effect of a 10%, 50%, and 100% increase in the timestep.

**More Coursework [Here](https://github.com/deaththeberry/ML-AI-HKG_Portfolio/blob/master/Labs/MAT%204880-D692%20(Math%20Modeling%20II)/README.md)**
