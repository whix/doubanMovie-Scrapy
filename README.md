# doubanMovie-Scrapy

Scrapy练习，爬取了豆瓣top250的电影，并存到Mysql 数据库中。
## 内容
- 爬取了电影名字(title)，评分(score)，电影信息(movieInfo)，以及豆瓣上的一句话介绍(quote)
- 如何翻页爬取
- log文件的设置
- Pipeline 类中from_settings 方法的执行逻辑，[StackOverflow 相关内容](http://stackoverflow.com/questions/25063117/how-do-scrapy-from-settings-and-from-crawler-class-methods-work)
- 如何在Pipeline 中连接数据库，执行数据库指令
