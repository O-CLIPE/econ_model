from econobj import *

def confirm(recursed=False):
    response = ''
    if not recursed:
        response = input("START y / n or r for reset:\ncontinue?> ")
    else:
        response = input("Answer should be y / n\ncontinue?> ")
    if response == 'y' or response == 'Y':
        return
    elif response == 'n' or response == 'N':
        return exit()
    elif response == 'r':
        db.drop()
        db.build()
        return exit(1)
    else:
        return confirm(recursed=True)

def main():
    confirm()
    cwc_id = db.create_entity('Cleen Water Company', cash=10_000, value=200_000)
    wb_id = db.create_good('bottled water')
    cwc_wb_id = db.create_product(cwc_id, wb_id, '100ml CWC water bottle', price=8.00, quantity=500)
    bob_id = db.create_entity('bob', cash=100.00)

    cwc = BaseEntity(**db.get_entity(cwc_id))
    wb_good = Good(**db.get_good(wb_id))
    cwc_wb = Product(**db.get_product(cwc_wb_id))
    bob = BaseEntity(**db.get_entity(bob_id))

    bob.buy(cwc_wb, 2)
    print(bob.cash)


if __name__ == '__main__':
    main()
    