# Author: Azu
# Date: 2018-7-13 23:21
# file: VMtranslator.py
# Description: Translates hack's virtual machine code to its machine code

class VMtranslator(object):
    """
    Translates hack's VM code into its machine code
    """
    def __init__(self):
        return
    
    @staticmethod    
    def parser(file_name):
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
                asm_codes = VMtranslator.translate_arithmmic_logical_cmd(vm_command)
                asm_file.write(asm_codes + '\n')
            elif cmd_type == 'ACCESS':
                asm_codes = VMtranslator.tranlate_memory_access_cmd(vm_command)
                asm_file.write(asm_codes + '\n')
        asm_file.close()
        
    @staticmethod
    def command_type(vm_command):
        """
        Given a line of vm code, determine its command type,
        the result is either 'ACCESS' or 'ARITHMMIC'
        """
        
        if vm_command.startswith('push') or vm_command.startswith('pop'):
            return 'ACCESS'
        else:
            return 'ARITHMMIC'
    
    @staticmethod
    def tranlate_memory_access_cmd(vm_command):
        """
        Translate VM memory access command into machine code
        """
        sub_commands = vm_command.split()
        machine_code = ''    # Machine code generated
        
        # Handles constant operation
        if sub_commands[1] == 'constant':
            machine_code = VMtranslator._push_constant(sub_commands[2])
        
        return machine_code
    
    @staticmethod
    def translate_arithmmic_logical_cmd(vm_command):
        """
        Translate VM arithmmic/logical commands into corresponding machine code.
        """
        
        machine_code = ''
        if vm_command == 'add':
            machine_code += VMtranslator._pop_to_temp()
            machine_code += '@SP\n'
            machine_code += 'D=M-1\n'
            machine_code += 'A=D\n'
            machine_code += 'D=M\n'
            machine_code += '@temp\n'
            machine_code += 'D=D+M\n'
            machine_code += '@SP\n'
            machine_code += 'A=M-1\n'
            machine_code += 'M=D\n'
        if vm_command == ''
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
    def _pop_to_temp():
        """
        Generate the machine code segment for pop from top of the stack.
        And store it into variable temp
        """
        
        machine_code = '@SP\n'
        machine_code += 'M=M-1\n'
        machine_code += 'D=M\n'
        machine_code += 'A=D\n'
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
    VMtranslator.parser(file_name)
            
            
                   
            
            
        