import kivy
kivy.require('2.1.0')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from data_provider import get_realtime_quote, get_history

class KLinePlaceholder(Label):
    pass

class StockItem(BoxLayout):
    def __init__(self, code, name, price, change, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 50
        self.code = code
        self.add_widget(Label(text=name, size_hint_x=0.3))
        self.price_label = Label(text=str(price), size_hint_x=0.2)
        self.change_label = Label(text=f"{change:.2f}%", size_hint_x=0.2)
        self.add_widget(self.price_label)
        self.add_widget(self.change_label)
        btn = Button(text='详情', size_hint_x=0.2)
        btn.bind(on_press=self.show_detail)
        self.add_widget(btn)

    def show_detail(self, instance):
        app = App.get_running_app()
        app.root.ids.detail_view.update(self.code)

class StockList(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = []

    def add_stock(self, code, name, price, change):
        self.data.append({'code': code, 'name': name, 'price': price, 'change': change})

    def refresh_all(self):
        for item in self.data:
            quote = get_realtime_quote(item['code'])
            if quote:
                item['price'] = quote['price']
                item['change'] = quote['change']
        self.refresh_from_data()

class DetailView(BoxLayout):
    current_code = None
    def update(self, code):
        self.current_code = code
        self.ids.code_label.text = code
        quote = get_realtime_quote(code)
        if quote:
            self.ids.name_label.text = quote['name']
            self.ids.price_label.text = f"{quote['price']:.2f}"
            self.ids.change_label.text = f"{quote['change']:.2f}%"
            self.ids.volume_label.text = str(quote['volume'])
        hist = get_history(code, days=30)
        if hist:
            closes = [d['close'] for d in hist[-5:]]
            self.ids.kline_text.text = f"最近5日收盘: {closes}"
        else:
            self.ids.kline_text.text = "无历史数据"

class RootWidget(BoxLayout):
    pass

class StockApp(App):
    def build(self):
        return RootWidget()

    def on_start(self):
        stock_list = self.root.ids.stock_list
        sample_stocks = [
            ('600519', '贵州茅台', 1700.0, 0.0),
            ('000858', '五粮液', 150.0, 0.0),
            ('300750', '宁德时代', 200.0, 0.0),
        ]
        for code, name, price, change in sample_stocks:
            stock_list.add_stock(code, name, price, change)
        Clock.schedule_interval(lambda dt: stock_list.refresh_all(), 5)

if __name__ == '__main__':
    StockApp().run()
