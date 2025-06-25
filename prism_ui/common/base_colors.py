import logging
logger = logging.getLogger(__name__)

class ColorsMeta(type):
    required_attrs = [
        # Text type Color
        "TextFillColorPrimaryBrush",
        "TextFillColorSecondaryBrush",
        "TextFillColorTertiaryBrush",
        "TextFillColorDisabledBrush",
        "AccentTextFillColorPrimaryBrush",
        "AccentTextFillColorSecondaryBrush",
        "AccentTextFillColorTertiaryBrush",
        "AccentTextFillColorDisabledBrush",
        "TextOnAccentFillColorPrimaryBrush",
        "TextOnAccentFillColorSecondaryBrush",
        "TextOnAccentFillColorDisabledBrush",
        "TextOnAccentFillColorSelectedTextBrush",
        # Fill type Color
        "ControlFillColorDefaultBrush",
        "ControlFillColorSecondaryBrush",
        "ControlFillColorTertiaryBrush",
        "ControlFillColorQuarternaryBrush",
        "ControlFillColorDisabledBrush",
        "ControlFillColorTransparentBrush",
        "ControlFillColorInputActiveBrush",
        "ControlAltFillColorTransparentBrush",
        "ControlAltFillColorSecondaryBrush",
        "ControlAltFillColorTertiaryBrush",
        "ControlAltFillColorQuarternaryBrush",
        "ControlAltFillColorDisabledBrush",
        "ControlSolidFillColorDefaultBrush",
        "ControlStrongFillColorDefaultBrush",
        "ControlStrongFillColorDisabledBrush",
        "SubtleFillColorTransparentBrush",
        "SubtleFillColorSecondaryBrush",
        "SubtleFillColorTertiaryBrush",
        "SubtleFillColorDisabledBrush",
        "ControlOnImageFillColorDefaultBrush",
        "ControlOnImageFillColorSecondaryBrush",
        "ControlOnImageFillColorTertiaryBrush",
        "ControlOnImageFillColorDisabledBrush",
        "AccentFillColorDefaultBrush",
        "AccentFillColorSecondaryBrush",
        "AccentFillColorTertiaryBrush",
        "AccentFillColorDisabledBrush",
        "AccentFillColorSelectedTextBackgroundBrush",
    ]

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)

        if name != "BaseColors":
            for attr in mcs.required_attrs:
                if not hasattr(cls, attr):
                    logger.warning(f"[{name}] Missing required color attribute: {attr}")
                else:
                    val = getattr(cls, attr)
                    if not isinstance(val, str) or not val.strip():
                        logger.warning(f"[{name}] Attribute {attr} should be a non-empty string")
        return cls


class BaseColors(metaclass=ColorsMeta):
    TextFillColorPrimaryBrush = ""
    TextFillColorSecondaryBrush = ""
    TextFillColorTertiaryBrush = ""
    TextFillColorDisabledBrush = ""
    AccentTextFillColorPrimaryBrush = ""
    AccentTextFillColorSecondaryBrush = ""
    AccentTextFillColorTertiaryBrush = ""
    AccentTextFillColorDisabledBrush = ""
    TextOnAccentFillColorPrimaryBrush = ""
    TextOnAccentFillColorSecondaryBrush = ""
    TextOnAccentFillColorDisabledBrush = ""
    TextOnAccentFillColorSelectedTextBrush = ""
    ControlFillColorDefaultBrush = ""
    ControlFillColorSecondaryBrush = ""
    ControlFillColorTertiaryBrush = ""
    ControlFillColorQuarternaryBrush = ""
    ControlFillColorDisabledBrush = ""
    ControlFillColorTransparentBrush = ""
    ControlFillColorInputActiveBrush = ""
    ControlAltFillColorTransparentBrush = ""
    ControlAltFillColorSecondaryBrush = ""
    ControlAltFillColorTertiaryBrush = ""
    ControlAltFillColorQuarternaryBrush = ""
    ControlAltFillColorDisabledBrush = ""
    ControlSolidFillColorDefaultBrush = ""
    ControlStrongFillColorDefaultBrush = ""
    ControlStrongFillColorDisabledBrush = ""
    SubtleFillColorTransparentBrush = ""
    SubtleFillColorSecondaryBrush = ""
    SubtleFillColorTertiaryBrush = ""
    SubtleFillColorDisabledBrush = ""
    ControlOnImageFillColorDefaultBrush = ""
    ControlOnImageFillColorSecondaryBrush = ""
    ControlOnImageFillColorTertiaryBrush = ""
    ControlOnImageFillColorDisabledBrush = ""
    AccentFillColorDefaultBrush = ""
    AccentFillColorSecondaryBrush = ""
    AccentFillColorTertiaryBrush = ""
    AccentFillColorDisabledBrush = ""
    AccentFillColorSelectedTextBackgroundBrush = ""
