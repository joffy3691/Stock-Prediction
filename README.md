Proposed Methodology:

In the scenario of stocks, trends of the stocks can repeat but the stock price may never repeat itself. In our algorithm, rather than predicting the stock price itself based on past values, we take into consideration the stock trends of the past and use it to predict the future. This stock trend is obtained by using the delta function. We take the delta of everyday and input it into our data-set. Therefore, the output given by our algorithm is also in terms of delta. To obtain the final result we add this delta value to the existing stock price of the previous day.

We have found this method to be far more superior than taking previous stock values as input to predict future values. The reason being, the future stock values depend only on the trends and not the past value itself. With this innovation we were able to increase the accuracy of our prediction significantly. 

![image](https://user-images.githubusercontent.com/70327869/126194990-a33a436e-55d8-42f1-ae77-fd50ba3e73bf.png)

 
In our project, after taking the delta as inputs, we train two different models: SVR and LSTM. By training two different models, we get results based on two different approaches which further enhances the likeliness of an outcome. The drawbacks of one model are made up by the other. Thus, we don't rely heavily on a single model, which increases the safety of our predictions.

The results of multiple researchers show that nonlinear systems performed better than linear ones, and two-model systems performed better than single-model ones. Generally, models that relied on predictions from more than one algorithm had better accuracy in predicting the future stock prices. Hence, we have come up with a two-model prediction system for predicting stock price movements.

Screenshots: 

HOME PAGE:

![image](https://user-images.githubusercontent.com/70327869/126195021-de921175-a06e-408d-8de5-19de714ecc4c.png)

TCS STOCK PREDICTION:

![image](https://user-images.githubusercontent.com/70327869/126195053-bb6349df-1070-4b88-8282-de887d1b51eb.png)


INFY STOCK PREDICTION:

![image](https://user-images.githubusercontent.com/70327869/126195071-966e7f35-a2cc-4c69-a5d7-72a529685998.png)


DEPOSIT PAGE:

![image](https://user-images.githubusercontent.com/70327869/126195085-4e7af0fc-fe38-4113-b748-c67583c2ca10.png)

TRADES  PAGE:

![image](https://user-images.githubusercontent.com/70327869/126195098-5e0dda1f-1452-4c1e-bd99-7dbcdb597489.png)

PORTFOLIO  PAGE:

![image](https://user-images.githubusercontent.com/70327869/126195119-b1f63c27-1d12-4dad-b9d6-9ed8a1842438.png)

## Document
[Link to Document](https://github.com/vishnu-06/Stock-Prediction/blob/main/Intelligent%20Stock%20Trading.pdf)
