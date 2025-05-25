#!/usr/bin/env Rscript

# Parse named arguments
args <- commandArgs(trailingOnly = TRUE)

# Show help if requested
if ("--help" %in% args || "-h" %in% args) {
  cat("Usage: Rscript run-nordpred-analysis.R [options]\n\n")
  cat("Options:\n")
  cat("  --input-dir DIR    Input directory containing data files [required]\n")
  cat("  --state STATE      State name (e.g., goa) [required]\n")
  cat("  --gender GENDER    Gender (male/female) [required]\n")
  cat("  --plot-type TYPE   Type of plot to generate [default: main]\n")
  cat("                     Options: main, trends, both\n")
  cat("  --help, -h         Show this help message\n\n")
  cat("Example:\n")
  cat("  Rscript run-nordpred-analysis.R --input-dir test --state goa --gender male --plot-type both\n")
  quit(status=0)
}

arg_names <- c("--input-dir", "--state", "--gender", "--plot-type")
arg_values <- character(length(arg_names))
names(arg_values) <- arg_names
arg_values["--plot-type"] <- "main"  # default value

# Parse arguments
i <- 1
while (i <= length(args)) {
  if (args[i] %in% arg_names) {
    if (i + 1 <= length(args)) {
      arg_values[args[i]] <- args[i + 1]
      i <- i + 2
    } else {
      stop(paste("Missing value for argument:", args[i]))
    }
  } else if (args[i] %in% c("--help", "-h")) {
    # Help already shown above
    quit(status=0)
  } else {
    stop(paste("Unknown argument:", args[i]))
  }
}

# Check if all required arguments are provided
missing_args <- arg_names[arg_values == "" & arg_names != "--plot-type"]
if (length(missing_args) > 0) {
  stop(paste("Missing required arguments:", paste(missing_args, collapse=", ")))
}

# Validate plot type
valid_plot_types <- c("main", "trends", "both")
if (!arg_values["--plot-type"] %in% valid_plot_types) {
  stop(paste("Invalid plot type. Must be one of:", paste(valid_plot_types, collapse=", ")))
}

# Extract values
input_dir <- arg_values["--input-dir"]
state <- tolower(arg_values["--state"])
gender <- tolower(arg_values["--gender"])
plot_type <- arg_values["--plot-type"]

# Compose filenames
cases_file <- file.path(input_dir, paste0(state, "-t1_", gender, ".txt"))
pop_hist_file <- file.path(input_dir, paste0("population-", gender, "-", state, ".txt"))
pop_pred_file <- file.path(input_dir, paste0("population-", gender, "-", state, "-pred.txt"))

# Load nordpred functions (assumes nordpred.s is in working dir)
source("nordpred.s")

# Read data
indata <- read.table(cases_file, header=TRUE, sep="", row.names=1)
inpop1 <- read.table(pop_hist_file, header=TRUE, sep=" ", row.names=1)
inpop2 <- read.table(pop_pred_file, header=TRUE, sep=" ", row.names=1)

# Clean column names (remove X prefix if present)
clean_colnames <- function(df) {
  colnames(df) <- gsub("^X", "", colnames(df))
  return(df)
}
indata <- clean_colnames(indata)
inpop1 <- clean_colnames(inpop1)
inpop2 <- clean_colnames(inpop2)

# Remove first column of indata if it's not a year (for compatibility)
if (!all(colnames(indata) %in% colnames(inpop1))) {
  indata <- indata[, -1]
}

# Combine population data
inpop <- cbind(inpop1, inpop2)

# Calculate number of periods (max 5)
n_periods <- min(5, floor(ncol(inpop) / 5))

# Run nordpred
est <- nordpred.estimate(cases=indata, pyr=inpop, noperiod=n_periods, startestage=5)
res <- nordpred.prediction(est, startuseage=6, cuttrend=c(0, .25, .5, .75, .75), recent=TRUE)

# Standard population weights (example)
wstand <- c(0.12, 0.1, 0.09, 0.09, 0.08, 0.08, 0.06, 0.06, 0.06, 0.06, 0.05, 0.04, 0.04, 0.03, 0.02, 0.01, 0.005, 0.005)

# Generate plots based on plot type
if (plot_type %in% c("main", "both")) {
  # Main plot
  png(file=file.path(input_dir, paste0("nordpred_plot_", state, "_", gender, ".png")), width=1000, height=800)
  par(mar=c(5, 5, 4, 2))  # Increase margin for labels
  plot(res, standpop=wstand, xlab="Year", ylab="Age-standardized rate", main=paste("Nordpred Analysis:", toupper(state), toupper(gender)))
  dev.off()
}

if (plot_type %in% c("trends", "both")) {
  # Trends plot with different cut trend scenarios
  png(file=file.path(input_dir, paste0("nordpred_trends_", state, "_", gender, ".png")), width=1000, height=800)
  par(mar=c(5, 5, 4, 2))  # Increase margin for labels
  
  # Create empty plot first
  plot(1, type="n", xlim=range(as.numeric(colnames(inpop))), ylim=c(0, max(nordpred.getpred(res, incidence=TRUE, standpop=wstand))),
       xlab="Year", ylab="Age-standardized rate", main=paste("Trend Scenarios:", toupper(state), toupper(gender)))
  
  # Add each trend line
  res1 <- nordpred.prediction(est, startuseage=6, cuttrend=c(0, 0, 0, 0, 0), recent=FALSE)
  res2 <- nordpred.prediction(est, startuseage=6, cuttrend=c(1, 1, 1, 1, 1), recent=FALSE)
  res3 <- nordpred.prediction(est, startuseage=6, cuttrend=c(0, .25, .5, .75, .75), recent=FALSE)
  
  lines(as.numeric(colnames(nordpred.getpred(res1))), nordpred.getpred(res1, incidence=TRUE, standpop=wstand), lty=1, col="black")
  lines(as.numeric(colnames(nordpred.getpred(res2))), nordpred.getpred(res2, incidence=TRUE, standpop=wstand), lty=2, col="red")
  lines(as.numeric(colnames(nordpred.getpred(res3))), nordpred.getpred(res3, incidence=TRUE, standpop=wstand), lty=4, col="blue")
  
  # Add legend
  legend("topleft", 
         legend=c("No trend", "Full trend", "Recent trend"),
         lty=c(1, 2, 4),
         col=c("black", "red", "blue"),
         bty="n",
         cex=1.2)
  dev.off()
}

# Save predictions as CSV
write.csv(nordpred.getpred(res, incidence=TRUE, standpop=wstand), file=file.path(input_dir, paste0("nordpred_predictions_", state, "_", gender, ".csv")), row.names=TRUE)

cat("Analysis complete. Plots and predictions saved in", input_dir, "\n") 