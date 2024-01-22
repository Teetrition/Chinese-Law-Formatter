# Chinese-Law-Formatter
A Python script to format Chinese law plain text to formatted XML file basically based on [Japanese e-Gov XML schema](https://elaws.e-gov.go.jp/download/).

将中国法纯文本格式化为XML文件的Python脚本，XML文件基本基于[日本e-Gov的XML schema](https://elaws.e-gov.go.jp/download/)。

Dependencies / 依赖：
* [cn2an](https://github.com/Ailln/cn2an)

Install cn2an / 可以通过以下命令安装它：
```
pip install cn2an
```

## 未适配以下法律法规：
* 包含**编**、**分编**的（如民法典、刑法、民刑诉法等）；
* 包含**目**及更低级别的（如海商法）；
* 宪法（含序言，列举条款部分未使用**项**）。

使用时请参照给出的示例（`中华人民共和国著作权法.txt`与`中华人民共和国公司法.txt`），文件名为法律名称，文件内容不要包含法律标题和题注，从第一章（如果法律分章）或第一条（如果法律不分章）开始。