writeLines("executed", "upstream_was_run.txt")
counts <- read.csv("data/summary.csv", stringsAsFactors = FALSE)
result_root <- "results"
dir.create(result_root, showWarnings = FALSE)
