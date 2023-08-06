
## Geotab Intersection Congestion

[Kaggle link](https://www.kaggle.com/c/bigquery-geotab-intersection-congestion)


### Data

In `data/` folder locally.

### Model

We will use a NN piecewise hazards approach, similar to the lifelike project. However, instead of using the log-likelihood as our loss, we will use the RMSE between predicted percentile and the actual percentile.

Ex:

S(t | x) = \exp(-H(t | x))

H(t | x) = \sum_{0}^t h_i(x)

where h_i(x) = NN(x)

The percentile, p, can be computed quickly (I think) using:


-log(1-p) = \sum_{0}^t h_i(x)

And solve t.


So we don't really need to ever work in the survival domain, we can just work in hazards.



#### Update

Solving -log(1-p) = \sum_{0}^t h_i(x) isn't trivial, at least it's not trivial to vectorize this.
Instead, we will predict values of -log(1-p), for p in np.linspace(0, 1, 100):



