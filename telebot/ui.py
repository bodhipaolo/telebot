# Copyright (c) --------- (see AUTHORS)
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#   DEALINGS IN THE SOFTWARE.

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
