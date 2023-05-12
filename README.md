最近在调整自己的论文追踪网站，发现从 arXiv 的 Comments 扒论文的中稿会议或期刊效率太低，且准确率也不高，想着还不如直接爬取会议接受的论文。

![image](https://github.com/chenluda/get-paper-from-openview/assets/45784833/71492fc8-8b9d-473d-a156-48baaf743806)

OpenReview 是一个旨在促进同行评审过程中透明度的平台。通常，OpenReview 公布接收结果的时间比会议官方网站要早。实际上，大部分论文推送网站也是从 OpenReview 上获取会议论文信息的。

![image](https://github.com/chenluda/get-paper-from-openview/assets/45784833/9ae045f8-34b8-4206-860e-ea6f5648cef5)

Github 上也有从该网站爬取会议论文集的项目，如 paper_downloader。但是，这个项目是通过直接请求页面元素并根据布局来查找相关论文信息的。由于不同会议在 OpenReview 上的页面布局各不相同，特别是在不同年份之间，这就导致了一个问题：代码变得极其冗余（因为每个会议在不同的年份都需要有自己独特的爬取代码）。

![image](https://github.com/chenluda/get-paper-from-openview/assets/45784833/28babc96-617e-4989-8f85-d4001d73a7a3)

要知道 OpenReview 是有自己的官方 API 文档的 :)
https://docs.openreview.net/getting-started/using-the-api
https://openreview-py.readthedocs.io/en/latest/
https://github.com/openreview/openreview-py
