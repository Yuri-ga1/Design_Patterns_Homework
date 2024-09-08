from settings_worker.settings_manager import SettingsManager


manager1 = SettingsManager()
if not manager1.open("settings.json"):
    print("Настройки не загружены!")
print(f"settings1: {manager1.settings.organization_name}")

manager2 = SettingsManager()
if not manager2.open("settings1.json"):
    print("Настройки не загружены!")
print(f"settings2: {manager2.settings.organization_name}")
