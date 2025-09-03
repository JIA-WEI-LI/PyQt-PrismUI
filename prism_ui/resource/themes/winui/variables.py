from .colors import LightTheme, DarkTheme
from ....utils.theme_manager import Theme

def get_variables(theme: Theme) -> dict:
    colors = DarkTheme if theme == Theme.DARK else LightTheme

    return {
        # Button Background Colors
        '--ThemeColor_Button_Background_Default': colors.ControlFillColorDefaultBrush,
        '--ThemeColor_Button_Background_Hovered': colors.ControlFillColorSecondaryBrush,
        '--ThemeColor_Button_Background_Pressed': colors.ControlFillColorTertiaryBrush,
        '--ThemeColor_Button_Background_Disabled': colors.ControlFillColorDisabledBrush,
        '--ThemeColor_Button_Background_On_Accent_Default': colors.AccentFillColorDefaultBrush,
        '--ThemeColor_Button_Background_On_Accent_Hovered': colors.AccentFillColorSecondaryBrush,
        '--ThemeColor_Button_Background_On_Accent_Pressed': colors.AccentFillColorTertiaryBrush,
        '--ThemeColor_Button_Background_On_Accent_Disabled': colors.AccentFillColorDisabledBrush,

        # Button Text Colors
        '--ThemeColor_Button_Text_Default': colors.TextFillColorPrimaryBrush,
        '--ThemeColor_Button_Text_Hovered': colors.TextFillColorSecondaryBrush,
        '--ThemeColor_Button_Text_Pressed': colors.TextFillColorTertiaryBrush,
        '--ThemeColor_Button_Text_Disabled': colors.TextFillColorDisabledBrush,
        '--ThemeColor_Button_Text_On_Accent_Default': colors.AccentTextFillColorPrimaryBrush,
        '--ThemeColor_Button_Text_On_Accent_Hovered': colors.AccentTextFillColorSecondaryBrush,
        '--ThemeColor_Button_Text_On_Accent_Pressed': colors.TextOnAccentFillColorSecondaryBrush,
        '--ThemeColor_Button_Text_On_Accent_Disabled': colors.AccentTextFillColorDisabledBrush,
        '--ThemeColor_Button_Text_Inverse': colors.TextFillColorInverseBrush,

        # CheckBox Background Colors
        '--ThemeColor_CheckBox_Background_Default': colors.ControlFillColorDefaultBrush,
        '--ThemeColor_CheckBox_Background_Hovered': colors.ControlFillColorSecondaryBrush,
        '--ThemeColor_CheckBox_Background_Pressed': colors.ControlFillColorTertiaryBrush,
        '--ThemeColor_CheckBox_Background_Disabled': colors.ControlFillColorDisabledBrush,
        '--ThemeColor_CheckBox_Background_On_Accent_Default': colors.AccentFillColorDefaultBrush,
        '--ThemeColor_CheckBox_Background_On_Accent_Hovered': colors.AccentFillColorSecondaryBrush,
        '--ThemeColor_CheckBox_Background_On_Accent_Pressed': colors.AccentFillColorTertiaryBrush,
        '--ThemeColor_CheckBox_Background_On_Accent_Disabled': colors.AccentFillColorDisabledBrush,

        # CheckBox Text Colors
        '--ThemeColor_CheckBox_Text_Default': colors.TextFillColorPrimaryBrush,
        '--ThemeColor_CheckBox_Text_Hovered': colors.TextFillColorSecondaryBrush,
        '--ThemeColor_CheckBox_Text_Pressed': colors.TextFillColorTertiaryBrush,
        '--ThemeColor_CheckBox_Text_Disabled': colors.TextFillColorDisabledBrush,
        '--ThemeColor_CheckBox_Text_On_Accent_Default': colors.AccentTextFillColorPrimaryBrush,
        '--ThemeColor_CheckBox_Text_On_Accent_Hovered': colors.AccentTextFillColorSecondaryBrush,
        '--ThemeColor_CheckBox_Text_On_Accent_Pressed': colors.TextOnAccentFillColorSecondaryBrush,
        '--ThemeColor_CheckBox_Text_On_Accent_Disabled': colors.AccentTextFillColorDisabledBrush,

        # TODO: Delete and rename into normal
        # Text Colors
        '--ThemeColor_Text_Default': colors.TextFillColorPrimaryBrush,
        '--ThemeColor_Text_Secondary': colors.TextFillColorSecondaryBrush,
        '--ThemeColor_Text_Tertiary': colors.TextFillColorTertiaryBrush,
        '--ThemeColor_Text_Disabled': colors.TextFillColorDisabledBrush,
        '--ThemeColor_Text_Inverse': colors.TextFillColorInverseBrush,
        '--ThemeColor_Text_Accent_Default': colors.AccentTextFillColorPrimaryBrush,
        '--ThemeColor_Text_Accent_Primary': colors.AccentTextFillColorPrimaryBrush,
        '--ThemeColor_Text_Accent_Secondary': colors.AccentTextFillColorSecondaryBrush,
        '--ThemeColor_Text_Accent_Tertiary': colors.AccentTextFillColorTertiaryBrush,
        '--ThemeColor_Text_Accent_Disabled': colors.AccentTextFillColorDisabledBrush,
        '--ThemeColor_Text_On_Accent_Default': colors.TextOnAccentFillColorPrimaryBrush,
        '--ThemeColor_Text_On_Accent_Secondary': colors.TextOnAccentFillColorSecondaryBrush,
        '--ThemeColor_Text_On_Accent_Disabled': colors.TextOnAccentFillColorDisabledBrush,
        '--ThemeColor_Text_On_Accent_SelectedText': colors.TextOnAccentFillColorSelectedTextBrush,

        # Fill Colors
        '--ThemeColor_Control_Default': colors.ControlFillColorDefaultBrush,
        '--ThemeColor_Control_Secondary': colors.ControlFillColorSecondaryBrush,
        '--ThemeColor_Control_Tertiary': colors.ControlFillColorTertiaryBrush,
        '--ThemeColor_Control_Disabled': colors.ControlFillColorDisabledBrush,
        '--ThemeColor_Control_Transparent': colors.ControlFillColorTransparentBrush,
        '--ThemeColor_Control_InputActive': colors.ControlFillColorInputActiveBrush,
        '--ThemeColor_Control_Solid_Default': colors.ControlSolidFillColorDefaultBrush,
        '--ThemeColor_Control_Strong_Default': colors.ControlStrongFillColorDefaultBrush,
        '--ThemeColor_Control_Strong_Disabled': colors.ControlStrongFillColorDisabledBrush,

        # Subtle Fill Colors
        '--ThemeColor_Subtle_Transparent': colors.SubtleFillColorTransparentBrush,
        '--ThemeColor_Subtle_Secondary': colors.SubtleFillColorSecondaryBrush,
        '--ThemeColor_Subtle_Tertiary': colors.SubtleFillColorTertiaryBrush,
        '--ThemeColor_Subtle_Disabled': colors.SubtleFillColorDisabledBrush,

        # Control Alt Fill Colors
        '--ThemeColor_ControlAlt_Transparent': colors.ControlAltFillColorTransparentBrush,
        '--ThemeColor_ControlAlt_Secondary': colors.ControlAltFillColorSecondaryBrush,
        '--ThemeColor_ControlAlt_Tertiary': colors.ControlAltFillColorTertiaryBrush,
        '--ThemeColor_ControlAlt_Quarternary': colors.ControlAltFillColorQuarternaryBrush,
        '--ThemeColor_ControlAlt_Disabled': colors.ControlAltFillColorDisabledBrush,

        # Control On Image Fill Colors
        '--ThemeColor_ControlOnImage_Default': colors.ControlOnImageFillColorDefaultBrush,
        '--ThemeColor_ControlOnImage_Secondary': colors.ControlOnImageFillColorSecondaryBrush,
        '--ThemeColor_ControlOnImage_Tertiary': colors.ControlOnImageFillColorTertiaryBrush,
        '--ThemeColor_ControlOnImage_Disabled': colors.ControlOnImageFillColorDisabledBrush,

        # Accent Fill Colors
        '--ThemeColor_Accent_Default': colors.AccentFillColorDefaultBrush,
        '--ThemeColor_Accent_Secondary': colors.AccentFillColorSecondaryBrush,
        '--ThemeColor_Accent_Tertiary': colors.AccentFillColorTertiaryBrush,
        '--ThemeColor_Accent_Disabled': colors.AccentFillColorDisabledBrush,
        '--ThemeColor_Accent_SelectedTextBackground': colors.AccentFillColorSelectedTextBackgroundBrush,

        # Stroke Colors
        '--ThemeColor_Card_Stroke_Default': colors.CardStrokeColorDefaultBrush,
        '--ThemeColor_Card_Stroke_Solid': colors.CardStrokeColorDefaultSolidBrush,
        '--ThemeColor_Control_Stroke_Default': colors.ControlStrokeColorDefaultBrush,
        '--ThemeColor_Control_Stroke_Secondary': colors.ControlStrokeColorSecondaryBrush,
        '--ThemeColor_Control_On_Accent_Stroke_Default': colors.ControlStrokeColorOnAccentDefaultBrush,
        '--ThemeColor_Control_On_Accent_Stroke_Secondary': colors.ControlStrokeColorOnAccentSecondaryBrush,
        '--ThemeColor_Control_On_Accent_Stroke_Tertiary': colors.ControlStrokeColorOnAccentTertiaryBrush,
        '--ThemeColor_Control_On_Accent_Stroke_Disabled': colors.ControlStrokeColorOnAccentDisabledBrush,
        '--ThemeColor_Control_StrongFillOnImage_Stroke': colors.ControlStrokeColorForStrongFillWhenOnImageBrush,
        '--ThemeColor_Control_Strong_Stroke_Default': colors.ControlStrongStrokeColorDefaultBrush,
        '--ThemeColor_Control_Strong_Stroke_Disabled': colors.ControlStrongStrokeColorDisabledBrush,
        '--ThemeColor_Surface_Stroke_Default': colors.SurfaceStrokeColorDefaultBrush,
        '--ThemeColor_Surface_Stroke_Flyout': colors.SurfaceStrokeColorFlyoutBrush,
        '--ThemeColor_Surface_Stroke_Inverse': colors.SurfaceStrokeColorInverseBrush,
        '--ThemeColor_Divider_Stroke_Default': colors.DividerStrokeColorDefaultBrush,
        '--ThemeColor_Focus_Stroke_Outer': colors.FocusStrokeColorOuterBrush,
        '--ThemeColor_Focus_Stroke_Inner': colors.FocusStrokeColorInnerBrush,

        # Background / Layer Colors
        '--ThemeColor_CardBackground_Default': colors.CardBackgroundFillColorDefaultBrush,
        '--ThemeColor_CardBackground_Secondary': colors.CardBackgroundFillColorSecondaryBrush,
        '--ThemeColor_Smoke_Default': colors.SmokeFillColorDefaultBrush,
        '--ThemeColor_Layer_Default': colors.LayerFillColorDefaultBrush,
        '--ThemeColor_Layer_Alt': colors.LayerFillColorAltBrush,
        '--ThemeColor_LayerOnAcrylic_Default': colors.LayerOnAcrylicFillColorDefaultBrush,
        '--ThemeColor_Layer_On_AccentAcrylic_Default': colors.LayerOnAccentAcrylicFillColorDefaultBrush,
        '--ThemeColor_LayerOnMicaBaseAlt_Default': colors.LayerOnMicaBaseAltFillColorDefaultBrush,
        '--ThemeColor_LayerOnMicaBaseAlt_Secondary': colors.LayerOnMicaBaseAltFillColorSecondaryBrush,
        '--ThemeColor_LayerOnMicaBaseAlt_Tertiary': colors.LayerOnMicaBaseAltFillColorTertiaryBrush,
        '--ThemeColor_LayerOnMicaBaseAlt_Transparent': colors.LayerOnMicaBaseAltFillColorTransparentBrush,

        # Solid Background Colors
        '--ThemeColor_SolidBackground_Base': colors.SolidBackgroundFillColorBaseBrush,
        '--ThemeColor_SolidBackground_Secondary': colors.SolidBackgroundFillColorSecondaryBrush,
        '--ThemeColor_SolidBackground_Tertiary': colors.SolidBackgroundFillColorTertiaryBrush,
        '--ThemeColor_SolidBackground_Quarternary': colors.SolidBackgroundFillColorQuarternaryBrush,
        '--ThemeColor_SolidBackground_BaseAlt': colors.SolidBackgroundFillColorBaseAltBrush,

        # System Fill Colors
        '--ThemeColor_System_Success': colors.SystemFillColorSuccessBrush,
        '--ThemeColor_System_Caution': colors.SystemFillColorCautionBrush,
        '--ThemeColor_System_Critical': colors.SystemFillColorCriticalBrush,
        '--ThemeColor_System_Neutral': colors.SystemFillColorNeutralBrush,
        '--ThemeColor_System_SolidNeutral': colors.SystemFillColorSolidNeutralBrush,
        '--ThemeColor_System_AttentionBackground': colors.SystemFillColorAttentionBackgroundBrush,
        '--ThemeColor_System_SuccessBackground': colors.SystemFillColorSuccessBackgroundBrush,
        '--ThemeColor_System_CautionBackground': colors.SystemFillColorCautionBackgroundBrush,
        '--ThemeColor_System_CriticalBackground': colors.SystemFillColorCriticalBackgroundBrush,
        '--ThemeColor_System_NeutralBackground': colors.SystemFillColorNeutralBackgroundBrush,
        '--ThemeColor_System_SolidAttentionBackground': colors.SystemFillColorSolidAttentionBackgroundBrush,
        '--ThemeColor_System_SolidNeutralBackground': colors.SystemFillColorSolidNeutralBackgroundBrush,

        # Temporary System Colors
        '--ThemeColor_System_WindowText': colors.SystemColorWindowTextColorBrush,
        '--ThemeColor_System_Window': colors.SystemColorWindowColorBrush,
        '--ThemeColor_System_ButtonFace': colors.SystemColorButtonFaceColorBrush,
        '--ThemeColor_System_ButtonText': colors.SystemColorButtonTextColorBrush,
        '--ThemeColor_System_Highlight': colors.SystemColorHighlightColorBrush,
        '--ThemeColor_System_HighlightText': colors.SystemColorHighlightTextColorBrush,
        '--ThemeColor_System_Hotlight': colors.SystemColorHotlightColorBrush,
        '--ThemeColor_System_GrayText': colors.SystemColorGrayTextColorBrush,
    }
