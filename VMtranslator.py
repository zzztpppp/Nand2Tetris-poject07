# Author: Azu
# Date: 2018-7-13 23:21
# file: VMtranslator.py
# Description: Translates hack's virtual machine code to its machine code

class VMtranslator(object):
    """
    Translates hack's VM code into its machine code
    """
    def __init__(self):
        self.num_operation = 0
        return
    
      
    def parser(self, file_name):
        """
        Parse lines of VM code into machine code
        and save them into a text file.
        """
        # Read the given VM code
        vm_file = open(file_name, 'r')
        vm_commands = vm_file.readlines()
        vm_file.close()
        
        # Generate machine code and write into new file.
        new_file_name = file_name[:file_name.find('.')] + '.asm'  # File name for generated machine code
        asm_file = open(new_file_name, 'w')
        for vm_command in vm_commands:
            vm_command = vm_command.strip()
            # Ignore comments and empty lines
            if vm_command.startswith('//'):
                continue
            if vm_command == '':
                continue
            if vm_command == '\n':
                continue
                
            # Detemine a command's type and tranlate
            cmd_type = VMtranslator.command_type(vm_command)
            if cmd_type == 'ARITHMMIC':
                asm_codes = self.translate_arithmmic_logical_cmd(vm_command)
                asm_file.write(asm_codes + '\n')
            elif cmd_type == 'ACCESS':
                asm_codes = self.tranlate_memory_access_cmd(vm_command)
                asm_file.write(asm_codes + '\n')
        asm_file.close()
        
    def command_type(vm_command):
        """
        Given a line of vm code, determine its command type,
        the result is either 'ACCESS' or 'ARITHMMIC'
        """
        
        if vm_command.startswith('push') or vm_command.startswith('pop'):
            return 'ACCESS'
        else:
            return 'ARITHMMIC'
    
    def tranlate_memory_access_cmd(self, vm_command):
        """
        Translate VM memory access command into machine code
        """
        sub_commands = vm_command.split()
        machine_code = ''    # Machine code generated
        
        # Handles constant operation
        if sub_commands[1] == 'constant':
            machine_code = VMtranslator._push_constant(sub_commands[2])
        if sub_commands[1] == 'local' or sub_commands[1] == 'argument' or sub_commands[1] == 'this' or sub_commands[1] == 'that' or sub_commands[1] == 'temp' or sub_commands[1] == 'pointer' or sub_commands[1] == 'static':
            machine_code += VMtranslator._handle_basic_memory_access(sub_commands)
        
        return machine_code
    

    def translate_arithmmic_logical_cmd(self, vm_command):
        """
        Translate VM arithmmic/logical commands into corresponding machine code.
        """
        self.num_operation += 1
        
        machine_code = ''
        if vm_command == 'add':
            machine_code += VMtranslator._pop_to_temp()
            machine_code += '@SP\n'
            machine_code += 'A=M-1\n'
            machine_code += 'D=M\n'
            machine_code += '@temp\n'
            machine_code += 'D=D+M\n'
            machine_code += '@SP\n'
            machine_code += 'A=M-1\n'
            machine_code += 'M=D\n'
        if vm_command == 'sub':
            machine_code += VMtranslator._pop_to_temp()
            machine_code += '@SP\n'
            machine_code += 'A=M-1\n'
            machine_code += 'D=M\n'
            machine_code += '@temp\n'
            machine_code += 'D=D-M\n'
            machine_code += '@SP\n'
            machine_code += 'A=M-1\n'
            machine_code += 'M=D\n'
        if vm_command == 'neg':
            machine_code += '@SP\n'
            machine_code += 'A=M-1\n'
            machine_code += 'M=-M\n'
        if vm_command == 'not':
            machine_code += '@SP\n'
            machine_code += 'A=M-1\n'
            machine_code += 'M=!M\n'
        if vm_command == 'and':
            machine_code += VMtranslator._pop_to_temp()
            machine_code += '@SP\n'
            machine_code += 'A=M-1\n'
            machine_code += 'D=M\n'
            machine_code += '@temp\n'
            machine_code += 'D=D&M\n'
            machine_code += '@SP\n'
            machine_code += 'A=M-1\n'
            machine_code += 'M=D\n'
        if vm_command == 'or':
            machine_code += VMtranslator._pop_to_temp()
            machine_code += '@SP\n'
            machine_code += 'A=M-1\n'
            machine_code += 'D=M\n'
            machine_code += '@temp\n'
            machine_code += 'D=D|M\n'
            machine_code += '@SP\n'
            machine_code += 'A=M-1\n'
            machine_code += 'M=D\n'
        if vm_command == 'eq' or vm_command == 'gt' or vm_command == 'lt':
            machine_code += VMtranslator._pop_to_temp()
            machine_code += '@SP\n'
            machine_code += 'A=M-1\n'
            machine_code += 'D=M\n'
            machine_code += '@temp\n'
            machine_code += 'D=D-M\n'
            machine_code += '@SP\n'
            machine_code += 'A=M-1\n'
            machine_code += 'M=0\n'
            
            if vm_command == 'eq':
                machine_code += '@EQUAL{}\n'.format(self.num_operation)
                machine_code += 'D;JEQ\n'
                machine_code += '@ENDEQ{}\n'.format(self.num_operation)
                machine_code += '0;JMP\n'
                
                machine_code += '(EQUAL{})\n'.format(self.num_operation)
                machine_code += '@SP\n'
                machine_code += 'A=M-1\n'
                machine_code += 'M=-1\n'
                machine_code += '@ENDEQ{}\n'.format(self.num_operation)
                machine_code += '0;JMP\n'
                machine_code += '(ENDEQ{})\n'.format(self.num_operation)
            if vm_command == 'gt':
                machine_code += '@GREATER{}\n'.format(self.num_operation)
                machine_code += 'D;JGT\n'
                machine_code += '@ENDGT{}\n'.format(self.num_operation)
                machine_code += '0;JMP\n'
                
                machine_code += '(GREATER{})\n'.format(self.num_operation)
                machine_code += '@SP\n'
                machine_code += 'A=M-1\n'
                machine_code += 'M=-1\n'
                machine_code += '@ENDGT{}\n'.format(self.num_operation)
                machine_code += '0;JMP\n'
                machine_code += '(ENDGT{})\n'.format(self.num_operation)
            
            if vm_command == 'lt':
                machine_code += '@LESS{}\n'.format(self.num_operation)
                machine_code += 'D;JLT\n'
                machine_code += '@ENDLT{}\n'.format(self.num_operation)
                machine_code += '0;JMP\n'
                
                machine_code += '(LESS{})\n'.format(self.num_operation)
                machine_code += '@SP\n'
                machine_code += 'A=M-1\n'
                machine_code += 'M=-1\n'
                machine_code += '@ENDLT{}\n'.format(self.num_operation)
                machine_code += '0;JMP\n'
                machine_code += '(ENDLT{})\n'.format(self.num_operation)
            
            
        return machine_code
       
    
    @staticmethod
    def _push_constant(number):
        """
        Push a constant into the stack
        """
        machine_code = '@{}\n'.format(number)
        machine_code += 'D=A\n'
        machine_code += '@SP\n'
        machine_code += 'A=M\n'
        machine_code += 'M=D\n'
        machine_code += '@SP\n'
        machine_code += 'M=M+1\n'
        
        return machine_code
        
    @staticmethod
    def _handle_basic_memory_access(sub_commands):
        map = {'local': 'LCL', 'argument': 'ARG', 'this': 'THIS', 'that': 'THAT', 'temp': '5', 
               'static': '16', 'pointer': '3'}
        machine_code = ''
        if sub_commands[0] == 'push':
            if sub_commands[1] == 'temp' or sub_commands[1] == 'static' or sub_commands[1] == 'pointer':
                machine_code += '@{}\n'.format(map[sub_commands[1]])
                machine_code += 'D=A\n'
            else: 
                machine_code += '@{}\n'.format(map[sub_commands[1]])
                machine_code += 'D=M\n'                
            machine_code += '@{}\n'.format(sub_commands[2])
            machine_code += 'A=A+D\n'
            machine_code += 'D=M\n'
            machine_code += '@SP\n'
            machine_code += 'A=M\n'
            machine_code += 'M=D\n'
            machine_code += '@SP\n'
            machine_code += 'M=M+1'
        if sub_commands[0] == 'pop':
            machine_code += VMtranslator._pop_to_temp()
            if sub_commands[1] == 'temp' or sub_commands[1] == 'static' or sub_commands[1] == 'pointer':
                machine_code += '@{}\n'.format(map[sub_commands[1]])
                machine_code += 'D=A\n'
            else:
                machine_code += '@{}\n'.format(map[sub_commands[1]])
                machine_code += 'D=M\n'
            machine_code += '@{}\n'.format(sub_commands[2])
            machine_code += 'D=D+A\n'
            machine_code += '@tempaddr\n'
            machine_code += 'M=D\n'
            machine_code += '@temp\n'
            machine_code += 'D=M\n'
            machine_code += '@tempaddr\n'
            machine_code += 'A=M\n'
            machine_code += 'M=D\n'
        
        return machine_code
        
    @staticmethod
    def _pop_to_temp():
        """
        Generate the machine code segment for pop from top of the stack.
        And store it into variable temp
        """
        
        machine_code = '@SP\n'
        machine_code += 'AM=M-1\n'
        machine_code += 'D=M\n'
        machine_code += '@temp\n'
        machine_code += 'M=D\n'
        
        
        return machine_code
    
    @staticmethod
    def command_type(vm_command):
        if vm_command.startswith('push') or vm_command.startswith('pop'):
            return 'ACCESS'
        else:
            return 'ARITHMMIC'
            

if __name__ == '__main__':
    import sys
    file_name = sys.argv[1]
    # print(file_name)
    vm = VMtranslator()
    vm.parser(file_name)
            
            
                   
            
            
        