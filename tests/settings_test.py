# coding=utf-8
from lbt_recipes.settings import RecipeSettings


def test_settings_init():
    """Test the initialization of RecipeSettings and basic properties."""
    settings = RecipeSettings()

    assert settings.folder is None
    assert settings.workers >= 1
    assert not settings.reload_old
    assert not settings.report_out


def test_settings_setability():
    """Test the setting of properties of settingsParameter."""
    settings = RecipeSettings()

    folder = './tests/assets/project folder'
    settings.folder = folder
    assert settings.folder == folder
    settings.workers = 8
    assert settings.workers == 8
    settings.reload_old = True
    assert settings.reload_old
    settings.report_out = True
    assert settings.report_out


def test_settings_equality():
    """Test the equality of settingsParameter objects."""
    folder = './tests/assets/project folder'
    settings = RecipeSettings(folder, 6)
    settings_dup = settings.duplicate()
    settings_alt = RecipeSettings(folder, 4)

    assert settings is settings
    assert settings is not settings_dup
    assert settings == settings_dup
    settings_dup.workers = 8
    assert settings != settings_dup
    assert settings != settings_alt


def test_settings_str_methods():
    """Test the to/from string methods."""
    folder = './tests/assets/project folder'
    settings = RecipeSettings(folder, 6, report_out=True)

    settings_str = str(settings)
    new_settings = RecipeSettings.from_string(settings_str)
    assert new_settings == settings
    assert settings_str == str(new_settings)
