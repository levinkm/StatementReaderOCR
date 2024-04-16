import re

# Sample text (replace with your actual text data)
text = """
Berqhote1
Grosse Scheidegg
3818 Grindelwald
Fai lie R. Mal er

Rech.Hr. 4572 80.07, 2007/ 13:29:17
Bar Tisch 7/01

xLatte Macchiata: 4.6
IxGloki: 5
IxSchweinschnitzel: 22,

0 CHF 8.0.
00 CHE 5.00
00 CHF 22.00
St

IxChisspatz 15 @ 18.50 CHF 18,50

**Total:** CHF 84.50**  # Emphasize potential total line format

Incl. 7.6% MwSt 54,50 CHF: 3.85

Entspricht in Euro 36.33 EUR
Es bedtente Ste: Ursula
...
E-mail: grossescheidegg@h luewin. ch
"""

# Improved item price pattern (consider adjustments based on data format)
item_price_pattern = r"(?P<item_name>.+?): (?P<price>\d+\.\d+|\d+)"  # Allow for prices without decimals

# Flexible total pattern (optional)
total_pattern = r"(?i)\b(Total|sum|gesamt)\s*:\s*(?P<total>\d+\.\d+|\d+)"  # Capture variations (total, sum, gesamt)

# Split the text into lines
lines = text.splitlines()

# Extract items and prices using loop and regular expression
items = []
for line in lines:
  if not line.startswith("Incl"):
    match = re.match(item_price_pattern, line)
    if match:
      items.append({
        "name": match.group("item_name").strip(),
        "price": float(match.group("price").replace(",", "."))  # Convert price to float
      })

# Extract total amount using regular expression (optional)
total_match = re.search(total_pattern, text)
if total_match:
  total = float(total_match.group("total").replace(",", "."))  # Convert total to float

# Print extracted data
print("Extracted Data:")
print("  Items:")
for item in items:
  print(f"    - {item['name']}: {item['price']:.2f} CHF")
if total_match:
  print(f"  Total: {total:.2f} CHF")
