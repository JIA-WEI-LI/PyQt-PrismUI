import logging
logger = logging.getLogger(__name__)

class ColorsMeta(type):
    required_attrs = [
        # Text Colors
        "TextFillColorPrimaryBrush",
        "TextFillColorSecondaryBrush",
        "TextFillColorTertiaryBrush",
        "TextFillColorDisabledBrush",
        "TextFillColorInverseBrush",
        "AccentTextFillColorSecondaryBrush",
        "AccentTextFillColorTertiaryBrush",
        "AccentTextFillColorDisabledBrush",
        "TextOnAccentFillColorPrimaryBrush",
        "TextOnAccentFillColorSecondaryBrush",
        "TextOnAccentFillColorDisabledBrush",
        "TextOnAccentFillColorSelectedTextBrush",

        # Fill Colors
        "ControlFillColorDefaultBrush",
        "ControlFillColorSecondaryBrush",
        "ControlFillColorTertiaryBrush",
        "ControlFillColorDisabledBrush",
        "ControlFillColorTransparentBrush",
        "ControlFillColorInputActiveBrush",
        "ControlAltFillColorTransparentBrush",
        "ControlAltFillColorSecondaryBrush",
        "ControlAltFillColorTertiaryBrush",
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

        # Accent Fill Colors
        "AccentFillColorDisabledBrush",
        "AccentFillColorSelectedTextBackgroundBrush",
        "AccentTextFillColorPrimaryBrush",
        "AccentFillColorDefaultBrush",
        "AccentFillColorSecondaryBrush",
        "AccentFillColorTertiaryBrush",

        # Stroke Colors
        "CardStrokeColorDefaultBrush",
        "CardStrokeColorDefaultSolidBrush",
        "ControlStrokeColorDefaultBrush",
        "ControlStrokeColorSecondaryBrush",
        "ControlStrokeColorOnAccentDefaultBrush",
        "ControlStrokeColorOnAccentSecondaryBrush",
        "ControlStrokeColorOnAccentTertiaryBrush",
        "ControlStrokeColorOnAccentDisabledBrush",
        "ControlStrokeColorForStrongFillWhenOnImageBrush",
        "ControlStrongStrokeColorDefaultBrush",
        "ControlStrongStrokeColorDisabledBrush",
        "SurfaceStrokeColorDefaultBrush",
        "SurfaceStrokeColorFlyoutBrush",
        "SurfaceStrokeColorInverseBrush",
        "DividerStrokeColorDefaultBrush",
        "FocusStrokeColorOuterBrush",
        "FocusStrokeColorInnerBrush",

        # Background / Layer Colors
        "CardBackgroundFillColorDefaultBrush",
        "CardBackgroundFillColorSecondaryBrush",
        "SmokeFillColorDefaultBrush",
        "LayerFillColorDefaultBrush",
        "LayerFillColorAltBrush",
        "LayerOnAcrylicFillColorDefaultBrush",
        "LayerOnAccentAcrylicFillColorDefaultBrush",
        "LayerOnMicaBaseAltFillColorDefaultBrush",
        "LayerOnMicaBaseAltFillColorSecondaryBrush",
        "LayerOnMicaBaseAltFillColorTertiaryBrush",
        "LayerOnMicaBaseAltFillColorTransparentBrush",

        # Solid Background Colors
        "SolidBackgroundFillColorBaseBrush",
        "SolidBackgroundFillColorSecondaryBrush",
        "SolidBackgroundFillColorTertiaryBrush",
        "SolidBackgroundFillColorQuarternaryBrush",
        "SolidBackgroundFillColorBaseAltBrush",

        # System Fill Colors
        "SystemFillColorSuccessBrush",
        "SystemFillColorCautionBrush",
        "SystemFillColorCriticalBrush",
        "SystemFillColorNeutralBrush",
        "SystemFillColorSolidNeutralBrush",
        "SystemFillColorAttentionBackgroundBrush",
        "SystemFillColorSuccessBackgroundBrush",
        "SystemFillColorCautionBackgroundBrush",
        "SystemFillColorCriticalBackgroundBrush",
        "SystemFillColorNeutralBackgroundBrush",
        "SystemFillColorSolidAttentionBackgroundBrush",
        "SystemFillColorSolidNeutralBackgroundBrush",

        # Temporary System Colors
        "SystemColorWindowTextColorBrush",
        "SystemColorWindowColorBrush",
        "SystemColorButtonFaceColorBrush",
        "SystemColorButtonTextColorBrush",
        "SystemColorHighlightColorBrush",
        "SystemColorHighlightTextColorBrush",
        "SystemColorHotlightColorBrush",
        "SystemColorGrayTextColorBrush"
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
    # Text Colors
    TextFillColorPrimaryBrush = ""
    TextFillColorSecondaryBrush = ""
    TextFillColorTertiaryBrush = ""
    TextFillColorDisabledBrush = ""
    TextFillColorInverseBrush = ""
    # AccentTextFillColorPrimaryBrush = ""
    AccentTextFillColorSecondaryBrush = ""
    AccentTextFillColorTertiaryBrush = ""
    AccentTextFillColorDisabledBrush = ""
    TextOnAccentFillColorPrimaryBrush = ""
    # TextOnAccentFillColorSecondaryBrush = ""
    TextOnAccentFillColorDisabledBrush = ""
    TextOnAccentFillColorSelectedTextBrush = ""

    # Fill Colors
    ControlFillColorDefaultBrush = ""
    ControlFillColorSecondaryBrush = ""
    ControlFillColorTertiaryBrush = ""
    ControlFillColorDisabledBrush = ""
    ControlFillColorTransparentBrush = ""
    ControlFillColorInputActiveBrush = ""
    ControlAltFillColorTransparentBrush = ""
    ControlAltFillColorSecondaryBrush = ""
    ControlAltFillColorTertiaryBrush = ""
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
    
    # Accent Fill Colors
    AccentFillColorDisabledBrush = ""
    AccentFillColorSelectedTextBackgroundBrush = ""
    AccentFillColorDefaultBrush = ""
    AccentFillColorSecondaryBrush = ""
    AccentFillColorTertiaryBrush = ""

    # Stroke Colors
    CardStrokeColorDefaultBrush = ""
    CardStrokeColorDefaultSolidBrush = ""
    ControlStrokeColorDefaultBrush = ""
    ControlStrokeColorSecondaryBrush = ""
    ControlStrokeColorOnAccentDefaultBrush = ""
    ControlStrokeColorOnAccentSecondaryBrush = ""
    ControlStrokeColorOnAccentTertiaryBrush = ""
    ControlStrokeColorOnAccentDisabledBrush = ""
    ControlStrokeColorForStrongFillWhenOnImageBrush = ""
    ControlStrongStrokeColorDefaultBrush = ""
    ControlStrongStrokeColorDisabledBrush = ""
    SurfaceStrokeColorDefaultBrush = ""
    SurfaceStrokeColorFlyoutBrush = ""
    SurfaceStrokeColorInverseBrush = ""
    DividerStrokeColorDefaultBrush = ""
    FocusStrokeColorOuterBrush = ""
    FocusStrokeColorInnerBrush = ""

    # Background / Layer Colors
    CardBackgroundFillColorDefaultBrush = ""
    CardBackgroundFillColorSecondaryBrush = ""
    SmokeFillColorDefaultBrush = ""
    LayerFillColorDefaultBrush = ""
    LayerFillColorAltBrush = ""
    LayerOnAcrylicFillColorDefaultBrush = ""
    LayerOnAccentAcrylicFillColorDefaultBrush = ""
    LayerOnMicaBaseAltFillColorDefaultBrush = ""
    LayerOnMicaBaseAltFillColorSecondaryBrush = ""
    LayerOnMicaBaseAltFillColorTertiaryBrush = ""
    LayerOnMicaBaseAltFillColorTransparentBrush = ""

    # Solid Background Colors
    SolidBackgroundFillColorBaseBrush = ""
    SolidBackgroundFillColorSecondaryBrush = ""
    SolidBackgroundFillColorTertiaryBrush = ""
    SolidBackgroundFillColorQuarternaryBrush = ""
    SolidBackgroundFillColorBaseAltBrush = ""

    # System Fill Colors
    SystemFillColorSuccessBrush = ""
    SystemFillColorCautionBrush = ""
    SystemFillColorCriticalBrush = ""
    SystemFillColorNeutralBrush = ""
    SystemFillColorSolidNeutralBrush = ""
    SystemFillColorAttentionBackgroundBrush = ""
    SystemFillColorSuccessBackgroundBrush = ""
    SystemFillColorCautionBackgroundBrush = ""
    SystemFillColorCriticalBackgroundBrush = ""
    SystemFillColorNeutralBackgroundBrush = ""
    SystemFillColorSolidAttentionBackgroundBrush = ""
    SystemFillColorSolidNeutralBackgroundBrush = ""

    # Temporary System Colors
    SystemColorWindowTextColorBrush = ""
    SystemColorWindowColorBrush = ""
    SystemColorButtonFaceColorBrush = ""
    SystemColorButtonTextColorBrush = ""
    SystemColorHighlightColorBrush = ""
    SystemColorHighlightTextColorBrush = ""
    SystemColorHotlightColorBrush = ""
    SystemColorGrayTextColorBrush = ""