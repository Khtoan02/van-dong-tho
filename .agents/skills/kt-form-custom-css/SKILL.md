---
name: kt-form-custom-css
description: Use when custom-styling an embedded KT Funnel Builder form.
version: 1.0.0
author: KT Funnel Builder, Antigravity Agent
license: MIT
platforms: [macos, windows, linux]
metadata:
  antigravity:
    tags: [agency, leandigi, gohighlevel, forms, css, iframe, landing-page]
    related_skills: [kt-form-embed, kt-frontend-landing]
---

# KT Funnel Builder Custom CSS Form

Dùng skill này khi cần custom giao diện bên trong native form trên nền tảng KT Funnel Builder đang được embed bằng iframe, nhưng muốn giảm thao tác trong Form Builder xuống còn một lần dán Custom CSS.

## When to Use

Tải skill này khi:

- Native form trong iframe không đồng bộ với thiết kế landing page.
- Cần custom input, label, placeholder, CTA, validation hoặc responsive bên trong iframe.
- Muốn dựng và duyệt giao diện local trước khi dán Custom CSS vào Form Builder.
- Cần xử lý rule nền tảng có specificity cao hoặc inline style.

Không dùng skill này để thay đổi field mapping, workflow, submission logic hoặc chuyển native form thành custom HTML production.

## Nguyên tắc

- CSS landing page không xuyên qua iframe khác domain.
- Không thay native form bằng HTML custom nếu cần giữ Form Submission, validation và workflow native.
- Dùng public widget URL để đọc DOM thật: `https://api.leadconnectorhq.com/widget/form/FORM_ID`.
- Dựng HTML lab local để thiết kế và duyệt trước.
- Bộ CSS cuối phải dùng selector thật và được inject thử vào DOM public trước khi dán trong Form Builder.
- Không submit lead thật khi chỉ QA giao diện.

## Workflow

### 1. Xác định form

1. Đọc embed code trong landing page hoặc generator.
2. Ghi lại `FORM_ID`, `data-form-name`, `data-height` và iframe URL.
3. Nếu landing page có generator, giữ generator là source of truth.
4. Mở public widget URL trực tiếp để kiểm tra form thật.

### 2. Trích xuất DOM và selector

Dùng browser/CDP lấy:

- Field `id`, `name`, `type`, class và placeholder.
- Label class và thuộc tính `for`.
- Button class và các node con chứa text.
- Chuỗi ancestor đến root form.
- Inline style, style rule và computed style thật.

Root ổn định thường gặp:

```css
#_builder-form
```

Class thường gặp:

```css
.form-builder--wrap
.form-builder--item
.form-control
.form-field-wrapper
.field-container
.fields-container
.form-side
.button-element
.button-content
.button-text
.input-icon
```

Không dùng class hash/ngẫu nhiên hoặc thuộc tính Vue `data-v-*` làm selector chính.

### 3. Tạo HTML style lab

Tạo trong project:

```text
form-style-lab.html
leandigi-custom-form.css
```

HTML lab phải:

- Mô phỏng đúng field, ID và class quan trọng của DOM thật.
- Đặt form trong wrapper/card thật của landing page.
- Không có submit handler và không gửi dữ liệu.
- Load chính file CSS cuối.
- QA desktop và mobile `390x844`.

Không thay iframe production bằng mock HTML. Lab chỉ dùng cho thiết kế và QA.

### 4. Viết CSS có scope

Scope vào root ổn định:

```css
#_builder-form label { ... }
#_builder-form input.form-control { ... }
#_builder-form .button-element { ... }
```

Xử lý nền trong suốt, font, label, placeholder, input, hover/focus, icon, validation, CTA và các node con chứa text. Mobile dùng input tối thiểu `16px`, target cao khoảng `50-54px`.

### 5. Xử lý specificity

Rule mặc định có thể rất cụ thể và dùng `!important`, ví dụ:

```css
#_builder-form .form-builder--item input[type=text][class=form-control] {
  ... !important;
}
```

Nếu CSS mới không thắng, tăng specificity bằng selector ổn định:

```css
#_builder-form.form-builder--wrap
  .form-builder--item
  input[type="text"].form-control {
  ... !important;
}
```

Nếu riêng field vẫn bị chặn, dùng ID field thật:

```css
#_builder-form input#first_name.form-control,
#_builder-form input#last_name.form-control {
  ... !important;
}
```

Không lạm dụng ID nếu stylesheet cần dùng cho nhiều form.

### 6. Inline `!important` pitfall

Inline `!important` có thể thắng stylesheet Custom CSS, ví dụ padding icon của email. Nếu computed style xác nhận không override được nhưng giá trị vẫn chấp nhận, giữ nguyên. Không báo đã override nếu runtime chưa xác nhận.

Button thường có inline background/radius/padding và text con có inline font/color. Style cả node text:

```css
#_builder-form .button-element,
#_builder-form .button-element .button-text,
#_builder-form .button-element .button-text * {
  ...
}
```

### 7. Inject thử trên form public

1. Mở public widget URL.
2. Inject toàn bộ CSS vào một `<style>` tạm.
3. Đo computed style input/button/root.
4. Chụp desktop và mobile.
5. Xác minh selector áp dụng, không tràn ngang, không crop đáy và CTA nằm trong `data-height`.
6. Nếu CSS không thắng, đọc rule thật và sửa specificity, không đoán.

Injection chỉ tồn tại trong tab và không Save vào Form Builder.

### 8. Một lần dán trong Form Builder

Sau khi người dùng duyệt lab:

1. Mở đúng sub-account và đúng form.
2. Người dùng hướng dẫn vị trí Custom CSS nếu workflow chưa được chứng minh.
3. Dán toàn bộ CSS một lần.
4. Preview trước khi Save nếu có thể.
5. Nếu đúng, Save.
6. Không sửa field, mapping, workflow hoặc submit behavior nếu task chỉ là CSS.

### 9. QA sau Save

- Reload public widget URL để xác nhận CSS được phục vụ thật.
- Reload landing page có iframe.
- Kiểm tra desktop và mobile `390x844`.
- Đo chiều cao nội dung và CTA bottom.
- Nếu cần đổi iframe height, sửa wrapper trong generator rồi build lại.
- Không coi lab hoặc injection tạm là bằng chứng CSS đã được lưu.

## Verification checklist

- [ ] Widget URL đúng Form ID.
- [ ] HTML lab dùng đúng field/class/ID thật.
- [ ] CSS scope vào root ổn định.
- [ ] Computed style xác nhận input và CTA nhận CSS.
- [ ] Không tràn ngang ở 390px.
- [ ] CTA không crop trong iframe height.
- [ ] Không submit lead thật.
- [ ] Dán đúng một lần sau khi duyệt.
- [ ] Reload widget và landing page sau Save.
- [ ] Nếu sửa wrapper, sửa generator trước.

## Pitfalls

1. Preview local đẹp không chứng minh CSS thắng rule thật - luôn inject thử vào DOM public.
2. `!important` không đủ nếu rule mặc định cũng `!important` và specificity cao hơn.
3. Inline `!important` có thể không override được từ Custom CSS.
4. Chỉ style button ngoài có thể không đổi màu chữ ở node con.
5. Không dùng class Vue/hash làm selector lâu dài.
6. Không thay mock HTML vào production rồi tưởng submission vẫn native.
7. HTTP 200 không phải visual QA; phải đo và chụp viewport thật.
8. Không Save trước khi Preview nếu người dùng đang hướng dẫn workflow lần đầu.
