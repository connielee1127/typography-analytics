from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

async def load_page(url):
    """
    Load a webpage and collect typographic data from visible text elements.
    """

    result = {
            "url": url,
            "scrape_status": None,
            "failure_reason":None,
            "elements": []
    }
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        try:
            await page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=10000
            )

            elements = await page.locator(
                "h1, h2, h3, p, div, span"
            ).all()

            for i, element in enumerate(elements):
                data = await element.evaluate("""
                    element => {
                        const style = getComputedStyle(element);
                        const rect = element.getBoundingClientRect();
                                              
                        const directText = Array.from(element.childNodes)
                            .filter(node => node.nodeType === Node.TEXT_NODE)
                            .map(node => node.textContent.trim())
                            .filter(text => text.length > 0)
                            .join(" ");
                                                    
                        return {
                            tag: element.tagName.toLowerCase(),
                            text: directText,
                            text_length: directText.length,

                            x: rect.x,
                            y: rect.y,
                            width: rect.width,
                            height: rect.height,
                                              
                            font_family: style.fontFamily,
                            font_size: style.fontSize,
                            font_weight: style.fontWeight,
                            line_height: style.lineHeight,
                            letter_spacing: style.letterSpacing,
                            text_transform: style.textTransform,
                            text_align: style.textAlign,
                                              
                            visible:
                                rect.width > 0 &&
                                rect.height > 0 &&
                                style.visibility !== "hidden" &&
                                style.display !== "none"
                        };
                    }
                """)

                if data["visible"] and data["text"]:
                    data["element_index"] = i
                    result["elements"].append(data)

            result["scrape_status"] = "success" 
            return result
        
        except PlaywrightTimeoutError:
            result["scrape_status"] = "failed"
            result["failure_reason"] = "timeout"
            return result
             
        except Exception as e:
            print(type(e).__name__)
            print(e)
            result["scrape_status"] = "failed"
            result["failure_reason"] = type(e).__name__
            return result
            
         
        finally:
            await browser.close()




