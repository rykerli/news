# 2019.9.15
新浪、搜狐、天涯各导出500个语篇(字数在20以上)，统计态度词表(积极、消极词)在各语篇出现的个数并降序排列   
# 2019.9.18
扩充否定词表(字数限到50到1000,100以上可以的话就做100)
```sql
# 下面是搜狐数据
select count(*)
from sj_sohu
where CHAR_LENGTH(article_content) > 50;
# 144523

select count(*)
from bzy_sohu_article
where CHAR_LENGTH(content) > 50;
# 22173
# 天涯数据
select count(*)
from sj_tianya_article
where CHAR_LENGTH(question_detail) > 50;
# 71022
# sina数据
select count(*)
from sj_sina_article
where CHAR_LENGTH(post_content_txt) > 50;
# 51490
```

```sql
# 下面是搜狐数据
select count(*)
from sj_sohu
where CHAR_LENGTH(article_content) > 100;
# 144523

select count(*)
from bzy_sohu_article
where CHAR_LENGTH(content) > 100;
# 21676
# 天涯数据
select count(*)
from sj_tianya_article
where CHAR_LENGTH(question_detail) > 100;
# 47812
# sina数据
select count(*)
from sj_sina_article
where CHAR_LENGTH(post_content_txt) > 100;
# 24223
```