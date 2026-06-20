from apscheduler.schedulers.background import BackgroundScheduler


scheduler = BackgroundScheduler()


def start_scheduler():
    if not scheduler.running:
        scheduler.start()
        print("Scheduler started successfully")


def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        print("Scheduler stopped")