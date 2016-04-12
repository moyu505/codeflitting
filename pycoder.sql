DROP TABLE IF EXISTS `pycoder_category`;
CREATE TABLE IF NOT EXISTS `pycoder_category` (
  `id` SMALLINT(6) UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL DEFAULT '',
  `num` MEDIUMINT(8) UNSIGNED NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

DROP TABLE IF EXISTS `pycoder_tag`;
CREATE TABLE IF NOT EXISTS `pycoder_tag` (
  `id` SMALLINT(6) UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL DEFAULT '',
  `num` MEDIUMINT(8) UNSIGNED NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

DROP TABLE IF EXISTS `pycoder_post`;
CREATE TABLE IF NOT EXISTS `pycoder_post` (
  `id` MEDIUMINT(8) UNSIGNED NOT NULL AUTO_INCREMENT,
  `views` INT(10) UNSIGNED NOT NULL DEFAULT '1',
  `title` VARCHAR(100) NOT NULL DEFAULT '',
  `markdown` MEDIUMTEXT NOT NULL,
  `html` MEDIUMTEXT NOT NULL,
  `tags` VARCHAR(100) NOT NULL,
  `category` VARCHAR(100) NOT NULL,
  `edit_time` INT(10) UNSIGNED NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

DROP TABLE IF EXISTS `pycoder_subscribe`;
CREATE TABLE IF NOT EXISTS `pycoder_subscribe`(
    `id` SMALLINT(6) UNSIGNED NOT NULL AUTO_INCREMENT,
    `email` VARCHAR (100) NOT NULL DEFAULT '',
    PRIMARY KEY (`id`)
)ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;
