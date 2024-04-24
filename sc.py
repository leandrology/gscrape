import gspread

gc = gspread.service_account(filename="creds.json")

sh = gc.open('prices').sheet1

sh.clear()

sh.append_row(['LIVE METAL PRICES'])
sh.append_row(['METAL', 'BID', 'ASK', '+/-', '%'])
sh.append_row(['Gold', '25.34', '23.53', '2.05', '12.4'])

