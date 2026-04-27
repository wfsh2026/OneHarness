---
name: ui-settings
display_name: 设置系统界面
category: ui
version: 1.0.0
dependencies: [ui-framework]
---

# 设置系统界面

游戏设置UI系统。UserSettings(33文件)管理画质/操作/音频设置，NewUserSetting(31文件)管理新版设置界面重构，PC(11文件)适配PC端键鼠操作，Graphic(4文件)管理画质预设，ServerList管理服务器选择。

## 代码文件

| 路径 |
|------|
| `Assets/Script/UI/UserSettings/AudioQualityButton.cs` |
| `Assets/Script/UI/UserSettings/DropdownColor.cs` |
| `Assets/Script/UI/UserSettings/GamepadInputCompositeGroup.cs` |
| `Assets/Script/UI/UserSettings/GamepadInputCompositeItem.cs` |
| `Assets/Script/UI/UserSettings/LeftUpFireExplainView.cs` |
| `Assets/Script/UI/UserSettings/LeftUpFireExplainWin.cs` |
| `Assets/Script/UI/UserSettings/OverideGridLayout.cs` |
| `Assets/Script/UI/UserSettings/PlatformSwitcher.cs` |
| `Assets/Script/UI/UserSettings/UserSettingBasics.cs` |
| `Assets/Script/UI/UserSettings/UserSettingCarOperation.cs` |
| `Assets/Script/UI/UserSettings/UserSettingGamePad.cs` |
| `Assets/Script/UI/UserSettings/UserSettingGoldDash.cs` |
| `Assets/Script/UI/UserSettings/UserSettingGraphics.cs` |
| `Assets/Script/UI/UserSettings/UserSettingInput.cs` |
| `Assets/Script/UI/UserSettings/UserSettingInputItem.cs` |
| `Assets/Script/UI/UserSettings/UserSettingLanguage.cs` |
| `Assets/Script/UI/UserSettings/UserSettingMode.cs` |
| `Assets/Script/UI/UserSettings/UserSettingOperation.cs` |
| `Assets/Script/UI/UserSettings/UserSettingPickItem.cs` |
| `Assets/Script/UI/UserSettings/UserSettingPrivacy.cs` |
| `Assets/Script/UI/UserSettings/UserSettingsBase.cs` |
| `Assets/Script/UI/UserSettings/UserSettingSensitivity.cs` |
| `Assets/Script/UI/UserSettings/UserSettingSound.cs` |
| `Assets/Script/UI/UserSettings/UserSettingsWin.cs` |
| `Assets/Script/UI/UserSettings/UserSettingTrackRoute.cs` |
| `Assets/Script/UI/UserSettings/Component/ButtonGroup.cs` |
| `Assets/Script/UI/UserSettings/Component/GroupItem.cs` |
| `Assets/Script/UI/UserSettings/Component/SettingToggle.cs` |
| `Assets/Script/UI/UserSettings/Component/SettingToggleGroup.cs` |
| `Assets/Script/UI/UserSettings/Component/SliderGroup.cs` |
| `Assets/Script/UI/UserSettings/Component/UserSettingBezierDraw.cs` |
| `Assets/Script/UI/UserSettings/Component/UserSettingCircleDraw.cs` |
| `Assets/Script/UI/UserSettings/Component/UserSettingItemBase.cs` |
| `Assets/Script/UI/NewUserSetting/NewUserSettingsWin.cs` |
| `Assets/Script/UI/NewUserSetting/UserSettingsBtnAgreement.cs` |
| `Assets/Script/UI/NewUserSetting/UserSettingsBtnModule.cs` |
| `Assets/Script/UI/NewUserSetting/UserSettingsExplainContentWidget.cs` |
| `Assets/Script/UI/NewUserSetting/UserSettingsModuleElementBase.cs` |
| `Assets/Script/UI/NewUserSetting/UserSettingsModuleElementBinaryOption.cs` |
| `Assets/Script/UI/NewUserSetting/UserSettingsModuleElementBinaryOptionItem.cs` |
| `Assets/Script/UI/NewUserSetting/UserSettingsModuleElementBinarySlider.cs` |
| `Assets/Script/UI/NewUserSetting/UserSettingsModuleElementBinarySliderItem.cs` |
| `Assets/Script/UI/NewUserSetting/UserSettingsModuleElementDropdown.cs` |
| `Assets/Script/UI/NewUserSetting/UserSettingsModuleElementDropdownItem.cs` |
| `Assets/Script/UI/NewUserSetting/UserSettingsModuleElementGamePad.cs` |
| `Assets/Script/UI/NewUserSetting/UserSettingsModuleElementGifBinaryOption.cs` |
| `Assets/Script/UI/NewUserSetting/UserSettingsModuleElementGifBinaryOptionItem.cs` |
| `Assets/Script/UI/NewUserSetting/UserSettingsModuleElementJoystick.cs` |
| `Assets/Script/UI/NewUserSetting/UserSettingsModuleElementJoystickItem.cs` |
| `Assets/Script/UI/NewUserSetting/UserSettingsModuleElementMultiOption.cs` |
| `Assets/Script/UI/NewUserSetting/UserSettingsModuleElementSelector.cs` |
| `Assets/Script/UI/NewUserSetting/UserSettingsModuleElementServerArea.cs` |
| `Assets/Script/UI/NewUserSetting/UserSettingsModuleElementSwitchArea.cs` |
| `Assets/Script/UI/NewUserSetting/UserSettingsModuleElementTraceroute.cs` |
| `Assets/Script/UI/NewUserSetting/UserSettingsModuleGraphicWidget.cs` |
| `Assets/Script/UI/NewUserSetting/UserSettingsModuleInputKey.cs` |
| `Assets/Script/UI/NewUserSetting/UserSettingsModuleInputTitle.cs` |
| `Assets/Script/UI/NewUserSetting/UserSettingsModuleInputWidget.cs` |
| `Assets/Script/UI/NewUserSetting/UserSettingsModulePickUpWidget.cs` |
| `Assets/Script/UI/NewUserSetting/UserSettingsModuleSensitivityWidget.cs` |
| `Assets/Script/UI/NewUserSetting/UserSettingsModuleTabItemWidget.cs` |
| `Assets/Script/UI/NewUserSetting/UserSettingsModuleTabWidget.cs` |
| `Assets/Script/UI/NewUserSetting/UserSettingsModuleWidget.cs` |
| `Assets/Script/UI/NewUserSetting/Editor/UserSettingsModuleElementGamePadInspector.cs` |
| `Assets/Script/UI/PC/GamepadButtonImage.cs` |
| `Assets/Script/UI/PC/GamepadInputWindow.cs` |
| `Assets/Script/UI/PC/KeyBoard.cs` |
| `Assets/Script/UI/PC/KeyboardTextExplain.cs` |
| `Assets/Script/UI/PC/PcBtnTip.cs` |
| `Assets/Script/UI/PC/PcBtnToFunc.cs` |
| `Assets/Script/UI/PC/PcButtonTip.cs` |
| `Assets/Script/UI/PC/PcNoviceGuide.cs` |
| `Assets/Script/UI/PC/PcNovicGuideCommon.cs` |
| `Assets/Script/UI/PC/PcTipsCenter.cs` |
| `Assets/Script/UI/PC/TipsScroll.cs` |
| `Assets/Script/UI/Graphic/ColorGradientImage.cs` |
| `Assets/Script/UI/Graphic/Gradient.cs` |
| `Assets/Script/UI/Graphic/QualityBackGround.cs` |
| `Assets/Script/UI/Graphic/Editor/ColorGradientImageInspector.cs` |
| `Assets/Script/UI/ServerList/ServerListGroupItem.cs` |
| `Assets/Script/UI/ServerList/ServerListWin.cs` |
| `Assets/Script/UI/VersionChecking/CheckingWin.cs` |
| `Assets/Script/UI/VersionChecking/VersionCheckingWin.cs` |
| `Assets/Script/UI/PrivacyPolicy/PrivacyPolicyWin.cs` |
| `Assets/Script/UI/VoiceDownload/VoiceDownloadCell.cs` |
| `Assets/Script/UI/VoiceDownload/VoiceDownloadWin.cs` |
| `Assets/Script/UI/UpdateClient/UpdateClientWin.cs` |
