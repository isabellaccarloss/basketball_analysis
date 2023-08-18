This prediction was made using the results of the first round of the playoffs due to the volume of data for the following rounds.

Therefore, the final result was assumed by using the % of chance of each team winning in the first round. 

Comments:
I collected data from regular seasons since 2001-02 and built a model to predict the winning probability in the first round. 
Setting the cutoff as 50% (if the probability is less than 50%, assume it is a loss and if higher, assume it a win), 
I got 81% of accuracy (first round only and probably overfit due to that).

Predicting the following rounds are harder (for each round we have less and less data, since have fewer teams playing) and it would 
take a little more time and creativity (I plan on working on that too, eventually). Therefore, in this analysis I assumed the 
probability of winning round 1 as the probability of winning the title and ranked the teams.

I wanted to post this today because the Lakers (against all odds, literally) beat the Timberwolves yesterday. 
A hard game that went to OT, so my guess was not that far from reality after all hahah. But this is the magic of basketball. 
It is always more than just data and probabilities. It is about heart, passion and how determined you are to win. 
Also, there is the "LeBron factor" that we obviously can not ignore neither calculate it. I believe the same thing is going to happen with the Warriors 
due to the "Curry factor". I added a "number of All Stars" variable to try to minimize this impact, but it was not enough 
(LeBron and Curry are not regular All Stars, let's be honest).
