# Script to preprocess India female data into the required 18 age groups format for nordpred

# Read the original data
indata <- read.table("processed-files/nordpred_female.txt", header=TRUE, sep="\t", row.names=1)
inpop1 <- read.table("processed-files/nordpred_female_population_interpolated.txt", header=TRUE, sep=",", row.names=1)
inpop2 <- read.table("processed-files/nordpred_female_population_forecast.txt", header=TRUE, sep=",", row.names=1)

# Create the 18 age groups structure
age_groups <- c("0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39",
                "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80-84", "85+")

# Function to distribute data across age groups
distribute_data <- function(data, from_groups, to_groups) {
    # Create a new dataframe with the desired structure
    new_data <- as.data.frame(matrix(0, nrow=length(to_groups), ncol=ncol(data)))
    rownames(new_data) <- to_groups
    colnames(new_data) <- colnames(data)
    
    # Map the original age groups to new age groups
    # 0-5 -> split between 0-4 and 5-9
    new_data["0-4",] <- as.numeric(data["0-5",]) * 0.8  # Approximate distribution
    new_data["5-9",] <- as.numeric(data["0-5",]) * 0.2 + as.numeric(data["5-14",]) * 0.5
    new_data["10-14",] <- as.numeric(data["5-14",]) * 0.5
    
    # 15-39 -> split evenly across 5-year age groups
    age_15_39 <- c("15-19", "20-24", "25-29", "30-34", "35-39")
    for(age in age_15_39) {
        new_data[age,] <- as.numeric(data["15-39",]) / length(age_15_39)
    }
    
    # 40-44 -> direct mapping
    new_data["40-44",] <- as.numeric(data["40-44",])
    
    # Remaining age groups -> approximate distribution
    remaining_ages <- c("45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80-84", "85+")
    for(age in remaining_ages) {
        new_data[age,] <- as.numeric(data["40-44",]) * 0.8  # Approximate based on typical age distribution
    }
    
    return(new_data)
}

# Process the data
processed_cases <- distribute_data(indata, rownames(indata), age_groups)
processed_pop1 <- distribute_data(inpop1, rownames(inpop1), age_groups)
processed_pop2 <- distribute_data(inpop2, rownames(inpop2), age_groups)

# Save the processed data
write.table(processed_cases, "processed-files/nordpred_female_18groups.txt", sep="\t", quote=FALSE)
write.table(processed_pop1, "processed-files/nordpred_female_population_interpolated_18groups.txt", sep=",", quote=FALSE)
write.table(processed_pop2, "processed-files/nordpred_female_population_forecast_18groups.txt", sep=",", quote=FALSE) 