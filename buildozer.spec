[app]

title = FinanceTracker
package.name = financetracker
package.domain = org.financetracker

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

version = 1.0

requirements = python3,kivy

orientation = portrait

osx.python_version = 3
osx.kivy_version = 2.3.1

fullscreen = 0

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.accept_sdk_license = True

android.archs = arm64-v8a,armeabi-v7a

log_level = 2
