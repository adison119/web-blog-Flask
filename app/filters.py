from markupsafe import Markup, escape
import markdown as md
import bleach
def nl2br(value):
    return Markup('<br>'.join(escape(value).splitlines()))

def render_markdown(value: str):
    html = md.markdown(value or "", extensions=["extra", "sane_lists", "codehilite"])
    allowed_tags = set(bleach.sanitizer.ALLOWED_TAGS) | {
        "p","br","pre","code","blockquote",
        "ul","ol","li",
        "h1","h2","h3","h4","h5","h6",
        "strong","em","a","img"
    }
    allowed_attrs = {
        "a": ["href","title","rel","target"],
        "img": ["src","alt","title","loading"]
    }
    clean = bleach.clean(html, tags=allowed_tags, attributes=allowed_attrs, strip=True)
    return Markup(clean)