from unicorn import *
from unicorn.arm_const import *

f=open('fw.bin','rb').read()
ro=open('rom.bin','rb').read()
sr=open('sram.bin','rb').read()

def hprint(eng,addr,ln,udata):
    if eng.reg_read(UC_ARM_REG_PC) == 0x10000466:
        eng.reg_write(UC_ARM_REG_PC,0x1000046a | 1)

def hscan(eng,addr,ln,udata):
    val = int(udata).to_bytes(2,byteorder='little')
    if eng.reg_read(UC_ARM_REG_PC) == 0x1000046a:
        eng.mem_write(0x20041cb8,val)
        eng.reg_write(UC_ARM_REG_PC, 0x10000472 | 1)

def hsleep(eng,addr,ln,udata):
    if eng.reg_read(UC_ARM_REG_PC) == 0x10000476:
        eng.reg_write(UC_ARM_REG_PC,0x1000047a | 1)

def hputs(eng,addr,ln,udata):
    if eng.reg_read(UC_ARM_REG_PC) == 0x100004ba:
        return

def main(f,ro,sr):
    regs_li = [[UC_ARM_REG_R0,0x13],[UC_ARM_REG_R1,0x0],[UC_ARM_REG_R2,0x0],[UC_ARM_REG_R3,0x3],[UC_ARM_REG_R4,0x20041de8],[UC_ARM_REG_R5,0x1000d3d8],[UC_ARM_REG_R6,0x1000d3d4],[UC_ARM_REG_R7,0x1000d36c],[UC_ARM_REG_R8,0xffffffff],[UC_ARM_REG_R9,0xffffffff],[UC_ARM_REG_R10,0xffffffff],[UC_ARM_REG_R11,0xffffffff],[UC_ARM_REG_R12,0x20000231],[UC_ARM_REG_SP,0x20041de0],[UC_ARM_REG_LR,0x10000a93],[UC_ARM_REG_PC,0x10000460],[UC_ARM_REG_XPSR,0x61000000],[UC_ARM_REG_MSP,0x20041de0],[UC_ARM_REG_PSP,0xfffffffc],[UC_ARM_REG_PRIMASK,0x0],[UC_ARM_REG_BASEPRI,0x0],[UC_ARM_REG_FAULTMASK,0x0],[UC_ARM_REG_CONTROL,0x0]]

    for i in range(9999):
        eng=Uc(UC_ARCH_ARM, UC_MODE_THUMB)
        print('current pin:',i)
        base_addr=0x10000000
        eng.mem_map(base_addr,len(f))
        eng.mem_map(0x00000000,len(ro))
        eng.mem_map(0x20000000,len(sr))

        eng.mem_write(base_addr,f)
        eng.mem_write(0x00000000,ro)
        eng.mem_write(0x20000000,sr)
        for value in regs_li:
            eng.reg_write(value[0],value[1])
        try:
            eng.hook_add(UC_HOOK_CODE, hprint, begin=0x10000466, end=0x1000046a)
            eng.hook_add(UC_HOOK_CODE, hscan, begin=0x1000046a, end=0x10000472, user_data=i)
            eng.hook_add(UC_HOOK_CODE, hsleep, begin=0x10000476, end=0x1000047a)
            eng.hook_add(UC_HOOK_CODE, hputs, begin=0x1000047a, end=0x100004ba)
            eng.emu_start(0x10000460 | 1, 0x100004c0)
        except UcError as err:
            temp = eng.mem_read(0x20041ccc,38)
            if 'sshs' in str(temp):
                print('pin found:',i)
                ind = int(str(temp).find('sshs'))
                print('here is the flag: ',str(temp)[ind:ind+38])
                break
            eng.emu_stop()
            continue
main(f,ro,sr)
