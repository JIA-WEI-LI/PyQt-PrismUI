class BaseTheme:
    TextFontFamily = ("Segoe UI", "Microsoft YaHei", "PingFang SC", "Helvetica", "Arial", "sans-serif")

    TextFontWeightNormal = "Normal"
    TextFontWeightBold = 'Bold'

    CaptionTextBlockSize = 12
    BodyTextBlockSize = 14
    BodyStrongTextBlockSize = 14
    SubtitleTextBlockSize = 20
    TitleTextBlockSize = 28
    TitleLargeTextBlockSize = 40
    DisplayTextBlockSize = 68

class LightTheme(BaseTheme):
    pass

class DarkTheme(BaseTheme):
    pass