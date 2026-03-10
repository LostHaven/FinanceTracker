# FinanceTracker Pro - Android

Мобильное приложение для учёта финансов на Android.

## Файлы проекта

```
FinanceTrackerAndroid/
├── main.py           # Главный код приложения (Kivy)
├── finance.kv        # UI разметка
├── buildozer.spec    # Конфигурация сборки
└── README.md         # Этот файл
```

## Как собрать APK на Windows

### Шаг 1: Установите Android SDK

1. Скачайте Android Command Line Tools:
   https://developer.android.com/studio#cmdline-tools

2. Распакуйте в папку, например `C:\Android\cmdline-tools`

3. Создайте папку `C:\Android\sdk`

4. Запустите терминал от администратора и выполните:
```cmd
setx ANDROID_HOME "C:\Android\sdk"
setx PATH "%PATH%;C:\Android\cmdline-tools\latest\bin;C:\Android\sdk\platform-tools"
```

5. Установите необходимые компоненты:
```cmd
sdkmanager --install "platforms;android-31" "build-tools;30.0.3" "platform-tools"
```

### Шаг 2: Установите зависимости Python

```cmd
pip install kivy buildozer
```

### Шаг 3: Соберите APK

```cmd
cd C:\путь\к\FinanceTrackerAndroid
buildozer android debug
```

APK появится в папке `bin/`

## Альтернативные способы

### Через Google Colab (без установки)

1. Откройте Google Colab: https://colab.research.google.com

2. Выполните код:
```python
!pip install buildozer
!mkdir -p /content/FinanceTrackerAndroid
# Загрузите файлы main.py и finance.kv
%cd /content/FinanceTrackerAndroid
!buildozer android debug
```

3. Скачайте APK из папки `bin/`

## Требования

- Python 3.8+
- Kivy 2.3.1
- Android SDK (API 21+)

## Возможности

- ✅ Учёт доходов и расходов
- ✅ Категоризация транзакций
- ✅ Просмотр истории
- ✅ Статистика по категориям
- ✅ Красивый мобильный интерфейс

## Структура экранов

1. **Главный экран** - баланс, доходы, расходы, меню
2. **Добавить транзакцию** - форма ввода
3. **История** - список всех транзакций  
4. **Статистика** - расходы/доходы по категориям
