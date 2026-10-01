# RSS 0.90 – 0.94 & 2.0 import fixtures

Generated test feeds for the RSS importer. Each version has its own folder; `common/` holds version-agnostic cases.

Categories: **valid** (should import), **invalid** (well-formed XML, wrong structure/data), **corrupted** (not well-formed / bad bytes), **security** (XXE, entity bombs — must never be expanded or fetched).

`Expected` is the suggested behaviour; where it says "or", pick one and assert it.


## common

| File | Category | Expected | Notes |
|---|---|---|---|
| `html_error_page.xml` | invalid | reject: unsupported format | Server returned HTML |
| `unsupported_rss_0.89.xml` | invalid | reject: unsupported version | Version just below supported range |
| `unsupported_rss_0.95.xml` | invalid | reject: unsupported version | Between 0.94 and 2.0, not supported |
| `unsupported_rss_1.0.xml` | invalid | reject: unsupported version (RSS 1.0 / RDF) | Unless 1.0 is supported |
| `unsupported_rss_2.1.xml` | invalid | reject: unsupported version | Just above 2.0 |
| `unsupported_rss_3.0.xml` | invalid | reject: unsupported version |  |
| `declaration_only.xml` | corrupted | reject: no root element |  |
| `empty_file.xml` | corrupted | reject: empty body | 0 bytes |
| `plain_text.xml` | corrupted | reject: not XML |  |
| `random_binary.xml` | corrupted | reject: not XML | 512 bytes of binary |
| `whitespace_only.xml` | corrupted | reject: empty body |  |

## rss_0.90

| File | Category | Expected | Notes |
|---|---|---|---|
| `valid_20_items.xml` | valid | import 20 items (spec caps at 15; decide truncate vs accept) | Above the 15-item limit of 0.90/0.91 |
| `valid_cdata.xml` | valid | import 1 item, CDATA text preserved | Title/description in CDATA |
| `valid_comments_and_pi.xml` | valid | import 3 items | XML comments + processing instruction |
| `valid_duplicate_items.xml` | valid | import 2 unique items (dedupe) | Same item repeated twice |
| `valid_empty_no_items.xml` | valid | import 0 items, no error | Valid channel with zero items |
| `valid_full.xml` | valid | import 3 items | All channel + item elements the version supports |
| `valid_iso_8859_1.xml` | valid | import 3 items, accents decoded | Real Latin-1 bytes, declared ISO-8859-1 |
| `valid_minimal.xml` | valid | import 1 item | Only the required elements |
| `valid_no_xml_declaration.xml` | valid | import 3 items | No <?xml ?> prolog |
| `valid_special_characters.xml` | valid | import 1 item, entities decoded | Predefined + numeric entities, accents, CJK, emoji |
| `valid_uppercase_url_scheme_and_query.xml` | valid | import 3 items | Uppercase scheme, query string, fragment |
| `valid_utf8_bom.xml` | valid | import 3 items | UTF-8 byte-order mark |
| `valid_whitespace_padded.xml` | valid | import 3 items, values trimmed | Leading/trailing whitespace and newlines in values |
| `invalid_channel_bad_url.xml` | invalid | reject or flag channel link |  |
| `invalid_empty_channel_values.xml` | invalid | reject: required values blank | <title></title> etc. |
| `invalid_item_bad_urls.xml` | invalid | skip/flag all 3 items (bad, javascript:, relative) | Invalid, dangerous and relative URLs |
| `invalid_item_empty.xml` | invalid | skip empty item, import 1 |  |
| `invalid_item_missing_link.xml` | invalid | skip bad item, import 1 | link required per item in 0.90/0.91 |
| `invalid_item_missing_title.xml` | invalid | skip bad item, import 1 | title required per item in 0.90/0.91 |
| `invalid_items_inside_channel.xml` | invalid | reject or tolerate (spec: items are siblings of channel) | Items nested inside channel |
| `invalid_missing_channel.xml` | invalid | reject: missing channel |  |
| `invalid_missing_channel_description.xml` | invalid | reject: channel description required |  |
| `invalid_missing_channel_link.xml` | invalid | reject: channel link required |  |
| `invalid_missing_channel_title.xml` | invalid | reject: channel title required |  |
| `invalid_missing_default_namespace.xml` | invalid | reject: unknown/undetectable version | No 0.90 namespace |
| `invalid_multiple_channels.xml` | invalid | reject or use first channel |  |
| `invalid_overlong_values.xml` | invalid | import 1 item, truncated to column limits | 5k title, 100k description |
| `invalid_rss_root_with_090_version.xml` | invalid | reject or treat as 0.90 | <rss version="0.90"> instead of rdf:RDF |
| `invalid_unknown_elements.xml` | invalid | import 3 items, ignore unknown | Extra unknown tags |
| `invalid_whitespace_only_channel_title.xml` | invalid | reject: blank title |  |
| `invalid_wrong_namespace.xml` | invalid | reject or detect as RSS 1.0, not 0.90 | RSS 1.0 namespace on 0.90 structure |
| `corrupted_binary_garbage_in_middle.xml` | corrupted | reject: parse error | Random high bytes injected |
| `corrupted_control_characters.xml` | corrupted | reject: parse error (or strip) | Illegal XML 1.0 chars 0x01 0x0B 0x1F |
| `corrupted_double_declaration.xml` | corrupted | reject: parse error | Two <?xml ?> prologs |
| `corrupted_duplicate_attribute.xml` | corrupted | reject: parse error | Same attribute twice |
| `corrupted_encoding_mismatch.xml` | corrupted | reject or mojibake (latin-1 bytes, declared UTF-8) | Declared UTF-8, bytes are Latin-1 |
| `corrupted_gzip_not_decompressed.xml` | corrupted | reject: parse error (or detect gzip) | Gzip body saved without decompressing |
| `corrupted_improper_nesting.xml` | corrupted | reject: parse error | Overlapping elements |
| `corrupted_invalid_utf8_bytes.xml` | corrupted | reject: encoding error | Invalid UTF-8 sequences |
| `corrupted_json_instead_of_xml.xml` | corrupted | reject: not XML |  |
| `corrupted_mismatched_tags.xml` | corrupted | reject: parse error | <link>...</title> |
| `corrupted_multiple_roots.xml` | corrupted | reject: parse error | Feed concatenated twice |
| `corrupted_null_bytes.xml` | corrupted | reject: parse error | NUL bytes in content |
| `corrupted_tags_with_spaces.xml` | corrupted | reject: parse error | < title> |
| `corrupted_text_after_root.xml` | corrupted | reject: parse error |  |
| `corrupted_truncated_mid_item.xml` | corrupted | reject: parse error (or recover 1 item) | File cut off mid-download |
| `corrupted_truncated_missing_root_close.xml` | corrupted | reject: parse error | Last closing tag missing |
| `corrupted_unclosed_cdata.xml` | corrupted | reject: parse error | CDATA with no ]]> |
| `corrupted_unclosed_comment.xml` | corrupted | reject: parse error |  |
| `corrupted_unclosed_tag.xml` | corrupted | reject: parse error | Missing </title> |
| `corrupted_undefined_entity.xml` | corrupted | reject: parse error (or 0.91 DTD-aware) | HTML entities not defined in XML |
| `corrupted_unescaped_ampersand.xml` | corrupted | reject: parse error | Raw & in text |
| `corrupted_unescaped_less_than.xml` | corrupted | reject: parse error | Raw < in text |
| `corrupted_unknown_encoding.xml` | corrupted | reject: unsupported encoding |  |
| `corrupted_unquoted_attribute.xml` | corrupted | reject: parse error | Attribute value without quotes |
| `corrupted_utf16_declared_utf8.xml` | corrupted | reject or detect UTF-16 via BOM | UTF-16 bytes, declaration says UTF-8 |
| `corrupted_whitespace_before_declaration.xml` | corrupted | reject: parse error | XML decl not at byte 0 |
| `security_billion_laughs.xml` | security | reject quickly; MUST NOT expand (~3GB) | Entity expansion bomb |
| `security_deep_nesting.xml` | security | reject or handle without stack overflow | 5000 nested elements |
| `security_external_dtd.xml` | security | parse without fetching DTD | Remote DTD fetch |
| `security_xxe_file.xml` | security | reject or leave entity unexpanded; MUST NOT read /etc/passwd | XXE local file |
| `security_xxe_ssrf.xml` | security | MUST NOT make HTTP request | XXE SSRF to AWS metadata |

## rss_0.91

| File | Category | Expected | Notes |
|---|---|---|---|
| `valid_20_items.xml` | valid | import 20 items (spec caps at 15; decide truncate vs accept) | Above the 15-item limit of 0.90/0.91 |
| `valid_cdata.xml` | valid | import 1 item, CDATA text preserved | Title/description in CDATA |
| `valid_comments_and_pi.xml` | valid | import 3 items | XML comments + processing instruction |
| `valid_duplicate_items.xml` | valid | import 2 unique items (dedupe) | Same item repeated twice |
| `valid_empty_no_items.xml` | valid | import 0 items, no error | Valid channel with zero items |
| `valid_full.xml` | valid | import 3 items | All channel + item elements the version supports |
| `valid_html_in_description.xml` | valid | import 1 item, HTML sanitised (script stripped) | Entity-encoded HTML incl. <script> |
| `valid_iso_8859_1.xml` | valid | import 3 items, accents decoded | Real Latin-1 bytes, declared ISO-8859-1 |
| `valid_minimal.xml` | valid | import 1 item | Only the required elements |
| `valid_no_xml_declaration.xml` | valid | import 3 items | No <?xml ?> prolog |
| `valid_single_item.xml` | valid | import 1 item |  |
| `valid_skiphours_skipdays_textinput.xml` | valid | import 3 items | rating, skipHours, skipDays, textinput |
| `valid_special_characters.xml` | valid | import 1 item, entities decoded | Predefined + numeric entities, accents, CJK, emoji |
| `valid_uppercase_url_scheme_and_query.xml` | valid | import 3 items | Uppercase scheme, query string, fragment |
| `valid_utf8_bom.xml` | valid | import 3 items | UTF-8 byte-order mark |
| `valid_whitespace_padded.xml` | valid | import 3 items, values trimmed | Leading/trailing whitespace and newlines in values |
| `valid_with_netscape_doctype.xml` | valid | import 3 items (must NOT fetch the DTD) | Netscape DOCTYPE, common in real 0.91 feeds |
| `invalid_channel_bad_url.xml` | invalid | reject or flag channel link |  |
| `invalid_empty_channel_values.xml` | invalid | reject: required values blank | <title></title> etc. |
| `invalid_empty_version_attribute.xml` | invalid | reject: unknown version |  |
| `invalid_item_bad_urls.xml` | invalid | skip/flag all 3 items (bad, javascript:, relative) | Invalid, dangerous and relative URLs |
| `invalid_item_empty.xml` | invalid | skip empty item, import 1 |  |
| `invalid_item_missing_link.xml` | invalid | skip bad item, import 1 | link required per item in 0.90/0.91 |
| `invalid_item_missing_title.xml` | invalid | skip bad item, import 1 | title required per item in 0.90/0.91 |
| `invalid_items_outside_channel.xml` | invalid | reject or import 0 items | Items as siblings of channel |
| `invalid_malformed_version.xml` | invalid | reject: unsupported version |  |
| `invalid_missing_channel.xml` | invalid | reject: missing channel |  |
| `invalid_missing_channel_description.xml` | invalid | reject: channel description required |  |
| `invalid_missing_channel_link.xml` | invalid | reject: channel link required |  |
| `invalid_missing_channel_title.xml` | invalid | reject: channel title required |  |
| `invalid_missing_language.xml` | invalid | reject or tolerate (language required in 0.91) |  |
| `invalid_missing_version_attribute.xml` | invalid | reject or default version | <rss> with no version |
| `invalid_multiple_channels.xml` | invalid | reject or use first channel |  |
| `invalid_overlong_values.xml` | invalid | import 1 item, truncated to column limits | 5k title, 100k description |
| `invalid_unknown_elements.xml` | invalid | import 3 items, ignore unknown | Extra unknown tags |
| `invalid_uppercase_root.xml` | invalid | reject (XML is case-sensitive) | <RSS> |
| `invalid_whitespace_only_channel_title.xml` | invalid | reject: blank title |  |
| `invalid_wrong_root_element.xml` | invalid | reject: unsupported format | <feed version=...> |
| `corrupted_binary_garbage_in_middle.xml` | corrupted | reject: parse error | Random high bytes injected |
| `corrupted_control_characters.xml` | corrupted | reject: parse error (or strip) | Illegal XML 1.0 chars 0x01 0x0B 0x1F |
| `corrupted_double_declaration.xml` | corrupted | reject: parse error | Two <?xml ?> prologs |
| `corrupted_duplicate_attribute.xml` | corrupted | reject: parse error | Same attribute twice |
| `corrupted_encoding_mismatch.xml` | corrupted | reject or mojibake (latin-1 bytes, declared UTF-8) | Declared UTF-8, bytes are Latin-1 |
| `corrupted_gzip_not_decompressed.xml` | corrupted | reject: parse error (or detect gzip) | Gzip body saved without decompressing |
| `corrupted_improper_nesting.xml` | corrupted | reject: parse error | Overlapping elements |
| `corrupted_invalid_utf8_bytes.xml` | corrupted | reject: encoding error | Invalid UTF-8 sequences |
| `corrupted_json_instead_of_xml.xml` | corrupted | reject: not XML |  |
| `corrupted_mismatched_tags.xml` | corrupted | reject: parse error | <link>...</title> |
| `corrupted_multiple_roots.xml` | corrupted | reject: parse error | Feed concatenated twice |
| `corrupted_null_bytes.xml` | corrupted | reject: parse error | NUL bytes in content |
| `corrupted_tags_with_spaces.xml` | corrupted | reject: parse error | < title> |
| `corrupted_text_after_root.xml` | corrupted | reject: parse error |  |
| `corrupted_truncated_mid_item.xml` | corrupted | reject: parse error (or recover 1 item) | File cut off mid-download |
| `corrupted_truncated_missing_root_close.xml` | corrupted | reject: parse error | Last closing tag missing |
| `corrupted_unclosed_cdata.xml` | corrupted | reject: parse error | CDATA with no ]]> |
| `corrupted_unclosed_comment.xml` | corrupted | reject: parse error |  |
| `corrupted_unclosed_tag.xml` | corrupted | reject: parse error | Missing </title> |
| `corrupted_undefined_entity.xml` | corrupted | reject: parse error (or 0.91 DTD-aware) | HTML entities not defined in XML |
| `corrupted_unescaped_ampersand.xml` | corrupted | reject: parse error | Raw & in text |
| `corrupted_unescaped_less_than.xml` | corrupted | reject: parse error | Raw < in text |
| `corrupted_unknown_encoding.xml` | corrupted | reject: unsupported encoding |  |
| `corrupted_unquoted_attribute.xml` | corrupted | reject: parse error | Attribute value without quotes |
| `corrupted_utf16_declared_utf8.xml` | corrupted | reject or detect UTF-16 via BOM | UTF-16 bytes, declaration says UTF-8 |
| `corrupted_whitespace_before_declaration.xml` | corrupted | reject: parse error | XML decl not at byte 0 |
| `security_billion_laughs.xml` | security | reject quickly; MUST NOT expand (~3GB) | Entity expansion bomb |
| `security_deep_nesting.xml` | security | reject or handle without stack overflow | 5000 nested elements |
| `security_external_dtd.xml` | security | parse without fetching DTD | Remote DTD fetch |
| `security_xxe_file.xml` | security | reject or leave entity unexpanded; MUST NOT read /etc/passwd | XXE local file |
| `security_xxe_ssrf.xml` | security | MUST NOT make HTTP request | XXE SSRF to AWS metadata |

## rss_0.92

| File | Category | Expected | Notes |
|---|---|---|---|
| `valid_20_items.xml` | valid | import 20 items | Above the 15-item limit of 0.90/0.91 |
| `valid_cdata.xml` | valid | import 1 item, CDATA text preserved | Title/description in CDATA |
| `valid_comments_and_pi.xml` | valid | import 3 items | XML comments + processing instruction |
| `valid_duplicate_items.xml` | valid | import 2 unique items (dedupe) | Same item repeated twice |
| `valid_empty_no_items.xml` | valid | import 0 items, no error | Valid channel with zero items |
| `valid_full.xml` | valid | import 3 items | All channel + item elements the version supports |
| `valid_html_in_description.xml` | valid | import 1 item, HTML sanitised (script stripped) | Entity-encoded HTML incl. <script> |
| `valid_iso_8859_1.xml` | valid | import 3 items, accents decoded | Real Latin-1 bytes, declared ISO-8859-1 |
| `valid_item_description_only.xml` | valid | import 1 item (title derived) or skip per rule | 0.92+ allows item with only description |
| `valid_item_title_only.xml` | valid | import 1 item or skip (no link/identity) | Item with only title |
| `valid_minimal.xml` | valid | import 1 item | Only the required elements |
| `valid_multiple_categories.xml` | valid | import 1 item with 3 categories | Multiple <category> per item |
| `valid_no_xml_declaration.xml` | valid | import 3 items | No <?xml ?> prolog |
| `valid_single_item.xml` | valid | import 1 item |  |
| `valid_special_characters.xml` | valid | import 1 item, entities decoded | Predefined + numeric entities, accents, CJK, emoji |
| `valid_uppercase_url_scheme_and_query.xml` | valid | import 3 items | Uppercase scheme, query string, fragment |
| `valid_utf8_bom.xml` | valid | import 3 items | UTF-8 byte-order mark |
| `valid_whitespace_padded.xml` | valid | import 3 items, values trimmed | Leading/trailing whitespace and newlines in values |
| `invalid_channel_bad_url.xml` | invalid | reject or flag channel link |  |
| `invalid_empty_channel_values.xml` | invalid | reject: required values blank | <title></title> etc. |
| `invalid_empty_version_attribute.xml` | invalid | reject: unknown version |  |
| `invalid_enclosure_bad_length.xml` | invalid | import item, ignore/zero length |  |
| `invalid_enclosure_missing_attributes.xml` | invalid | import item, ignore bad enclosure | enclosure without length/type |
| `invalid_item_bad_urls.xml` | invalid | skip/flag all 3 items (bad, javascript:, relative) | Invalid, dangerous and relative URLs |
| `invalid_item_empty.xml` | invalid | skip empty item, import 1 |  |
| `invalid_item_missing_identity.xml` | invalid | skip item with no link/guid, import 1 | No link and no guid |
| `invalid_item_missing_title_and_description.xml` | invalid | skip bad item, import 1 | 0.92+ needs title or description |
| `invalid_items_outside_channel.xml` | invalid | reject or import 0 items | Items as siblings of channel |
| `invalid_malformed_version.xml` | invalid | reject: unsupported version |  |
| `invalid_missing_channel.xml` | invalid | reject: missing channel |  |
| `invalid_missing_channel_description.xml` | invalid | reject: channel description required |  |
| `invalid_missing_channel_link.xml` | invalid | reject: channel link required |  |
| `invalid_missing_channel_title.xml` | invalid | reject: channel title required |  |
| `invalid_missing_version_attribute.xml` | invalid | reject or default version | <rss> with no version |
| `invalid_multiple_channels.xml` | invalid | reject or use first channel |  |
| `invalid_overlong_values.xml` | invalid | import 1 item, truncated to column limits | 5k title, 100k description |
| `invalid_unknown_elements.xml` | invalid | import 3 items, ignore unknown | Extra unknown tags |
| `invalid_uppercase_root.xml` | invalid | reject (XML is case-sensitive) | <RSS> |
| `invalid_whitespace_only_channel_title.xml` | invalid | reject: blank title |  |
| `invalid_wrong_root_element.xml` | invalid | reject: unsupported format | <feed version=...> |
| `corrupted_binary_garbage_in_middle.xml` | corrupted | reject: parse error | Random high bytes injected |
| `corrupted_control_characters.xml` | corrupted | reject: parse error (or strip) | Illegal XML 1.0 chars 0x01 0x0B 0x1F |
| `corrupted_double_declaration.xml` | corrupted | reject: parse error | Two <?xml ?> prologs |
| `corrupted_duplicate_attribute.xml` | corrupted | reject: parse error | Same attribute twice |
| `corrupted_encoding_mismatch.xml` | corrupted | reject or mojibake (latin-1 bytes, declared UTF-8) | Declared UTF-8, bytes are Latin-1 |
| `corrupted_gzip_not_decompressed.xml` | corrupted | reject: parse error (or detect gzip) | Gzip body saved without decompressing |
| `corrupted_improper_nesting.xml` | corrupted | reject: parse error | Overlapping elements |
| `corrupted_invalid_utf8_bytes.xml` | corrupted | reject: encoding error | Invalid UTF-8 sequences |
| `corrupted_json_instead_of_xml.xml` | corrupted | reject: not XML |  |
| `corrupted_mismatched_tags.xml` | corrupted | reject: parse error | <link>...</title> |
| `corrupted_multiple_roots.xml` | corrupted | reject: parse error | Feed concatenated twice |
| `corrupted_null_bytes.xml` | corrupted | reject: parse error | NUL bytes in content |
| `corrupted_tags_with_spaces.xml` | corrupted | reject: parse error | < title> |
| `corrupted_text_after_root.xml` | corrupted | reject: parse error |  |
| `corrupted_truncated_mid_item.xml` | corrupted | reject: parse error (or recover 1 item) | File cut off mid-download |
| `corrupted_truncated_missing_root_close.xml` | corrupted | reject: parse error | Last closing tag missing |
| `corrupted_unclosed_cdata.xml` | corrupted | reject: parse error | CDATA with no ]]> |
| `corrupted_unclosed_comment.xml` | corrupted | reject: parse error |  |
| `corrupted_unclosed_tag.xml` | corrupted | reject: parse error | Missing </title> |
| `corrupted_undefined_entity.xml` | corrupted | reject: parse error (or 0.91 DTD-aware) | HTML entities not defined in XML |
| `corrupted_unescaped_ampersand.xml` | corrupted | reject: parse error | Raw & in text |
| `corrupted_unescaped_less_than.xml` | corrupted | reject: parse error | Raw < in text |
| `corrupted_unknown_encoding.xml` | corrupted | reject: unsupported encoding |  |
| `corrupted_unquoted_attribute.xml` | corrupted | reject: parse error | Attribute value without quotes |
| `corrupted_utf16_declared_utf8.xml` | corrupted | reject or detect UTF-16 via BOM | UTF-16 bytes, declaration says UTF-8 |
| `corrupted_whitespace_before_declaration.xml` | corrupted | reject: parse error | XML decl not at byte 0 |
| `security_billion_laughs.xml` | security | reject quickly; MUST NOT expand (~3GB) | Entity expansion bomb |
| `security_deep_nesting.xml` | security | reject or handle without stack overflow | 5000 nested elements |
| `security_external_dtd.xml` | security | parse without fetching DTD | Remote DTD fetch |
| `security_xxe_file.xml` | security | reject or leave entity unexpanded; MUST NOT read /etc/passwd | XXE local file |
| `security_xxe_ssrf.xml` | security | MUST NOT make HTTP request | XXE SSRF to AWS metadata |

## rss_0.93

| File | Category | Expected | Notes |
|---|---|---|---|
| `valid_20_items.xml` | valid | import 20 items | Above the 15-item limit of 0.90/0.91 |
| `valid_cdata.xml` | valid | import 1 item, CDATA text preserved | Title/description in CDATA |
| `valid_comments_and_pi.xml` | valid | import 3 items | XML comments + processing instruction |
| `valid_duplicate_items.xml` | valid | import 2 unique items (dedupe) | Same item repeated twice |
| `valid_empty_no_items.xml` | valid | import 0 items, no error | Valid channel with zero items |
| `valid_expired_item.xml` | valid | import 1 item (expired one skipped) or 2 | Item whose expirationDate is in the past |
| `valid_full.xml` | valid | import 3 items | All channel + item elements the version supports |
| `valid_html_in_description.xml` | valid | import 1 item, HTML sanitised (script stripped) | Entity-encoded HTML incl. <script> |
| `valid_iso_8859_1.xml` | valid | import 3 items, accents decoded | Real Latin-1 bytes, declared ISO-8859-1 |
| `valid_item_description_only.xml` | valid | import 1 item (title derived) or skip per rule | 0.92+ allows item with only description |
| `valid_item_title_only.xml` | valid | import 1 item or skip (no link/identity) | Item with only title |
| `valid_minimal.xml` | valid | import 1 item | Only the required elements |
| `valid_multiple_categories.xml` | valid | import 1 item with 3 categories | Multiple <category> per item |
| `valid_no_xml_declaration.xml` | valid | import 3 items | No <?xml ?> prolog |
| `valid_single_item.xml` | valid | import 1 item |  |
| `valid_special_characters.xml` | valid | import 1 item, entities decoded | Predefined + numeric entities, accents, CJK, emoji |
| `valid_uppercase_url_scheme_and_query.xml` | valid | import 3 items | Uppercase scheme, query string, fragment |
| `valid_utf8_bom.xml` | valid | import 3 items | UTF-8 byte-order mark |
| `valid_whitespace_padded.xml` | valid | import 3 items, values trimmed | Leading/trailing whitespace and newlines in values |
| `invalid_channel_bad_url.xml` | invalid | reject or flag channel link |  |
| `invalid_empty_channel_values.xml` | invalid | reject: required values blank | <title></title> etc. |
| `invalid_empty_version_attribute.xml` | invalid | reject: unknown version |  |
| `invalid_enclosure_bad_length.xml` | invalid | import item, ignore/zero length |  |
| `invalid_enclosure_missing_attributes.xml` | invalid | import item, ignore bad enclosure | enclosure without length/type |
| `invalid_future_date.xml` | invalid | import 1 item, date kept or clamped | pubDate year 2100 |
| `invalid_item_bad_dates.xml` | invalid | import 3 items, dates null/fallback (no crash) | Unparseable / empty pubDate |
| `invalid_item_bad_urls.xml` | invalid | skip/flag all 3 items (bad, javascript:, relative) | Invalid, dangerous and relative URLs |
| `invalid_item_empty.xml` | invalid | skip empty item, import 1 |  |
| `invalid_item_missing_identity.xml` | invalid | skip item with no link/guid, import 1 | No link and no guid |
| `invalid_item_missing_title_and_description.xml` | invalid | skip bad item, import 1 | 0.92+ needs title or description |
| `invalid_items_outside_channel.xml` | invalid | reject or import 0 items | Items as siblings of channel |
| `invalid_malformed_version.xml` | invalid | reject: unsupported version |  |
| `invalid_missing_channel.xml` | invalid | reject: missing channel |  |
| `invalid_missing_channel_description.xml` | invalid | reject: channel description required |  |
| `invalid_missing_channel_link.xml` | invalid | reject: channel link required |  |
| `invalid_missing_channel_title.xml` | invalid | reject: channel title required |  |
| `invalid_missing_version_attribute.xml` | invalid | reject or default version | <rss> with no version |
| `invalid_multiple_channels.xml` | invalid | reject or use first channel |  |
| `invalid_overlong_values.xml` | invalid | import 1 item, truncated to column limits | 5k title, 100k description |
| `invalid_unknown_elements.xml` | invalid | import 3 items, ignore unknown | Extra unknown tags |
| `invalid_uppercase_root.xml` | invalid | reject (XML is case-sensitive) | <RSS> |
| `invalid_whitespace_only_channel_title.xml` | invalid | reject: blank title |  |
| `invalid_wrong_root_element.xml` | invalid | reject: unsupported format | <feed version=...> |
| `corrupted_binary_garbage_in_middle.xml` | corrupted | reject: parse error | Random high bytes injected |
| `corrupted_control_characters.xml` | corrupted | reject: parse error (or strip) | Illegal XML 1.0 chars 0x01 0x0B 0x1F |
| `corrupted_double_declaration.xml` | corrupted | reject: parse error | Two <?xml ?> prologs |
| `corrupted_duplicate_attribute.xml` | corrupted | reject: parse error | Same attribute twice |
| `corrupted_encoding_mismatch.xml` | corrupted | reject or mojibake (latin-1 bytes, declared UTF-8) | Declared UTF-8, bytes are Latin-1 |
| `corrupted_gzip_not_decompressed.xml` | corrupted | reject: parse error (or detect gzip) | Gzip body saved without decompressing |
| `corrupted_improper_nesting.xml` | corrupted | reject: parse error | Overlapping elements |
| `corrupted_invalid_utf8_bytes.xml` | corrupted | reject: encoding error | Invalid UTF-8 sequences |
| `corrupted_json_instead_of_xml.xml` | corrupted | reject: not XML |  |
| `corrupted_mismatched_tags.xml` | corrupted | reject: parse error | <link>...</title> |
| `corrupted_multiple_roots.xml` | corrupted | reject: parse error | Feed concatenated twice |
| `corrupted_null_bytes.xml` | corrupted | reject: parse error | NUL bytes in content |
| `corrupted_tags_with_spaces.xml` | corrupted | reject: parse error | < title> |
| `corrupted_text_after_root.xml` | corrupted | reject: parse error |  |
| `corrupted_truncated_mid_item.xml` | corrupted | reject: parse error (or recover 1 item) | File cut off mid-download |
| `corrupted_truncated_missing_root_close.xml` | corrupted | reject: parse error | Last closing tag missing |
| `corrupted_unclosed_cdata.xml` | corrupted | reject: parse error | CDATA with no ]]> |
| `corrupted_unclosed_comment.xml` | corrupted | reject: parse error |  |
| `corrupted_unclosed_tag.xml` | corrupted | reject: parse error | Missing </title> |
| `corrupted_undefined_entity.xml` | corrupted | reject: parse error (or 0.91 DTD-aware) | HTML entities not defined in XML |
| `corrupted_unescaped_ampersand.xml` | corrupted | reject: parse error | Raw & in text |
| `corrupted_unescaped_less_than.xml` | corrupted | reject: parse error | Raw < in text |
| `corrupted_unknown_encoding.xml` | corrupted | reject: unsupported encoding |  |
| `corrupted_unquoted_attribute.xml` | corrupted | reject: parse error | Attribute value without quotes |
| `corrupted_utf16_declared_utf8.xml` | corrupted | reject or detect UTF-16 via BOM | UTF-16 bytes, declaration says UTF-8 |
| `corrupted_whitespace_before_declaration.xml` | corrupted | reject: parse error | XML decl not at byte 0 |
| `security_billion_laughs.xml` | security | reject quickly; MUST NOT expand (~3GB) | Entity expansion bomb |
| `security_deep_nesting.xml` | security | reject or handle without stack overflow | 5000 nested elements |
| `security_external_dtd.xml` | security | parse without fetching DTD | Remote DTD fetch |
| `security_xxe_file.xml` | security | reject or leave entity unexpanded; MUST NOT read /etc/passwd | XXE local file |
| `security_xxe_ssrf.xml` | security | MUST NOT make HTTP request | XXE SSRF to AWS metadata |

## rss_0.94

| File | Category | Expected | Notes |
|---|---|---|---|
| `valid_20_items.xml` | valid | import 20 items | Above the 15-item limit of 0.90/0.91 |
| `valid_cdata.xml` | valid | import 1 item, CDATA text preserved | Title/description in CDATA |
| `valid_comments_and_pi.xml` | valid | import 3 items | XML comments + processing instruction |
| `valid_duplicate_items.xml` | valid | import 2 unique items (dedupe) | Same item repeated twice |
| `valid_empty_no_items.xml` | valid | import 0 items, no error | Valid channel with zero items |
| `valid_expired_item.xml` | valid | import 1 item (expired one skipped) or 2 | Item whose expirationDate is in the past |
| `valid_full.xml` | valid | import 3 items | All channel + item elements the version supports |
| `valid_guid_not_permalink.xml` | valid | import 1 item, guid used as id | guid isPermaLink=false |
| `valid_html_in_description.xml` | valid | import 1 item, HTML sanitised (script stripped) | Entity-encoded HTML incl. <script> |
| `valid_iso_8859_1.xml` | valid | import 3 items, accents decoded | Real Latin-1 bytes, declared ISO-8859-1 |
| `valid_item_description_only.xml` | valid | import 1 item (title derived) or skip per rule | 0.92+ allows item with only description |
| `valid_item_guid_no_link.xml` | valid | import 1 item, identity from guid | No <link>, has <guid> |
| `valid_item_title_only.xml` | valid | import 1 item or skip (no link/identity) | Item with only title |
| `valid_minimal.xml` | valid | import 1 item | Only the required elements |
| `valid_multiple_categories.xml` | valid | import 1 item with 3 categories | Multiple <category> per item |
| `valid_no_xml_declaration.xml` | valid | import 3 items | No <?xml ?> prolog |
| `valid_single_item.xml` | valid | import 1 item |  |
| `valid_special_characters.xml` | valid | import 1 item, entities decoded | Predefined + numeric entities, accents, CJK, emoji |
| `valid_uppercase_url_scheme_and_query.xml` | valid | import 3 items | Uppercase scheme, query string, fragment |
| `valid_utf8_bom.xml` | valid | import 3 items | UTF-8 byte-order mark |
| `valid_whitespace_padded.xml` | valid | import 3 items, values trimmed | Leading/trailing whitespace and newlines in values |
| `invalid_channel_bad_url.xml` | invalid | reject or flag channel link |  |
| `invalid_duplicate_guids.xml` | invalid | import 1 or 2 (guid collision) | Two items share a guid |
| `invalid_empty_channel_values.xml` | invalid | reject: required values blank | <title></title> etc. |
| `invalid_empty_version_attribute.xml` | invalid | reject: unknown version |  |
| `invalid_enclosure_bad_length.xml` | invalid | import item, ignore/zero length |  |
| `invalid_enclosure_missing_attributes.xml` | invalid | import item, ignore bad enclosure | enclosure without length/type |
| `invalid_future_date.xml` | invalid | import 1 item, date kept or clamped | pubDate year 2100 |
| `invalid_item_bad_dates.xml` | invalid | import 3 items, dates null/fallback (no crash) | Unparseable / empty pubDate |
| `invalid_item_bad_urls.xml` | invalid | skip/flag all 3 items (bad, javascript:, relative) | Invalid, dangerous and relative URLs |
| `invalid_item_empty.xml` | invalid | skip empty item, import 1 |  |
| `invalid_item_missing_identity.xml` | invalid | skip item with no link/guid, import 1 | No link and no guid |
| `invalid_item_missing_title_and_description.xml` | invalid | skip bad item, import 1 | 0.92+ needs title or description |
| `invalid_items_outside_channel.xml` | invalid | reject or import 0 items | Items as siblings of channel |
| `invalid_malformed_version.xml` | invalid | reject: unsupported version |  |
| `invalid_missing_channel.xml` | invalid | reject: missing channel |  |
| `invalid_missing_channel_description.xml` | invalid | reject: channel description required |  |
| `invalid_missing_channel_link.xml` | invalid | reject: channel link required |  |
| `invalid_missing_channel_title.xml` | invalid | reject: channel title required |  |
| `invalid_missing_version_attribute.xml` | invalid | reject or default version | <rss> with no version |
| `invalid_multiple_channels.xml` | invalid | reject or use first channel |  |
| `invalid_overlong_values.xml` | invalid | import 1 item, truncated to column limits | 5k title, 100k description |
| `invalid_ttl_not_numeric.xml` | invalid | import 3 items, ignore ttl |  |
| `invalid_unknown_elements.xml` | invalid | import 3 items, ignore unknown | Extra unknown tags |
| `invalid_uppercase_root.xml` | invalid | reject (XML is case-sensitive) | <RSS> |
| `invalid_whitespace_only_channel_title.xml` | invalid | reject: blank title |  |
| `invalid_wrong_root_element.xml` | invalid | reject: unsupported format | <feed version=...> |
| `corrupted_binary_garbage_in_middle.xml` | corrupted | reject: parse error | Random high bytes injected |
| `corrupted_control_characters.xml` | corrupted | reject: parse error (or strip) | Illegal XML 1.0 chars 0x01 0x0B 0x1F |
| `corrupted_double_declaration.xml` | corrupted | reject: parse error | Two <?xml ?> prologs |
| `corrupted_duplicate_attribute.xml` | corrupted | reject: parse error | Same attribute twice |
| `corrupted_encoding_mismatch.xml` | corrupted | reject or mojibake (latin-1 bytes, declared UTF-8) | Declared UTF-8, bytes are Latin-1 |
| `corrupted_gzip_not_decompressed.xml` | corrupted | reject: parse error (or detect gzip) | Gzip body saved without decompressing |
| `corrupted_improper_nesting.xml` | corrupted | reject: parse error | Overlapping elements |
| `corrupted_invalid_utf8_bytes.xml` | corrupted | reject: encoding error | Invalid UTF-8 sequences |
| `corrupted_json_instead_of_xml.xml` | corrupted | reject: not XML |  |
| `corrupted_mismatched_tags.xml` | corrupted | reject: parse error | <link>...</title> |
| `corrupted_multiple_roots.xml` | corrupted | reject: parse error | Feed concatenated twice |
| `corrupted_null_bytes.xml` | corrupted | reject: parse error | NUL bytes in content |
| `corrupted_tags_with_spaces.xml` | corrupted | reject: parse error | < title> |
| `corrupted_text_after_root.xml` | corrupted | reject: parse error |  |
| `corrupted_truncated_mid_item.xml` | corrupted | reject: parse error (or recover 1 item) | File cut off mid-download |
| `corrupted_truncated_missing_root_close.xml` | corrupted | reject: parse error | Last closing tag missing |
| `corrupted_unclosed_cdata.xml` | corrupted | reject: parse error | CDATA with no ]]> |
| `corrupted_unclosed_comment.xml` | corrupted | reject: parse error |  |
| `corrupted_unclosed_tag.xml` | corrupted | reject: parse error | Missing </title> |
| `corrupted_undefined_entity.xml` | corrupted | reject: parse error (or 0.91 DTD-aware) | HTML entities not defined in XML |
| `corrupted_unescaped_ampersand.xml` | corrupted | reject: parse error | Raw & in text |
| `corrupted_unescaped_less_than.xml` | corrupted | reject: parse error | Raw < in text |
| `corrupted_unknown_encoding.xml` | corrupted | reject: unsupported encoding |  |
| `corrupted_unquoted_attribute.xml` | corrupted | reject: parse error | Attribute value without quotes |
| `corrupted_utf16_declared_utf8.xml` | corrupted | reject or detect UTF-16 via BOM | UTF-16 bytes, declaration says UTF-8 |
| `corrupted_whitespace_before_declaration.xml` | corrupted | reject: parse error | XML decl not at byte 0 |
| `security_billion_laughs.xml` | security | reject quickly; MUST NOT expand (~3GB) | Entity expansion bomb |
| `security_deep_nesting.xml` | security | reject or handle without stack overflow | 5000 nested elements |
| `security_external_dtd.xml` | security | parse without fetching DTD | Remote DTD fetch |
| `security_xxe_file.xml` | security | reject or leave entity unexpanded; MUST NOT read /etc/passwd | XXE local file |
| `security_xxe_ssrf.xml` | security | MUST NOT make HTTP request | XXE SSRF to AWS metadata |

## rss_2.0

| File | Category | Expected | Notes |
|---|---|---|---|
| `valid_20_items.xml` | valid | import 20 items | Above the 15-item limit of 0.90/0.91 |
| `valid_atom_self_link.xml` | valid | import 3 items | atom:link rel=self in channel |
| `valid_cdata.xml` | valid | import 1 item, CDATA text preserved | Title/description in CDATA |
| `valid_comments_and_pi.xml` | valid | import 3 items | XML comments + processing instruction |
| `valid_content_encoded_no_description.xml` | valid | import 1 item, body from content:encoded |  |
| `valid_dc_creator_no_author.xml` | valid | import 1 item, author from dc:creator |  |
| `valid_dc_date_no_pubdate.xml` | valid | import 1 item, date from dc:date (ISO 8601) |  |
| `valid_duplicate_items.xml` | valid | import 2 unique items (dedupe) | Same item repeated twice |
| `valid_empty_no_items.xml` | valid | import 0 items, no error | Valid channel with zero items |
| `valid_full.xml` | valid | import 3 items | All channel + item elements the version supports |
| `valid_guid_default_permalink.xml` | valid | import 1 item, guid treated as permalink | guid without isPermaLink (defaults to true) |
| `valid_guid_not_permalink.xml` | valid | import 1 item, guid used as id | guid isPermaLink=false |
| `valid_html_in_description.xml` | valid | import 1 item, HTML sanitised (script stripped) | Entity-encoded HTML incl. <script> |
| `valid_iso_8859_1.xml` | valid | import 3 items, accents decoded | Real Latin-1 bytes, declared ISO-8859-1 |
| `valid_item_description_only.xml` | valid | import 1 item (title derived) or skip per rule | 0.92+ allows item with only description |
| `valid_item_guid_no_link.xml` | valid | import 1 item, identity from guid | No <link>, has <guid> |
| `valid_item_title_only.xml` | valid | import 1 item or skip (no link/identity) | Item with only title |
| `valid_itunes_podcast.xml` | valid | import 1 item | Podcast feed with iTunes namespace |
| `valid_minimal.xml` | valid | import 1 item | Only the required elements |
| `valid_multiple_categories.xml` | valid | import 1 item with 3 categories | Multiple <category> per item |
| `valid_no_namespaces.xml` | valid | import 3 items | Plain 2.0 with no xmlns declarations |
| `valid_no_xml_declaration.xml` | valid | import 3 items | No <?xml ?> prolog |
| `valid_rfc822_date_variants.xml` | valid | import 5 items, all dates parsed | Offsets, US zones, no weekday, no seconds, 2-digit year, Z/UT |
| `valid_single_item.xml` | valid | import 1 item |  |
| `valid_special_characters.xml` | valid | import 1 item, entities decoded | Predefined + numeric entities, accents, CJK, emoji |
| `valid_uppercase_url_scheme_and_query.xml` | valid | import 3 items | Uppercase scheme, query string, fragment |
| `valid_utf8_bom.xml` | valid | import 3 items | UTF-8 byte-order mark |
| `valid_whitespace_padded.xml` | valid | import 3 items, values trimmed | Leading/trailing whitespace and newlines in values |
| `valid_xml_stylesheet.xml` | valid | import 3 items | Browser-friendly XSL stylesheet PI |
| `invalid_atom_entries_in_rss.xml` | invalid | import 0 items (atom:entry is not an RSS item) |  |
| `invalid_channel_bad_url.xml` | invalid | reject or flag channel link |  |
| `invalid_duplicate_guids.xml` | invalid | import 1 or 2 (guid collision) | Two items share a guid |
| `invalid_empty_channel_values.xml` | invalid | reject: required values blank | <title></title> etc. |
| `invalid_empty_guid.xml` | invalid | import 1 item, fall back to link for identity | <guid></guid> |
| `invalid_empty_version_attribute.xml` | invalid | reject: unknown version |  |
| `invalid_enclosure_bad_length.xml` | invalid | import item, ignore/zero length |  |
| `invalid_enclosure_missing_attributes.xml` | invalid | import item, ignore bad enclosure | enclosure without length/type |
| `invalid_future_date.xml` | invalid | import 1 item, date kept or clamped | pubDate year 2100 |
| `invalid_guid_permalink_not_url.xml` | invalid | import 1 item, guid used as opaque id (not as link) | isPermaLink="true" but value is not a URL |
| `invalid_item_bad_dates.xml` | invalid | import 3 items, dates null/fallback (no crash) | Unparseable / empty pubDate |
| `invalid_item_bad_urls.xml` | invalid | skip/flag all 3 items (bad, javascript:, relative) | Invalid, dangerous and relative URLs |
| `invalid_item_empty.xml` | invalid | skip empty item, import 1 |  |
| `invalid_item_missing_identity.xml` | invalid | skip item with no link/guid, import 1 | No link and no guid |
| `invalid_item_missing_title_and_description.xml` | invalid | skip bad item, import 1 | 0.92+ needs title or description |
| `invalid_items_outside_channel.xml` | invalid | reject or import 0 items | Items as siblings of channel |
| `invalid_malformed_version.xml` | invalid | reject: unsupported version |  |
| `invalid_missing_channel.xml` | invalid | reject: missing channel |  |
| `invalid_missing_channel_description.xml` | invalid | reject: channel description required |  |
| `invalid_missing_channel_link.xml` | invalid | reject: channel link required |  |
| `invalid_missing_channel_title.xml` | invalid | reject: channel title required |  |
| `invalid_missing_version_attribute.xml` | invalid | reject or default version | <rss> with no version |
| `invalid_multiple_channels.xml` | invalid | reject or use first channel |  |
| `invalid_multiple_enclosures.xml` | invalid | import 1 item, first enclosure (spec allows one) |  |
| `invalid_overlong_values.xml` | invalid | import 1 item, truncated to column limits | 5k title, 100k description |
| `invalid_ttl_not_numeric.xml` | invalid | import 3 items, ignore ttl |  |
| `invalid_unknown_elements.xml` | invalid | import 3 items, ignore unknown | Extra unknown tags |
| `invalid_uppercase_root.xml` | invalid | reject (XML is case-sensitive) | <RSS> |
| `invalid_version_2.00.xml` | invalid | reject or normalise to 2.0 | version="2.00" |
| `invalid_version_2.xml` | invalid | reject or normalise to 2.0 | version="2" |
| `invalid_version_with_spaces.xml` | invalid | reject or trim to 2.0 | version=" 2.0 " |
| `invalid_whitespace_only_channel_title.xml` | invalid | reject: blank title |  |
| `invalid_wrong_namespace_uri.xml` | invalid | import 3 items, ignore unknown-namespace content | content: prefix bound to wrong URI |
| `invalid_wrong_root_element.xml` | invalid | reject: unsupported format | <feed version=...> |
| `corrupted_binary_garbage_in_middle.xml` | corrupted | reject: parse error | Random high bytes injected |
| `corrupted_control_characters.xml` | corrupted | reject: parse error (or strip) | Illegal XML 1.0 chars 0x01 0x0B 0x1F |
| `corrupted_double_declaration.xml` | corrupted | reject: parse error | Two <?xml ?> prologs |
| `corrupted_duplicate_attribute.xml` | corrupted | reject: parse error | Same attribute twice |
| `corrupted_encoding_mismatch.xml` | corrupted | reject or mojibake (latin-1 bytes, declared UTF-8) | Declared UTF-8, bytes are Latin-1 |
| `corrupted_gzip_not_decompressed.xml` | corrupted | reject: parse error (or detect gzip) | Gzip body saved without decompressing |
| `corrupted_improper_nesting.xml` | corrupted | reject: parse error | Overlapping elements |
| `corrupted_invalid_utf8_bytes.xml` | corrupted | reject: encoding error | Invalid UTF-8 sequences |
| `corrupted_json_instead_of_xml.xml` | corrupted | reject: not XML |  |
| `corrupted_mismatched_tags.xml` | corrupted | reject: parse error | <link>...</title> |
| `corrupted_multiple_roots.xml` | corrupted | reject: parse error | Feed concatenated twice |
| `corrupted_nested_cdata.xml` | corrupted | reject: parse error | CDATA inside CDATA |
| `corrupted_null_bytes.xml` | corrupted | reject: parse error | NUL bytes in content |
| `corrupted_raw_html_in_content_encoded.xml` | corrupted | reject: parse error | HTML in content:encoded without CDATA |
| `corrupted_tags_with_spaces.xml` | corrupted | reject: parse error | < title> |
| `corrupted_text_after_root.xml` | corrupted | reject: parse error |  |
| `corrupted_truncated_mid_item.xml` | corrupted | reject: parse error (or recover 1 item) | File cut off mid-download |
| `corrupted_truncated_missing_root_close.xml` | corrupted | reject: parse error | Last closing tag missing |
| `corrupted_unclosed_cdata.xml` | corrupted | reject: parse error | CDATA with no ]]> |
| `corrupted_unclosed_comment.xml` | corrupted | reject: parse error |  |
| `corrupted_unclosed_tag.xml` | corrupted | reject: parse error | Missing </title> |
| `corrupted_undeclared_namespace_prefix.xml` | corrupted | reject: unbound prefix | dc: used without xmlns:dc |
| `corrupted_undefined_entity.xml` | corrupted | reject: parse error (or 0.91 DTD-aware) | HTML entities not defined in XML |
| `corrupted_unescaped_ampersand.xml` | corrupted | reject: parse error | Raw & in text |
| `corrupted_unescaped_less_than.xml` | corrupted | reject: parse error | Raw < in text |
| `corrupted_unknown_encoding.xml` | corrupted | reject: unsupported encoding |  |
| `corrupted_unquoted_attribute.xml` | corrupted | reject: parse error | Attribute value without quotes |
| `corrupted_utf16_declared_utf8.xml` | corrupted | reject or detect UTF-16 via BOM | UTF-16 bytes, declaration says UTF-8 |
| `corrupted_whitespace_before_declaration.xml` | corrupted | reject: parse error | XML decl not at byte 0 |
| `security_billion_laughs.xml` | security | reject quickly; MUST NOT expand (~3GB) | Entity expansion bomb |
| `security_deep_nesting.xml` | security | reject or handle without stack overflow | 5000 nested elements |
| `security_external_dtd.xml` | security | parse without fetching DTD | Remote DTD fetch |
| `security_xxe_file.xml` | security | reject or leave entity unexpanded; MUST NOT read /etc/passwd | XXE local file |
| `security_xxe_ssrf.xml` | security | MUST NOT make HTTP request | XXE SSRF to AWS metadata |
