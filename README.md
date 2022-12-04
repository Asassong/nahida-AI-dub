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

获取`知识，与你分享。.wav`这样的wav格式音频文件，用我提供的程序即可转换。

其他样式请自行处理，数据集格式参见PaddleSpeech官方文档。

### 下载预训练模型

参考PaddleSpeech官方文档。

### 训练

用git bash运行官方的run.sh或者python运行我的程序run.py,官方的应该需要把所有路径改为绝对路径，expanduser方法对windows系统无效。后面的参数参考官方文档或自行查看程序。

## 其他

若米哈游觉得该项目侵犯了你们的权利，请提前通知。
