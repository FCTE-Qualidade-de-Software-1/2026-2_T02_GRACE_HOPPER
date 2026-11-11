"""Hook do MkDocs para ocultar o índice lateral direito (TOC) em todas as páginas."""

def on_page_markdown(markdown, page, config, files):
    if not hasattr(page, "meta") or page.meta is None:
        page.meta = {}
    hide = page.meta.get("hide", [])
    if isinstance(hide, list):
        if "toc" not in hide:
            hide.append("toc")
        page.meta["hide"] = hide
    elif isinstance(hide, str):
        page.meta["hide"] = [hide, "toc"]
    return markdown
