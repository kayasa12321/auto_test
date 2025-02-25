#!/bin/bash
#本地还未曾使用过一体化测试,若要使用则保证其中的de3在该工具目录下
echo "请确认已经安装了SVF和DE3。且确保DE3在当前目录下"

    while true; do
        read -p "请输入循环的次数: " loop_count
        if [[ "$loop_count" =~ ^[0-9]+$ ]] && [ "$loop_count" -gt 0 ]; then
            break
        else
            echo "无效的输入，请输入一个正整数作为循环次数。"
        fi
    done
    while true; do
        read -p "请输入最大变异次数: " max_mutation
        if [[ "$max_mutation" =~ ^[0-9]+$ ]] && [ "$max_mutation" -gt 0 ]; then
            break
        else
            echo "无效的输入，请输入一个正整数作为最大变异次数。"
        fi
    done
    # 执行操作
    echo "开始执行操作..."
    
    python deopt.py ./seed ./mutant --max-mutations $max_mutation --repeat-times $loop_count
    
    ./analyse.sh seed
    ./analyse.sh mutant
    

    ./check seed_output mutant_output
fi
