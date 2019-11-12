### database
CREATE TABLE `yqc_shenzhen` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL comment '标题',
  `url` varchar(255) DEFAULT NULL COMMENT '标题',
  `pub_time` datetime DEFAULT NULL COMMENT '发布时间',
  `pub_org` varchar(50) DEFAULT NULL COMMENT '发布机构',
  `doc_id` varchar(100) DEFAULT NULL COMMENT '文号',
  `index_id` varchar(100) DEFAULT NULL COMMENT '索引号',
  `key_cnt` int(11) DEFAULT '0' COMMENT '关键字匹配数',
  `cont` longtext COMMENT '内容',
  KEY `index_id` (`id`),
  KEY `index_title` (`title`),
  KEY `index_pub_org` (`pub_org`),
  KEY `index_pub_time` (`pub_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='james__yqc_shenzhen爬虫数据';

### cmd