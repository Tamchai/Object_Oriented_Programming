class User:
    def __init__(self, citizen_id: str, name: str):
        self.__citizen_id = citizen_id
        self.__name = name
        self.__accounts = []
        self.__atm_cards = []

    @property
    def name(self):
        return self.__name

    @property
    def accounts(self):
        return self.__accounts

    def add_account(self, account):
        self.__accounts.append(account)

    @property
    def atm_cards(self):
        return self.__atm_cards

    def add_atm_card(self, atm_card):
        self.__atm_cards.append(atm_card)


class Account:
    def __init__(self, account_number: str, owner: User, balance=0):
        self.__account_number = account_number
        self.__owner = owner
        self.__balance = balance
        self.__atm_card = None
        self.__transaction_history = []

    @property
    def account_number(self):
        return self.__account_number

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, amount):
        self.__balance = amount

    @property
    def atm_card(self):
        return self.__atm_card

    @atm_card.setter
    def atm_card(self, card):
        self.__atm_card = card

    @property
    def transaction_history(self):
        return self.__transaction_history

    def add_transaction(self, transaction):
        self.__transaction_history.append(transaction)

    def deposit(self, account, amount: float):
        if amount <= 0:
            return "Error"

        self.__balance += amount
        self.__transaction_history.append(TransactionHistory("D",amount,machine_id,self.__balance))
        return "Success"

    def withdraw(self, account, amount: float):
        if amount <= 0:
            return "Error"
        if amount > ATMMachine.Max_withdraw:
            return "Error"
        if amount > self.__balance:
            return "Error"
        if amount > account.balance:
            return "Error"

        self.__balance -= amount
        self.__transaction_history.append(TransactionHistory("W",amount,machine_id,self.__balance))
        return "Successful"

    def transfer(self, from_account, to_account, amount: float):
        if amount <= 0:
            return "Invalid Transfer Amount"
        if amount > from_account.balance:
            return "Insufficient Balance in Sender Account"

        self.__balance -= amount
        to_account.balance += amount
        self.__transaction_history.append(TransactionHistory("TD",amount,machine_id,self.__balance))
        return "Transfer Successful"



class ATMCard:
    def __init__(self, card_number: str, account: Account, pin: str):
        self.__card_number = card_number
        self.__account = account
        self.__pin = pin

    @property
    def card_number(self):
        return self.__card_number

    @property
    def account(self):
        return self.__account

    @property
    def pin(self):
        return self.__pin


class ATMMachine:
    Max_withdraw = 40000

    def __init__(self, machine_id: str, initial_amount: float = 1000000):
        self.__machine_id = machine_id
        self.__balance = initial_amount

    @property
    def machine_id(self):
        return self.__machine_id

    @property
    def balance(self):
        return self.__balance

    def insert_card(self, bank, atm_card: ATMCard, pin: str) -> Account | None:
        if atm_card.pin != pin:
            return "Invalid PIN"

        for user in bank.users:
            for account in user.accounts:
                if account.atm_card == atm_card:
                    return account
        return None

    def deposit(self, account: Account, amount: float):
        if amount <= 0:
            return "Error"

        account.balance += amount
        self.__balance += amount
        account.add_transaction(TransactionHistory("D", amount, account.balance, self.__machine_id))
        return "Success"

    def withdraw(self, account: Account, amount: float):
        if amount <= 0:
            return "Error"
        if amount > ATMMachine.Max_withdraw:
            return "Error"
        if amount > self.__balance:
            return "Error"
        if amount > account.balance:
            return "Error"

        account.balance -= amount
        self.__balance -= amount
        account.add_transaction(TransactionHistory("W", amount, account.balance, self.__machine_id))
        return "Successful"

    def transfer(self, from_account: Account, to_account: Account, amount: float):
        if amount <= 0:
            return "Invalid Transfer Amount"
        if amount > from_account.balance:
            return "Insufficient Balance in Sender Account"

        from_account.balance -= amount
        to_account.balance += amount
        from_account.add_transaction(TransactionHistory("TW", amount, from_account.balance, self.__machine_id))
        to_account.add_transaction(TransactionHistory("TD", amount, to_account.balance, self.__machine_id))
        return "Transfer Successful"


class Bank:
    def __init__(self, name: str):
        self.__name = name
        self.__users = []
        self.__atm_machines = []

    @property
    def users(self):
        return self.__users

    def add_user(self, user):
        self.__users.append(user)

    def add_atm_machine(self, atm_machine):
        self.__atm_machines.append(atm_machine)

    def get_atm_machine(self, machine_id) -> None | ATMMachine:
        for machine in self.__atm_machines:
            if machine.machine_id == machine_id:
                return machine
        return None


class TransactionHistory:
    def __init__(self, type, amount, after_amount, machine_id):
        self.__type = type
        self.__amount = amount
        self.__after_amount = after_amount
        self.__machine_id = machine_id

    def __str__(self):
        return f"{self.__type}-ATM:{self.__machine_id}-{self.__amount}-{self.__after_amount}"

##################################################################################

# กำหนดรูปแบบของ user ดังนี้ {รหัสประชาชน : [ชื่อ, หมายเลขบัญชี, จำนวนเงิน, หมายเลข ATM ]}
user_data = {'1-1101-12345-12-0': ['Harry Potter', '1234567890', '12345', 20000],
             '1-1101-12345-13-0': ['Hermione Jean Granger', '0987654321', '12346', 1000]}

atm_data = {'1001': 1000000, '1002': 200000}

bank = Bank("Tamjai_bank")

# แยก Keyกับvalue ของ user_data
for citizen_id, data in user_data.items():
    user = User(citizen_id, data[0])
    account = Account(data[1], user, data[3])
    atm_card = ATMCard(data[2], account, "1234")

    user.add_account(account)
    user.add_atm_card(atm_card)
    account.atm_card = atm_card

    bank.add_user(user)

# แยก keyกับvalue ของ atm_data
for machine_id, balance in atm_data.items():
    atm_machine = ATMMachine(machine_id, balance)
    bank.add_atm_machine(atm_machine)

def todo():
    # TODO 1 : จากข้อมูลใน user ให้สร้าง instance โดยมีข้อมูล
    # TODO :   key:value โดย key เป็นรหัสบัตรประชาชน และ value เป็นข้อมูลของคนนั้น ประกอบด้วย
    # TODO :   [ชื่อ, หมายเลขบัญชี, หมายเลขบัตร ATM, จำนวนเงินในบัญชี]
    # TODO :   return เป็น instance ของธนาคาร
    # TODO :   และสร้าง instance ของเครื่อง ATM จำนวน 2 เครื่อง
    print("TODO 1", bank)
    print("TODO 1 ATM Machine:", [atm.machine_id for atm in bank._Bank__atm_machines])

    # TODO 2 : เขียน method ที่ทำหน้าที่สอดบัตรเข้าเครื่อง ATM มี parameter 2 ตัว ได้แก่ 1) instance ของธนาคาร
    # TODO     2) atm_card เป็นหมายเลขของ atm_card
    # TODO     return ถ้าบัตรถูกต้องจะได้ instance ของ account คืนมา ถ้าไม่ถูกต้องได้เป็น None
    # TODO     ควรเป็น method ของเครื่อง ATM
    user_citizen_id = list(user_data.keys())[0]
    user = None
    for u in bank.users:
        if u.name == user_data[user_citizen_id][0]:
            user = u
            break
    if user:
        atm_card = user.atm_cards[0]
        account = atm_machine.insert_card(bank, atm_card, atm_card.pin)
        print("TODO 2:", account)
    else:
        print("User not found.")


    # TODO 3 : เขียน method ที่ทำหน้าที่ฝากเงิน โดยรับ parameter 3 ตัว คือ 1) instance ของเครื่อง atm
    # TODO     2) instance ของ account 3) จำนวนเงิน
    # TODO     การทำงาน ให้เพิ่มจำนวนเงินในบัญชี และ สร้าง transaction ลงในบัญชี
    # TODO     return หากการทำรายการเรียบร้อยให้ return success ถ้าไม่เรียบร้อยให้ return error
    # TODO     ต้อง validate การทำงาน เช่น ตัวเลขต้องมากกว่า 0
    deposit = atm_machine.deposit(account, 500)
    print("TODO 3", deposit)

    #TODO 4 : เขียน method ที่ทำหน้าที่ถอนเงิน โดยรับ parameter 3 ตัว คือ 1) instance ของเครื่อง atm
    # TODO     2) instance ของ account 3) จำนวนเงิน
    # TODO     การทำงาน ให้ลดจำนวนเงินในบัญชี และ สร้าง transaction ลงในบัญชี
    # TODO     return หากการทำรายการเรียบร้อยให้ return success ถ้าไม่เรียบร้อยให้ return error
    # TODO     ต้อง validate การทำงาน เช่น ตัวเลขต้องมากกว่า 0 และ ไม่ถอนมากกว่าเงินที่มี
    withdraw = atm_machine.withdraw(account, 500)
    print("TODO 4", withdraw)

    #TODO 5 : เขียน method ที่ทำหน้าที่โอนเงิน โดยรับ parameter 4 ตัว คือ 1) instance ของเครื่อง atm
    # TODO     2) instance ของ account ตนเอง 3) instance ของ account ที่โอนไป 4) จำนวนเงิน
    # TODO     การทำงาน ให้ลดจำนวนเงินในบัญชีตนเอง และ เพิ่มเงินในบัญชีคนที่โอนไป และ สร้าง transaction ลงในบัญชี
    # TODO     return หากการทำรายการเรียบร้อยให้ return success ถ้าไม่เรียบร้อยให้ return error
    # TODO     ต้อง validate การทำงาน เช่น ตัวเลขต้องมากกว่า 0 และ ไม่ถอนมากกว่าเงินที่มี
    all_accounts = [account for user in bank.users for account in user.accounts]
    from_account = all_accounts[0]
    to_account = all_accounts[1]
    transfer = atm_machine.transfer(from_account, to_account, 1000)
    print("TODO 5", transfer)

###############################Test Cases###############################################
def test_cases():
    atm1 = bank.get_atm_machine('1001')
    atm2 = bank.get_atm_machine('1002')
    harry = bank.users[0]
    hermione = bank.users[1]

    # Test case #1 : ทดสอบ การ insert บัตร โดยค้นหาเครื่อง atm เครื่องที่ 1 และบัตร atm ของ harry
    # และเรียกใช้ function หรือ method จากเครื่อง ATM
    # ผลที่คาดหวัง : พิมพ์ หมายเลข account ของ harry อย่างถูกต้อง และ พิมพ์หมายเลขบัตร ATM อย่างถูกต้อง
    # Ans : 12345, 1234567890, Success
    harry_account = atm1.insert_card(bank, harry.atm_cards[0], "1234")
    print("Test Case 1")
    print(f"Ans : {harry_account.account_number}, {harry.atm_cards[0].card_number}, Success")
    print("-------------------------")

    # Test case #2 : ทดสอบฝากเงินเข้าในบัญชีของ Hermione ในเครื่อง atm เครื่องที่ 2 เป็นจำนวน 1000 บาท
    # ให้เรียกใช้ method ที่ทำการฝากเงิน
    # ผลที่คาดหวัง : แสดงจำนวนเงินในบัญชีของ Hermione ก่อนฝาก หลังฝาก และ แสดง transaction
    # Hermione account before test : 1000
    # Hermione account after test : 2000
    print("\nTest Case 2")
    print(f"Hermione account before test : {hermione.accounts[0].balance}")
    atm2.deposit(hermione.accounts[0], 1000)
    print(f"Hermione account after test : {hermione.accounts[0].balance}")
    print("-------------------------")

    # Test case #3 : ทดสอบฝากเงินเข้าในบัญชีของ Hermione ในเครื่อง atm เครื่องที่ 2 เป็นจำนวน -1 บาท
    # ผลที่คาดหวัง : แสดง Error
    print("\nTest Case 3")
    result = atm2.deposit(hermione.accounts[0], -1)
    print(f"Ans : {result}")
    print("-------------------------")

    # Test case #4 : ทดสอบการถอนเงินจากบัญชีของ Hermione ในเครื่อง atm เครื่องที่ 2 เป็นจำนวน 500 บาท
    # ให้เรียกใช้ method ที่ทำการถอนเงิน
    # ผลที่คาดหวัง : แสดงจำนวนเงินในบัญชีของ Hermione ก่อนถอน หลังถอน และ แสดง transaction
    # Hermione account before test : 2000
    # Hermione account after test : 1500
    print("\nTest Case 4")
    print(f"Hermione account before test: {hermione.accounts[0].balance}")
    result = atm2.withdraw(hermione.accounts[0], 500)
    print(f"Hermione account after test: {hermione.accounts[0].balance}")
    print("-------------------------")

    # Test case #5 : ทดสอบถอนเงินจากบัญชีของ Hermione ในเครื่อง atm เครื่องที่ 2 เป็นจำนวน 2000 บาท
    # ผลที่คาดหวัง : แสดง Error
    print("\nTest Case 5")
    result = atm2.withdraw(hermione.accounts[0], 2000)
    print(f"Ans : {result}")
    print("-------------------------")

    # Test case #6 : ทดสอบการโอนเงินจากบัญชีของ Harry ไปยัง Hermione จำนวน 10000 บาท ในเครื่อง atm เครื่องที่ 2
    # ให้เรียกใช้ method ที่ทำการโอนเงิน
    # ผลที่คาดหวัง : แสดงจำนวนเงินในบัญชีของ Harry ก่อนถอน หลังถอน และ แสดงจำนวนเงินในบัญชีของ Hermione ก่อนถอน หลังถอน แสดง transaction
    # Harry account before test : 20000
    # Hermione account before test : 1500

    # Harry account after test : 10000
    # Hermione account after test : 11500
    print("\nTest Case 6")
    print(f"Harry account before test: {harry.accounts[0].balance}")
    print(f"Hermione account before test: {hermione.accounts[0].balance}")
    result = atm2.transfer(harry.accounts[0], hermione.accounts[0], 10000)
    print(f"Harry account after test: {harry.accounts[0].balance}")
    print(f"Hermione account after test: {hermione.accounts[0].balance}")
    print("-------------------------")

    # Test case #7 : แสดง transaction ของ Hermione ทั้งหมด 
    # ผลที่คาดหวัง
    # Hermione transaction : D-ATM:1002-1000-2000
    # Hermione transaction : W-ATM:1002-500-1500
    # Hermione transaction : TD-ATM:1002-10000-11500
    print("\nTest Case 7")
    for transaction in hermione.accounts[0].transaction_history:
        print(f"Hermione transaction : {transaction}")
    print("-------------------------")

    # Test case #8 : ทดสอบการใส่ PIN ไม่ถูกต้อง 
    # ให้เรียกใช้ method ที่ทำการ insert card และตรวจสอบ PIN
    # atm_machine = bank.get_atm('1001')
    # test_result = atm_machine.insert_card('12345', '9999')  # ใส่ PIN ผิด
    # ผลที่คาดหวัง
    # Invalid PIN
    print("\nTest Case 8")
    result = atm1.insert_card(bank, harry.atm_cards[0], "9999")
    print(f"Ans : {result}")
    print("-------------------------")

    # Test case #9 : ทดสอบการถอนเงินเกินวงเงินต่อวัน (40,000 บาท)
    # atm_machine = bank.get_atm('1001')
    # account = atm_machine.insert_card('12345', '1234')  # PIN ถูกต้อง
    # harry_balance_before = account.get_balance()

    # print(f"Harry account before test: {harry_balance_before}")
    # print("Attempting to withdraw 45,000 baht...")
    # result = atm_machine.withdraw(account, 45000)
    # print(f"Expected result: Exceeds daily withdrawal limit of 40,000 baht")
    # print(f"Actual result: {result}")
    # print(f"Harry account after test: {account.get_balance()}")
    # print("-------------------------")
    print("\nTest Case 9")
    harry_account = atm1.insert_card(bank, harry.atm_cards[0], "1234")
    print(f"Harry account before test: {harry_account.balance}")
    result = atm1.withdraw(harry_account, 45000)
    print(f"Expected result: Exceeds daily withdrawal limit of 40,000 baht")
    print(f"Actual result: {result}")
    print(f"Harry account after test: {harry_account.balance}")
    print("-------------------------")

    # Test case #10 : ทดสอบการถอนเงินเมื่อเงินในตู้ ATM ไม่พอ
    # atm_machine = bank.get_atm('1002')  # สมมติว่าตู้ที่ 2 มีเงินเหลือ 200,000 บาท
    # account = atm_machine.insert_card('12345', '1234')

    # print("Test case #10 : Test withdrawal when ATM has insufficient funds")
    # print(f"ATM machine balance before: {atm_machine.get_balance()}")
    # print("Attempting to withdraw 250,000 baht...")
    # result = atm_machine.withdraw(account, 250000)
    # print(f"Expected result: ATM has insufficient funds")
    # print(f"Actual result: {result}")
    # print(f"ATM machine balance after: {atm_machine.get_balance()}")
    # print("-------------------------")
    print("\nTest Case 10")
    atm2 = bank.get_atm_machine('1002')  
    harry_account = atm2.insert_card(bank, harry.atm_cards[0], "1234")
    print(f"ATM machine balance before: {atm2.balance}")
    print(f"Attempting to withdraw 250,000 baht...")
    result = atm2.withdraw(harry_account, 250000)
    print(f"Expected result: ATM has insufficient funds")
    print(f"Actual result: {result}")
    print(f"ATM machine balance after: {atm2.balance}")
    print("-------------------------")

test_cases()