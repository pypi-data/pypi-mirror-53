def main():
    print("Enter/Paste your content. Ctrl-D or Ctrl-Z ( windows ) to save it.")
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)
    balance = 0
    # Check if contents originate from Santander PDF
    #   - Santander uses "H" for credit and no sign for debit
    santander = False
    for x in contents:
        if "H" in x:
            santander = True
    for tx in contents:
        if not tx or "#" in tx:
            continue
        tx = tx.replace("EUR", "")
        if santander:
            tx = tx.replace(".", "")
            tx = tx.replace(",", ".")
            if "H" in tx:
                tx = tx.replace("+", "")
                tx = tx.replace("H", "").strip()
                balance += float(tx)
                print("New balance: %s" % balance)
            else:
                balance -= float(tx.strip())
                print("New balance: %s" % balance)
        else:
            tx = tx.replace(".", "")
            tx = tx.replace(",", ".")
            if "-" in tx:
                balance -= float(tx.replace("-", ""))
                print("New balance: %s" % balance)
            else:
                balance += float(tx.replace("+", ""))
                print("New balance: %s" % balance)
    print("Final balance: %s" % balance)
