# Personal Finance Manager — UI Integration v1

## Run
Run `main.py` from the project root:

```bash
python main.py
```

## Tests
```bash
python -m unittest discover -s tests -v
```

## What's connected
- Tkinter dashboard reads live totals from `TransactionController`.
- Transaction form validates amount, chooses a category compatible with the selected type, creates `Income` or `Expense`, and submits it through the controller.
- Transaction list and dashboard recent transactions show the in-memory transactions.
- Categories page reads the seeded category list.
- No persistent storage yet; data is reset when the app restarts.
- The category page is currently read-only; adding/editing/deleting categories is a later step.

If you're merging this into an existing project, back up your current files first. This ZIP is a standalone integration sample containing its own compatible `model`, `service`, `controller`, `view`, and `tests` folders.
