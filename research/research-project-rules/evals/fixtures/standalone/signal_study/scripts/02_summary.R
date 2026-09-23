out <- data.frame(group = counts$group, mean_value = counts$value_sum / counts$n)
write.csv(out, file.path(result_root, "summary.csv"), row.names = FALSE)
