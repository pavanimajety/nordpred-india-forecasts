# Example of use of "nordpred"-functions.

# Nordpred:     R (www.r-project.org) & S-PLUS (www.insightful.com) functions 
#               for prediction of cancer incidence (as used in the Nordpred project).
# Written by:	Bjørn Møller and Harald Fekjaer <harald.fekjar@kreftregisteret.no>, 2000-2002
# See also:	http://www.kreftregisteret.no/software/nordpred

# Reading package:
source("nordpred.s")

# Reading data (Colon cancer for Norwegian males)
indata <- read.table("test/india-tye1_male.txt", header=TRUE, sep="", row.names=1)
inpop1 <- read.table("test/male-india.txt", header=TRUE, sep=",", row.names=1)
inpop2 <- read.table("test/male-india-pred.txt", header=TRUE, sep=",", row.names=1)
# Print column names for debugging
print("indata colnames:")
print(colnames(indata))
print("inpop1 colnames:")
print(colnames(inpop1))
# Remove the first column of indata to align with inpop1
indata <- indata[, -1]
# Combine historical and future population data
inpop <- cbind(inpop1, inpop2)
# Print dimensions for debugging
print(paste("Number of columns in indata:", ncol(indata)))
print(paste("Number of columns in inpop:", ncol(inpop)))

# Calculate number of periods based on available data
n_periods <- min(5, floor(ncol(inpop) / 5))  # Ensure we don't exceed 5 periods
print(paste("Number of periods:", n_periods))

# Run predictions:
est <- nordpred.estimate(cases=indata, pyr=inpop, noperiod=n_periods, startestage=5)
res <- nordpred.prediction(est, startuseage=6, cuttrend=c(0, .25, .5, .75, .75), recent=TRUE)

# This can also be done in one command:
# res <- nordpred(cases=indata, pyr=inpop, startestage=5, startuseage=6, noperiods=n_periods, cuttrend=c(0, .25, .5, .75, .75))

# The "nordpred"-function can also choose number periods to base predictions on:
  # This is done by listing candidate number of periods in "noperiods". 
  # If the goodness of fit test is rejected based on the widest base, 
  # the first period is exclude etc.
res <- nordpred(indata, inpop, startestage=5, startuseage=6, noperiods=4:6, cuttrend=c(0, .25, .5, .75, .75))

# Or with poisson link function (instead of the powerlink as used in the nordpred predictions):
est2 <- nordpred.estimate(indata, inpop, 4, 5, linkfunc="poisson")
res2 <- nordpred.prediction(est2, startuseage=6, cuttrend=c(0, .25, .5, .75, .75), recent=TRUE)

# Get results:
print.nordpred(res)
nordpred.getpred(res)
summary(res, printpred=FALSE)

# Get results with standardisation:
wstand <- c(0.12, 0.1, 0.09, 0.09, 0.08, 0.08, 0.06, 0.06, 0.06, 0.06, 0.05, 
            0.04, 0.04, 0.03, 0.02, 0.01, 0.005, 0.005)
            
round(nordpred.getpred(res, incidence=TRUE, standpop=NULL), 2)
round(nordpred.getpred(res, incidence=TRUE, standpop=wstand), 2)

# Plot results:
pdf("nordpred_example_plot.pdf", width=10, height=8)
plot(res, standpop=wstand)
dev.off()

# Plot results with power5 and poisson links:
pdf("nordpred_example_plot_poisson.pdf", width=10, height=8)
plot(res2, standpop=wstand)
dev.off()

# Different cut trend scenarios, using average drift (recent=FALSE):
pdf("nordpred_example_plot_trends.pdf", width=10, height=8)
plot(nordpred.prediction(est, startuseage=6, cuttrend=c(0, 0, 0, 0, 0), recent=FALSE), standpop=wstand, new=TRUE)
plot(nordpred.prediction(est, startuseage=6, cuttrend=c(1, 1, 1, 1, 1), recent=FALSE), standpop=wstand, new=FALSE, lty=c(1, 2))
plot(nordpred.prediction(est, startuseage=6, cuttrend=c(0, .25, .5, .75, .75), recent=FALSE), standpop=wstand, new=FALSE, lty=c(1, 4))
dev.off()

# Save predictions to a file
write.csv(nordpred.getpred(res, incidence=TRUE, standpop=wstand), "nordpred_example_predictions.csv") 