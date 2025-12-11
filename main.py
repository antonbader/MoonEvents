from moon_events.gui import MondApp

if __name__ == "__main__":
    app = MondApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
