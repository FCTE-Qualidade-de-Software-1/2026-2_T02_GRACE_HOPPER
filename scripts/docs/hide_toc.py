"""Hook do MkDocs para preservação de metadados de página (no-op)."""

def on_page_markdown(markdown, page, config, files):
    # O índice lateral direito (TOC) é gerenciado nativamente pelo Material for MkDocs
    # e pode ser ocultado individualmente via frontmatter (ex: hide: - toc em index.md).
    return markdown
