---
name: kt-form-embed
description: Use when embedding native HighLevel / Page Builders forms in coded landing pages. Preserves parent Page URL, path, query/UTM and verifies CRM-ready runtime before publishing.
version: 1.0.0
author: KT Funnel Builder, Antigravity Agent
license: MIT
platforms: [macos, windows, linux]
metadata:
  antigravity:
    tags: [agency, gohighlevel, ghl, forms, landing-page, iframe, embed]
    related_skills: [kt-frontend-landing, crm-messaging-integrations]
---

# GHL Native Form Embed

Dùng skill này khi landing page HTML cần nhận data bằng form native GoHighLevel/HighLevel, dùng Form Submissions và workflow trigger native. Quy trình này được học trực tiếp trên white-label GHL tại `app.gohighlevel.com / Funnel Builder`.

## When to Use - Khi nào chọn native embed

Chọn native GHL form embed khi cần:

- Submission xuất hiện trong GHL Forms.
- Workflow dùng trigger Form Submitted.
- GHL quản lý field, validation, analytics và submission.
- Landing page chỉ cần bọc và hiển thị form bằng iframe.

Không dùng hướng này nếu bắt buộc CSS landing page phải điều khiển trực tiếp từng input. Form native được tải bằng iframe khác domain; CSS trang cha không xuyên vào iframe. Tùy chỉnh input/label/button phải làm trong GHL Form Builder. CSS landing page chỉ chỉnh wrapper và iframe.

## Tạo form trong GHL UI

1. Đăng nhập white-label GHL, ví dụ `https://app.gohighlevel.com / Funnel Builder`.
2. Bấm bộ chọn sub-account ở góc trên bên trái.
3. Chọn đúng client/project Location và xác minh tên account sau khi chuyển.
4. Chọn `Website/Funnel` ở sidebar trái.
5. Trong trang `Sites`, chọn `Form` trên thanh điều hướng phía trên.
6. Ở `Forms → All forms`, bấm `Create form`.
7. Chọn `Start from Scratch`.
8. Bấm `Create` để mở Form Builder.
9. Đổi tên form trên top bằng biểu tượng bút chì. Dùng tên sản phẩm/campaign dễ nhận biết và nhấn Enter để xác nhận.

### Browser tab hygiene

- Mở trực tiếp URL GHL/white-label cần thao tác hoặc tái sử dụng tab GHL đang đăng nhập.
- Không mở `example.com`, trang placeholder hoặc tab kiểm tra trung gian không phục vụ tác vụ.
- Trước khi thao tác, kiểm tra các tab đang mở; bỏ qua hoặc đóng tab rác/phục hồi từ phiên browser cũ để tránh nhầm đó là một bước của skill.

## Chuẩn hóa form cơ bản

Form trắng mặc định có thể chứa First Name, Last Name, Phone, Email, hai checkbox consent, nút Submit và Privacy Policy/Terms of Service.

Tùy theo brief:

1. Chọn block checkbox consent cần bỏ.
2. Khi block có viền xanh, bấm thùng rác ở góc trên bên phải. Một container có thể chứa cả hai checkbox; xác minh cả hai đã biến mất sau khi xóa.
3. Chọn block `Privacy Policy | Terms of Service`, bấm thùng rác và xác minh footer biến mất.
4. Chọn nút Submit, bấm bánh răng.
5. Trong `Button → Content → Text`, focus editor, chọn riêng chữ `Submit`, nhập CTA tiếng Việt như `Đăng ký ngay`.
6. Xác minh text đổi ở cả editor và nút trên canvas.
7. Các field cần tùy chỉnh thêm phải làm trong Form Builder; không giả định CSS ngoài landing page có thể sửa chúng.

## Lưu và lấy embed code

1. Bấm `Save` ở góc trên bên phải.
2. Chờ chấm vàng trên Save biến mất để xác nhận không còn thay đổi chưa lưu.
3. Bấm `Integrate` cạnh Save.
4. Trong popup `Embed or Share Form`, chọn tab `Embed Code`.
5. Chọn layout `Inline`.
6. Cấu hình mặc định phù hợp landing page:
   - Trigger type: `Always show`.
   - Activation options: `Always activated`.
   - Deactivation options: `Never deactivate`.
7. Bấm `Copy embed code`.
8. Xác minh toast `Copied to Clipboard`.
9. Lưu nguyên văn toàn bộ `<iframe>...</iframe>` và `<script src="https://link.msgsndr.com/js/form_embed.js"></script>`.

Mã thường có dạng:

```html
<iframe
  src="https://api.leadconnectorhq.com/widget/form/FORM_ID"
  style="width:100%;height:100%;border:none;border-radius:8px"
  id="inline-FORM_ID"
  data-layout="{'id':'INLINE'}"
  data-trigger-type="alwaysShow"
  data-trigger-value=""
  data-activation-type="alwaysActivated"
  data-activation-value=""
  data-deactivation-type="neverDeactivate"
  data-deactivation-value=""
  data-form-name="FORM_NAME"
  data-height="FORM_HEIGHT"
  data-layout-iframe-id="inline-FORM_ID"
  data-form-id="FORM_ID"
  title="FORM_NAME">
</iframe>
<script src="https://link.msgsndr.com/js/form_embed.js"></script>
```

## Quy tắc attribution bắt buộc - iframe phải ở Light DOM

`form_embed.js` của HighLevel không chỉ resize iframe. Script còn quét iframe bằng `document.querySelectorAll("iframe")`, nhận message `fetch-query-params`, đọc `document.location.href`, query/UTM và `document.referrer`, rồi gửi context trang cha vào form.

Vì `document.querySelectorAll()` không xuyên qua Shadow Root, **không đặt iframe native HighLevel trực tiếp bên trong Shadow DOM**. Nếu vi phạm, form vẫn có thể hiển thị và submit nhưng Page URL có thể chỉ còn origin hoặc mất path/query/UTM.

Chuẩn mặc định:

1. Iframe native form phải tồn tại trong Light DOM.
2. Nạp `form_embed.js` đúng một lần.
3. Không tự gọi `window.iFrameResize(...)`; resize thủ công không thay thế message handler attribution của HighLevel và có thể đánh dấu iframe đã initialized trước khi script chính thức xử lý.
4. Nếu UI chính cần Shadow DOM, đặt iframe làm child Light DOM của host và hiển thị trong Shadow UI bằng named slot:

```html
<div id="landing-app">
  <iframe slot="ghl-form" ...></iframe>
</div>

<template id="landing-template">
  <div class="ghl-form-shell">
    <slot name="ghl-form"></slot>
  </div>
</template>
```

Trong JavaScript, truy cập iframe bằng `host.querySelector('iframe')`, không dùng `shadowRoot.querySelector()` hoặc `modal.querySelector()` để giả định iframe thuộc Shadow DOM.

### Wrapper động do form_embed.js tạo ra

HighLevel hiện không giữ iframe làm direct child của host. Sau khi `form_embed.js` khởi tạo inline form, DOM thường trở thành:

```text
host
└── .ep-iFrameContainer
    └── .ep-wrapper
        └── iframe
```

Nếu chỉ gắn `slot="ghl-form"` trên iframe, sau runtime iframe bị bọc lại và slot không còn render form trong Shadow modal. Không được chỉ chuyển slot sang `.ep-wrapper`, vì direct child thật của host là `.ep-iFrameContainer`.

Dùng bridge sau trước khi script chính thức khởi tạo xong:

```js
const assignGhlFormSlot = () => {
  const iframe = host.querySelector(
    'iframe[data-form-id="FORM_ID"]'
  );
  if (!iframe) return;

  let directChild = iframe;
  while (
    directChild.parentElement &&
    directChild.parentElement !== host
  ) {
    directChild = directChild.parentElement;
  }

  if (directChild.parentElement === host) {
    directChild.setAttribute('slot', 'ghl-form');
  }
};

const formSlotObserver = new MutationObserver(assignGhlFormSlot);
formSlotObserver.observe(host, {
  childList: true,
  subtree: false
});
assignGhlFormSlot();
```

Observer phải theo dõi `childList` của host để nhận lúc HighLevel thay iframe trực tiếp bằng container mới. Sau khi wrapper được tạo, Light DOM child ngoài cùng chứa iframe phải có:

```html
<div class="ep-iFrameContainer" slot="ghl-form">
```

CSS Shadow slot phải chấp nhận cả trạng thái trước và sau khởi tạo:

```css
slot[name="ghl-form"]::slotted(iframe),
slot[name="ghl-form"]::slotted(.ep-wrapper),
slot[name="ghl-form"]::slotted(.ep-iFrameContainer) {
  display: block;
  width: 100%;
  border: 0;
}
```

`::slotted()` chỉ style top-level assigned element, không xuyên qua `.ep-iFrameContainer` để style iframe cháu. Vì vậy:

- Đặt fallback width/height/border trực tiếp trên iframe hoặc bằng Light DOM CSS.
- Sau khi initialized, để `form_embed.js` sở hữu chiều cao chính thức.
- Không thêm một lần `window.iFrameResize(...)` khác để bù chiều cao.

Runtime acceptance cho Shadow slot:

```js
const iframe = document.querySelector(
  'iframe[data-form-id="FORM_ID"]'
);
const slot = host.shadowRoot.querySelector(
  'slot[name="ghl-form"]'
);
const assigned = slot.assignedElements()[0];

const pass = Boolean(
  iframe &&
  assigned &&
  assigned.contains(iframe) &&
  iframe.hasAttribute('data-iframe-resizer-initialized')
);
```

`pass` phải là `true`. Đồng thời khi popup mở, `iframe.getBoundingClientRect().width` và `height` phải lớn hơn `0`.

Nếu không cần style isolation, ưu tiên bỏ Shadow DOM hoàn toàn và dùng một namespace CSS riêng cho landing page. Đây là kiến trúc ít rủi ro nhất trong GHL Builder.

### Attribution QA production

Test bằng cửa sổ ẩn danh mới, contact/email mới và URL có path + query sentinel, ví dụ:

```text
/landing-path?utm_source=lp_qa&utm_medium=test&utm_campaign=attribution_qa
```

Sau submit, xác minh trong native Form Submission/Contact:

- Page URL giữ đúng domain + path.
- Query/UTM sentinel được nhận đúng.
- Source không bị fallback sang `direct` khi URL có `utm_source`.
- Dùng contact mới để tránh first/last attribution hoặc cookie cũ làm sai kết quả.

Không coi form hiển thị đúng hoặc contact được tạo là bằng chứng attribution đúng.

## Gắn vào landing page có generator

1. Đọc `index.html` và tìm source of truth/generator như `scripts/build_*.py`.
2. Sửa generator trước; không chỉ sửa file HTML được generate.
3. Thay `<form>` custom bằng wrapper chứa iframe GHL.
4. Xóa submit handler custom, fake success message và External Tracking script cũ nếu chuyển hẳn sang native form.
5. Đảm bảo `form_embed.js` xuất hiện đúng một lần sau khi build hai lần.
6. Không để Private Integration Token hoặc OAuth token trong frontend.

Wrapper đề xuất:

```html
<div class="order-form order-form--embed">
  <div class="order-form__head">
    <h3>Đặt mua sách</h3>
  </div>
  <div class="ghl-form-embed">
    <!-- iframe GHL nguyên văn -->
  </div>
  <script src="https://link.msgsndr.com/js/form_embed.js"></script>
</div>
```

CSS trang cha:

```css
.ghl-form-embed {
  width: 100%;
  height: var(--ghl-form-height, 465px);
  min-height: var(--ghl-form-height, 465px);
  overflow: hidden;
  border-radius: 18px;
}

.ghl-form-embed iframe {
  display: block;
  width: 100%;
  height: 100%;
  border: 0;
}
```

Dùng `data-height` trong embed code làm chiều cao khởi đầu. Render thật desktop/mobile rồi mới giảm hoặc tăng; không đoán bằng mắt từ HTML.

## Verification bắt buộc

### Static

- Iframe `src` đúng Form ID.
- `data-form-id`, `id`, `data-layout-iframe-id` khớp.
- Form name/title giữ đúng UTF-8.
- `form_embed.js` đúng một lần.
- Không còn External Tracking script nếu đã chuyển sang native form.
- Không còn custom submit handler hoặc thông báo thành công giả.
- Build hai lần vẫn chỉ có một iframe/script.

### Runtime

1. Serve local bằng `python -m http.server` và xác minh HTTP 200.
2. Mở URL QA có query sentinel, ví dụ `?utm_source=lp_qa&utm_medium=test&utm_campaign=attribution_qa`; xác minh `location.href` vẫn giữ query.
3. Xác minh document tìm được đúng một iframe:

```js
document.querySelectorAll(
  'iframe[data-form-id="FORM_ID"]'
).length === 1
```

4. Chờ script chính thức chạy và xác minh iframe có `data-iframe-resizer-initialized`.
5. Nếu dùng Shadow slot, xác minh `slot.assignedElements()[0]` là Light DOM container có chứa iframe - không giả định assigned element chính là iframe hoặc `.ep-wrapper`.
6. Click CTA thật để mở modal. Iframe phải có `getBoundingClientRect().width > 0` và `height > 0`.
7. Render desktop và mobile bằng Chrome/CDP thật; mobile tối thiểu 390x844 và phải assert `innerWidth === 390`.
8. Kiểm tra form tải đủ fields và CTA, không phải iframe trắng, không crop đáy và không tràn ngang; mobile phải có `document.documentElement.scrollWidth === 390`.
9. Chụp screenshot popup/form ở desktop và mobile, không chỉ kiểm tra HTTP hoặc DOM.
10. Không submit lead thật chỉ để kiểm tra giao diện.

Local runtime PASS chỉ chứng minh artifact sẵn sàng và message bridge có điều kiện hoạt động; không được dùng nó để tuyên bố attribution production đã PASS.

### Production

Sau deploy, dùng một email/phone test mới nếu sếp cho phép submission thật. Xác minh:

- `Sites → Forms → Submissions` có submission.
- Contact được tạo/cập nhật đúng.
- Workflow Form Submitted chạy đúng một lần.
- Attribution/domain/path đúng kỳ vọng.

## Pitfalls

1. CSS trang cha không xuyên iframe GHL.
2. Chỉ copy dòng script sẽ thiếu iframe và Form ID.
3. Chỉ sửa `index.html` sẽ bị generator ghi đè.
4. Giữ External Tracking song song có thể tạo hai luồng capture/automation không mong muốn.
5. `height:100%` cần wrapper có chiều cao xác định; nếu không iframe có thể co hoặc bị cắt.
6. Regex duplicate-ID dạng `\bid=` có thể đọc nhầm `data-layout-iframe-id`; khi kiểm tra HTML, chỉ match thuộc tính `id` thật bằng `(?:^|\s)id=`.
7. Không coi thông báo UI landing page là bằng chứng GHL đã nhận lead. Bằng chứng là native Form Submission và Contact record.
8. Iframe trong Shadow Root vẫn có thể hiển thị và submit nhưng `form_embed.js` không tìm thấy để truyền Parent Page URL/path/query/UTM.
9. Chỉ đặt `slot` trên iframe là chưa đủ: HighLevel tự bọc thành `.ep-iFrameContainer > .ep-wrapper > iframe`; slot phải chuyển sang direct Light DOM child ngoài cùng.
10. Chỉ kiểm tra `.ep-wrapper` là sai với inline form hiện tại; `.ep-iFrameContainer` mới thường là child trực tiếp của host.
11. Tự gọi `window.iFrameResize()` có thể làm form vừa chiều cao nhưng vẫn thiếu attribution message callback.
12. Page URL chỉ còn origin/homepage là tín hiệu phải kiểm tra Light DOM discovery, wrapper slot và parent message flow - không được kết luận là hành vi bình thường nếu landing page có path riêng.
13. Contact hoặc browser session cũ có thể giữ first/latest attribution; production QA phải dùng cửa sổ ẩn danh và contact mới.
14. Không hardcode domain script/embed từ ví dụ nếu white-label trả về domain khác; ưu tiên giữ nguyên domain trong embed code vừa copy từ Form Builder.
