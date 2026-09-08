LDG SALE PAGE — CẨM NANG PHÁT TRIỂN VẬN ĐỘNG THÔ THÔNG QUA VUI CHƠI
======================================================================

PROJECT FOLDER: /Users/khanhtoan/Projects/ldg-sale-page-phat-trien-van-dong-tho
SOURCE: sale-page-phat-trien-van-dong-tho-v1.md
OBJECTIVE: Landing page HTML/CSS cho cẩm nang PDF 18 trang, giá 29.000₫

INPUTS READ:
- sale-page-phat-trien-van-dong-tho-v1.md (bản nháp cẩm nang + brief sale page)
- ldg-landing-page-frontend/SKILL.md (chuẩn implement)
- references/*.md (responsive QA, token convention, encoding, visual QA)

OUTPUTS:
- index.html (trang chủ sale page — full 13 section)
- style.css (design tokens + responsive rules)

STATUS:
- Chưa render. Chưa xác nhận với người bán về: quà tặng, cam kết, feedback,
  phương thức thanh toán, platform, thời hạn ưu đãi, thông tin Khánh Toàn,
  ảnh sản phẩm/mockup.

ASSUMPTIONS (placeholder — sẽ hỏi người bán):
- Charset UTF-8, viewport <meta> có.
- Màu primary: cam/sáng (theo brief hero), cools background cream/trắng.
- Font body: system stack; headline: hệ thống tương tự hoặc Google Font nếu
  người bán approval.
- Chưa có ảnh thật: dùng placeholder neutral (SVG abstract / icon) cho hero,
  instructor, product mockup. Không bịa nội dung feedback hay cam kết.
- FAQ giữ lại vì brief có sẵn.
- CTA chính: "Tải cẩm nang ngay — 29.000₫", CTA phụ: "Xem thử 3 hoạt động
  đầu tiên (miễn phí)".
- Section 9 (quà tặng), 11 (cam kết), 12 (feedback) giữ placeholder rõ ràng
  theo brief, không tự bịa giá trị quy đổi hay review.

NEXT ACTION:
- Xây dựng file HTML/CSS sau — nếu dùng Claude Code / terminal / Hermes Agent,
  bắt đầu từ folder Project.
- Sau khi có file, mở browser / Preview Pane, chụp desktop + mobile,
  kiểm tra overflow và Vietnamese encoding, báo kết quả.
