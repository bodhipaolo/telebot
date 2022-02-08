class ButtonsRow:
	"""A row of inline keyboard
	"""

	def __init__(self):
		self._row = []

	def callback(self, label, call_name, callback_data):
		if callback_data == "":
			callback_data = call_name

		self._row.append({"text": label, "callback_data": callback_data})

	def url(self, label, url):
		self._row.append({"text": label, "url": url})

	def _get_content(self):
		"""Get the content of this row
		"""
		for item in self._row:
			new = item.copy()

			yield new

class Buttons:
    """Manage Buttons"""

    def __init__(self):
        self._rows = {}

    def __getitem__(self, idx):
        if idx not in self._rows:
            self._rows[idx] = ButtonsRow()
        return self._rows[idx]

    def _serialize_attachment(self):
        rows = [
            list(row._get_content()) for i, row in sorted(
                tuple(self._rows.items()), key=lambda i: i[0]
            )
        ]

        return {"inline_keyboard": rows} 
