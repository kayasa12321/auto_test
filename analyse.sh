#!/bin/bash
cd $SVF_HOME
. ./setup.sh

input_dir="$1"
output_dir="${2:-$(dirname "$input_dir")/$(basename "$input_dir")_output}"  # 默认输出目录为输入目录的名称加 _output


if [ ! -d "$input_dir" ]; then
    echo "输入目录不存在!"
    exit 1
fi

# 如果输出目录不存在，则创建
if [ ! -d "$output_dir" ]; then
    echo "输出目录不存在，正在创建..."
    mkdir -p "$output_dir"
fi

find "$input_dir" -type f | while read -r file; do

    relative_path="${file#$input_dir/}"
    dir_path=$(dirname "$relative_path")
    filename=$(basename "$file")
    output_dir_path="$output_dir/$dir_path"

    if [ ! -d "$output_dir_path" ]; then
        mkdir -p "$output_dir_path"
    fi
    
    # 定义输出文件路径
    output_file="$output_dir_path/$filename.txt"
    
    # 执行三条命令并将输出保存到文件
    echo "处理文件: $file"
    saber -leak -stat=false "$file" > "$output_file"  #可以按照自己的需求找一下saber命令的绝对地址
    saber -dfree -stat=false "$file" >> "$output_file"
    saber -fileck -stat=false "$file" >> "$output_file"
done

echo "所有文件处理完成!"
