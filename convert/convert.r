# Install and load required packages if not already installed
if (!requireNamespace("jsonlite", quietly = TRUE)) {
  install.packages("jsonlite")
}
if (!requireNamespace("readr", quietly = TRUE)) {
  install.packages("readr")
}
if (!requireNamespace("dplyr", quietly = TRUE)) {
  install.packages("dplyr")
}
library(jsonlite)
library(readr)
library(dplyr)

# Function to create folder if it doesn't exist
create_folder <- function(folder_path) {
  if (!file.exists(folder_path)) {
    dir.create(folder_path)
    cat("created empty folder, need to make sure files are in appropriate folders, and restart the script\n")
    quit(save = "no", status = 0, runLast = FALSE)
  }
}

# Function to convert CSV to JSON
csv_to_json <- function(csv_file, json_file) {
  create_folder(dirname(json_file))
  
  data <- read.csv(csv_file, na.strings = "", stringsAsFactors = FALSE)  
  json_data <- toJSON(data, pretty = TRUE, na = "null")
  writeLines(json_data, json_file)
  cat("Conversion from CSV to JSON completed for file:", csv_file, "\n")
}

# Function to convert JSON to CSV
json_to_csv <- function(json_file, csv_file) {
  create_folder(dirname(csv_file))
  
  json_data <- fromJSON(json_file)
  df <- as.data.frame(json_data)
  df[is.na(df)] <- ""
  write.csv(df, csv_file, row.names = FALSE)
  cat("Conversion from JSON to CSV completed for file:", json_file, "\n")
}

# Function to process a list of files
process_files <- function(input_folder, output_folder) {
  input_files <- list.files(input_folder, full.names = TRUE)
  
  for (file in input_files) {
    
    if (tools::file_ext(file) %in% c("csv", "CSV")) {
      output_file <- file.path(output_folder, paste0(tools::file_path_sans_ext(basename(file)), "_output.json"))
      csv_to_json(file, output_file)
    } else if (tools::file_ext(file) %in% c("json", "JSON")) {
      output_file <- file.path(output_folder, paste0(tools::file_path_sans_ext(basename(file)), "_output.csv"))
      json_to_csv(file, output_file)
    } else {
      warning("Unsupported file format for conversion:", file, "\n")
    }
  }
}

# Example usage
input_folder <- "input_folder"
output_folder <- "output_folder"

process_files(input_folder, output_folder)
