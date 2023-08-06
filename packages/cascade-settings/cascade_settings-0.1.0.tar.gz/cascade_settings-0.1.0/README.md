# cascade_settings
Wrapper for simple-settings.

```
settings = create_settings(
    'library.settings',     # created in library
    'library.user_settings',# created in library during development, usually in .gitignore
    'settings.library',     # created in project, that uses library
)
```
