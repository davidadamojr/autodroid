PLATFORM_TOOLS_DIR = "platform-tools"


class ScriptPath:
    ADB_RESET_SCRIPT = "appiumatic/scripts/adb_reset.sh"
    CHECK_BOOT_ANIM_SCRIPT = "appiumatic/scripts/check_boot_anim.sh"
    BOOT_STANDARD_EMU_SCRIPT = "appiumatic/scripts/boot_standard_emulator.sh"
    BOOT_GENYMOTION_EMU_SCRIPT = "appiumatic/scripts/boot_genymotion_emulator.sh"
    KILL_STANDARD_EMU_SCRIPT = "appiumatic/scripts/kill_standard_emulator.sh"
    KILL_GENYMOTION_EMU_SCRIPT = "appiumatic/scripts/kill_genymotion_emulator.sh"
    START_APPIUM_SCRIPT = "appiumatic/scripts/start_appium.sh"


class GUIAction:
    CLICK = "click"
    LONG_CLICK = "long-click"
    CHECK = "check"
    UNCHECK = "uncheck"
    SWIPE_UP = "swipe-up"
    SWIPE_DOWN = "swipe-down"
    SWIPE_RIGHT = "swipe-right"
    SWIPE_LEFT = "swipe-left"
    TEXT_ENTRY = "text-entry"
    HOME_NAV = "home"
    BACK_NAV = "back"
    ENTER_KEY = "enter"


class SystemAction:
    LAUNCH = "launch"
    RUN_IN_BACKGROUND = "run-in-background"


class TargetType:
    APP = "app"
    NAV = "nav"
    SPINNER = "spinner"


class SelectorType:
    ID = "id"
    XPATH = "xpath"
    SYSTEM = "system"


class KeyCode:
    HOME = 3
    BACK = 4
    RETURN = 66


class TargetState:
    ENABLED = "enabled"
    DISABLED = "disabled"
