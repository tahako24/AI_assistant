def route(text: str) -> str:
    text = text.lower()

    local_keywords = [
        # общее
        "открой",
        "запусти",

        # браузеры
        "открой браузер",
        "открой chrome",
        "открой хром",
        "запусти chrome",
        "запусти хром",

        # discord
        "открой дискорд",
        "открой discord",
        "запусти дискорд",
        "запусти discord",

        # figma
        "открой figma",
        "открой фигма",
        "запусти figma",
        "запусти фигма",

        # steam
        "открой steam",
        "открой стим",
        "запусти steam",
        "запусти стим",

        # visual studio
        "открой visual studio",
        "открой visual studio 2022",
        "открой студию",
        "запусти visual studio",
        "запусти visual studio 2022",

        # nvidia
        "открой nvidia",
        "открой nvidia app",
        "открой нвидиа",
        "запусти nvidia",
        "запусти nvidia app",

        # minecraft / legacy launcher
        "открой minecraft",
        "открой майнкрафт",
        "запусти minecraft",
        "запусти майнкрафт",
        "открой legacy launcher",
        "запусти legacy launcher",
    ]

    for word in local_keywords:
        if word in text:
            return "local"

    return "api"
