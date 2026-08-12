CREATE DATABASE IF NOT EXISTS classmate CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE classmate;

-- 1. 회원
CREATE TABLE tb_member (
    member_id     BIGINT       NOT NULL AUTO_INCREMENT,
    member_no     VARCHAR(32)  NOT NULL,
    name          VARCHAR(32)  NOT NULL,
    email         VARCHAR(255) NOT NULL,
    phone         VARCHAR(16)  NULL,
    created_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (member_id),
    UNIQUE KEY uix_member_no (member_no),
    UNIQUE KEY uix_email (email)
) COMMENT='회원, 그레인: 사람 1명';

-- 2. 카테고리
CREATE TABLE tb_category (
    category_id        INT         NOT NULL AUTO_INCREMENT,
    code               VARCHAR(16) NOT NULL,
    name               VARCHAR(32) NOT NULL,
    parent_category_id INT         NULL,
    PRIMARY KEY (category_id),
    UNIQUE KEY uix_category_cd (code),
    CONSTRAINT fk_cat_parent FOREIGN KEY (parent_category_id) REFERENCES tb_category(category_id)
) COMMENT='카테고리, 그레인: 분류 1개';

-- 3. 강사
CREATE TABLE tb_instructor (
    member_id   BIGINT       NOT NULL,
    bio         VARCHAR(300) NULL,
    profile_img VARCHAR(300) NULL,
    PRIMARY KEY (member_id),
    CONSTRAINT fk_inst_member FOREIGN KEY (member_id) REFERENCES tb_member(member_id)
) COMMENT='강사, 그레인: 강사 1명';

-- 4. 강의
CREATE TABLE tb_course (
    course_id     INT           NOT NULL AUTO_INCREMENT,
    code          VARCHAR(32)   NOT NULL,
    title         VARCHAR(128)  NOT NULL,
    category_id   INT           NOT NULL,
    instructor_id BIGINT        NOT NULL,
    price         DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (course_id),
    UNIQUE KEY uix_course_cd (code),
    CONSTRAINT fk_course_cat  FOREIGN KEY (category_id)   REFERENCES tb_category(category_id),
    CONSTRAINT fk_course_inst FOREIGN KEY (instructor_id) REFERENCES tb_instructor(member_id)
) COMMENT='강의, 그레인: 강의 1개';

-- 5. 커리큘럼 섹션
CREATE TABLE tb_section (
    section_id  INT          NOT NULL AUTO_INCREMENT,
    course_id   INT          NOT NULL,
    section_no  INT          NOT NULL,
    title       VARCHAR(128) NOT NULL,
    PRIMARY KEY (section_id),
    CONSTRAINT fk_sec_course FOREIGN KEY (course_id) REFERENCES tb_course(course_id)
) COMMENT='섹션, 그레인: 강의 안의 챕터 1개';

-- 6. 레슨
CREATE TABLE tb_lesson (
    lesson_id   INT          NOT NULL AUTO_INCREMENT,
    section_id  INT          NOT NULL,
    lesson_no   INT          NOT NULL,
    title       VARCHAR(128) NOT NULL,
    PRIMARY KEY (lesson_id),
    CONSTRAINT fk_les_sec FOREIGN KEY (section_id) REFERENCES tb_section(section_id)
) COMMENT='레슨, 그레인: 섹션 안의 영상 1개';

-- 7. 태그 
CREATE TABLE tb_tag (
    tag_id INT         NOT NULL AUTO_INCREMENT,
    name   VARCHAR(32) NOT NULL,
    PRIMARY KEY (tag_id),
    UNIQUE KEY uix_tag_nm (name)
) COMMENT='태그, 그레인: 검색용 태그 1개';

-- 8. 강의-태그 연결 
CREATE TABLE tb_course_tag (
    course_id INT NOT NULL,
    tag_id    INT NOT NULL,
    PRIMARY KEY (course_id, tag_id),
    CONSTRAINT fk_ct_course FOREIGN KEY (course_id) REFERENCES tb_course(course_id),
    CONSTRAINT fk_ct_tag    FOREIGN KEY (tag_id)    REFERENCES tb_tag(tag_id)
) COMMENT='강의 태그 연결, 그레인: 강의에 붙은 태그 1개';

-- 9. 결제
CREATE TABLE tb_payment (
    payment_id    INT           NOT NULL AUTO_INCREMENT,
    member_id     BIGINT        NOT NULL,
    paid_at       DATETIME      NOT NULL,
    total_amount  INT           NOT NULL,
    PRIMARY KEY (payment_id),
    CONSTRAINT fk_pay_member FOREIGN KEY (member_id) REFERENCES tb_member(member_id)
) COMMENT='결제, 그레인: 결제 1건';

-- 10. 결제 상세 
CREATE TABLE tb_payment_item (
    payment_item_id INT           NOT NULL AUTO_INCREMENT,
    payment_id      INT           NOT NULL,
    course_id       INT           NOT NULL,
    paid_price      INT           NOT NULL,
    PRIMARY KEY (payment_item_id),
    CONSTRAINT fk_pi_pay    FOREIGN KEY (payment_id) REFERENCES tb_payment(payment_id),
    CONSTRAINT fk_pi_course FOREIGN KEY (course_id)  REFERENCES tb_course(course_id)
) COMMENT='결제 상세, 그레인: 결제 내역 안의 강의 1개';

-- 11. 수강신청 
CREATE TABLE tb_enrollment (
    enrollment_id   INT      NOT NULL AUTO_INCREMENT,
    member_id       BIGINT   NOT NULL,
    course_id       INT      NOT NULL,
    enrolled_at     DATETIME NOT NULL,
    PRIMARY KEY (enrollment_id),
    CONSTRAINT fk_enr_member FOREIGN KEY (member_id) REFERENCES tb_member(member_id),
    CONSTRAINT fk_enr_course FOREIGN KEY (course_id) REFERENCES tb_course(course_id)
) COMMENT='수강신청, 그레인: 회원이 신청한 강의 1개';

-- 12. 리뷰 
CREATE TABLE tb_review (
    review_id  INT      NOT NULL AUTO_INCREMENT,
    member_id  BIGINT   NOT NULL,
    course_id  INT      NOT NULL,
    rating     INT      NOT NULL,
    content    TEXT     NULL,
    created_at DATETIME NOT NULL,
    PRIMARY KEY (review_id),
    CONSTRAINT fk_rev_member FOREIGN KEY (member_id) REFERENCES tb_member(member_id),
    CONSTRAINT fk_rev_course FOREIGN KEY (course_id) REFERENCES tb_course(course_id)
) COMMENT='리뷰, 그레인: 강의에 남긴 리뷰 1건';

-- 13. 문의 
CREATE TABLE tb_inquiry (
    inquiry_id    INT      NOT NULL AUTO_INCREMENT,
    member_id     BIGINT   NOT NULL,
    course_id     INT      NOT NULL,
    lesson_id     INT      NULL,     
    content       TEXT     NOT NULL,
    created_at    DATETIME NOT NULL,
    PRIMARY KEY (inquiry_id),
    CONSTRAINT fk_inq_member FOREIGN KEY (member_id) REFERENCES tb_member(member_id),
    CONSTRAINT fk_inq_course FOREIGN KEY (course_id) REFERENCES tb_course(course_id),
    CONSTRAINT fk_inq_lesson FOREIGN KEY (lesson_id) REFERENCES tb_lesson(lesson_id)
) COMMENT='문의, 그레인: 강의 또는 레슨에 남긴 질문 1건';