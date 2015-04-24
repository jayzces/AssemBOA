import array, collections

class Computer(object):
    def __init__(self):
        super(Computer, self).__init__()
        self.stack_maxlen = 5
        self.code_max = 30
        self.vars_max = 10
        self.fatal_error = False
        self.address_space = [None] * 40
        self.stack = collections.deque(maxlen=self.stack_maxlen)
        self.methods_dict = {}
        self.errors = {
            'MaxLines' : 'AssemBOA: Load Error - Maximum number of lines reached. Truncating code.\n',
            'NotAnInteger' : 'Invalid argument: not an integer.',
            'EOF' : 'EOFError: Reached an end-of-file condition. Exiting.',
            'Overflow' : 'Overflow Error: Argument or result is lesser than 0 or greater than 99.',
            'NullOperand' : 'Null Operand Error: Needed operand does not exist.',
            'StackUnderflow' : 'Fatal Error: Stack Underflow.',
            'StackOverflow' : 'Fatal Error: Stack Overflow.',
            'UndefinedVariable' : 'Fatal Error: Undefined Variable',
            'InvalidMemReference' : 'Fatal Error: Segmentation Fault - Invalid memory reference.',
            'WritingToReadOnlyMem' : 'Fatal Error: Segmentation Fault - Writing to read-only memory.',
        }

    def begin(self, arg):
        print 'AssemBOA: Executing code...'
        print '-------------------------------\n'

    def end(self, arg):
        print '\n-------------------------------'
        print 'AssemBOA: Execution finished...'

    def read(self, arg):
        try:
            arg = int(arg)
            if arg < 0 or arg >= self.vars_max:
                print self.errors['WritingToReadOnlyMem']
                self.fatal_error = True
                return
        except ValueError:
            print self.errors['InvalidMemReference']
            self.fatal_error = True

        try:
            integer = raw_input('Enter a number: ')

            while len(integer) < 1 or len(integer) > 2:
                integer = int(integer)
                if integer < 0 or integer > 99:
                    print self.errors['Overflow']
                integer = raw_input('Enter a number: ')

            self.address_space[- 1 - int(arg)] = integer
        except ValueError:
            print self.errors['NotAnInteger']
        except EOFError:
            print self.errors['EOF']
            self.fatal_error = True

    def disp(self, arg):
        try:
            arg = int(arg)
            if arg < 0 or arg >= self.vars_max:
                print self.errors['InvalidMemReference']
                self.fatal_error = True
                return

            print self.address_space[-1 - arg]
        except ValueError:
            print self.errors['InvalidMemReference']
            self.fatal_error = True

    def pushi(self, arg):
        try:
            arg = int(arg)

            if arg < 0 or arg > 99:
                print self.errors['Overflow']
                self.fatal_error = True
                return

            if len(self.stack) >= self.stack_maxlen:
                print self.errors['StackOverflow']
                self.fatal_error = True
                return

            self.stack.append(arg)
        except ValueError:
            print self.errors['InvalidMemReference']
            self.fatal_error = True

    def pushv(self, arg):
        try:
            arg = int(arg)

            if arg < 0 or arg >= self.vars_max:
                print self.errors['UndefinedVariable']
                self.fatal_error = True
                return

            if len(self.stack) >= self.stack_maxlen:
                print self.errors['StackOverflow']
                self.fatal_error = True
                return

            self.stack.append(self.address_space[- 1 - int(arg)])
        except ValueError:
            print self.errors['InvalidMemReference']
            self.fatal_error = True

    def pop(self, arg):
        try:
            arg = int(arg)
            if arg < 0 or arg >= self.vars_max:
                print self.errors['WritingToReadOnlyMem']
                self.fatal_error = True
                return

            self.address_space[- 1 - int(arg)] = self.stack.pop()
        except ValueError:
            print self.errors['InvalidMemReference']
            self.fatal_error = True
        except IndexError:
            print self.errors['StackUnderflow']
            self.fatal_error = True

    def mod(self, arg):
        try:
            num1 = self.stack.pop()
            num2 = self.stack.pop()
            result = num2 % num1
            self.stack.append(result)
        except IndexError:
            print self.errors['NullOperand']
            self.fatal_error = True

    def add(self, arg):
        try:
            num1 = self.stack.pop()
            num2 = self.stack.pop()
            result = num2 + num1

            if result > 99:
                print self.errors['Overflow']
                self.fatal_error = True
                return

            self.stack.append(result)
        except IndexError:
            print self.errors['NullOperand']
            self.fatal_error = True

    def sub(self, arg):
        try:
            num1 = self.stack.pop()
            num2 = self.stack.pop()
            result = num2 - num1

            if result < 0:
                print self.errors['Overflow']
                self.fatal_error = True
                return

            self.stack.append(result)
        except IndexError:
            print self.errors['NullOperand']
            self.fatal_error = True

    def compare(self, arg):
        try:
            num1 = self.stack.pop()
            num2 = self.stack.pop()
            result = num2 == num1

            if result:
                self.stack.append(1)
            else:
                self.stack.append(0)
            
        except IndexError:
            print self.errors['NullOperand']
            self.fatal_error = True

    def load_to_mem(self, file_to_read):
        machine_code = open(file_to_read, 'rb')
        for idx, line in enumerate(machine_code):
            if idx >= self.code_max:
                print self.errors['MaxLines']
                return
            self.address_space[idx] = line.strip()

    def execute(self, file_to_read):        
        self.methods_dict = {
            '00': self.begin,
            '01': self.read,
            '02': self.disp,
            '03': self.pushi,
            '04': self.pushv,
            '05': self.pop,
            '06': self.mod,
            # '07': self.jmp,
            # '08': self.jl,
            # '09': self.jg,
            # '10': self.jeq,
            '11': self.add,
            '12': self.sub,
            '13': self.compare,
            '99': self.end,
        }

        self.load_to_mem(file_to_read)

        for code in self.address_space:
            if self.fatal_error is not True and code is not None:
                command = code[0:2]
                arg = code[2:4]
                self.methods_dict[command](arg)
            else:
                break
