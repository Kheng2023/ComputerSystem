class VMTranslator:

    label_counter=0
    return_counter=0

    def push_stack():
        '''Generate Hack Assembly code for pushing a value from a segment onto the stack'''
        result = "@SP\n"
        result += "AM=M+1\n"
        result += "A=A-1\n"
        result += "M=D\n"
        return result

    def pop_stack():
        '''Generate Hack Assembly code for popping a value from a stack'''
        result = "@SP\n"
        result += "AM=M-1\n"
        result += "D=M\n"
        return result

    def vm_push(segment, offset):
        '''Generate Hack Assembly code for a VM push operation'''
        result=""
        if segment == "constant":
            result += "@" + str(offset) + "\n"
            result += "D=A\n"
        elif segment == "static":
            result += "@" + str(16+offset) + "\n"
            result += "D=M\n"
        elif segment == "temp":
            result += "@" + str(5+offset) + "\n"
            result += "D=M\n"
        elif segment == "pointer":
            if offset == 0:
                base_address = "THIS"
            elif offset == 1:
                base_address = "THAT"
            result += "@" + base_address + "\n"
            result += "D=M\n"
        else:
            if segment == "local":
                base_address = "LCL"
            elif segment == "argument":
                base_address = "ARG"
            elif segment == "this":
                base_address = "THIS"
            elif segment == "that":
                base_address = "THAT"
            result += "@"+str(offset)+"\n"
            result += "D=A\n"
            result += "@"+base_address+"\n"
            result += "A=D+M\n"
            result += "D=M\n"

        result += VMTranslator.push_stack()

        return result.strip()

    def vm_pop(segment, offset):
        '''Generate Hack Assembly code for a VM pop operation'''
        result=""
        if segment == "static":
            result += VMTranslator.pop_stack()
            result += "@" + str(16+offset) + "\n"
            result += "M=D"
        elif segment == "temp":
            result += VMTranslator.pop_stack()
            result += "@" + str(5+offset) + "\n"
            result += "M=D"
        elif segment == "pointer":
            if offset == 0:
                base_address = "THIS"
            elif offset == 1:
                base_address = "THAT"
            result += VMTranslator.pop_stack()
            result += "@" + base_address + "\n"
            result += "M=D"
        else:
            if segment == "local":
                base_address = "LCL"
            elif segment == "argument":
                base_address = "ARG"
            elif segment == "this":
                base_address = "THIS"
            elif segment == "that":
                base_address = "THAT"
            result += "@"+str(offset)+"\n"
            result += "D=A\n"
            result += "@"+base_address+"\n"
            result += "D=D+M\n"
            result += "@15\n"
            result += "M=D\n" #temporary save address
            result += VMTranslator.pop_stack()
            result += "@15\n"
            result += "A=M\n"
            result += "M=D"

        return result

    def vm_add():
        '''Generate Hack Assembly code for a VM add operation'''
        result=""
        result += VMTranslator.pop_stack()
        result += "A=A-1\n"
        result += "M=M+D"
        return result

    def vm_sub():
        '''Generate Hack Assembly code for a VM sub operation'''
        result=""
        result += VMTranslator.pop_stack()
        result += "A=A-1\n"
        result += "M=M-D"
        return result

    def vm_neg():
        '''Generate Hack Assembly code for a VM neg operation'''
        result=""
        result += "@SP\n"
        result += "A=M-1\n"
        result += "M=-M"
        return result

    def vm_eq():
        '''Generate Hack Assembly code for a VM eq operation'''
        result=""
        result += VMTranslator.pop_stack()
        result += "A=A-1\n"
        result += "D=M-D\n"
        result += f"@EQ_TRUE_{VMTranslator.label_counter}\n"
        result += "D;JEQ\n"
        result += "D=0\n"
        result += f"@EQ_FALSE_{VMTranslator.label_counter}\n"
        result += "0;JMP\n"
        result += f"(EQ_TRUE_{VMTranslator.label_counter})\n"
        result += "D=-1\n"
        result += f"(EQ_FALSE_{VMTranslator.label_counter})\n"
        result += "@SP\n"
        result += "A=M-1\n"
        result += "M=D"
        VMTranslator.label_counter += 1  # Increment label counter to ensure uniqueness
        return result

    def vm_gt():
        '''Generate Hack Assembly code for a VM gt operation'''
        result=""
        result += VMTranslator.pop_stack()
        result += "A=A-1\n"
        result += "D=M-D\n"
        result += f"@EQ_TRUE_{VMTranslator.label_counter}\n"
        result += "D;JGT\n"
        result += "D=0\n"
        result += f"@EQ_FALSE_{VMTranslator.label_counter}\n"
        result += "0;JMP\n"
        result += f"(EQ_TRUE_{VMTranslator.label_counter})\n"
        result += "D=-1\n"
        result += f"(EQ_FALSE_{VMTranslator.label_counter})\n"
        result += "@SP\n"
        result += "A=M-1\n"
        result += "M=D"
        VMTranslator.label_counter += 1  # Increment label counter to ensure uniqueness
        return result

    def vm_lt():
        '''Generate Hack Assembly code for a VM lt operation'''
        result=""
        result += VMTranslator.pop_stack()
        result += "A=A-1\n"
        result += "D=M-D\n"
        result += f"@EQ_TRUE_{VMTranslator.label_counter}\n"
        result += "D;JLT\n"
        result += "D=0\n"
        result += f"@EQ_FALSE_{VMTranslator.label_counter}\n"
        result += "0;JMP\n"
        result += f"(EQ_TRUE_{VMTranslator.label_counter})\n"
        result += "D=-1\n"
        result += f"(EQ_FALSE_{VMTranslator.label_counter})\n"
        result += "@SP\n"
        result += "A=M-1\n"
        result += "M=D"
        VMTranslator.label_counter += 1  # Increment label counter to ensure uniqueness
        return result

    def vm_and():
        '''Generate Hack Assembly code for a VM and operation'''
        result=""
        result += VMTranslator.pop_stack()
        result += "A=A-1\n"
        result += "M=D&M"
        return result

    def vm_or():
        '''Generate Hack Assembly code for a VM or operation'''
        result=""
        result += VMTranslator.pop_stack()
        result += "A=A-1\n"
        result += "M=D|M"
        return result

    def vm_not():
        '''Generate Hack Assembly code for a VM not operation'''
        result=""
        result += "@SP\n"
        result += "A=M-1\n"
        result += "M=!M"
        return result

    def vm_label(label):
        '''Generate Hack Assembly code for a VM label operation'''
        result = "("+label+")"
        return result

    def vm_goto(label):
        '''Generate Hack Assembly code for a VM goto operation'''
        result=""
        result += "@"+label+"\n"
        result += "0;JMP"
        return result

    def vm_if(label):
        '''Generate Hack Assembly code for a VM if-goto operation'''
        result = VMTranslator.pop_stack()
        result += "@"+label+"\n"
        result += "D;JNE"
        return result

    def vm_function(function_name, n_vars):
        '''Generate Hack Assembly code for a VM function operation'''
        result = "("+function_name+")\n"
        for i in range(n_vars):
            result += "@SP\n"
            result += "AM=M+1\n"
            result += "A=A-1\n"
            result += "M=0\n"
        return result.strip()

    def vm_call(function_name, n_args):
        '''Generate Hack Assembly code for a VM call operation'''
        result=""
        # Generate a unique label for the return address
        return_label = f"retAddr_{VMTranslator.return_counter}"
          
        # Push the return address onto the stack
        result += f"@{return_label}\n"
        result += "D=A\n"
        result += VMTranslator.push_stack()

        # Push LCL, ARG, THIS, and THAT onto the stack
        segments = ['LCL', 'ARG', 'THIS', 'THAT']
        for i in segments:
            result += "@"+i+"\n"
            result += "D=M\n"
            result += VMTranslator.push_stack()

        # Reposition ARG for the called function
        result += "@SP\n"
        result += "D=M\n"
        result += "@"+str(n_args + 5)+"\n"  # 5 = Number of standard segments
        result += "D=D-A\n"
        result += "@ARG\n"
        result += "M=D\n"

        #LCL = SP (repositions LCL)
        result += "@SP\n"
        result += "D=M\n"
        result += "@LCL\n"
        result += "M=D\n"

        #goto function_name - transfer control to the callee
        result += "@"+function_name+"\n"
        result += "0;JMP\n"

        #(return address) injects the return address label into the code
        result += "("+return_label+")"

        # Increment return label counter for uniqueness
        VMTranslator.return_counter += 1

        return result.strip()

    def vm_return():
        '''Generate Hack Assembly code for a VM return operation'''
        result=""
        #frame=LCL -- frame is a temporary variable
        #return_address = *(frame-5) -- puts the return address in a temporary variable
        result += "@5\n" 
        result += "D=A\n"
        result += "@LCL\n"
        result += "A=M-D\n"
        result += "D=M\n"
        result += "@15\n" 
        result += "M=D\n"

        #*ARG=pop() -- repositions the return value for the caller
        result += VMTranslator.pop_stack()
        result += "@ARG\n"
        result += "A=M\n"
        result += "M=D\n"

        #SP=ARG+1 -- repositions the SP for the caller
        result += "D=A+1\n"
        result += "@SP\n"
        result += "M=D\n"

        # Restore THAT, THIS, ARG, and LCL for the caller
        segments = ['THAT', 'THIS', 'ARG', 'LCL']
        for segment in segments:
            result += "@LCL\n"
            result += "AM=M-1\n"
            result += "D=M\n"
            result += f"@{segment}\n"
            result += "M=D\n"

        #goto return_address -- go to the return address
        result += "@R15\n"     # Load return address from R15
        result += "A=M\n"      # Jump to the return address
        result += "0;JMP"

        return result

# A quick-and-dirty parser when run as a standalone script.
if __name__ == "__main__":
    import sys
    if(len(sys.argv) > 1):
        #output_file_name = sys.argv[1].replace(".vm", ".asm")
        #sys.stdout = open(output_file_name, "w")
        with open(sys.argv[1], "r") as a_file:
            for line in a_file:
                tokens = line.strip().lower().split()
                if(len(tokens)==1):
                    if(tokens[0]=='add'):
                        print(VMTranslator.vm_add())
                    elif(tokens[0]=='sub'):
                        print(VMTranslator.vm_sub())
                    elif(tokens[0]=='neg'):
                        print(VMTranslator.vm_neg())
                    elif(tokens[0]=='eq'):
                        print(VMTranslator.vm_eq())
                    elif(tokens[0]=='gt'):
                        print(VMTranslator.vm_gt())
                    elif(tokens[0]=='lt'):
                        print(VMTranslator.vm_lt())
                    elif(tokens[0]=='and'):
                        print(VMTranslator.vm_and())
                    elif(tokens[0]=='or'):
                        print(VMTranslator.vm_or())
                    elif(tokens[0]=='not'):
                        print(VMTranslator.vm_not())
                    elif(tokens[0]=='return'):
                        print(VMTranslator.vm_return())
                elif(len(tokens)==2):
                    if(tokens[0]=='label'):
                        print(VMTranslator.vm_label(tokens[1]))
                    elif(tokens[0]=='goto'):
                        print(VMTranslator.vm_goto(tokens[1]))
                    elif(tokens[0]=='if-goto'):
                        print(VMTranslator.vm_if(tokens[1]))
                elif(len(tokens)==3):
                    if(tokens[0]=='push'):
                        print(VMTranslator.vm_push(tokens[1],int(tokens[2])))
                    elif(tokens[0]=='pop'):
                        print(VMTranslator.vm_pop(tokens[1],int(tokens[2])))
                    elif(tokens[0]=='function'):
                        print(VMTranslator.vm_function(tokens[1],int(tokens[2])))
                    elif(tokens[0]=='call'):
                        print(VMTranslator.vm_call(tokens[1],int(tokens[2])))
    #sys.stdout.close()