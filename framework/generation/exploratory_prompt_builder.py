

def build_exploratory_prompt(requirement: str, strategy: dict, themes: list) -> str:

    focus_areas = "\n".join(
        f"- {area}"
        for area in strategy["focus_areas"]
    )

    exploratory_themes = "\n".join(
        f"- {theme}"
        for theme in themes
    )

    return f"""
Requirement:
{requirement}

Domain:
{strategy["domain"]}

Focus Areas:
{focus_areas}

Exploratory Themes:
{exploratory_themes}
"""