import time
from threading import Timer

class CryptoNotifier:
    def __init__(self):
        self.notif_enabled = True       # Are notifications enabled
        self.notif_list = []            # Stores notifications
        self.mute_duration = 0          # Duration in seconds for mute
        self._mute_timer = None         # Internal timer for unmuting

    # notification control
    def toggle_notif(self):
        """Enable or disable all notifications."""
        self.notif_enabled = not self.notif_enabled
        state = "enabled" if self.notif_enabled else "disabled"
        print(f"Notifications {state}.")

    def mute_notif(self, duration=None):
        """
        Mute notifications temporarily or indefinitely.
        :param duration: seconds to mute, None for indefinite
        """
        self.notif_enabled = False
        if duration:
            self.mute_duration = duration
            # Cancel existing timer if active
            if self._mute_timer:
                self._mute_timer.cancel()
            self._mute_timer = Timer(duration, self.unmute_notif)
            self._mute_timer.start()
            print(f"Notifications muted for {duration} seconds.")
        else:
            print("Notifications muted indefinitely.")

    def unmute_notif(self):
        """Unmute notifications and restore default alerts."""
        self.notif_enabled = True
        self.mute_duration = 0
        if self._mute_timer:
            self._mute_timer.cancel()
            self._mute_timer = None
        print("Notifications unmuted.")

    # notification management
    def add_price_alert(self, crypto, target_price):
        """Add a price alert for a cryptocurrency."""
        alert = {"crypto": crypto, "target_price": target_price}
        self.notif_list.append(alert)
        print(f"Added price alert: {crypto} → {target_price}")

    def remove_price_alert(self, crypto, target_price):
        """Remove an existing price alert."""
        removed = False
        for alert in self.notif_list:
            if alert["crypto"] == crypto and alert["target_price"] == target_price:
                self.notif_list.remove(alert)
                removed = True
                print(f"Removed price alert: {crypto} → {target_price}")
                break
        if not removed:
            print("Price alert not found.")

    def clear_notif(self):
        """Clear all notifications."""
        self.notif_list.clear()
        print("All notifications cleared.")

    # sending notifications
    def notify(self, message):
        """Send a notification if enabled."""
        if self.notif_enabled:
            print(f" Notification: {message}")
        else:
            print("Notification suppressed (muted/disabled).")

  # utility
    def show_alerts(self):
        """Display all current price alerts."""
        if not self.notif_list:
            print("No active alerts.")
        else:
            print("Current Alerts:")
            for alert in self.notif_list:
                print(f" - {alert['crypto']} → {alert['target_price']}")


# example use
if __name__ == "__main__":
    notifier = CryptoNotifier()

    notifier.add_price_alert("BTC", 30000)
    notifier.add_price_alert("ETH", 2000)
    notifier.show_alerts()

    notifier.notify("BTC just hit $29,500!")

    notifier.mute_notif(duration=5)  # Mute for 5 seconds
    notifier.notify("ETH is at $1995")  # Should be suppressed

    time.sleep(6)  # Wait for unmute
    notifier.notify("ETH reached $2000!")  # Should notify now

    notifier.clear_notif()
    notifier.show_alerts()
