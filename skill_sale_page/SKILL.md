---
name: sale-page-phat-trien-van-dong-tho
description: >
  Use when building or iterating the landing page for Khánh Toàn's
  "Cẩm nang phát triển vận động thô thông qua vui chơi" PDF sale page
  (18 trang, 10 hoạt động, 29.000₫). Covers Hero/Guide/USP/Who/Benefits/
  Contents/Instructor/What-you-get/Gifts/Pricing/Guarantee/Social-proof/
  Final CTA + FAQ.
version: 1.0.0
author: KNT
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [frontend, landing-page, html, css, responsive, vietnamese]
    related_skills: [ldg-landing-page-frontend]
---

# Sale Page — Cẩm nang vận động thô cho bé tự kỷ

 landing page HTML/CSS cho sản phẩm PDF 18 trang của Khánh Toàn.

## Trigger
 Use when the user asks to "thiết kế landing page", "xây index", "render sale
 page", or khi bản nháp sale-page-phat-trien-van-dong-tho-v1.md được cập nhật.

## Folder
 Deliverables nằm trong project folder:
 `/Users/khanhtoan/Projects/ldg-sale-page-phat-trien-van-dong-tho/`
 Không dùng thư mục system của Hermes.

## Inputs
 - sale-page-phat-trien-van-dong-tho-v1.md — nguồn copy + brief 13 section.
 - BUILD_NOTES.md — chương trình làm việc, assumption, items cần xác nhận.
 - ldg-landing-page-frontend/SKILL.md — chuẩn implement + responsive QA.
 - references/*.md trong skill — encoding, viewport, visual-QA.

## Process
 1. Tách copy từ brief, giữ nguyên placeholder [CẦN BỔ SUNG] cho tài khoản
    thực tế (quà tặng, cam kết, feedback, platform, thanh toán, Khánh Toàn,
    ảnh_mockup). Không tự bịa.
 2. Viết index.html + style.css theo design tokens (cam/sáng primary,
    cream background, system typography, responsive-first). Có <meta charset>
    và viewport.
 3. Render desktop + mobile (390×844), kiểm tra overflow horizon, encoding
    Vietnamese, CTA kích thước tap, hierarchy 5s đầu.
 4. Báo deliver: output path, verification evidence, assumption, next action.

## Verification gates
 - Files tồn tại trong project folder.
 - HTML parse / CSS braces OK.
 - Desktop render + mobile render có viewport đúng.
 - Không có horizontal overflow thực tế.
 - Tiếng Việt hiển thị đúng (không lỗi encoding).
 - Placeholder section (gift/ guarantee/ feedback) giữ nguyên và rõ.

## Items cần xác nhận từ người bán
 - Giá chính xác (brief dùng 29.000₫ placeholder).
 - Phương thức thanh toán + platform (ZaloPay/MoMo/chuyển khoản/Gumroad...)
 - Quà tặng (section 9).
 - Cam kết/ hoàn tiền (section 11).
 - Feedback thực tế (section 12).
 - Thông tin Khánh Toàn (section 7).
 - Ảnh sản phẩm / mockup PDF (section 6, 8).
 - Thời hạn ưu đãi (section 10).
