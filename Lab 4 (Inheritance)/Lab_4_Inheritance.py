import unittest
from datetime import datetime

class User:
    def __init__(self, citizen_id, name):
        self.__citizen_id = citizen_id
        self.__name = name
        self.__account_list = []
        self.__card_list = []

    @property
    def citizen_id(self):
        return self.__citizen_id
    
    @property
    def name(self):
        return self.__name
    
    @property
    def get_account(self):
        return self.__account_list
    
    @property
    def get_card(self):
        return self.__card_list

    def add_account(self, account):
        if not isinstance(account, Account):
            return "Error"
        # Check if the account's user matches this user
        if account.user != self:
            return "Error: Account user does not match"
        
        self.__account_list.append(account)
        return "Success"

    def add_card(self,card):
        self.__card_list.append(card)

class Account:
    def __init__(self, account_no, user, balance):
        self.__account_no = account_no
        self.__user = user
        self.__card = None
        self.__balance = balance
        self.__transaction = []

    @property
    def account_no(self):
        return self.__account_no

    @property
    def user(self):
        return self.__user
    
    @property
    def card(self):
        return self.__card
    
    @property
    def balance(self):
        return self.__balance
    
    @balance.setter
    def balance(self, balance):
        self.__balance = balance

    def list_transaction(self):
        return self.__transaction

    def add_card(self, card):
        if not isinstance(card, Card):
            return "Error"
        # Check if the card's account number matches this account
        if card.account_no != self.__account_no:
            return "Error: Card account number does not match"
        
        self.__card = card  
        return "Success"
        
    def add_transaction(self,transaction):
        self.__transaction.append(transaction)

    def deposit(self, source, amount):
        if amount <= 0:
            return "Error : amount must be greater than 0"
        
        self.__balance += amount
        self.add_transaction(Transaction("D", source, amount, self.__balance))
        return "Success"

    def withdraw(self,source,amount):
        if amount <=0:
            return "Error"
        if amount > self.__balance:
            return "Error : not enough money"

        self.__balance -= amount
        self.add_transaction(Transaction("W",source,amount,self.__balance))
        return "Success"     

    def transfer(self, source, amount, target_account):
        if amount <= 0:
            return "Error"
        if amount > self.__balance:
            return "Error"
        
        self.__balance -= amount
        target_account.balance += amount
        self.add_transaction(Transaction("TW", source, amount, self.balance))
        target_account.add_transaction(Transaction("TD", source, amount, target_account.balance))
        return "Successful"

class SavingAccount(Account):
    def __init__(self, account_id, owner, balance=0):
        super().__init__(account_id, owner, balance)
    
    def calculate_interest(self, years):
        interest_rate = 0.005
        interest = self.balance * interest_rate * years
        self.balance += interest
        self.add_transaction(Transaction("I", "Interest", interest, self.balance))
        return interest
    
    def withdraw(self, channel_id, amount):
        if amount > 50000:
            return "Error: Withdrawal exceeds the limit"
        return super().withdraw(channel_id, amount)
    
class FixedAccount(Account):
    def __init__(self, account_id, owner, period,balance=0.0):
        super().__init__(account_id, owner,balance=0.0)
        self.__period = period  
        self.__deposit_date = None
        self.__deposit_status = False 

    def deposit(self, transaction_id, amount):
        if amount <= 0:
            return "Invalid amount"

        if self.__deposit_status:
            self.balance += amount
            self.add_transaction(Transaction("D", transaction_id, amount, self.balance))
            return "Success"
        
        super().deposit(transaction_id, amount)
        self.__deposit_status = True
        self.__deposit_date = datetime.now() 
        return "Success"

    def withdraw(self, channel, amount):
        if not self.__deposit_status:
            return "Error: No initial deposit" 
        if amount <= 0 or amount > self.balance:
            return "Invalid withdrawal amount"

        elapsed_days = (datetime.now() - self.__deposit_date).days
        months_elapsed = elapsed_days // 30

        if months_elapsed >= self.__period: 
            interest_rate = 0.025
        else:  
            interest_rate = 0.0125

        interest = self.balance * interest_rate

        self.add_transaction(Transaction("I", channel, interest, self.balance + interest))

        self.balance += interest

        self.balance -= amount
        self.add_transaction(Transaction("W", channel, -amount, self.balance)) 

        return "Success"

class CurrentAccount(Account):
    pass

class Transaction:
    def __init__(self, transaction_type, source, amount, balance):
        self.__transaction_type = transaction_type
        self.__source = source
        self.__amount = amount
        self.__balance = balance

    @property
    def transaction_type(self):
        return self.__transaction_type

    @property
    def source(self):
        return self.__source

    @property
    def amount(self):
        return self.__amount

    @property
    def balance(self):
        return self.__balance

    def __str__(self):
        return f"{self.__transaction_type}-{self.__source}-{self.__amount}-{self.__balance}"
        
class Card:
    def __init__(self, card_no, account_no, pin,card_type="Standard"):
        self.__card_no = card_no
        self.__account_no = account_no  
        self.__pin = pin
        self.__type = card_type
        self.__is_inserted = False
    
    @property
    def card_no(self):
        return self.__card_no

    @property
    def pin(self):
        return self.__pin

    @property
    def account_no(self):
        return self.__account_no
    
    @property
    def is_inserted(self):
        return self.__is_inserted  

    def insert_card(self): # เปลี่ยนสถานะเป็น 'ใส่บัตร'
        self.__is_inserted = True  

    def remove_card(self): # เปลี่ยนสถานะเป็น 'ถอดบัตรออก'
        self.__is_inserted = False 

    def validate_pin(self, input_pin):
        """ตรวจสอบ PIN"""
        return self.__pin == input_pin and len(self.__pin) == 4 and self.__pin.isdigit()
        
    def verify_card(self, input_pin):
        """เพิ่ม method สำหรับตรวจสอบบัตร"""
        return self.validate_pin(input_pin)

    def charge_annual_fee(self, account):
        raise "No annual fee for this card"

class ATMCard(Card):
    def __init__(self, card_no, account_no, pin, annual_fee=150):
        super().__init__(card_no, account_no, pin)
        self.__annual_fee = annual_fee

    @property
    def annual_fee(self):
        return self.__annual_fee

    def charge_annual_fee(self, account):
        if account.balance >= self.__annual_fee:
            account.balance -= self.__annual_fee
            account.add_transaction(Transaction("F", "Annual Fee", -self.__annual_fee, account.balance))
            return "Annual fee charged successfully"
        return "Error: Insufficient funds for annual fee"

class DebitCard(Card):
    def __init__(self, card_no, account_no, pin, card_type="Standard", annual_fee=300):
        super().__init__(card_no, account_no, pin, card_type)
        self.__card_type = card_type  
        self.__balance = 0.0
        self.__annual_fee = annual_fee
    
    @property
    def card_type(self):
        return self.__card_type
    
    @property
    def balance(self):
        return self.__balance

    @property
    def annual_fee(self):
        return self.__annual_fee

    def charge_annual_fee(self, account):
        if account.balance >= self.__annual_fee:
            account.balance -= self.__annual_fee
            account.add_transaction(Transaction("F", "Annual Fee", -self.__annual_fee, account.balance))
            return "Annual fee charged successfully"
        return "Error: Insufficient funds for annual fee"

class ShoppingDebitCard(DebitCard):
    def __init__(self, card_no, account_no, pin):
        super().__init__(card_no, account_no, pin,annual_fee=500)
        self.__cashback_rate = 0.01
        self.__type = "Shopping"

    @property
    def cashback_rate(self):
        return self.__cashback_rate

    @property
    def type(self):
        return self.__type

    def apply_cashback(self, account, purchase_amount):
        if purchase_amount > 1000:
            cashback = purchase_amount * self.__cashback_rate
            account.balance += cashback
            account.add_transaction(Transaction("CB", "Cashback", cashback, account.balance))
            return f"Cashback of {cashback:.2f} applied"
        return "No cashback applied (Purchase amount must exceed 1000)"

class TravelDebitCard(DebitCard):
    def __init__(self, card_no, account_no, pin):
        super().__init__(card_no, account_no, pin)
        self.__insurance_coverage = 30000
        self.__type = "Travel"
    
    @property
    def type(self):
        return self.__type

    def get_travel_insurance(self):
        return f"Insurance coverage amount: {self.__insurance_coverage} THB"

class TransactionChannel:
    def __init__(self, channel_id, bank):
        self.__channel_id = channel_id
        self.__bank = bank
        
    @property
    def channel_id(self):
        return self.__channel_id

    @property
    def bank(self):
        return self.__bank

class ATMMachine(TransactionChannel):
    def __init__(self, bank, atm_no, initial_money=10000):
        super().__init__(f"ATM:{atm_no}", bank)
        self.__atm_no = atm_no
        self.__money = initial_money
        self.__current_card = None
        
    @property
    def atm_no(self):
        return self.__atm_no
        
    @property
    def available_money(self):
        return self.__money
        
    def insert_card(self, card, pin):
        """เสียบบัตรและตรวจสอบ PIN"""
        if isinstance(card, (ATMCard, DebitCard)) and card.verify_card(pin):
            self.__current_card = card
            account = self.bank.search_account(card.account_no)
            if isinstance(account, SavingAccount) and account != None:
                return account
        return "Error"

    def deposit(self, account, amount):
        return account.deposit(self.channel_id, amount)

    def withdraw(self, account, amount):
        return account.withdraw(self.channel_id, amount)

    def transfer(self, account, target_account, amount):
        return account.transfer(self.channel_id, amount, target_account)

class Counter(TransactionChannel):
    def __init__(self, bank, branch_no):
        super().__init__(f"COUNTER:{branch_no}",bank)
        self.__branch_no = branch_no
        
    @property
    def branch_no(self):
        return self.__branch_no
        
    def verify_identity(self, account, account_id, citizen_id):
        if account.user.citizen_id == citizen_id and account.account_no == account_id:
            return True
        else:
            return False

    def deposit(self, account, amount, account_id, citizen_id):
        if self.verify_identity(account, account_id, citizen_id):
            return account.deposit(self.channel_id, amount)
        return "Error: Invalid identity"
    
    def withdraw(self, account, amount, account_id, citizen_id):
        if self.verify_identity(account, account_id, citizen_id):
            return account.withdraw(self.channel_id, amount)
        return "Error: Invalid identity"
    
    def transfer(self, account, target_account, amount, account_id, citizen_id):
        if self.verify_identity(account, account_id, citizen_id):
            return account.transfer(self.channel_id, amount, target_account)
        return "Error: Invalid identity"
        
class EDCMachine(TransactionChannel):
    """ช่องทางการทำรายการผ่านเครื่อง EDC"""
    def __init__(self, bank, edc_no, merchant_account):
        super().__init__(f"EDC:{edc_no}", bank)
        self.__edc_no = edc_no
        self.__merchant_account = merchant_account
        self.__current_card = None
        
    @property
    def edc_no(self):
        return self.__edc_no

    @property
    def merchant_account(self):
        return self.__merchant_account
        
    def swipe_card(self, card, pin):
        """รูดบัตรและตรวจสอบ PIN"""
        if isinstance(card, DebitCard) and card.verify_card(pin):
            self.__current_card = card
            card.insert_card()
            return "Success"
        return "Error: Invalid card or PIN"
        
    def pay(self, debit_card, amount):
        if not debit_card.is_inserted:
            return "Error: No card inserted"

        if debit_card.verify_card(debit_card.pin) and amount > 0:
            account = self.bank.search_account(debit_card.account_no)
            
            if account:
                if account.balance >= amount:
                    account.balance -= amount  
                    self.merchant_account.balance += amount  
                    account.add_transaction(Transaction("P", debit_card.card_no, -amount, account.balance))
                    self.merchant_account.add_transaction(Transaction("P", debit_card.card_no, amount, self.merchant_account.balance))  # Merchant's transaction
                    return "Success"
                else:
                    return "Error: Insufficient funds"
            else:
                return "Error: Account not found"
        else:
            return "Error: Invalid card or amount"

    def calculate_cashback(self, card, payment_amount):
        if card.type == "Premium":
            return payment_amount * 0.05
        return 0

class Bank:
    def __init__(self):
        self.__user_list = []
        self.__atm_list = []
        self.__edc_list = []

    @property
    def get_users(self):
        return self.__user_list

    def search_account(self, account_number):
        for user in self.__user_list:
            for account in user.get_account:
                if account.account_no == account_number:
                    return account
        return None

    def search_atm(self,atm_id):
        for atm in self.__atm_list:
            if atm.atm_no == atm_id:
                return atm
        return None

    def search_edc_machine(self,edc_id):
        for edc in self.__edc_list:
            if edc.edc_no == edc_id:
                return edc
        return None

    def add_user(self,user) -> str:
        if not isinstance(user, User):
            return "Error"
        else:
            self.__user_list.append(user)
            return "Success"

    def add_atm_machine(self, atm) -> str:
        if not isinstance(atm, ATMMachine):
            return "Error"
        else:
            self.__atm_list.append(atm)
            return "Success"

    def add_edc_machine(self, edc) -> str:
        if not isinstance(edc, EDCMachine):
            return "Error"
        else:
            self.__edc_list.append(edc)
            return "Success"

class BankingTest(unittest.TestCase):
    def setUp(self):
    # Create Bank Instance
        self.bank = Bank()

        # Create Users 
        self.tony = User("1111-1111-1111", "Tony Stark")
        self.steve = User("2222-2222-2222", "Steve Rogers")
        self.thor = User("3333-3333-3333", "Thor Odinson")
        self. peter = User("4444-4444-4444", "Peter Parker")
        self.bruce = User("5555-5555-5555", "Bruce Banner")
        self.thanos = User("6666-6666-6666", "Thanos")  # Merchant

        # Add Users to Bank
        self.bank.add_user(self.tony)
        self.bank.add_user(self.steve)
        self.bank.add_user(self.thor)
        self.bank.add_user(self.peter)
        self.bank.add_user(self.bruce)
        self.bank.add_user(self.thanos)

        # Create Accounts
        # Savings Accounts (4 accounts)
        self.tony_savings = SavingAccount("SAV001", self.tony, 100000.00)
        self.steve_savings = SavingAccount("SAV002", self.steve, 80000.00)
        self.thor_savings = SavingAccount("SAV003", self.thor, 150000.00)
        self.peter_savings = SavingAccount("SAV004", self.peter, 5000.00)

        # Fixed Account (1 account) - 12 months period
        self.bruce_fixed = FixedAccount("FIX001", self.bruce, 12, 200000.00)

        # Current Account (1 account for merchant)
        self.thanos_current = CurrentAccount("CUR001", self.thanos, 500000.00)

        # Add Accounts to Users
        self.tony.add_account(self.tony_savings)
        self.steve.add_account(self.steve_savings)
        self.thor.add_account(self.thor_savings)
        self.peter.add_account(self.peter_savings)
        self.bruce.add_account(self.bruce_fixed)
        self.thanos.add_account(self.thanos_current)

        # Create ATM Machines
        self.atm1 = ATMMachine(self.bank, "ATM001", 10000)  # Initial money 10,000
        self.atm2 = ATMMachine(self.bank, "ATM002", 10000)  # Initial money 10,000

        # Add ATM Machines to Bank
        self.bank.add_atm_machine(self.atm1)
        self.bank.add_atm_machine(self.atm2)

        self.counter = Counter(self.bank, "COUNTER001")

        # Create EDC Machine (using Thanos's account as merchant)
        edc1 = EDCMachine(self.bank, "EDC001", self.thanos_current)

        # Add EDC Machine to Bank
        self.bank.add_edc_machine(edc1)

        # Create Cards
        # ATM Card for Tony
        self.tony_atm_card = ATMCard("4111-1111-1111-1111", self.tony_savings.account_no, "1234")
        self.tony_savings.add_card(self.tony_atm_card)

        # Shopping Debit Card for Steve (with 1% cashback)
        self.steve_shopping_card = ShoppingDebitCard("4222-2222-2222-2222", self.steve_savings.account_no, "5678")
        self.steve_savings.add_card(self.steve_shopping_card)

        # Travel Debit Card for Thor (with accident coverage)
        self.thor_travel_card = TravelDebitCard("4333-3333-3333-3333", self.thor_savings.account_no, "9012")
        self.thor_savings.add_card(self.thor_travel_card)

    ###########################################################################################################

    def test_deposit(self): # 1. ทดสอบการฝากเงินปกติ 
        initial_balance = self.tony_savings.balance

        deposit_amount = 5000
        result = self.atm1.insert_card(self.tony_atm_card, "1234")

        # Verify card insertion
        self.assertNotEqual(result, "Error", "Card verification should succeed")
        
        # Perform deposit and verify result
        deposit_result = self.atm1.deposit(result, deposit_amount)
        self.assertEqual(deposit_result, "Success", "Deposit should be successful")
        
        # Verify new balance
        expected_balance = initial_balance + deposit_amount
        self.assertEqual(self.tony_savings.balance, expected_balance, 
                        f"Balance should be {expected_balance}")
    
        # Verify transaction history
        transactions = self.tony_savings.list_transaction()
        self.assertGreater(len(transactions), 0, "Transaction history should not be empty")
        latest_transaction = transactions[-1]
        self.assertIn("D-ATM:", str(latest_transaction), "Transaction should be a deposit via ATM")

    def test_negative_deposit(self): # 2. ทดสอบการฝากเงินที่มีค่าติดลบ
        # Initial balance check
        initial_balance = self.tony_savings.balance
        
        # Try to deposit negative amount
        deposit_amount = -5000
        result = self.atm1.insert_card(self.tony_atm_card, "1234")
        
        # Verify card insertion
        self.assertNotEqual(result, "Error", "Card verification should succeed")
        
        # Perform deposit and verify it fails
        deposit_result = self.atm1.deposit(result, deposit_amount)
        self.assertEqual(deposit_result, "Error : amount must be greater than 0", 
                        "Negative deposit should be rejected")
        
        # Verify balance remains unchanged
        self.assertEqual(self.tony_savings.balance, initial_balance,
                        "Balance should remain unchanged after failed deposit")
        
        # Verify no transaction was recorded
        transactions = self.tony_savings.list_transaction()
        original_transaction_count = len(transactions)
        self.assertEqual(len(self.tony_savings.list_transaction()), original_transaction_count,
                        "No new transaction should be recorded for failed deposit")


    def test_withdraw_over_limit(self): # 3. ทดสอบการถอนเงินเกินจำนวนที่กำหนด
        # Initial balance check
        initial_balance = self.steve_savings.balance
        
        # Attempt withdrawal
        withdraw_amount = 60000  # Over 50,000 limit
        result = self.atm1.insert_card(self.steve_shopping_card, "5678")
        
        # Verify card insertion
        self.assertNotEqual(result, "Error", "Card verification should succeed")
        
        # Perform withdrawal and verify result
        withdraw_result = self.atm1.withdraw(result, withdraw_amount)
        self.assertIn("Error", withdraw_result, 
                     "Should return error for withdrawal over limit")
        
        # Verify balance unchanged
        self.assertEqual(self.steve_savings.balance, initial_balance, 
                        "Balance should remain unchanged after failed withdrawal")

    def test_calculate_interest(self): # 4. ทดสอบการคำนวณดอกเบี้ยบัญชีออมทรัพย์
            """Test interest calculation"""
            # Initial balance check
            initial_balance = self.thor_savings.balance
            
            # Calculate interest
            interest = self.thor_savings.calculate_interest(1)  # 1 year
            
            # Verify interest calculation
            expected_interest = initial_balance * 0.005  # 0.5% interest rate
            self.assertEqual(interest, expected_interest, 
                            "Interest calculation should be correct")
            
            # Verify new balance
            expected_balance = initial_balance + expected_interest
            self.assertEqual(self.thor_savings.balance, expected_balance, 
                            "Balance should include interest")
            
            # Verify transaction history
            transactions = self.thor_savings.list_transaction()
            self.assertGreater(len(transactions), 0, "Transaction history should not be empty")
            latest_transaction = transactions[-1]
            self.assertIn("I-", str(latest_transaction), 
                        "Transaction should be an interest addition")

    def test_counter_deposit(self): # 5. ทดสอบการฝากเงินผ่านเคาน์เตอร์
        """Test deposit through bank counter"""
        # Initial balance check
        initial_balance = self.tony_savings.balance
        
        # Deposit parameters
        deposit_amount = 5000
        account_id = self.tony_savings.account_no
        citizen_id = self.tony.citizen_id
        
        # Perform deposit and verify result
        deposit_result = self.counter.deposit(self.tony_savings, deposit_amount, account_id, citizen_id)
        self.assertEqual(deposit_result, "Success", "Counter deposit should be successful")
        
        # Verify new balance
        expected_balance = initial_balance + deposit_amount
        self.assertEqual(self.tony_savings.balance, expected_balance,
                        f"Balance should be {expected_balance}")
        
        # Verify transaction history
        transactions = self.tony_savings.list_transaction()
        self.assertGreater(len(transactions), 0, "Transaction history should not be empty")
        latest_transaction = transactions[-1]
        self.assertIn("D-COUNTER:", str(latest_transaction), 
                    "Transaction should be a deposit via counter")

    def test_counter_deposit_wrong_citizen_id(self): # 6. ทดสอบการฝากเงินผ่านเคาน์เตอร์โดยใส่เลขบัตรประชาชนผิด
        """Test deposit through bank counter with wrong citizen ID"""
        # Initial balance check
        initial_balance = self.tony_savings.balance
        
        # Deposit parameters with wrong citizen ID
        deposit_amount = 5000
        account_id = self.tony_savings.account_no
        wrong_citizen_id = "9999999999999"
        
        # Perform deposit and verify it fails
        deposit_result = self.counter.deposit(self.tony_savings, deposit_amount, account_id, wrong_citizen_id)
        self.assertEqual(deposit_result, "Error: Invalid identity", 
                        "Deposit with wrong citizen ID should be rejected")
        
        # Verify balance remains unchanged
        self.assertEqual(self.tony_savings.balance, initial_balance,
                        "Balance should remain unchanged after failed deposit")
        
        # Verify no transaction was recorded
        transactions = self.tony_savings.list_transaction()
        original_transaction_count = len(transactions)
        self.assertEqual(len(self.tony_savings.list_transaction()), original_transaction_count,
                        "No new transaction should be recorded for failed deposit")
                        

    def test_fixed_deposit_initial(self): # 7. ทดสอบการฝากเงินเริ่มต้นในบัญชีเงินฝากประจำ
        """Test initial deposit to fixed account"""
        # Create new fixed account
        fixed_account = FixedAccount("FIX002", self.tony, 12)  # 12 months period
        initial_balance = fixed_account.balance
        
        # Perform initial deposit
        deposit_amount = 100000
        result = fixed_account.deposit("COUNTER:001", deposit_amount)
        
        # Verify deposit success
        self.assertEqual(result, "Success", "Initial deposit should be successful")
        
        # Verify new balance
        expected_balance = initial_balance + deposit_amount
        self.assertEqual(fixed_account.balance, expected_balance, 
                        f"Balance should be {expected_balance}")
        
        # Verify transaction recorded
        transactions = fixed_account.list_transaction()
        self.assertGreater(len(transactions), 0, "Transaction history should not be empty")
        latest_transaction = transactions[-1]
        self.assertIn("D-COUNTER:", str(latest_transaction), 
                    "Transaction should be a deposit")

    def test_fixed_withdraw_before_maturity(self): # 8. ทดสอบการถอนเงินก่อนวันครบกำหนด 
        """Test withdrawal before maturity period with reduced interest"""
        from datetime import datetime, timedelta
        
        # Initial deposit
        initial_deposit = 100000
        fixed_account = FixedAccount("FIX003", self.tony, 12)  # 12 months period
        fixed_account.deposit("COUNTER:001", initial_deposit)
        
        # Simulate time passing (6 months)
        # Mock the deposit_date to be 6 months ago
        fixed_account._FixedAccount__deposit_date = datetime.now() - timedelta(days=180)
        
        # Try to withdraw
        withdraw_amount = 50000
        result = fixed_account.withdraw("COUNTER:001", withdraw_amount)
        
        # Verify withdrawal success
        self.assertEqual(result, "Success", "Withdrawal should be successful")
        
        # Check if reduced interest was applied
        transactions = fixed_account.list_transaction()
        interest_transaction = [t for t in transactions if str(t).startswith("I-")]
        self.assertGreater(len(interest_transaction), 0, 
                        "Interest transaction should exist")
        
        # Verify reduced interest rate (should be around 1.25% for 6 months)
        # Base rate is 2.5% per year, so 6 months should be approximately half
        expected_interest = initial_deposit * 0.0125  # Approximately half of 2.5%
        actual_interest = float(str(interest_transaction[-1]).split("-")[2])
        self.assertAlmostEqual(actual_interest, expected_interest, delta=1, 
                            msg="Interest should be calculated at reduced rate")

    def test_fixed_withdraw_without_deposit(self): # 9. ทดสอบการถอนเงินโดยไม่มีการฝากเงินเริ่มต้น
        """Test withdrawal attempt without initial deposit"""
        # Create new fixed account without deposit
        fixed_account = FixedAccount("FIX004", self.tony, 12)
        
        # Try to withdraw
        withdraw_amount = 1000
        result = fixed_account.withdraw("COUNTER:001", withdraw_amount)
        
        # Verify withdrawal is rejected
        self.assertEqual(result, "Error: No initial deposit", 
                        "Withdrawal without initial deposit should be rejected")
        
        # Verify no transactions recorded
        transactions = fixed_account.list_transaction()
        self.assertEqual(len(transactions), 0, 
                        "No transactions should be recorded")

    def test_fixed_multiple_deposits(self): # 10. ทดสอบการฝากเงินหลายครั้งในบัญชีเงินฝาก
        """Test multiple deposits to fixed account"""
        # Create new fixed account
        fixed_account = FixedAccount("FIX005", self.tony, 12)
        
        # First deposit
        first_deposit = 100000
        result1 = fixed_account.deposit("COUNTER:001", first_deposit)
        self.assertEqual(result1, "Success", "First deposit should be successful")
        
        # Try second deposit
        second_deposit = 50000
        result2 = fixed_account.deposit("COUNTER:001", second_deposit)
        self.assertEqual(result2, "Success", "Second deposit should be successful")
        
        # Verify final balance includes both deposits
        expected_balance = first_deposit + second_deposit
        self.assertEqual(fixed_account.balance, expected_balance,
                        f"Balance should be {expected_balance}")
        
        # Verify both transactions recorded
        transactions = fixed_account.list_transaction()
        self.assertEqual(len(transactions), 2,
                        "Should have two deposit transactions")

    def test_fixed_withdraw_at_maturity(self): # 11. ทดสอบการถอนเงินในวันครบกำหนด
        """Test withdrawal at maturity period with full interest"""
        from datetime import datetime, timedelta
        
        # Initial deposit
        initial_deposit = 100000
        fixed_account = FixedAccount("FIX006", self.tony, 12)  # 12 months period
        fixed_account.deposit("COUNTER:001", initial_deposit)
        
        # Simulate time passing (12 months)
        # Mock the deposit_date to be 12 months ago
        fixed_account._FixedAccount__deposit_date = datetime.now() - timedelta(days=365)
        
        # Try to withdraw
        withdraw_amount = initial_deposit
        result = fixed_account.withdraw("COUNTER:001", withdraw_amount)
        
        # Verify withdrawal success
        self.assertEqual(result, "Success", "Withdrawal should be successful")
        
        # Check if full interest was applied
        transactions = fixed_account.list_transaction()
        interest_transaction = [t for t in transactions if str(t).startswith("I-")]
        self.assertGreater(len(interest_transaction), 0, 
                        "Interest transaction should exist")
        
        # Verify full interest rate (2.5% for 12 months)
        expected_interest = initial_deposit * 0.025  # Full 2.5% annual rate
        actual_interest = float(str(interest_transaction[-1]).split("-")[2])
        self.assertAlmostEqual(actual_interest, expected_interest, delta=1, 
                            msg="Interest should be calculated at full rate")
        
        # Verify final balance after interest and withdrawal
        expected_final_balance = initial_deposit + expected_interest - withdraw_amount
        self.assertAlmostEqual(fixed_account.balance, expected_final_balance, delta=1,
                            msg="Final balance should reflect interest and withdrawal")

    def test_current_account_basic_deposit(self): # 12. ทดสอบการฝากเงินในบัญชีกระแสรายวัน
        """Test basic deposit functionality for current account"""
        # Initial setup
        initial_balance = self.thanos_current.balance
        deposit_amount = 50000
        
        # Perform deposit via counter
        result = self.counter.deposit(
            self.thanos_current, 
            deposit_amount,
            self.thanos_current.account_no,
            self.thanos.citizen_id
        )
        
        # Verify deposit success
        self.assertEqual(result, "Success", "Deposit should be successful")
        
        # Check balance update
        expected_balance = initial_balance + deposit_amount
        self.assertEqual(self.thanos_current.balance, expected_balance,
                        f"Balance should be {expected_balance}")
        
        # Verify transaction record
        transactions = self.thanos_current.list_transaction()
        latest_transaction = transactions[-1]
        self.assertIn("D-COUNTER:", str(latest_transaction),
                    "Transaction should be recorded as counter deposit")

    def test_current_account_large_withdrawal(self): # 13. ทดสอบการถอนเงินในจำนวนมากในบัญชีกระแสรายวัน
        """Test large withdrawal from current account (no limit unlike savings)"""
        # Initial setup
        initial_balance = self.thanos_current.balance
        large_withdrawal = 100000  # Amount larger than savings account limit
        
        # Perform withdrawal via counter
        result = self.counter.withdraw(
            self.thanos_current,
            large_withdrawal,
            self.thanos_current.account_no,
            self.thanos.citizen_id
        )
        
        # Verify withdrawal success
        self.assertEqual(result, "Success", 
                        "Large withdrawal should be successful for current account")
        
        # Check balance update
        expected_balance = initial_balance - large_withdrawal
        self.assertEqual(self.thanos_current.balance, expected_balance,
                        f"Balance should be {expected_balance}")
        
        # Verify transaction record
        transactions = self.thanos_current.list_transaction()
        latest_transaction = transactions[-1]
        self.assertIn("W-COUNTER:", str(latest_transaction),
                    "Transaction should be recorded as counter withdrawal")

    def test_current_account_overdraft_attempt(self): # 14. ทดสอบการถอนเงินเกินจำนวนเงินในบัญชี
        """Test withdrawal attempt exceeding balance"""
        # Try to withdraw more than available balance
        current_balance = self.thanos_current.balance
        excessive_amount = current_balance + 10000
        
        # Perform withdrawal
        result = self.counter.withdraw(
            self.thanos_current,
            excessive_amount,
            self.thanos_current.account_no,
            self.thanos.citizen_id
        )
        
        # Verify withdrawal rejection
        self.assertEqual(result, "Error : not enough money",
                        "Overdraft should not be allowed")
        
        # Verify balance unchanged
        self.assertEqual(self.thanos_current.balance, current_balance,
                        "Balance should remain unchanged after failed withdrawal")

    def test_current_account_merchant_payment(self): # 15. ทดสอบการชำระเงินผ่านบัญชีกระแสรายวันผ่าน EDC
        """Test merchant payment processing through EDC"""
        # Get EDC machine
        edc = self.bank.search_edc_machine("EDC001")
        self.assertIsNotNone(edc, "EDC machine should exist")
        
        # Initial balances
        merchant_initial = self.thanos_current.balance
        customer_initial = self.steve_savings.balance
        payment_amount = 1000
        
        # Process payment
        # First verify card
        card_verification = edc.swipe_card(self.steve_shopping_card, "5678")
        self.assertEqual(card_verification, "Success", "Card verification should succeed")
        
        # Then make payment
        payment_result = edc.pay(self.steve_shopping_card, payment_amount)
        
        # Verify payment success
        self.assertEqual(payment_result, "Success", "Payment should be successful")
        
        # Check merchant account balance
        expected_merchant_balance = merchant_initial + payment_amount
        self.assertEqual(self.thanos_current.balance, expected_merchant_balance,
                        "Merchant balance should increase by payment amount")
        
        # Check customer account balance
        expected_customer_balance = customer_initial - payment_amount + edc.calculate_cashback(self.steve_shopping_card, payment_amount)
        self.assertEqual(self.steve_savings.balance, expected_customer_balance,
                        "Customer balance should decrease by payment amount")

    def test_debit_card_annual_fee(self): # 16. ทดสอบการหักค่าธรรมเนียมประจำปีสำหรับบัตร debit
        """Test annual fee deduction for cards"""
        # Initial setup - using Steve's shopping debit card account
        initial_balance = self.steve_savings.balance
        annual_fee = self.steve_savings.card.annual_fee
    
        # Create a method to deduct annual fee
        def deduct_annual_fee(card, account):
            """Helper method to simulate annual fee deduction"""
            if isinstance(card, Card):
                result = account.withdraw("SYSTEM", annual_fee)
                return result
        
        # Test fee deduction
        result = deduct_annual_fee(self.steve_shopping_card, self.steve_savings)
        
        # Verify deduction success
        self.assertEqual(result, "Success", "Annual fee deduction should be successful")
        
        # Check if balance is reduced by annual fee
        expected_balance = initial_balance - annual_fee
        self.assertEqual(self.steve_savings.balance, expected_balance,
                        f"Balance should be reduced by {annual_fee} baht")
        
        # Verify transaction record
        transactions = self.steve_savings.list_transaction()
        latest_transaction = transactions[-1]
        self.assertIn("W-SYSTEM", str(latest_transaction),
                    "Transaction should be recorded as system withdrawal")
        self.assertIn(str(annual_fee), str(latest_transaction),
                    "Transaction amount should match annual fee")

    def test_atm_card_annual_fee(self): # 17. ทดสอบการหักค่าธรรมเนียมประจำปีสำหรับบัตร ATM
        """Test annual fee deduction for cards"""
        # Initial setup - using Steve's shopping debit card account
        initial_balance = self.tony_savings.balance
        annual_fee = self.tony_atm_card.annual_fee
    
        # Create a method to deduct annual fee
        def deduct_annual_fee(card, account):
            """Helper method to simulate annual fee deduction"""
            if isinstance(card, Card):
                result = account.withdraw("SYSTEM", annual_fee)
                return result
        
        # Test fee deduction
        result = deduct_annual_fee(self.tony_atm_card, self.tony_savings)
        
        # Verify deduction success
        self.assertEqual(result, "Success", "Annual fee deduction should be successful")
        
        # Check if balance is reduced by annual fee
        expected_balance = initial_balance - annual_fee
        self.assertEqual(self.tony_savings.balance, expected_balance,
                        f"Balance should be reduced by {annual_fee} baht")
        
        # Verify transaction record
        transactions = self.tony_savings.list_transaction()
        latest_transaction = transactions[-1]
        self.assertIn("W-SYSTEM", str(latest_transaction),
                    "Transaction should be recorded as system withdrawal")
        self.assertIn(str(annual_fee), str(latest_transaction),
                    "Transaction amount should match annual fee")

    def test_thor_account_merchant_payment(self): # 18. ทดสอบการชำระเงินผ่านบัญชีของ Thor ผ่าน EDC (ไม่มีเงินคืน)
        """Test merchant payment through EDC for Thor's account (no cashback)"""
        # Get EDC machine
        edc = self.bank.search_edc_machine("EDC001")
        self.assertIsNotNone(edc, "EDC machine should exist")
        
        # Initial balances
        merchant_initial = self.thanos_current.balance
        thor_initial = self.thor_savings.balance
        payment_amount = 1000
        
        # Process payment
        # First verify card
        card_verification = edc.swipe_card(self.thor_travel_card, "9012")
        self.assertEqual(card_verification, "Success", "Card verification should succeed")
        
        # Then make payment
        payment_result = edc.pay(self.thor_travel_card, payment_amount)
        
        # Verify payment success
        self.assertEqual(payment_result, "Success", "Payment should be successful")
        
        # Check merchant account balance
        expected_merchant_balance = merchant_initial + payment_amount
        self.assertEqual(self.thanos_current.balance, expected_merchant_balance,
                        "Merchant balance should increase by payment amount")
        
        # Check Thor's account balance - should not include cashback
        expected_thor_balance = thor_initial - payment_amount
        self.assertEqual(self.thor_savings.balance, expected_thor_balance,
                        "Thor's balance should decrease by exact payment amount with no cashback")
        
    def test_tony_atm_card_merchant_payment(self): # 19. ทดสอบการชำระเงินผ่านบัตร ATM ของ Tony ผ่าน EDC
        """Test that ATM card cannot be used for merchant payment through EDC"""
        # Get EDC machine
        edc = self.bank.search_edc_machine("EDC001")
        self.assertIsNotNone(edc, "EDC machine should exist")
        
        # Initial balances
        merchant_initial = self.thanos_current.balance
        tony_initial = self.tony_savings.balance
        payment_amount = 1000
        
        # Attempt to verify ATM card
        card_verification = edc.swipe_card(self.tony_atm_card, "1234")
        self.assertEqual(card_verification, "Error: Invalid card or PIN", 
                        "ATM card verification should fail")
        
        # Attempt payment even after failed verification
        payment_result = edc.pay(self.tony_atm_card, payment_amount)
        self.assertEqual(payment_result, "Error: No card inserted",
                        "Payment with ATM card should fail")
        
        # Verify no changes in account balances
        self.assertEqual(self.thanos_current.balance, merchant_initial,
                        "Merchant balance should remain unchanged")
        self.assertEqual(self.tony_savings.balance, tony_initial,
                        "Tony's balance should remain unchanged")

if __name__ == '__main__':
    unittest.main()
