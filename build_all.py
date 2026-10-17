import os

def create_complete_project():
    print("[*] در حال ساخت کامل پروژه‌ی APK برای گیت‌هاب...")
    
    # ساخت دایرکتوری‌ها
    os.makedirs(".github/workflows", exist_ok=True)
    os.makedirs("app/src/main/java/com/sam/app", exist_ok=True)
    os.makedirs("app/src/main/res/values", exist_ok=True)
    
    # ۱. فایل settings.gradle
    with open("settings.gradle", "w") as f:
        f.write("""pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = "CustomOdinApp"
include ':app'
""")

    # ۲. فایل app/build.gradle
    with open("app/build.gradle", "w") as f:
        f.write("""plugins {
    id 'com.android.application'
}

android {
    namespace 'com.sam.app'
    compileSdk 34

    defaultConfig {
        applicationId "com.sam.app"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0"
    }

    buildTypes {
        release {
            minifyEnabled false
        }
    }
}

dependencies {
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.9.0'
}
""")

    # ۳. فایل AndroidManifest.xml
    with open("app/src/main/AndroidManifest.xml", "w") as f:
        f.write("""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <application
        android:label="Custom Odin Flasher"
        android:theme="@style/Theme.AppCompat.Light.NoActionBar">
        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
""")

    # ۴. فایل MainActivity.java
    with open("app/src/main/java/com/sam/app/MainActivity.java", "w") as f:
        f.write("""package com.sam.app;

import android.os.Bundle;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        TextView tv = new TextView(this);
        tv.setText("Custom Odin App - Ready to Rock!");
        tv.setTextSize(22f);
        setContentView(tv);
    }
}
""")

    # ۵. فایل ورک‌فلو گیت‌هاب (.github/workflows/build_apk.yml)
    with open(".github/workflows/build_apk.yml", "w") as f:
        f.write("""name: Build APK

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'

      - name: Setup Gradle
        uses: gradle/actions/setup-gradle@v3

      - name: Build APK with Gradle
        run: gradle assembleRelease

      - name: Upload APK Artifact
        uses: actions/upload-artifact@v4
        with:
          name: app-release
          path: app/build/outputs/apk/release/app-release-unsigned.apk
""")

    print("[+] تمام فایل‌های پروژه با موفقیت و بدون نقص ساخته شدند!")

if __name__ == "__main__":
    create_complete_project()

