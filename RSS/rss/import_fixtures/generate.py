import os, sys
OUT = sys.argv[1]
DECL = '<?xml version="1.0" encoding="UTF-8"?>\n'
NS090 = 'http://my.netscape.com/rdf/simple/0.9/'
RDF = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
NS20 = ('\n  xmlns:dc="http://purl.org/dc/elements/1.1/"\n  xmlns:content="http://purl.org/rss/1.0/modules/content/"'
        '\n  xmlns:atom="http://www.w3.org/2005/Atom"\n  xmlns:media="http://search.yahoo.com/mrss/"'
        '\n  xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"')
seen, BASELINE = {}, {}
manifest = []  # (path, category, expected, note)

ARTICLES = [
    ("Artificial Intelligence", "Artificial_intelligence", "Artificial intelligence is intelligence demonstrated by machines.", "Computer Science", "Mon, 05 Jan 2026 09:00:00 GMT"),
    ("Ruby on Rails", "Ruby_on_Rails", "Ruby on Rails is a server-side web application framework written in Ruby.", "Web Development", "Tue, 06 Jan 2026 10:30:00 GMT"),
    ("PostgreSQL", "PostgreSQL", "PostgreSQL is a free and open-source relational database management system.", "Databases", "Wed, 07 Jan 2026 14:15:00 GMT"),
]

def w(ver, name, content, cat, expected, note):
    d = os.path.join(OUT, f"rss_{ver}" if ver else "common")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, name)
    data = content if isinstance(content, bytes) else content.encode("utf-8")
    if data in seen.setdefault(d, set()):
        return  # identical to a fixture already generated for this version
    if BASELINE.get(d) == data:
        print("NO-OP:", p)
    seen[d].add(data)
    open(p, "wb").write(data)
    manifest.append((os.path.relpath(p, OUT), cat, expected, note))

# ---------- item / channel builders ----------
def item(ver, a, i=0, extra="", title=True, link=True, desc=True):
    t, slug, d, c, date = a
    url = f"https://en.wikipedia.org/wiki/{slug}"
    parts = []
    if title: parts.append(f"<title>{t}</title>")
    if link: parts.append(f"<link>{url}</link>")
    if ver != "0.90" and desc: parts.append(f"<description>{d}</description>")
    if ver in ("0.92", "0.93", "0.94", "2.0"): parts.append(f"<category>{c}</category>" if ver not in ("0.94", "2.0") else f'<category domain="https://en.wikipedia.org/wiki/Category:">{c}</category>')
    if ver in ("0.93", "0.94", "2.0"): parts.append(f"<pubDate>{date}</pubDate>")
    if ver in ("0.94", "2.0"):
        parts.append(f'<guid isPermaLink="true">{url}</guid>')
        parts.append("<author>editors@wikipedia.org (Wikipedia Editors)</author>")
        parts.append(f"<comments>https://en.wikipedia.org/wiki/Talk:{slug}</comments>")
    if extra: parts.append(extra)
    return "    <item>\n" + "".join(f"      {p}\n" for p in parts) + "    </item>\n"

def chan_head(ver, title="Wikipedia Articles - RSS {v}", link="https://www.wikipedia.org/", desc="Notable Wikipedia articles in RSS {v} format.", extra=""):
    parts = []
    if title is not None: parts.append(f"<title>{title.format(v=ver)}</title>")
    if link is not None: parts.append(f"<link>{link}</link>")
    if desc is not None: parts.append(f"<description>{desc.format(v=ver)}</description>")
    if ver != "0.90": parts.append("<language>en-us</language>")
    if extra: parts.append(extra)
    return "".join(f"    {p}\n" for p in parts)

def doc(ver, items="", head=None, decl=DECL, root_attrs=None, doctype=""):
    head = chan_head(ver) if head is None else head
    if ver == "0.90":
        attrs = root_attrs or f'xmlns:rdf="{RDF}"\n  xmlns="{NS090}"'
        # 0.90: items are siblings of channel
        body = "  <channel>\n" + head.replace("    ", "    ", 1) + "  </channel>\n" + items.replace("    <item>", "  <item>").replace("\n      ", "\n    ").replace("    </item>", "  </item>")
        return f"{decl}{doctype}<rdf:RDF\n  {attrs}>\n{body}</rdf:RDF>\n"
    attrs = root_attrs if root_attrs is not None else f'version="{ver}"' + (NS20 if ver == "2.0" else "")
    return f"{decl}{doctype}<rss {attrs}>\n  <channel>\n{head}{items}  </channel>\n</rss>\n"

def items_all(ver, **kw): return "".join(item(ver, a, **kw) for a in ARTICLES)

FULL_EXTRA = {
    "0.90": "",
    "0.91": "<copyright>CC BY-SA 4.0</copyright>\n    <managingEditor>editors@wikipedia.org</managingEditor>\n    <webMaster>webmaster@wikipedia.org</webMaster>\n    <pubDate>Mon, 05 Jan 2026 08:00:00 GMT</pubDate>\n    <lastBuildDate>Wed, 07 Jan 2026 15:00:00 GMT</lastBuildDate>\n    <docs>http://my.netscape.com/publish/formats/rss-spec-0.91.html</docs>\n    <image>\n      <title>Wikipedia</title>\n      <url>https://upload.wikimedia.org/wikipedia/commons/6/63/Wikipedia-logo.png</url>\n      <link>https://www.wikipedia.org/</link>\n      <width>88</width>\n      <height>31</height>\n    </image>",
}
FULL_EXTRA["0.92"] = FULL_EXTRA["0.91"].replace("rss-spec-0.91.html", "rss-0.92.html").replace("http://my.netscape.com/publish/formats/", "http://backend.userland.com/") + '\n    <cloud domain="rpc.sys.com" port="80" path="/RPC2" registerProcedure="pingMe" protocol="soap"/>'
FULL_EXTRA["0.93"] = FULL_EXTRA["0.92"].replace("rss-0.92.html", "rss093")
FULL_EXTRA["0.94"] = FULL_EXTRA["0.93"].replace("rss093", "rss094") + "\n    <ttl>60</ttl>"

ITEM_EXTRA = {
    "0.92": '<source url="https://www.wikipedia.org/rss">Wikipedia</source>\n      <enclosure url="https://upload.wikimedia.org/sample.mp3" length="24986239" type="audio/mpeg"/>',
}
ITEM_EXTRA["0.93"] = ITEM_EXTRA["0.92"] + "\n      <expirationDate>Fri, 31 Dec 2027 23:59:59 GMT</expirationDate>"
ITEM_EXTRA["0.94"] = ITEM_EXTRA["0.92"]
FULL_EXTRA["2.0"] = (FULL_EXTRA["0.94"].replace("http://backend.userland.com/rss094", "https://www.rssboard.org/rss-specification")
    .replace("<height>31</height>", "<height>31</height>\n      <description>Wikipedia logo</description>")
    + '\n    <generator>PathFactory fixture generator</generator>'
    + '\n    <category domain="https://www.wikipedia.org/">Encyclopedia</category>'
    + '\n    <atom:link href="https://www.wikipedia.org/rss" rel="self" type="application/rss+xml"/>'
    + '\n    <textInput>\n      <title>Search</title>\n      <description>Search Wikipedia</description>\n      <name>q</name>\n      <link>https://en.wikipedia.org/w/index.php</link>\n    </textInput>'
    + '\n    <skipHours><hour>0</hour><hour>23</hour></skipHours>\n    <skipDays><day>Sunday</day></skipDays>'
    + '\n    <itunes:author>Wikipedia</itunes:author>\n    <itunes:explicit>false</itunes:explicit>')
ITEM_EXTRA["2.0"] = ITEM_EXTRA["0.92"] + (
    '\n      <dc:creator>Wikipedia Editors</dc:creator>'
    '\n      <content:encoded><![CDATA[<p>Full <b>HTML</b> body &amp; more.</p>]]></content:encoded>'
    '\n      <media:content url="https://upload.wikimedia.org/sample.jpg" medium="image" width="640" height="480"/>'
    '\n      <media:thumbnail url="https://upload.wikimedia.org/sample_thumb.jpg"/>')

for ver in ["0.90", "0.91", "0.92", "0.93", "0.94", "2.0"]:
    V = lambda name, c, exp, note: w(ver, name, c, "valid", exp, note)
    I = lambda name, c, exp, note: w(ver, name, c, "invalid", exp, note)
    C = lambda name, c, exp, note: w(ver, name, c, "corrupted", exp, note)
    S = lambda name, c, exp, note: w(ver, name, c, "security", exp, note)
    full_items = "".join(item(ver, a, extra=ITEM_EXTRA.get(ver, "")) for a in ARTICLES)
    if ver == "0.90":
        img = '  <image>\n    <title>Wikipedia</title>\n    <url>https://upload.wikimedia.org/wikipedia/commons/6/63/Wikipedia-logo.png</url>\n    <link>https://www.wikipedia.org/</link>\n  </image>\n'
        txt = '  <textinput>\n    <title>Search Wikipedia</title>\n    <description>Search Wikipedia articles</description>\n    <name>search</name>\n    <link>https://en.wikipedia.org/w/index.php</link>\n  </textinput>\n'
        full = doc(ver, items_all(ver)).replace("</rdf:RDF>", txt + "</rdf:RDF>").replace("  </channel>\n", "  </channel>\n" + img, 1)
    else:
        full = doc(ver, full_items, head=chan_head(ver, extra=FULL_EXTRA[ver]))
    good = doc(ver, items_all(ver))
    BASELINE[os.path.join(OUT, f"rss_{ver}")] = good.encode()

    # ---------------- VALID ----------------
    V("valid_full.xml", full, "import 3 items", "All channel + item elements the version supports")
    V("valid_minimal.xml", doc(ver, item(ver, ARTICLES[0], desc=False) if ver != "0.90" else item(ver, ARTICLES[0]), head=chan_head(ver).replace("    <language>en-us</language>\n", "") if ver != "0.91" else None),
      "import 1 item", "Only the required elements")
    V("valid_empty_no_items.xml", doc(ver, ""), "import 0 items, no error", "Valid channel with zero items")
    V("valid_single_item.xml", doc(ver, item(ver, ARTICLES[0])), "import 1 item", "")
    many = "".join(item(ver, (f"Article {n}", f"Article_{n}", f"Description for article {n}.", "General", f"Thu, {n:02d} Jan 2026 12:00:00 GMT")) for n in range(1, 21))
    V("valid_20_items.xml", doc(ver, many), "import 20 items" + (" (spec caps at 15; decide truncate vs accept)" if ver in ("0.90", "0.91") else ""), "Above the 15-item limit of 0.90/0.91")
    V("valid_duplicate_items.xml", doc(ver, item(ver, ARTICLES[0]) * 2 + item(ver, ARTICLES[1])), "import 2 unique items (dedupe)", "Same item repeated twice")
    special = ("C++ &amp; C# &lt;Languages&gt;", "C%2B%2B", "Quotes &quot;double&quot; &apos;single&apos; &#169; &#x2603; café 日本語 \U0001F680", "Programming", "Thu, 08 Jan 2026 09:00:00 GMT")
    V("valid_special_characters.xml", doc(ver, item(ver, special)), "import 1 item, entities decoded", "Predefined + numeric entities, accents, CJK, emoji")
    cdata = ("<![CDATA[Ruby & Rails <Guide>]]>", "Ruby_on_Rails", "<![CDATA[<p>Rails uses <b>MVC</b> & conventions.</p>]]>", "Web Development", "Fri, 09 Jan 2026 09:00:00 GMT")
    V("valid_cdata.xml", doc(ver, item(ver, cdata)), "import 1 item, CDATA text preserved", "Title/description in CDATA")
    if ver != "0.90":
        html = ("PostgreSQL", "PostgreSQL", "&lt;p&gt;An &lt;a href=&quot;https://www.postgresql.org&quot;&gt;open-source&lt;/a&gt; database.&lt;/p&gt;&lt;script&gt;alert(1)&lt;/script&gt;", "Databases", "Sat, 10 Jan 2026 09:00:00 GMT")
        V("valid_html_in_description.xml", doc(ver, item(ver, html)), "import 1 item, HTML sanitised (script stripped)", "Entity-encoded HTML incl. <script>")
    V("valid_no_xml_declaration.xml", good.replace(DECL, ""), "import 3 items", "No <?xml ?> prolog")
    V("valid_utf8_bom.xml", b"\xef\xbb\xbf" + good.encode(), "import 3 items", "UTF-8 byte-order mark")
    V("valid_iso_8859_1.xml", good.replace("UTF-8", "ISO-8859-1").replace("Ruby on Rails", "Café Résumé").encode("latin-1"), "import 3 items, accents decoded", "Real Latin-1 bytes, declared ISO-8859-1")
    V("valid_whitespace_padded.xml", good.replace("<title>Artificial Intelligence</title>", "<title>\n        Artificial Intelligence   \n      </title>").replace("<link>https://en.wikipedia.org/wiki/Ruby_on_Rails</link>", "<link>  https://en.wikipedia.org/wiki/Ruby_on_Rails  </link>"),
      "import 3 items, values trimmed", "Leading/trailing whitespace and newlines in values")
    V("valid_comments_and_pi.xml", good.replace("  <channel>", "  <!-- generated by test fixture -->\n  <?processing instruction?>\n  <channel>", 1), "import 3 items", "XML comments + processing instruction")
    V("valid_uppercase_url_scheme_and_query.xml", good.replace("https://en.wikipedia.org/wiki/PostgreSQL", "HTTPS://en.wikipedia.org/w/index.php?title=PostgreSQL&amp;action=view#History"), "import 3 items", "Uppercase scheme, query string, fragment")
    if ver == "0.91":
        V("valid_with_netscape_doctype.xml", doc(ver, items_all(ver), doctype='<!DOCTYPE rss PUBLIC "-//Netscape Communications//DTD RSS 0.91//EN" "http://my.netscape.com/publish/formats/rss-0.91.dtd">\n'),
          "import 3 items (must NOT fetch the DTD)", "Netscape DOCTYPE, common in real 0.91 feeds")
        V("valid_skiphours_skipdays_textinput.xml", doc(ver, items_all(ver), head=chan_head(ver, extra="<rating>(PICS-1.1 \"http://www.rsac.org/ratingsv01.html\" l by \"webmaster@wikipedia.org\" on \"2026.01.01T08:15-0500\" r (n 0 s 0 v 0 l 0))</rating>\n    <skipHours><hour>1</hour><hour>2</hour></skipHours>\n    <skipDays><day>Saturday</day><day>Sunday</day></skipDays>\n    <textinput><title>Search</title><description>Search Wikipedia</description><name>q</name><link>https://en.wikipedia.org/w/index.php</link></textinput>")),
          "import 3 items", "rating, skipHours, skipDays, textinput")
    if ver in ("0.92", "0.93", "0.94", "2.0"):
        V("valid_item_description_only.xml", doc(ver, item(ver, ARTICLES[0], title=False, link=False)), "import 1 item (title derived) or skip per rule", "0.92+ allows item with only description")
        V("valid_item_title_only.xml", doc(ver, item(ver, ARTICLES[0], link=False, desc=False)), "import 1 item or skip (no link/identity)", "Item with only title")
        V("valid_multiple_categories.xml", doc(ver, item(ver, ARTICLES[0], extra="<category>Machine Learning</category>\n      <category>Robotics</category>")), "import 1 item with 3 categories", "Multiple <category> per item")
    if ver in ("0.93", "0.94"):
        V("valid_expired_item.xml", doc(ver, item(ver, ARTICLES[0], extra="<expirationDate>Thu, 01 Jan 2015 00:00:00 GMT</expirationDate>") + item(ver, ARTICLES[1])), "import 1 item (expired one skipped) or 2", "Item whose expirationDate is in the past")
    if ver in ("0.94", "2.0"):
        V("valid_guid_not_permalink.xml", doc(ver, item(ver, ARTICLES[0]).replace('isPermaLink="true">https://en.wikipedia.org/wiki/Artificial_intelligence', 'isPermaLink="false">wiki-article-0001')), "import 1 item, guid used as id", "guid isPermaLink=false")
        V("valid_item_guid_no_link.xml", doc(ver, item(ver, ARTICLES[0], link=False)), "import 1 item, identity from guid", "No <link>, has <guid>")

    # ---------------- INVALID (well-formed but wrong) ----------------
    if ver == "0.90":
        I("invalid_missing_channel.xml", f'{DECL}<rdf:RDF\n  xmlns:rdf="{RDF}"\n  xmlns="{NS090}">\n' + items_all(ver).replace("    ", "  ") + "</rdf:RDF>\n", "reject: missing channel", "")
        I("invalid_wrong_namespace.xml", doc(ver, items_all(ver), root_attrs=f'xmlns:rdf="{RDF}"\n  xmlns="http://purl.org/rss/1.0/"'), "reject or detect as RSS 1.0, not 0.90", "RSS 1.0 namespace on 0.90 structure")
        I("invalid_missing_default_namespace.xml", doc(ver, items_all(ver), root_attrs=f'xmlns:rdf="{RDF}"'), "reject: unknown/undetectable version", "No 0.90 namespace")
        I("invalid_items_inside_channel.xml", f'{DECL}<rdf:RDF\n  xmlns:rdf="{RDF}"\n  xmlns="{NS090}">\n  <channel>\n' + chan_head(ver) + items_all(ver) + "  </channel>\n</rdf:RDF>\n", "reject or tolerate (spec: items are siblings of channel)", "Items nested inside channel")
        I("invalid_rss_root_with_090_version.xml", doc("0.91", items_all("0.91"), root_attrs='version="0.90"'), "reject or treat as 0.90", "<rss version=\"0.90\"> instead of rdf:RDF")
        I("invalid_multiple_channels.xml", good.replace("  </channel>\n", "  </channel>\n  <channel>\n" + chan_head(ver, title="Second Channel") + "  </channel>\n", 1), "reject or use first channel", "")
    else:
        I("invalid_missing_channel.xml", f'{DECL}<rss version="{ver}">\n' + items_all(ver).replace("    ", "  ").replace("      ", "    ") + "</rss>\n", "reject: missing channel", "")
        I("invalid_missing_version_attribute.xml", doc(ver, items_all(ver), root_attrs=""), "reject or default version", "<rss> with no version")
        I("invalid_empty_version_attribute.xml", doc(ver, items_all(ver), root_attrs='version=""'), "reject: unknown version", "")
        I("invalid_malformed_version.xml", doc(ver, items_all(ver), root_attrs=f'version="v{ver}-beta"'), "reject: unsupported version", "")
        I("invalid_wrong_root_element.xml", doc(ver, items_all(ver)).replace("<rss ", "<feed ").replace("</rss>", "</feed>"), "reject: unsupported format", "<feed version=...>")
        I("invalid_uppercase_root.xml", doc(ver, items_all(ver)).replace("<rss ", "<RSS ").replace("</rss>", "</RSS>"), "reject (XML is case-sensitive)", "<RSS>")
        I("invalid_multiple_channels.xml", good.replace("  </channel>\n", "  </channel>\n  <channel>\n" + chan_head(ver, title="Second Channel") + "  </channel>\n", 1), "reject or use first channel", "")
        I("invalid_items_outside_channel.xml", f'{DECL}<rss version="{ver}">\n  <channel>\n' + chan_head(ver) + "  </channel>\n" + items_all(ver) + "</rss>\n", "reject or import 0 items", "Items as siblings of channel")
        if ver == "0.91":
            I("invalid_missing_language.xml", good.replace("    <language>en-us</language>\n", ""), "reject or tolerate (language required in 0.91)", "")
    I("invalid_missing_channel_title.xml", doc(ver, items_all(ver), head=chan_head(ver, title=None)), "reject: channel title required", "")
    I("invalid_missing_channel_link.xml", doc(ver, items_all(ver), head=chan_head(ver, link=None)), "reject: channel link required", "")
    I("invalid_missing_channel_description.xml", doc(ver, items_all(ver), head=chan_head(ver, desc=None)), "reject: channel description required", "")
    I("invalid_empty_channel_values.xml", doc(ver, items_all(ver), head=chan_head(ver, title="", link="", desc="")), "reject: required values blank", "<title></title> etc.")
    I("invalid_whitespace_only_channel_title.xml", doc(ver, items_all(ver), head=chan_head(ver, title="   ")), "reject: blank title", "")
    if ver in ("0.90", "0.91"):
        I("invalid_item_missing_title.xml", doc(ver, item(ver, ARTICLES[0], title=False) + item(ver, ARTICLES[1])), "skip bad item, import 1", "title required per item in 0.90/0.91")
        I("invalid_item_missing_link.xml", doc(ver, item(ver, ARTICLES[0], link=False) + item(ver, ARTICLES[1])), "skip bad item, import 1", "link required per item in 0.90/0.91")
    else:
        I("invalid_item_missing_title_and_description.xml", doc(ver, item(ver, ARTICLES[0], title=False, desc=False) + item(ver, ARTICLES[1])), "skip bad item, import 1", "0.92+ needs title or description")
    I("invalid_item_empty.xml", doc(ver, "    <item>\n    </item>\n" + item(ver, ARTICLES[1])), "skip empty item, import 1", "")
    I("invalid_item_missing_identity.xml", doc(ver, item(ver, ARTICLES[0], link=False, extra="") .replace(f'<guid isPermaLink="true">https://en.wikipedia.org/wiki/Artificial_intelligence</guid>\n      ', "") + item(ver, ARTICLES[1])),
      "skip item with no link/guid, import 1", "No link and no guid")
    I("invalid_item_bad_urls.xml", doc(ver, item(ver, ARTICLES[0]).replace("https://en.wikipedia.org/wiki/Artificial_intelligence", "not a url") + item(ver, ARTICLES[1]).replace("https://en.wikipedia.org/wiki/Ruby_on_Rails", "javascript:alert(1)") + item(ver, ARTICLES[2]).replace("https://en.wikipedia.org/wiki/PostgreSQL", "/wiki/PostgreSQL")),
      "skip/flag all 3 items (bad, javascript:, relative)", "Invalid, dangerous and relative URLs")
    I("invalid_channel_bad_url.xml", doc(ver, items_all(ver), head=chan_head(ver, link="ftp//broken")), "reject or flag channel link", "")
    if ver in ("0.93", "0.94", "2.0"):
        I("invalid_item_bad_dates.xml", doc(ver, item(ver, ARTICLES[0]).replace("Mon, 05 Jan 2026 09:00:00 GMT", "yesterday") + item(ver, ARTICLES[1]).replace("Tue, 06 Jan 2026 10:30:00 GMT", "2026-13-45T99:99:99Z") + item(ver, ARTICLES[2]).replace("Wed, 07 Jan 2026 14:15:00 GMT", "")),
          "import 3 items, dates null/fallback (no crash)", "Unparseable / empty pubDate")
        I("invalid_future_date.xml", doc(ver, item(ver, ARTICLES[0]).replace("Mon, 05 Jan 2026", "Fri, 01 Jan 2100")), "import 1 item, date kept or clamped", "pubDate year 2100")
    if ver in ("0.92", "0.93", "0.94", "2.0"):
        I("invalid_enclosure_missing_attributes.xml", doc(ver, item(ver, ARTICLES[0], extra='<enclosure url="https://upload.wikimedia.org/sample.mp3"/>')), "import item, ignore bad enclosure", "enclosure without length/type")
        I("invalid_enclosure_bad_length.xml", doc(ver, item(ver, ARTICLES[0], extra='<enclosure url="https://upload.wikimedia.org/sample.mp3" length="-12abc" type="audio/mpeg"/>')), "import item, ignore/zero length", "")
    if ver in ("0.94", "2.0"):
        I("invalid_ttl_not_numeric.xml", doc(ver, items_all(ver), head=chan_head(ver, extra="<ttl>sixty</ttl>")), "import 3 items, ignore ttl", "")
        I("invalid_duplicate_guids.xml", doc(ver, item(ver, ARTICLES[0]) + item(ver, ARTICLES[1]).replace('<guid isPermaLink="true">https://en.wikipedia.org/wiki/Ruby_on_Rails', '<guid isPermaLink="true">https://en.wikipedia.org/wiki/Artificial_intelligence')), "import 1 or 2 (guid collision)", "Two items share a guid")
    I("invalid_overlong_values.xml", doc(ver, item(ver, ("A" * 5000, "Long", "B" * 100000, "Long", "Mon, 05 Jan 2026 09:00:00 GMT"))), "import 1 item, truncated to column limits", "5k title, 100k description")
    I("invalid_unknown_elements.xml", good.replace("<item>", "<foo:bar xmlns:foo=\"urn:x\">ignored</foo:bar>\n  <unknownTag>ignored</unknownTag>\n  <item>", 1), "import 3 items, ignore unknown", "Extra unknown tags")

    # ---------------- CORRUPTED (not well-formed) ----------------
    C("corrupted_unclosed_tag.xml", good.replace("</title>", "", 2).replace("</title>", "</title>"), "reject: parse error", "Missing </title>")
    C("corrupted_mismatched_tags.xml", good.replace("<link>https://en.wikipedia.org/wiki/Ruby_on_Rails</link>", "<link>https://en.wikipedia.org/wiki/Ruby_on_Rails</title>"), "reject: parse error", "<link>...</title>")
    C("corrupted_improper_nesting.xml", __import__("re").sub(r"<title>Artificial Intelligence</title>\s*<link>(.*?)</link>", r"<title>Artificial Intelligence<link>\1</title></link>", good, count=1), "reject: parse error", "Overlapping elements")
    C("corrupted_unescaped_ampersand.xml", good.replace("Ruby on Rails", "Ruby & Rails"), "reject: parse error", "Raw & in text")
    C("corrupted_unescaped_less_than.xml", good.replace("Artificial Intelligence</title>", "AI < Humans</title>", 1), "reject: parse error", "Raw < in text")
    C("corrupted_undefined_entity.xml", good.replace("Ruby on Rails", "Ruby&nbsp;on&nbsp;Rails&mdash;Guide"), "reject: parse error (or 0.91 DTD-aware)", "HTML entities not defined in XML")
    C("corrupted_truncated_mid_item.xml", good[: good.index("Ruby on Rails") + 5], "reject: parse error (or recover 1 item)", "File cut off mid-download")
    C("corrupted_truncated_missing_root_close.xml", good.rsplit("</", 1)[0], "reject: parse error", "Last closing tag missing")
    C("corrupted_unclosed_cdata.xml", doc(ver, item(ver, ("<![CDATA[Never closed", "x", "desc", "c", "Mon, 05 Jan 2026 09:00:00 GMT"))), "reject: parse error", "CDATA with no ]]>")
    C("corrupted_unclosed_comment.xml", good.replace("  <channel>", "  <!-- never closed\n  <channel>", 1), "reject: parse error", "")
    C("corrupted_unquoted_attribute.xml", good.replace(f'version="{ver}"', f"version={ver}") if ver != "0.90" else good.replace(f'xmlns="{NS090}"', f"xmlns={NS090}"), "reject: parse error", "Attribute value without quotes")
    C("corrupted_duplicate_attribute.xml", good.replace("<rss ", f'<rss version="{ver}" ') if ver != "0.90" else good.replace("<rdf:RDF\n", f'<rdf:RDF xmlns:rdf="{RDF}"\n'), "reject: parse error", "Same attribute twice")
    C("corrupted_multiple_roots.xml", good + good.replace(DECL, ""), "reject: parse error", "Feed concatenated twice")
    C("corrupted_text_after_root.xml", good + "trailing garbage <<>>\n", "reject: parse error", "")
    C("corrupted_whitespace_before_declaration.xml", "\n\n   " + good, "reject: parse error", "XML decl not at byte 0")
    C("corrupted_double_declaration.xml", DECL + good, "reject: parse error", "Two <?xml ?> prologs")
    C("corrupted_control_characters.xml", good.replace("Ruby on Rails", "Ruby\x01on\x0bRails\x1f"), "reject: parse error (or strip)", "Illegal XML 1.0 chars 0x01 0x0B 0x1F")
    C("corrupted_null_bytes.xml", good.encode().replace(b"PostgreSQL</title>", b"Postgre\x00\x00SQL</title>"), "reject: parse error", "NUL bytes in content")
    C("corrupted_invalid_utf8_bytes.xml", good.encode().replace("Ruby on Rails".encode(), b"Ruby \xc3\x28 \xff\xfe Rails"), "reject: encoding error", "Invalid UTF-8 sequences")
    C("corrupted_encoding_mismatch.xml", good.replace("Ruby on Rails", "Café Résumé").encode("latin-1"), "reject or mojibake (latin-1 bytes, declared UTF-8)", "Declared UTF-8, bytes are Latin-1")
    C("corrupted_utf16_declared_utf8.xml", good.encode("utf-16"), "reject or detect UTF-16 via BOM", "UTF-16 bytes, declaration says UTF-8")
    C("corrupted_unknown_encoding.xml", good.replace("UTF-8", "KLINGON-1"), "reject: unsupported encoding", "")
    C("corrupted_binary_garbage_in_middle.xml", good.encode().replace(b"  <channel>", b"  " + bytes(range(128, 256)) + b"\n  <channel>", 1), "reject: parse error", "Random high bytes injected")
    C("corrupted_gzip_not_decompressed.xml", __import__("gzip").compress(good.encode(), mtime=0), "reject: parse error (or detect gzip)", "Gzip body saved without decompressing")
    C("corrupted_json_instead_of_xml.xml", '{"rss":{"version":"%s","channel":{"title":"Wikipedia"}}}\n' % ver, "reject: not XML", "")
    C("corrupted_tags_with_spaces.xml", good.replace("<title>", "< title>", 1), "reject: parse error", "< title>")

    # ---------------- SECURITY ----------------
    xxe = f'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE rss [\n  <!ENTITY xxe SYSTEM "file:///etc/passwd">\n]>\n'
    S("security_xxe_file.xml", xxe + good.replace(DECL, "").replace("Ruby on Rails</title>", "&xxe;</title>"), "reject or leave entity unexpanded; MUST NOT read /etc/passwd", "XXE local file")
    S("security_xxe_ssrf.xml", xxe.replace("file:///etc/passwd", "http://169.254.169.254/latest/meta-data/") + good.replace(DECL, "").replace("Ruby on Rails</title>", "&xxe;</title>"), "MUST NOT make HTTP request", "XXE SSRF to AWS metadata")
    bl = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE rss [\n  <!ENTITY lol "lol">\n' + "".join(f'  <!ENTITY lol{n} "{("&lol" + (str(n - 1) if n > 1 else "") + ";") * 10}">\n' for n in range(1, 10)) + "]>\n"
    S("security_billion_laughs.xml", bl + good.replace(DECL, "").replace("Ruby on Rails</title>", "&lol9;</title>"), "reject quickly; MUST NOT expand (~3GB)", "Entity expansion bomb")
    S("security_external_dtd.xml", good.replace(DECL, DECL + '<!DOCTYPE rss SYSTEM "http://attacker.example.com/evil.dtd">\n'), "parse without fetching DTD", "Remote DTD fetch")
    S("security_deep_nesting.xml", good.replace("<description>Artificial", "<description>" + "<x>" * 5000 + "</x>" * 5000 + "Artificial", 1) if ver != "0.90" else good.replace("<title>Artificial Intelligence", "<title>" + "<x>" * 5000 + "</x>" * 5000 + "Artificial Intelligence", 1), "reject or handle without stack overflow", "5000 nested elements")

    if ver == "2.0":
        a0 = ARTICLES[0]; i0 = item(ver, a0)
        V("valid_guid_default_permalink.xml", doc(ver, i0.replace(' isPermaLink="true"', "")), "import 1 item, guid treated as permalink", "guid without isPermaLink (defaults to true)")
        V("valid_content_encoded_no_description.xml", doc(ver, item(ver, a0, desc=False, extra="<content:encoded><![CDATA[<p>Body only in content:encoded</p>]]></content:encoded>")), "import 1 item, body from content:encoded", "")
        V("valid_dc_date_no_pubdate.xml", doc(ver, i0.replace("<pubDate>Mon, 05 Jan 2026 09:00:00 GMT</pubDate>", "<dc:date>2026-01-05T09:00:00+05:30</dc:date>")), "import 1 item, date from dc:date (ISO 8601)", "")
        V("valid_dc_creator_no_author.xml", doc(ver, i0.replace("<author>editors@wikipedia.org (Wikipedia Editors)</author>", "<dc:creator>Jimmy Wales</dc:creator>")), "import 1 item, author from dc:creator", "")
        dates = ["Mon, 05 Jan 2026 09:00:00 +0530", "Tue, 6 Jan 2026 10:30:00 EST", "07 Jan 2026 14:15 -0800", "Thu, 08 Jan 26 09:00:00 Z", "Fri, 09 Jan 2026 09:00:00 UT"]
        V("valid_rfc822_date_variants.xml", doc(ver, "".join(item(ver, (f"Date {n}", f"Date_{n}", d, "Dates", d)) for n, d in enumerate(dates, 1))), "import 5 items, all dates parsed", "Offsets, US zones, no weekday, no seconds, 2-digit year, Z/UT")
        V("valid_xml_stylesheet.xml", good.replace(DECL, DECL + '<?xml-stylesheet type="text/xsl" href="https://www.wikipedia.org/rss.xsl"?>\n'), "import 3 items", "Browser-friendly XSL stylesheet PI")
        V("valid_itunes_podcast.xml", doc(ver, item(ver, a0, extra='<enclosure url="https://upload.wikimedia.org/ep1.mp3" length="1048576" type="audio/mpeg"/>\n      <itunes:duration>00:42:10</itunes:duration>\n      <itunes:episode>1</itunes:episode>'), head=chan_head(ver, extra='<itunes:author>Wikipedia</itunes:author>\n    <itunes:image href="https://upload.wikimedia.org/cover.jpg"/>\n    <itunes:category text="Education"/>')), "import 1 item", "Podcast feed with iTunes namespace")
        V("valid_atom_self_link.xml", doc(ver, items_all(ver), head=chan_head(ver, extra='<atom:link href="https://www.wikipedia.org/rss" rel="self" type="application/rss+xml"/>')), "import 3 items", "atom:link rel=self in channel")
        V("valid_no_namespaces.xml", doc(ver, items_all(ver), root_attrs='version="2.0"'), "import 3 items", "Plain 2.0 with no xmlns declarations")
        I("invalid_version_2.xml", doc(ver, items_all(ver), root_attrs='version="2"'), "reject or normalise to 2.0", 'version="2"')
        I("invalid_version_2.00.xml", doc(ver, items_all(ver), root_attrs='version="2.00"'), "reject or normalise to 2.0", 'version="2.00"')
        I("invalid_version_with_spaces.xml", doc(ver, items_all(ver), root_attrs='version=" 2.0 "'), "reject or trim to 2.0", 'version=" 2.0 "')
        I("invalid_atom_entries_in_rss.xml", doc(ver, '    <atom:entry>\n      <atom:title>Artificial Intelligence</atom:title>\n      <atom:link href="https://en.wikipedia.org/wiki/Artificial_intelligence"/>\n    </atom:entry>\n'), "import 0 items (atom:entry is not an RSS item)", "")
        I("invalid_empty_guid.xml", doc(ver, i0.replace(">https://en.wikipedia.org/wiki/Artificial_intelligence</guid>", "></guid>")), "import 1 item, fall back to link for identity", "<guid></guid>")
        I("invalid_guid_permalink_not_url.xml", doc(ver, i0.replace(">https://en.wikipedia.org/wiki/Artificial_intelligence</guid>", ">article-0001</guid>")), "import 1 item, guid used as opaque id (not as link)", 'isPermaLink="true" but value is not a URL')
        I("invalid_multiple_enclosures.xml", doc(ver, item(ver, a0, extra='<enclosure url="https://upload.wikimedia.org/a.mp3" length="1" type="audio/mpeg"/>\n      <enclosure url="https://upload.wikimedia.org/b.mp3" length="2" type="audio/mpeg"/>')), "import 1 item, first enclosure (spec allows one)", "")
        I("invalid_wrong_namespace_uri.xml", doc(ver, items_all(ver, extra="<content:encoded>Wrong namespace</content:encoded>"), root_attrs='version="2.0" xmlns:content="http://example.com/not-content"'), "import 3 items, ignore unknown-namespace content", "content: prefix bound to wrong URI")
        C("corrupted_undeclared_namespace_prefix.xml", doc(ver, items_all(ver, extra="<dc:creator>Wikipedia Editors</dc:creator>"), root_attrs='version="2.0"'), "reject: unbound prefix", "dc: used without xmlns:dc")
        C("corrupted_raw_html_in_content_encoded.xml", doc(ver, item(ver, a0, extra="<content:encoded><p>Unclosed <br> paragraph & raw</content:encoded>")), "reject: parse error", "HTML in content:encoded without CDATA")
        C("corrupted_nested_cdata.xml", doc(ver, item(ver, a0, extra="<content:encoded><![CDATA[outer <![CDATA[inner]]> tail]]></content:encoded>")), "reject: parse error", "CDATA inside CDATA")

# ---------------- COMMON (version-agnostic) ----------------
w(None, "empty_file.xml", b"", "corrupted", "reject: empty body", "0 bytes")
w(None, "whitespace_only.xml", "   \n\t\n  ", "corrupted", "reject: empty body", "")
w(None, "declaration_only.xml", DECL, "corrupted", "reject: no root element", "")
w(None, "html_error_page.xml", "<!DOCTYPE html>\n<html><head><title>404 Not Found</title></head><body><h1>Not Found</h1></body></html>\n", "invalid", "reject: unsupported format", "Server returned HTML")
w(None, "random_binary.xml", bytes((i * 37 + 11) % 256 for i in range(512)), "corrupted", "reject: not XML", "512 bytes of binary")
w(None, "plain_text.xml", "This is not a feed.\n", "corrupted", "reject: not XML", "")
w(None, "unsupported_rss_0.95.xml", doc("0.94", items_all("0.94"), root_attrs='version="0.95"'), "invalid", "reject: unsupported version", "Between 0.94 and 2.0, not supported")
w(None, "unsupported_rss_1.0.xml", f'{DECL}<rdf:RDF\n  xmlns:rdf="{RDF}"\n  xmlns="http://purl.org/rss/1.0/">\n  <channel rdf:about="https://www.wikipedia.org/">\n    <title>Wikipedia</title>\n    <link>https://www.wikipedia.org/</link>\n    <description>RSS 1.0</description>\n  </channel>\n</rdf:RDF>\n', "invalid", "reject: unsupported version (RSS 1.0 / RDF)", "Unless 1.0 is supported")
w(None, "unsupported_rss_2.1.xml", doc("2.0", items_all("2.0"), root_attrs='version="2.1"'), "invalid", "reject: unsupported version", "Just above 2.0")
w(None, "unsupported_rss_3.0.xml", doc("2.0", items_all("2.0"), root_attrs='version="3.0"'), "invalid", "reject: unsupported version", "")
w(None, "unsupported_rss_0.89.xml", doc("0.91", items_all("0.91"), root_attrs='version="0.89"'), "invalid", "reject: unsupported version", "Version just below supported range")

# README
rows = sorted(manifest, key=lambda r: (r[0].split("/")[0], ["valid", "invalid", "corrupted", "security"].index(r[1]), r[0]))
with open(os.path.join(OUT, "README.md"), "w") as f:
    f.write("# RSS 0.90 – 0.94 & 2.0 import fixtures\n\nGenerated test feeds for the RSS importer. Each version has its own folder; `common/` holds version-agnostic cases.\n\n"
            "Categories: **valid** (should import), **invalid** (well-formed XML, wrong structure/data), **corrupted** (not well-formed / bad bytes), **security** (XXE, entity bombs — must never be expanded or fetched).\n\n"
            "`Expected` is the suggested behaviour; where it says \"or\", pick one and assert it.\n\n")
    cur = None
    for p, cat, exp, note in rows:
        top = p.split("/")[0]
        if top != cur:
            cur = top
            f.write(f"\n## {top}\n\n| File | Category | Expected | Notes |\n|---|---|---|---|\n")
        f.write(f"| `{p.split('/', 1)[1]}` | {cat} | {exp} | {note} |\n")
print(len(manifest), "files")
