# History

---
## 0.8.0
- JSON Schema & Python API:
    - make `FormItem.description` optional
    - Rename `FormItem.confirmation_needed` to `FormItem.skip_confirmation`, which says the opposite and defaults to `false`
    - Add `FormItem.pattern` attribute
    - Add `FormItemType.regex` (used only with not null `FormItem.pattern`)
 - HTML API:
    - Rename `<form>`'s attribute `confirmation-needed` to `skip-confirmation`, which defaults to `false`
    - Support new `<input>` standard attribute: `pattern`
- Bug fixes:
    - `FormItem`s of type "form-menu" were having the options duplicated in description

---
## 0.7.0
- HTML API:
    - Added new `<input>` types: "email", "location", "url".
- Python API:
    - Added new `FormItem` types: "email", "location", "url".
- Added tests
- Bug fixes:
    - input attribute `maxlength_error` was assigned to both
    `FormItem.min_length_error` and `FormItem.max_length_error`

---
## 0.6.0
- Decreased the minimum Python version to 3.6.

- HTML API:
  - Added a bunch of new attributes on `<input>`: `min`, `min_error`,
  `minlength`, `minlength_error`, `max`, `max_error`, `maxlength`,
  `maxlength_error`, `step`, `value`
  - Added a bunch of new attributes on `<section>`: `chunking_footer`,
  `confirmation_label`, `method`, `required`, `status_exclude`,
  `status_prepend`, `url`, `validate_type_error`, `validate_type_error_footer`,
  `validate_url`
  - Added new input types: `number`, `hidden`
  - Added `text-search` attribute on `<li>`

- Python API
  - Removed `FormItemMenu` and `FormItemContent`. Use a single model instead -
  `FormItem` which achieves the functionality of both old models
  - A bunch of new properties were added on `FormItem`, taken from `<input>`
  and `<section>` tags (see changes in HTML API above).
  - Added `text_search` property on `MenuItemFormItem`

- Fixes:
  - Fix some bad tests
---
## 0.5.0
- HTML API:
  - Added `auto-select`, `multi-select` and `numbered` flags on `<section>` 
  tag. They take effect only if the `<section>` tag contains options
  - Boolean attributes are evaluated according to HTML5 (if present, a boolean
  attribute is true; if absent, it's false)

- Python API:
  - Added `MenuMeta` and `FormItemMenuMeta` objects to describe `Menu` objects 
  and `FormItemMenu` objects respectively.
    - `MenuMeta` can contain `auto_select`
    - `FormItemMenuMeta` can contain `auto_select`, `multi_select` and `numbered`
    - these attributes have origin in `<section>` tag
---
