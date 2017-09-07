
**Data Visualization of U.S. Airline Delays & On-Time Performance, 2003-2017**
-- by Krish

***

**Summary**

There are 6 visualizations shown here. The first 5 graphs try to show which type of delay actually affects the most to a U.S. Airline Carrier. The last one shows each airlines' annual average of on-time arrivals. The data was collected from RITA for the period of 2003 - 2017.

**Design, EDA & Data Preparation**

The data was downloaded from RITA for the time period of June 2003 to June 2017. It included all domestic flights from all carriers to and from major airports. EDA (Exploratory Data Analysis) was conducted using Rstudio.

At first we loaded the data into a data-frame and checked first 10 values. NA values were then replaced with zeros (0).

Considering the variables at hand, we can focus our analysis on many things. I decided to focus on 2 things:

1. The type of delay which affects the most in the overall delay of a particular carrier
2. The overall performance of a carrier based on the "On Time" arrival percentage.
On Time = Arrival/(Total Flights)

While studying the data, I presumed that there might be trends in individual airline performance (Arrival/(Total Flights)) over the period.
A line chart for each carrier might best show the different trends across different airline carriers.

An initial plot of the arrival flights to year for each carrier is made. From the plot nothing is clear as it's too chaotic with high number of carriers present and hence we need to check with smaller number of carriers.

```{r, echo=FALSE, message=FALSE, warning=FALSE,fig.width=13}

library(ggplot2)
library(dplyr)

airlines <- read.csv("airline_delay_causes.csv")
head(airlines, 10)
airlines[is.na(airlines)] <- 0

ggplot(data = airlines,
       aes(x = year, y = arr_flights)) +
  geom_line(aes(color = carrier_name)) +
  scale_x_continuous(limits=c(2003, 2017), breaks=c(2003:2017))

```
![Image_01](https://github.com/sekhar989/Udacity-DAND/blob/master/P6-Data%20Viz%20-Dimple.js/images/unnamed-chunk-1-1.png?raw=true)
```{r, echo=FALSE, message=FALSE, warning=FALSE,}

a_new <- airlines %>%
  group_by(carrier_name) %>%
  summarise(n = n()) %>%
  arrange(desc(n))

a_new <- head(a_new, 5)

cr_nm <- a_new$carrier_name
droplevels(a_new$carrier_name)

airlines_sub <- subset(airlines, carrier_name == cr_nm)
```
After replacing the NA values, a check was made with the number of occurences of a Flight Carrier. We took a count of the carrier names which were present in the dataset and sorted the count in descending order. We selected top 5 carriers from that list and created a subset of the main data-frame which has only those 5 carriers. They are listed below:

a. SkyWest Airlines Inc.
b. ExpressJet Airlines Inc.
c. Delta Air Lines Inc.
d. American Eagle Airlines Inc.
e. American Airlines Inc.

```{r, echo=FALSE, message=FALSE, warning=FALSE,}
airlines_sub <- airlines_sub %>%
  group_by(year, carrier_name) %>%
  summarise(arrival = sum(arr_flights),
            delay = sum(arr_del15),
            cancelled = sum(arr_cancelled),
            diverted = sum(arr_diverted),
            arrival_delay = sum(X.arr_delay),
            carrier_delay = sum(X.carrier_delay),
            wthr_delay = sum(weather_delay),
            ns_delay = sum(nas_delay),
            sec_delay = sum(security_delay),
            lt_air_delay = sum(late_aircraft_delay)) %>%
  transform(on_time = arrival/(delay + cancelled + diverted + arrival)) %>%
  transform(carrier_delay = carrier_delay/arrival_delay) %>%
  transform(wthr_delay = wthr_delay/arrival_delay) %>%
  transform(ns_delay = ns_delay/arrival_delay) %>%
  transform(sec_delay = sec_delay/arrival_delay) %>%
  transform(lt_air_delay = lt_air_delay/arrival_delay)
```

After filtering the data with the top 5 carriers occuring in the dataset, we plot the same plot again along with another plot (on_time vs year for each carrier). Things are easier to handle now.


```{r, echo=FALSE, message=FALSE, warning=FALSE,fig.width=13, fig.height=9}
ggplot(data = airlines_sub,
       aes(x = year, y = arrival)) +
  geom_line(aes(color = carrier_name)) +
  scale_x_continuous(limits=c(2003, 2017), breaks=c(2003:2017))

ggplot(data = airlines_sub,
       aes(x = year, y = on_time)) +
  geom_line(aes(color = carrier_name)) +
  scale_x_continuous(limits=c(2003, 2017), breaks=c(2003:2017))
```
![Image_02](https://github.com/sekhar989/Udacity-DAND/blob/master/P6-Data%20Viz%20-Dimple.js/images/unnamed-chunk-4-1.png?raw=true)
![Image_03](https://github.com/sekhar989/Udacity-DAND/blob/master/P6-Data%20Viz%20-Dimple.js/images/unnamed-chunk-4-2.png?raw=true)

The frist thing which is noticed is that "American Eagle Airlines"  do not have data after 2014.
Further analyis on delay was made by potting the different delays with time for each carrier.
There are 5 types of delay mentioned in the data set, listed below:

1. Carrier Delay: Delay caused by the carriers
2. Weather Delay: Delay caused due to weather conditions
3. NAS Delay: Delay caused by National Aviation Services
4. Security Delay: Delay caused due to Security
5. Late Arrival Delay: Delay by late arrival of flights

```{r, fig.width=13, fig.height=9}
ggplot(data = airlines_sub,
       aes(x = year, y = carrier_delay)) +
  geom_line(aes(color = carrier_name)) +
  scale_x_continuous(limits=c(2003, 2017), breaks=c(2003:2017))
```
![Image_04](https://github.com/sekhar989/Udacity-DAND/blob/master/P6-Data%20Viz%20-Dimple.js/images/unnamed-chunk-5-1.png?raw=true)
```{r, fig.width=13, fig.height=9}
ggplot(data = airlines_sub,
       aes(x = year, y = wthr_delay)) +
  geom_line(aes(color = carrier_name)) +
  scale_x_continuous(limits=c(2003, 2017), breaks=c(2003:2017))
```
![Image_05](https://github.com/sekhar989/Udacity-DAND/blob/master/P6-Data%20Viz%20-Dimple.js/images/unnamed-chunk-5-2.png?raw=true)
```{r, fig.width=13, fig.height=9}
ggplot(data = airlines_sub,
       aes(x = year, y = ns_delay)) +
  geom_line(aes(color = carrier_name)) +
  scale_x_continuous(limits=c(2003, 2017), breaks=c(2003:2017))
```
![Image_06](https://github.com/sekhar989/Udacity-DAND/blob/master/P6-Data%20Viz%20-Dimple.js/images/unnamed-chunk-5-3.png?raw=true)
```{r, fig.width=13, fig.height=9}
ggplot(data = airlines_sub,
       aes(x = year, y = sec_delay)) +
  geom_line(aes(color = carrier_name)) +
  scale_x_continuous(limits=c(2003, 2017), breaks=c(2003:2017))
```
![Image_07](https://github.com/sekhar989/Udacity-DAND/blob/master/P6-Data%20Viz%20-Dimple.js/images/unnamed-chunk-5-4.png?raw=true)
```{r, fig.width=13, fig.height=9}
ggplot(data = airlines_sub,
       aes(x = year, y = lt_air_delay)) +
  geom_line(aes(color = carrier_name)) +
  scale_x_continuous(limits=c(2003, 2017), breaks=c(2003:2017))
```
![Image_08](https://github.com/sekhar989/Udacity-DAND/blob/master/P6-Data%20Viz%20-Dimple.js/images/unnamed-chunk-5-5.png?raw=true)

From the visualizations it's clearly visible that "security delay"" has the least amount of contribution among all the delay types. So, our focus will be on the other delay types.

Our cleaned & modified dataset seems good and hence, we write this data-frame to a .csv file
```{r}
write.csv(airlines_sub, file="airline_dimple_01.csv", row.names=FALSE)
```

Initial evaluation of these charts is that they are able to visualize the different trends of the 5 airlines properly. It can be seen how some airlines improved or deteriorated over time. We can also see which airline is currently performing better than the other four.

It also showed the general trends that all 5 airlines experienced: an aggregate dip in performance from 2005 to 2007 and another dip between 2012 to 2014.

A significant increase in the performace between 2011 to 2013 and again in between 2014 to 2016.

Moving on to the delay section, it's seen that delays caused by carrier, NAS & Late Arrival  of flight are the main contributors in the overall delay.

Though with time the contribution in delay from NAS side has reduced, the other two i.e. the contribution from Airlines Carrier & Late Arrival of flight,  has still a contribution of 30-40%.

**Data Visualization (dimple.js)**

A re-evaluation of the design was made, and still considered that a line chart is the best way to represent a trend of over time. Each line is given a specific color in order to visually encode each airline in a better fashion.
In order to improve the initial data visualization I improved it with dimple.js in the following ways:

a. Fix scaling in the y-axis, by converting the values to percentage for easier understanding.

b. Overlay scatter plot points to emphasize each airline's individual data points at each year.

c. Add transparency, as some areas of the graph (2010-2012) have considerable overlap.

This initial iteration can be viewed at index-initial.html, or below:
![Initial](https://github.com/sekhar989/Udacity-DAND/blob/master/P6-Data%20Viz%20-Dimple.js/images/localhost%208000%20main_01.html.png?raw=true)

**Feedback**

I requested for feedback from 3 individuals with a small set of questions. Their comments from them are listed below:

Feedback #1

***

> There are a number of graphs one after the other and it's hard to keep up if the 2nd or 3rd graph is related to the initial heading/title.

> The carrier and flight arrival delay has a similar percentage value for most of the airlines.

> The main takeaway here is that the on-time performance of the airlines fall and rise and again fall with time. Carrier and Late Arrival are the main reasons for delays.

> Highlighting a particular line and fading the rest will help in better focus on the area of study.

Feedback #2

***

> Line are easier to follow each "path" of points. It would have been a lot more confusing if there were only points.

> Large dips in in 2007, 2014 & again in 2017 is noticed showcasing the airlines'  performance.

> A more explanatory title would've been better.

Feedback #3

***

> The lines and points are colored differently, but I think it would be good to highlight or emphasize individual line when it is selected. It's a bit hard to follow a specific trend line.

> After having an idea of what the graphs were, I looked all the way to the right, because I wanted to know which airlines is delayed the most because of their carrier itself.

> Overall, it's clean.

**Post-feedback Modifications***

After receiving the feedback, I did the following changes:

i. Changed the chart title to be more consistent with the data presented.
ii. Made the delay graphs smaller in size and made them place in one grid.
iii. Added a mouseover event for the lines, in order to highlight the path. It'll help in better understanding a particular line of focus.
iv. Subdued and muted the grid lines.
v. Excluded the security delay related chart as the target is to showcase the main reasons which ultimately cause a delay.

Below is the final form of the data visualization:

![Final Image](https://github.com/sekhar989/Udacity-DAND/blob/master/P6-Data%20Viz%20-Dimple.js/images/plot.png?raw=true)

**Resources**

* [dimple.js Documentation](http://dimplejs.org/)
* [Dimple.js Lessons (Udacity)](https://classroom.udacity.com/nanodegrees/nd002/parts/00213454010/modules/318423863275460/lessons/3168988586/concepts/30639889960923)
* Stack Overflow posts
