import time
import os
from customInput import customInput
import settings


controls = customInput((100, 200), 0.1, (0,0,1919,1079), settings.pathToImages)

while True:
	object = controls.wait_until("create_label")
	if object:
		controls.wait_until("total_postage_cost")
		label = controls.wait_until("create_label")
		if not label:
			continue
		controls.click(label)
		printer_button = controls.wait_until("printer_button")
		if not printer_button:
			continue
		controls.click(printer_button)
		print_button = controls.wait_until("print")
		if not print_button:
			continue
		controls.click(print_button)
		x_button = controls.wait_until("x", wait=2)
		if not x_button:
			continue
		controls.click(x_button)
