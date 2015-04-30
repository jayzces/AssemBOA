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
        self.output = ''
        self.output_message = ''
        self.exec_log = []

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
        # print 'AssemBOA: Executing code...'
        # print '-------------------------------\n'
        return 'AssemBOA - Begin: Executing code...'

    def end(self, arg):
        # print '\n-------------------------------'
        # print 'AssemBOA: Execution finished...'
        return 'AssemBOA - End: Execution finished...'

    def read(self, arg):
        try:
            arg = int(arg)
            if arg < 0 or arg >= self.vars_max:
                self.fatal_error = True
                self.output = self.errors['WritingToReadOnlyMem']
                return self.errors['WritingToReadOnlyMem']
                return
        except ValueError:
            self.fatal_error = True
            self.output = self.errors['InvalidMemReference']
            return self.errors['InvalidMemReference']

        parsed = False
        while not parsed:
            try:
                integer = raw_input('Enter a number: ')

                integer = int(integer)
                if integer < 0 or integer > 99:
                    self.output = self.errors['Overflow']
                else:
                    self.address_space[- 1 - int(arg)] = integer
                    parsed = True
            except ValueError:
                self.output = self.errors['NotAnInteger']
                return self.errors['NotAnInteger']
            except EOFError:
                self.fatal_error = True
                self.output = self.errors['EOF']
                return self.errors['EOF']

        return 'AssemBOA - Read (' + str(self.address_space[self.prog_counter]) + '): Stored value ' + str(integer) + ' in address ' + str(arg).zfill(2)

    def disp(self, arg):
        try:
            arg = int(arg)
            if arg < 0 or arg >= self.vars_max:
                self.fatal_error = True
                self.output = self.errors['InvalidMemReference']
                return self.errors['InvalidMemReference']

            # print self.address_space[-1 - arg]
            self.output = str(self.address_space[-1 - arg])
            return 'AssemBOA - Display (' + str(self.address_space[self.prog_counter]) + '): Value at address ' + str(arg).zfill(2) + ' is ' + str(self.address_space[-1 - arg])
        except ValueError:
            self.fatal_error = True
            self.output = self.errors['InvalidMemReference']
            return self.errors['InvalidMemReference']

    def pushi(self, arg):
        try:
            arg = int(arg)

            if arg < 0 or arg > 99:
                self.fatal_error = True
                self.output = self.errors['Overflow']
                return self.errors['Overflow']

            if len(self.stack) >= self.stack_maxlen:
                self.fatal_error = True
                self.output = self.errors['StackOverflow']
                return self.errors['StackOverflow']

            self.stack.append(arg)
            return 'AssemBOA - Push Integer to Stack (' + str(self.address_space[self.prog_counter]) + '): Pushed value ' + str(arg) + ' to stack.'
        except ValueError:
            self.fatal_error = True
            self.output = self.errors['InvalidMemReference']
            return self.errors['InvalidMemReference']

    def pushv(self, arg):
        try:
            arg = int(arg)

            if arg < 0 or arg >= self.vars_max:
                self.fatal_error = True
                self.output = self.errors['UndefinedVariable']
                return self.errors['UndefinedVariable']

            if len(self.stack) >= self.stack_maxlen:
                self.fatal_error = True
                self.output = self.errors['StackOverflow']
                return self.errors['StackOverflow']

            self.stack.append(self.address_space[- 1 - int(arg)])
            return 'AssemBOA - Push Variable Value to Stack (' + str(self.address_space[self.prog_counter]) + '): Pushed value ' + str(self.address_space[- 1 - int(arg)]) + ' at address ' + str(arg).zfill(2) + ' to stack.'
        except ValueError:
            self.fatal_error = True
            self.output = self.errors['InvalidMemReference']
            return self.errors['InvalidMemReference']

    def pop(self, arg):
        try:
            arg = int(arg)
            if arg < 0 or arg >= self.vars_max:
                self.fatal_error = True
                self.output = self.errors['WritingToReadOnlyMem']
                return self.errors['WritingToReadOnlyMem']

            self.address_space[- 1 - int(arg)] = self.stack.pop()
            return 'AssemBOA - Pop Value from Stack (' + str(self.address_space[self.prog_counter]) + '): Stored pop value ' + str(self.address_space[- 1 - int(arg)]) + ' from stack to address ' + str(arg).zfill(2)
        except ValueError:
            self.fatal_error = True
            self.output = self.errors['InvalidMemReference']
            return self.errors['InvalidMemReference']
        except IndexError:
            self.fatal_error = True
            self.output = self.errors['StackUnderflow']
            return self.errors['StackUnderflow']

    def mod(self, arg):
        try:
            num1 = self.stack.pop()
            num2 = self.stack.pop()
            result = num2 % num1
            self.stack.append(result)
            return 'AssemBOA - Mod (' + str(self.address_space[self.prog_counter]) + '): ' + str(num2) + ' % ' + str(num1) + ' = ' + str(result)
        except IndexError:
            self.fatal_error = True
            self.output = self.errors['NullOperand']
            return self.errors['NullOperand']

    def jmp(self, arg):
        try:
            arg = int(arg)
            if arg < 0 or arg >= self.vars_max:
                self.fatal_error = True
                self.output = self.errors['InvalidMemReference']
                return self.errors['InvalidMemReference']

            self.prog_counter = self.address_space[- 1 - int(arg)]
            return 'AssemBOA - Jump to Address (' + str(self.address_space[self.prog_counter]) + '): Jumped to line ' + str(self.prog_counter + 1)
        except ValueError:
            self.fatal_error = True
            self.output = self.errors['InvalidMemReference']
            return self.errors['InvalidMemReference']

    def jmpl(self, arg):
        try:
            num1 = self.stack.pop()
            num2 = self.stack.pop()
            result = num1 < num2

            if result:
                arg = int(arg)
                if arg < 0 or arg >= self.vars_max:
                    self.fatal_error = True
                    self.output = self.errors['InvalidMemReference']
                    return self.errors['InvalidMemReference']

                self.prog_counter = self.address_space[- 1 - int(arg)]
                return 'AssemBOA - Jump if Less Than (' + str(self.address_space[self.prog_counter]) + '): Jumped to line ' + str(self.prog_counter + 1) + ' because ' + str(num1) + ' < ' + str(num2)
            else:
                return 'AssemBOA - Jump if Equal (' + str(self.address_space[self.prog_counter]) + '): Did not jump to line ' + str(self.prog_counter + 1) + ' because ' + str(num1) + ' !< ' + str(num2)
        except IndexError:
            self.fatal_error = True
            self.output = self.errors['NullOperand']
            return self.errors['NullOperand']
        except ValueError:
            self.fatal_error = True
            self.output = self.errors['InvalidMemReference']
            return self.errors['InvalidMemReference']

    def jmpg(self, arg):
        try:
            num1 = self.stack.pop()
            num2 = self.stack.pop()
            result = num1 > num2

            if result:
                arg = int(arg)
                if arg < 0 or arg >= self.vars_max:
                    self.fatal_error = True
                    self.output = self.errors['InvalidMemReference']
                    return self.errors['InvalidMemReference']

                self.prog_counter = self.address_space[- 1 - int(arg)]
                return 'AssemBOA - Jump if Greater Than (' + str(self.address_space[self.prog_counter]) + '): Jumped to line ' + str(self.prog_counter + 1) + ' because ' + str(num1) + ' > ' + str(num2)
            else:
                return 'AssemBOA - Jump if Equal (' + str(self.address_space[self.prog_counter]) + '): Did not jump to line ' + str(self.prog_counter + 1) + ' because ' + str(num1) + ' !> ' + str(num2)
        except IndexError:
            self.fatal_error = True
            self.output = self.errors['NullOperand']
            return self.errors['NullOperand']
        except ValueError:
            self.fatal_error = True
            self.output = self.errors['InvalidMemReference']
            return self.errors['InvalidMemReference']

    def jeq(self, arg):
        try:
            num1 = self.stack.pop()
            num2 = self.stack.pop()
            result = num1 == num2

            if result:
                arg = int(arg)
                if arg < 0 or arg >= self.vars_max:
                    self.fatal_error = True
                    self.output = self.errors['InvalidMemReference']
                    return self.errors['InvalidMemReference']
                self.prog_counter = self.address_space[- 1 - int(arg)]
                return 'AssemBOA - Jump if Equal (' + str(self.address_space[self.prog_counter]) + '): Jumped to line ' + str(self.prog_counter + 1) + ' because ' + str(num1) + ' = ' + str(num2)
            else:
                return 'AssemBOA - Jump if Equal (' + str(self.address_space[self.prog_counter]) + '): Did not jump to line ' + str(self.prog_counter + 1) + ' because ' + str(num1) + ' != ' + str(num2)

        except IndexError:
            self.fatal_error = True
            self.output = self.errors['NullOperand']
            return self.errors['NullOperand']
        except ValueError:
            self.fatal_error = True
            self.output = self.errors['InvalidMemReference']
            return self.errors['InvalidMemReference']

    def add(self, arg):
        try:
            num1 = self.stack.pop()
            num2 = self.stack.pop()
            result = num2 + num1

            if result > 99:
                self.fatal_error = True
                self.output = self.errors['Overflow']
                return self.errors['Overflow']

            self.stack.append(result)
            return 'AssemBOA - Add (' + str(self.address_space[self.prog_counter]) + '): ' + str(num2) + ' + ' + str(num1) + ' = ' + str(result)
        except IndexError:
            self.fatal_error = True
            self.output = self.errors['NullOperand']
            return self.errors['NullOperand']

    def sub(self, arg):
        try:
            num1 = self.stack.pop()
            num2 = self.stack.pop()
            result = num2 - num1

            if result < 0:
                self.fatal_error = True
                self.output = self.errors['Overflow']
                return self.errors['Overflow']

            self.stack.append(result)
            return 'AssemBOA - Subtract (' + str(self.address_space[self.prog_counter]) + '): ' + str(num2) + ' - ' + str(num1) + ' = ' + str(result)
        except IndexError:
            self.fatal_error = True
            self.output = self.errors['NullOperand']
            return self.errors['NullOperand']

    def compare(self, arg):
        try:
            num1 = self.stack.pop()
            num2 = self.stack.pop()
            result = num2 == num1

            if result:
                self.stack.append(1)
            else:
                self.stack.append(0)
            return 'AssemBOA - Compare (' + str(self.address_space[self.prog_counter]) + '): ' + str(num2) + ' == ' + str(num1) + ' is ' + str(result)
        except IndexError:
            self.fatal_error = True
            self.output = self.errors['NullOperand']
            return self.errors['NullOperand']

    def load_to_mem(self, file_to_read):
        machine_code = open(file_to_read, 'rb')
        for idx, line in enumerate(machine_code):
            if idx >= self.code_max:
                self.output = self.errors['MaxLines']
                return self.errors['MaxLines']
            self.address_space[idx] = line.strip()

            if self.address_space[idx][0:2] == self.label_code:
                try:
                    self.address_space[- 1 - int(self.address_space[idx][2:4])] = idx
                except IndexError:
                    self.fatal_error = True
                    self.output = self.errors['WritingToReadOnlyMem']
                    return self.errors['WritingToReadOnlyMem']

            self.code_lines += 1
        return 'AssemBOA: Successfully loaded file ' + file_to_read + ' to memory.'

    def run(self, step_by_step = False):
        self.prog_counter = 0
        while self.prog_counter < self.code_lines:
            if self.fatal_error is not True:
                command = self.address_space[self.prog_counter][0:2]
                arg = self.address_space[self.prog_counter][2:4]
                
                try:
                    if step_by_step:
                        print raw_input()

                    if command != self.label_code:
                        self.output_message = self.methods_dict[command](arg)
                        self.exec_log.append('Line ' + str(self.prog_counter).zfill(2) + ' -> ' + self.output_message)
                        # self.exec_log.append(self.output_message)
                        print self.output

                except KeyError:
                    self.fatal_error = True
                    self.output = self.errors['UnknownCommand']
                    return self.errors['UnknownCommand']

                self.prog_counter += 1

            else:
                break

        return 'AssemBOA: Execution complete.'


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

        self.output_message = self.run(step_by_step)
        
