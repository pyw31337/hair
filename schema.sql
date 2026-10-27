-- --------------------------------------------------------
-- J.Hair Shop Reservation Database Schema
-- Table: jhair
-- --------------------------------------------------------

CREATE TABLE IF NOT EXISTS `jhair` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50) NOT NULL DEFAULT '',
  `tel` VARCHAR(25) NOT NULL DEFAULT '',
  `style` VARCHAR(100) NOT NULL DEFAULT '',
  `comment` TEXT,
  `reserve_date` VARCHAR(10) NOT NULL DEFAULT '',
  `reserve_time` VARCHAR(10) NOT NULL DEFAULT '',
  `write_date` DATE DEFAULT NULL,
  `write_time` TIME DEFAULT NULL,
  `write_ip` VARCHAR(45) DEFAULT '',
  `trash` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '0: 정상, 1: 삭제(취소)',
  `holiday` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '0: 영업, 1: 매장휴무',
  PRIMARY KEY (`id`),
  INDEX `idx_reserve` (`reserve_date`, `trash`, `holiday`),
  INDEX `idx_trash` (`trash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 공지사항 저장용 초기 레코드 (id = 1)
INSERT INTO `jhair` (`id`, `name`, `tel`, `style`, `comment`, `reserve_date`, `reserve_time`, `trash`, `holiday`)
VALUES (1, '관리자', '0315550628', '공지', '영업시간 12:00 ~ 20:00 (매월 첫째주/셋째주 일요일 휴무)', '2024-01-01', '00:00:00', 0, 0)
ON DUPLICATE KEY UPDATE `id`=`id`;
