import subprocess
import argparse
import os

def run_deoptgen_for_all(seed_dir, output_dir, max_mutations, pipeline_type, executable="./build/deoptgen", ld_preload="/home/kayasa/gcc131/lib64/libstdc++.so.6"):
    """
    对 seed_dir 下的每个文件执行 deoptgen 指令，并将结果保存到 output_dir 中。
    
    :param seed_dir: 种子文件夹路径
    :param output_dir: 输出结果文件夹路径
    :param max_mutations: 最大变异次数
    :param pipeline_type: 变异流水线类型
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

    # 创建输出目录（如果不存在）
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 遍历种子文件夹中的每个文件
    for seed_file in os.listdir(seed_dir):
        seed_path = os.path.join(seed_dir, seed_file)
        
        # 检查是否是文件
        if not os.path.isfile(seed_path):
            print(f"Skipping non-file entry: {seed_file}")
            continue

        # 设置输出文件路径，修改文件名以反映当前的变异次数
        output_path = os.path.join(output_dir, f"mutant_{max_mutations}_{seed_file}")
        
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
            print(f"Processing seed file: {seed_file} with max_mutations = {max_mutations}")
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

def repeat_execution(seed_dir, output_dir, max_mutations, pipeline_type, repeat_times, executable, ld_preload, script_path):
    """
    反复执行 deoptgen 多次，每次使用相同的变异次数和流水线类型。
    
    :param seed_dir: 种子文件夹路径
    :param output_dir: 输出结果文件夹路径
    :param max_mutations: 最大变异次数
    :param pipeline_type: 变异流水线类型
    :param repeat_times: 执行次数
    :param executable: deoptgen 可执行文件路径
    :param ld_preload: LD_PRELOAD 环境变量路径
    :param script_path: 要执行的外部 shell 脚本路径
    """
    for i in range(repeat_times):
        print(f"Starting execution {i + 1} of {repeat_times}...")
        current_output_dir = os.path.join(output_dir, f"execution_{i + 1}")
        
        # 运行一次指定变异次数和流水线类型的处理
        run_deoptgen_for_all(seed_dir, current_output_dir, max_mutations, pipeline_type, executable, ld_preload)

    # 在所有 deoptgen 操作完成后，执行指定的外部 shell 脚本
    print("Executing the external shell script for seed_dir and output_dir...")
    try:
        # 执行外部 shell 脚本，并分别传递 seed_dir 和 output_dir 作为参数
        subprocess.run([script_path, seed_dir], check=True)
        subprocess.run([script_path, output_dir], check=True)
        print(f"Successfully executed {script_path} with {seed_dir} and {output_dir} as arguments.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing shell script: {e}")

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
    parser.add_argument("--script-path", type=str, required=True, help="Path to the external shell script to execute")

    args = parser.parse_args()

    # 执行主函数，反复执行指定次数
    repeat_execution(
        seed_dir=args.seed_dir,
        output_dir=args.output_dir,
        max_mutations=args.max_mutations,
        pipeline_type=args.pipeline_type,
        repeat_times=args.repeat_times,
        executable=args.executable,
        ld_preload=args.ld_preload,
        script_path=args.script_path
    )
