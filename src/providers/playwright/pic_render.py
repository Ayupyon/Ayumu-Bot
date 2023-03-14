from io import BytesIO

from jinja2 import Environment, FileSystemLoader

from src.providers.pathutil import resource_path
from src.providers.playwright import get_new_page


async def template_to_html(template_name: str, **kwargs) -> str:
    env = Environment(
        loader=FileSystemLoader(str(resource_path(""))),
        enable_async=True,
    )
    template = env.get_template(template_name)
    return await template.render_async(**kwargs)


async def render(template_name: str, **kwargs) -> BytesIO:
    html = await template_to_html(template_name, **kwargs)
    path = resource_path(template_name)
    async with get_new_page() as page:
        await page.goto(f"file://{str(path)}")
        await page.set_content(html, wait_until="networkidle")
        return BytesIO(await page.locator("css=#main").screenshot())