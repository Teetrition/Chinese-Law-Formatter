# Chinese-Law-Formatter
A Python script to format Chinese law plain text to formatted XML file basically based on [Japanese e-Gov XML schema](https://elaws.e-gov.go.jp/download/), which is licensed under [its license](https://elaws.e-gov.go.jp/terms/). This license is compatible with CC BY 4.0. It is recommended and necessary to make sure your processed files has made attribution to [Japanese e-Gov XML schema](https://elaws.e-gov.go.jp/download/) and declare you have made modification. Attribution to this repository is not compulsory but welcomed.

将中国法纯文本格式化为XML文件的Python脚本，XML文件基本基于[日本e-Gov的XML schema](https://elaws.e-gov.go.jp/download/)，该schema在[其使用条款](https://elaws.e-gov.go.jp/terms/)下授权，该许可证兼容CC BY 4.0。您有必要在被处理后的文件中对[日本e-Gov的XML schema](https://elaws.e-gov.go.jp/download/)署名且声明您作出了修改。对本仓库的署名不是强制的，但我们欢迎您这么做。

Dependencies / 依赖：
* [cn2an](https://github.com/Ailln/cn2an)

Install cn2an / 可以通过以下命令安装它：
```
pip install cn2an
```

## 技术上不予适配以下法律法规，手工处理更为经济，请直接使用example中处理好的文件：
* 包含附件或附表的（如刑法）；
* 包含**目**及更低级别的（如海商法）；
* 宪法（含序言，列举条款部分未使用**项**）。

使用时请参照给出的示例（`中华人民共和国著作权法.txt`与`中华人民共和国公司法.txt`），文件名为法律名称，文件内容不要包含法律标题、题注和目录，从第一编/章（如果法律分编/章）或第一条（如果法律不分章）开始。
