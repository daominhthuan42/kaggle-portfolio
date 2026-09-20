from pathlib import Path
from playwright.sync_api import sync_playwright


def html_to_pdf(
    html_path: str | Path,
    pdf_path: str | Path,
) -> None:
    """
    Convert a Jupyter/JupyterLab exported HTML file to PDF.

    Parameters
    ----------
    html_path : str | Path
        Path to the input HTML file.
    pdf_path : str | Path
        Path to the output PDF file.
    """

    html_path = Path(html_path).resolve()
    pdf_path = Path(pdf_path).resolve()

    if not html_path.exists():
        raise FileNotFoundError(f"HTML file not found: {html_path}")

    pdf_path.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page(
            viewport={
                "width": 1440,
                "height": 900,
            },
            device_scale_factor=1,
        )

        # --------------------------------------------------------
        # Load HTML
        # --------------------------------------------------------

        page.goto(
            html_path.as_uri(),
            wait_until="load",
        )

        # Wait for fonts and images to finish loading.
        page.evaluate("""
            async () => {
                if (document.fonts) {
                    await document.fonts.ready;
                }

                const images = Array.from(document.images);

                await Promise.all(
                    images.map(img => {
                        if (img.complete) {
                            return Promise.resolve();
                        }

                        return new Promise(resolve => {
                            img.addEventListener("load", resolve);
                            img.addEventListener("error", resolve);
                        });
                    })
                );
            }
        """)

        # --------------------------------------------------------
        # Print-specific CSS
        # --------------------------------------------------------

        page.add_style_tag(content="""
            /* ====================================================
               PDF PRINT SETTINGS
               ==================================================== */

            @page {
                size: A4;
                margin: 12mm 12mm 14mm 12mm;
            }

            html,
            body {
                width: 100%;
                margin: 0 !important;
                padding: 0 !important;
            }

            /* Main notebook container */
            .jp-Notebook {
                width: 100% !important;
                max-width: none !important;
                margin: 0 !important;
                padding: 0 !important;
            }

            /* Remove notebook UI elements */
            .jp-InputPrompt,
            .jp-OutputPrompt,
            .jp-Collapser {
                display: none !important;
            }

            /* Make notebook content use the full page width */
            .jp-Cell {
                max-width: none !important;
            }

            .jp-RenderedHTMLCommon,
            .jp-RenderedMarkdown {
                max-width: none !important;
            }

            /* Keep headings together with following content */
            h1,
            h2,
            h3,
            h4 {
                break-after: avoid-page;
                page-break-after: avoid;
            }

            /* Avoid splitting important blocks */
            .jp-MarkdownCell {
                break-inside: avoid;
            }

            /* Tables */
            table {
                max-width: 100% !important;
                width: auto;
                break-inside: auto;
            }

            tr {
                break-inside: avoid;
                page-break-inside: avoid;
            }

            /* Images / charts */
            img {
                max-width: 100% !important;
                height: auto !important;
                break-inside: avoid;
                page-break-inside: avoid;
            }

            figure {
                max-width: 100% !important;
                break-inside: avoid;
                page-break-inside: avoid;
            }

            /* Code blocks */
            pre {
                white-space: pre-wrap !important;
                word-break: break-word !important;
                overflow-wrap: anywhere !important;
            }

            /* Links */
            a {
                color: inherit !important;
                text-decoration: none !important;
            }

            /* Remove notebook anchors such as "¶" */
            .anchor-link {
                display: none !important;
            }

            /* Prevent horizontal overflow */
            * {
                box-sizing: border-box;
            }
        """)

        # --------------------------------------------------------
        # Generate PDF
        # --------------------------------------------------------

        page.pdf(
            path=str(pdf_path),
            format="A4",
            print_background=True,
            prefer_css_page_size=True,
            margin={
                "top": "12mm",
                "right": "12mm",
                "bottom": "14mm",
                "left": "12mm",
            },
        )

        browser.close()


if __name__ == "__main__":

    html_to_pdf(
        html_path="D:/02_DATA/00_kaggle-portfolio/50-predicting-electric-vehicle-purchases/notebook/predicting-electric-vehicle-full-eda.html",
        pdf_path="D:/02_DATA/00_kaggle-portfolio/50-predicting-electric-vehicle-purchases/notebook/predicting-electric-vehicle-full-eda.pdf",
    )
