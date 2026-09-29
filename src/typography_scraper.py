from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

async def load_page(url):
    """
    Load a webpage and extract typography properties from its first H1.
    """

    result = {
            "url": url,
            "font_family": None,
            "font_size": None,
            "font_weight": None,
            "line_height": None,
            "scrape_status": None,
            "failure_reason":None
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

            heading = await page.query_selector("h1")

            if heading is None:
                result["scrape_status"] = "failed"
                result["failure_reason"] = "no_h1"
                return result
            
            typography = await heading.evaluate("""
                element => {
                    const style = getComputedStyle(element);
                                                
                    return {
                        font_family: style.fontFamily,
                        font_size: style.fontSize,
                        font_weight: style.fontWeight,
                        line_height: style.lineHeight
                    };
                }
            """)

            result.update(typography)
            result["scrape_status"] = "success" 
            return result
        
        except PlaywrightTimeoutError:
            result["scrape_status"] = "failed"
            result["failure_reason"] = "timeout"
            return result
             
        except Exception as e:
            result["scrape_status"] = "failed"
            result["failure_reason"] = type(e).__name__
            return result
            
         
        finally:
            await browser.close()




