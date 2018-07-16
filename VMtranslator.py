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
        new_file_name = file_name[:file_name.find('.') + '.asm']  # File name for generated machine code
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
            cmd_type = VMtranslator.command_type()
            if cmd_type == 'ARITHMMIC':
                asm_codes = VMtranslator.tranlate_stack_arithmmic_cmd(vm_command)
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
            
            
        