[app]
title = StockWatcher
package.name = stockwatcher
package.domain = org.example.stock
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt
version = 0.1
requirements = python3,kivy==2.1.0,pandas,akshare,requests
osx.python_version = 3
osx.kivy_version = 2.1.0
android.permissions = INTERNET
android.api = 34
android.minapi = 21
android.ndk = 25b

[buildozer]
log_level = 2
warn_on_root = 1
