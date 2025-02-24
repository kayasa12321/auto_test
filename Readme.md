# 使用手册
## 前置步骤
1.首先确保自己已经安装de3并且按照手册的方法已经成功的配置好。[de3工具地址](https://github.com/XChy/de3)
2.配置需要的工具SVF，并且按照其手册配置完成saber的配置。[svf地址](https://github.com/SVF-tools/SVF)
3.wllvm（因为svf接受的是链接后的文件的bitcode）
## 生成负优化版本的代码
直接执行deopt.py这个脚本。
`python deopt.py /path/to/seed_dir /path/to/output_dir --max-mutations 15 --repeat-times 3 --executable ./de3/build/deoptgen --ld-preload /home/kayasa/gcc131/lib64/libstdc++.so.6`
其中 前两个是输入的文件目录以及输出的文件目录，然后max-mutations是最大的混乱度，其中默认的是15，然后repeat-times是指重复执行的次数，其默认为1，--executable是指其中de3中可执行文件的地址，其默认的地址是./de3/build/deoptgen，可以自行修改，后续的--ld-preload是所需要的其余的环境变量。
当执行这条指令后，他会对seed_dir目录下所有的bitcode文件执行de3中的` ./build/deoptgen -pipeline-type=1 -m 15 /path/to/seed -o /path/to/mutant`这条指令，并且会按照输入文件的名字在输出文件下生成子目录来生成对应的多次负优化版本的ir，为了防止重名，输出就会变为`output_dir/seed_filename/execution_<execution_num>_mutant_<max_mutations>_<seed_file> `。

## SVF中的saber分析
直接执行analyse.sh这个脚本（首先就是给脚本权限），其中提供输入文件目录和输出文件目录两个参数，其中输出文件目录可以不用提供，能根据输入文件目录自动创建，然后利用saber的三种支持的类型检测，其中包括内存泄漏、资源泄露和释放后使用，对输入文件目录以及其子文件目录中的每一个ir文件执行
```  
    saber -leak -stat=false "$file" > "$output_file"
    saber -dfree -stat=false "$file" >> "$output_file"
    saber -fileck -stat=false "$file" >> "$output_file" 
```
并且将输出结果输出到对应的txt文档中，并且使得输出文件目录结构和输入文件目录结构能够保持一致。

因为我们需要的是将负优化和优化版本都需要比较，所以要对前一个步骤所下的seed文件目录和output文件目录下的结果都需要执行这个脚本，然后用作前后比较。

### 一体化执行
可以直接执行union——version.py这个脚本，输入参数和前面的deopt.py类似，但是需要进行的就是其中的末尾需要添加一个参数--script-path ./your_script.sh，这个必须提供，因为没有提供默认参数。

## 结果对比
就是将svf对优化和负优化版本的结果进行比较，找出其中结果不同的样例，其需要三个参数，其中一个是原先版本的分析结果所在文件，还有一个就是负优化结果所在的文件地址，最后一个就是比对结果所在的地址