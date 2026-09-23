# 科研分析入口的路径示例。
# 放到 study_project/scripts/01_analysis.R，并将 study_project 改为真实目录名。
# 只初始化路径并创建输出目录；不会读取数据或生成分析结果。

library(myutils)

# 先初始化项目及其适用的 renv 环境，再加载分析包。
ensure_wd(workdir = "study_project")

# 按实际分析需要加载依赖，例如：
# library(data.table)

# 当前项目的输入与输出；替换为项目声明的真实文件。
input_file <- wd_path("data", "analysis_input.rds")
out_dir <- wd_path("results", "01_analysis")
output_file <- file.path(out_dir, "analysis_result.rds")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

# 需要外层工作区文件时使用；要求已识别工作区或指定 workspace_root。
# shared_input_file <- ws_path("shared_data", "reference.rds")

# 只有实际存在并需要共享函数时才加载；不要为模板创建空 helper。
# source(wd_path("src", "analysis_helpers.R"))

# 在此加入真实分析。读取前核对声明的输入；仅输出允许的汇总。
# 本示例不自动加载数据、挑选统计方法或保存虚构结果。

cat("输入路径：", input_file, "\n", sep = "")
cat("输出路径：", output_file, "\n", sep = "")
