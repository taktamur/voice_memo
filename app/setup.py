#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
setup.py - py2appを使用してスタンドアロンアプリケーションをビルドするためのセットアップスクリプト
"""

from setuptools import setup

APP = ['src/voice_memo_app.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'LSUIElement': True,  # ドックにアイコンを表示しない設定
        'CFBundleName': 'Voice Memo',
        'CFBundleDisplayName': 'Voice Memo',
        'CFBundleIdentifier': 'com.example.VoiceMemo',
        'CFBundleVersion': '0.1.0',
        'CFBundleShortVersionString': '0.1.0',
    },
    'packages': ['rumps'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    name='Voice Memo',
    version='0.1.0',
    description='Voice Memo アプリケーション',
    author='Claude',
    author_email='example@example.com',
)
