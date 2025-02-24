import subprocess
import argparse
import os

def run_deoptgen_for_all(seed_dir, output_dir, max_mutations, pipeline_type, execution_num, executable="./build/deoptgen", ld_preload="/home/kayasa/gcc131/lib64/libstdc++.so.6"):
    """
    对 seed_dir 下的每个文件执行 deoptgen 指令，并将结果保存到 output_dir 中。
    
    :param seed_dir: 种子文件夹路径
    :param output_dir: 输出结果文件夹路径
    :param max_mutations: 最大变异次数
    :param pipeline_type: 变异流水线类型
    :param execution_num: 当前的执行次数，用于区分不同执行的结果
    :param executable: deoptgen 可执行文件路径
    :param ld_preload: LD_PRELOAD 环境变量路径
    """
    # 检查输入种子目录是否存在
    if not os.path.isdir(seed_dir):
        print(f"Error: Seed directory '{seed_dir}' does not exist.")
        return
    
    # 检查可执行文件是否存在
    if not os.path.isfile(executable):
        print(f"Error: Executable '{executable}' not found.")
        return

    # 确保输出目录存在（如果不存在）
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 遍历种子文件夹中的每个文件
    for seed_file in os.listdir(seed_dir):
        seed_path = os.path.join(seed_dir, seed_file)
        
        # 检查是否是文件
        if not os.path.isfile(seed_path):
            print(f"Skipping non-file entry: {seed_file}")
            continue

        # 为每个种子文件创建子目录
        seed_output_dir = os.path.join(output_dir, os.path.splitext(seed_file)[0])  # 使用种子文件名（不包括扩展名）作为子目录名
        if not os.path.exists(seed_output_dir):
            os.makedirs(seed_output_dir)

        # 设置输出文件路径，文件名包含当前的执行次数和变异次数
        output_path = os.path.join(seed_output_dir, f"execution_{execution_num}_mutant_{max_mutations}_{seed_file}")
        
        # 构造命令（修正 -m 参数）
        command = [
            executable,
            f"-pipeline-type={pipeline_type}",
            "-m", str(max_mutations),  # 使用当前的最大变异次数
            seed_path,
            "-o", output_path
        ]

        # 设置环境变量
        env = os.environ.copy()
        env["LD_PRELOAD"] = ld_preload

        try:
            # 执行命令
            print(f"Processing seed file: {seed_file} with max_mutations = {max_mutations} in execution {execution_num}")
            result = subprocess.run(command, text=True, capture_output=True, check=True, env=env)
            print(f"Success: Output written to {output_path}")

        except subprocess.CalledProcessError as e:
            # 捕获命令执行失败
            print(f"Error processing {seed_file}!")
            print("STDOUT:", e.stdout)
            print("STDERR:", e.stderr)

        except Exception as e:
            # 捕获其他异常
            print(f"Unexpected error processing {seed_file}: {e}")

def run_deoptgen_for_range(seed_dir, output_dir, max_mutations, pipeline_type, repeat_times, executable, ld_preload):
    """
    对每个种子文件，在每次执行时，从 6 到 max_mutations 执行多个变异次数。
    
    :param seed_dir: 种子文件夹路径
    :param output_dir: 输出结果文件夹路径
    :param max_mutations: 最大变异次数
    :param pipeline_type: 变异流水线类型
    :param repeat_times: 执行次数
    :param executable: deoptgen 可执行文件路径
    :param ld_preload: LD_PRELOAD 环境变量路径
    """
    for execution_num in range(1, repeat_times + 1):
        print(f"Starting execution {execution_num} of {repeat_times}...")
        
        # 对每个种子文件执行变异次数从 6 到 max_mutations
        for max_mutations in range(6, max_mutations + 1):
            print(f"Running with max_mutations = {max_mutations} in execution {execution_num}")
            run_deoptgen_for_all(seed_dir, output_dir, max_mutations, pipeline_type, execution_num, executable, ld_preload)

if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="Run deoptgen on seed files with specific mutation counts and repeat the execution.")
    parser.add_argument("seed_dir", type=str, help="Directory containing seed files")
    parser.add_argument("output_dir", type=str, help="Directory to save output files")
    parser.add_argument("--max-mutations", type=int, default=15, help="Maximum number of mutations (default: 15)")
    parser.add_argument("--pipeline-type", type=int, default=1, help="Pipeline type (default: 1)")
    parser.add_argument("--repeat-times", type=int, default=1, help="Number of times to repeat the execution (default: 1)")
    parser.add_argument("--executable", type=str, default="./build/deoptgen", help="Path to deoptgen executable")
    parser.add_argument("--ld-preload", type=str, default="/home/kayasa/gcc131/lib64/libstdc++.so.6", help="Path to LD_PRELOAD library")

    args = parser.parse_args()

    # 执行主函数，反复执行指定次数
    run_deoptgen_for_range(
        seed_dir=args.seed_dir,
        output_dir=args.output_dir,
        max_mutations=args.max_mutations,
        pipeline_type=args.pipeline_type,
        repeat_times=args.repeat_times,
        executable=args.executable,
        ld_preload=args.ld_preload
    )
