import array, collections

class Computer(object):
    def __init__(self):
        super(Computer, self).__init__()
        self.verbose = False
        self.code_lines = 0
        self.code_max = 30
        self.fatal_error = False
        self.prog_counter = 0
        self.stack_maxlen = 5
        self.vars_max = 10
        self.label_code = '69'

        self.address_space = [None] * 40
        self.stack = collections.deque(maxlen=self.stack_maxlen)
        self.methods_dict = {}
        self.errors = {
            'MaxLines' : 'AssemBOA: Load Error - Maximum number of lines reached. Truncating code.\n',
            'UnknownCommand' : 'Unknown Command. Exiting.',
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
        if self.verbose:
            print 'Reading integer to store to address', arg, '...'

        try:
            arg = int(arg)
            if arg < 0 or arg >= self.vars_max:
                print self.errors['WritingToReadOnlyMem']
                self.fatal_error = True
                return
        except ValueError:
            print self.errors['InvalidMemReference']
            self.fatal_error = True

        parsed = False
        while not parsed:
            try:
                integer = raw_input('Enter a number: ')

                integer = int(integer)
                if integer < 0 or integer > 99:
                    print self.errors['Overflow']
                else:
                    self.address_space[- 1 - int(arg)] = integer
                    parsed = True
            except ValueError:
                print self.errors['NotAnInteger']
            except EOFError:
                print self.errors['EOF']
                self.fatal_error = True
                return

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

    def jmp(self, arg):
        try:
            arg = int(arg)
            if arg < 0 or arg >= self.vars_max:
                print self.errors['InvalidMemReference']
                self.fatal_error = True
                return

            self.prog_counter = self.address_space[- 1 - int(arg)]
        except ValueError:
            print self.errors['InvalidMemReference']
            self.fatal_error = True

    def jmpl(self, arg):
        try:
            num1 = self.stack.pop()
            num2 = self.stack.pop()
            result = num1 < num2

            if result:
                arg = int(arg)
                if arg < 0 or arg >= self.vars_max:
                    print self.errors['InvalidMemReference']
                    self.fatal_error = True
                    return

                self.prog_counter = self.address_space[- 1 - int(arg)]
        except IndexError:
            print self.errors['NullOperand']
            self.fatal_error = True
        except ValueError:
            print self.errors['InvalidMemReference']
            self.fatal_error = True

    def jmpg(self, arg):
        try:
            num1 = self.stack.pop()
            num2 = self.stack.pop()
            result = num1 > num2

            if result:
                arg = int(arg)
                if arg < 0 or arg >= self.vars_max:
                    print self.errors['InvalidMemReference']
                    self.fatal_error = True
                    return

                self.prog_counter = self.address_space[- 1 - int(arg)]
        except IndexError:
            print self.errors['NullOperand']
            self.fatal_error = True
        except ValueError:
            print self.errors['InvalidMemReference']
            self.fatal_error = True

    def jeq(self, arg):
        try:
            num1 = self.stack.pop()
            num2 = self.stack.pop()
            result = num1 == num2

            if result:
                arg = int(arg)
                if arg < 0 or arg >= self.vars_max:
                    print self.errors['InvalidMemReference']
                    self.fatal_error = True
                    return
                self.prog_counter = self.address_space[- 1 - int(arg)]
        except IndexError:
            print self.errors['NullOperand']
            self.fatal_error = True
        except ValueError:
            print self.errors['InvalidMemReference']
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

            if self.address_space[idx][0:2] == self.label_code:
                try:
                    self.address_space[- 1 - int(self.address_space[idx][2:4])] = idx
                except IndexError:
                    print self.errors['WritingToReadOnlyMem']
                    self.fatal_error = True
                    return

            self.code_lines += 1

    def run(self, step_by_step = False):
        self.prog_counter = 0
        while self.prog_counter < self.code_lines:
            if self.fatal_error is not True:
                command = self.address_space[self.prog_counter][0:2]
                arg = self.address_space[self.prog_counter][2:4]
                
                try:
                    if step_by_step:
                        print self.address_space[self.prog_counter]
                        print '----', raw_input()

                    if command != self.label_code:
                        self.methods_dict[command](arg)

                except KeyError:
                    print self.errors['UnknownCommand']
                    self.fatal_error = True
                    return

                self.prog_counter += 1

            else:
                break


    def execute(self, file_to_read, step_by_step = False):
        self.methods_dict = {
            '00': self.begin,
            '01': self.read,
            '02': self.disp,
            '03': self.pushi,
            '04': self.pushv,
            '05': self.pop,
            '06': self.mod,
            '07': self.jmp,
            '08': self.jmpl,
            '09': self.jmpg,
            '10': self.jeq,
            '11': self.add,
            '12': self.sub,
            '13': self.compare,
            '99': self.end,
        }

        self.verbose = step_by_step

        self.load_to_mem(file_to_read)

        self.run(step_by_step)
        
