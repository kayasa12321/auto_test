#!/bin/bash
# 获取两个目录路径和输出目录路径
dir1="$1"
dir2="$2"
output_dir="$3"

# 检查输出目录是否存在，如果不存在则创建
if [[ ! -d "$output_dir" ]]; then
    echo "输出目录 '$output_dir' 不存在，正在创建..."
    mkdir -p "$output_dir"
fi

# 遍历第一个目录中的所有文件
for file1 in "$dir1"/*; do
    # 获取文件名
    filename=$(basename "$file1")

    # 检查第二个目录中是否有同名的子目录
    subdir="$dir2/$filename"
    if [[ -d "$subdir" ]]; then
        echo "找到同名子目录: $filename"
        
        # 遍历子目录中的文件
        for file2 in "$subdir"/*; do
            # 获取文件名
            subfile=$(basename "$file2")
            

                # 使用 diff 比较两个文件
                if ! diff "$file1" "$file2" > /dev/null; then
                    echo "文件内容不同，复制到输出目录..."
                    
                    # 创建一个新的子目录，用于存放不同的文件
                    diff_dir="$output_dir/$filename"
                    mkdir -p "$diff_dir"
                    
                    # 将文件复制到输出目录
                    cp "$file1" "$diff_dir/$(basename "$file1")"
                    cp "$file2" "$diff_dir/$(basename "$file2")"
                    
                    echo "---------------------------"
                fi
            fi
        done
    fi
done
