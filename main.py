"""
FinanceTracker Pro - Android Mobile Application
A professional-grade mobile app for tracking income and expenses.

Author: Senior MIT Developer
Version: 1.0.0
"""

import os
import json
import uuid
from datetime import datetime
from typing import Optional, Dict, List
from dataclasses import dataclass, field
from enum import Enum

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from kivy.uix.switch import Switch
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.metrics import dp, sp
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ListProperty
from kivy.utils import get_color_from_hex


# ============================================================================
# DATA MODELS
# ============================================================================

class TransactionType(Enum):
    INCOME = "income"
    EXPENSE = "expense"


class Category:
    DEFAULT_CATEGORIES = {
        TransactionType.INCOME: ["Salary", "Freelance", "Investments", "Gift", "Other"],
        TransactionType.EXPENSE: ["Food", "Transport", "Housing", "Utilities", "Entertainment", "Shopping", "Healthcare", "Education", "Other"]
    }
    
    def __init__(self, name: str, color: str = "#3498db"):
        self.name = name
        self.color = color


@dataclass
class Transaction:
    id: str
    amount: float
    category: str
    transaction_type: TransactionType
    description: str
    date: datetime
    
    @staticmethod
    def create(amount: float, category: str, trans_type: TransactionType, description: str = "", date: Optional[datetime] = None):
        return Transaction(
            id=str(uuid.uuid4())[:8],
            amount=amount,
            category=category,
            transaction_type=trans_type,
            description=description,
            date=date or datetime.now()
        )


# ============================================================================
# DATA MANAGER
# ============================================================================

class DataManager:
    def __init__(self):
        self.data_dir = App.get_running_app().user_data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        self.transactions_file = os.path.join(self.data_dir, "transactions.json")
    
    def load_transactions(self) -> List[Transaction]:
        if not os.path.exists(self.transactions_file):
            return []
        try:
            with open(self.transactions_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Transaction(
                    id=t["id"],
                    amount=t["amount"],
                    category=t["category"],
                    transaction_type=TransactionType(t["type"]),
                    description=t["description"],
                    date=datetime.fromisoformat(t["date"])
                ) for t in data]
        except:
            return []
    
    def save_transactions(self, transactions: List[Transaction]):
        with open(self.transactions_file, "w", encoding="utf-8") as f:
            json.dump([{
                "id": t.id,
                "amount": t.amount,
                "category": t.category,
                "type": t.transaction_type.value,
                "description": t.description,
                "date": t.date.isoformat()
            } for t in transactions], f, indent=2, ensure_ascii=False)


# ============================================================================
# CONTROLLER
# ============================================================================

class FinanceController:
    def __init__(self):
        self.data_manager = DataManager()
        self.transactions: List[Transaction] = self.data_manager.load_transactions()
    
    def add_transaction(self, amount: float, category: str, trans_type: TransactionType, description: str = "", date: Optional[datetime] = None):
        if amount <= 0:
            return None
        transaction = Transaction.create(amount, category, trans_type, description, date)
        self.transactions.append(transaction)
        self.data_manager.save_transactions(self.transactions)
        return transaction
    
    def delete_transaction(self, transaction_id: str) -> bool:
        for i, t in enumerate(self.transactions):
            if t.id == transaction_id:
                self.transactions.pop(i)
                self.data_manager.save_transactions(self.transactions)
                return True
        return False
    
    def get_balance(self) -> float:
        income = sum(t.amount for t in self.transactions if t.transaction_type == TransactionType.INCOME)
        expense = sum(t.amount for t in self.transactions if t.transaction_type == TransactionType.EXPENSE)
        return income - expense
    
    def get_total_income(self) -> float:
        return sum(t.amount for t in self.transactions if t.transaction_type == TransactionType.INCOME)
    
    def get_total_expense(self) -> float:
        return sum(t.amount for t in self.transactions if t.transaction_type == TransactionType.EXPENSE)
    
    def get_expenses_by_category(self) -> Dict[str, float]:
        result = {}
        for t in self.transactions:
            if t.transaction_type == TransactionType.EXPENSE:
                result[t.category] = result.get(t.category, 0) + t.amount
        return result
    
    def get_income_by_category(self) -> Dict[str, float]:
        result = {}
        for t in self.transactions:
            if t.transaction_type == TransactionType.INCOME:
                result[t.category] = result.get(t.category, 0) + t.amount
        return result
    
    def get_recent_transactions(self, limit: int = 50) -> List[Transaction]:
        sorted_trans = sorted(self.transactions, key=lambda x: x.date, reverse=True)
        return sorted_trans[:limit]


# ============================================================================
# UI COMPONENTS
# ============================================================================

class ModernButton(Button):
    pass


class CardLayout(BoxLayout):
    pass


class TransactionItem(BoxLayout):
    id = StringProperty()
    amount = StringProperty()
    category = StringProperty()
    description = StringProperty()
    date = StringProperty()
    type_color = ListProperty([1, 1, 1, 1])
    
    def __init__(self, transaction: Transaction, **kwargs):
        super().__init__(**kwargs)
        self.id = transaction.id
        self.amount = f"{transaction.amount:,.0f} ₽"
        self.category = transaction.category
        self.description = transaction.description or "-"
        self.date = transaction.date.strftime("%d.%m.%Y %H:%M")
        
        if transaction.transaction_type == TransactionType.INCOME:
            self.type_color = get_color_from_hex("#27ae60")
        else:
            self.type_color = get_color_from_hex("#e74c3c")


# ============================================================================
# SCREENS
# ============================================================================

class HomeScreen(Screen):
    def on_enter(self):
        self.update_balance()
    
    def update_balance(self):
        app = App.get_running_app()
        balance = app.controller.get_balance()
        income = app.controller.get_total_income()
        expense = app.controller.get_total_expense()
        
        self.ids.balance_label.text = f"{balance:,.0f} ₽"
        self.ids.balance_label.color = get_color_from_hex("#2ecc71" if balance >= 0 else "#e74c3c")
        self.ids.income_label.text = f"{income:,.0f} ₽"
        self.ids.expense_label.text = f"{expense:,.0f} ₽"


class TransactionsScreen(Screen):
    def on_enter(self):
        self.load_transactions()
    
    def load_transactions(self):
        app = App.get_running_app()
        transactions = app.controller.get_recent_transactions(100)
        
        self.ids.transactions_list.clear_widgets()
        
        for t in transactions:
            item = TransactionItem(t, size_hint_y=None, height=dp(80))
            self.ids.transactions_list.add_widget(item)


class AddTransactionScreen(Screen):
    def on_enter(self):
        self.reset_form()
    
    def reset_form(self):
        self.ids.amount_input.text = ""
        self.ids.description_input.text = ""
        self.ids.type_spinner.text = "Расход"
        self.ids.category_spinner.text = "Еда"
    
    def on_type_change(self, *args):
        trans_type = self.ids.type_spinner.text
        if trans_type == "Расход":
            categories = Category.DEFAULT_CATEGORIES[TransactionType.EXPENSE]
        else:
            categories = Category.DEFAULT_CATEGORIES[TransactionType.INCOME]
        
        self.ids.category_spinner.values = categories
        self.ids.category_spinner.text = categories[0]
    
    def save_transaction(self):
        amount_text = self.ids.amount_input.text.strip().replace(",", ".")
        
        try:
            amount = float(amount_text)
            if amount <= 0:
                self.show_error("Введите корректную сумму")
                return
        except ValueError:
            self.show_error("Введите корректную сумму")
            return
        
        category = self.ids.category_spinner.text
        description = self.ids.description_input.text.strip()
        
        trans_type = TransactionType.EXPENSE if self.ids.type_spinner.text == "Расход" else TransactionType.INCOME
        
        app = App.get_running_app()
        app.controller.add_transaction(amount, category, trans_type, description)
        
        self.reset_form()
        self.show_success("Транзакция добавлена!")
    
    def show_error(self, message: str):
        box = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(10))
        box.add_widget(Label(text=message, font_size=dp(16)))
        btn = Button(text="OK", size_hint_y=None, height=dp(50), background_color=get_color_from_hex("#e74c3c"))
        box.add_widget(btn)
        
        popup = Popup(title="Ошибка", content=box, size_hint=(0.8, 0.3), auto_dismiss=True)
        btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def show_success(self, message: str):
        box = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(10))
        box.add_widget(Label(text=message, font_size=dp(16)))
        btn = Button(text="OK", size_hint_y=None, height=dp(50), background_color=get_color_from_hex("#27ae60"))
        box.add_widget(btn)
        
        popup = Popup(title="Успех", content=box, size_hint=(0.8, 0.3), auto_dismiss=True)
        btn.bind(on_press=popup.dismiss)
        btn.bind(on_press=lambda *args: setattr(self.manager, 'current', 'home'))
        popup.open()


class StatisticsScreen(Screen):
    def on_enter(self):
        self.load_statistics()
    
    def load_statistics(self):
        app = App.get_running_app()
        
        expense_data = app.controller.get_expenses_by_category()
        income_data = app.controller.get_income_by_category()
        
        expense_text = "Расходы по категориям:\n\n"
        for cat, amount in sorted(expense_data.items(), key=lambda x: x[1], reverse=True):
            expense_text += f"{cat}: {amount:,.0f} ₽\n"
        
        income_text = "Доходы по категориям:\n\n"
        for cat, amount in sorted(income_data.items(), key=lambda x: x[1], reverse=True):
            income_text += f"{cat}: {amount:,.0f} ₽\n"
        
        if not expense_data:
            expense_text = "Нет данных о расходах"
        if not income_data:
            income_text = "Нет данных о доходах"
        
        self.ids.expense_label.text = expense_text
        self.ids.income_label.text = income_text


# ============================================================================
# MAIN APP
# ============================================================================

class FinanceTrackerApp(App):
    controller = FinanceController()
    
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(TransactionsScreen(name="transactions"))
        sm.add_widget(AddTransactionScreen(name="add"))
        sm.add_widget(StatisticsScreen(name="statistics"))
        
        return sm
    
    def on_start(self):
        pass
    
    def on_pause(self):
        return True


if __name__ == "__main__":
    FinanceTrackerApp().run()
