
from hashlib import sha256

def balloon_hash(msg, salt, space_cost=1024, time_cost=3, dependencies=3):
    msg = msg.encode("utf-8")
    salt = salt.encode("utf-8")

    count = 0
    main_buffer = []
    
    main_buffer.append(sha256_hash(count,msg,salt))
    count += 1
    for space_i in range(1,space_cost):
        main_buffer.append(sha256_hash(count,main_buffer[space_i-1]))
        count += 1

    for time_i in range(time_cost):
        for space_i in range(space_cost):
            if space_i == 0:
                main_buffer[space_i] = sha256_hash(count,main_buffer[space_cost-1],main_buffer[space_i])
            else:
                main_buffer[space_i] = sha256_hash(count,main_buffer[space_i-1],main_buffer[space_i])
            count += 1
            for dependency_i in range(0,dependencies):
                index_block = sha256_hash(time_i,space_i,dependency_i)
                other_space_i = int.from_bytes(sha256_hash(count,salt,index_block),"little")%space_cost
                count += 1
                main_buffer[space_i] = sha256_hash(count,main_buffer[space_i],main_buffer[other_space_i])
                count += 1

    return main_buffer[-1].hex()

def sha256_hash(*args):
    t = b''
    for arg in args:
        if type(arg) is int:
            t += arg.to_bytes(8, "little")
        elif type(arg) is str:
            t += arg.encode('utf-8')
        else:
            t += arg
    return sha256(t).digest()
