from models.alert import Alert

alerts = Alert.all()

for alert in alerts:
    alert.load_item_price()
    alert.notify_if_price_reached()

if not alerts:
    print('No alerts available. Add items/alerts to begin!')
