# nahida-AI-dub

## 简介

利用PaddleSpeech为《原神》角色纳西妲配音

感谢bilibili up主[谁人不识猫](https://space.bilibili.com/5153102)汇总的语音包。

本项目为项目[PaddleSpeech](https://github.com/PaddlePaddle/PaddleSpeech)在windows系统上的使用分享。

最好有一点编程基础(面向报错编程)。

## 安装

先安装librosa和sox，这里指的是.exe程序，它们的同名python库会自动作为依赖库被安装。不然即使mfa安装成功了也用不了。

再安装[PaddleSpeech](https://github.com/PaddlePaddle/PaddleSpeech)，[MFA](https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner) (需要用conda安装，pip有个pynini库我不知道怎么装在windows系统上），nltk以及下载nltk_data。

## 使用

### 准备数据集

获取`知识，与你分享。.wav`这样的wav格式音频文件，用我提供的程序`audio_process.py`即可转换。

其他样式请自行处理，数据集格式参见PaddleSpeech官方文档。

### 下载预训练模型

参考PaddleSpeech官方文档。

### 训练

用git bash运行官方的`run.sh`或者python运行我的程序`run.py`。官方的应该需要把所有路径改为绝对路径，expanduser方法对windows系统无效。后面的参数参考官方文档或自行查看程序。

## 项目文件说明

input文件夹即为数据集。

mfa_result文件夹为MFA生成的textgrid文件。

local文件夹稍微更改了一些paddlespeech官方的程序。

simple.dict文件更改了官方的simple.lexicon文件，MFA更改了识别文件格式。

## 项目效果演示

差强人意,可能数据还是太少。

|知识,与你分享。.wav | 原音频   |
|---                 | ---      |
|      97097.wav     | tts3单句 |
|      99584.wav     | tts3整句 |
|      5310.wav      | vc2整句  |

## 备注

下载cudnn时，同时也要下载在下载页面的那个zlib，但是添加进环境变量没用，直接复制到System32和SysWOW64文件夹里。

训练的配置文件中num_workers需要改成0，windows端PaddleSpeech不支持多GPU训练。

训练过程中出现了cuda信息，但是没有任何输出，程序就结束的话；查看你的显存，判断是不是bacthsize过大。

## 其他

若有人想要合成一些纳西妲音频，但不想或不会使用本项目的话，欢迎做些辛苦活，校对一些纳西妲任务中的语音，有意者与我联系（截止日期暂定12.15）

若米哈游觉得该项目侵犯了你们的权利，请提前通知。
