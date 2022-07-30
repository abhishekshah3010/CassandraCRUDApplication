## ASSIGNMENT 3

- For implementing an enhanced feature in terms of query processing and optimization, we decided to implement a custom aggregate function: Quartile to the H2 database. Aggregate functions are functions that combine multiple records and then perform the function and return a single value as result. We decided Quartiles because it is a very commonly used statistical method for retrieving meaningful information from the dataset.

- Quartiles are used to summarize a group of numbers from the given data on which we use this function. Instead of looking at a big list of numbers, we look at just a few numbers that give us an insight of what’s going on with the data.

- Quartiles split up the data into four equal size groups. Out of them, the three main quartile are as follows:

- The first quartile (Q1) is defined as the middle number between the smallest number which is the minimum and the median which is the middle of the dataset. Q1 is the number that separates the lowest 25% of the data from the remaining 75% of the data.

- The second quartile (Q2) is the median of the data set. Q2 is the number in the middle of the group.

- The third quartile (Q3) is the middle number between the median and the highest value which is the maximum value in the dataset. Q3 is the number that separates the lowest 75% of the data from the highest 25% of the data.

- Quartiles divide the number of data points evenly. Therefore, the range is not the same between all three quartiles and this range is known as the interquartile range. Quartiles are generally used to calculate the interquartile range, which is a measure of variability around the median. 


- The interquartile range is simply calculated as the difference between the first and third quartile that is Q3–Q1. In effect, it is the range of the middle half of the data that shows how spread out the data is.

- The significance of Quartiles is that the upper and lower quartiles can provide more detailed information on the location of specific data points, the presence of outliers in the data set, and the difference in spread between the middle (50%) of the data and the outer data points.
