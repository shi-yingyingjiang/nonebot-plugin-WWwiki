from jinja2 import Template



def Get_html(data: str):
    template = Template("{{ content }}")
    rendered = template.render(content=data)
    return rendered