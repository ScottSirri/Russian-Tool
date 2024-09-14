import russian_tool
import my_gui

fields = russian_tool.generate_card_fields()
for field in fields:
    print(f"{field}: {fields[field]}")
    print()
